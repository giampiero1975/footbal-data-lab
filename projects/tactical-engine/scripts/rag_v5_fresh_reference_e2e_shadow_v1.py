#!/usr/bin/env python3
"""Read-only V5 fresh-reference retrieval, rerank and optional grounded generation.

The four cases are diagnostic, not independent gold. Baseline and augmented
retrieval use the same embedding and reranker; generation uses the same prompt
and Ollama settings as smoke_test_rag_v5_e2e.py.
"""
from __future__ import annotations
import argparse, hashlib, json, re, time
from pathlib import Path
from urllib.request import Request,urlopen

DB=Path('/opt/football-data-lab/knowledge/rag/chroma')
COLLECTION='dribbling_tactics_v5_multisource'
MODEL='qwen3.5:9b'
CASES=[
 ('ussia_4b','Che cosa succede nella figura 4/B di Ussia?','Transizioni.Ussia'),
 ('ussia_6b','Quale esercizio è illustrato come esercitazione 6/B da Ussia?','Transizioni.Ussia'),
 ('foscarini_fig9','Che movimenti mostra la fig. 9 di Foscarini?','manovre_offensive_vari_sistemi_gioco_Foscarini'),
 ('foscarini_fig20','Quali movimenti sono illustrati nella figura 20 di Foscarini?','manovre_offensive_vari_sistemi_gioco_Foscarini')]
SYSTEM=("Sei DRIBBLING, assistente di analisi tattica calcistica. "
"Rispondi esclusivamente in base agli estratti numerati forniti. "
"Non inventare fatti, autori, pagine o citazioni. "
"Ogni affermazione tattica sostanziale deve avere una citazione nel formato [F1], [F2], ecc. "
"Se le fonti non consentono una risposta affidabile, esplicita il limite. "
"Rispondi in italiano in modo chiaro e sintetico.")
REF_RE=re.compile(r'\b(?:esercitazione|esercizio|figura|figure|fig)\.?\s*(?:n(?:umero|\.)?\s*)?(\d{1,3})(?:\s*[/\\-]?\s*([a-z]))?\b',re.I)
def reference(q):
    m=REF_RE.search(q)
    return (m.group(1),m.group(2).upper() if m.group(2) else None) if m else None
def hits(text,ref):
    n,letter=ref
    suffix=rf'\s*[/\\-]?\s*{re.escape(letter)}\b' if letter else r'(?!\d)'
    return len(re.findall(rf'\b(?:esercitazione|esercizio|figura|figure|fig)\.?\s*(?:n(?:umero|\.)?\s*)?{re.escape(n)}{suffix}',text,re.I))
def toc(text):
    return len(re.findall(r'\.{8,}',text))>=2
def norm(text):
    return re.sub(r'\s+',' ',re.sub(r'[^\w\s]',' ',text.casefold())).strip()
def exact(coll,source,ref):
    data=coll.get(where={'source':source},include=['documents','metadatas'])
    out=[]
    for rid,doc,meta in zip(data['ids'],data['documents'],data['metadatas']):
        count=hits(doc or '',ref)
        if count and not toc(doc or ''):
            out.append({'id':rid,'text':doc or '','source':meta['source'],
                        'pages':meta.get('page_numbers'),'origin':'exact','matches':count})
    return sorted(out,key=lambda r:(-r['matches'],r['id']))[:12]
def select(q,rows,reranker):
    if not rows:return []
    scores=reranker.predict([(q,r['text']) for r in rows],batch_size=1,show_progress_bar=False)
    order=sorted(range(len(rows)),key=lambda i:(-float(scores[i]),rows[i]['id']))
    out=[];seen=set()
    for i in order:
        r=rows[i]
        key=(r['source'],hashlib.sha256(norm(r['text']).encode()).hexdigest())
        if key in seen:continue
        seen.add(key)
        out.append({'label':f'F{len(out)+1}','id':r['id'],'source':r['source'],
                    'pages':r['pages'],'origin':r['origin'],'score':round(float(scores[i]),6),
                    'text':r['text']})
        if len(out)==8:break
    return out
