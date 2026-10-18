#!/usr/bin/env python3
"""Benchmark read-only, same Qwen embeddings and identical Chroma candidates."""
import json
import time
from collections import Counter

import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

DB = '/opt/football-data-lab/knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v4_qwen3_embedding_06b'
SOURCE = '334_principi_Glerean'
TESTS = [
    (9, 'Quali sono i compiti dei difensori nel 3-3-4 di Glerean?', '18b453669851'),
    (8, 'Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?', None),
    (7, 'Come viene organizzata la fase di non possesso nel 3-3-4 di Glerean?', 'e61c6b95f769'),
]


def heading(meta):
    raw = meta.get('headings', '[]')
    try:
        value = json.loads(raw) if isinstance(raw, str) else raw
        return ' / '.join(map(str, value))[:83]
    except (TypeError, ValueError):
        return str(raw)[:83]


def rank(model, question, candidates):
    pairs = [(question, x['text']) for x in candidates]
    start = time.perf_counter()
    scores = model.predict(pairs, batch_size=1, show_progress_bar=False)
    elapsed = time.perf_counter() - start
    order = sorted(range(len(candidates)), key=lambda i: float(scores[i]), reverse=True)
    return [(candidates[i], float(scores[i])) for i in order[:5]], elapsed


def print_top(label, ranked, elapsed, gold):
    print(f'  {label} TOP5 | tempo={elapsed:.1f}s', flush=True)
    for i, (c, score) in enumerate(ranked, 1):
        flag = ' [PASSAGGIO ATTESO]' if gold and c['id'].startswith(gold) else ''
        print(f'    {i}. {c["source"]} | {heading(c["meta"])} | {c["id"][:12]} | score={score:.3f}{flag}', flush=True)
    if gold:
        position = next((i for i, (c, _) in enumerate(ranked, 1) if c['id'].startswith(gold)), None)
        print(f'  GOLD IN TOP5: {label} = {position if position else "NO"}', flush=True)


def main():
    client = chromadb.PersistentClient(path=DB)
    coll = client.get_collection(COLLECTION)
    assert coll.count() == 86, f'Collection inattesa: {coll.count()}'
    embedding = OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434')
    print('Caricamento BGE...', flush=True)
    bge = CrossEncoder('BAAI/bge-reranker-v2-m3', device='cpu', max_length=1024)
    print('Caricamento Qwen3-Reranker-0.6B...', flush=True)
    qwen = CrossEncoder('Qwen/Qwen3-Reranker-0.6B', device='cpu', max_length=1024)
    print('Entrambi caricati. Scores NON confrontabili fra modelli.', flush=True)
    for num, question, gold in TESTS:
        vec = embedding.get_query_embedding(question)
        for filtered in (False, True):
            kwargs = {'where': {'source': SOURCE}} if filtered else {}
            result = coll.query(query_embeddings=[vec], n_results=15,
                                include=['documents', 'metadatas', 'distances'], **kwargs)
            candidates = [
                {'id': uid, 'text': doc, 'meta': meta, 'source': meta['source']}
                for uid, doc, meta in zip(result['ids'][0], result['documents'][0], result['metadatas'][0])
            ]
            print('\n' + '=' * 85, flush=True)
            print(f'DOMANDA {num} | filtro_autore={filtered} | {question}', flush=True)
            print(f'DENSE15 fonti={dict(Counter(c["source"] for c in candidates))}', flush=True)
            if gold:
                dense_position = next((i for i, c in enumerate(candidates, 1) if c['id'].startswith(gold)), None)
                print(f'PASSAGGIO ATTESO nei candidati: {dense_position if dense_position else "ASSENTE"}', flush=True)
            for label, model in [('BGE', bge), ('QWEN_RERANKER', qwen)]:
                ranked, elapsed = rank(model, question, candidates)
                print_top(label, ranked, elapsed, gold)
    print('\nFINE: nessuna collection modificata. Q8 richiede ancora verifica del gold.', flush=True)


if __name__ == '__main__':
    main()
