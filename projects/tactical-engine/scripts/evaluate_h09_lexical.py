#!/usr/bin/env python3
"""Read-only H09 retrieval evaluation with manually specified expected figure IDs.

Evaluation labels are never used by the retriever. This is a small diagnostic
suite, not an unbiased holdout and not an answer-quality metric.
"""
import argparse
import json
from pathlib import Path
from probe_h09_lexical_retrieval import rank

CASES = [
    {"query": "Come si dispongono gli attaccanti quando recuperiamo palla in difesa?",
     "expected_figure_id": "15/a"},
    {"query": "Qual è il ruolo del portiere e dei difensori in appoggio?",
     "expected_figure_id": "15/b"},
    {"query": "Come si muovono i compagni quando conquistiamo palla in attacco?",
     "expected_figure_id": "17"},
]


def evaluate(records, cases, k):
    rows = []
    for case in cases:
        results = rank(case["query"], records, top_k=max(k, len(records)))
        ids = [r.get("figure_id") for _, r in results]
        expected = case["expected_figure_id"]
        position = ids.index(expected) + 1 if expected in ids else None
        rows.append({
            "query": case["query"], "expected_figure_id": expected,
            "rank": position, "top_k": ids[:k],
            "hit_at_1": position == 1, "hit_at_k": position is not None and position <= k,
            "reciprocal_rank": round(1 / position, 6) if position else 0,
        })
    n = len(rows)
    return {"cases": n, "k": k, "hit_at_1": sum(r["hit_at_1"] for r in rows),
            "hit_at_k": sum(r["hit_at_k"] for r in rows),
            "mrr": round(sum(r["reciprocal_rank"] for r in rows) / n, 6) if n else 0,
            "rows": rows, "warning": "Development diagnostics only; not independent holdout."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence", required=True, type=Path)
    p.add_argument("--cases", type=Path, help="Optional JSON array of query and expected_figure_id")
    p.add_argument("--top-k", type=int, default=5)
    args = p.parse_args()
    if args.top_k < 1:
        p.error("--top-k must be >= 1")
    records = json.loads(args.evidence.read_text(encoding="utf-8"))["records"]
    cases = json.loads(args.cases.read_text(encoding="utf-8")) if args.cases else CASES
    for case in cases:
        if not isinstance(case.get("query"), str) or not isinstance(case.get("expected_figure_id"), str):
            p.error("Each case requires query and expected_figure_id strings")
    print(json.dumps(evaluate(records, cases, args.top_k), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
