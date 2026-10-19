#!/usr/bin/env python3
"""Benchmark generazione Q8 read-only con tre contesti BGE controllati.

Mantiene LLM e prompt del test V4; forza gli stessi chunk tramite retriever
fisso, preservando CitationQueryEngine/compact/refine. Non altera Chroma.
"""
import argparse
import json
import re
import time
from pathlib import Path

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.schema import TextNode, NodeWithScore
from llama_index.core.retrievers import BaseRetriever
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from sentence_transformers import CrossEncoder

from test_dribbling_v4_top5_top10 import DB,COLLECTION,SOURCE,QUESTION,QA,REFINE

GOLD={16,17,21}
class FixedRetriever(BaseRetriever):
    def __init__(self,nodes):
        super().__init__()
        self._nodes=nodes
    def _retrieve(self,query_bundle):
        return self._nodes

def headings(m):
    value=m.get("headings","[]")
    return tuple(json.loads(value) if isinstance(value,str) else value)

def structural(m,doc):
    return len(m.get("raw_text",doc).strip())<80 or any(
        h.strip().casefold() in {"premessa","prefazione","indice","sommario"}
        for h in headings(m))

def expand(anchors,by_idx):
    result=[]
    for anchor in anchors:
        doc,meta,_=by_idx[anchor]
        if structural(meta,doc): continue
        for neighbor in (anchor-1,anchor+1):
            if neighbor in by_idx and neighbor not in anchors and neighbor not in result:
                ndoc,nmeta,_=by_idx[neighbor]
                if headings(nmeta)==headings(meta) and not structural(nmeta,ndoc):
                    result.append(neighbor)
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="/opt/football-data-lab/projects/tactical-engine/benchmark_generazione_contesti_q8.txt")
    args=ap.parse_args()
    coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    if coll.count()!=86: raise RuntimeError("V4 non corrisponde al baseline")
    rows=coll.get(where={"source":SOURCE},include=["documents","metadatas"])
    by_idx={m["chunk_index"]:(doc,m,cid) for doc,m,cid in zip(rows["documents"],rows["metadatas"],rows["ids"])}
    embedding=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    vec=embedding.get_query_embedding(QUESTION)
    hits=coll.query(query_embeddings=[vec],n_results=20,where={"source":SOURCE},include=["documents","metadatas"])
    candidates=list(zip(hits["documents"][0],hits["metadatas"][0]))
    bge=CrossEncoder("BAAI/bge-reranker-v2-m3",device="cpu",max_length=512)
    scores=bge.predict([(QUESTION,doc) for doc,_ in candidates],batch_size=1,show_progress_bar=False)
    ranking=[candidates[i][1]["chunk_index"] for i in sorted(range(len(candidates)),key=lambda i:(-float(scores[i]),i))]
    anchors=ranking[:5]
    neighbors=expand(anchors,by_idx)
    baseline=anchors
    expanded=(anchors+neighbors+ranking[5:])[:7]
    core=[i for i in anchors if not structural(by_idx[i][1],by_idx[i][0])]
    options=core+expand(core,by_idx)+ranking[5:]
    optimized=[]
    for idx in options:
        doc,meta,_=by_idx[idx]
        if idx not in optimized and not structural(meta,doc): optimized.append(idx)
        if len(optimized)==5: break
    variants=[("BGE5",baseline),("BGE7_espansione",expanded),("TOP5_tecnico",optimized)]
    llm=Ollama(model="qwen3.5:9b",base_url="http://127.0.0.1:11434",
               request_timeout=900.0,temperature=0.1,context_window=8192,thinking=False)
    index=VectorStoreIndex.from_vector_store(
        ChromaVectorStore(chroma_collection=coll),embed_model=embedding)
    reports=[]
    for label,indices in variants:
        fixed=[]
        for idx in indices:
            doc,meta,cid=by_idx[idx]
            node=TextNode(id_=cid,text=doc,metadata=meta)
            fixed.append(NodeWithScore(node=node,score=1.0))
        engine=CitationQueryEngine.from_args(
            index=index,retriever=FixedRetriever(fixed),llm=llm,
            citation_chunk_size=2048,citation_chunk_overlap=0,
            citation_qa_template=QA,citation_refine_template=REFINE,
            response_mode="compact")
        start=time.monotonic()
        response=engine.query(QUESTION)
        seconds=time.monotonic()-start
        answer=str(response)
        sources=list(response.source_nodes or [])
        cited=[int(n) for n in re.findall(r"\[(\d+)\]",answer)]
        invalid=sorted(set(cited)-set(range(1,len(sources)+1)))
        report=(f"=== {label} ===\nchunk_index={indices} gold={len(set(indices)&GOLD)}/3 "
                f"chars={sum(len(by_idx[i][0]) for i in indices)} tempo={seconds:.1f}s\n"
                f"RISPOSTA:\n{answer}\nCITAZIONI={cited} fuori_intervallo={invalid}\n"
                "FONTI:\n"+ "\n".join(
                    f"[{j}] chunk={n.node.metadata.get('chunk_index','?')} "
                    f"pages={n.node.metadata.get('page_numbers','?')} "
                    f"text={n.node.get_content()[:450]!r}" for j,n in enumerate(sources,1)))
        print(report,flush=True)
        reports.append(report)
        Path(args.output).write_text("\n\n".join(reports)+"\n",encoding="utf-8")
    print(f"FINE. Report: {args.output}. Nessuna modifica alla collection.",flush=True)

if __name__=="__main__":
    main()
