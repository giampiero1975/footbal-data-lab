#!/usr/bin/env python3
"""Read-only Ragas 0.4.x API inspection; no LLM calls or mutations.

Official references:
https://docs.ragas.io/en/v0.4.3/howtos/migrations/migrate_from_v03_to_v04/
https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/
"""
from __future__ import annotations
import importlib
import importlib.metadata
import inspect
import json
from pathlib import Path
import argparse

def describe(module_name, attr):
    try:
        module = importlib.import_module(module_name)
        obj = getattr(module, attr)
        return {"available": True, "module": module_name,
                "signature": str(inspect.signature(obj)),
                "ascore": str(inspect.signature(obj.ascore)) if hasattr(obj, "ascore") else None,
                "score": str(inspect.signature(obj.score)) if hasattr(obj, "score") else None}
    except Exception as exc:
        return {"available": False, "error": type(exc).__name__ + ": " + str(exc)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = {"ragas_version": importlib.metadata.version("ragas"),
              "checks": {
                  "collections.Faithfulness": describe("ragas.metrics.collections", "Faithfulness"),
                  "ragas.llms.llm_factory": describe("ragas.llms", "llm_factory"),
                  "ragas.metrics.Faithfulness_legacy": describe("ragas.metrics", "Faithfulness"),
                  "openai.AsyncOpenAI": describe("openai", "AsyncOpenAI")
              },
              "no_inference": True, "no_installation": True,
              "official_docs": [
                  "https://docs.ragas.io/en/v0.4.3/howtos/migrations/migrate_from_v03_to_v04/",
                  "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/"
              ]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
