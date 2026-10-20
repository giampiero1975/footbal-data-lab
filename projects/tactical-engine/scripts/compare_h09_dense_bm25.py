#!/usr/bin/env python3
"""H09 offline semantic-vs-lexical retrieval, no Chroma writes or gold in retrieval.

Uses installed Ollama qwen3-embedding:0.6b via documented /api/embed endpoint.
Only evaluates figure-linked H09 paragraphs, not V4's full 86-chunk corpus.
"""
import argparse
import json
import math
import time
import urllib.error
import urllib.request
from pathlib import Path
from evaluate_h09_lexical import CASES
from probe_h09_lexical_retrieval import rank

def embed(texts, url, model, batch_size, timeout):
    vectors = []
    for start in range(0, len(texts), batch_size):
        payload = json.dumps({"model": model, "input": texts[start:start + batch_size],
                              "truncate": False, "keep_alive": "0"}).encode()
        request = urllib.request.Request(url.rstrip("/") + "/api/embed", data=payload,
                                         headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.load(response)
        chunk = result.get("embeddings")
        if not isinstance(chunk, list) or len(chunk) != len(texts[start:start + batch_size]):
            raise ValueError("Ollama returned unexpected embedding count")
        vectors.extend(chunk)
    return vectors

def cosine(a, b):
    if len(a) != len(b) or not a:
        raise ValueError("Embedding dimensions differ")
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if not na or not nb:
        raise ValueError("Zero embedding norm")
    return sum(x*y for x,y in zip(a,b)) / (na*nb)

def metrics(ids, expected, k):
    pos = ids.index(expected)+1 if expected in ids else None
    return {"rank": pos, "hit_at_1": pos == 1,
            "hit_at_k": pos is not None and pos <= k,
            "reciprocal_rank": round(1/pos, 6) if pos else 0,
            "top_k": ids[:k]}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence", type=Path, required=True)
    p.add_argument("--cases", type=Path)
    p.add_argument("--model", default="qwen3-embedding:0.6b")
    p.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if min(args.batch_size,args.timeout,args.top_k) < 1:
        p.error("batch-size, timeout and top-k must be positive")
    records = json.loads(args.evidence.read_text(encoding="utf-8"))["records"]
    cases = json.loads(args.cases.read_text(encoding="utf-8")) if args.cases else CASES
    if not records or not cases:
        p.error("Evidence and cases must be nonempty")
    start = time.monotonic()
    try:
        vectors = embed([r["text"] for r in records], args.ollama_url, args.model,
                        args.batch_size, args.timeout)
        qvectors = embed([c["query"] for c in cases], args.ollama_url, args.model,
                         args.batch_size, args.timeout)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        p.error(f"Ollama embedding failed: {exc}")
    results = []
    for case, qvector in zip(cases, qvectors):
        expected = case["expected_figure_id"]
        dense = sorted(zip([cosine(qvector, v) for v in vectors], records),
                       key=lambda pair: (-pair[0], str(pair[1].get("id", ""))))
        lexical = rank(case["query"], records, len(records))
        results.append({
            "query": case["query"], "expected_figure_id": expected,
            "bm25": metrics([r["figure_id"] for _,r in lexical], expected, args.top_k),
            "dense": metrics([r["figure_id"] for _,r in dense], expected, args.top_k),
        })
    summary = {}
    for method in ("bm25", "dense"):
        summary[method] = {
            "hit_at_1": sum(row[method]["hit_at_1"] for row in results),
            "hit_at_k": sum(row[method]["hit_at_k"] for row in results),
            "mrr": round(sum(row[method]["reciprocal_rank"] for row in results)/len(results), 6),
        }
    report = {"experiment": "h09_dense_vs_bm25_dev", "model": args.model,
              "corpus_records": len(records), "cases": len(cases), "k": args.top_k,
              "embedding_dimensions": len(vectors[0]),
              "elapsed_seconds": round(time.monotonic()-start, 3),
              "summary": summary, "rows": results,
              "limitations": "Development queries; H09 subset only; no V4 A/B, reranker, answer generation or holdout."}
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        if args.output.resolve() == args.evidence.resolve():
            p.error("Output cannot overwrite evidence")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
