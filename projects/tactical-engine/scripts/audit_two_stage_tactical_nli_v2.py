#!/usr/bin/env python3
"""Read-only structural and conservative rationale audit of two-stage NLI reports.

Flags are diagnostic, never alter judgments. Negation scope is deliberately
conservative: uncertain linguistic constructions remain unflagged.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

POSITIVE = re.compile(r"\b(?:in diretta contraddizione|sono in (?:diretta )?contraddizione|sono concetti opposti|sono (?:direttamente )?incompatibili|contraddice direttamente|contraddicono direttamente|in contrasto con|contraddizione diretta)\b", re.I)
NEGATED = re.compile(r"\b(?:non|nessuna|alcuna|manca|senza|assenza|non c['’]è|non vi è)\b", re.I)


def quote_status(value, evidence):
    if not isinstance(value, str):
        return "invalid_type"
    if not value.strip():
        return "absent"
    return "exact" if value in evidence else "nonliteral"


def positive_contradiction(rationale):
    """Return positive contradiction cues excluding nearby clause negation."""
    hits = []
    for match in POSITIVE.finditer(rationale):
        left = rationale[max(0, match.start()-75):match.start()]
        clause = re.split(r"[.;:!?\n]", left)[-1]
        if NEGATED.search(clause):
            continue
        hits.append(match.group(0))
    return hits


def audit(report):
    evidence = {item["id"]: item["evidence"] for item in report["input_signature"]}
    counts = {"absent": 0, "exact": 0, "nonliteral": 0, "invalid_type": 0}
    flagged = []
    for row in report["results"]:
        if "prediction" not in row:
            continue
        flags, citations, matches = [], {}, {}
        for stage in ("support", "contradiction"):
            if stage not in row:
                continue
            judgment = row[stage]
            status = quote_status(judgment.get("evidence_quote"), evidence[row["id"]])
            citations[stage] = status
            counts[status] += 1
            if status in ("nonliteral", "invalid_type"):
                flags.append(stage + "_quote_" + status)
            if not isinstance(judgment.get("yes"), bool):
                flags.append(stage + "_invalid_yes_type")
            if not isinstance(judgment.get("rationale"), str):
                flags.append(stage + "_invalid_rationale_type")
            if stage == "contradiction" and judgment.get("yes") is False and isinstance(judgment.get("rationale"), str):
                hits = positive_contradiction(judgment["rationale"])
                if hits:
                    flags.append("contradiction_false_with_positive_rationale_cue")
                    matches[stage] = hits
        if flags:
            flagged.append({"id": row["id"], "gold": row["gold"], "prediction": row["prediction"],
                            "flags": flags, "citation_status": citations, "matched_cues": matches})
    return {"test": "two_stage_deterministic_audit_v2", "source_test": report.get("test"),
            "total_predictions": sum("prediction" in r for r in report["results"]),
            "citation_status_counts": counts, "flagged_cases": flagged,
            "flagged_count": len(flagged),
            "limitations": ["Heuristic cues are not semantic proof; manual review required.",
                            "Conservative clause negation may miss genuine inconsistencies.",
                            "No relabeling or mutation of input benchmark.",
                            "Absent citations are distinct from nonliteral quotations."]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input and output must differ")
    result = audit(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("REPORT", args.output)


if __name__ == "__main__":
    main()
