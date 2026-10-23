#!/usr/bin/env python3
"""Read-only audit of source-specific passages, without embeddings or LLM."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

DB = Path('/opt/football-data-lab/knowledge/rag/chroma')
COLLECTION = 'dribbling_tactics_v5_multisource'
TARGETS = {
    'ussia_4a': {'source': 'Transizioni.Ussia', 'patterns': [r'4\s*[/\\]\s*A', r'5\s*secondi', r'cinque\s+secondi']},
    'foscarini_b': {'source': 'manovre_offensive_vari_sistemi_gioco_Foscarini', 'patterns': [r'zona\s+B', r'lateral', r'pressing']},
}

def audit(collection, targets):
    result = {}
    for name, cfg in targets.items():
        batch = collection.get(where={'source': cfg['source']}, include=['documents', 'metadatas'])
        rows = []
        for record_id, document, metadata in zip(batch['ids'], batch['documents'], batch['metadatas']):
            text = document or ''
            matches = []
            for pattern in cfg['patterns']:
                hits = list(re.finditer(pattern, text, re.IGNORECASE))
                if hits:
                    matches.append({'pattern': pattern, 'count': len(hits),
                                    'snippets': [text[max(0, m.start()-180):min(len(text), m.end()+240)] for m in hits[:3]]})
            if matches:
                rows.append({'id': record_id, 'source': metadata.get('source'),
                             'source_relative': metadata.get('source_relative'),
                             'page_numbers': metadata.get('page_numbers'),
                             'matches': matches, 'text': text})
        result[name] = {'source': cfg['source'], 'source_record_count': len(batch['ids']),
                        'matching_record_count': len(rows), 'matching_records': rows}
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, default=DB)
    parser.add_argument('--collection', default=COLLECTION)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not args.db.is_dir(): parser.error(f'Chroma directory missing: {args.db}')
    if args.output.exists(): parser.error(f'Refusing overwrite: {args.output}')
    import chromadb
    collection = chromadb.PersistentClient(path=str(args.db)).get_collection(args.collection)
    before = collection.count()
    if before != 5319: raise RuntimeError(f'Unexpected collection size: {before}')
    report = {'schema': 'audit_v5_target_passages_v1', 'collection': args.collection,
              'count_before': before, 'targets': audit(collection, TARGETS),
              'count_after': collection.count(), 'generation_called': False}
    report['index_unchanged'] = report['count_before'] == report['count_after']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    for key, value in report['targets'].items():
        print(f'{key}: {value["matching_record_count"]}/{value["source_record_count"]} matching chunks', flush=True)
    print(f'REPORT {args.output}', flush=True)
    if not report['index_unchanged']: raise SystemExit('Collection count changed')

if __name__ == '__main__':
    main()
