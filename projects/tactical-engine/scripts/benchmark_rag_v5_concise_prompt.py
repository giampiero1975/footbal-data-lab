#!/usr/bin/env python3
"""Read-only V5 concise prompt regression using unchanged Q3/Q5 evidence.

Does not access or mutate Chroma. Existing baseline and targeted generations
are reused from their reports; only the concise variant calls Ollama.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import time
from benchmark_rag_v5_prompt_ab import BASELINE, chat

CONCISE = (
    "Sei DRIBBLING, analista tattico calcistico. Rispondi soltanto alla domanda "
    "e soltanto con le fonti numerate. Per ogni conclusione conserva le condizioni "
    "in cui la fonte la ritiene valida; non unire alternative riferite a situazioni "
    "diverse. Distingui cio' che le fonti dimostrano da cio' che non dimostrano: "
    "non trasformare caratteristiche di un sistema in conseguenze di un cambiamento. "
    "Se manca la prova necessaria, dichiaralo senza inventare. "
    "Prima di concludere verifica che le affermazioni non si contraddicano e "
    "che ciascuna sia sostenuta dalla citazione [F1], [F2], ecc. "
    "Rispondi in italiano, in modo sintetico e pertinente."
)

def citation_ids(answer):
    return sorted({int(n) for n in re.findall(r"\[F(\d+)\]", answer)})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--targeted", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()

    base = json.loads(args.baseline.read_text(encoding="utf-8"))
    targeted = json.loads(args.targeted.read_text(encoding="utf-8"))
    if base.get("collection") != "dribbling_tactics_v5_multisource" or not base.get("index_unchanged"):
        raise RuntimeError("Baseline report not validated for V5")
    if targeted.get("model") != args.model or base.get("model") != args.model:
        raise RuntimeError("Model mismatch across reports")
    base_by_id = {q["id"]: q for q in base["questions"]}
    targeted_by_id = {q["id"]: q for q in targeted["questions"]}
    report = {
        "method": "Same Q3/Q5 questions and four evidence chunks; concise prompt vs prior baseline/targeted",
        "model": args.model,
        "prompts": {"baseline": BASELINE, "concise": CONCISE,
                    "targeted": targeted["prompts"]["targeted"]},
        "questions": [],
        "limitations": [
            "Automatic citation checks validate syntax, not factual faithfulness.",
            "Qualitative source-based review is required before promotion.",
            "No Chroma access or mutation; baseline and targeted generations are reused."
        ]
    }
    def save():
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    try:
        for qid in ("q3", "q5"):
            original = base_by_id[qid]
            prior = targeted_by_id[qid]
            evidence = original["variants"]["dedup_gated"]["evidence"]
            if len(evidence) != 4 or [r["id"] for r in evidence] != [r["id"] for r in prior["evidence"]]:
                raise RuntimeError(f"{qid}: evidence mismatch between reports")
            entry = {"id": qid, "question": original["question"], "evidence": evidence,
                     "variants": {
                         "baseline": {**prior["variants"]["baseline"], "reused_from_input": True},
                         "targeted": {**prior["variants"]["targeted"], "reused_from_input": True}
                     }}
            report["questions"].append(entry)
            save()
            print("START", qid, "concise", flush=True)
            start = time.monotonic()
            answer, stats = chat(args.model, CONCISE, original["question"], evidence, args.timeout)
            cited = citation_ids(answer)
            entry["variants"]["concise"] = {
                "answer": answer,
                "citation_ids": cited,
                "invalid_citation_ids": [n for n in cited if n < 1 or n > len(evidence)],
                "elapsed_seconds": round(time.monotonic() - start, 2),
                "generation": stats,
                "reused_from_input": False
            }
            save()
            print("DONE", qid, "concise", entry["variants"]["concise"]["elapsed_seconds"], flush=True)
    except (Exception, KeyboardInterrupt) as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        save()
        raise
    print("PASS: read-only concise prompt comparison completed", flush=True)

if __name__ == "__main__":
    main()
