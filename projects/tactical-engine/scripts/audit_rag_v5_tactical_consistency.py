#!/usr/bin/env python3
"""Offline regression checks for two known V5 tactical failure modes.

Rules are narrow, explicitly scoped to Q3/Q5; this is NOT a general
entailment/faithfulness judge. Never promotes a response as factually verified.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

def normalize(s):
    return re.sub(r"\s+", " ", s.casefold())

def sentences(s):
    return re.split(r"(?<=[.!?])\s+|\n+", s)

def check(qid, answer, evidence):
    a = normalize(answer)
    findings = []
    citation_ids = sorted({int(x) for x in re.findall(r"\[F(\d+)\]", answer)})
    invalid = [x for x in citation_ids if not 1 <= x <= len(evidence)]
    if invalid:
        findings.append({"severity": "contraddittoria", "code": "INVALID_CITATIONS",
                         "detail": f"Invalid citation IDs: {invalid}"})
    if not citation_ids:
        findings.append({"severity": "da_verificare", "code": "NO_CITATIONS",
                         "detail": "No citations found"})
    if qid == "q3":
        # Check the documented distinction, not mere mention of low defenses.
        for line in sentences(a):
            low = bool(re.search(r"difes[ae] bass[ae]|difendono bass[ae]|rintanat[oi]|pressi dell.area di rigore", line))
            vertical = bool(re.search(r"verticalizz|profondit", line))
            positive = bool(re.search(r"indicata|favorit[ao]|preferibil|privileg|efficace|sfruttament", line))
            negated = bool(re.search(r"non (?:è |e |sono )?(?:indicata|favorita|preferibile|efficace)|difficile|sconsigliat|non è favorita", line))
            if low and vertical and positive and not negated:
                findings.append({"severity": "contraddittoria", "code": "Q3_LOW_BLOCK_VERTICAL",
                                 "detail": "Possible unsupported positive association of depth with a low block",
                                 "excerpt": line[:400]})
        if not re.search(r"difes[ae] bass[ae]|difendono bass[ae]|rintanat[oi]", a):
            findings.append({"severity": "da_verificare", "code": "Q3_MISSING_LOW_BLOCK",
                             "detail": "Low-block limitation not discussed"})
    elif qid == "q5":
        limitation = bool(re.search(r"non (?:documentano|esistono evidenze|è possibile dedurre|e possibile dedurre)|non necessariamente come conseguenza", a))
        static_distinction = bool(re.search(r"static[oihe]|intrinsec[oihe]|singoli sistemi|caratteristiche.*sistemi", a))
        if not (limitation and static_distinction):
            findings.append({"severity": "da_verificare", "code": "Q5_CHANGE_VS_STATIC",
                             "detail": "Insufficient explicit separation of in-game changes from static system properties"})
        if re.search(r"variar(?:e|ando) il sistema comporta", a) and not limitation:
            findings.append({"severity": "contraddittoria", "code": "Q5_UNSUPPORTED_CHANGE_EFFECT",
                             "detail": "Presents system properties as demonstrated effects of changing systems"})
    status = ("contraddittoria" if any(f["severity"] == "contraddittoria" for f in findings)
              else "da_verificare")
    return {"status": status, "findings": findings, "citation_ids": citation_ids,
            "note": "Rule-based screening only; no response is certified as factually conforming."}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    src = json.loads(args.input.read_text(encoding="utf-8"))
    questions = src.get("questions", [])
    if {q["id"] for q in questions} != {"q3", "q5"}:
        raise RuntimeError("Expected exactly Q3 and Q5 in concise prompt report")
    report = {"method": "Offline rule-based screening of known Q3/Q5 failures",
              "scope": "Regression heuristics, not a general faithfulness metric",
              "questions": []}
    for q in questions:
        row = {"id": q["id"], "variants": {}}
        for name, v in q["variants"].items():
            row["variants"][name] = check(q["id"], v["answer"], q["evidence"])
        report["questions"].append(row)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    for q in report["questions"]:
        for name, result in q["variants"].items():
            print(q["id"], name, result["status"], ",".join(f["code"] for f in result["findings"]) or "no_flags")
    print("DONE: heuristic screening; manual source verification still required")

if __name__ == "__main__":
    main()
