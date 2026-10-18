#!/usr/bin/env python3
"""DRIBBLING: clone V3 texts/metadata into a separate Qwen3-Embedding collection.

The source collection is read-only. No PDF extraction, chunking or LLM generation.
"""
from __future__ import annotations

import argparse
import time

import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding

DB_PATH = '/opt/football-data-lab/knowledge/rag/chroma'
SOURCE = 'dribbling_tactics_v3_contextualized'
TARGET = 'dribbling_tactics_v4_qwen3_embedding_06b'
MODEL = 'qwen3-embedding:0.6b'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch-size', type=int, default=4)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error('--batch-size must be >= 1')

    db = chromadb.PersistentClient(path=DB_PATH)
    src = db.get_collection(SOURCE)
    data = src.get(include=['documents', 'metadatas'])
    ids = data['ids']
    docs = data['documents']
    metas = data['metadatas']
    if len(ids) != 86 or len(set(ids)) != len(ids):
        raise RuntimeError(f'Unexpected source count/duplicate IDs: {len(ids)}')
    if any(not isinstance(doc, str) or not doc.strip() for doc in docs):
        raise RuntimeError('Empty or invalid source document')
    if any(meta is None for meta in metas):
        raise RuntimeError('Missing source metadata')

    existing = {c.name for c in db.list_collections()}
    if TARGET in existing:
        raise RuntimeError(f'Target collection already exists: {TARGET}. Refusing to overwrite.')

    print(f'Source: {SOURCE} ({len(ids)} records)', flush=True)
    print(f'Target: {TARGET}', flush=True)
    print(f'Embedding: {MODEL}', flush=True)
    embedder = OllamaEmbedding(model_name=MODEL, base_url='http://127.0.0.1:11434')
    target = db.create_collection(
        name=TARGET,
        metadata={'description': 'DRIBBLING V3 contextualized texts embedded with Qwen3-Embedding 0.6B',
                  'embedding_model': MODEL, 'source_collection': SOURCE},
    )
    start = time.monotonic()
    expected_dim = None
    for offset in range(0, len(ids), args.batch_size):
        stop = min(offset + args.batch_size, len(ids))
        batch_docs = docs[offset:stop]
        vectors = embedder.get_text_embedding_batch(batch_docs, show_progress=False)
        if len(vectors) != len(batch_docs):
            raise RuntimeError('Embedding count mismatch')
        dimensions = {len(v) for v in vectors}
        if len(dimensions) != 1:
            raise RuntimeError(f'Inconsistent embedding dimensions: {dimensions}')
        dim = dimensions.pop()
        if expected_dim is None:
            expected_dim = dim
            print(f'Embedding dimension: {dim}', flush=True)
        elif dim != expected_dim:
            raise RuntimeError('Embedding dimension changed between batches')
        target.add(ids=ids[offset:stop], documents=batch_docs,
                   metadatas=metas[offset:stop], embeddings=vectors)
        print(f'Indexed {stop}/{len(ids)} in {time.monotonic()-start:.1f}s', flush=True)

    check = target.get(include=['documents', 'metadatas'])
    if target.count() != len(ids):
        raise RuntimeError('Target record count mismatch')
    source_map = {key: (doc, meta) for key, doc, meta in zip(ids, docs, metas)}
    for key, doc, meta in zip(check['ids'], check['documents'], check['metadatas']):
        if source_map[key] != (doc, meta):
            raise RuntimeError(f'Text or metadata mismatch for {key}')
    print(f'PASS: {target.count()} identical IDs/texts/metadata; new embeddings {expected_dim}D.', flush=True)
    print(f'Completed in {time.monotonic()-start:.1f}s. V3 unchanged.', flush=True)


if __name__ == '__main__':
    main()
