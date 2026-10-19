#!/usr/bin/env python3
"""Esperimento read-only MMR su V4: ranking denso vs selezione diversificata.

MMR = lambda * cos(query, doc) - (1-lambda) * max cos(doc, selected).
Nessun gold influenza la selezione; i gold sono usati solo per il report.
"""
import json
from pathlib import Path

import chromadb
import numpy as np
from llama_index.embeddings.ollama import OllamaEmbedding

ROOT = Path("/opt/football-data-lab")
SOURCE = "334_principi_Glerean"
COLLECTION = "dribbling_tactics_v4_qwen3_embedding_06b"
Q8_GOLD = {16, 17, 21}
LAMBDAS = (0.3, 0.5, 0.7, 0.9)
FETCH = (15, 30)


def normalized(matrix):
    matrix = np.asarray(matrix, dtype=np.float64)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Embedding con norma zero")
    return matrix / norms


def mmr(query_vector, doc_vectors, limit, weight):
    docs = normalized(doc_vectors)
    query = normalized(np.asarray(query_vector).reshape(1, -1))[0]
    relevance = docs @ query
    similarity = docs @ docs.T
    chosen = []
    remaining = set(range(len(docs)))
    for _ in range(min(limit, len(docs))):
        if not chosen:
            idx = int(np.argmax(relevance))
        else:
            idx = max(remaining, key=lambda i: (
                weight * relevance[i] - (1 - weight) * max(similarity[i, j] for j in chosen),
                relevance[i],
                -i,
            ))
        chosen.append(idx)
        remaining.remove(idx)
    return chosen


def main():
    collection = chromadb.PersistentClient(path=str(ROOT / "knowledge/rag/chroma")).get_collection(COLLECTION)
    if collection.count() != 86:
        raise RuntimeError("V4 non corrisponde al baseline atteso")
    gold_path = ROOT / "projects/tactical-engine/evaluation/gold_glerean_principi_v1.json"
    cases = [("Q8", "Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?", Q8_GOLD)]
    for case in json.loads(gold_path.read_text(encoding="utf-8"))["cases"]:
        cases.append((case["case_id"], case["question"], None))
    embedder = OllamaEmbedding(model_name="qwen3-embedding:0.6b", base_url="http://127.0.0.1:11434")
    for case_id, question, gold in cases:
        query = embedder.get_query_embedding(question)
        print(f"\nCASO {case_id}: {question}", flush=True)
        for fetch in FETCH:
            result = collection.query(
                query_embeddings=[query], n_results=fetch,
                where={"source": SOURCE}, include=["metadatas", "embeddings"],
            )
            ids = result["ids"][0]
            metadata = result["metadatas"][0]
            vectors = result["embeddings"][0]
            if len(ids) != fetch or len(set(ids)) != len(ids):
                raise RuntimeError(f"Candidati inattesi per {case_id}: {len(ids)}")
            labels = [meta["chunk_index"] for meta in metadata]
            baseline = labels[:5]
            score = f" gold={len(set(baseline) & gold)}/{len(gold)}" if gold else ""
            print(f"  dense fetch={fetch} TOP5={baseline}{score}", flush=True)
            for weight in LAMBDAS:
                chosen = mmr(query, vectors, 5, weight)
                selected = [labels[i] for i in chosen]
                score = f" gold={len(set(selected) & gold)}/{len(gold)}" if gold else ""
                print(f"  MMR fetch={fetch} lambda={weight:.1f} TOP5={selected}{score}", flush=True)
    print("\nFINE: nessuna modifica a Chroma.", flush=True)


if __name__ == "__main__":
    main()
