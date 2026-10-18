#!/usr/bin/env python3
"""DRIBBLING V3: Docling official HybridChunker contextualization + Chroma.

Keeps V1/V2 untouched. Run inside the tactical-engine virtualenv.
"""
import hashlib
import json
from pathlib import Path

import chromadb
from docling_core.types.doc import DoclingDocument
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer
from llama_index.embeddings.ollama import OllamaEmbedding

ROOT = Path('/opt/football-data-lab')
INPUTS = [
    ROOT / 'knowledge/processed/formations-and-systems/334_principi_Glerean.json',
    ROOT / 'knowledge/processed/formations-and-systems/il_3412_Giustinetti.json',
]
CHROMA_PATH = ROOT / 'knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v3_contextualized'


def main():
    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True),
        max_tokens=512,
    )
    chunker = HybridChunker(tokenizer=tokenizer, merge_peers=True)
    embedder = OllamaEmbedding(model_name='nomic-embed-text', base_url='http://127.0.0.1:11434')
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(name=COLLECTION, metadata={'hnsw:space': 'cosine'})
    count = 0
    for path in INPUTS:
        if not path.is_file():
            raise FileNotFoundError(path)
        doc = DoclingDocument.model_validate_json(path.read_text(encoding='utf-8'))
        rows = []
        for i, chunk in enumerate(chunker.chunk(dl_doc=doc)):
            contextualized = chunker.contextualize(chunk)
            if not contextualized.strip():
                continue
            pages = sorted({p.page_no for item in chunk.meta.doc_items for p in item.prov})
            source = path.stem
            node_id = hashlib.sha256(f'{source}:{i}:{contextualized}'.encode()).hexdigest()
            rows.append((node_id, contextualized, {
                'source': source,
                'source_json': str(path),
                'page_numbers': json.dumps(pages),
                'headings': json.dumps(chunk.meta.headings or [], ensure_ascii=False),
                'raw_text': chunk.text,
                'chunk_index': i,
                'version': 'v3_contextualized',
            }))
        print(f'{path.name}: {len(rows)} chunks', flush=True)
        for start in range(0, len(rows), 12):
            batch = rows[start:start + 12]
            texts = [r[1] for r in batch]
            vectors = embedder.get_text_embedding_batch(texts, show_progress=False)
            collection.upsert(
                ids=[r[0] for r in batch],
                documents=texts,
                embeddings=vectors,
                metadatas=[r[2] for r in batch],
            )
            count += len(batch)
            print(f'  indexed {min(start + 12, len(rows))}/{len(rows)}', flush=True)
    print(f'DONE: {COLLECTION} / {collection.count()} records; processed {count}', flush=True)
    print('NOTE: V3 uses contextualized text for both embedding and retrieval; no prev/next or docstore yet.')


if __name__ == '__main__':
    main()
