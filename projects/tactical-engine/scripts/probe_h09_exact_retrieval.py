#!/usr/bin/env python3
"""H09 read-only exact-reference retrieval probe, no embeddings or production index.

This is a deterministic smoke test, NOT a semantic RAG benchmark.
"""
import argparse
import json
import re
from pathlib import Path

FIG = re.compile(r"(?i)\b(?:fig(?:ura|ure|g)?\.?|schema|diagramma)\s*(?:n\.?\s*)?(\d{1,3}(?:\s*[/\\.-]\s*[a-z])?)\b")

def normalize(value):
    return re.sub(r"\s+", "", value.lower()).replace("\\", "/").replace(".", "/")

def self_test():
    cases = {"Spiega la Fig.15/a": ["15/a"], "Spiega la Fig.15/b": ["15/b"],
             "Spiega la Fig.17": ["17"], "Spiega fig.15\\\\a": ["15/a"]}
    for query, expected in cases.items():
        actual = [normalize(v) for v in FIG.findall(query)]
        if actual != expected:
            raise AssertionError(f"{query!r}: expected {expected}, got {actual}")
    print("SELF_TEST_OK", len(cases))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence", type=Path)
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--query", action="append")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.evidence or not args.query:
        p.error("--evidence and --query are required unless --self-test")
    data = json.loads(args.evidence.read_text(encoding="utf-8"))
    rows = data.get("records", [])
    for q in args.query:
        ids = {normalize(v) for v in FIG.findall(q)}
        hits = [r for r in rows if r.get("figure_id") in ids]
        print(json.dumps({"query": q, "figure_ids": sorted(ids),
                          "matches": len(hits),
                          "results": [{"id": r.get("id"), "figure_id": r.get("figure_id"),
                                       "page": r.get("figure_page"),
                                       "paragraph_ref": r.get("paragraph_ref"),
                                       "text_preview": r.get("text", "")[:260]}
                                      for r in hits]}, ensure_ascii=False))
    print("LIMITATION: Exact figure lookup only; semantic retrieval and answer quality untested.")

if __name__ == "__main__":
    main()
