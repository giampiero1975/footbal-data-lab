#!/usr/bin/env python3
"""Diagnostica read-only dei chunk dominanti Q8 e copertura dense dei gold Glerean.

Non modifica collection, embedding, configurazione o modelli.
"""
import json
import time
from pathlib import Path
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding

ROOT = Path("/opt/football-data-lab")
COLLECTION = "dribbling_tactics_v4_qwen3_embedding_06b"
SOURCE = "334_principi_Glerean"
QUESTION = "Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?"
CHUNKS = {0, 2, 16, 17, 21}
GOLD_PATHS = [
    ROOT / "projects/tactical-engine/evaluation/gold_glerean_ampiezza_v1.json",
    ROOT / "projects/tactical-engine/evaluation/gold_glerean_principi_v1.json",
]

def main():
    collection = chromadb.PersistentClient(path=str(ROOT / "knowledge/rag/chroma")).get_collection(COLLECTION)
    assert collection.count() == 86, "Collection V4 inattesa"
    result = collection.get(where={"source": SOURCE}, include=["documents", "metadatas"])
    matches = [(cid, doc, meta) for cid, doc, meta in zip(result["ids"], result["documents"], result["metadatas"])
               if meta.get("chunk_index") in CHUNKS]
    print(f"Chunk richiesti {sorted(CHUNKS)}; trovati {len(matches)}", flush=True)
    for cid, doc, meta in sorted(matches, key=lambda item: item[2]["chunk_index"]):
        print(f"\\n{'='*72}\\nCHUNK {meta['chunk_index']} ID {cid} PAGINE {meta.get('pages')}\\n{'='*72}", flush=True)
        print(doc, flush=True)
    embedder = OllamaEmbedding(model_name="qwen3-embedding:0.6b", base_url="http://127.0.0.1:11434")
    cases = [{"case_id": "Q8", "question": QUESTION}]
    for path in GOLD_PATHS:
        data = json.loads(path.read_text(encoding="utf-8"))
        for case in data.get("cases", []):
            cases.append({"case_id": case.get("case_id", "?"), "question": case["question"]})
    seen = set()
    for case in cases:
        if case["question"] in seen:
            continue
        seen.add(case["question"])
        t0 = time.perf_counter()
        vec = embedder.get_query_embedding(case["question"])
        hits = collection.query(query_embeddings=[vec], n_results=10, where={"source": SOURCE},
                                include=["metadatas", "distances"])
        chunks = [m.get("chunk_index") for m in hits["metadatas"][0]]
        print(f"\\nQUERY {case['case_id']}: {case['question']}\\nDENSE TOP10: {chunks} | {time.perf_counter()-t0:.2f}s", flush=True)
    print("\\nFINE: sola lettura.", flush=True)

if __name__ == "__main__":
    main()
