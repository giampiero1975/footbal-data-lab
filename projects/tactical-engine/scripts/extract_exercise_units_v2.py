#!/usr/bin/env python3
"""Offline Docling exercise extractor with stronger section boundaries."""
import argparse
import hashlib
import json
import re
from pathlib import Path

HEADING = re.compile(r"^(?:Esercitazione|Esecitazione)\s+(\d+(?:\s*/\s*[A-Za-z])?)\s*$", re.I)
STOP = {"INDICE", "SOMMARIO", "BIBLIOGRAFIA", "CONCLUSIONI",
        "L\'ALLENAMENTO ATTRAVERSO LA PSICOCINETICA", "IL PORTIERE NELLE TRANSIZIONI"}

def extract(doc, source):
    units = []
    current = None
    for index, item in enumerate(doc.get("texts", [])):
        value = (item.get("text") or "").strip()
        if not value or item.get("content_layer") == "furniture":
            continue
        label = item.get("label", "")
        is_heading = label in ("section_header", "title")
        match = HEADING.fullmatch(value) if is_heading else None
        if is_heading and (match or value.upper() in STOP):
            if current is not None:
                units.append(current)
                current = None
            if match:
                ref = item.get("self_ref") or f"#/texts/{index}"
                current = {"exercise_id": re.sub(r"\s+", "", match.group(1)).upper(),
                           "title": value, "source": source, "heading_ref": ref,
                           "pages": [], "doc_item_refs": [], "parts": []}
        if current is None:
            continue
        pages = {p["page_no"] for p in item.get("prov", [])
                 if isinstance(p.get("page_no"), int)}
        current["pages"] = sorted(set(current["pages"]) | pages)
        current["doc_item_refs"].append(item.get("self_ref") or f"#/texts/{index}")
        current["parts"].append(value)
    if current is not None:
        units.append(current)
    for unit in units:
        unit["text"] = "\n".join(unit.pop("parts"))
        key = "|".join(("exercise-v2", source, unit["heading_ref"], unit["text"]))
        unit["id"] = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return units

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input and output must differ")
    doc = json.loads(args.input.read_text(encoding="utf-8"))
    units = extract(doc, args.input.name)
    result = {"schema": "exercise-units-v2", "count": len(units), "units": units}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"UNITS={len(units)} REPORT={args.output}")

if __name__ == "__main__":
    main()
