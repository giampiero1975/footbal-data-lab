#!/usr/bin/env python3
"""Inspect existing fresh_03 manual chunks; read only, no reranker or LLM."""
import argparse
import json
from pathlib import Path
import chromadb

SOURCE = 'FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale'
DB = '/opt/football-data-lab/knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v5_multisource'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    collection = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    before = collection.count()
    if before != 5319:
        raise RuntimeError('Frozen corpus count mismatch')
    data = collection.get(where={'source': SOURCE}, include=['documents', 'metadatas'])
    passages = []
    for cid, document, metadata in zip(data['ids'], data['documents'], data['metadatas']):
        passages.append({'id': cid, 'pages': metadata.get('page_numbers'), 'text': metadata.get('raw_text') or document})
    after = collection.count()
    if before != after:
        raise RuntimeError('Corpus count changed')
    if args.output.exists():
        raise FileExistsError(str(args.output))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {'source': SOURCE, 'count_before': before, 'count_after': after, 'index_unchanged': True, 'passages': passages}
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print('REPORT', args.output, 'PASSAGES', len(passages), 'INDEX_UNCHANGED', True)

if __name__ == '__main__':
    main()