def chat(q,evidence,timeout):
    context='\n\n'.join(f"[F{i}] Fonte: {r['source']} | Pagine: {r['pages']}\n{r['text']}"
                        for i,r in enumerate(evidence,1))
    payload={'model':MODEL,'stream':False,'think':False,
        'messages':[{'role':'system','content':SYSTEM},
                    {'role':'user','content':f'DOMANDA:\n{q}\n\nFONTI:\n{context}'}],
        'options':{'temperature':0,'num_ctx':8192}}
    req=Request('http://127.0.0.1:11434/api/chat',
        data=json.dumps(payload,ensure_ascii=False).encode(),
        headers={'Content-Type':'application/json'},method='POST')
    with urlopen(req,timeout=timeout) as response: obj=json.load(response)
    answer=(obj.get('message') or {}).get('content','')
    if not answer.strip():raise RuntimeError('Empty model response')
    cited=sorted(set(re.findall(r'\[F(\d+)\]',answer)),key=int)
    valid={str(i) for i in range(1,len(evidence)+1)}
    return {'answer':answer,'citation_ids':cited,'invalid_citation_ids':[x for x in cited if x not in valid],
            'has_any_citation':bool(cited),'total_duration_ns':obj.get('total_duration')}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--db',type=Path,default=DB)
    p.add_argument('--timeout',type=int,default=900)
    p.add_argument('--generate',action='store_true',help='Run one generated answer per fresh case')
    args=p.parse_args()
    if args.output.exists():p.error(f'Refusing overwrite: {args.output}')
    assert reference('figura 9')==('9',None)
    assert reference('Fig. 15/a')==('15','A')
    assert reference('esercitazione 4B')==('4','B')
    assert hits('Figura 4/B',('4','B'))==1
    assert hits('Fig. 9',('9',None))==1
    assert hits('Fig. 19',('9',None))==0
    import chromadb
    from llama_index.embeddings.ollama import OllamaEmbedding
    from sentence_transformers import CrossEncoder
    coll=chromadb.PersistentClient(path=str(args.db)).get_collection(COLLECTION)
    before=coll.count()
    if before!=5319:raise RuntimeError(f'Unexpected collection count: {before}')
    embed=OllamaEmbedding(model_name='qwen3-embedding:0.6b',base_url='http://127.0.0.1:11434')
    reranker=CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1',device='cpu',max_length=512)
    report={'schema':'rag_v5_fresh_reference_e2e_shadow_v1','count_before':before,
            'generation_requested':args.generate,'index_writes':False,'cases':[]}
    try:
        for cid,q,source in CASES:
            start=time.monotonic()
            emb=embed.get_query_embedding(q)
            result=coll.query(query_embeddings=[emb],n_results=24,where={'source':source},
                include=['documents','metadatas','distances'])
            dense=[{'id':rid,'text':doc or '','source':meta['source'],
                    'pages':meta.get('page_numbers'),'origin':'dense'}
                for rid,doc,meta in zip(result['ids'][0],result['documents'][0],result['metadatas'][0])]
            ref=reference(q); lexical=exact(coll,source,ref)
            merged=list(dense); seen={r['id'] for r in merged}
            for r in lexical:
                if r['id'] not in seen:merged.append(r);seen.add(r['id'])
            base=select(q,dense,reranker); augmented=select(q,merged,reranker)
            exact_ids={r['id'] for r in lexical}
            item={'id':cid,'question':q,'source':source,'reference':ref,
                'dense_count':len(dense),'exact_non_toc_count':len(lexical),
                'new_candidates':len(merged)-len(dense),
                'exact_ranks_baseline':[r['label'] for r in base if r['id'] in exact_ids],
                'exact_ranks_augmented':[r['label'] for r in augmented if r['id'] in exact_ids],
                'baseline_top8':base,'augmented_top8':augmented}
            if args.generate:item['generation']=chat(q,augmented,args.timeout)
            item['elapsed_seconds']=round(time.monotonic()-start,2)
            report['cases'].append(item)
            print(f'DONE {cid} added={item["new_candidates"]} ranks={item["exact_ranks_augmented"]} generated={args.generate}',flush=True)
    except (Exception,KeyboardInterrupt) as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    report['count_after']=coll.count()
    report['index_unchanged']=before==report['count_after']
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'REPORT {args.output}',flush=True)
    if report.get('error') or not report['index_unchanged']:
        raise SystemExit(report.get('error','Collection count changed'))

if __name__=='__main__':main()
