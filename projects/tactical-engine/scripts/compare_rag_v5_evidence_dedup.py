#!/usr/bin/env python3
"""Read-only V5 retrieval comparison: existing source-scoped vs global exact text dedup.

Does not generate LLM answers or write to ChromaDB. Same retrieval/rerank for both.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import time

import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

COLLECTION = "dribbling_tactics_v5_multisource"
DB = "/opt/football-data-lab/knowledge/rag/chroma"
ALIASES = {
    "Allegati_222010155625": "LA TECNICA APPLICATA COME PRESUPPOSTO DEL GIOCO COLLETTIVO",
    "Allegati_45201211489": "Conseiderazione sul sistema di gioco 4-3-2-1",
    "Allegati_71201095736": "IL CONCETTO DI MARCAMENTO NELLA DIFESA AD UOMO E A ZONA",
    "Categoria_Tattiche del calcio - Wikipedia(1)": "Categoria_Tattiche del calcio - Wikipedia",
}
QUESTIONS = [
    ("q1", "Come affrontare con il 4-4-2 una squadra schierata con il 3-4-1-2?"),
    ("q2", "Come creare superiorità numerica in fase di possesso palla?"),
    ("q3", "Quali principi favoriscono la verticalizzazione nella fase offensiva?"),
    ("q4", "Come sfruttare i triangoli per sviluppare il gioco di squadra?"),
    ("q5", "Quali vantaggi e rischi comporta variare il sistema di gioco durante una partita?"),
]

def normalize(value):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", value.casefold())).strip()

def select(rows, *, global_text_dedup):
    selected, seen = [], set()
    for row in rows:
        # Preserve existing behavior for baseline; only key differs for candidate.
        key = row["fingerprint"] if global_text_dedup else (ALIASES.get(row["source"], row["source"]), row["fingerprint"])
        if key in seen:
            continue
        seen.add(key)
        selected.append(row)
        if len(selected) == 8:
            break
    return selected

def slim(row):
    return {k: row[k] for k in ("id", "source", "pages", "rerank_score", "rank", "fingerprint")}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--questions", nargs="+", choices=[q[0] for q in QUESTIONS], default=[q[0] for q in QUESTIONS])
    args = p.parse_args()

    collection = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    count_before = collection.count()
    if count_before != 5319:
        raise RuntimeError(f"Unexpected V5 size: {count_before}")

    embedding = OllamaEmbedding(model_name="qwen3-embedding:0.6b", base_url="http://127.0.0.1:11434")
    reranker = CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1", device="cpu", max_length=512)
    report = {"collection": COLLECTION, "count_before": count_before,
              "mode": "read_only_same_24_candidates_same_reranker",
              "questions": [], "limitations": [
                  "Only normalized exact text matches are deduplicated; semantic near-duplicates remain.",
                  "Replacing evidence is not proof of improved answer quality.",
                  "Source provenance is retained for each selected chunk.",
                  "No generation or deployment is performed.",
              ]}
    for qid, question in QUESTIONS:
        if qid not in args.questions:
            continue
        started = time.monotonic()
        got = collection.query(query_embeddings=[embedding.get_query_embedding(question)], n_results=24,
                               include=["documents", "metadatas", "distances"])
        rows = []
        for cid, doc, meta, dist in zip(got["ids"][0], got["documents"][0],
                                         got["metadatas"][0], got["distances"][0]):
            raw = meta.get("raw_text") or doc
            rows.append({"id": cid, "source": meta["source"], "pages": meta.get("page_numbers"),
                         "text": doc, "distance": round(float(dist), 5),
                         "fingerprint": hashlib.sha256(normalize(raw).encode()).hexdigest()})
        scores = reranker.predict([(question, row["text"]) for row in rows],
                                  batch_size=1, show_progress_bar=False)
        for i, score in enumerate(scores):
            rows[i]["rerank_score"] = round(float(score), 6)
        rows.sort(key=lambda r: r["rerank_score"], reverse=True)
        for rank, row in enumerate(rows, 1):
            row["rank"] = rank

        baseline = select(rows, global_text_dedup=False)
        candidate = select(rows, global_text_dedup=True)
        baseline_ids = {r["id"] for r in baseline}
        candidate_ids = {r["id"] for r in candidate}
        removed = [slim(r) for r in baseline if r["id"] not in candidate_ids]
        added = [slim(r) for r in candidate if r["id"] not in baseline_ids]
        result = {"id": qid, "question": question, "retrieved": len(rows),
                  "baseline": [slim(r) for r in baseline],
                  "candidate": [slim(r) for r in candidate],
                  "removed": removed, "added": added,
                  "candidate_unique_fingerprints": len({r["fingerprint"] for r in candidate}),
                  "elapsed_seconds": round(time.monotonic()-started, 2)}
        report["questions"].append(result)
        print(f"{qid}: removed={len(removed)} added={len(added)} "
              f"candidate={len(candidate)} elapsed={result['elapsed_seconds']}s", flush=True)

    report["count_after"] = collection.count()
    report["index_unchanged"] = report["count_before"] == report["count_after"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("REPORT:", args.output, "V5 unchanged:", report["index_unchanged"], flush=True)

if __name__ == "__main__":
    main()
