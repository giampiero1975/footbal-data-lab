#!/usr/bin/env python3
"""Read-only repeated NLI diagnostic using frozen evidence and canonical V2 judge.

Ollama API contract: https://docs.ollama.com/api/chat
Structured outputs: https://docs.ollama.com/capabilities/structured-outputs
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

from benchmark_shadow_nli_contrastive_v1 import CASES
from shadow_nli_v2_inference import judge_pair, load_v2_instruction

IDS = ("low_width_preferred", "low_vertical_preferred", "low_vertical_difficult",
       "all_football_systems", "every_team_methodist", "no_other_system")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_baseline_20261022.json"))
    p.add_argument("--output", type=Path, default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_repeatability_v1_20261022.json"))
    p.add_argument("--execute", action="store_true")
    a = p.parse_args()
    if not a.execute:
        p.error("--execute required")
    if a.output.exists() or a.source.resolve() == a.output.resolve():
        p.error("Output exists or overlaps source; refusing overwrite")
    if not a.source.is_file():
        p.error(f"Baseline mancante: {a.source}; nessun benchmark avviato")
    if not a.output.parent.is_dir():
        p.error(f"Directory report mancante: {a.output.parent}; non viene creata automaticamente")
    data = json.loads(a.source.read_text(encoding="utf-8"))
    questions = {q["id"]: q for q in data["questions"]}
    selected = [c for c in CASES if c[2] in IDS]
    evidence = {}
    for qid, sid, *_ in selected:
        evidence[(qid, sid)] = next(e["text"] for e in questions[qid]["evidence"] if e["label"] == sid)
    results = []
    for repetition in (1, 2):
        for qid, sid, case_id, claim, expected, category in selected:
            started = time.monotonic()
            item = {"repeat": repetition, "id": case_id, "expected": expected,
                    "question_id": qid, "source_id": sid,
                    "evidence_chars": len(evidence[(qid, sid)]),
                    "evidence_sha256": hashlib.sha256(evidence[(qid, sid)].encode("utf-8")).hexdigest()}
            try:
                item["actual"] = judge_pair(claim, evidence[(qid, sid)])
                item["pass"] = item["actual"] == expected
            except Exception as exc:
                item["actual"] = None
                item["pass"] = False
                item["error"] = type(exc).__name__ + ": " + str(exc)[:300]
            item["elapsed_seconds"] = round(time.monotonic() - started, 3)
            results.append(item)
            print("REPEAT", repetition, case_id, item["actual"], "expected", expected, flush=True)
    by_case = {id_: [r["actual"] for r in results if r["id"] == id_] for id_ in IDS}
    report = {"schema": "shadow_nli_repeatability_v1", "mode": "shadow_only",
              "model": "qwen3.5:9b", "temperature": 0, "think": False,
              "num_ctx": 4096, "num_predict": 1024,
              "canonical_instruction_sha256": hashlib.sha256(load_v2_instruction().encode("utf-8")).hexdigest(),
              "attempted": len(results), "passed": sum(r["pass"] for r in results),
              "errors": sum("error" in r for r in results),
              "stable_cases": sum(len(set(v)) == 1 for v in by_case.values()),
              "total_cases": len(IDS), "case_outputs": by_case,
              "cases": results,
              "limitations": ["Two repetitions per claim cannot establish statistical stability",
                              "No production changes; frozen source evidence only"]}

    with a.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print("REPORT", a.output, "stable", report["stable_cases"], "/", report["total_cases"], "errors", report["errors"], flush=True)

if __name__ == "__main__":
    main()
