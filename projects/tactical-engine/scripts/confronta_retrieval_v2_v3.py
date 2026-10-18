#!/usr/bin/env python3
"""DRIBBLING: confronto read-only V2/V3, 5 domande, embedding e BGE identici.

Usa Chroma query ufficiale e SentenceTransformerRerank di LlamaIndex.
Non modifica gli indici e non introduce ranking, filtri semantici o chunker custom.
"""
import argparse
import json
import re
import time

import chromadb
from llama_index.core.schema import NodeWithScore, QueryBundle, TextNode
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank

PATH = '/opt/football-data-lab/knowledge/rag/chroma'
COLLECTIONS = {
    'V2': 'dribbling_tactics_v2',
    'V3': 'dribbling_tactics_v3_contextualized',
}
QUESTIONS = [
    'Come si organizza il 3-4-1-2 in fase di non possesso?',
    'Come funzionano marcature e coperture difensive nel 3-4-1-2?',
    'Quali sono i compiti difensivi dei centrocampisti esterni?',
    'Come viene organizzato il pressing nel 3-4-1-2?',
    'Qual è il ruolo del trequartista in fase di non possesso?',
]


def pages(metadata):
    if metadata.get('page_numbers'):
        try:
            return ','.join(map(str, json.loads(metadata['page_numbers']))) or '?'
        except (ValueError, TypeError):
            pass
    if metadata.get('page'):
        return str(metadata['page'])
    try:
        items = json.loads(metadata.get('doc_items', '[]'))
        nums = sorted({p['page_no'] for item in items for p in item.get('prov', []) if p.get('page_no')})
        return ','.join(map(str, nums)) or '?'
    except (ValueError, TypeError, KeyError):
        return '?'


def headings(metadata):
    try:
        h = json.loads(metadata.get('headings', '[]'))
        return ' / '.join(map(str, h)) if h else '—'
    except (ValueError, TypeError):
        return str(metadata.get('section', '—'))


def run_one(collection, question, embedding, reranker, k, top):
    start = time.monotonic()
    result = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=['documents', 'metadatas', 'distances'],
    )
    candidates = [
        NodeWithScore(node=TextNode(id_=nid, text=doc, metadata=meta or {}), score=1.0 - dist)
        for nid, doc, meta, dist in zip(
            result['ids'][0], result['documents'][0],
            result['metadatas'][0], result['distances'][0]
        )
    ]
    ranked = reranker.postprocess_nodes(candidates, query_bundle=QueryBundle(query_str=question))
    return ranked[:top], time.monotonic() - start


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--question', type=int, choices=range(1, 6), help='Solo una domanda (1-5)')
    parser.add_argument('--candidates', type=int, default=15)
    parser.add_argument('--top', type=int, default=5)
    args = parser.parse_args()

    db = chromadb.PersistentClient(path=PATH)
    collections = {name: db.get_collection(coll) for name, coll in COLLECTIONS.items()}
    for name, coll in collections.items():
        print(f'{name}: {coll.count()} record | {COLLECTIONS[name]}', flush=True)
    embedder = OllamaEmbedding(model_name='nomic-embed-text', base_url='http://127.0.0.1:11434')
    reranker = SentenceTransformerRerank(model='BAAI/bge-reranker-v2-m3', top_n=args.top, device='cpu')
    numbers = [args.question] if args.question else range(1, 6)
    for number in numbers:
        question = QUESTIONS[number - 1]
        print(f'\n{"=" * 78}\nDOMANDA {number}: {question}', flush=True)
        # Stesso vettore di query per entrambi gli indici: confronto controllato.
        vector = embedder.get_query_embedding(question)
        for version, collection in collections.items():
            ranked, elapsed = run_one(collection, question, vector, reranker, args.candidates, args.top)
            print(f'\n{version}: {len(ranked)} risultati | retrieval + BGE: {elapsed:.1f}s', flush=True)
            for i, item in enumerate(ranked, 1):
                m = item.node.metadata
                excerpt = re.sub(r'\s+', ' ', item.node.text).strip()[:430]
                print(f'  {i}. score={item.score:.3f} | pagina={pages(m)} | sezione={headings(m)}', flush=True)
                print(f'     {excerpt}', flush=True)
    print('\nFINE: nessuna modifica agli indici. I punteggi BGE non sono voti di qualità.', flush=True)


if __name__ == '__main__':
    main()
