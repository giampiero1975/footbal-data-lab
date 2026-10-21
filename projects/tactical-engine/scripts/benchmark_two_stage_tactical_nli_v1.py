#!/usr/bin/env python3
"""Two-stage tactical claim judge: entailment first, explicit contradiction second.

Experiment only. Native Ollama /api/chat structured output:
https://docs.ollama.com/api/chat
"""
from __future__ import annotations
import argparse
import asyncio
import json
import os
import time
from pathlib import Path
from pydantic import BaseModel, Field
from smoke_ragas_043_native_ollama_v1 import NativeOllamaRagasLLM

class Decision(BaseModel):
    yes: bool
    rationale: str
    evidence_quote: str = Field(description="Exact contiguous substring of the source or empty string")

SUPPORT = """Valuta solo se la fonte SUPPORTA l'intera affermazione, con tutti i dettagli e quantificatori.
YES soltanto se tutti gli elementi sono esplicitamente presenti o direttamente inferibili.
Riconosci sinonimi contestuali (es. rintanato presso l'area = blocco basso).
NO se manca anche solo una prova: finalità non è risultato, rischio non è certezza, una possibilità non è sempre, e non inferire statistiche.
Non decidere se la fonte contraddice: qui NO include sia contraddizione sia insufficienza.
Restituisci una citazione letterale CONTIGUA della fonte, o stringa vuota. JSON soltanto."""

CONTRADICTION = """Valuta soltanto se la fonte CONTRADDICE DIRETTAMENTE l'affermazione.
YES solo se la fonte stabilisce esplicitamente un fatto incompatibile con la proposizione (compresi negazione, polarità, quantità, confronti e significato).
NO se la fonte semplicemente NON DIMOSTRA l'affermazione, anche se questa usa 'sempre', 'garantisce', 'solo', probabilità o numeri. Mancanza di prova NON è prova del contrario.
Esempi concettuali: 'difficile' non dimostra 'impossibile', ma neppure dimostra 'possibile'; 'ridurre imprevedibilità' e 'perdere imprevedibilità' significano la stessa cosa; 'togliere spazio' contraddice 'concedere molto spazio'.
Cerca una prova diretta del contrario nella fonte, non nella conoscenza generale. Restituisci una citazione letterale CONTIGUA o stringa vuota. JSON soltanto."""

def save(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    os.replace(tmp,path)

async def run(a):
    cases=json.loads(a.gold.read_text(encoding="utf-8"))["cases"]
    signature=[{"id":c["id"],"gold":c["gold"],"claim":c["claim"],"evidence":c["evidence"]} for c in cases]
    config={"model":a.model,"max_tokens":a.max_tokens,"prompts":{"support":SUPPORT,"contradiction":CONTRADICTION}}
    if a.output.exists():
        report=json.loads(a.output.read_text(encoding="utf-8"))
        if report.get("input_signature")!=signature or report.get("config")!=config:
            raise ValueError("Output incompatible with dataset or configuration; use a new path")
    else:
        report={"test":"two_stage_tactical_nli_v1","input_signature":signature,"config":config,
                "limitations":["Experimental prompts informed by observed errors on the same source excerpts.",
                               "New claims do not make this independent-source validation.",
                               "Citation validity is an exact substring check, not a semantic citation quality assessment."],
                "results":[]}
    completed={r["id"] for r in report["results"]}
    llm=NativeOllamaRagasLLM(a.model,a.ollama_url,a.timeout,a.max_tokens)
    count=0
    for c in cases:
        if c["id"] in completed: continue
        if a.limit and count>=a.limit: break
        row={"id":c["id"],"gold":c["gold"]}
        start=time.monotonic()
        try:
            common="\n\nFONTE:\n"+c["evidence"]+"\n\nAFFERMAZIONE:\n"+c["claim"]
            support=(await llm.agenerate(SUPPORT+common,Decision)).model_dump()
            row["support"]=support
            if support["yes"]:
                row["prediction"]="supported"
            else:
                contradiction=(await llm.agenerate(CONTRADICTION+common,Decision)).model_dump()
                row["contradiction"]=contradiction
                row["prediction"]="contradicted" if contradiction["yes"] else "insufficient"
            for stage in ("support","contradiction"):
                if stage in row:
                    q=row[stage]["evidence_quote"]
                    row[stage]["quote_found"]=bool(q and q in c["evidence"])
            row["correct_3way"]=row["prediction"]==c["gold"]
            row["correct_binary"]=(row["prediction"]=="supported")==(c["gold"]=="supported")
        except Exception as exc:
            row["error"]=type(exc).__name__+": "+str(exc)[:1200]
        row["elapsed_seconds"]=round(time.monotonic()-start,2)
        report["results"].append(row)
        valid=[r for r in report["results"] if "prediction" in r]
        report["summary"]={"total":len(cases),"completed":len(report["results"]),
                           "remaining":len(cases)-len(report["results"]),
                           "errors":sum("error" in r for r in report["results"]),
                           "accuracy_3way":sum(r["correct_3way"] for r in valid)/len(valid) if valid else None,
                           "accuracy_binary":sum(r["correct_binary"] for r in valid)/len(valid) if valid else None,
                           "confusion":{g:{p:sum(r["gold"]==g and r["prediction"]==p for r in valid)
                                           for p in ("supported","contradicted","insufficient")}
                                        for g in ("supported","contradicted","insufficient")},
                           "invalid_citations":sum(not r[s]["quote_found"] for r in valid for s in ("support","contradiction") if s in r)}
        save(a.output,report)
        print(json.dumps({"id":row["id"],"gold":row["gold"],"prediction":row.get("prediction"),
                          "error":row.get("error"),"seconds":row["elapsed_seconds"]},ensure_ascii=False),flush=True)
        count+=1
        if "error" in row and a.stop_on_error: break
    print("SUMMARY",json.dumps(report.get("summary"),ensure_ascii=False),flush=True)
    print("REPORT",a.output,flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--gold",type=Path,default=Path("projects/tactical-engine/eval/claim_fidelity_adversarial_v1.json"))
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    p.add_argument("--timeout",type=int,default=180)
    p.add_argument("--max-tokens",type=int,default=1024)
    p.add_argument("--limit",type=int,default=0)
    p.add_argument("--stop-on-error",action="store_true")
    asyncio.run(run(p.parse_args()))
if __name__=="__main__":main()
