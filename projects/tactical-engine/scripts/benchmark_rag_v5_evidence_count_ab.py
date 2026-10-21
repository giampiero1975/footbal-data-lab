#!/usr/bin/env python3
"""Controlled read-only generation test: 8 baseline vs gated deduplicated evidence.

Inputs: existing V5 retrieval comparison JSON and offline gate JSON.
Reuses the exact baseline prompt and Ollama chat options from the original A/B.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
import time

import chromadb
from benchmark_rag_v5_prompt_ab import BASELINE, COLLECTION, DB, chat

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--comparison", type=Path, required=True)
    p.add_argument("--gate", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--questions", nargs="+", default=["q3", "q4", "q5"])
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--timeout", type=int, default=900)
    args = p.parse_args()
    comparison = json.loads(args.comparison.read_text(encoding="utf-8"))
    gate = json.loads(args.gate.read_text(encoding="utf-8"))
    if comparison["collection"] != COLLECTION or comparison.get("count_before") != 5319:
        raise RuntimeError("Unexpected comparison collection/count")
    coll = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    if coll.count() != 5319:
        raise RuntimeError("Unexpected current V5 count")
    gate_by_id = {q["id"]: q for q in gate["questions"]}
    report = {"collection": COLLECTION, "model": args.model, "prompt": BASELINE,
              "count_before": coll.count(), "questions": [],
              "limitations": ["Citation syntax is not factual correctness.",
                              "This compares existing 8-slot evidence against gated evidence; it does not tune the gate.",
                              "Fewer passages can omit useful minority evidence; inspect answers and source text."]}
    def save():
        report["count_after"] = coll.count()
        report["index_unchanged"] = report["count_before"] == report["count_after"]
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    try:
        for q in comparison["questions"]:
            if q["id"] not in args.questions:
                continue
            g = gate_by_id[q["id"]]
            variants = {"baseline_8": q["baseline"], "dedup_gated": g["kept"]}
            all_ids = list(dict.fromkeys(r["id"] for rows in variants.values() for r in rows))
            fetched = coll.get(ids=all_ids, include=["documents", "metadatas"])
            by_id = {cid: (doc, meta) for cid, doc, meta in zip(fetched["ids"], fetched["documents"], fetched["metadatas"])}
            entry = {"id": q["id"], "question": q["question"], "variants": {}}
            report["questions"].append(entry)
            save()
            for name, selected in variants.items():
                evidence = []
                for r in selected:
                    doc, meta = by_id[r["id"]]
                    if meta.get("source") != r["source"]:
                        raise RuntimeError(f"Source mismatch: {r['id']}")
                    evidence.append({"id": r["id"], "source": r["source"],
                                     "pages": meta.get("page_numbers"), "text": doc,
                                     "rerank_score": r["rerank_score"]})
                print("START", q["id"], name, len(evidence), flush=True)
                started = time.monotonic()
                answer, stats = chat(args.model, BASELINE, q["question"], evidence, args.timeout)
                cited = sorted({int(n) for n in re.findall(r"\[F(\d+)\]", answer)})
                entry["variants"][name] = {"evidence": evidence, "answer": answer,
                    "citation_ids": cited,
                    "invalid_citation_ids": [n for n in cited if n < 1 or n > len(evidence)],
                    "elapsed_seconds": round(time.monotonic()-started, 2), "generation": stats}
                save()
                print("DONE", q["id"], name, entry["variants"][name]["elapsed_seconds"], flush=True)
    except (Exception, KeyboardInterrupt) as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        save()
        raise
    save()
    print("PASS: controlled generation completed; V5 unchanged =", report["index_unchanged"], flush=True)

if __name__ == "__main__":
    main()
