#!/usr/bin/env python3
"""Benchmark Glerean 3 casi: BGE5 vs TOP5 tecnico; read-only, output JSON.

Una generazione per variante/caso; non e' prova statistica.
Il report conserva testo completo dei chunk per audit citazioni.
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
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from sentence_transformers import CrossEncoder

from test_dribbling_v4_top5_top10 import DB,COLLECTION,SOURCE,QA,REFINE
from benchmark_generazione_contesti_q8_v4 import FixedRetriever,structural,expand

ROOT=Path("/opt/football-data-lab/projects/tactical-engine")
DEFAULT=ROOT/"benchmark_generazione_glerean_3casi.json"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default=str(DEFAULT))
    args=ap.parse_args()
    output=Path(args.output)
    if output.exists():
        raise FileExistsError(f"Report gia presente, non sovrascrivo: {output}")
    gold=json.loads((ROOT/"evaluation/gold_glerean_principi_v1.json").read_text(encoding="utf-8"))
    coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    if coll.count()!=86: raise RuntimeError("Collection V4 inattesa")
    rows=coll.get(where={"source":SOURCE},include=["documents","metadatas"])
    by_idx={int(m["chunk_index"]):(doc,m,cid) for doc,m,cid in zip(rows["documents"],rows["metadatas"],rows["ids"])}
    embed=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    bge=CrossEncoder("BAAI/bge-reranker-v2-m3",device="cpu",max_length=512)
    llm=Ollama(model="qwen3.5:9b",base_url="http://127.0.0.1:11434",
               request_timeout=900.0,temperature=0.1,context_window=8192,thinking=False)
    index=VectorStoreIndex.from_vector_store(ChromaVectorStore(chroma_collection=coll),embed_model=embed)
    report={"experiment":"BGE5_vs_TOP5_tecnico_Glerean","collection":COLLECTION,
            "generation":{"model":"qwen3.5:9b","temperature":0.1,"thinking":False,
                          "context_window":8192,"response_mode":"compact","citation_chunk_size":2048},
            "notes":["Gold claims non usati per retrieval","Una sola generazione per caso/variante",
                     "Le citazioni in range non garantiscono supporto semantico",
                     "Figure non verificate visivamente"],"runs":[]}
    for case in gold["cases"]:
        question=case["question"]
        vec=embed.get_query_embedding(question)
        hits=coll.query(query_embeddings=[vec],n_results=20,where={"source":SOURCE},
                        include=["documents","metadatas"])
        candidates=list(zip(hits["documents"][0],hits["metadatas"][0]))
        scores=bge.predict([(question,doc) for doc,_ in candidates],batch_size=1,show_progress_bar=False)
        ranking=[int(candidates[i][1]["chunk_index"]) for i in sorted(
            range(len(candidates)),key=lambda i:(-float(scores[i]),i))]
        anchors=ranking[:5]
        core=[i for i in anchors if not structural(by_idx[i][1],by_idx[i][0])]
        optimized=[]
        for idx in core+expand(core,by_idx)+ranking[5:]:
            doc,meta,_=by_idx[idx]
            if idx not in optimized and not structural(meta,doc): optimized.append(idx)
            if len(optimized)==5: break
        if len(optimized)!=5: raise RuntimeError("TOP5 tecnico incompleto")
        for label,indices in (("BGE5",anchors),("TOP5_tecnico",optimized)):
            nodes=[NodeWithScore(node=TextNode(id_=by_idx[i][2],text=by_idx[i][0],
                                             metadata=by_idx[i][1]),score=1.0) for i in indices]
            engine=CitationQueryEngine.from_args(
                index=index,retriever=FixedRetriever(nodes),llm=llm,
                citation_chunk_size=2048,citation_chunk_overlap=0,
                citation_qa_template=QA,citation_refine_template=REFINE,
                response_mode="compact")
            start=time.monotonic()
            response=engine.query(question)
            elapsed=time.monotonic()-start
            answer=str(response)
            sources=list(response.source_nodes or [])
            cited=[int(n) for n in re.findall(r"\[(\d+)\]",answer)]
            entry={"case_id":case["case_id"],"question":question,"variant":label,
                   "chunk_indices":indices,"context_chars":sum(len(by_idx[i][0]) for i in indices),
                   "seconds":round(elapsed,1),"answer":answer,
                   "citations":cited,"out_of_range":sorted(set(cited)-set(range(1,len(sources)+1))),
                   "gold_claims":[{"id":g["id"],"claim":g["claim"],"evidence":g["evidence"]}
                                  for g in case["gold_claims"]],
                   "sources":[{"citation_number":j,"chunk_index":n.node.metadata.get("chunk_index"),
                               "pages":n.node.metadata.get("page_numbers"),
                               "text":n.node.get_content()}
                              for j,n in enumerate(sources,1)]}
            report["runs"].append(entry)
            output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            print(f'{case["case_id"]} {label}: {elapsed:.1f}s, chunks={indices}, '
                  f'citazioni_fuori_intervallo={entry["out_of_range"]}',flush=True)
    print(f"COMPLETATO: {output} | {len(report['runs'])} generazioni; Chroma invariato",flush=True)

if __name__=="__main__":
    main()
