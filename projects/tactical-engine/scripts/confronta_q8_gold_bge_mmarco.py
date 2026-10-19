#!/usr/bin/env python3
"""Q8 Glerean: confronto read-only BGE/mMARCO sui medesimi 15 candidati V4.

Gold ancorati al testo verificato dei chunk 16, 17 e 21.
Non modifica collection, embedding, modelli o configurazione.
"""
import time
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

DB = "/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION = "dribbling_tactics_v4_qwen3_embedding_06b"
SOURCE = "334_principi_Glerean"
QUESTION = "Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?"
GOLD = {
    16: "Palla in difesa: quattro attaccanti centrali, centrocampisti esterni larghi",
    17: "Palla a centrocampo: attaccanti esterni larghi",
    21: "Palla ai centrocampisti: laterali in ampiezza e profondita",
}

def main():
    coll = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    if coll.count() != 86:
        raise RuntimeError("Numero record V4 inatteso; benchmark interrotto")
    embedder = OllamaEmbedding(model_name="qwen3-embedding:0.6b", base_url="http://127.0.0.1:11434")
    t0 = time.perf_counter()
    vector = embedder.get_query_embedding(QUESTION)
    result = coll.query(query_embeddings=[vector], n_results=15,
                        where={"source": SOURCE},
                        include=["documents", "metadatas", "distances"])
    candidates = list(zip(result["ids"][0], result["documents"][0],
                          result["metadatas"][0], result["distances"][0]))
    print(f"Embedding + retrieval: {time.perf_counter()-t0:.2f}s; candidati: {len(candidates)}", flush=True)
    if len(candidates) != 15:
        raise RuntimeError("Attesi esattamente 15 candidati")
    for idx, (cid, doc, meta, dist) in enumerate(candidates, 1):
        if meta.get("chunk_index") in GOLD:
            print(f"DENSE {idx}: chunk {meta['chunk_index']} | id={cid[:12]} | distanza={dist:.4f}", flush=True)
    for name, model_name in [
        ("BGE", "BAAI/bge-reranker-v2-m3"),
        ("mMARCO", "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"),
    ]:
        print(f"Carico {name}...", flush=True)
        model = CrossEncoder(model_name, device="cpu", max_length=512)
        t0 = time.perf_counter()
        scores = model.predict([(QUESTION, doc) for _, doc, _, _ in candidates],
                               batch_size=1, show_progress_bar=False)
        ranked = sorted(range(len(candidates)), key=lambda i: float(scores[i]), reverse=True)
        print(f"{name}: reranking {time.perf_counter()-t0:.2f}s", flush=True)
        positions = {candidates[i][2].get("chunk_index"): rank
                     for rank, i in enumerate(ranked, 1)}
        for chunk, description in GOLD.items():
            pos = positions.get(chunk)
            print(f"  chunk {chunk} | posizione {pos if pos is not None else 'ASSENTE'}"
                  f" | top5={bool(pos and pos <= 5)} | top10={bool(pos and pos <= 10)}"
                  f" | {description}", flush=True)
        for k in (5, 10):
            covered = sum(1 for chunk in GOLD if positions.get(chunk, 999) <= k)
            print(f"  {name} copertura gold@{k}: {covered}/{len(GOLD)}", flush=True)
        print("  TOP10 (rank | chunk | id | score):", flush=True)
        for rank, i in enumerate(ranked[:10], 1):
            cid, _, meta, _ = candidates[i]
            print(f"    {rank:2d} | {meta.get('chunk_index')} | {cid[:12]} | {float(scores[i]):.3f}", flush=True)
    print("FINE: benchmark di sola lettura.", flush=True)

if __name__ == "__main__":
    main()
