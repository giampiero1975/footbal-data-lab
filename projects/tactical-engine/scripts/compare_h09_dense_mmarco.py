#!/usr/bin/env python3
"""Read-only H09 dense top-N vs mMARCO reranking; development diagnostics only."""
import argparse
import datetime
import hashlib
import json
import subprocess
import time
from pathlib import Path
from compare_h09_dense_bm25 import embed, cosine, metrics
from evaluate_h09_lexical import CASES

MODEL = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
DOCS = ["https://www.sbert.net/docs/cross_encoder/usage/usage.html",
        "https://sbert.net/docs/package_reference/cross_encoder/model.html",
        "https://docs.ollama.com/api/embed"]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence", type=Path, required=True)
    p.add_argument("--cases", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--top-n", type=int, default=15)
    p.add_argument("--top-k", type=int, default=5)
    args = p.parse_args()
    if args.top_n < 1 or args.top_k < 1:
        p.error("top-n and top-k must be positive")
    if args.output.resolve() == args.evidence.resolve():
        p.error("Output cannot overwrite evidence")
    from sentence_transformers import CrossEncoder
    from importlib.metadata import version
    records = json.loads(args.evidence.read_text(encoding="utf-8"))["records"]
    cases = json.loads(args.cases.read_text(encoding="utf-8")) if args.cases else CASES
    if not records or not cases:
        p.error("Evidence and cases must be nonempty")
    start = time.monotonic()
    vectors = embed([r["text"] for r in records], "http://127.0.0.1:11434",
                    "qwen3-embedding:0.6b", 4, 120)
    qvectors = embed([c["query"] for c in cases], "http://127.0.0.1:11434",
                     "qwen3-embedding:0.6b", 4, 120)
    reranker = CrossEncoder(MODEL, device="cpu", max_length=512)
    rows = []
    for case, qv in zip(cases, qvectors):
        dense = sorted(zip([cosine(qv, v) for v in vectors], records),
                       key=lambda pair: (-pair[0], str(pair[1].get("id", ""))))
        candidates = dense[:args.top_n]
        scores = reranker.predict([(case["query"], row["text"]) for _, row in candidates],
                                  batch_size=1, show_progress_bar=False)
        reranked = sorted(zip(scores, candidates),
                          key=lambda pair: (-float(pair[0]), str(pair[1][1].get("id", ""))))
        expected = case["expected_figure_id"]
        rows.append({"query": case["query"], "expected_figure_id": expected,
                     "dense": metrics([row["figure_id"] for _, row in dense], expected, args.top_k),
                     "dense_mmarco": metrics([item[1][1]["figure_id"] for item in reranked],
                                            expected, args.top_k),
                     "rerank_candidate_count": len(candidates)})
    summary = {method: {"hit_at_1": sum(r[method]["hit_at_1"] for r in rows),
                        "hit_at_k": sum(r[method]["hit_at_k"] for r in rows),
                        "mrr": round(sum(r[method]["reciprocal_rank"] for r in rows) / len(rows), 6)}
               for method in ("dense", "dense_mmarco")}
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                                text=True, check=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        commit = None
    report = {"experiment": "h09_dense_mmarco_dev",
              "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "git_commit": commit, "evidence_sha256": hashlib.sha256(args.evidence.read_bytes()).hexdigest(),
              "cases_sha256": hashlib.sha256(args.cases.read_bytes()).hexdigest() if args.cases else None,
              "embedding_model": "qwen3-embedding:0.6b", "reranker_model": MODEL,
              "sentence_transformers_version": version("sentence-transformers"),
              "reranker_device": "cpu", "reranker_max_length": 512, "reranker_batch_size": 1,
              "dense_candidate_top_n": args.top_n, "top_k": args.top_k,
              "corpus_records": len(records), "cases": len(cases),
              "elapsed_seconds": round(time.monotonic()-start, 3),
              "official_documentation": DOCS, "summary": summary, "rows": rows,
              "limitations": "3 development cases; H09 figure-only corpus; no independent holdout or V4 A/B."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
