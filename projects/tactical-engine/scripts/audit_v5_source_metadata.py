#!/usr/bin/env python3
"""Read-only metadata inventory for the existing Chroma V5 collection."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path

DEFAULT_DB = Path("/opt/football-data-lab/knowledge/rag/chroma")
DEFAULT_COLLECTION = "dribbling_tactics_v5_multisource"

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--collection", default=DEFAULT_COLLECTION)
    p.add_argument("--batch-size", type=int, default=500)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    if a.batch_size < 1:
        p.error("--batch-size must be positive")
    if not a.db.is_dir():
        p.error(f"Database directory not found: {a.db}")
    if a.output.exists():
        p.error(f"Refusing overwrite: {a.output}")
    import chromadb
    col = chromadb.PersistentClient(path=str(a.db)).get_collection(a.collection)
    before = col.count()
    sources = Counter()
    types = defaultdict(Counter)
    examples = {}
    pages = {}
    missing = Counter()
    scanned = 0
    while scanned < before:
        result = col.get(limit=min(a.batch_size, before - scanned), offset=scanned,
                         include=["metadatas"])
        ids, metas = result["ids"], result["metadatas"]
        if not ids or metas is None or len(ids) != len(metas):
            raise RuntimeError(f"Invalid batch at offset {scanned}/{before}")
        for rid, meta in zip(ids, metas):
            meta = meta or {}
            for key in ("source", "source_relative", "page_numbers", "raw_text"):
                if key not in meta or meta[key] is None:
                    missing[key] += 1
                else:
                    types[key][type(meta[key]).__name__] += 1
            source = meta.get("source")
            if isinstance(source, str) and source:
                sources[source] += 1
                examples.setdefault(source, {
                    "record_id": rid, "source_relative": meta.get("source_relative"),
                    "page_numbers": meta.get("page_numbers")})
            page = meta.get("page_numbers")
            if page is not None:
                pages.setdefault(type(page).__name__, str(page)[:180])
        scanned += len(ids)
    after = col.count()
    if scanned != before or after != before:
        raise RuntimeError(f"Collection count drift: {before}, {scanned}, {after}")
    report = {
        "schema": "v5_source_metadata_audit_v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "db": str(a.db), "collection": a.collection,
        "count_before": before, "scanned": scanned, "count_after": after,
        "index_unchanged": True, "distinct_sources": len(sources),
        "sources": [{"source": s, "count": n, "example": examples[s]}
                    for s, n in sorted(sources.items())],
        "field_types": {k: dict(v) for k, v in types.items()},
        "missing_fields": dict(missing), "page_examples_by_type": pages,
        "notes": ["Metadata only; no embedding, LLM, or collection mutations.",
                  "Gold source titles are not validated Chroma filter values.",
                  "page_numbers may refer to PDF rather than printed pages."]}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str),
                        encoding="utf-8")
    print(f"REPORT {a.output}", flush=True)
    print(f"RECORDS {scanned} SOURCES {len(sources)} INDEX_UNCHANGED true", flush=True)

if __name__ == "__main__":
    main()
