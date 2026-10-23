#!/usr/bin/env python3
"""Read-only exact-reference augmentation of V5 source-filtered dense candidates."""
from __future__ import annotations
import argparse, hashlib, json, re, time
from pathlib import Path

DB=Path('/opt/football-data-lab/knowledge/rag/chroma')
COLLECTION='dribbling_tactics_v5_multisource'
CASES=[
 ('ussia_4a','Nell’esercitazione 4/A di Ussia quale limite temporale è previsto?','Transizioni.Ussia'),
 ('foscarini_b','Perché per Foscarini è rischioso costruire attraverso i laterali nella zona B?','manovre_offensive_vari_sistemi_gioco_Foscarini'),
 ('foscarini_centro','Secondo Foscarini che ruolo ha il centrocampista centrale nella zona B?','manovre_offensive_vari_sistemi_gioco_Foscarini')]

def reference(question):
    m=re.search(r'\b(?:esercitazione|esercizio|figura|fig\.)\s*(?:n(?:umero|\.)?\s*)?(\d{1,3})\s*[/\\-]\s*([a-z])\b',question,re.I)
    return (m.group(1),m.group(2).upper()) if m else None

def candidates(coll,source,ref):
    if not ref: return []
    batch=coll.get(where={'source':source},include=['documents','metadatas'])
    pattern=rf'\b(?:esercitazione|esercizio|figura|fig\.)\s*(?:n(?:umero|\.)?\s*)?{re.escape(ref[0])}\s*[/\\-]\s*{re.escape(ref[1])}\b'
    rows=[]
    for rid,doc,meta in zip(batch['ids'],batch['documents'],batch['metadatas']):
        doc=doc or ''
        matches=len(re.findall(pattern,doc,re.I))
        if not matches: continue
        toc=len(re.findall(r'\.{8,}',doc))>=2
        rows.append({'id':rid,'text':doc,'source':meta.get('source'),'pages':meta.get('page_numbers'),
                     'origin':'exact','toc_like':toc,'matches':matches})
    rows.sort(key=lambda r:(r['toc_like'],-r['matches'],r['id']))
    return rows[:12]

def select(question,rows,reranker):
    scores=reranker.predict([(question,r['text']) for r in rows],batch_size=1,show_progress_bar=False)
    order=sorted(range(len(rows)),key=lambda i:(-float(scores[i]),rows[i]['id']))
    result=[]; seen=set()
    for i in order:
        r=rows[i]; key=(r['source'],hashlib.sha256(re.sub(r'\s+',' ',r['text'].casefold()).encode()).hexdigest())
        if key in seen: continue
        seen.add(key)
        result.append({'rank':len(result)+1,'id':r['id'],'source':r['source'],'pages':r['pages'],
                       'origin':r['origin'],'score':round(float(scores[i]),6),'text':r['text']})
        if len(result)==8: break
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,default=DB)
    p.add_argument('--collection',default=COLLECTION)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists(): p.error(f'Refusing overwrite: {a.output}')
    if not a.db.is_dir(): p.error(f'Missing Chroma directory: {a.db}')
    import chromadb
    from llama_index.embeddings.ollama import OllamaEmbedding
    from sentence_transformers import CrossEncoder
    coll=chromadb.PersistentClient(path=str(a.db)).get_collection(a.collection)
    before=coll.count()
    if before!=5319: raise RuntimeError(f'Unexpected collection count: {before}')
    embed=OllamaEmbedding(model_name='qwen3-embedding:0.6b',base_url='http://127.0.0.1:11434')
    reranker=CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1',device='cpu',max_length=512)
    report={'schema':'rag_v5_exact_reference_shadow_v1','count_before':before,'generation_called':False,
            'index_writes':False,'cases':[]}
    try:
        for cid,question,source in CASES:
            start=time.monotonic(); ref=reference(question)
            emb=embed.get_query_embedding(question)
            raw=coll.query(query_embeddings=[emb],n_results=24,where={'source':source},
                           include=['documents','metadatas','distances'])
            dense=[{'id':rid,'text':doc or '','source':meta.get('source'),
                    'pages':meta.get('page_numbers'),'origin':'dense'}
                   for rid,doc,meta in zip(raw['ids'][0],raw['documents'][0],raw['metadatas'][0])]
            exact=candidates(coll,source,ref)
            combined=list(dense); seen={r['id'] for r in dense}
            for r in exact:
                if r['id'] not in seen: combined.append(r);seen.add(r['id'])
            baseline=select(question,dense,reranker)
            augmented=select(question,combined,reranker)
            valid={r['id'] for r in exact if not r['toc_like']}
            report['cases'].append({'id':cid,'source':source,'reference':ref,
                'dense_candidates':len(dense),'exact_candidates':len(exact),'new_candidates':len(combined)-len(dense),
                'exact_details':[{k:r[k] for k in ('id','pages','toc_like','matches')} for r in exact],
                'baseline_top8':baseline,'augmented_top8':augmented,
                'exact_ranks_baseline':[r['rank'] for r in baseline if r['id'] in valid],
                'exact_ranks_augmented':[r['rank'] for r in augmented if r['id'] in valid],
                'elapsed_seconds':round(time.monotonic()-start,2)})
            print(f'DONE {cid}: new={len(combined)-len(dense)} exact_ranks={report["cases"][-1]["exact_ranks_augmented"]}',flush=True)
    except (Exception,KeyboardInterrupt) as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    report['count_after']=coll.count()
    report['index_unchanged']=report['count_before']==report['count_after']
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'REPORT {a.output}',flush=True)
    if report.get('error') or not report['index_unchanged']:
        raise SystemExit(report.get('error','Collection count changed'))

if __name__=='__main__': main()
