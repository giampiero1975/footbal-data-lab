#!/usr/bin/env python3
"""DRIBBLING: benchmark read-only nomic vs Qwen3-Embedding 0.6B.

Same 86 contextualized passages, independent query embeddings, Chroma top15,
identical official LlamaIndex SentenceTransformerRerank top5. No LLM generation.
Scores are not comparable as absolute quality. Review relevant source IDs manually.
"""
from __future__ import annotations
import argparse
import json
import re
import time
from pathlib import Path

import chromadb
from llama_index.core.schema import NodeWithScore, QueryBundle, TextNode
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank

DB = '/opt/football-data-lab/knowledge/rag/chroma'
CONFIGS = (
    ('NOMIC', 'dribbling_tactics_v3_contextualized', 'nomic-embed-text'),
    ('QWEN_06B', 'dribbling_tactics_v4_qwen3_embedding_06b', 'qwen3-embedding:0.6b'),
)
QUESTIONS = (
    ('Gustinetti', 'Come si organizza il 3-4-1-2 in fase di non possesso?'),
    ('Gustinetti', 'Come funzionano marcature e coperture difensive nel 3-4-1-2?'),
    ('Gustinetti', 'Quali sono i compiti difensivi dei centrocampisti esterni?'),
    ('Gustinetti', 'Come viene organizzato il pressing nel 3-4-1-2?'),
    ('Gustinetti', 'Qual è il ruolo del trequartista in fase di non possesso?'),
    ('Glerean', 'Quali sono i principi fondamentali del sistema 3-3-4 di Ezio Glerean?'),
    ('Glerean', 'Come viene organizzata la fase di non possesso nel 3-3-4 di Glerean?'),
    ('Glerean', 'Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?'),
    ('Glerean', 'Quali sono i compiti dei difensori nel 3-3-4 di Glerean?'),
    ('Glerean', 'Come viene affrontata la riconquista del pallone nel 3-3-4 di Glerean?'),
)

def field(meta, key):
    try:
        x = json.loads(meta.get(key, '[]'))
        return ' / '.join(map(str, x)) if x else '—'
    except (ValueError, TypeError):
        return str(meta.get(key, '—'))

def retrieve(coll, embedder, reranker, question, k, top):
    started = time.monotonic()
    vector = embedder.get_query_embedding(question)
    data = coll.query(query_embeddings=[vector], n_results=k,
                      include=['documents', 'metadatas', 'distances'])
    candidates = [NodeWithScore(node=TextNode(id_=uid, text=doc, metadata=meta or {}),
                                score=1.0-dist)
                  for uid, doc, meta, dist in zip(data['ids'][0], data['documents'][0],
                                                   data['metadatas'][0], data['distances'][0])]
    ranked = reranker.postprocess_nodes(candidates, query_bundle=QueryBundle(query_str=question))
    return data['ids'][0], ranked[:top], time.monotonic()-started

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--question', type=int, choices=range(1, 11))
    p.add_argument('--candidates', type=int, default=15)
    p.add_argument('--top', type=int, default=5)
    p.add_argument('--output', default='/opt/football-data-lab/projects/tactical-engine/benchmark_embedding_v3_v4.txt')
    args = p.parse_args()
    db = chromadb.PersistentClient(path=DB)
    collections = {}
    embeddings = {}
    for label, collection_name, model in CONFIGS:
        coll = db.get_collection(collection_name)
        if coll.count() != 86:
            raise RuntimeError(f'{label}: expected 86 records, found {coll.count()}')
        collections[label] = coll
        embeddings[label] = OllamaEmbedding(model_name=model, base_url='http://127.0.0.1:11434')
    ids = [set(collections[label].get()['ids']) for label, _, _ in CONFIGS]
    if ids[0] != ids[1]:
        raise RuntimeError('Collections do not contain identical IDs')
    reranker = SentenceTransformerRerank(model='BAAI/bge-reranker-v2-m3', top_n=args.top, device='cpu')
    output = []
    def log(s=''):
        print(s, flush=True)
        output.append(s)
    log('DRIBBLING — retrieval benchmark: 86 identical IDs, separate query embeddings, BGE top5')
    numbers = [args.question] if args.question else range(1, len(QUESTIONS)+1)
    for number in numbers:
        author, question = QUESTIONS[number-1]
        log(f'\n{"="*75}\nDOMANDA {number} [{author}]: {question}')
        results = {}
        for label, _, model in CONFIGS:
            candidate_ids, ranked, seconds = retrieve(collections[label], embeddings[label], reranker,
                                                       question, args.candidates, args.top)
            results[label] = (candidate_ids, [node.node.node_id for node in ranked])
            log(f'\n{label} ({model}) | {seconds:.1f}s | top-{args.candidates} -> BGE top-{args.top}')
            for pos, node in enumerate(ranked, 1):
                m = node.node.metadata or {}
                text = re.sub(r'\s+', ' ', node.node.get_content()).strip()
                log(f'  {pos}. ID={node.node.node_id} | BGE={node.score:.3f} | '
                    f'source={m.get("source", "?")} | pages={field(m,"page_numbers")} | '
                    f'heading={field(m,"headings")}')
                log('     '+text[:600])
        a, b = results['NOMIC'], results['QWEN_06B']
        log(f'\nOVERLAP: dense top-{args.candidates} {len(set(a[0])&set(b[0]))}/{args.candidates}; '
            f'BGE top-{args.top} {len(set(a[1])&set(b[1]))}/{args.top}')
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(output)+'\n', encoding='utf-8')
    log('\nCOMPLETATO. Interpretare i risultati rispetto ai passaggi attesi, non al valore BGE.')
    Path(args.output).write_text('\n'.join(output)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
