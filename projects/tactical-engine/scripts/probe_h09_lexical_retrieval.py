#!/usr/bin/env python3
"""H09 offline lexical retrieval baseline (not semantic embedding retrieval).

BM25-style ranking on original paragraph text only. No gold, no index writes.
"""
import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

TOKEN = re.compile(r"[^\W_]+", re.UNICODE)
STOP = set("""a ad al alla allo ai agli alle anche che chi con da dal dalla dei del della
di e ed è gli i il in la le lo ma nei nel nella non o per più quale quali
quando se si su sul sulla tra un una uno come cosa sono viene viene""".split())


def tokens(s):
    return [w for w in TOKEN.findall(s.casefold()) if len(w) >= 3 and w not in STOP]


def rank(query, records, top_k=5):
    docs = [Counter(tokens(r.get("text", ""))) for r in records]
    n = len(docs)
    if not n:
        return []
    avg = sum(sum(d.values()) for d in docs) / n or 1
    df = Counter()
    for d in docs:
        df.update(d.keys())
    q = set(tokens(query))
    scored = []
    for row, counts in zip(records, docs):
        score = 0.0
        length = sum(counts.values())
        for term in q:
            freq = counts.get(term, 0)
            if not freq:
                continue
            idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            score += idf * freq * 2.2 / (freq + 1.2 * (0.25 + 0.75 * length / avg))
        if score > 0:
            scored.append((score, row))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("id", ""))))
    return scored[:top_k]


def self_test():
    rows = [{"id": "a", "text": "Gli attaccanti mantengono una posizione centrale"},
            {"id": "b", "text": "Il portiere resta in appoggio ai difensori"}]
    assert rank("posizione centrale degli attaccanti", rows)[0][1]["id"] == "a"
    assert rank("appoggio del portiere", rows)[0][1]["id"] == "b"
    assert rank("calcio d'angolo", rows) == []
    print("SELF_TEST_OK 3")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence", type=Path)
    p.add_argument("--query", action="append")
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.evidence or not args.query or args.top_k < 1:
        p.error("--evidence, --query and --top-k >= 1 required")
    data = json.loads(args.evidence.read_text(encoding="utf-8"))
    records = data.get("records", [])
    for query in args.query:
        results = rank(query, records, args.top_k)
        print(json.dumps({"query": query, "method": "lexical_bm25_baseline",
                          "corpus_records": len(records),
                          "results": [{"score": round(score, 4), "figure_id": row.get("figure_id"),
                                       "page": row.get("figure_page"),
                                       "paragraph_ref": row.get("paragraph_ref"),
                                       "text_preview": row.get("text", "")[:220]}
                                      for score, row in results]}, ensure_ascii=False))
    print("LIMITATION: lexical H09-only baseline; not semantic retrieval or V4 A/B.")


if __name__ == "__main__":
    main()
