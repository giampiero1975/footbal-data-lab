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
        "Ogni affermazione tattica sostanziale deve avere una citazione nel formato [F1], [F2], ecc. "
        "Se le fonti non consentono una risposta affidabile, esplicita il limite. "
        "Rispondi in italiano in modo chiaro e sintetico.")
def norm(s):
    return re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",s.casefold())).strip()
def chat(model,question,evidence,timeout):
    context="\n\n".join(f"[F{i}] Fonte: {r['source']} | Pagine: {r['pages']}\n{r['text']}"
                         for i,r in enumerate(evidence,1))
    payload={"model":model,"stream":False,"think":False,
             "messages":[{"role":"system","content":SYSTEM},
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
    args=ap.parse_args()
    if not 1<=args.limit<=12:ap.error("limit must be between 1 and 12")
    coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    count=coll.count()
    if count!=5319:raise RuntimeError(f"V5 record count changed: {count}; refusing test")
    embed=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    rerank=CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",device="cpu",max_length=512)
    report={"collection":COLLECTION,"count_before":count,"model":args.model,
            "retrieval":"dense24 -> mMARCO CPU -> exact-alias chunk collapse -> top8",
            "alias_pairs":ALIASES,"questions":[],"notes":[
                "Citation checks are syntactic only, not factual faithfulness or correctness.",
                "Only four full-text-equal document pairs are aliased; other sources stay separate.",
                "All source IDs and pages refer to existing Chroma metadata."]}
    try:
        for qid,question in QUESTIONS:
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
                             "pages":meta.get("page_numbers"),"text":doc,
                             "distance":float(dist),
                             "fingerprint":hashlib.sha256(norm(raw).encode()).hexdigest()})
            scores=rerank.predict([(question,r["text"]) for r in rows],
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
            evidence=[{"label":f"F{i}","id":r["id"],"source":r["source"],
                       "canonical_source":ALIASES.get(r["source"],r["source"]),
                       "source_relative":r["source_relative"],"pages":r["pages"],
                       "distance":round(r["distance"],5),"text":r["text"]}
                      for i,r in enumerate(selected,1)]
            answer,stats=chat(args.model,question,evidence,args.timeout)
            cited=sorted(set(re.findall(r"\[F(\d+)\]",answer)),key=int)
            valid={str(i) for i in range(1,len(evidence)+1)}
            entry={"id":qid,"question":question,"answer":answer,"evidence":evidence,
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
    report["index_unchanged"]=(report["count_after"]==count)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        print("REPORT:",args.output,flush=True)
    print(f"COMPLETE {len(report['questions'])}/{len(QUESTIONS)}; V5 unchanged={report['index_unchanged']}",flush=True)
    if "error" in report:raise SystemExit(1)
if __name__=="__main__":main()
