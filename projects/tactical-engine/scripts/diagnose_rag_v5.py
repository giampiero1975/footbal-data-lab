#!/usr/bin/env python3
"""Read-only V5 corpus duplicate and retrieval/reranking diagnostics.

No writes to Chroma. JSON report only when --output is explicitly supplied.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re
import time

import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding

DB="/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION="dribbling_tactics_v5_multisource"
QUESTIONS=[
 ("q1","Come affrontare con il 4-4-2 una squadra schierata con il 3-4-1-2?","Affrontare con il 4-4-2 un avversario schierato con il 3-4-1-2"),
 ("q2","Come creare superiorità numerica in fase di possesso palla?","superiorita_in_possesso_palla_Tesser"),
 ("q3","Quali principi favoriscono la verticalizzazione nella fase offensiva?","verticalizzazione_Bonacini"),
 ("q4","Come sfruttare i triangoli per sviluppare il gioco di squadra?","triangoli_20_squadra_20_Trombetta"),
 ("q5","Quali vantaggi e rischi comporta variare il sistema di gioco durante una partita?","variazione_sistema_gioco_Pane"),
]
def normalize(s):
    return re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",s.casefold())).strip()

def duplicates(ids,docs,metas):
    exact=defaultdict(set)
    sources=defaultdict(list)
    for cid,doc,meta in zip(ids,docs,metas):
        source=meta["source"]
        text=normalize(meta.get("raw_text") or doc)
        if len(text)>=100:
            exact[hashlib.sha256(text.encode()).hexdigest()].add(source)
            sources[source].append(text)
    exact_groups=[sorted(group) for group in exact.values() if len(group)>1]
    counts=Counter(tuple(g) for g in exact_groups)
    by_source={}
    for source,texts in sources.items():
        unique=set(texts)
        by_source[source]=unique
    candidate_pairs=Counter()
    for group,n in counts.items():
        for i,a in enumerate(group):
            for b in group[i+1:]:
                candidate_pairs[(a,b)]+=n
    report=[]
    for (a,b),shared in candidate_pairs.most_common(30):
        union=len(by_source[a]|by_source[b])
        overlap=shared/union if union else 0
        report.append({"sources":[a,b],"shared_exact_chunks":shared,
                       "unique_chunks":[len(by_source[a]),len(by_source[b])],
                       "shared_over_union":round(overlap,4)})
    return {"cross_source_exact_text_groups":len(exact_groups),
            "candidate_pairs":report,
            "note":"Chunk-level exact matches are evidence of overlap, not proof of duplicate PDFs."}

def diversified(rows,limit=8,max_per_source=2):
    selected=[]; used=Counter()
    for row in rows:
        source=row["source"]
        if used[source]<max_per_source:
            selected.append(row);used[source]+=1
            if len(selected)>=limit:break
    return selected

def summarize(rows,gold):
    sources=[r["source"] for r in rows]
    return {"sources":dict(Counter(sources)),"unique_sources":len(set(sources)),
            "target_source_rank":next((i+1 for i,s in enumerate(sources) if s==gold),None),
            "top":[{"source":r["source"],"pages":r["pages"],"distance":r["distance"],
                    "id":r["id"][:12]} for r in rows]}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--rerank",action="store_true",help="Load mMARCO CrossEncoder on CPU")
    args=ap.parse_args()
    coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    count=coll.count()
    if count!=5319:raise RuntimeError(f"Unexpected collection size: {count}")
    print(f"V5 records={count} (read-only)",flush=True)
    result=coll.get(include=["documents","metadatas"])
    ids=result["ids"]; docs=result["documents"]; metas=result["metadatas"]
    assert len(ids)==len(docs)==len(metas)==count
    invalid_pages=[]
    for cid,meta in zip(ids,metas):
        try:
            pages=json.loads(meta["page_numbers"])
            if not isinstance(pages,list) or any(not isinstance(p,int) or p<1 for p in pages):
                raise ValueError("invalid page numbers")
        except (ValueError,KeyError,TypeError):
            invalid_pages.append(cid[:12])
    report={"collection":COLLECTION,"count":count,"documents":len(set(m["source_relative"] for m in metas)),
            "missing_or_invalid_page_metadata":len(invalid_pages),
            "invalid_page_examples":invalid_pages[:10],
            "duplicates":duplicates(ids,docs,metas),"queries":[]}
    print("Cross-source exact-text overlap candidates:",flush=True)
    for pair in report["duplicates"]["candidate_pairs"][:12]:
        print(" ",pair,flush=True)
    print("Missing/invalid page metadata:",len(invalid_pages),flush=True)
    embedder=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    reranker=None
    if args.rerank:
        from sentence_transformers import CrossEncoder
        reranker=CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",device="cpu",max_length=512)
    for key,question,gold in QUESTIONS:
        start=time.perf_counter()
        vector=embedder.get_query_embedding(question)
        retrieved=coll.query(query_embeddings=[vector],n_results=24,
                             include=["documents","metadatas","distances"])
        rows=[{"id":cid,"source":meta["source"],"pages":meta["page_numbers"],
               "distance":round(float(dist),5),"document":doc}
              for cid,meta,dist,doc in zip(retrieved["ids"][0],retrieved["metadatas"][0],
                                            retrieved["distances"][0],retrieved["documents"][0])]
        baseline=rows[:8]
        diverse=diversified(rows)
        entry={"id":key,"question":question,"target_source":gold,
               "dense":summarize(baseline,gold),
               "diversified":summarize(diverse,gold),
               "embedding_retrieval_seconds":round(time.perf_counter()-start,2)}
        if reranker:
            scores=reranker.predict([(question,row["document"]) for row in rows],
                                    batch_size=1,show_progress_bar=False)
            reranked=[rows[i] for i in sorted(range(len(rows)),key=lambda i:float(scores[i]),reverse=True)]
            entry["reranked"]=summarize(reranked[:8],gold)
            entry["reranked_diversified"]=summarize(diversified(reranked),gold)
        report["queries"].append(entry)
        print(f"\n{key} target={gold}",flush=True)
        for label in ("dense","diversified","reranked","reranked_diversified"):
            if label in entry:
                e=entry[label]
                print(f" {label}: target_rank={e['target_source_rank']} unique_sources={e['unique_sources']} sources={e['sources']}",flush=True)
    if args.output:
        path=args.output.expanduser().resolve()
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        print("REPORT:",path,flush=True)
    print("V5 DIAGNOSTIC COMPLETE: Chroma unchanged; no quality score assigned.",flush=True)

if __name__=="__main__":
    main()
