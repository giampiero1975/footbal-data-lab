#!/usr/bin/env python3
"""Esperimento read-only: espansione documentale di BGE TOP5 con budget fisso.

Selezione primaria BGE su 20 candidati; vicini +/-1 della stessa fonte e
stessa intestazione, ordinati per distanza dall'ancora. Non usa gold per
selezionare; gold Q8 solo per valutare. Nessuna modifica alla collection.
"""
import json
from pathlib import Path
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

ROOT = Path("/opt/football-data-lab")
SOURCE = "334_principi_Glerean"
COLLECTION = "dribbling_tactics_v4_qwen3_embedding_06b"
Q8 = "Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?"
GOLD = {16, 17, 21}
BUDGETS = (5, 7, 10)

def section(meta):
    value = meta.get("headings", "[]")
    headings = json.loads(value) if isinstance(value, str) else value
    return tuple(headings or [])

def main():
    coll = chromadb.PersistentClient(path=str(ROOT / "knowledge/rag/chroma")).get_collection(COLLECTION)
    if coll.count() != 86:
        raise RuntimeError("Collection V4 diversa dal baseline")
    records = coll.get(where={"source": SOURCE}, include=["documents", "metadatas"])
    by_index = {m["chunk_index"]: (cid, doc, m)
                for cid, doc, m in zip(records["ids"], records["documents"], records["metadatas"])}
    if len(by_index) != len(records["ids"]):
        raise RuntimeError("chunk_index duplicato")
    cases = [("Q8", Q8)]
    gold_path = ROOT / "projects/tactical-engine/evaluation/gold_glerean_principi_v1.json"
    cases.extend((c["case_id"], c["question"])
                 for c in json.loads(gold_path.read_text(encoding="utf-8"))["cases"])
    embed = OllamaEmbedding(model_name="qwen3-embedding:0.6b", base_url="http://127.0.0.1:11434")
    reranker = CrossEncoder("BAAI/bge-reranker-v2-m3", device="cpu", max_length=512)
    for case_id, question in cases:
        vec = embed.get_query_embedding(question)
        result = coll.query(query_embeddings=[vec], n_results=20, where={"source": SOURCE},
                            include=["documents", "metadatas"])
        candidates = list(zip(result["ids"][0], result["documents"][0], result["metadatas"][0]))
        scores = reranker.predict([(question, doc) for _, doc, _ in candidates],
                                  batch_size=1, show_progress_bar=False)
        order = sorted(range(len(candidates)), key=lambda i: (-float(scores[i]), i))
        anchors = [candidates[i][2]["chunk_index"] for i in order[:5]]
        # Alterna ancore e vicini per non assegnare tutto il budget a una sola sezione.
        neighbors = []
        for anchor in anchors:
            if anchor not in by_index:
                continue
            parent_section = section(by_index[anchor][2])
            for offset in (-1, 1):
                neighbor = anchor + offset
                if neighbor in by_index and section(by_index[neighbor][2]) == parent_section:
                    if neighbor not in anchors and neighbor not in neighbors:
                        neighbors.append(neighbor)
        print(f"\\n{case_id}: {question}", flush=True)
        print(f"  BGE TOP5={anchors} | adiacenti stessa sezione={neighbors}", flush=True)
        for budget in BUDGETS:
            # TOP5 invariato; gli slot aggiuntivi sono occupati dai vicini,
            # poi dai successivi risultati BGE, se necessario.
            chosen = list(anchors)
            for idx in neighbors:
                if len(chosen) >= budget:
                    break
                if idx not in chosen:
                    chosen.append(idx)
            for i in order[5:]:
                if len(chosen) >= budget:
                    break
                idx = candidates[i][2]["chunk_index"]
                if idx not in chosen:
                    chosen.append(idx)
            if case_id == "Q8":
                print(f"  budget={budget} chunks={chosen} gold={len(GOLD.intersection(chosen))}/3", flush=True)
            else:
                print(f"  budget={budget} chunks={chosen} (gold non mappati)", flush=True)
    print("\\nFINE: sola lettura.", flush=True)

if __name__ == "__main__":
    main()
