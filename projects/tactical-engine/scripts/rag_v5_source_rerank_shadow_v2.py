#!/usr/bin/env python3
"""Read-only comparison of global and source-filtered V5 mMARCO reranking.

No generation, no changes to Chroma, no gold used in retrieval/ranking.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import time

DB = Path('/opt/football-data-lab/knowledge/rag/chroma')
COLLECTION = 'dribbling_tactics_v5_multisource'
ALIASES = {
    'Allegati_222010155625': 'LA TECNICA APPLICATA COME PRESUPPOSTO DEL GIOCO COLLETTIVO',
    'Allegati_45201211489': 'Conseiderazione sul sistema di gioco 4-3-2-1',
    'Allegati_71201095736': 'IL CONCETTO DI MARCAMENTO NELLA DIFESA AD UOMO E A ZONA',
    'Categoria_Tattiche del calcio - Wikipedia(1)': 'Categoria_Tattiche del calcio - Wikipedia',
}
CASES = [
    {'id': 'ussia_4a', 'question': 'Nell’esercitazione 4/A di Ussia quale limite temporale è previsto?', 'source': 'Transizioni.Ussia'},
    {'id': 'foscarini_b', 'question': 'Perché per Foscarini è rischioso costruire attraverso i laterali nella zona B?', 'source': 'manovre_offensive_vari_sistemi_gioco_Foscarini'},
    {'id': 'foscarini_centro', 'question': 'Secondo Foscarini che ruolo ha il centrocampista centrale nella zona B?', 'source': 'manovre_offensive_vari_sistemi_gioco_Foscarini'},
]

def norm(value: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', value.casefold())).strip()

def convert(result):
    rows = []
    for rid, doc, meta, dist in zip(result['ids'][0], result['documents'][0], result['metadatas'][0], result['distances'][0]):
        meta = meta or {}
        raw = meta.get('raw_text') or doc or ''
        rows.append({'id': rid, 'source': meta.get('source'), 'pages': meta.get('page_numbers'),
                     'source_relative': meta.get('source_relative'), 'text': doc or '',
                     'distance': float(dist), 'fingerprint': hashlib.sha256(norm(raw).encode()).hexdigest()})
    return rows

def select(question, rows, reranker, limit=8):
    if not rows:
        return []
    scores = reranker.predict([(question, r['text']) for r in rows], batch_size=1, show_progress_bar=False)
    ranked = sorted(range(len(rows)), key=lambda i: (-float(scores[i]), rows[i]['id']))
    seen = set()
    selected = []
    for i in ranked:
        r = rows[i]
        canonical = ALIASES.get(r['source'], r['source'])
        key = (canonical, r['fingerprint'])
        if key in seen:
            continue
        seen.add(key)
        selected.append({'rank': len(selected)+1, 'id': r['id'], 'source': r['source'],
                         'pages': r['pages'], 'distance': round(r['distance'], 6),
                         'rerank_score': round(float(scores[i]), 6), 'text': r['text']})
        if len(selected) >= limit:
            break
    return selected

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db', type=Path, default=DB)
    p.add_argument('--collection', default=COLLECTION)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--top-k', type=int, default=24)
    p.add_argument('--limit', type=int, default=8)
    a = p.parse_args()
    if a.output.exists(): p.error(f'Refusing overwrite: {a.output}')
    if not a.db.is_dir(): p.error(f'Chroma directory missing: {a.db}')
    if a.top_k < 1 or not 1 <= a.limit <= a.top_k: p.error('Require top-k >= limit >= 1')
    import chromadb
    from llama_index.embeddings.ollama import OllamaEmbedding
    from sentence_transformers import CrossEncoder
    coll = chromadb.PersistentClient(path=str(a.db)).get_collection(a.collection)
    before = coll.count()
    if before != 5319: raise RuntimeError(f'Unexpected collection count {before}')
    embed = OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434')
    reranker = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', device='cpu', max_length=512)
    report = {'schema': 'rag_v5_source_rerank_shadow_v2', 'collection': a.collection,
              'count_before': before, 'generation_called': False,
              'retrieval': 'global dense24 vs source-filtered dense24; mMARCO CPU; exact-alias collapse; top8',
              'cases': []}
    try:
        for case in CASES:
            start = time.monotonic()
            source = case['source']
            if not coll.get(where={'source': source}, limit=1, include=['metadatas'])['ids']:
                raise RuntimeError(f'Source not present: {source}')
            embedding = embed.get_query_embedding(case['question'])
            options = {'query_embeddings': [embedding], 'n_results': a.top_k,
                       'include': ['documents', 'metadatas', 'distances']}
            global_rows = convert(coll.query(**options))
            filtered_rows = convert(coll.query(**options, where={'source': source}))
            if any(r['source'] != source for r in filtered_rows):
                raise RuntimeError(f'Filter mismatch for {source}')
            global_top = select(case['question'], global_rows, reranker, a.limit)
            filtered_top = select(case['question'], filtered_rows, reranker, a.limit)
            item = {'id': case['id'], 'question': case['question'], 'source': source,
                    'global_source_hits_dense': sum(r['source'] == source for r in global_rows),
                    'global_source_hits_top': sum(r['source'] == source for r in global_top),
                    'filtered_source_hits_top': sum(r['source'] == source for r in filtered_top),
                    'global_top': global_top, 'filtered_top': filtered_top,
                    'elapsed_seconds': round(time.monotonic()-start, 2)}
            report['cases'].append(item)
            print(f"DONE {case['id']} global_top={item['global_source_hits_top']} filtered_top={item['filtered_source_hits_top']}", flush=True)
    except (Exception, KeyboardInterrupt) as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    report['count_after'] = coll.count()
    report['index_unchanged'] = report['count_before'] == report['count_after']
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'REPORT {a.output}', flush=True)
    if report.get('error') or not report['index_unchanged']:
        raise SystemExit(report.get('error', 'Collection count changed'))

if __name__ == '__main__':
    main()
