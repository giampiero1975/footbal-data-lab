#!/usr/bin/env python3
"""Ablazione read-only dei chunk brevi e diagnostica metadati V4."""
import json
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from pathlib import Path

ROOT = Path("/opt/football-data-lab")
COLLECTION = "dribbling_tactics_v4_qwen3_embedding_06b"
SOURCE = "334_principi_Glerean"
THRESHOLDS = (0, 80, 160, 300)
QUESTIONS = [("Q8", "Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?", {16,17,21})]

def main():
    coll = chromadb.PersistentClient(path=str(ROOT / "knowledge/rag/chroma")).get_collection(COLLECTION)
    if coll.count() != 86:
        raise RuntimeError("Collection V4 inattesa")
    rows = coll.get(where={"source": SOURCE}, include=["documents","metadatas"])
    by_id = {cid:(doc,meta) for cid,doc,meta in zip(rows["ids"],rows["documents"],rows["metadatas"])}
    for cid,(doc,meta) in sorted(by_id.items(),key=lambda x:x[1][1].get("chunk_index",-1)):
        if meta.get("chunk_index") in (0,2,16,17,21):
            print(f"META chunk={meta.get('chunk_index')} chars={len(doc)} keys={sorted(meta)} values={json.dumps(meta,ensure_ascii=False)}",flush=True)
    for path in [ROOT/"projects/tactical-engine/evaluation/gold_glerean_principi_v1.json"]:
        for case in json.loads(path.read_text(encoding="utf-8"))["cases"]:
            QUESTIONS.append((case["case_id"],case["question"],None))
    emb = OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    for name,question,gold in QUESTIONS:
        vec=emb.get_query_embedding(question)
        hits=coll.query(query_embeddings=[vec],n_results=30,where={"source":SOURCE},include=["metadatas"])
        ids=hits["ids"][0]
        print(f"\\nQUERY {name}: {question}",flush=True)
        for threshold in THRESHOLDS:
            selected=[cid for cid in ids if len(by_id[cid][0])>=threshold][:10]
            chunks=[by_id[cid][1].get("chunk_index") for cid in selected]
            covered=f"{len(gold.intersection(chunks))}/{len(gold)}" if gold else "gold chunks non mappati"
            print(f"min_chars={threshold}: top5={chunks[:5]} top10={chunks} Q8_gold@5={covered if gold else 'n/a'}",flush=True)
        if gold:
            for threshold in THRESHOLDS:
                chunks=[by_id[cid][1].get("chunk_index") for cid in ids if len(by_id[cid][0])>=threshold][:5]
                print(f"Q8 min_chars={threshold}: gold@5={len(gold.intersection(chunks))}/{len(gold)}",flush=True)
    print("FINE: nessuna scrittura su Chroma.",flush=True)

if __name__=="__main__":
    main()
