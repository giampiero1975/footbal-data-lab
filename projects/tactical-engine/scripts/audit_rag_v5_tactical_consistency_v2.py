#!/usr/bin/env python3
"""Offline regression audit of known Q3/Q5 errors; not a general entailment judge."""
import argparse
import json
import re
from pathlib import Path


def audit(qid, answer, evidence):
    text = re.sub(r'\s+', ' ', answer.casefold())
    findings = []
    cited = sorted({int(x) for x in re.findall(r'\[F(\d+)\]', answer)})
    invalid = [x for x in cited if x < 1 or x > len(evidence)]
    if invalid or not cited:
        findings.append({'code': 'CITATIONS', 'severity': 'da_verificare', 'detail': 'Missing or invalid citation IDs'})
    if qid == 'q3':
        for m in re.finditer(r'(?:verticalizzazion\w*|profondit[aà])\s+(?:è|e|sono)\s+(?:indicata|favorita|efficace|preferibile)[^.\n]{0,220}?(?:rintanat\w*|difes\w* bass\w*|pressi dell.area di rigore)', text):
            findings.append({'code': 'Q3_LOW_BLOCK_VERTICAL', 'severity': 'contraddittoria', 'excerpt': m.group(0)[:260]})
        if not any(f['code'] == 'Q3_LOW_BLOCK_VERTICAL' for f in findings):
            for s in re.split(r'(?<=[.!?])\s+|\n+', text):
                if re.search(r'verticalizz|profondit', s) and re.search(r'rintanat|difes\w* bass\w*|pressi dell.area di rigore', s) and re.search(r'\b(?:indicata|favorita|efficace)\b', s) and not re.search(r'\b(?:non|difficile|sconsigliat)\b', s):
                    findings.append({'code': 'Q3_LOW_BLOCK_VERTICAL', 'severity': 'contraddittoria', 'excerpt': s[:260]})
                    break
    if qid == 'q5':
        lead = text.split('**condizioni e distinzioni:**')[0].split('**conclusione:**')[0]
        explicit_limit = bool(re.search(r'(?:fonti|estratti)[^.!?]{0,90}non documentano|non (?:esistono evidenze|è possibile dedurre|e possibile dedurre)[^.!?]{0,100}(?:variazion|cambi)', lead))
        leading_claim = bool(re.search(r'^\s*variare il sistema comporta|^\s*variare il sistema di gioco comporta', lead))
        if leading_claim and not explicit_limit:
            findings.append({'code': 'Q5_UNSUPPORTED_CHANGE_EFFECT', 'severity': 'contraddittoria', 'detail': 'Leading claim attributes static properties to a change'})
        elif not explicit_limit:
            findings.append({'code': 'Q5_CHANGE_VS_STATIC', 'severity': 'da_verificare', 'detail': 'No explicit source limitation for change effects'})
    status = 'contraddittoria' if any(f['severity'] == 'contraddittoria' for f in findings) else 'da_verificare'
    return {'status': status, 'findings': findings, 'citation_ids': cited, 'note': 'Heuristic screening only; no automatic factual certification.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    src = json.loads(args.input.read_text(encoding='utf-8'))
    questions = src['questions']
    if {q['id'] for q in questions} != {'q3', 'q5'}:
        raise ValueError('Expected q3 and q5')
    report = {'scope': 'Known Q3/Q5 failure modes; NOT a general faithfulness judge', 'questions': []}
    for q in questions:
        report['questions'].append({'id': q['id'], 'variants': {k: audit(q['id'], v['answer'], q['evidence']) for k, v in q['variants'].items()}})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for q in report['questions']:
        for name, result in q['variants'].items():
            print(q['id'], name, result['status'], [f['code'] for f in result['findings']])


if __name__ == '__main__':
    main()
