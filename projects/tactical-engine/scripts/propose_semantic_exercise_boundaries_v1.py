#!/usr/bin/env python3
"""Offline semantic boundary proposals from the existing four-window report."""
import argparse
import json
import re
from pathlib import Path

NUMBERED = re.compile(r"^Esercitazione\s+(?:n\.\s*)?\d+\b", re.I)
DESCRIPTIVE = re.compile(r"^Esercitazione\s+per\b", re.I)
COLLECTIVE = re.compile(r"^Esercitazioni\b", re.I)
SUBSECTIONS = {"descrizione", "regole e scopo del gioco"}

def classify(item, previous):
    title = item["excerpt"].strip()
    norm = title.casefold()
    if norm in SUBSECTIONS:
        return "section_boundary", "subsection_title"
    if COLLECTIVE.search(title):
        return "section_boundary", "collective_heading"
    if NUMBERED.search(title):
        return "exercise_start", "numbered_title"
    if DESCRIPTIVE.search(title):
        return "exercise_start", "descriptive_title"
    if norm == "partita 11vs11 a tre settori" and previous and previous["excerpt"].strip().casefold() == "esercitazione 16":
        return "review_required", "subtitle_after_numbered_title"
    return "non_exercise", "no_heading_signal"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    if args.output.exists():
        ap.error("Output exists")
    source = json.loads(args.input.read_text(encoding="utf-8"))
    if source.get("schema") != "exercise-boundary-windows-v1" or len(source.get("windows", [])) != 4:
        ap.error("Unexpected input report")
    output = []
    for window in source["windows"]:
        items = window["items"]
        for i, item in enumerate(items):
            kind, reason = classify(item, items[i-1] if i else None)
            if kind == "non_exercise":
                continue
            if window["source"] == "smarcamento_marcamento.json" and NUMBERED.search(item["excerpt"]):
                kind, reason = "review_required", "repeated_numbered_title"
            output.append({"source": window["source"], "ref": item["ref"],
                           "label": item["label"], "pages": item["pages"],
                           "title_excerpt": item["excerpt"], "candidate_type": kind,
                           "reason": reason, "decision": "review_required"})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as f:
        json.dump({"schema": "exercise-semantic-boundary-proposals-v1",
                   "candidates": output, "count": len(output),
                   "note": "Proposals only, not validated boundaries."},
                  f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"CANDIDATES={len(output)} REPORT={args.output}")

if __name__ == "__main__":
    main()
