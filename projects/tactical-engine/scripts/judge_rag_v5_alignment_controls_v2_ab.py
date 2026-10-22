#!/usr/bin/env python3
"""Shadow V2 comparison, preserving V1 evaluator and input reports."""
import argparse
import json
from pathlib import Path
import judge_rag_v5_alignment_controls_v1 as judge

judge.PROMPTS["nli"] = (
    "Evaluate whether EVIDENCE entails the full CLAIM. "
    "Compare quantifiers and domain scope: three specific systems cannot prove a claim about all systems. "
    "supported requires every clause and quantifier; contradicted requires explicit opposite; otherwise insufficient. "
    "Return JSON with label and reason."
)
judge.PROMPTS["alignment"] = (
    "Decide whether CLAIM directly answers QUESTION. "
    "When asked about changing formations during a match, distinguish consequences of the switch "
    "from static properties of a formation and from changing passing lanes during an action. "
    "Never infer an unmentioned formation switch. "
    "direct means a direct answer; contextual means relevant background; off_target means another event. "
    "Return JSON with label and reason."
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        parser.error("--execute required")
    if len({args.input.resolve(), args.baseline.resolve(), args.output.resolve()}) != 3:
        parser.error("Paths must differ")
    controls = json.loads(args.input.read_text(encoding="utf-8"))
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    if controls.get("schema") != "rag_v5_alignment_controls_v1":
        parser.error("Invalid controls schema")
    if baseline.get("schema") != "rag_v5_alignment_judge_shadow_v1":
        parser.error("Invalid baseline schema")
    old = {row["id"]: row for row in baseline["results"]}
    if len(controls["controls"]) != 10 or set(old) != {r["id"] for r in controls["controls"]}:
        parser.error("Controls and baseline mismatch")
    results = []
    for index, row in enumerate(controls["controls"], 1):
        result = {"id": row["id"], "category": row["category"],
                  "expected_provisional": row["expected"],
                  "baseline_predicted": old[row["id"]]["predicted"]}
        try:
            verdict, elapsed = judge.evaluate(row, "http://127.0.0.1:11434", args.model, args.timeout)
            result.update(predicted=verdict["label"], reason=verdict["reason"],
                          elapsed_seconds=elapsed, error=None,
                          match_provisional=verdict["label"] == row["expected"])
        except Exception as exc:
            result.update(predicted=None, error=str(exc), match_provisional=None)
        results.append(result)
        print(f"{index}/10 {row['id']} baseline={result['baseline_predicted']} v2={result['predicted']}", flush=True)
    summary = {
        "attempted": len(results),
        "completed": sum(r["error"] is None for r in results),
        "errors": sum(r["error"] is not None for r in results),
        "baseline_matches_provisional": sum(r["baseline_predicted"] == r["expected_provisional"] for r in results),
        "v2_matches_provisional": sum(r["match_provisional"] is True for r in results),
        "changed_verdicts": sum(r["predicted"] is not None and r["predicted"] != r["baseline_predicted"] for r in results)
    }
    report = {"schema": "rag_v5_alignment_judge_shadow_v2_ab",
              "reference_status": "provisional_not_gold", "model": args.model,
              "summary": summary, "results": results}
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print("SHADOW V2:", summary, "REPORT:", args.output)

if __name__ == "__main__":
    main()
