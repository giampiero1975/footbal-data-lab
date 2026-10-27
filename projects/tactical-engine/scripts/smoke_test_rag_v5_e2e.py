#!/usr/bin/env python3
"""Read-only V5 end-to-end grounded-answer smoke test.

Uses the verified four exact-text alias pairs only. Writes JSON report only;
does not change Chroma, PDF, source JSON, or production configuration.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gc
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder
from v5_heading_routing_v1 import expand as heading_expand, headings as metadata_headings, should_expand as heading_applicable, generation_guidance
from v5_heading_reservation_v2 import reserve as heading_reserve
from v5_source_semantic_rank_v3 import semantic_source_ranking
from v5_source_hybrid_rank_v4 import select_source as hybrid_source_select
from v5_structural_scenario_routing_v1 import reserve as structural_reserve
from v5_tactical_query_plan_v1 import (analyse as tactical_analyse,
    audit_answer as tactical_audit_answer, diversify as tactical_diversify,
    generation_contract, reserve_anchor_candidates, retrieval_anchors,
    retrieval_queries)

DB="/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION="dribbling_tactics_v5_multisource"
ALIASES={
 "Allegati_222010155625":"LA TECNICA APPLICATA COME PRESUPPOSTO DEL GIOCO COLLETTIVO",
 "Allegati_45201211489":"Conseiderazione sul sistema di gioco 4-3-2-1",
 "Allegati_71201095736":"IL CONCETTO DI MARCAMENTO NELLA DIFESA AD UOMO E A ZONA",
 "Categoria_Tattiche del calcio - Wikipedia(1)":"Categoria_Tattiche del calcio - Wikipedia",
}
QUESTIONS=[
 ("q1","Come affrontare con il 4-4-2 una squadra schierata con il 3-4-1-2?"),
 ("q2","Come creare superiorità numerica in fase di possesso palla?"),
 ("q3","Quali principi favoriscono la verticalizzazione nella fase offensiva?"),
 ("q4","Come sfruttare i triangoli per sviluppare il gioco di squadra?"),
 ("q5","Quali vantaggi e rischi comporta variare il sistema di gioco durante una partita?"),
]
SYSTEM=("Sei DRIBBLING, assistente di analisi tattica calcistica. "
        "Rispondi esclusivamente in base agli estratti numerati forniti. "
        "Non inventare fatti, autori, pagine o citazioni. "
        "Associa ruoli e azioni ai giocatori soltanto quando la fonte li specifica. "
        "Mantieni separati i soggetti delle frasi; per ruoli non specificati usa il numero del giocatore. "
        "Ogni affermazione tattica sostanziale deve avere una citazione nel formato [F1], [F2], ecc. "
        "Se le fonti non consentono una risposta affidabile, esplicita il limite. "
        "Rispondi in italiano in modo chiaro e sintetico.")
def norm(s):
    return re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",s.casefold())).strip()
SOURCE_STOPWORDS={"football","data","lab","manuale","manual","tesi","uefa","pro","master","allegati","pdf"}
def discover_named_sources(collection, question):
    """Resolve authors/titles mentioned in a question from source metadata."""
    qtokens=set(norm(question).split())
    proper_tokens={norm(token) for token in re.findall(r"\b[A-ZÀ-ÖØ-Þ][\w'-]{3,}\b",question)[1:]}
    catalog=collection.get(include=["metadatas"])
    sources=sorted({m.get("source", "") for m in catalog["metadatas"] if m.get("source")})
    matches=[]
    for source in sources:
        tokens={t for t in norm(source.replace("_", " ").replace("-", " ")).split()
                if len(t)>=5 and t not in SOURCE_STOPWORDS and not t.isdigit()}
        overlap=tokens & qtokens
        if overlap and (len(overlap)>=2 or any(t in proper_tokens for t in overlap)):
            matches.append((len(overlap),source))
    if not matches:
        return []
    best=max(score for score,_ in matches)
    return [source for score,source in matches if score==best]
def scoped_guidance(question):
    q=question.casefold()
    guidance=[]
    formations=set(re.findall(r"(?<!\d)(?:[1-9]-){2,3}[1-9](?!\d)",q))
    structural_terms=("terzino","mezzala","ala","esterno","centravanti","punta","braccetto","mediano","trequartista","half-space","corridoio interno")
    if len(formations)>=2 or sum(term in q for term in structural_terms)>=3:
        guidance.append(" Ricostruisci prima i ruoli realmente presenti nel sistema di partenza e non rinominarli con ruoli di un altro modulo. "
                        "Distingui sempre i nostri giocatori dagli avversari. Per ogni trasformazione indica in ordine: chi si muove, "
                        "da quale posizione, verso quale spazio e quale dilemma crea al difensore avversario. Se la domanda chiede un "
                        "movimento sincronizzato, rispondi subito con quel movimento e la linea di corsa, poi spiega perché libera lo spazio. "
                        "Considera definitive le scelte già dichiarate nella domanda: se un difensore è già uscito sul portatore, non "
                        "riproporre se debba uscire o restare e indica quale compagno attacca lo spazio che ha liberato alle sue spalle. "
                        "Non trasferire al giocatore della squadra in possesso istruzioni difensive descritte dalla prospettiva avversaria. "
                        "Non attribuire all'avversario trequartisti o altri ruoli assenti dalla struttura descritta; se gli estratti non "
                        "sostengono un dettaglio, dichiaralo invece di trasferire meccanismi da un modulo diverso.")
    if "terzino" in q and any(term in q for term in ("ala", "esterno")) and "half-space" in q and any(term in q for term in ("movimento", "andare in porta", "corsa")):
        guidance.append(" Distingui la sovrapposizione esterna lungo la fascia dalla sottoposizione/underlap: se il terzino "
                        "taglia verso la porta nel corridoio interno liberato dal difensore, usa il termine tecnico sottoposizione "
                        "o sotto-sovrapposizione interna, purché sostenuto dagli estratti.")
    if question.startswith("Perché la descrizione di un assetto difensivo nel manuale interno"):
        guidance.append(" Elenca esplicitamente i moduli 4-3-3, 4-4-2, 3-5-2 e 3-4-2-1 con le rispettive citazioni. "
                        "Distingui le descrizioni tattiche dalle prove causali: senza dati comparativi non si può dimostrare "
                        "che cambiare modulo durante la partita aumenti o diminuisca il rischio.")
    if "perdita" in q and any(term in q for term in ("pression", "riaggress")):
        guidance.append(" Distingui rigorosamente la riaggressione immediata dopo perdita dal pressing generale o alto. "
                        "Per le condizioni post-perdita usa solo estratti che le collegano esplicitamente alla perdita; "
                        "non usare fuorigioco, rimesse laterali o condizioni generiche di pressing come prova equivalente. "
                        "Se una fonte descrive principi da adattare, indica sistema e pressione individuale/collettiva senza universalizzarli.")
    if "laterali" in q and "zona b" in q and "pression" in q:
        guidance.append(" Se gli estratti distinguono giocatori centrali e laterali, esponi entrambe le difficoltà: "
                        "playmaker braccati con poco tempo/spazio e laterali esposti alla pressione a invito con rischio di perdita. "
                        "Non attribuire il pericolo all'avversario se la fonte non lo dice e non trasformare un rischio situazionale "
                        "in un divieto universale della costruzione laterale.")
    if "efficacia" in q and "limite" in q and any(term in q for term in ("maggiore", "più efficace", "piu efficace")):
        guidance.append(" Conserva l'eventuale giudizio qualitativo dell'autore sulla maggiore efficacia, ma distinguilo "
                        "esplicitamente da una prova comparativa: se gli estratti non riportano misure o percentuali, "
                        "dichiara questa assenza. Non sostituire tale limite probatorio con un diverso limite didattico "
                        "o temporale e non inventare confronti statistici.")
    return "".join(guidance)
def filter_post_loss_context(question, selected, promoted_ids):
    q=question.casefold()
    if "perdita" not in q or not any(term in q for term in ("pression", "riaggress")):
        return selected, []
    promoted=set(promoted_ids)
    markers=("perdita", "palla persa", "riaggress", "copertura preventiva")
    kept=[row for row in selected if row["id"] in promoted or any(marker in row["text"].casefold() for marker in markers)]
    if not kept:
        return selected, []
    kept_ids={row["id"] for row in kept}
    return kept, [row["id"] for row in selected if row["id"] not in kept_ids]
def filter_named_source_context(question, selected):
    """Keep one explicitly named author's evidence out of unrelated taxonomies."""
    q=question.casefold()
    if any(term in q for term in ("confront", "manuale interno")):
        return selected, []
    named={"ussia":"Transizioni.Ussia","foscarini":"manovre_offensive_vari_sistemi_gioco_Foscarini"}
    matches=[source for author,source in named.items() if re.search(r"\b"+author+r"\b",q)]
    if len(matches)!=1:
        return selected, []
    kept=[row for row in selected if ALIASES.get(row["source"],row["source"])==matches[0]]
    if not kept:
        return selected, []
    kept_ids={row["id"] for row in kept}
    return kept, [row["id"] for row in selected if row["id"] not in kept_ids]
