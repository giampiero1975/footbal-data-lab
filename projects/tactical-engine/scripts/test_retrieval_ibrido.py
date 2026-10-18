#!/usr/bin/env python3
"""Test read-only: retrieval V1+V2, BGE e pila senza testi duplicati."""
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
        headings = json.loads(meta.get('headings', '[]'))
        return ' / '.join(map(str, headings)) if headings else '—'
    except (ValueError, TypeError):
        return '—'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--question', type=int, choices=range(1, 6), default=5)
    args = ap.parse_args()

    db = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding = OllamaEmbedding(model_name='nomic-embed-text', base_url='http://127.0.0.1:11434')
    reranker = SentenceTransformerRerank(model='BAAI/bge-reranker-v2-m3', top_n=20, device='cpu')
    filters = MetadataFilters(filters=[ExactMatchFilter(key='source', value=SOURCE)])
    question = QUESTIONS[args.question - 1]
    print(f'DOMANDA {args.question}: {question}', flush=True)

    start = time.monotonic()
    candidates = []
    origins = {}
    for version in ('v1', 'v2'):
        coll = db.get_collection(f'dribbling_tactics_{version}')
        index = VectorStoreIndex.from_vector_store(
            ChromaVectorStore(chroma_collection=coll), embed_model=embedding
        )
        nodes = index.as_retriever(similarity_top_k=10, filters=filters).retrieve(question)
        print(f'{version.upper()}: {len(nodes)} candidati', flush=True)
        for node in nodes:
            origins[node.node.node_id] = version.upper()
        candidates.extend(nodes)

    # Un solo reranker ufficiale sui candidati combinati, senza fusione artigianale dei punteggi.
    ranked = reranker.postprocess_nodes(candidates, query_str=question)

    # Pila ordinata: conserva il primo (score BGE più alto) e salta
    # duplicati testuali esatti o testi interamente contenuti in altri.
    # Non è un algoritmo di similarità: niente soglie arbitrarie o embedding aggiuntivi.
    selected = []
    keys = []
    skipped = 0
    for item in ranked:
        key = re.sub(r'\s+', ' ', item.node.text).strip().casefold()
        source = item.node.metadata.get('source', '')
        duplicate = any(
            source == other_source and
            (key == other_key or (len(key) >= 100 and key in other_key) or
             (len(other_key) >= 100 and other_key in key))
            for other_source, other_key in keys
        )
        if duplicate:
            skipped += 1
            continue
        selected.append(item)
        keys.append((source, key))
        if len(selected) == 5:
            break

    print(f'\nIBRIDO — {len(candidates)} candidati; {len(selected)} risultati distinti; '
          f'{skipped} duplicati saltati; tempo: {time.monotonic()-start:.1f}s', flush=True)
    for rank, item in enumerate(selected, 1):
        meta = item.node.metadata
        excerpt = re.sub(r'\s+', ' ', item.node.get_content()).strip()[:300]
        score = f'{item.score:.3f}' if item.score is not None else '—'
        print(f' {rank}. [{origins.get(item.node.node_id, "?")}] pagina {location(meta)} | sezione: {section(meta)} | score: {score}', flush=True)
        print(f'    {excerpt}', flush=True)
    print('\nTEST COMPLETATO: nessuna modifica agli indici.', flush=True)


if __name__ == '__main__':
    main()
