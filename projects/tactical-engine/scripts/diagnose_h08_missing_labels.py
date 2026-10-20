#!/usr/bin/env python3
"""H08 diagnostic: inspect missing figure labels in original Docling text, without assigning labels."""
import argparse
import json
import re
from pathlib import Path

PATTERN = re.compile(r"(?i)\b(?:fig(?:ura|ure|g)?\.?|schema|diagramma)\s*(?:n\.?\s*)?(15\s*[/.-]\s*a|15\s*[/.-]\s*b|17)\b")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--docling-json", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    args = p.parse_args()
    doc = json.loads(args.docling_json.read_text(encoding="utf-8"))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    texts = doc.get("texts", [])
    for page in (9, 10):
        print("PAGE", page)
        for pic in manifest:
            if pic.get("page") == page:
                print("FIGURE", pic.get("figure_index"), "ref", pic.get("self_ref"),
                      "captions", pic.get("captions"), "bbox", pic.get("bbox"))
        for t in texts:
            prov = t.get("prov") or []
            if not any(x.get("page_no") == page for x in prov if isinstance(x, dict)):
                continue
            value = t.get("text") or ""
            if PATTERN.search(value) or t.get("label") == "caption":
                print("TEXT", t.get("self_ref"), "label", t.get("label"),
                      "text", value[:500], "prov", prov[:1])

if __name__ == "__main__":
    main()
