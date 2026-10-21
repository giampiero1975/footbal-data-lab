#!/usr/bin/env python3
"""Trace structured LLM calls inside official Ragas 0.4.3 Faithfulness.

Docs: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/
      https://docs.ollama.com/api/chat
Read-only, two cases, original metric and prompt; trace is observational.
"""
from __future__ import annotations
import argparse
import asyncio
import json
import os
import time
from pathlib import Path
from smoke_ragas_043_native_ollama_v1 import NativeOllamaRagasLLM
from ragas.metrics.collections import Faithfulness

class TracingNativeOllamaLLM(NativeOllamaRagasLLM):
    def __init__(self, *args):
        super().__init__(*args)
        self.calls = []

    def generate(self, prompt, response_model):
        record = {"response_model": getattr(response_model, "__name__", str(response_model)),
                  "prompt": str(prompt), "schema": response_model.model_json_schema()}
        start = time.monotonic()
        try:
            result = super().generate(prompt, response_model)
            record["structured_output"] = result.model_dump(mode="json")
            return result
        except Exception as exc:
            record["error"] = type(exc).__name__ + ": " + str(exc)[:1000]
            raise
        finally:
            record["elapsed_seconds"] = round(time.monotonic() - start, 2)
            self.calls.append(record)

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)

async def run(args):
    gold = json.loads(args.gold.read_text(encoding="utf-8"))
    selected = [c for c in gold["cases"] if c["id"] in {"q3_03", "q5_04"}]
    if len(selected) != 2:
        raise ValueError("Missing q3_03 or q5_04 in gold set")
    report = {"test": "ragas_043_faithfulness_error_trace_v1",
              "model": args.model, "cases": [],
              "note": "Traces Ragas prompts and validated intermediate Pydantic outputs without changing scoring logic."}
    for case in selected:
        llm = TracingNativeOllamaLLM(args.model, args.ollama_url, args.timeout, args.max_tokens)
        metric = Faithfulness(llm=llm)
        row = {"id": case["id"], "gold": case["gold"],
               "claim": case["claim"], "evidence": case["evidence"]}
        start = time.monotonic()
        try:
            result = await metric.ascore(
                user_input="Valuta se l'affermazione è sostenuta dalla fonte.",
                response=case["claim"], retrieved_contexts=[case["evidence"]])
            row["score"] = getattr(result, "value", None)
        except Exception as exc:
            row["error"] = type(exc).__name__ + ": " + str(exc)[:1200]
        row["elapsed_seconds"] = round(time.monotonic() - start, 2)
        row["llm_calls"] = llm.calls
        report["cases"].append(row)
        save(args.output, report)
        print(json.dumps({"id": row["id"], "score": row.get("score"),
                          "error": row.get("error"), "calls": len(llm.calls),
                          "elapsed_seconds": row["elapsed_seconds"]}, ensure_ascii=False), flush=True)
        if "error" in row:
            break
    print("REPORT", args.output, flush=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gold", type=Path,
                   default=Path("projects/tactical-engine/eval/claim_fidelity_gold_v1.json"))
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument("--max-tokens", type=int, default=1024)
    args = p.parse_args()
    asyncio.run(run(args))

if __name__ == "__main__":
    main()
