#!/usr/bin/env python3
"""Offline regression checks for Glerean 3-3-4 answer texts.

This is a conservative lint: flags specific documented contradictions; it does
not claim to certify football tactics or replace human source review.
"""
import argparse
import json
import re
from pathlib import Path

ROLE_ERRORS = [
    ("wide_forwards_mislabeled_midfielders",
     re.compile(r"centrocampist[iaei]+\\s+estern[iaei]+[^.\\n]{0,65}?(?:n\\.?\\s*7|n\\.?\\s*11)", re.I)),
    ("midfield_run_behind_defenders",
     re.compile(r"(?:n\\.?\\s*6|n\\.?\\s*8)[^.\\n]{0,130}?(?:dietro le spalle|alle spalle)[^.\\n]{0,55}?difensor", re.I)),
]
# Source citations must have stable identifiers; figure references use Fig. N.
NUMERIC_BRACKET = re.compile(r"\\[(?:\\d+)(?:\\s*,\\s*\\d+)*\\]")
STABLE_REF = re.compile(r"\\[GLEREAN-C\\d{3}(?:\\s*,\\s*(?:GLEREAN-C)?\\d{3})*\\]")

def lint(answer, mode):
    findings = []
    for code, pattern in ROLE_ERRORS:
        if pattern.search(answer):
            findings.append(code)
    if mode == "numeric" and NUMERIC_BRACKET.search(answer):
        findings.append("numeric_bracket_citation_requires_migration")
    if mode == "stable" and not re.search(r"\\[GLEREAN-C\\d{3}", answer):
        findings.append("missing_stable_source_citation")
    return findings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    runs = report.get("runs", [])
    if not runs:
        raise SystemExit("No runs")
    for run in runs:
        findings = lint(run["answer_raw"], run["mode"])
        print(f'{run["model"]} {run["case_id"]} {run["mode"]}: '
              + (", ".join(findings) if findings else "no lint findings"))
    print(f"Checked {len(runs)} responses. This lint does not score semantic correctness.")

if __name__ == "__main__":
    main()
