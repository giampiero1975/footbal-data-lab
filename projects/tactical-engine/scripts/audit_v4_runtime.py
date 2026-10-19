#!/usr/bin/env python3
"""Inspect existing Chroma V3/V4 metadata; no index mutations or Ollama calls.

Chroma PersistentClient may write internal housekeeping files. Run on existing DB.
Does not inspect active processes, query prompts or document content.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import math
from pathlib import Path

import chromadb

DEFAULT_DB = "/opt/football-data-lab/knowledge/rag/chroma"
COLLECTIONS = ("dribbling_tactics_v3_contextualized",
               "dribbling_tactics_v4_qwen3_embedding_06b")


def inspect_collection(client, name):
    try:
        coll = client.get_collection(name)
    except Exception as exc:
        return {"name": name, "status": "unavailable", "error_type": type(exc).__name__}
    count = coll.count()
    data = {"name": name, "status": "found", "count": count,
            "metadata": coll.metadata,
            "configuration": getattr(coll, "configuration", None)}
    sources, ids = Counter(), set()
    for offset in range(0, count, 100):
        batch = coll.get(limit=100, offset=offset, include=["metadatas"])
        for chunk_id, meta in zip(batch["ids"], batch["metadatas"] or []):
            ids.add(chunk_id)
            sources[str((meta or {}).get("source", "<missing>"))] += 1
    # Vector norms are diagnostic; sampling does not prove whole-collection normalization.
    sample = coll.get(limit=min(20, count), include=["embeddings"]) if count else None
    vectors = sample["embeddings"] if sample is not None else None
    if vectors is not None and len(vectors):
        norms = [math.sqrt(sum(float(x) ** 2 for x in vector)) for vector in vectors]
        data["embedding_sample"] = {
            "size": len(norms), "dimensions": sorted({len(v) for v in vectors}),
            "min_l2_norm": round(min(norms), 6),
            "max_l2_norm": round(max(norms), 6),
            "max_abs_deviation_from_unit": round(max(abs(n - 1.0) for n in norms), 6),
        }
    data.update(source_counts=dict(sorted(sources.items())),
                unique_ids=len(ids), expected_count_86=(count == 86))
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=DEFAULT_DB)
    args = parser.parse_args()
    if not Path(args.db).is_dir():
        parser.error("Chroma directory missing: refusing to create a new database")
    client = chromadb.PersistentClient(path=args.db)
    print(json.dumps({
        "audit": "V4-READONLY",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "db_path": args.db, "chromadb_version": chromadb.__version__,
        "collections": [inspect_collection(client, name) for name in COLLECTIONS],
        "note": "Collection metadata and a 20-vector norm sample; not proof of active runtime pipeline.",
    }, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
