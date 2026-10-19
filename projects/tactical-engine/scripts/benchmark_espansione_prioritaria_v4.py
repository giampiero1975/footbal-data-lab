#!/usr/bin/env python3
"""Ablazione read-only: espansione BGE con priorita a sezioni tecniche.

Confronta adiacenza ingenua vs priorita alle ancore con contenuto operativo.
Il gold Q8 viene usato esclusivamente per valutare.
"""
import json
from pathlib import Path
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

ROOT=Path("/opt/football-data-lab")
SOURCE="334_principi_Glerean"
COLLECTION="dribbling_tactics_v4_qwen3_embedding_06b"
GOLD={16,17,21}
Q8="Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?"

def headings(meta):
    v=meta.get("headings","[]")
    return tuple(json.loads(v) if isinstance(v,str) else v)

def structural(meta,doc):
    hs=headings(meta)
    return len(meta.get("raw_text",doc).strip())<80 or any(
        h.strip().casefold() in {"premessa","prefazione","indice","sommario"}
        for h in hs)

def expand(anchors,by_index,priority):
    ordered=sorted(anchors,key=lambda a:(structural(by_index[a][2],by_index[a][1]),anchors.index(a))) if priority else anchors
    neighbors=[]
    for anchor in ordered:
        h=headings(by_index[anchor][2])
        for near in (anchor-1,anchor+1):
            if near in by_index and near not in anchors and near not in neighbors:
                if headings(by_index[near][2])==h:
                    if not priority or not structural(by_index[near][2],by_index[near][1]):
                        neighbors.append(near)
    return neighbors

def main():
    coll=chromadb.PersistentClient(path=str(ROOT/"knowledge/rag/chroma")).get_collection(COLLECTION)
    if coll.count()!=86: raise RuntimeError("V4 baseline non corrisponde")
    allrows=coll.get(where={"source":SOURCE},include=["documents","metadatas"])
    by_index={m["chunk_index"]:(cid,doc,m) for cid,doc,m in zip(allrows["ids"],allrows["documents"],allrows["metadatas"])}
    cases=[("Q8",Q8)]
    path=ROOT/"projects/tactical-engine/evaluation/gold_glerean_principi_v1.json"
    cases.extend((c["case_id"],c["question"]) for c in json.loads(path.read_text(encoding="utf-8"))["cases"])
    embed=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    model=CrossEncoder("BAAI/bge-reranker-v2-m3",device="cpu",max_length=512)
    for name,question in cases:
        vec=embed.get_query_embedding(question)
        hits=coll.query(query_embeddings=[vec],n_results=20,where={"source":SOURCE},include=["documents","metadatas"])
        rows=list(zip(hits["ids"][0],hits["documents"][0],hits["metadatas"][0]))
        scores=model.predict([(question,doc) for _,doc,_ in rows],batch_size=1,show_progress_bar=False)
        order=sorted(range(len(rows)),key=lambda i:(-float(scores[i]),i))
        anchors=[rows[i][2]["chunk_index"] for i in order[:5]]
        print(f"\n{name}: anchors={anchors}",flush=True)
        for label,priority in [("adiacenza originale",False),("adiacenza tecnica prioritaria",True)]:
            neighbors=expand(anchors,by_index,priority)
            for budget in (5,7,10):
                chosen=(anchors+neighbors)[:budget]
                for i in order[5:]:
                    if len(chosen)>=budget: break
                    idx=rows[i][2]["chunk_index"]
                    if idx not in chosen: chosen.append(idx)
                cov=f" gold={len(GOLD.intersection(chosen))}/3" if name=="Q8" else ""
                print(f"  {label} budget={budget} neighbors={neighbors} chunks={chosen}{cov}",flush=True)
    print("\nFINE: nessuna scrittura.",flush=True)

if __name__=="__main__":
    main()
