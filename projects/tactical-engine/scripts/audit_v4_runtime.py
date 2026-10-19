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
        "note": "Collection metadata only, not proof of active runtime pipeline.",
    }, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
