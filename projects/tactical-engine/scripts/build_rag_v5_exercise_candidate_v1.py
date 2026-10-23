#!/usr/bin/env python3
"""Build an isolated exercise candidate collection; never modify V5 baseline.

Default: offline plan only. Explicit --write-candidate is required to embed.
Only Ussia V2 exercise units are eligible; no automatic promotion.
"""
import argparse
import hashlib
import json
from pathlib import Path
from extract_exercise_units_v2 import extract

ROOT = Path("/opt/football-data-lab")
CHROMA = ROOT / "knowledge/rag/chroma"
BASELINE = "dribbling_tactics_v5_multisource"
CANDIDATE = "dribbling_tactics_v5_exercise_candidate_v1"
MODEL = "qwen3-embedding:0.6b"

def rows(path):
    source = path.stem
    doc = json.loads(path.read_text(encoding="utf-8"))
    units = extract(doc, source)
    if not units:
        raise ValueError("No exercise units: " + str(path))
    for unit in units:
        if not unit["pages"] or not unit["text"].strip():
            raise ValueError("Incomplete unit " + unit["heading_ref"])
        text = unit["title"] + "\n" + unit["text"]
        identifier = hashlib.sha256(("exercise-candidate-v1|" + source + "|" + unit["heading_ref"] + "|" + text).encode()).hexdigest()
        meta = {"source": source, "source_json": str(path), "source_relative": path.relative_to(ROOT / "knowledge/processed").as_posix(),
                "page_numbers": json.dumps(unit["pages"]), "headings": json.dumps([unit["title"]], ensure_ascii=False),
                "heading_ref": unit["heading_ref"], "exercise_id": unit["exercise_id"],
                "version": "v5_exercise_candidate_v1", "embedding_model": MODEL}
        yield identifier, text, meta

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=ROOT / "knowledge/processed/formations-and-systems/Transizioni.Ussia.json")
    ap.add_argument("--write-candidate", action="store_true")
    ap.add_argument("--resume-candidate", action="store_true", help="Resume only verified partial candidate records")
    ap.add_argument("--batch-size", type=int, default=4)
    args = ap.parse_args()
    if args.write_candidate and args.resume_candidate:
        ap.error("Choose --write-candidate or --resume-candidate, not both")
    if args.batch_size < 1:
        ap.error("batch-size must be positive")
    path = args.input.resolve()
    if not path.is_file() or not path.is_relative_to((ROOT / "knowledge/processed").resolve()):
        ap.error("Input must be an existing Docling JSON under knowledge/processed")
    if "ussia" not in path.stem.lower():
        ap.error("Only Ussia is enabled for this isolated candidate")
    data = list(rows(path))
    if len({r[0] for r in data}) != len(data):
        raise RuntimeError("Duplicate candidate IDs")
    print(f"PLAN candidate={CANDIDATE} source={path.name} units={len(data)}")
    if not (args.write_candidate or args.resume_candidate):
        print("DRY_RUN: no Chroma access, no embeddings, no writes")
        return
    import chromadb
    from llama_index.embeddings.ollama import OllamaEmbedding
    db = chromadb.PersistentClient(path=str(CHROMA))
    if BASELINE not in [c.name for c in db.list_collections()]:
        raise RuntimeError("Baseline V5 missing; refusing write")
    baseline_before = db.get_collection(BASELINE).count()
    names = {c.name for c in db.list_collections()}
    if args.resume_candidate:
        if CANDIDATE not in names:
            raise RuntimeError("No partial candidate exists")
        collection = db.get_collection(CANDIDATE)
        if collection.metadata != {"embedding_model": MODEL, "pipeline": "v5_exercise_candidate_v1", "source": path.name}:
            raise RuntimeError("Candidate metadata mismatch")
        old = collection.get(include=["documents", "metadatas"])
        expected = {identifier: (document, metadata) for identifier, document, metadata in data}
        for i, identifier in enumerate(old["ids"]):
            if identifier not in expected or old["documents"][i] != expected[identifier][0] or old["metadatas"][i] != expected[identifier][1]:
                raise RuntimeError("Candidate contains unexpected or changed record: " + identifier)
        existing = set(old["ids"])
        print(f"RESUME verified_existing={len(existing)} missing={len(data)-len(existing)}")
    else:
        if CANDIDATE in names:
            raise RuntimeError("Candidate already exists; refusing overwrite")
        collection = db.create_collection(CANDIDATE, metadata={"embedding_model": MODEL, "pipeline": "v5_exercise_candidate_v1", "source": path.name})
        existing = set()
    embedder = OllamaEmbedding(model_name=MODEL, base_url="http://127.0.0.1:11434")
    for offset in range(0, len(data), args.batch_size):
        batch = [row for row in data[offset:offset + args.batch_size] if row[0] not in existing]
        if not batch:
            continue
        vectors = embedder.get_text_embedding_batch([r[1] for r in batch], show_progress=False)
        collection.add(ids=[r[0] for r in batch], documents=[r[1] for r in batch], metadatas=[r[2] for r in batch], embeddings=vectors)
    if db.get_collection(BASELINE).count() != baseline_before:
        raise RuntimeError("Baseline count changed; investigate immediately")
    final = collection.get(include=[])
    if set(final["ids"]) != {r[0] for r in data}:
        raise RuntimeError("Candidate incomplete after write")
    print(f"CANDIDATE_COMPLETE rows={collection.count()} baseline_unchanged={baseline_before}")

if __name__ == "__main__":
    main()
