#!/usr/bin/env python3
"""Benchmark read-only: Qwen embedding + Chroma identical candidates; BGE vs mMARCO.
Gold passages are provisional and manually selected; Q8 deliberately has no gold.
"""
import json
import statistics
import time
from collections import Counter

import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

DB = '/opt/football-data-lab/knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v4_qwen3_embedding_06b'
GLEREAN = '334_principi_Glerean'
GUSTINETTI = 'il_3412_Giustinetti'
TOP_K = 15
TESTS = [
    (1, 'Come si organizza la fase di non possesso nel 3-4-1-2 di Gustinetti?', GUSTINETTI, ['ff52244de23c', '9068a7891f59', '4c72fea6b689']),
    (2, 'Come funzionano marcature e coperture difensive nel 3-4-1-2 di Gustinetti?', GUSTINETTI, ['9068a7891f59', '42c668c42537', '4c72fea6b689']),
    (3, 'Quali sono i compiti difensivi dei centrocampisti esterni nel 3-4-1-2 di Gustinetti?', GUSTINETTI, ['4c72fea6b689', '83bbed4b4422']),
    (4, 'Come funziona il pressing nel 3-4-1-2 di Gustinetti?', GUSTINETTI, ['270557ceb70c', 'cf37545a89ed']),
    (5, 'Qual è il ruolo del trequartista in fase di non possesso nel 3-4-1-2 di Gustinetti?', GUSTINETTI, ['494bfdf47f21', 'ff52244de23c']),
    (7, 'Come viene organizzata la fase di non possesso nel 3-3-4 di Glerean?', GLEREAN, ['e61c6b95f769']),
    (8, 'Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?', GLEREAN, []),
    (9, 'Quali sono i compiti dei difensori nel 3-3-4 di Glerean?', GLEREAN, ['18b453669851']),
    (10, 'Come avviene la riconquista del pallone nel 3-3-4 di Glerean?', GLEREAN, ['efba60713930', 'e61c6b95f769']),
]


def heading(meta):
    raw = meta.get('headings', '[]')
    try:
        h = json.loads(raw) if isinstance(raw, str) else raw
        return ' / '.join(map(str, h))[:85] if isinstance(h, list) else str(h)[:85]
    except (ValueError, TypeError):
        return str(raw)[:85]


def score_model(model, question, candidates):
    start = time.perf_counter()
    scores = model.predict([(question, c['text']) for c in candidates], batch_size=1, show_progress_bar=False)
    elapsed = time.perf_counter() - start
    order = sorted(range(len(candidates)), key=lambda i: float(scores[i]), reverse=True)
    return [(candidates[i], float(scores[i])) for i in order], elapsed


def gold_rank(ranked, gold):
    return min((i for i, (c, _) in enumerate(ranked, 1) if any(c['id'].startswith(g) for g in gold)), default=None)


def main():
    client = chromadb.PersistentClient(path=DB)
    coll = client.get_collection(COLLECTION)
    if coll.count() != 86:
        raise RuntimeError(f'Collection inattesa: {coll.count()} invece di 86')
    embedding = OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434')
    print('Carico BGE...', flush=True)
    bge = CrossEncoder('BAAI/bge-reranker-v2-m3', device='cpu', max_length=512)
    print('Carico mMARCO MiniLM...', flush=True)
    mmarco = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', device='cpu', max_length=512)
    models = [('BGE', bge), ('mMARCO', mmarco)]
    stats = {name: {'times': [], 'rr': [], 'hits': 0, 'gold_tests': 0, 'foreign': []} for name, _ in models}
    print('Stesso embedding, stessi 15 candidati e max_length=512 per entrambi.', flush=True)
    print('Gold provvisori; Q8 senza gold; punteggi tra modelli NON confrontabili.', flush=True)
    for number, question, source, gold in TESTS:
        t0 = time.perf_counter()
        vec = embedding.get_query_embedding(question)
        embed_seconds = time.perf_counter() - t0
        # Filtered test is the production-like condition. Unfiltered Q7/Q9 also probes contamination.
        for filtered in ([True, False] if number in (7, 9) else [True]):
            opts = {'where': {'source': source}} if filtered else {}
            t0 = time.perf_counter()
            result = coll.query(query_embeddings=[vec], n_results=TOP_K, include=['documents', 'metadatas'], **opts)
            chroma_seconds = time.perf_counter() - t0
            candidates = [dict(id=i, text=d, source=m['source'], meta=m)
                          for i, d, m in zip(result['ids'][0], result['documents'][0], result['metadatas'][0])]
            print('\n' + '=' * 100, flush=True)
            print(f'Q{number} | filtro_autore={filtered} | {question}', flush=True)
            print(f'Embedding={embed_seconds:.2f}s | Chroma={chroma_seconds:.3f}s | fonti={dict(Counter(c["source"] for c in candidates))}', flush=True)
            dense_gold = min((i for i, c in enumerate(candidates, 1) if any(c['id'].startswith(g) for g in gold)), default=None)
            print(f'GOLD dense15: {dense_gold if gold else "NON DEFINITO"}', flush=True)
            for name, model in models:
                ranked, seconds = score_model(model, question, candidates)
                first_gold = gold_rank(ranked, gold) if gold else None
                foreign = sum(c['source'] != source for c, _ in ranked[:5])
                print(f'  {name} | {seconds:.2f}s | gold_rank={first_gold if gold else "NON DEFINITO"} | gold@5={bool(first_gold and first_gold <= 5) if gold else "N/D"} | fonti_estranee_top5={foreign}', flush=True)
                for j, (c, score) in enumerate(ranked[:5], 1):
                    marker = ' [GOLD]' if any(c['id'].startswith(g) for g in gold) else ''
                    print(f'    {j}. {c["source"]} | {heading(c["meta"])} | {c["id"][:12]} | score={score:.3f}{marker}', flush=True)
                # Summary only for filtered trials; unfiltered cases are diagnostic.
                if filtered:
                    st = stats[name]
                    st['times'].append(seconds)
                    st['foreign'].append(foreign)
                    if gold:
                        st['gold_tests'] += 1
                        st['hits'] += bool(first_gold and first_gold <= 5)
                        st['rr'].append(1.0 / first_gold if first_gold else 0.0)
    print('\n' + '#' * 100, flush=True)
    print('RIEPILOGO: solo test filtrati, gold provvisori (non valutazione definitiva della qualità)', flush=True)
    for name, st in stats.items():
        print(f'{name}: media_tempo={statistics.mean(st["times"]):.2f}s | mediana_tempo={statistics.median(st["times"]):.2f}s | '
              f'gold_hit@5={st["hits"]}/{st["gold_tests"]} | MRR={statistics.mean(st["rr"]):.3f} | '
              f'fonti_estranee_top5={sum(st["foreign"])}', flush=True)
    print('FINE. Read-only: nessuna collection modificata.', flush=True)


if __name__ == '__main__':
    main()
