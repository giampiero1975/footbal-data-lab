#!/usr/bin/env python3
"""Reversible passage-level shadow replay; no Chroma access."""
import argparse, hashlib, json, re, time
from pathlib import Path
from urllib.request import Request, urlopen

def definition(text):
    sentences=re.split(r'(?<=[.!?])\s+',text)
    candidates=[s.strip() for s in sentences if 'transizione positiva' in s.lower() and 'transizione negativa' in s.lower()]
    if not candidates: raise ValueError('No phase definition')
    s=candidates[0]
    if any(x in s.lower() for x in ('ripiegando','ritardare','temporeggiare','togliere profondità')):
        raise ValueError('Unsafe definition')
    return s

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--ablation',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--dry-run',action='store_true')
    mode.add_argument('--execute',action='store_true')
    p.add_argument('--timeout',type=int,default=900)
    a=p.parse_args()
    if a.output.exists() or a.output.resolve()==a.ablation.resolve():p.error('Refusing overwrite')
    raw=a.ablation.read_bytes(); source=json.loads(raw)
    if source.get('schema')!='rag_v5_phase_ablation_v1' or source.get('status')!='complete':
        p.error('Expected completed phase ablation')
    report={'schema':'rag_v5_phase_passage_shadow_v1','status':'dry_run' if a.dry_run else 'running',
            'source_sha256':hashlib.sha256(raw).hexdigest(),'model':source['model'],
            'system_prompt':source['system_prompt'],'policy':'frozen evidence, unchanged labels, no Chroma','questions':[]}
    for q in source['questions']:
        if q['id'] not in ('holdout_06','holdout_10'):continue
        kept=[]; changes=[]
        for original in q['evidence']:
            e=dict(original); label=e['label']
            if q['id']=='holdout_06' and label in ('F5','F7'):
                changes.append({'label':label,'action':'drop'});continue
            if q['id']=='holdout_10' and label=='F3':
                before=len(e['text']);e['text']=definition(e['text'])
                changes.append({'label':label,'action':'keep_definition','before_chars':before,'after_chars':len(e['text'])})
            kept.append(e)
        entry={'id':q['id'],'question':q['question'],'changes':changes,'evidence':kept,
               'previous_answer':q['ablation_answer'],'previous_citation_ids':q['citation_ids']}
        if a.execute:
            context='\n\n'.join(f"[{e['label']}] Fonte: {e['source']} | Pagine: {e['pages']}\n{e['text']}" for e in kept)
            payload={'model':source['model'],'stream':False,'think':False,
                     'messages':[{'role':'system','content':source['system_prompt']},
                                 {'role':'user','content':f"DOMANDA:\n{q['question']}\n\nFONTI:\n{context}"}],
                     'options':{'temperature':0,'num_ctx':8192}}
            req=Request('http://127.0.0.1:11434/api/chat',
                        data=json.dumps(payload,ensure_ascii=False).encode(),
                        headers={'Content-Type':'application/json'},method='POST')
            start=time.monotonic()
            try:
                with urlopen(req,timeout=a.timeout) as response: result=json.load(response)
                answer=(result.get('message') or {}).get('content','')
                if not answer.strip():raise ValueError('Empty answer')
                ids=sorted(set(re.findall(r'\[F(\d+)\]',answer)),key=int)
                valid={e['label'][1:] for e in kept}
                entry.update({'answer':answer,'citation_ids':ids,
                              'invalid_citation_ids':[x for x in ids if x not in valid],
                              'elapsed_seconds':round(time.monotonic()-start,2)})
            except Exception as exc:
                entry['error']=f'{type(exc).__name__}: {exc}';report['status']='partial_error'
                report['questions'].append(entry);break
        report['questions'].append(entry)
    if a.execute and report['status']=='running':report['status']='complete'
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x',encoding='utf-8') as f:
        json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
    print('REPORT',a.output,'STATUS',report['status'])
    if report['status']=='partial_error':raise SystemExit(1)
if __name__=='__main__':main()
