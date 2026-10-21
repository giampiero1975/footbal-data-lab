#!/usr/bin/env python3
"""Experimental strict claim-level NLI judge for tactical evidence.

Independent of Ragas Faithfulness; compare with original holdout without modifying it.
Docs: https://docs.ollama.com/api/chat
"""
from __future__ import annotations
import argparse
import asyncio
import json
import math
import os
import time
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field
from smoke_ragas_043_native_ollama_v1 import NativeOllamaRagasLLM

class ClaimJudgment(BaseModel):
    label: Literal["supported", "contradicted", "insufficient"]
    rationale: str = Field(description="Short evidence-grounded explanation")
    evidence_quote: str = Field(description="Exact short quote from evidence, or empty if no relevant passage")

RULES = """Sei un verificatore rigoroso di affermazioni tattiche calcistiche. Valuta l'INTERA affermazione, non singoli frammenti. Usa soltanto la fonte fornita.
Etichette:
- supported: TUTTI gli elementi essenziali dell'affermazione sono espliciti o logicamente inferibili dalla fonte.
- contradicted: la fonte afferma il contrario di almeno un elemento essenziale.
- insufficient: la fonte non dimostra l'intera affermazione e non la contraddice esplicitamente.
Riconosci sinonimi tattici dal contesto: un avversario 'rintanato nei pressi dell'area' descrive un blocco basso. Non richiedere identità letterale.
Non confondere finalità strategiche con risultati osservati: 'ricercare un contrattacco' NON dimostra aumento di probabilità di segnare. Non inferire causalità, percentuali, garanzie, 'sempre', 'sicuramente' o superiorità statistica senza prove.
Una frase che contiene sia una parte vera sia una conclusione non dimostrata è INSUFFICIENT, non supported.
Fornisci una breve motivazione e una citazione letterale della fonte quando pertinente. JSON soltanto."""

def atomic(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)

async def main_async(a):
    cases = json.loads(a.gold.read_text(encoding="utf-8"))["cases"]
    signature = [{"id": c["id"], "gold": c["gold"], "claim": c["claim"], "evidence": c["evidence"]} for c in cases]
    if a.output.exists():
        report = json.loads(a.output.read_text(encoding="utf-8"))
        if report.get("input_signature") != signature or report.get("model") != a.model:
            raise ValueError("Existing output incompatible; use a different path")
    else:
        report = {"test": "strict_tactical_claim_nli_experiment_v1", "model": a.model,
                  "input_signature": signature, "rules": RULES,
                  "limitations": ["Exploratory in-sample test: rules explicitly target observed failures q3_03 and q5_04.",
                                  "Do not treat this as independent holdout accuracy.",
                                  "No retrieval quality assessment; context supplied from gold."],
                  "results": []}
    completed = {r["id"] for r in report["results"]}
    llm = NativeOllamaRagasLLM(a.model, a.ollama_url, a.timeout, a.max_tokens)
    n = 0
    for c in cases:
        if c["id"] in completed: continue
        if a.limit and n >= a.limit: break
        start = time.monotonic()
        row = {"id": c["id"], "gold": c["gold"]}
        prompt = RULES + "\n\nFONTE:\n" + c["evidence"] + "\n\nAFFERMAZIONE:\n" + c["claim"]
        try:
            result = await llm.agenerate(prompt, ClaimJudgment)
            obj = result.model_dump()
            row["prediction"] = obj["label"]
            row["rationale"] = obj["rationale"]
            row["evidence_quote"] = obj["evidence_quote"]
            quote = obj["evidence_quote"].strip()
            row["quote_found"] = bool(quote and quote in c["evidence"])
            row["correct_3way"] = obj["label"] == c["gold"]
            row["correct_binary"] = (obj["label"] == "supported") == (c["gold"] == "supported")
        except Exception as exc:
            row["error"] = type(exc).__name__ + ": " + str(exc)[:1200]
        row["elapsed_seconds"] = round(time.monotonic()-start,2)
        report["results"].append(row)
        valid = [r for r in report["results"] if "prediction" in r]
        report["summary"] = {
            "total": len(cases), "completed": len(report["results"]),
            "remaining": len(cases)-len(report["results"]),
            "errors": sum("error" in r for r in report["results"]),
            "accuracy_3way": sum(r["correct_3way"] for r in valid)/len(valid) if valid else None,
            "accuracy_binary": sum(r["correct_binary"] for r in valid)/len(valid) if valid else None,
            "confusion": {gold: {pred: sum(r["gold"]==gold and r["prediction"]==pred for r in valid)
                               for pred in ("supported","contradicted","insufficient")}
                          for gold in ("supported","contradicted","insufficient")}
        }
        atomic(a.output, report)
        print(json.dumps({"id":row["id"],"gold":row["gold"],"prediction":row.get("prediction"),
                          "error":row.get("error"),"seconds":row["elapsed_seconds"]},ensure_ascii=False),flush=True)
        n += 1
        if "error" in row and a.stop_on_error: break
    print("SUMMARY",json.dumps(report.get("summary"),ensure_ascii=False),flush=True)
    print("REPORT",a.output,flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--gold",type=Path,default=Path("projects/tactical-engine/eval/claim_fidelity_gold_v1.json"))
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    p.add_argument("--timeout",type=int,default=180)
    p.add_argument("--max-tokens",type=int,default=1024)
    p.add_argument("--limit",type=int,default=0)
    p.add_argument("--stop-on-error",action="store_true")
    a=p.parse_args()
    asyncio.run(main_async(a))
if __name__=="__main__":main()
