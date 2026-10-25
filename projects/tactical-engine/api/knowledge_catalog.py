#!/usr/bin/env python3
"""Read-only derived catalog for the active Chroma collection."""
from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path


def _pages(value) -> list[int]:
    try:
        parsed = json.loads(value) if isinstance(value, str) else value
        return sorted({int(x) for x in (parsed or [])})
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


def aggregate_rows(collection_name: str, collection_metadata: dict, rows: dict) -> dict:
    sources: dict[str, dict] = {}
    chunks = []
    empty_raw_text = 0
    for identifier, document, metadata in zip(rows["ids"], rows["documents"], rows["metadatas"]):
        source = str(metadata.get("source") or "origine_incompleta")
        pages = _pages(metadata.get("page_numbers"))
        raw_text = str(metadata.get("raw_text") or "")
        if not raw_text.strip():
            empty_raw_text += 1
        item = sources.setdefault(source, {
            "source": source,
            "source_relative": metadata.get("source_relative"),
            "source_pdf": metadata.get("source_pdf"),
            "source_json": metadata.get("source_json"),
            "chunk_count": 0,
            "pages": set(),
            "origin_complete": source != "origine_incompleta" and bool(metadata.get("source_pdf")),
        })
        item["chunk_count"] += 1
        item["pages"].update(pages)
        chunks.append({
            "id": identifier,
            "source": source,
            "source_relative": metadata.get("source_relative"),
            "pages": pages,
            "headings": metadata.get("headings"),
            "chunk_index": metadata.get("chunk_index"),
            "text": document or raw_text,
            "origin_complete": item["origin_complete"],
        })
    documents = []
    for item in sources.values():
        item["pages"] = sorted(item["pages"])
        item["page_count_observed"] = len(item["pages"])
        documents.append(item)
    documents.sort(key=lambda x: x["source"].casefold())
    return {
        "schema": "knowledge_catalog_v1",
        "collection": collection_name,
        "collection_metadata": collection_metadata or {},
        "chunk_count": len(chunks),
        "document_count": len(documents),
        "empty_raw_text_count": empty_raw_text,
        "documents": documents,
        "chunks": chunks,
    }


def load_catalog(chroma_path: Path, collection_name: str) -> dict:
    import chromadb
    collection = chromadb.PersistentClient(path=str(chroma_path)).get_collection(collection_name)
    rows = collection.get(include=["documents", "metadatas"])
    return aggregate_rows(collection_name, collection.metadata or {}, rows)


def search_catalog(catalog: dict, query: str, limit: int = 20) -> list[dict]:
    terms = [term for term in query.casefold().split() if len(term) >= 2]
    if not terms:
        return []
    ranked = []
    for chunk in catalog["chunks"]:
        haystack = " ".join((chunk["source"], str(chunk.get("headings") or ""), chunk["text"])).casefold()
        matches = sum(haystack.count(term) for term in terms)
        if matches:
            ranked.append((matches, chunk))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["source"].casefold(), pair[1]["chunk_index"] or 0))
    return [{**chunk, "lexical_score": score} for score, chunk in ranked[:limit]]
