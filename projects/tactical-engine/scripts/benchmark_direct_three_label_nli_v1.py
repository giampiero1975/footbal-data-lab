#!/usr/bin/env python3
"""Read-only experiment: direct three-label NLI via Ollama structured output.

Docs: https://docs.ollama.com/api/chat
      https://docs.ollama.com/capabilities/structured-outputs
"""
import argparse
import asyncio
import json
import os
import time
from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from smoke_ragas_043_native_ollama_v1 import NativeOllamaRagasLLM

class Verdict(BaseModel):
    label: Literal["supported", "contradicted", "insufficient"]

INSTRUCTION = """Classifica l'intera affermazione rispetto alla fonte, senza conoscenze esterne.
supported: la fonte dimostra tutta l'affermazione, inclusi sinonimi e parafrasi fedeli.
contradicted: la fonte afferma esplicitamente qualcosa di incompatibile con l'affermazione.
insufficient: la fonte non dimostra né smentisce direttamente l'affermazione.
Controlla negazioni, direzione dei confronti e quantificatori. Un numero o una garanzia non documentati non sono automaticamente falsi. Un'affermazione può omettere dettagli della fonte ed essere comunque supportata.
Rispondi soltanto con JSON contenente label."""

def summary(rows):
    labels=("supported", "contradicted", "insufficient")
    valid=[r for r in rows if "prediction" in r]
    n=len(valid)
    return {
        "completed":n,
        "errors":sum("error" in r for r in rows),
        "accuracy_3way":sum(r["prediction"]==r["gold"] for r in valid)/n if n else None,
        "accuracy_binary":sum((r["prediction"]=="supported")==(r["gold"]=="supported") for r in valid)/n if n else None,
        "confusion":{g:{p:sum(r["gold"]==g and r["prediction"]==p for r in valid) for p in labels} for g in labels},
    }

async def run(args):
    cases=json.loads(args.gold.read_text(encoding="utf-8"))["cases"]
    signature=[{k:c[k] for k in ("id","gold","claim","evidence")} for c in cases]
    config={"model":args.model,"max_tokens":args.max_tokens,"instruction":INSTRUCTION}
    if args.output.exists():
        report=json.loads(args.output.read_text(encoding="utf-8"))
        if report.get("signature")!=signature or report.get("config")!=config:
            raise ValueError("Checkpoint incompatible with this dataset or configuration")
    else:
        report={
            "test":"direct_three_label_nli_v1",
            "signature":signature,
            "config":config,
            "limitations":[
                "Development comparison on previously inspected cases; not independent validation.",
                "Does not test source retrieval, citation quality, or production answer generation.",
                "No production changes."
            ],
            "results":[]
        }
    completed={r["id"] for r in report["results"]}
    llm=NativeOllamaRagasLLM(args.model,args.ollama_url,args.timeout,args.max_tokens)
    processed=0
    for c in cases:
        if c["id"] in completed: continue
        if args.limit and processed>=args.limit: break
        row={"id":c["id"],"gold":c["gold"]}
        start=time.monotonic()
        try:
            prompt=INSTRUCTION+"\n\nFONTE:\n"+c["evidence"]+"\n\nAFFERMAZIONE:\n"+c["claim"]
            result=await llm.agenerate(prompt,Verdict)
            row["prediction"]=result.label
        except Exception as exc:
            row["error"]=type(exc).__name__+": "+str(exc)[:1000]
        row["elapsed_seconds"]=round(time.monotonic()-start,2)
        report["results"].append(row)
        report["summary"]={"total":len(cases),"remaining":len(cases)-len(report["results"]),**summary(report["results"])}
        args.output.parent.mkdir(parents=True,exist_ok=True)
        temp=args.output.with_suffix(args.output.suffix+".tmp")
        temp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        os.replace(temp,args.output)
        print(json.dumps({"id":row["id"],"gold":row["gold"],"prediction":row.get("prediction"),"error":row.get("error")},ensure_ascii=False),flush=True)
        processed+=1
        if "error" in row and args.stop_on_error: break
    print("SUMMARY",json.dumps(report.get("summary"),ensure_ascii=False),flush=True)
    print("REPORT",args.output,flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--gold",type=Path,default=Path("projects/tactical-engine/eval/claim_fidelity_external_sources_holdout_v1.json"))
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--model",default="qwen3.5:9b")
    parser.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    parser.add_argument("--timeout",type=int,default=180)
    parser.add_argument("--max-tokens",type=int,default=1024)
    parser.add_argument("--limit",type=int,default=0)
    parser.add_argument("--stop-on-error",action="store_true")
    asyncio.run(run(parser.parse_args()))

if __name__=="__main__":
    main()
