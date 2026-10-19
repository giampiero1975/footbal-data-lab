#!/usr/bin/env python3
"""Ablazione read-only: BGE baseline vs esclusione chunk strutturali.

Regola indipendente dal gold: rimuove soltanto chunk che sono titoli
senza corpo oppure premesse esplicitamente marcate PREMESSA.
"""
import json
import time
from pathlib import Path
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

ROOT = Path("/opt/football-data-lab")
SOURCE = "334_principi_Glerean"
COLLECTION = "dribbling_tactics_v4_qwen3_embedding_06b"
QUESTION = "Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?"
GOLD = {16, 17, 21}

def structural(meta, doc):
    headings = json.loads(meta.get("headings", "[]"))
    raw = meta.get("raw_text", doc).strip()
    title_only = len(raw) < 80
    preface = any(h.strip().casefold() in {"premessa", "prefazione", "indice", "sommario"} for h in headings)
    return title_only or preface

def main():
    coll = chromadb.PersistentClient(path=str(ROOT / "knowledge/rag/chroma")).get_collection(COLLECTION)
    if coll.count() != 86:
        raise RuntimeError("Collection V4 diversa dal baseline")
    cases = [("Q8", QUESTION)]
    path = ROOT / "projects/tactical-engine/evaluation/gold_glerean_principi_v1.json"
    cases += [(c["case_id"], c["question"]) for c in json.loads(path.read_text(encoding="utf-8"))["cases"]]
    embed = OllamaEmbedding(model_name="qwen3-embedding:0.6b", base_url="http://127.0.0.1:11434")
    model = CrossEncoder("BAAI/bge-reranker-v2-m3", device="cpu", max_length=512)
    for case_id, question in cases:
        vec = embed.get_query_embedding(question)
        hits = coll.query(query_embeddings=[vec], n_results=20, where={"source": SOURCE},
                          include=["documents", "metadatas"])
        candidates = list(zip(hits["ids"][0], hits["documents"][0], hits["metadatas"][0]))
        scores = model.predict([(question, doc) for _, doc, _ in candidates], batch_size=1,
                               show_progress_bar=False)
        ranked = sorted(range(len(candidates)), key=lambda i: (-float(scores[i]), i))
        kept = [i for i in ranked if not structural(candidates[i][2], candidates[i][1])]
        excluded = [(candidates[i][2].get("chunk_index"), candidates[i][2].get("headings"))
                    for i in ranked if structural(candidates[i][2], candidates[i][1])]
        print(f"\\n{case_id}: {question}", flush=True)
        print(f"  esclusi (chunk, headings): {excluded}", flush=True)
        for label, ranking in [("BGE baseline", ranked), ("BGE senza strutturali", kept)]:
            chunks = [candidates[i][2]["chunk_index"] for i in ranking[:10]]
            coverage = f" gold@5={len(set(chunks[:5]) & GOLD)}/3 gold@10={len(set(chunks) & GOLD)}/3" if case_id == "Q8" else ""
            print(f"  {label}: top5={chunks[:5]} top10={chunks}{coverage}", flush=True)
    print("\\nFINE: nessuna scrittura.", flush=True)

if __name__ == "__main__":
    main()
