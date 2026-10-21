#!/usr/bin/env python3
"""Read-only audit of DRIBBLING V5 prompt A/B JSON. Standard library only."""
import argparse
import hashlib
import json
import re
from pathlib import Path

def normalize(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', text.casefold())).strip()

def audit(data):
    result = {'collection': data.get('collection'), 'count_before': data.get('count_before'),
              'count_after': data.get('count_after'), 'index_unchanged': data.get('index_unchanged'),
              'questions': [], 'totals': {'baseline_seconds': 0, 'strict_seconds': 0,
                                           'invalid_citations': 0, 'duplicate_evidence_pairs': 0}}
    for q in data['questions']:
        evidence = q['evidence']
        fingerprints = {}
        duplicates = []
        for i, row in enumerate(evidence, 1):
            key = hashlib.sha256(normalize(row['text']).encode()).hexdigest()
            if key in fingerprints:
                duplicates.append({'first': fingerprints[key], 'duplicate': i,
                                   'sources': [evidence[fingerprints[key]-1]['source'], row['source']]})
            else:
                fingerprints[key] = i
        item = {'id': q['id'], 'question': q['question'], 'evidence_count': len(evidence),
                'exact_normalized_duplicate_pairs': duplicates, 'variants': {}}
        for name, variant in q['variants'].items():
            cited = sorted(set(map(int, re.findall(r'\[F(\d+)\]', variant['answer']))))
            invalid = [n for n in cited if n < 1 or n > len(evidence)]
            item['variants'][name] = {'seconds': variant['elapsed_seconds'], 'cited_ids': cited,
                                      'invalid_citations': invalid,
                                      'uncited_evidence_ids': [n for n in range(1, len(evidence)+1) if n not in cited]}
            result['totals'][f'{name}_seconds'] += variant['elapsed_seconds']
            result['totals']['invalid_citations'] += len(invalid)
        result['totals']['duplicate_evidence_pairs'] += len(duplicates)
        result['questions'].append(item)
    totals = result['totals']
    totals['strict_to_baseline_time_ratio'] = round(totals['strict_seconds'] / totals['baseline_seconds'], 2)
    for k in ('baseline_seconds', 'strict_seconds'):
        totals[k] = round(totals[k], 2)
    result['limitations'] = ['Valid citations do not imply factual faithfulness.',
                             'Normalized exact matching does not detect paraphrased or overlapping near-duplicates.',
                             'Tactical correctness requires claim-level evidence review.']
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8'))
    result = audit(data)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + '\n', encoding='utf-8')
    print(rendered)

if __name__ == '__main__':
    main()
