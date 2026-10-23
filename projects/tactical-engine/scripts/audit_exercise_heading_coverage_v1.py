#!/usr/bin/env python3
"""Read-only inventory of Docling exercise heading conventions; no extraction benchmark."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

PATTERNS = {
    "v2_compatible": re.compile(r"^(?:Esercitazione|Esecitazione)\s+\d+(?:\s*/\s*[A-Za-z])?\s*$", re.I),
    "exercise_other": re.compile(r"^(?:Esercitazion\w*|Esercizi?\b|Situazion\w*\b|Propost\w*\b|Allenament\w*\b)", re.I),
}
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if not args.root.is_dir():
        ap.error("root must be a directory")
    docs = []
    for path in sorted(args.root.rglob("*.json")):
        if path.name.endswith(".meta.json") or path.name == "images.json":
            continue
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if not isinstance(obj, dict) or not isinstance(obj.get("texts"), list):
            continue
        headings = [(str(t.get("text") or "").strip(), t.get("label", ""))
                    for t in obj["texts"] if isinstance(t, dict)]
        heads = [v for v, label in headings if label in ("section_header", "title") and v]
        exact = [v for v in heads if PATTERNS["v2_compatible"].fullmatch(v)]
        other = [v for v in heads if PATTERNS["exercise_other"].match(v)
                 and not PATTERNS["v2_compatible"].fullmatch(v)]
        docs.append({"source": str(path.relative_to(args.root)), "headings": len(heads),
                     "v2_compatible": len(exact), "other_exercise_like": len(other),
                     "other_examples": other[:8]})
    report = {"schema": "exercise-heading-coverage-v1", "documents": len(docs),
              "with_v2_headings": sum(bool(d["v2_compatible"]) for d in docs),
              "with_other_exercise_headings": sum(bool(d["other_exercise_like"]) for d in docs),
              "items": docs}
    if args.output.exists():
        ap.error("output already exists; refusing to overwrite")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"DOCUMENTS={len(docs)} V2_HEADING_DOCS={report['with_v2_headings']} REPORT={args.output}")

if __name__ == "__main__":
    main()
