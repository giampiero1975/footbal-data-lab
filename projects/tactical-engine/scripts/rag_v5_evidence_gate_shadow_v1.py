#!/usr/bin/env python3
"""Offline read-only diagnostic: evidence gating on existing V5 audit JSON."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

RULES = {
    'ussia_4a': {'required': (r'4\s*[/\\]\s*A', r'5\s*secondi'), 'index_marker': r'\.{8,}'},
    'foscarini_b': {'required': (r'zona\s+B', r'lateral', r'pressing'), 'index_marker': r'\.{8,}'},
}

def rank_records(records, rules):
    ranked = []
    for record in records:
        content = record['text']
        matched = [bool(re.search(pattern, content, re.I)) for pattern in rules['required']]
        is_index = bool(re.search(rules['index_marker'], content))
        ranked.append({'id': record['id'], 'source': record['source'],
                       'pages': record['page_numbers'], 'all_terms': all(matched),
                       'matched_terms': sum(matched), 'index_like': is_index,
                       'diagnostic_score': sum(matched) - (2 if is_index else 0)})
    return sorted(ranked, key=lambda item: (-item['diagnostic_score'], item['index_like'], item['id']))

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audit', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists(): p.error(f'Refusing overwrite: {args.output}')
    source = json.loads(args.audit.read_text(encoding='utf-8'))
    if source.get('schema') != 'audit_v5_target_passages_v1' or not source.get('index_unchanged'):
        p.error('Unexpected or incomplete audit input')
    report = {'schema': 'rag_v5_evidence_gate_shadow_v1', 'source_audit': str(args.audit),
              'offline_only': True, 'generation_called': False, 'cases': {}}
    for case, rules in RULES.items():
        target = source['targets'][case]
        ranked = rank_records(target['matching_records'], rules)
        report['cases'][case] = {'source': target['source'], 'matching_records': len(ranked),
                                 'all_terms_count': sum(row['all_terms'] for row in ranked),
                                 'ranked': ranked}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'REPORT {args.output}')
    for case, result in report['cases'].items():
        print(f'{case}: {result["all_terms_count"]} complete matches; top={result["ranked"][0]["id"]}')

if __name__ == '__main__':
    main()
