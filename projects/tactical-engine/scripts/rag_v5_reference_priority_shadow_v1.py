#!/usr/bin/env python3
"""Read-only replay of existing V5 mMARCO scores with exact-reference priority.

Optional --generate-figure20 calls Ollama once; no Chroma, embeddings or reranking.
"""
import argparse,json,re
from pathlib import Path
from urllib.request import Request,urlopen

SYSTEM=("Sei DRIBBLING. Rispondi solo alla figura o esercitazione richiesta usando le fonti. "
"Cita ogni affermazione con [F1], [F2], ecc. Distingui i movimenti descritti dai ruoli "
"dei giocatori: non attribuire ruoli, intenzioni o fasi di gioco non esplicitamente "
"attestati. Non confondere numeri di maglia con numeri di figura. "
"Se un dettaglio manca, dichiaralo. Rispondi in italiano.")

def toc(s):
    return len(re.findall(r'\.{8,}',s))>=2

def prioritize(case,cap=2):
    rows=case['augmented_top8']
    ids={r['id'] for r in rows if r['label'] in case['exact_ranks_augmented']}
    matching=sorted((r for r in rows if r['id'] in ids and not toc(r['text'])),
                    key=lambda r:(-r['score'],r['id']))
    chosen=matching[:cap]
    chosen_ids={r['id'] for r in chosen}
    remaining=[r for r in rows if r['id'] not in chosen_ids]
    return [dict(r,label=f'F{i}') for i,r in enumerate(chosen+remaining,1)]

def chat(q,evidence,timeout):
    context='\n\n'.join(f"[{r['label']}] Fonte: {r['source']} | Pagine: {r['pages']}\n{r['text']}" for r in evidence)
    payload={'model':'qwen3.5:9b','stream':False,'think':False,
        'messages':[{'role':'system','content':SYSTEM},
                    {'role':'user','content':f'DOMANDA:\n{q}\n\nEVIDENZE:\n{context}'}],
        'options':{'temperature':0,'num_ctx':8192}}
    req=Request('http://127.0.0.1:11434/api/chat',
        data=json.dumps(payload,ensure_ascii=False).encode(),
        headers={'Content-Type':'application/json'},method='POST')
    with urlopen(req,timeout=timeout) as resp: obj=json.load(resp)
    answer=(obj.get('message') or {}).get('content','')
    if not answer.strip():raise RuntimeError('Empty model response')
    cited=sorted(set(re.findall(r'\[F(\d+)\]',answer)),key=int)
    return {'answer':answer,'citation_ids':cited,
        'invalid_citation_ids':[x for x in cited if int(x)>len(evidence) or int(x)<1],
        'duration_ns':obj.get('total_duration')}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--generate-figure20',action='store_true')
    p.add_argument('--timeout',type=int,default=900)
    a=p.parse_args()
    if a.output.exists():p.error('Refusing overwrite')
    src=json.loads(a.input.read_text(encoding='utf-8'))
    assert src['schema']=='rag_v5_fresh_reference_e2e_shadow_v1'
    assert src['index_unchanged'] and not src['index_writes']
    report={'schema':'rag_v5_reference_priority_shadow_v1',
        'source_report':str(a.input),'reused_existing_rerank_scores':True,
        'chroma_access':False,'reranker_calls':0,'embedding_calls':0,
        'index_writes':False,'cases':[]}
    for c in src['cases']:
        old=c['augmented_top8']
        new=prioritize(c)
        assert len(old)==len(new)==8
        assert {r['id'] for r in old}=={r['id'] for r in new}
        ids={r['id'] for r in old if r['label'] in c['exact_ranks_augmented']}
        entry={'id':c['id'],'original_exact_ranks':c['exact_ranks_augmented'],
            'priority_exact_ranks':[r['label'] for r in new if r['id'] in ids],
            'top8_same_ids':True,'priority_top8':new}
        report['cases'].append(entry)
        print(f"REPLAY {c['id']}: {entry['original_exact_ranks']} -> {entry['priority_exact_ranks']}",flush=True)
    if a.generate_figure20:
        c=next(x for x in src['cases'] if x['id']=='foscarini_fig20')
        entry=next(x for x in report['cases'] if x['id']=='foscarini_fig20')
        try:entry['generation']=chat(c['question'],entry['priority_top8'],a.timeout)
        except Exception as exc:entry['generation_error']=f'{type(exc).__name__}: {exc}'
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('REPORT',a.output,flush=True)
    if any('generation_error' in x for x in report['cases']):raise SystemExit(1)

if __name__=='__main__':main()
