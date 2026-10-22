#!/usr/bin/env python3
"""Read-only paired prompt shadow replay against frozen RAG V5 pilot evidence.

Uses the *same* question and retrieved passages as baseline; only system prompt
changes. No Chroma access or index mutation. Outputs new file exclusively.
"""
import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.request import Request, urlopen

SHADOW_SYSTEM = (
    "Sei DRIBBLING, assistente di analisi tattica calcistica. Rispondi in italiano "
    "esclusivamente sulla base degli estratti numerati. "
    "Prima di formulare ogni affermazione, verifica che il passaggio citato riguardi "
    "la STESSA fase di gioco (possesso, non possesso, transizione positiva o negativa), "
    "lo STESSO evento richiesto (es. cambio di modulo in partita vs caratteristiche "
    "statiche del modulo) e le STESSE condizioni tattiche. "
    "Non trasformare un esempio particolare in una regola universale. "
    "Non dedurre l'assenza di informazioni in tutto il corpus dai soli estratti ricevuti. "
    "Ogni affermazione tattica sostanziale deve citare [F1], [F2], ecc. "
    "Se le evidenze sono indirette, dichiaralo e distingui l'inferenza dalla fonte. "
    "Se mancano prove sufficienti, esplicita il limite senza inventare.")
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--baseline",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--timeout",type=int,default=900)
    p.add_argument("--execute",action="store_true")
    args=p.parse_args()
    if not args.execute:p.error("Explicit --execute required")
    if args.baseline.resolve()==args.output.resolve() or args.output.exists():
        p.error("Refusing to overwrite existing file or baseline")
    raw=args.baseline.read_bytes()
    baseline=json.loads(raw)
    questions=baseline.get("questions",[])
    if len(questions)!=10 or not all(q.get("evidence") and q.get("answer") for q in questions):
        p.error("Expected 10 complete baseline question/answer/evidence records")
    report={"schema":"rag_v5_quality_shadow_frozen_evidence_v1",
            "baseline_sha256":hashlib.sha256(raw).hexdigest(),
            "model":args.model,"intervention":"system_prompt_only",
            "evidence_policy":"identical_to_baseline; no retrieval or reranking",
            "system_prompt":SHADOW_SYSTEM,"questions":[]}
    try:
        for q in questions:
            start=time.monotonic()
            context="\n\n".join(
                f"[{e['label']}] Fonte: {e['source']} | Pagine: {e['pages']}\n{e['text']}"
                for e in q["evidence"])
            payload={"model":args.model,"stream":False,"think":False,
                     "messages":[{"role":"system","content":SHADOW_SYSTEM},
                                 {"role":"user","content":f"DOMANDA:\n{q['question']}\n\nFONTI:\n{context}"}],
                     "options":{"temperature":0,"num_ctx":8192}}
            req=Request("http://127.0.0.1:11434/api/chat",
                        data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
                        headers={"Content-Type":"application/json"},method="POST")
            with urlopen(req,timeout=args.timeout) as resp:
                result=json.load(resp)
            answer=(result.get("message") or {}).get("content","")
            if not answer.strip():raise RuntimeError("Empty answer for "+q["id"])
            citations=sorted(set(re.findall(r"\[F(\d+)\]",answer)),key=int)
            valid={str(i) for i in range(1,len(q["evidence"])+1)}
            report["questions"].append({
                "id":q["id"],"question":q["question"],
                "baseline_answer":q["answer"],"shadow_answer":answer,
                "evidence":q["evidence"],"citation_ids":citations,
                "invalid_citation_ids":[c for c in citations if c not in valid],
                "elapsed_seconds":round(time.monotonic()-start,2),
                "generation":{"total_duration_ns":result.get("total_duration"),
                              "eval_count":result.get("eval_count")}})
            print("DONE",q["id"],flush=True)
    except (Exception,KeyboardInterrupt) as e:
        report["error"]=f"{type(e).__name__}: {e}"
        print("ERROR",report["error"],flush=True)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(report,f,ensure_ascii=False,indent=2)
        f.write("\n")
    print("REPORT",args.output,flush=True)
    if report.get("error"):raise SystemExit(1)
if __name__=="__main__":main()