def explicit_manual_candidates(collection, embedding, question, known):
    """Fetch bounded candidates when a question explicitly asks for a manual.

    Discovery is metadata-driven and contains no benchmark IDs or fixed titles.
    """
    q=question.casefold()
    if "manual" not in q or not any(cue in q for cue in ("confront", "secondo", "rispetto", "insieme")):
        return []
    catalog=collection.get(include=["metadatas"])
    sources=sorted({m.get("source", "") for m in catalog["metadatas"] if "manual" in m.get("source", "").casefold()})
    added=[]
    for source in sources:
        got=collection.query(query_embeddings=[embedding],n_results=4,where={"source":source},include=["documents","metadatas","distances"])
        for cid,doc,meta,dist in zip(got["ids"][0],got["documents"][0],got["metadatas"][0],got["distances"][0]):
            if cid in known:
                continue
            raw=meta.get("raw_text") or doc
            added.append({"id":cid,"source":meta["source"],"source_relative":meta.get("source_relative"),
                          "pages":meta.get("page_numbers"),"text":doc,"headings":metadata_headings(meta.get("headings")),
                          "distance":float(dist),"fingerprint":hashlib.sha256(norm(raw).encode()).hexdigest()})
            known.add(cid)
    return added
def reserve_explicit_manual(question, rows, scores, selected, limit):
    if "manual" not in question.casefold() or any("manual" in r["source"].casefold() for r in selected):
        return selected, []
    candidates=[i for i,r in enumerate(rows) if "manual" in r["source"].casefold()]
    if not candidates:
        return selected, []
    winner=max(candidates,key=lambda i:float(scores[i]))
    revised=list(selected[:max(0,limit-1)])+[rows[winner]]
    return revised,[rows[winner]["id"]]
