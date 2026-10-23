#!/usr/bin/env python3
"""Read-only reference retrieval validation on distinct figure/exercise formats.

This is a retrieval diagnostic, not an independent gold benchmark.
"""
from __future__ import annotations
import argparse
import json
import re
import time
from pathlib import Path

DB=Path('/opt/football-data-lab/knowledge/rag/chroma')
COLLECTION='dribbling_tactics_v5_multisource'
# Deliberately different from the three prior shadow queries.
CASES=[
    ('ussia_4b','Che cosa succede nella figura 4/B di Ussia?','Transizioni.Ussia'),
    ('ussia_6b','Quale esercizio è illustrato come esercitazione 6/B da Ussia?','Transizioni.Ussia'),
    ('foscarini_fig9','Che movimenti mostra la fig. 9 di Foscarini?','manovre_offensive_vari_sistemi_gioco_Foscarini'),
    ('foscarini_fig20','Quali movimenti sono illustrati nella figura 20 di Foscarini?','manovre_offensive_vari_sistemi_gioco_Foscarini'),
]
REF_RE=re.compile(r'\b(?:esercitazione|esercizio|figure?|fig)\.?\s*(?:n(?:umero|\.)?\s*)?(\d{1,3})(?:\s*[/\\-]?\s*([a-z]))?\b',re.I)
def parse_reference(question):
    m=REF_RE.search(question)
    return (m.group(1),m.group(2).upper() if m.group(2) else None) if m else None

def match_reference(text,ref):
    number,letter=ref
    if letter:
        pat=rf'\b(?:esercitazione|esercizio|figure?|fig)\.?\s*(?:n(?:umero|\.)?\s*)?{re.escape(number)}\s*[/\\-]?\s*{re.escape(letter)}\b'
    else:
        # A bare number must not match a numbered suffix such as 20/A.
        pat=rf'\b(?:esercitazione|esercizio|figure?|fig)\.?\s*(?:n(?:umero|\.)?\s*)?{re.escape(number)}(?!\d)\b'
    return len(re.findall(pat,text,re.I))

def toc_like(text):
    return len(re.findall(r'\.{8,}',text))>=2

def find_candidates(collection,source,ref):
    data=collection.get(where={'source':source},include=['documents','metadatas'])
    out=[]
    for rid,doc,meta in zip(data['ids'],data['documents'],data['metadatas']):
        n=match_reference(doc or '',ref)
        if n:
            out.append({'id':rid,'pages':meta.get('page_numbers'),
                        'matches':n,'toc_like':toc_like(doc or ''),
                        'preview':(doc or '')[:360]})
    out.sort(key=lambda x:(x['toc_like'],-x['matches'],x['id']))
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--db',type=Path,default=DB)
    p.add_argument('--collection',default=COLLECTION)
    args=p.parse_args()
    if args.output.exists(): p.error('Refusing overwrite')
    # Pure parser checks before importing or opening Chroma.
    expected={
      'esercitazione 4/A':('4','A'),'Fig. 15/a':('15','A'),
      'figura 9':('9',None),'esercitazione 4B':('4','B'),
      'fig. 20':('20',None)}
    for q,gold in expected.items():
        assert parse_reference(q)==gold,(q,parse_reference(q),gold)
    assert match_reference('Figura 4/B',('4','B'))==1
    assert match_reference('Fig. 15/a',('15','A'))==1
    assert match_reference('fig. 9',('9',None))==1
    assert match_reference('fig. 19',('9',None))==0
    assert not toc_like('Figura 4/B: azione e recupero')
    assert toc_like('Figura 4/B ............... 15\nFigura 5 ............... 16')
    import chromadb
    coll=chromadb.PersistentClient(path=str(args.db)).get_collection(args.collection)
    before=coll.count()
    if before!=5319: raise RuntimeError(f'Unexpected collection count: {before}')
    report={'schema':'rag_v5_reference_generalization_shadow_v1','count_before':before,
            'generation_called':False,'index_writes':False,'parser_checks_passed':True,'cases':[]}
    try:
        for cid,question,source in CASES:
            t=time.monotonic()
            ref=parse_reference(question)
            hits=find_candidates(coll,source,ref)
            report['cases'].append({'id':cid,'question':question,'source':source,
                'reference':ref,'total_matches':len(hits),
                'non_toc_matches':sum(not x['toc_like'] for x in hits),
                'candidates':hits[:12],'elapsed_seconds':round(time.monotonic()-t,3)})
            print(f'DONE {cid} matches={len(hits)} non_toc={report["cases"][-1]["non_toc_matches"]}',flush=True)
    except (Exception,KeyboardInterrupt) as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    report['count_after']=coll.count()
    report['index_unchanged']=before==report['count_after']
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f'REPORT {args.output}',flush=True)
    if report.get('error') or not report['index_unchanged']:
        raise SystemExit(report.get('error','Collection count changed'))

if __name__=='__main__': main()
