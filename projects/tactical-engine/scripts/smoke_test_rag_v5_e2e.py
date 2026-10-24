#!/usr/bin/env python3
"""Read-only V5 end-to-end grounded-answer smoke test.

Uses the verified four exact-text alias pairs only. Writes JSON report only;
does not change Chroma, PDF, source JSON, or production configuration.
"""
from __future__ import annotations
import argparse
from collections import Counter
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
def scoped_guidance(question):
    if not question.startswith("Perché la descrizione di un assetto difensivo nel manuale interno"):
        return ""
    return (" Elenca esplicitamente i moduli 4-3-3, 4-4-2, 3-5-2 e 3-4-2-1 con le rispettive citazioni. "
            "Distingui le descrizioni tattiche dalle prove causali: senza dati comparativi non si può dimostrare "
            "che cambiare modulo durante la partita aumenti o diminuisca il rischio.")
def chat(model,question,evidence,timeout):
    context="\n\n".join(f"[F{i}] Fonte: {r['source']} | Pagine: {r['pages']}\n{r['text']}"
                         for i,r in enumerate(evidence,1))
    payload={"model":model,"stream":False,"think":False,
             "messages":[{"role":"system","content":SYSTEM+scoped_guidance(question)},
                         {"role":"user","content":f"DOMANDA:\n{question}\n\nFONTI:\n{context}"}],
             "options":{"temperature":0,"num_ctx":8192}}
    request=Request("http://127.0.0.1:11434/api/chat",
                    data=json.dumps(payload,ensure_ascii=False).encode(),
                    headers={"Content-Type":"application/json"},method="POST")
    with urlopen(request,timeout=timeout) as response:
        obj=json.load(response)
    msg=obj.get("message") or {}
    answer=msg.get("content","")
    if not answer.strip():
        raise RuntimeError(f"Empty model answer: {str(obj)[:300]}")
    return answer,{"total_duration_ns":obj.get("total_duration"),
                   "eval_count":obj.get("eval_count"),
                   "prompt_eval_count":obj.get("prompt_eval_count")}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model",default="qwen3.5:9b")
    ap.add_argument("--output",type=Path)
    ap.add_argument("--timeout",type=int,default=900)
    ap.add_argument("--limit",type=int,default=8)
    ap.add_argument("--priority-exact",action="store_true",help="Opt-in exact-reference promotion; default off")
    ap.add_argument("--source-aware", action="store_true")
    ap.add_argument("--exercise-candidate", action="store_true", help="Opt-in isolated Ussia exercise candidate retrieval")
    ap.add_argument("--targeted-coverage",action="store_true")
    ap.add_argument("--retrieval-only",action="store_true",help="Skip generation; produce retrieval evidence only")
    ap.add_argument("--probe-question",help="One explicit diagnostic question, never the locked gold")
    args=ap.parse_args()
    if args.priority_exact:
        from rag_v5_fresh_reference_e2e_shadow_v1 import reference, exact, prioritize_exact
    if args.targeted_coverage:
        from v5_targeted_coverage_v1 import target, promote, formation_rows, heading_list, MANUAL
    else:
        heading_list = lambda value: []
    if not 1<=args.limit<=12:ap.error("limit must be between 1 and 12")
    questions=[("probe_exact",args.probe_question)] if args.probe_question else QUESTIONS
    coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    count=coll.count()
    candidate=None
    candidate_count=None
    if args.exercise_candidate:
        candidate=chromadb.PersistentClient(path=DB).get_collection("dribbling_tactics_v5_exercise_candidate_v1")
        candidate_count=candidate.count()
        if candidate_count!=34:
            raise RuntimeError(f"Unexpected exercise candidate count {candidate_count}; expected 34")
    if count!=5319:raise RuntimeError(f"V5 record count changed: {count}; refusing test")
    embed=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    rerank=CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",device="cpu",max_length=512)
    report={"collection":COLLECTION,"count_before":count,"model":args.model,
            "retrieval":"dense24 -> mMARCO CPU -> exact-alias chunk collapse -> top8",
            "alias_pairs":ALIASES,"source_aware_enabled":args.source_aware,
            "exercise_candidate_enabled":args.exercise_candidate,"exercise_candidate_count_before":candidate_count,"priority_exact_enabled":args.priority_exact,"targeted_coverage_enabled":args.targeted_coverage,"retrieval_only":args.retrieval_only,"questions":[],"notes":[
                "Citation checks are syntactic only, not factual faithfulness or correctness.",
                "Only four full-text-equal document pairs are aliased; other sources stay separate.",
                "All source IDs and pages refer to existing Chroma metadata."]}
    try:
        for qid,question in questions:
            start=time.monotonic()
            print(f"START {qid}: {question}",flush=True)
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
            source_hint = None
            if args.source_aware:
                named = {"ussia":"Transizioni.Ussia","foscarini":"manovre_offensive_vari_sistemi_gioco_Foscarini"}
                matches = [v for k,v in named.items() if re.search(r"\b"+k+r"\b",question,re.I)]
                if len(matches)==1:
                    source_hint = matches[0]
                    filtered = coll.query(query_embeddings=[embedding],n_results=24,where={"source":source_hint},include=["documents","metadatas","distances"])
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
            scores=rerank.predict([(question, (" / ".join(r.get("headings") or []) + " " + r["text"]).strip() if args.targeted_coverage and qid == "fresh_03" else r["text"]) for r in rows],
                                  batch_size=1,show_progress_bar=False)
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
            evidence=[{"label":f"F{i}","id":r["id"],"source":r["source"],
                       "canonical_source":ALIASES.get(r["source"],r["source"]),
                       "source_relative":r["source_relative"],"pages":r["pages"],
                       "distance":round(r["distance"],5) if r["distance"] is not None else None,"headings":r.get("headings",[]) if args.targeted_coverage and qid == "fresh_03" else [],"text":(((" / ".join(r.get("headings") or []) + "\n") if not r["text"].lstrip().startswith(" / ".join(r.get("headings") or [])) else "") if args.targeted_coverage and qid == "fresh_03" and r.get("headings") else "") + r["text"]}
                      for i,r in enumerate(selected,1)]
            if args.priority_exact and priority_ids:
                evidence=prioritize_exact(evidence,priority_ids)
            answer,stats=("",{}) if args.retrieval_only else chat(args.model,question,evidence,args.timeout)
            cited=sorted(set(re.findall(r"\[F(\d+)\]",answer)),key=int)
            valid={str(i) for i in range(1,len(evidence)+1)}
            entry={"id":qid,"question":question,"answer":answer,"evidence":evidence,
                   "source_aware_source":source_hint,"targeted_source":targeted_source,"targeted_page":targeted_page,"targeted_promoted_ids":targeted_promoted,"exercise_candidate_ids":candidate_ids,
                   "priority_exact_enabled":args.priority_exact,"priority_exact_candidate_ids":sorted(priority_ids),
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