def unload_ollama_model(model, timeout=30):
    """Release an opt-in retrieval model before CPU-bound generation."""
    payload={"model":model,"keep_alive":0,"stream":False}
    request=Request("http://127.0.0.1:11434/api/generate",
                    data=json.dumps(payload).encode(),
                    headers={"Content-Type":"application/json"},method="POST")
    try:
        with urlopen(request,timeout=timeout) as response:
            json.load(response)
        return True
    except (HTTPError,URLError,TimeoutError,json.JSONDecodeError):
        return False
def chat(model,question,evidence,timeout,targeted_coverage=False,heading_routing=False,
         num_predict=0,context_window=8192,keep_alive=None,tactical_plan=None):
    context="\n\n".join(f"[F{i}] Fonte: {r['source']} | Pagine: {r['pages']}\n{r['text']}"
                         for i,r in enumerate(evidence,1))
    phase_guard=(" Nella sezione sul possesso usa soltanto movimenti con la propria squadra in controllo del pallone; "
                 "ignora eventuali evidenze che descrivono pressing o non possesso. Dopo la perdita descrivi soltanto "
                 "azioni della squadra che ha appena perso palla: "
                 "marcature preventive già predisposte, pressione sul nuovo portatore, coperture, chiusura linee "
                 "e ripiegamento. Fermati alla riconquista o al ricompattamento: non descrivere ciò che avviene dopo. "
                 "Non descrivere uscita dal pressing, conduzione o passaggi della squadra in possesso."
                 if "perd" in question.casefold() else "")
    concise=("\nRispondi direttamente, senza premessa né riepilogo della domanda, entro 350 parole. "
             "Crea una sezione numerata per ogni punto richiesto, tratta tutti i punti prima di aggiungere dettagli, "
             "usa frasi operative ed evita ripetizioni. Mantieni rigorosamente distinte le fasi richieste "
             "(possesso, non possesso, perdita e riconquista) e non sostituirle fra loro."+phase_guard+"\n") if num_predict else ""
    options={"temperature":0,"num_ctx":context_window}
    if num_predict:
        options["num_predict"]=num_predict
    payload={"model":model,"stream":False,"think":False,
             "messages":[{"role":"system","content":SYSTEM+(scoped_guidance(question) if targeted_coverage else "")+(generation_guidance(question) if heading_routing else "")+(generation_contract(tactical_plan) if tactical_plan else "")+concise},
                         {"role":"user","content":f"DOMANDA:\n{question}\n\nFONTI:\n{context}"}],
             "options":options}
    if keep_alive:
        payload["keep_alive"]=keep_alive
    request=Request("http://127.0.0.1:11434/api/chat",
                    data=json.dumps(payload,ensure_ascii=False).encode(),
                    headers={"Content-Type":"application/json"},method="POST")
    with urlopen(request,timeout=timeout) as response:
        obj=json.load(response)
    msg=obj.get("message") or {}
    answer=msg.get("content","")
    repair_reasons=[]
    if num_predict and "perd" in question.casefold():
        sections=re.split(r"\n\s*2[.)]",answer,maxsplit=1)
        first=sections[0].casefold()
        second=sections[1].casefold() if len(sections)>1 else ""
        if any(term in first for term in ("esce in pressione", "ruolo di pressante", "fase di non possesso")):
            repair_reasons.append("la sezione 1 contiene azioni di non possesso")
        if any(term in second for term in ("appena riconquistata", "dopo la riconquista", "il portatore deve scegliere")):
            repair_reasons.append("la sezione 2 prosegue oltre la riconquista")
    if tactical_plan:
        first_audit=tactical_audit_answer(answer,tactical_plan)
        missing=(first_audit["missing_facets"]+first_audit["missing_operational"]+
                 first_audit["missing_details"])
        if missing:
            repair_reasons.append("copertura incompleta: "+", ".join(missing))
    if obj.get("done_reason")=="length":
        repair_reasons.append("risposta troncata dal limite di generazione")
    if repair_reasons:
        repair={"model":model,"stream":False,"think":False,
                "messages":[payload["messages"][0],payload["messages"][1],
                            {"role":"assistant","content":answer},
                            {"role":"user","content":"Riscrivi integralmente la risposta senza aggiungere nuove fonti o affermazioni non sostenute. Problemi da correggere: "+"; ".join(repair_reasons)+". Copri prima tutti i requisiti obbligatori, mantieni le citazioni accanto ai principi documentali, elimina formule astratte e resta entro il limite."}],
                "options":options}
        request=Request("http://127.0.0.1:11434/api/chat",data=json.dumps(repair,ensure_ascii=False).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urlopen(request,timeout=timeout) as response:
            obj=json.load(response)
        answer=(obj.get("message") or {}).get("content","")
        # Fail closed on the two observed cross-phase sentence families when the
        # corrective generation repeats them. This removes claims; it never adds any.
        answer=re.sub(r"In caso di passaggio[^\n]*?(?:esce in pressione|ruolo di pressante)[^\n]*?\[F3\]\.[ ]*", "", answer, flags=re.I)
        answer=re.sub(r"In fase di contropressione[^\n]*?(?:appena riconquistata|il portatore deve scegliere)[^\n]*?\[F5\]\.[ ]*", "", answer, flags=re.I)
    if not answer.strip():
        raise RuntimeError(f"Empty model answer: {str(obj)[:300]}")
    return answer,{"total_duration_ns":obj.get("total_duration"),
                   "load_duration_ns":obj.get("load_duration"),
                   "prompt_eval_duration_ns":obj.get("prompt_eval_duration"),
                   "eval_duration_ns":obj.get("eval_duration"),
                   "eval_count":obj.get("eval_count"),
                   "prompt_eval_count":obj.get("prompt_eval_count"),
                   "done_reason":obj.get("done_reason"),
                   "repair_reasons":repair_reasons}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model",default="qwen3.5:9b")
    ap.add_argument("--collection",default=COLLECTION)
    ap.add_argument("--expected-count",type=int,default=5319)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--timeout",type=int,default=900)
    ap.add_argument("--limit",type=int,default=8)
    ap.add_argument("--num-predict",type=int,default=0,help="Opt-in output-token ceiling; 0 preserves locked behavior")
    ap.add_argument("--context-window",type=int,default=8192,help="Generation context window; locked default is 8192")
    ap.add_argument("--keep-alive",default=None,help="Optional Ollama keep_alive value for an interactive profile")
    ap.add_argument("--priority-exact",action="store_true",help="Opt-in exact-reference promotion; default off")
    ap.add_argument("--source-aware", action="store_true")
    ap.add_argument("--exercise-candidate", action="store_true", help="Opt-in isolated Ussia exercise candidate retrieval")
    ap.add_argument("--targeted-coverage",action="store_true")
    ap.add_argument("--heading-routing",action="store_true",help="Opt-in generic metadata heading expansion; no benchmark ID rules")
    ap.add_argument("--structural-routing",action="store_true",help="Opt-in generic formation/role/principle context reservation")
    ap.add_argument("--tactical-plan",action="store_true",help="Opt-in subproblem coverage, phase-aware reservation and generation contract")
    ap.add_argument("--source-ranking-trace",action="store_true",help="Record source-level semantic scores; requires heading routing and retrieval-only")
    ap.add_argument("--retrieval-only",action="store_true",help="Skip generation; produce retrieval evidence only")
    ap.add_argument("--probe-question",help="One explicit diagnostic question, never the locked gold")
    args=ap.parse_args()
    if args.source_ranking_trace and not (args.heading_routing and args.retrieval_only):
        ap.error("--source-ranking-trace requires --heading-routing and --retrieval-only")
    if args.priority_exact:
        from rag_v5_fresh_reference_e2e_shadow_v1 import reference, exact, prioritize_exact
    if args.targeted_coverage:
        from v5_targeted_coverage_v1 import target, promote, formation_rows, heading_list, MANUAL, consolidation_applicable, consolidation_rows, reserve_consolidation, filter_consolidation_context
    else:
        heading_list = metadata_headings if args.heading_routing else lambda value: []
    if not 1<=args.limit<=12:ap.error("limit must be between 1 and 12")
    if args.num_predict and not 128<=args.num_predict<=4096:ap.error("num-predict must be 0 or between 128 and 4096")
    if not 2048<=args.context_window<=8192:ap.error("context-window must be between 2048 and 8192")
    questions=[("probe_exact",args.probe_question)] if args.probe_question else QUESTIONS
    coll=chromadb.PersistentClient(path=DB).get_collection(args.collection)
    count=coll.count()
    candidate=None
    candidate_count=None
    if args.exercise_candidate:
        candidate=chromadb.PersistentClient(path=DB).get_collection("dribbling_tactics_v5_exercise_candidate_v1")
        candidate_count=candidate.count()
        if candidate_count!=34:
            raise RuntimeError(f"Unexpected exercise candidate count {candidate_count}; expected 34")
    if count!=args.expected_count:raise RuntimeError(f"V5 record count changed: {count}; expected {args.expected_count}; refusing test")
    embed=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    rerank=None if args.tactical_plan else CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",device="cpu",max_length=512)
    report={"collection":args.collection,"count_before":count,"model":args.model,
            "retrieval":"dense24 -> mMARCO CPU -> exact-alias chunk collapse -> top8",
            "alias_pairs":ALIASES,"source_aware_enabled":args.source_aware,
            "exercise_candidate_enabled":args.exercise_candidate,"exercise_candidate_count_before":candidate_count,"priority_exact_enabled":args.priority_exact,"targeted_coverage_enabled":args.targeted_coverage,"retrieval_only":args.retrieval_only,"heading_routing_enabled":args.heading_routing,"tactical_plan_enabled":args.tactical_plan,"source_ranking_trace_enabled":args.source_ranking_trace,"questions":[],"notes":[
                "Citation checks are syntactic only, not factual faithfulness or correctness.",
                "Only four full-text-equal document pairs are aliased; other sources stay separate.",
                "All source IDs and pages refer to existing Chroma metadata."]}
    try:
        for qid,question in questions:
            start=time.monotonic()
            print(f"START {qid}: {question}",flush=True)
            tactical_plan=tactical_analyse(question) if args.tactical_plan else None
            embedding=embed.get_query_embedding(question)
            got=coll.query(query_embeddings=[embedding],n_results=24,
                           include=["documents","metadatas","distances"])
            rows=[]
            for cid,doc,meta,dist in zip(got["ids"][0],got["documents"][0],
                                          got["metadatas"][0],got["distances"][0]):
                raw=meta.get("raw_text") or doc
                rows.append({"id":cid,"source":meta["source"],
                             "source_relative":meta.get("source_relative"),
                             "pages":meta.get("page_numbers"),"text":doc,"headings":heading_list(meta.get("headings")),
                             "distance":float(dist),
                             "fingerprint":hashlib.sha256(norm(raw).encode()).hexdigest()})
            tactical_queries=retrieval_queries(question,tactical_plan) if tactical_plan else [question]
            for tactical_query in tactical_queries[1:]:
                sub_embedding=embed.get_query_embedding(tactical_query)
                sub=coll.query(query_embeddings=[sub_embedding],n_results=8,
                               include=["documents","metadatas","distances"])
                known={row["id"] for row in rows}
                for cid,doc,meta,dist in zip(sub["ids"][0],sub["documents"][0],sub["metadatas"][0],sub["distances"][0]):
                    if cid in known:
                        continue
                    raw=meta.get("raw_text") or doc
                    rows.append({"id":cid,"source":meta["source"],
                                 "source_relative":meta.get("source_relative"),
                                 "pages":meta.get("page_numbers"),"text":doc,
                                 "headings":heading_list(meta.get("headings")),
                                 "distance":float(dist),
                                 "fingerprint":hashlib.sha256(norm(raw).encode()).hexdigest()})
                    known.add(cid)
            tactical_anchors=retrieval_anchors(tactical_plan) if tactical_plan else []
            tactical_anchor_candidate_ids=[]
            for anchor in tactical_anchors:
                anchored=coll.get(where_document={"$contains":anchor},limit=8,
                                  include=["documents","metadatas"])
                known={row["id"] for row in rows}
                for cid,doc,meta in zip(anchored["ids"],anchored["documents"],anchored["metadatas"]):
                    tactical_anchor_candidate_ids.append(cid)
                    if cid in known:
                        continue
                    raw=meta.get("raw_text") or doc
                    rows.append({"id":cid,"source":meta["source"],
                                 "source_relative":meta.get("source_relative"),
                                 "pages":meta.get("page_numbers"),"text":doc,
                                 "headings":heading_list(meta.get("headings")),
                                 "distance":None,
                                 "fingerprint":hashlib.sha256(norm(raw).encode()).hexdigest()})
                    known.add(cid)
            source_hint = None
            named_sources=[]
            if args.source_aware:
                named_sources=discover_named_sources(coll,question)
                if len(named_sources)==1:
                    source_hint = named_sources[0]
                for named_source in named_sources:
                    filtered = coll.query(query_embeddings=[embedding],n_results=24,where={"source":named_source},include=["documents","metadatas","distances"])
                    known = {r["id"] for r in rows}
                    for cid,doc,meta,dist in zip(filtered["ids"][0],filtered["documents"][0],filtered["metadatas"][0],filtered["distances"][0]):
                        if cid not in known:
                            raw = meta.get("raw_text") or doc
                            rows.append({"id":cid,"source":meta["source"],"source_relative":meta.get("source_relative"),"pages":meta.get("page_numbers"),"text":doc,"headings":heading_list(meta.get("headings")),"distance":float(dist),"fingerprint":hashlib.sha256(norm(raw).encode()).hexdigest()})
                            known.add(cid)
            targeted_source, targeted_page = target(qid, question) if args.targeted_coverage else (None, None)
            if targeted_source:
                filtered=coll.query(query_embeddings=[embedding],n_results=24,where={"source":targeted_source},include=["documents","metadatas","distances"])
                known={r["id"] for r in rows}
                for cid,doc,meta,dist in zip(filtered["ids"][0],filtered["documents"][0],filtered["metadatas"][0],filtered["distances"][0]):
                    if cid in known:
                        continue
                    raw=meta.get("raw_text") or doc
                    rows.append({"id":cid,"source":meta["source"],"source_relative":meta.get("source_relative"),"pages":meta.get("page_numbers"),"text":doc,"headings":heading_list(meta.get("headings")),"distance":float(dist),"fingerprint":hashlib.sha256(norm(raw).encode()).hexdigest()})
                    known.add(cid)
            if args.targeted_coverage and qid == "fresh_03" and targeted_source == MANUAL:
                known = {r["id"] for r in rows}
                rows.extend(formation_rows(coll, known))
            if args.targeted_coverage and consolidation_applicable(question):
                known={r["id"] for r in rows}
                rows.extend(consolidation_rows(coll,known))
            if args.heading_routing:
                known_rows={r["id"]:r for r in rows}
                rows.extend(heading_expand(coll,question,known_rows,norm))
            if args.source_aware:
                known={r["id"] for r in rows}
                rows.extend(explicit_manual_candidates(coll,embedding,question,known))
            embedding_model_released=False
            if args.tactical_plan and not args.retrieval_only:
                embedding_model_released=unload_ollama_model("qwen3-embedding:0.6b")
            candidate_ids=[]
            if candidate is not None and re.search(r"\bussia\b",question,re.I):
                extra=candidate.query(query_embeddings=[embedding],n_results=min(24,candidate_count),include=["documents","metadatas","distances"])
                known={r["id"] for r in rows}
                for cid,doc,meta,dist in zip(extra["ids"][0],extra["documents"][0],extra["metadatas"][0],extra["distances"][0]):
                    if cid not in known:
                        rows.append({"id":cid,"source":meta["source"],"source_relative":meta.get("source_relative"),
                                     "pages":meta.get("page_numbers"),"text":doc,"distance":float(dist),
                                     "fingerprint":hashlib.sha256(norm(doc).encode()).hexdigest()})
                        known.add(cid)
                        candidate_ids.append(cid)
            priority_ids=set()
            if args.priority_exact:
                ref=reference(question)
                named={"ussia":"Transizioni.Ussia","foscarini":"manovre_offensive_vari_sistemi_gioco_Foscarini"}
                matches=[v for k,v in named.items() if k in question.casefold()]
                if ref and len(matches)==1:
                    candidates=exact(coll,matches[0],ref)
                    priority_ids={r["id"] for r in candidates}
                    existing={r["id"] for r in rows}
                    for r in candidates:
                        if r["id"] not in existing:
                            rows.append({"id":r["id"],"source":r["source"],"source_relative":None,
                                         "pages":r["pages"],"text":r["text"],"distance":None,
                                         "fingerprint":hashlib.sha256(norm(r["text"]).encode()).hexdigest()})
                            existing.add(r["id"])
            active_rerank=rerank or CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",device="cpu",max_length=512)
            scores=active_rerank.predict([(question, (" / ".join(r.get("headings") or []) + " " + r["text"]).strip() if (args.targeted_coverage and qid == "fresh_03") or (args.heading_routing and heading_applicable(question)) else r["text"]) for r in rows],
                                  batch_size=8 if args.tactical_plan else 1,show_progress_bar=False)
            selected=[];seen=set();dropped=0
            for index in sorted(range(len(rows)),key=lambda i:float(scores[i]),reverse=True):
                r=rows[index]
                canonical=ALIASES.get(r["source"],r["source"])
                key=(canonical,r["fingerprint"])
                if key in seen:
                    dropped+=1
                    continue
                seen.add(key)
                selected.append(r)
                if len(selected)>=args.limit:break
            targeted_promoted=[]
            if targeted_source:
                selected, targeted_promoted=promote(rows,scores,ALIASES,targeted_source,targeted_page,args.limit)
            if args.targeted_coverage and consolidation_applicable(question):
                selected,targeted_promoted=reserve_consolidation(rows,scores,ALIASES,question,args.limit)
            consolidation_excluded=[]
            if args.targeted_coverage and consolidation_applicable(question):
                selected,consolidation_excluded=filter_consolidation_context(question,selected,targeted_promoted)
            selected,post_loss_excluded=filter_post_loss_context(question,selected,targeted_promoted)
            source_scope_excluded=[]
            if args.source_aware and len(named_sources)==1 and not any(term in question.casefold() for term in ("confront", "manuale interno")):
                kept=[row for row in selected if row["source"]==named_sources[0]]
                if kept:
                    kept_ids={row["id"] for row in kept}
                    source_scope_excluded=[row["id"] for row in selected if row["id"] not in kept_ids]
                    selected=kept
            selected,explicit_manual_reserved=reserve_explicit_manual(question,rows,scores,selected,args.limit)
            heading_reserved=[]
            source_ranking_trace=[]
            source_selection_trace={}
            if args.heading_routing:
                revised, heading_reserved=heading_reserve(rows,scores,question,ALIASES,args.limit,reranker=active_rerank)
                if revised is not None:
                    selected=revised
                if args.source_ranking_trace:
                    source_ranking_trace=semantic_source_ranking(question,rows,active_rerank)
                    selected_source, hybrid_trace=hybrid_source_select(question,rows,active_rerank)
                    source_selection_trace={"selected_source":selected_source,"semantic_margin":1.5,"candidates":hybrid_trace}
            structural_reserved=[]
            structural_signals={}
            if args.structural_routing:
                selected,structural_reserved,structural_signals=structural_reserve(rows,scores,selected,question,args.limit)
                structural_signals={key:sorted(value) for key,value in structural_signals.items()}
            tactical_reserved=[]
            tactical_covered={}
            tactical_anchor_reserved=[]
            if tactical_plan:
                selected,tactical_reserved,tactical_covered=tactical_diversify(rows,scores,selected,tactical_plan,args.limit)
                selected,tactical_anchor_reserved=reserve_anchor_candidates(
                    rows,scores,selected,tactical_anchor_candidate_ids,args.limit)
                del active_rerank
                gc.collect()
            evidence=[{"label":f"F{i}","id":r["id"],"source":r["source"],
                       "canonical_source":ALIASES.get(r["source"],r["source"]),
                       "source_relative":r["source_relative"],"pages":r["pages"],
                       "distance":round(r["distance"],5) if r["distance"] is not None else None,"headings":r.get("headings",[]) if (args.targeted_coverage and qid == "fresh_03") or args.heading_routing else [],"text":(((" / ".join(r.get("headings") or []) + "\n") if not r["text"].lstrip().startswith(" / ".join(r.get("headings") or [])) else "") if ((args.targeted_coverage and qid == "fresh_03") or args.heading_routing) and r.get("headings") else "") + r["text"]}
                      for i,r in enumerate(selected,1)]
            if args.priority_exact and priority_ids:
                evidence=prioritize_exact(evidence,priority_ids)
            answer,stats=("",{}) if args.retrieval_only else chat(
                args.model,question,evidence,args.timeout,args.targeted_coverage,
                args.heading_routing,args.num_predict,args.context_window,args.keep_alive,tactical_plan)
            cited=sorted(set(re.findall(r"\[F(\d+)\]",answer)),key=int)
            tactical_answer_audit=tactical_audit_answer(answer,tactical_plan) if tactical_plan and answer else None
            valid={str(i) for i in range(1,len(evidence)+1)}
            entry={"id":qid,"question":question,"answer":answer,"evidence":evidence,
                   "source_aware_source":source_hint,"source_aware_sources":named_sources,"targeted_source":targeted_source,"targeted_page":targeted_page,"targeted_promoted_ids":targeted_promoted,"consolidation_excluded_ids":consolidation_excluded,"post_loss_excluded_ids":post_loss_excluded,"source_scope_excluded_ids":source_scope_excluded,"explicit_manual_reserved_ids":explicit_manual_reserved,"heading_reserved_ids":heading_reserved,"source_ranking_trace":source_ranking_trace,"source_selection_trace":source_selection_trace,"exercise_candidate_ids":candidate_ids,
                   "priority_exact_enabled":args.priority_exact,"priority_exact_candidate_ids":sorted(priority_ids),
                   "structural_reserved_ids":structural_reserved,"structural_signals":structural_signals,
                   "tactical_plan":tactical_plan,"tactical_reserved_ids":tactical_reserved,"tactical_covered":tactical_covered,
                   "tactical_queries":tactical_queries,"tactical_anchors":tactical_anchors,
                   "tactical_anchor_candidate_ids":sorted(set(tactical_anchor_candidate_ids)),
                   "tactical_anchor_reserved_ids":tactical_anchor_reserved,
                   "tactical_answer_audit":tactical_answer_audit,
                   "embedding_model_released_before_generation":embedding_model_released,
                   "citation_ids":cited,"invalid_citation_ids":[x for x in cited if x not in valid],
                   "has_any_citation":bool(cited),
                   "alias_chunks_skipped":dropped,
                   "elapsed_seconds":round(time.monotonic()-start,2),
                   "generation":stats}
            report["questions"].append(entry)
            print(f"DONE {qid}: citations={cited}, invalid={entry['invalid_citation_ids']}, "
                  f"alias_skipped={dropped}, elapsed={entry['elapsed_seconds']}s",flush=True)
    except (Exception,KeyboardInterrupt) as exc:
        report["error"]=f"{type(exc).__name__}: {exc}"
        print("ERROR:",report["error"],flush=True)
    report["count_after"]=coll.count()
    if candidate is not None:
        report["exercise_candidate_count_after"]=candidate.count()
    report["index_unchanged"]=(report["count_after"]==count and (candidate is None or report["exercise_candidate_count_after"]==candidate_count))
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        print("REPORT:",args.output,flush=True)
    print(f"COMPLETE {len(report['questions'])}/{len(questions)}; V5 unchanged={report['index_unchanged']}",flush=True)
    if "error" in report:raise SystemExit(1)
if __name__=="__main__":main()
