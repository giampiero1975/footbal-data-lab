#!/usr/bin/env python3
"""Confronto read-only: BGE5, espansione7, TOP5 tecnico con espansione.

Gold usato solo per valutare. Stampa fonti complete per revisione manuale.
"""
import json
from pathlib import Path
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

ROOT=Path("/opt/football-data-lab")
COLLECTION="dribbling_tactics_v4_qwen3_embedding_06b"
SOURCE="334_principi_Glerean"
Q8="Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?"
GOLD={16,17,21}

def headings(m):
    v=m.get("headings","[]")
    return tuple(json.loads(v) if isinstance(v,str) else v)

def structural(m,doc):
    return len(m.get("raw_text",doc).strip())<80 or any(
        h.strip().casefold() in {"premessa","prefazione","indice","sommario"}
        for h in headings(m))

def expand(anchors,by_idx):
    neighbors=[]
    for anchor in anchors:
        doc,meta=by_idx[anchor]
        if structural(meta,doc): continue
        for n in (anchor-1,anchor+1):
            if n in by_idx and n not in anchors and n not in neighbors:
                ndoc,nmeta=by_idx[n]
                if headings(nmeta)==headings(meta) and not structural(nmeta,ndoc):
                    neighbors.append(n)
    return neighbors

def main():
    coll=chromadb.PersistentClient(path=str(ROOT/"knowledge/rag/chroma")).get_collection(COLLECTION)
    if coll.count()!=86: raise RuntimeError("Collection V4 non corrisponde al baseline")
    data=coll.get(where={"source":SOURCE},include=["documents","metadatas"])
    by_idx={m["chunk_index"]:(doc,m) for doc,m in zip(data["documents"],data["metadatas"])}
    cases=[("Q8",Q8)]
    path=ROOT/"projects/tactical-engine/evaluation/gold_glerean_principi_v1.json"
    cases.extend((c["case_id"],c["question"]) for c in json.loads(path.read_text(encoding="utf-8"))["cases"])
    embed=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    bge=CrossEncoder("BAAI/bge-reranker-v2-m3",device="cpu",max_length=512)
    for name,question in cases:
        vec=embed.get_query_embedding(question)
        hits=coll.query(query_embeddings=[vec],n_results=20,where={"source":SOURCE},include=["documents","metadatas"])
        rows=list(zip(hits["documents"][0],hits["metadatas"][0]))
        scores=bge.predict([(question,doc) for doc,_ in rows],batch_size=1,show_progress_bar=False)
        order=sorted(range(len(rows)),key=lambda i:(-float(scores[i]),i))
        ranking=[rows[i][1]["chunk_index"] for i in order]
        anchors=ranking[:5]
        expansion=expand(anchors,by_idx)
        bge5=anchors
        bge7=(anchors+expansion+ranking[5:])[:7]
        # TOP5 tecnico: solo ancore non strutturali, poi adiacenti,
        # poi altri risultati BGE non strutturali.
        core=[i for i in anchors if not structural(*reversed(by_idx[i]))]
        technical_neighbors=expand(core,by_idx)
        candidates=core+technical_neighbors+ranking[5:]
        optimized=[]
        for idx in candidates:
            doc,meta=by_idx[idx]
            if idx not in optimized and not structural(meta,doc):
                optimized.append(idx)
            if len(optimized)==5: break
        if len(optimized)!=5: raise RuntimeError("Candidati insufficienti")
        print(f"\n{name}: {question}",flush=True)
        for label,selected in [("BGE5",bge5),("BGE7_espansione",bge7),("TOP5_tecnico",optimized)]:
            gold=f" gold={len(set(selected)&GOLD)}/3" if name=="Q8" else ""
            print(f"  {label}: {selected}{gold} chars={sum(len(by_idx[i][0]) for i in selected)}",flush=True)
        if name=="Q8":
            print("  TOP5 tecnico: evidenze per controllo manuale:",flush=True)
            for idx in optimized:
                doc,meta=by_idx[idx]
                print(f"    CHUNK {idx} pagine={meta.get('page_numbers')} heading={headings(meta)}",flush=True)
                print(f"    TESTO: {doc[:1600]}",flush=True)
    print("\nFINE: nessuna scrittura.",flush=True)

if __name__=="__main__":
    main()
