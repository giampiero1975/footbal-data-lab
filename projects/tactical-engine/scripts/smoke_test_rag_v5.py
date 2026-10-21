#!/usr/bin/env python3
"""Read-only V5 retrieval smoke test across tactical documents."""
import chromadb
from collections import Counter
from llama_index.embeddings.ollama import OllamaEmbedding

DB="/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION="dribbling_tactics_v5_multisource"
QUESTIONS=[
    "Come affrontare con il 4-4-2 una squadra schierata con il 3-4-1-2?",
    "Come creare superiorità numerica in fase di possesso palla?",
    "Quali principi favoriscono la verticalizzazione nella fase offensiva?",
    "Come sfruttare i triangoli per sviluppare il gioco di squadra?",
    "Quali vantaggi e rischi comporta variare il sistema di gioco durante una partita?",
]

def main():
    db=chromadb.PersistentClient(path=DB)
    coll=db.get_collection(COLLECTION)
    count=coll.count()
    print(f"COLLECTION={COLLECTION} COUNT={count}",flush=True)
    if count!=5319:
        raise RuntimeError(f"Unexpected V5 count: {count}")
    embedding=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    for i,q in enumerate(QUESTIONS,1):
        vector=embedding.get_query_embedding(q)
        result=coll.query(query_embeddings=[vector],n_results=8,include=["documents","metadatas","distances"])
        ids=result["ids"][0]
        metas=result["metadatas"][0]
        docs=result["documents"][0]
        distances=result["distances"][0]
        print(f"\nQ{i}: {q}",flush=True)
        print("SOURCES_TOP8:",dict(Counter(m["source"] for m in metas)),flush=True)
        for rank,(cid,meta,doc,distance) in enumerate(zip(ids,metas,docs,distances),1):
            print(f" {rank}. source={meta['source']} pages={meta.get('page_numbers')} distance={distance:.4f} id={cid[:12]}",flush=True)
            print("    "+doc.replace("\n"," ")[:220],flush=True)
    print("\nSMOKE TEST COMPLETE (read-only; no quality score assigned)",flush=True)

if __name__=="__main__":
    main()
