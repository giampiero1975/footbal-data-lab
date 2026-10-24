#!/usr/bin/env python3
"""DRIBBLING V5: incremental Docling multi-document index with Qwen3 embeddings.

Default is read-only dry-run. --write creates/resumes a NEW V5 collection.
Never modifies or deletes V1-V4 collections. Existing V5 IDs are verified
and skipped, rather than overwritten. Fail closed on changed source content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("/opt/football-data-lab")
PROCESSED = ROOT / "knowledge/processed"
CHROMA = ROOT / "knowledge/rag/chroma"
COLLECTION = "dribbling_tactics_v5_multisource"
EMBED_MODEL = "qwen3-embedding:0.6b"
TOKENIZER_MODEL = "nomic-ai/nomic-embed-text-v1.5"
MAX_TOKENS = 512


def inputs_under(root: Path) -> list[Path]:
    return sorted(
        p for p in root.rglob("*.json")
        if not p.name.endswith(".meta.json")
        and p.name != "images.json"
        and not any(part.endswith("_images") for part in p.relative_to(root).parts)
    )


def build_rows(paths: list[Path], root: Path, source_root: Path):
    from docling_core.types.doc import DoclingDocument
    from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
    from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
    from transformers import AutoTokenizer

    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(TOKENIZER_MODEL, trust_remote_code=True),
        max_tokens=MAX_TOKENS,
    )
    chunker = HybridChunker(tokenizer=tokenizer, merge_peers=True)
    ids_seen: set[str] = set()
    for path in paths:
        relative = path.relative_to(root).as_posix()
        try:
            doc = DoclingDocument.model_validate_json(path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise RuntimeError(f"Invalid Docling JSON {relative}: {exc}") from exc
        count = 0
        for index, chunk in enumerate(chunker.chunk(dl_doc=doc)):
            contextualized = chunker.contextualize(chunk).strip()
            if not contextualized:
                continue
            pages = sorted({p.page_no for item in chunk.meta.doc_items for p in item.prov})
            identifier = hashlib.sha256(
                f"{relative}:{index}:{contextualized}".encode("utf-8")
            ).hexdigest()
            if identifier in ids_seen:
                raise RuntimeError(f"Duplicate ID: {identifier}")
            ids_seen.add(identifier)
            metadata = {
                "source": path.stem,
                "source_json": str(path),
                "source_relative": relative,
                "source_pdf": str((source_root / relative).with_suffix(".pdf")),
                "page_numbers": json.dumps(pages),
                "headings": json.dumps(chunk.meta.headings or [], ensure_ascii=False),
                "raw_text": chunk.text,
                "chunk_index": index,
                "version": "v5_multisource",
                "embedding_model": EMBED_MODEL,
            }
            count += 1
            yield identifier, contextualized, metadata
        print(f"[CHUNKED] {relative}: {count}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="Create/resume V5 (default: dry-run)")
    ap.add_argument("--processed", type=Path, default=PROCESSED)
    ap.add_argument("--source-root", type=Path, default=ROOT / "knowledge/sources")
    ap.add_argument("--collection", default=COLLECTION)
    ap.add_argument("--baseline-collection", help="Copy an immutable baseline into a new candidate before adding inputs")
    ap.add_argument("--batch-size", type=int, default=4)
    args = ap.parse_args()
    if args.batch_size < 1:
        ap.error("--batch-size must be >= 1")
    root = args.processed.expanduser().resolve()
    source_root = args.source_root.expanduser().resolve()
    if not root.is_dir():
        ap.error(f"Missing processed directory: {root}")
    paths = inputs_under(root)
    if not paths:
        ap.error(f"No Docling JSON found under {root}")

    print(f"Documents: {len(paths)}; target: {COLLECTION}; model: {EMBED_MODEL}", flush=True)
    if not args.write:
        total = sum(1 for _ in build_rows(paths, root, source_root))
        if not total:
            raise RuntimeError("No chunks generated")
        print(f"DRY RUN PASS: {len(paths)} documents, {total} chunks. Chroma untouched.", flush=True)
        return 0

    import chromadb
    from llama_index.embeddings.ollama import OllamaEmbedding

    db = chromadb.PersistentClient(path=str(CHROMA))
    existing_names = {c.name for c in db.list_collections()}
    if args.baseline_collection == args.collection:
        ap.error("baseline and target collection must differ")
    if args.collection in existing_names:
        collection = db.get_collection(args.collection)
        meta = collection.metadata or {}
        if meta.get("embedding_model") != EMBED_MODEL or meta.get("pipeline") != "v5_multisource":
            raise RuntimeError("Existing V5 metadata incompatible; refusing to modify")
    else:
        collection = db.create_collection(
            args.collection,
            metadata={"hnsw:space": "cosine", "embedding_model": EMBED_MODEL,
                      "pipeline": "v5_multisource"},
        )

    embedder = OllamaEmbedding(model_name=EMBED_MODEL, base_url="http://127.0.0.1:11434")
    batch = []
    skipped = 0
    inserted = 0
    expected_ids = set()
    if args.baseline_collection:
        if args.baseline_collection not in existing_names:
            raise RuntimeError(f"Missing baseline collection: {args.baseline_collection}")
        baseline = db.get_collection(args.baseline_collection)
        baseline_rows = baseline.get(include=["documents", "metadatas", "embeddings"])
        expected_ids.update(baseline_rows["ids"])
        target_ids = set(collection.get(include=[])["ids"])
        missing = [i for i, identifier in enumerate(baseline_rows["ids"]) if identifier not in target_ids]
        for start in range(0, len(missing), 64):
            positions = missing[start:start + 64]
            collection.add(
                ids=[baseline_rows["ids"][i] for i in positions],
                documents=[baseline_rows["documents"][i] for i in positions],
                metadatas=[baseline_rows["metadatas"][i] for i in positions],
                embeddings=[baseline_rows["embeddings"][i] for i in positions],
            )
        print(f"[BASELINE] source={args.baseline_collection} expected={len(baseline_rows['ids'])} copied={len(missing)}", flush=True)

    def flush():
        nonlocal inserted
        if not batch:
            return
        vectors = embedder.get_text_embedding_batch(
            [row[1] for row in batch], show_progress=False
        )
        if len(vectors) != len(batch) or len({len(v) for v in vectors}) != 1:
            raise RuntimeError("Invalid embedding batch")
        collection.add(
            ids=[row[0] for row in batch],
            documents=[row[1] for row in batch],
            metadatas=[row[2] for row in batch],
            embeddings=vectors,
        )
        inserted += len(batch)
        print(f"[INDEXED] new={inserted} skipped={skipped}", flush=True)
        batch.clear()

    for identifier, document, metadata in build_rows(paths, root, source_root):
        expected_ids.add(identifier)
        previous = collection.get(ids=[identifier], include=["documents", "metadatas"])
        if previous["ids"]:
            if previous["documents"][0] != document or previous["metadatas"][0] != metadata:
                raise RuntimeError(f"Existing record differs: {identifier}")
            skipped += 1
            continue
        batch.append((identifier, document, metadata))
        if len(batch) >= args.batch_size:
            flush()
    flush()
    actual = set(collection.get(include=[])["ids"])
    if actual != expected_ids:
        raise RuntimeError(
            f"V5 content mismatch: expected={len(expected_ids)} actual={len(actual)} "
            f"missing={len(expected_ids - actual)} unexpected={len(actual - expected_ids)}"
        )
    print(f"PASS V5: documents={len(paths)} chunks={len(actual)} "
          f"new={inserted} existing={skipped}; V1-V4 untouched.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
