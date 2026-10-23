#!/usr/bin/env python3
"""Opt-in evidence-selection shadow. No Chroma writes or model generation."""
import argparse, json, re
from pathlib import Path

def select(rows, scores, source, page=None, limit=8):
    """Preserve ranked evidence plus best matching source/page evidence."""
    if len(rows) != len(scores):
        raise ValueError('Rows and scores differ')
    ordering=sorted(range(len(rows)),key=lambda i:float(scores[i]),reverse=True)
    keep=[];seen=set()
    def append(i):
        key=rows[i]['id']
        if key not in seen:
            seen.add(key);keep.append(i)
    matches=[i for i in ordering if rows[i].get('source')==source]
    if matches:append(matches[0])
    if page is not None:
        pages=[i for i in matches if str(page) in re.findall(r'\d+',str(rows[i].get('pages')))]
        if pages:append(pages[0])
    for i in ordering:
        if len(keep)>=limit:break
        append(i)
    return [rows[i] for i in sorted(keep,key=lambda i:float(scores[i]),reverse=True)][:limit]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    data=json.loads(args.trace.read_text(encoding='utf-8'))
    result={'schema':'v5_source_coverage_shadow_v1','read_only':True,'questions':[]}
    targets={'fresh_03':('FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale',None),'fresh_10':('Transizioni.Ussia',17)}
    for q in data['questions']:
        if q['id'] not in targets:continue
        source,page=targets[q['id']]
        rows=q['candidates'];scores=[r['score'] for r in rows]
        selected=select(rows,scores,source,page)
        result['questions'].append({'id':q['id'],'source':source,'page':page,'coverage_present':any(r.get('source')==source for r in rows),'page_present':(None if page is None else any(r.get('source')==source and str(page) in re.findall(r'\d+',str(r.get('pages'))) for r in rows)),'selected':[{'id':r['id'],'source':r['source'],'pages':r['pages'],'rerank_rank':r['rerank_rank']} for r in selected]})
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('REPORT:',args.output)

if __name__=='__main__':main()
