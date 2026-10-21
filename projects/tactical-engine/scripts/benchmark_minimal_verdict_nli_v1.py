#!/usr/bin/env python3
"""Final experimental comparison: verdict-only structured NLI vs saved two-stage baseline.

No production changes. First-stage yes/no and conditional second-stage yes/no use
the SAME tactical decision rules as the original two-stage evaluator; remove
rationale and quotation from the response schema to isolate output complexity.
Sources: https://docs.ollama.com/api/chat and
https://docs.ollama.com/capabilities/structured-outputs
"""
from __future__ import annotations
import argparse
import asyncio
import json
import os
import time
from pathlib import Path
from pydantic import BaseModel
from smoke_ragas_043_native_ollama_v1 import NativeOllamaRagasLLM
from benchmark_two_stage_tactical_nli_v1 import SUPPORT, CONTRADICTION

class Verdict(BaseModel):
    yes: bool

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    os.replace(tmp,path)

def metrics(rows):
    labels=("supported","contradicted","insufficient")
    good=[r for r in rows if "prediction" in r]
    return {"completed":len(good),"errors":sum("error" in r for r in rows),
            "accuracy_3way":sum(r["prediction"]==r["gold"] for r in good)/len(good) if good else None,
            "accuracy_binary":sum((r["prediction"]=="supported")==(r["gold"]=="supported") for r in good)/len(good) if good else None,
            "confusion":{g:{p:sum(r["gold"]==g and r["prediction"]==p for r in good) for p in labels} for g in labels}}

async def main_async(a):
    cases=json.loads(a.gold.read_text(encoding="utf-8"))["cases"]
    signature=[{"id":c["id"],"gold":c["gold"],"claim":c["claim"],"evidence":c["evidence"]} for c in cases]
    # Retain semantic rules verbatim, removing only the quotation instruction.
    prompts={"support":SUPPORT.replace("Restituisci una citazione letterale CONTIGUA della fonte, o stringa vuota. JSON soltanto.","Rispondi soltanto con il campo booleano yes nello schema JSON."),
             "contradiction":CONTRADICTION.replace("Restituisci una citazione letterale CONTIGUA o stringa vuota. JSON soltanto.","Rispondi soltanto con il campo booleano yes nello schema JSON.")}
    config={"model":a.model,"max_tokens":a.max_tokens,"prompts":prompts,"schema":"yes:boolean"}
    if a.output.exists():
        report=json.loads(a.output.read_text(encoding="utf-8"))
        if report.get("input_signature")!=signature or report.get("config")!=config:
            raise ValueError("Incompatible checkpoint: use a new output path")
    else:
        report={"test":"minimal_verdict_two_stage_v1","input_signature":signature,"config":config,"results":[],
                "limitations":["Same external-source cases used to diagnose prior evaluator; comparison is paired, not a fresh untouched holdout.",
                               "Removing rationale and quotation changes the generation task; no citation-quality measurement.",
                               "No claims about production RAG retrieval or deployment."]}
    completed={r["id"] for r in report["results"]}
    llm=NativeOllamaRagasLLM(a.model,a.ollama_url,a.timeout,a.max_tokens)
    count=0
    for case in cases:
        if case["id"] in completed: continue
        if a.limit and count>=a.limit: break
        row={"id":case["id"],"gold":case["gold"]}
        start=time.monotonic()
        try:
            common="\n\nFONTE:\n"+case["evidence"]+"\n\nAFFERMAZIONE:\n"+case["claim"]
            s=await llm.agenerate(prompts["support"]+common,Verdict)
            row["support_yes"]=s.yes
            if s.yes:
                row["prediction"]="supported"
            else:
                c=await llm.agenerate(prompts["contradiction"]+common,Verdict)
                row["contradiction_yes"]=c.yes
                row["prediction"]="contradicted" if c.yes else "insufficient"
        except Exception as exc:
            row["error"]=type(exc).__name__+": "+str(exc)[:1200]
        row["elapsed_seconds"]=round(time.monotonic()-start,2)
        report["results"].append(row)
        report["summary"]={"total":len(cases),"remaining":len(cases)-len(report["results"]),**metrics(report["results"])}
        save(a.output,report)
        print(json.dumps({"id":row["id"],"prediction":row.get("prediction"),"gold":row["gold"],"error":row.get("error")},ensure_ascii=False),flush=True)
        count+=1
        if "error" in row and a.stop_on_error: break
    print("SUMMARY",json.dumps(report.get("summary"),ensure_ascii=False),flush=True)
    print("REPORT",a.output,flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--gold",type=Path,default=Path("projects/tactical-engine/eval/claim_fidelity_external_sources_holdout_v1.json"))
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    p.add_argument("--timeout",type=int,default=180)
    p.add_argument("--max-tokens",type=int,default=1024)
    p.add_argument("--limit",type=int,default=0)
    p.add_argument("--stop-on-error",action="store_true")
    asyncio.run(main_async(p.parse_args()))
if __name__=="__main__":main()
