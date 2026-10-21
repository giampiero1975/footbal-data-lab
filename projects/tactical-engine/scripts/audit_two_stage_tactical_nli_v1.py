#!/usr/bin/env python3
"""Deterministic audit of two-stage tactical NLI outputs; never changes predictions.

Reads saved benchmark JSON. Reports quote states and suspicious verdict/rationale
inconsistencies for manual review. Heuristics are diagnostic, not an NLI oracle.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

CONTRADICTION_CUES = (
    "in diretta contraddizione", "contraddice direttamente",
    "sono in contraddizione diretta", "sono concetti opposti",
    "due proposizioni incompatibili", "incompatibili nel contesto",
    "affermazione è contraddetta", "contraddizione diretta",
)
SUPPORT_CUES = (
    "supporta pienamente", "pienamente supportata",
    "supporta direttamente", "conferma esplicitamente",
    "conferma direttamente", "fonte supporta l'affermazione",
)

def quote_status(quote: str, evidence: str) -> str:
    if not quote or not quote.strip():
        return "absent"
    if quote in evidence:
        return "exact"
    return "nonliteral"

def audit(report: dict) -> dict:
    evidence = {x["id"]: x["evidence"] for x in report["input_signature"]}
    rows = []
    totals = {"absent": 0, "exact": 0, "nonliteral": 0}
    for row in report["results"]:
        if "prediction" not in row:
            continue
        flags = []
        citations = {}
        for stage in ("support", "contradiction"):
            if stage not in row:
                continue
            judgment = row[stage]
            quote = judgment.get("evidence_quote", "")
            status = quote_status(quote, evidence[row["id"]])
            totals[status] += 1
            citations[stage] = status
            rationale = judgment.get("rationale", "").casefold()
            if stage == "contradiction" and not judgment.get("yes") and any(cue in rationale for cue in CONTRADICTION_CUES):
                flags.append("contradiction_no_but_rationale_states_direct_contradiction")
            if stage == "support" and not judgment.get("yes") and any(cue in rationale for cue in SUPPORT_CUES):
                flags.append("support_no_but_rationale_states_support")
            if status == "nonliteral":
                flags.append(stage + "_nonliteral_quote")
        if flags or any(s == "nonliteral" for s in citations.values()):
            rows.append({"id": row["id"], "gold": row["gold"],
                         "prediction": row["prediction"], "flags": sorted(set(flags)),
                         "citation_status": citations})
    return {"test": "two_stage_deterministic_audit_v1",
            "source_test": report.get("test"),
            "total_predictions": sum("prediction" in r for r in report["results"]),
            "citation_status_counts": totals,
            "flagged_cases": rows,
            "flagged_count": len(rows),
            "limitations": [
                "Cue-based flags may produce false positives and false negatives.",
                "No automatic relabeling; audit flags are not ground truth.",
                "Absent quotes are not counted as fabricated quotations.",
                "Exact substring matching is case-sensitive and does not verify semantic relevance.",
            ]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    if a.input.resolve() == a.output.resolve():
        p.error("Input and output must differ")
    result = audit(json.loads(a.input.read_text(encoding="utf-8")))
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("REPORT", a.output)

if __name__ == "__main__":
    main()
