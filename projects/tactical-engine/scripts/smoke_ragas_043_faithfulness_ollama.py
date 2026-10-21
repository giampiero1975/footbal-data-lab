#!/usr/bin/env python3
"""Minimal, isolated Ragas 0.4.3 Faithfulness smoke test with local Ollama.

References:
https://docs.ragas.io/en/v0.4.3/howtos/migrations/migrate_from_v03_to_v04/
https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/
https://docs.ollama.com/openai
No production writes, downloads, or package installations.
"""
from __future__ import annotations
import argparse
import asyncio
import json
import time
from pathlib import Path

async def run(args):
    from openai import AsyncOpenAI
    from ragas.llms import llm_factory
    from ragas.metrics.collections import Faithfulness
    client = AsyncOpenAI(base_url=args.ollama_url.rstrip("/") + "/v1/",
                         api_key="ollama", timeout=args.timeout, max_retries=0)
    llm = llm_factory(args.model, provider="openai", client=client)
    metric = Faithfulness(llm=llm)
    cases = [
        {"id": "supported", "user_input": "Quale condizione favorisce la profondità?",
         "response": "Lo spazio dietro la linea difensiva favorisce la ricerca della profondità.",
         "retrieved_contexts": ["Se vi è spazio alle spalle della difesa avversaria, è possibile ricercare la profondità."]},
        {"id": "unsupported", "user_input": "Quale condizione favorisce la profondità?",
         "response": "Una difesa bassa lascia sempre ampio spazio alle proprie spalle.",
         "retrieved_contexts": ["Se la squadra avversaria difende vicino alla propria area, la profondità è difficile da attaccare e si preferisce l'ampiezza."]}
    ]
    results = []
    for case in cases:
        started = time.monotonic()
        row = {"id": case["id"]}
        try:
            result = await metric.ascore(user_input=case["user_input"],
                                         response=case["response"],
                                         retrieved_contexts=case["retrieved_contexts"])
            row["score"] = getattr(result, "value", None)
            row["result_repr"] = str(result)[:1200]
        except Exception as exc:
            row["error"] = type(exc).__name__ + ": " + str(exc)[:1500]
        row["elapsed_seconds"] = round(time.monotonic() - started, 2)
        results.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        if "error" in row:
            break
    return results

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    p.add_argument("--timeout", type=float, default=240)
    args = p.parse_args()
    report = {"test": "ragas_0_4_3_official_faithfulness_smoke",
              "model": args.model, "ollama_url": args.ollama_url,
              "note": "Two synthetic cases test integration, not metric accuracy.",
              "results": asyncio.run(run(args))}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("REPORT", args.output)

if __name__ == "__main__":
    main()
