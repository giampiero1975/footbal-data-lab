#!/usr/bin/env python3
"""Offline Glerean benchmark audit. Does not invoke Ollama or change V4."""
import argparse
import json
import re
from pathlib import Path

CITATION = re.compile(r'\[([^\[\]\n]{1,100})\]')
STABLE = re.compile(r'GLEREAN-C\d{3}')
NUMBER = re.compile(r'\d+')
ROLE = re.compile(r'centrocampist\w*\s+estern\w*\s*\(?(?:n\.?\s*)?(?:7\s+e\s+(?:n\.?\s*)?11|11\s+e\s+(?:n\.?\s*)?7|7\s*,\s*(?:n\.?\s*)?11|11\s*,\s*(?:n\.?\s*)?7)\b', re.I)

def audit(run):
    answer = run['answer_raw']
    issues = []
    if ROLE.search(answer):
        issues.append('wrong_wide_forward_role')
    citations = []
    for raw in CITATION.findall(answer):
        if run['mode'] == 'stable':
            citations.extend(STABLE.findall(raw))
        else:
            parts = [x.strip() for x in raw.split(',')]
            if parts and all(NUMBER.fullmatch(x) for x in parts):
                citations.extend(parts)
            elif len(parts) == 2 and NUMBER.fullmatch(parts[0]) and re.fullmatch(r'pagina\s+\d+', parts[1], re.I):
                citations.append(parts[0])
    if not citations:
        issues.append('missing_machine_readable_citations')
    if run.get('invalid_refs'):
        issues.append('benchmark_invalid_refs:' + ','.join(run['invalid_refs']))
    if not run.get('comparable_context'):
        issues.append('context_not_comparable')
    return dict(model=run['model'], case_id=run['case_id'], mode=run['mode'],
                citations=sorted(set(citations)), issues=sorted(set(issues)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    runs = json.loads(args.report.read_text(encoding='utf-8'))['runs']
    results = [audit(r) for r in runs]
    payload = dict(method='glerean_offline_lint_v2', total=len(results),
                   results=results, note='Selected rule-based checks, not full tactical validation.')
    if args.output:
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for result in results:
        print(result['model'], result['case_id'], result['mode'],
              ', '.join(result['issues']) or 'no issues detected')
    print('TOTAL', len(results), 'FLAGGED', sum(bool(r['issues']) for r in results))

if __name__ == '__main__':
    main()
