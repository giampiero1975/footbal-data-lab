#!/usr/bin/env python3
"""Read-only source-aware V5 retrieval shadow; never calls generation."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import time

DB = Path('/opt/football-data-lab/knowledge/rag/chroma')
COLLECTION = 'dribbling_tactics_v5_multisource'
CASES = [
    ('ussia_4a', 'Nell’esercitazione 4/A di Ussia quale limite temporale è previsto?', 'Transizioni.Ussia'),
    ('foscarini_b', 'Perché per Foscarini è rischioso costruire attraverso i laterali nella zona B?', 'manovre_offensive_vari_sistemi_gioco_Foscarini'),
    ('foscarini_centro', 'Secondo Foscarini che ruolo ha il centrocampista centrale nella zona B?', 'manovre_offensive_vari_sistemi_gioco_Foscarini'),
]

def ids_and_sources(result):
    return [{'id': rid, 'source': meta.get('source'), 'page_numbers': meta.get('page_numbers'),
             'distance': round(float(distance), 6), 'text_preview': (doc or '')[:350]}
            for rid, meta, doc, distance in zip(result['ids'][0], result['metadatas'][0],
                                                result['documents'][0], result['distances'][0])]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db', type=Path, default=DB)
    ap.add_argument('--collection', default=COLLECTION)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--top-k', type=int, default=24)
    args = ap.parse_args()
    if args.top_k < 1: ap.error('--top-k must be positive')
    if not args.db.is_dir(): ap.error(f'Chroma DB not found: {args.db}')
    if args.output.exists(): ap.error(f'Output already exists: {args.output}')
    import chromadb
    from llama_index.embeddings.ollama import OllamaEmbedding
    coll = chromadb.PersistentClient(path=str(args.db)).get_collection(args.collection)
    before = coll.count()
    if before != 5319: raise RuntimeError(f'Unexpected collection count: {before}')
    embed = OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434')
    out = {'schema': 'rag_v5_source_shadow_v1', 'collection': args.collection,
           'count_before': before, 'cases': [], 'generation_called': False}
    try:
        for cid, question, source in CASES:
            started = time.monotonic()
            if not coll.get(where={'source': source}, limit=1, include=['metadatas'])['ids']:
                raise RuntimeError(f'Missing source in collection: {source}')
            embedding = embed.get_query_embedding(question)
            opts = {'query_embeddings': [embedding], 'n_results': args.top_k,
                    'include': ['documents', 'metadatas', 'distances']}
            global_result = coll.query(**opts)
            filtered_result = coll.query(**opts, where={'source': source})
            global_rows = ids_and_sources(global_result)
            filtered_rows = ids_and_sources(filtered_result)
            out['cases'].append({'id': cid, 'question': question, 'requested_source': source,
                                 'global_source_hits': sum(r['source'] == source for r in global_rows),
                                 'global': global_rows, 'filtered': filtered_rows,
                                 'filtered_all_match': all(r['source'] == source for r in filtered_rows),
                                 'elapsed_seconds': round(time.monotonic() - started, 2)})
            print(f'DONE {cid}: global_source_hits={out["cases"][-1]["global_source_hits"]} '
                  f'filtered={len(filtered_rows)}', flush=True)
    except Exception as exc:
        out['error'] = f'{type(exc).__name__}: {exc}'
    out['count_after'] = coll.count()
    out['index_unchanged'] = out['count_before'] == out['count_after']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'REPORT {args.output}', flush=True)
    if 'error' in out: raise SystemExit(out['error'])
    if not out['index_unchanged']: raise SystemExit('Collection count changed')

if __name__ == '__main__':
    main()
