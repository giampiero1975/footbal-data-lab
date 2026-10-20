#!/usr/bin/env python3
"""H09 BM25 + Qwen dense hybrid retrieval using reciprocal rank fusion (RRF).

Read-only; no Chroma writes. Development diagnostic, not independent holdout.
"""
import argparse
import datetime
import hashlib
import json
import subprocess
import time
from pathlib import Path
from compare_h09_dense_bm25 import embed, cosine, metrics
from evaluate_h09_lexical import CASES
from probe_h09_lexical_retrieval import rank

DOCS = ["https://docs.ollama.com/api/embed",
        "https://github.com/QwenLM/Qwen3-Embedding",
        "https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking"]

def rrf(rankings, constant=60):
    if constant < 1:
        raise ValueError("RRF constant must be positive")
    scores = {}
    for ids in rankings:
        for position, doc_id in enumerate(ids, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (constant + position)
    return sorted(scores, key=lambda doc_id: (-scores[doc_id], doc_id))

def self_test():
    assert rrf([["a", "b"], ["b", "a"]]) == ["a", "b"]
    assert rrf([["a", "b"], ["b", "c"]])[0] == "b"
    assert rrf([[], ["a"]]) == ["a"]
    print("SELF_TEST_OK 3")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence", type=Path)
    p.add_argument("--cases", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--model", default="qwen3-embedding:0.6b")
    p.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--rrf-k", type=int, default=60)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.evidence or min(args.batch_size, args.timeout, args.top_k, args.rrf_k) < 1:
        p.error("--evidence and positive batch-size, timeout, top-k, rrf-k required")
    if args.output and args.output.resolve() == args.evidence.resolve():
        p.error("Output cannot overwrite evidence")
    records = json.loads(args.evidence.read_text(encoding="utf-8"))["records"]
    cases = json.loads(args.cases.read_text(encoding="utf-8")) if args.cases else CASES
    if not records or not cases:
        p.error("Nonempty evidence and cases required")
    ids = [r["figure_id"] for r in records]
    if len(ids) != len(set(ids)):
        p.error("Duplicate figure IDs in H09 corpus")
    start = time.monotonic()
    vectors = embed([r["text"] for r in records], args.ollama_url, args.model,
                    args.batch_size, args.timeout)
    queries = embed([c["query"] for c in cases], args.ollama_url, args.model,
                    args.batch_size, args.timeout)
    rows = []
    for case, query_vector in zip(cases, queries):
        dense = [row["figure_id"] for _, row in sorted(
            zip([cosine(query_vector, v) for v in vectors], records),
            key=lambda pair: (-pair[0], str(pair[1]["id"])))]
        lexical = [row["figure_id"] for _, row in rank(case["query"], records, len(records))]
        hybrid = rrf([lexical, dense], args.rrf_k)
        expected = case["expected_figure_id"]
        rows.append({"query": case["query"], "expected_figure_id": expected,
                     "bm25": metrics(lexical, expected, args.top_k),
                     "dense": metrics(dense, expected, args.top_k),
                     "hybrid_rrf": metrics(hybrid, expected, args.top_k)})
    summary = {method: {"hit_at_1": sum(r[method]["hit_at_1"] for r in rows),
                        "hit_at_k": sum(r[method]["hit_at_k"] for r in rows),
                        "mrr": round(sum(r[method]["reciprocal_rank"] for r in rows) / len(rows), 6)}
               for method in ("bm25", "dense", "hybrid_rrf")}
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], check=True,
                                capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        commit = None
    report = {"experiment": "h09_hybrid_rrf_dev", "timestamp_utc": datetime.datetime.now(
        datetime.timezone.utc).isoformat(), "git_commit": commit,
        "evidence_sha256": hashlib.sha256(args.evidence.read_bytes()).hexdigest(),
        "cases_sha256": hashlib.sha256(args.cases.read_bytes()).hexdigest() if args.cases else None,
        "model": args.model, "api": "/api/embed", "ollama_url": args.ollama_url,
        "batch_size": args.batch_size, "timeout_seconds": args.timeout,
        "truncate": False, "keep_alive": "0", "embedding_dimensions": len(vectors[0]),
        "rrf_k": args.rrf_k, "fusion": "RRF of all positive-score BM25 hits and all dense hits",
        "corpus_records": len(records), "cases": len(cases), "top_k": args.top_k,
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "official_documentation": DOCS, "summary": summary, "rows": rows,
        "limitations": "Development queries and 23 H09 figure records only; not V4 A/B, reranking or answer quality."}
    result = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result + "\n", encoding="utf-8")
    print(result)

if __name__ == "__main__":
    main()
