#!/usr/bin/env python3
"""Inspect the installed Ragas 0.4.3 LLM adapter contract without inference.

Official API reference: https://docs.ragas.io/en/v0.4.3/
Ollama native chat reference: https://docs.ollama.com/api/chat
This probe reads local Python objects only and does not alter the environment.
"""
from __future__ import annotations
import argparse
import importlib
import inspect
import json
from pathlib import Path

TARGETS = [
    ("ragas.llms", "InstructorBaseRagasLLM"),
    ("ragas.llms", "llm_factory"),
    ("ragas.metrics.collections", "Faithfulness"),
    ("ragas.llms.base", "BaseRagasLLM"),
]

def describe(module_name, symbol):
    try:
        obj = getattr(importlib.import_module(module_name), symbol)
        out = {"available": True, "module": getattr(obj, "__module__", module_name),
               "signature": str(inspect.signature(obj))}
        if inspect.isclass(obj):
            out["mro"] = [c.__module__ + "." + c.__name__ for c in inspect.getmro(obj)]
            out["abstract_methods"] = sorted(getattr(obj, "__abstractmethods__", ()))
            out["methods"] = {}
            for method in ("generate", "agenerate", "generate_text", "agenerate_text",
                           "ascore", "score", "from_config", "create", "acomplete"):
                if hasattr(obj, method):
                    fn = getattr(obj, method)
                    try:
                        out["methods"][method] = str(inspect.signature(fn))
                    except (ValueError, TypeError):
                        out["methods"][method] = "signature unavailable"
            out["annotations"] = {k: str(v) for k, v in getattr(obj, "__annotations__", {}).items()}
        return out
    except Exception as exc:
        return {"available": False, "error": type(exc).__name__ + ": " + str(exc)[:500]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = {"purpose": "Inspect Ragas 0.4.3 adapter interface before implementing a native Ollama adapter",
              "targets": {f"{module}.{symbol}": describe(module, symbol) for module, symbol in TARGETS},
              "references": ["https://docs.ragas.io/en/v0.4.3/",
                             "https://docs.ollama.com/api/chat"],
              "no_inference": True, "no_modifications": True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
