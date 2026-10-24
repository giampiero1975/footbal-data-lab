#!/usr/bin/env python3
"""Read-only trace of page-4 module headings from Docling JSON to frozen V5."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SOURCE = "FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale"
COLLECTION = "dribbling_tactics_v5_multisource"
CHROMA = Path("/opt/football-data-lab/knowledge/rag/chroma")
BODY_MARKERS = {
    "4-3-3": "Il vertice basso è spesso il principale equilibrio",
    "4-4-2": "Le due punte offrono riferimenti",
    "3-5-2": "I quinti possono essere sbocchi di ripartenza",
    "3-4-2-1": "I due trequartisti possono ricevere immediatamente",
}


def page_numbers(item: dict) -> list[int]:
    return sorted({
        prov["page_no"] for prov in item.get("prov", [])
        if isinstance(prov, dict) and isinstance(prov.get("page_no"), int)
    })


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--processed-json", required=True, type=Path,
                    help="Docling JSON produced by ingest_pdfs.py for the source PDF")
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    if not args.processed_json.is_file():
        ap.error(f"Missing Docling JSON: {args.processed_json}")
    if args.output.exists():
        ap.error(f"Output already exists: {args.output}")

    document = json.loads(args.processed_json.read_text(encoding="utf-8"))
    source_items = []
    for index, item in enumerate(document.get("texts", [])):
        text = (item.get("text") or "").strip()
        pages = page_numbers(item)
        if not text or 4 not in pages:
            continue
        source_items.append({
            "index": index,
            "self_ref": item.get("self_ref") or f"#/texts/{index}",
            "parent": item.get("parent"),
            "label": item.get("label"),
            "text": text,
            "pages": pages,
        })

    import chromadb

    collection = chromadb.PersistentClient(path=str(CHROMA)).get_collection(COLLECTION)
    count_before = collection.count()
    if count_before != 5319:
        raise RuntimeError(f"Frozen V5 count mismatch: expected 5319, got {count_before}")
    records = collection.get(where={"source": SOURCE}, include=["documents", "metadatas"])
    page4_chunks = []
    for identifier, text, metadata in zip(records["ids"], records["documents"], records["metadatas"]):
        raw_pages = metadata.get("page_numbers", "[]")
        try:
            pages = json.loads(raw_pages) if isinstance(raw_pages, str) else raw_pages
        except (TypeError, json.JSONDecodeError):
            pages = []
        if 4 not in (pages or []):
            continue
        headings = metadata.get("headings", "[]")
        try:
            headings = json.loads(headings) if isinstance(headings, str) else headings
        except (TypeError, json.JSONDecodeError):
            headings = headings
        page4_chunks.append({
            "id": identifier,
            "pages": pages,
            "headings": headings,
            "raw_text": metadata.get("raw_text") or text,
        })

    matches = {}
    for module, marker in BODY_MARKERS.items():
        matches[module] = [row for row in page4_chunks if marker in row["raw_text"]]
        if len(matches[module]) != 1:
            raise RuntimeError(f"Expected one page-4 chunk for {module} body, got {len(matches[module])}")

    count_after = collection.count()
    if count_after != count_before:
        raise RuntimeError(f"Frozen V5 count changed: {count_before} -> {count_after}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "v5-fresh03-heading-loss-trace-v1",
        "source": SOURCE,
        "processed_json": str(args.processed_json),
        "source_page": 4,
        "source_page_text_items": source_items,
        "module_body_matches": matches,
        "page4_indexed_chunks": page4_chunks,
        "chroma_count_before": count_before,
        "chroma_count_after": count_after,
        "index_unchanged": True,
        "note": "Read-only trace. No retrieval, embeddings, generation, or index writes.",
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"SOURCE_ITEMS={len(source_items)} PAGE4_CHUNKS={len(page4_chunks)} "
          f"MODULE_BODIES={len(matches)} INDEX_UNCHANGED=true REPORT={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
