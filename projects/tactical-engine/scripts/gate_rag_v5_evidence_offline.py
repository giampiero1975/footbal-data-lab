#!/usr/bin/env python3
"""Offline, read-only gate for V5 deduplicated evidence; consumes existing comparison JSON.

Uses a relative-to-best score gate, not a universal zero threshold: cross-encoder
logits are uncalibrated and may be negative even for useful passages.
"""
import argparse
import json
from pathlib import Path

def gate(report, max_drop=2.0, max_evidence=8):
    output = {"mode": "offline_relative_score_gate", "max_drop": max_drop,
              "max_evidence": max_evidence, "questions": [],
              "limitations": [
                  "Cross-encoder scores are uncalibrated; relative gate is heuristic.",
                  "No claim-level relevance or factual correctness is established.",
                  "Source texts are not included in comparison JSON; human review is still required.",
                  "This report does not regenerate LLM answers or alter ChromaDB."
              ]}
    for q in report["questions"]:
        pool = q["candidate"]
        best = max((r["rerank_score"] for r in pool), default=None)
        floor = best-max_drop if best is not None else None
        kept = [r for r in pool if r["rerank_score"] >= floor][:max_evidence]
        excluded = [r for r in pool if r["id"] not in {k["id"] for k in kept}]
        output["questions"].append({
            "id": q["id"], "best_score": best, "minimum_score": floor,
            "before": len(pool), "after": len(kept),
            "kept": kept, "excluded_by_gate": excluded,
            "warning": "No eligible evidence" if not kept else None
        })
    return output

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--max-drop", type=float, default=2.0)
    args = p.parse_args()
    if args.max_drop < 0:
        p.error("--max-drop must be >= 0")
    report = json.loads(args.input.read_text(encoding="utf-8"))
    result = gate(report, args.max_drop)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    for q in result["questions"]:
        print(f'{q["id"]}: {q["before"]} -> {q["after"]}; threshold={q["minimum_score"]:.3f}')

if __name__ == "__main__":
    main()
