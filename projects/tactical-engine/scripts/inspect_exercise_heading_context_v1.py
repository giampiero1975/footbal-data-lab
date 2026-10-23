#!/usr/bin/env python3
"""Read-only inspection of heading context for three selected Docling sources."""
import argparse
import json
import re
from pathlib import Path

SOURCES = ("smarcamento_marcamento.json", "la_punta_centrale_Gritti.json", "Allegati_2832014181753.json")
PATTERN = re.compile(r"^(?:esercitazion\w*|esercizi?\b|situazion\w*\b)", re.I)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists")
    rows = []
    for filename in SOURCES:
        file = args.root / filename
        if not file.is_file():
            parser.error(f"Missing source: {file}")
        doc = json.loads(file.read_text(encoding="utf-8"))
        headings = []
        for idx, element in enumerate(doc.get("texts", [])):
            if not isinstance(element, dict):
                continue
            if element.get("label") not in ("title", "section_header"):
                continue
            value = str(element.get("text") or "").strip()
            if not value:
                continue
            pages = sorted({p["page_no"] for p in element.get("prov", []) if isinstance(p, dict) and isinstance(p.get("page_no"), int)})
            headings.append({"text": value, "label": element["label"], "ref": element.get("self_ref") or f"#/texts/{idx}", "pages": pages})
        for idx, heading in enumerate(headings):
            if not PATTERN.match(heading["text"]):
                continue
            rows.append({"source": filename, "candidate": heading, "previous_headings": headings[max(0, idx-2):idx], "next_headings": headings[idx+1:idx+3], "decision": "review_required"})
    result = {"schema": "exercise-heading-context-v1", "sources": list(SOURCES), "candidate_count": len(rows), "items": rows, "note": "Heading-only inspection. No extraction validation."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CANDIDATES={len(rows)} REPORT={args.output}")

if __name__ == "__main__":
    main()
