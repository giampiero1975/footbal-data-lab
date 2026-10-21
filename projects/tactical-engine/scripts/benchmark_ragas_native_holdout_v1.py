#!/usr/bin/env python3
"""Holdout benchmark for official Ragas 0.4.3 Faithfulness via native Ollama.

Docs: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/
      https://docs.ollama.com/api/chat
Faithfulness is binary support at claim level; it is NOT a three-way NLI classifier.
Read-only evaluation; checkpoints are written atomically to --output.
"""
from __future__ import annotations
import argparse
import asyncio
import json
import math
import os
import time
from collections import Counter
from pathlib import Path

from smoke_ragas_043_native_ollama_v1 import NativeOllamaRagasLLM
from ragas.metrics.collections import Faithfulness


def save_atomic(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def summarize(cases, results, threshold):
    indexed = {r["id"]: r for r in results}
    valid = [r for r in results if isinstance(r.get("score"), (float, int))
             and math.isfinite(r["score"]) and 0 <= r["score"] <= 1]
    support = [r for r in valid if r["gold"] == "supported"]
    negative = [r for r in valid if r["gold"] != "supported"]
    tp = sum(r["score"] >= threshold for r in support)
    fn = len(support) - tp
    fp = sum(r["score"] >= threshold for r in negative)
    tn = len(negative) - fp
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    return {
        "total": len(cases), "completed": len(results), "valid_scores": len(valid),
        "errors": sum("error" in r for r in results),
        "remaining": sum(c["id"] not in indexed for c in cases),
        "gold_distribution": dict(Counter(c["gold"] for c in cases)),
        "threshold_exploratory": threshold,
        "binary_support_only": {
            "true_positive": tp, "false_negative": fn,
            "false_positive": fp, "true_negative": tn,
            "accuracy_on_valid": (tp + tn) / len(valid) if valid else None,
            "precision": precision, "recall": recall,
            "note": "Contradicted and insufficient are grouped ONLY as not-supported; this is not contradiction detection.",
        },
        "scores_by_gold": {
            label: [r["score"] for r in valid if r["gold"] == label]
            for label in ("supported", "contradicted", "insufficient")
        },
    }


async def main_async(args):
    gold = json.loads(args.gold.read_text(encoding="utf-8"))
    cases = gold["cases"]
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate case IDs")
    signature = [{"id": c["id"], "gold": c["gold"], "claim": c["claim"],
                  "evidence": c["evidence"]} for c in cases]
    if args.output.exists():
        report = json.loads(args.output.read_text(encoding="utf-8"))
        if report.get("input_signature") != signature:
            raise ValueError("Existing report does not match current gold set; choose a different --output")
        if report.get("model") != args.model or report.get("max_tokens") != args.max_tokens:
            raise ValueError("Existing report settings differ; choose a different --output")
    else:
        report = {
            "test": "ragas_043_native_ollama_claim_fidelity_holdout_v1",
            "model": args.model, "max_tokens": args.max_tokens,
            "input_signature": signature,
            "metric": "ragas.metrics.collections.Faithfulness",
            "limitations": [
                "Faithfulness measures evidence support, not three-way contradiction/insufficient classification.",
                "Threshold is exploratory, not calibrated on a separate development set.",
                "16 manually labeled examples are too few for reliable generalization estimates.",
                "Source evidence is provided as retrieved context; retrieval quality is not tested.",
            ],
            "results": [],
        }
    completed = {r["id"] for r in report["results"]}
    metric = Faithfulness(llm=NativeOllamaRagasLLM(args.model, args.ollama_url,
                                                  args.timeout, args.max_tokens))
    count = 0
    for case in cases:
        if case["id"] in completed:
            continue
        if args.limit and count >= args.limit:
            break
        started = time.monotonic()
        row = {"id": case["id"], "gold": case["gold"],
               "source": case.get("source"), "page": case.get("page")}
        try:
            result = await metric.ascore(
                user_input="Valuta se l'affermazione è sostenuta dalla fonte.",
                response=case["claim"],
                retrieved_contexts=[case["evidence"]],
            )
            value = getattr(result, "value", None)
            if not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"Invalid metric score: {value!r}")
            row["score"] = float(value)
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {str(exc)[:1200]}"
        row["elapsed_seconds"] = round(time.monotonic() - started, 2)
        report["results"].append(row)
        report["summary"] = summarize(cases, report["results"], args.threshold)
        save_atomic(args.output, report)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        count += 1
        if "error" in row and args.stop_on_error:
            break
    report["summary"] = summarize(cases, report["results"], args.threshold)
    save_atomic(args.output, report)
    print("SUMMARY", json.dumps(report["summary"], ensure_ascii=False), flush=True)
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
    p.add_argument("--threshold", type=float, default=0.5)
    p.add_argument("--limit", type=int, default=0,
                   help="Run at most N new cases; 0 means all")
    p.add_argument("--stop-on-error", action="store_true")
    args = p.parse_args()
    if not 0 <= args.threshold <= 1:
        p.error("--threshold must be in [0, 1]")
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
