#!/usr/bin/env python3
"""Confronto read-only V1/V2: retrieval semantico + BGE reranker ufficiale."""
import argparse
import json
import re
import time

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from llama_index.vector_stores.chroma import ChromaVectorStore

CHROMA_PATH = '/opt/football-data-lab/knowledge/rag/chroma'
SOURCE = 'formations-and-systems/il_3412_Giustinetti.json'
QUESTIONS = [
    'Come si organizza il 3-4-1-2 in fase di non possesso?',
    'Come funzionano marcature e coperture difensive nel 3-4-1-2?',
    'Quali sono i compiti difensivi dei centrocampisti esterni?',
    'Come viene organizzato il pressing nel 3-4-1-2?',
    'Qual è il ruolo del trequartista in fase di non possesso?',
]


def location(meta):
    if 'page' in meta:
        return str(meta['page'])
    try:
        items = json.loads(meta.get('doc_items', '[]'))
        pages = sorted({p['page_no'] for item in items for p in item.get('prov', []) if p.get('page_no')})
        return ','.join(map(str, pages)) or '?'
    except (ValueError, TypeError, KeyError):
        return '?'


def section(meta):
    if meta.get('section'):
        return str(meta['section'])
    try:
        h = json.loads(meta.get('headings', '[]'))
        return ' / '.join(map(str, h)) if h else '—'
    except (ValueError, TypeError):
        return '—'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--question', type=int, choices=range(1, 6), help='Una domanda (1-5); default: tutte')
    args = ap.parse_args()
    db = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding = OllamaEmbedding(model_name='nomic-embed-text', base_url='http://127.0.0.1:11434')
    reranker = SentenceTransformerRerank(model='BAAI/bge-reranker-v2-m3', top_n=5, device='cpu')
    indices = {}
    for version in ('v1', 'v2'):
        name = f'dribbling_tactics_{version}'
        coll = db.get_collection(name)
        indices[version] = VectorStoreIndex.from_vector_store(
            ChromaVectorStore(chroma_collection=coll), embed_model=embedding
        )
        print(f'{name}: {coll.count()} record', flush=True)
    filters = MetadataFilters(filters=[ExactMatchFilter(key='source', value=SOURCE)])
    selected = [(i, q) for i, q in enumerate(QUESTIONS, 1) if args.question is None or i == args.question]
    for i, question in selected:
        print(f'\nDOMANDA {i}: {question}', flush=True)
        for version in ('v1', 'v2'):
            start = time.monotonic()
            retriever = indices[version].as_retriever(similarity_top_k=15, filters=filters)
            retrieved = retriever.retrieve(question)
            ranked = reranker.postprocess_nodes(retrieved, query_str=question)
            print(f'\n{version.upper()} — candidati: {len(retrieved)}; rerank: {len(ranked)}; tempo: {time.monotonic()-start:.1f}s', flush=True)
            for rank, item in enumerate(ranked, 1):
                meta = item.node.metadata
                excerpt = re.sub(r'\s+', ' ', item.node.get_content()).strip()[:240]
                print(f' {rank}. pagina {location(meta)} | sezione: {section(meta)} | score: {item.score:.3f}' if item.score is not None else f' {rank}. pagina {location(meta)} | sezione: {section(meta)}', flush=True)
                print(f'    {excerpt}', flush=True)
    print('\nTEST COMPLETATO: nessuna modifica agli indici.', flush=True)


if __name__ == '__main__':
    main()
