#!/usr/bin/env python3
"""EXP-001: A/B read-only Qwen query instruction on existing V4 Chroma collection.

No LLM generation, index writes, installs or model pulls. Prints JSON to stdout.
Run ONLY after confirming runtime collection and model configuration.
Gold prefixes below are provisional; metrics are diagnostic, not final quality.
"""
from __future__ import annotations

import argparse
import json
import statistics
import time

import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding

DB = "/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION = "dribbling_tactics_v4_qwen3_embedding_06b"
MODEL = "qwen3-embedding:0.6b"
INSTRUCTION = (
    "Retrieve relevant passages from football tactical manuals that answer "
    "the question accurately, respecting the named coach and playing system."
)
# Manually selected in earlier diagnostic scripts; NOT independently validated.
TESTS = [
    ("Come si organizza la fase di non possesso nel 3-4-1-2 di Gustinetti?",
     "il_3412_Giustinetti", ["ff52244de23c", "9068a7891f59", "4c72fea6b689"]),
    ("Come funzionano marcature e coperture difensive nel 3-4-1-2 di Gustinetti?",
     "il_3412_Giustinetti", ["9068a7891f59", "42c668c42537", "4c72fea6b689"]),
    ("Quali sono i compiti difensivi dei centrocampisti esterni nel 3-4-1-2 di Gustinetti?",
     "il_3412_Giustinetti", ["4c72fea6b689", "83bbed4b4422"]),
    ("Come funziona il pressing nel 3-4-1-2 di Gustinetti?",
     "il_3412_Giustinetti", ["270557ceb70c", "cf37545a89ed"]),
    ("Qual è il ruolo del trequartista in fase di non possesso nel 3-4-1-2 di Gustinetti?",
     "il_3412_Giustinetti", ["494bfdf47f21", "ff52244de23c"]),
    ("Come viene organizzata la fase di non possesso nel 3-3-4 di Glerean?",
     "334_principi_Glerean", ["e61c6b95f769"]),
    ("Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?",
     "334_principi_Glerean", []),
    ("Quali sono i compiti dei difensori nel 3-3-4 di Glerean?",
     "334_principi_Glerean", ["18b453669851"]),
    ("Come avviene la riconquista del pallone nel 3-3-4 di Glerean?",
     "334_principi_Glerean", ["efba60713930", "e61c6b95f769"]),
]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=DB)
    ap.add_argument("--collection", default=COLLECTION)
    ap.add_argument("--top-k", type=int, default=15)
    ap.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    args = ap.parse_args()
    if args.top_k < 1:
        ap.error("--top-k must be positive")

    collection = chromadb.PersistentClient(path=args.db).get_collection(args.collection)
    if collection.count() != 86:
        raise RuntimeError(f"Expected 86 chunks, found {collection.count()}; aborting")
    # Verify the provisional IDs before interpreting retrieval metrics.\n    known_ids = collection.get(include=[])['ids']\n    for question, source, gold in TESTS:\n        for prefix in gold:\n            matches = [item for item in known_ids if item.startswith(prefix)]\n            if len(matches) != 1:\n                raise RuntimeError(f'Gold prefix {prefix} matches {len(matches)} IDs for {question!r}')\n    embed = OllamaEmbedding(model_name=MODEL, base_url=args.ollama_url)
    results = []
    for question, source, gold in TESTS:
        row = {"question": question, "source": source, "gold_prefixes": gold}
        for variant, query in (
            ("baseline", question),
            ("instruct", f"Instruct: {INSTRUCTION}\nQuery:{question}"),
        ):
            started = time.perf_counter()
            vector = embed.get_query_embedding(query)
            embedding_seconds = time.perf_counter() - started
            started = time.perf_counter()
            out = collection.query(
                query_embeddings=[vector],
                n_results=args.top_k,
                where={"source": source},
                include=["metadatas", "distances"],
            )
            search_seconds = time.perf_counter() - started
            ids = out["ids"][0]
            ranks = [
                rank for rank, chunk_id in enumerate(ids, 1)
                if any(chunk_id.startswith(prefix) for prefix in gold)
            ]
            row[variant] = {
                "returned": len(ids),
                "ids": ids,
                "first_gold_rank": min(ranks) if ranks else None,
                "gold_prefix_recall": (sum(
                    any(chunk_id.startswith(prefix) for chunk_id in ids)
                    for prefix in gold
                ) / len(gold)) if gold else None,
                "embedding_seconds": round(embedding_seconds, 3),
                "search_seconds": round(search_seconds, 3),
            }
        results.append(row)
    summary = {}
    for variant in ("baseline", "instruct"):
        summary[variant] = {
            "mean_recall_at_k": statistics.mean(r[variant]["gold_prefix_recall"] for r in results if r[variant]["gold_prefix_recall"] is not None),
            "mrr_first_gold": statistics.mean(
                1 / r[variant]["first_gold_rank"] if r[variant]["first_gold_rank"] else 0
                for r in results
            ),
            "mean_embedding_seconds": statistics.mean(
                r[variant]["embedding_seconds"] for r in results
            ),
        }
    print(json.dumps({
        "experiment": "EXP-001", "read_only": True,
        "collection": args.collection, "count": collection.count(),
        "model": MODEL, "top_k": args.top_k,
        "instruction": INSTRUCTION,
        "warning": "Gold prefixes copied exactly from historical reranker benchmark, still provisional; Q8 excluded from gold metrics; no reranker or semantic assessment.",
        "summary": summary, "questions": results,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
