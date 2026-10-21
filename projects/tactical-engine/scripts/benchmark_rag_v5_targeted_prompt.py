#!/usr/bin/env python3
"""Read-only paired prompt test on exactly the same four evidence chunks for Q3/Q5."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import time
from benchmark_rag_v5_prompt_ab import BASELINE, chat

TARGETED = (
    "Sei DRIBBLING, analista tattico calcistico. Usa soltanto gli estratti numerati. "
    "Rispondi precisamente alla domanda posta, non a una domanda simile. "
    "Distingui esplicitamente le condizioni tattiche che cambiano la validita' di un principio: "
    "non attribuire alla difesa bassa i vantaggi della profondita' contro una difesa alta. "
    "Se la domanda riguarda la VARIAZIONE del sistema DURANTE una partita, distingui "
    "le conseguenze documentate del cambio dalle proprieta' statiche dei singoli sistemi. "
    "Non dedurre automaticamente le prime dalle seconde. "
    "Se le fonti non documentano gli effetti del cambio, dichiaralo chiaramente e "
    "presenta eventuali caratteristiche dei sistemi soltanto come contesto, non come prova. "
    "Se due estratti sembrano contraddirsi, esplicita le rispettive condizioni; "
    "non affermare due regole incompatibili per la stessa situazione. "
    "Non inventare elementi mancanti. Cita ogni affermazione tattica con [F1], [F2], ecc., "
    "utilizzando esclusivamente gli identificatori forniti. "
    "Rispondi in italiano con risposta diretta e limiti delle evidenze, senza prolissita'."
)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--timeout", type=int, default=900)
    args = p.parse_args()
    original = json.loads(args.input.read_text(encoding="utf-8"))
    if original.get("collection") != "dribbling_tactics_v5_multisource" or not original.get("index_unchanged"):
        raise RuntimeError("Input must be the validated read-only V5 benchmark")
    questions = {q["id"]: q for q in original["questions"]}
    if not {"q3", "q5"}.issubset(questions):
        raise RuntimeError("Missing q3/q5 in input")
    report = {
        "method": "Same question, evidence, model and Ollama options; baseline vs targeted prompt",
        "source_benchmark": str(args.input),
        "model": args.model,
        "prompts": {"baseline": BASELINE, "targeted": TARGETED},
        "questions": [],
        "limitations": ["Prompt-only experiment; no automatic factual correctness certification.",
                        "Input evidence is reused unchanged; Chroma is not accessed or modified."]
    }
    def save():
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    try:
        for qid in ("q3", "q5"):
            source = questions[qid]
            prior = source["variants"]["dedup_gated"]
            evidence = prior["evidence"]
            if len(evidence) != 4:
                raise RuntimeError(f"{qid}: expected 4 evidence chunks, got {len(evidence)}")
            entry = {"id": qid, "question": source["question"], "evidence": evidence, "variants": {}}
            report["questions"].append(entry)
            # Reuse the already measured baseline answer to avoid redundant CPU generation.
            entry["variants"]["baseline"] = {
                "answer": prior["answer"], "citation_ids": prior["citation_ids"],
                "invalid_citation_ids": prior["invalid_citation_ids"],
                "elapsed_seconds": prior["elapsed_seconds"],
                "generation": prior["generation"], "reused_from_input": True}
            save()
            print("START", qid, "targeted", flush=True)
            started = time.monotonic()
            answer, stats = chat(args.model, TARGETED, source["question"], evidence, args.timeout)
            citations = sorted({int(x) for x in re.findall(r"\[F(\d+)\]", answer)})
            entry["variants"]["targeted"] = {
                "answer": answer, "citation_ids": citations,
                "invalid_citation_ids": [x for x in citations if not 1 <= x <= len(evidence)],
                "elapsed_seconds": round(time.monotonic()-started, 2),
                "generation": stats, "reused_from_input": False}
            save()
            print("DONE", qid, entry["variants"]["targeted"]["elapsed_seconds"], flush=True)
    except (Exception, KeyboardInterrupt) as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        save()
        raise
    print("PASS: read-only targeted prompt test completed", flush=True)

if __name__ == "__main__":
    main()
