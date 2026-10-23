#!/usr/bin/env python3
"""Read-only exercise segmentation from ordered Docling JSON; no Chroma or LLM."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

HEADING = re.compile(r"^Esercitazione\s+(\d+(?:\s*/\s*[A-Za-z])?)\s*$", re.I)
INDEX = re.compile(r"^Esercitazione\s+\d+(?:\s*/\s*[A-Za-z])?\s*\.{3,}\s*\d+\s*$", re.I)
END_SECTIONS = {"indice", "sommario", "conclusioni", "bibliografia"}

def extract(doc: dict, source: str) -> list[dict]:
    units = []
    current = None
    for position, item in enumerate(doc.get("texts", [])):
        value = (item.get("text") or "").strip()
        label = item.get("label", "")
        if not value or item.get("content_layer") == "furniture" or INDEX.fullmatch(value):
            continue
        match = HEADING.fullmatch(value) if label in ("section_header", "title") else None
        if match:
            if current is not None:
                units.append(current)
            exercise_id = re.sub(r"\s+", "", match.group(1)).upper()
            current = {"exercise_id": exercise_id, "title": value, "source": source,
                       "parts": [], "pages": [], "doc_item_refs": []}
        elif label in ("section_header", "title") and value.casefold() in END_SECTIONS:
            if current is not None:
                units.append(current)
                current = None
            continue
        if current is None:
            continue
        pages = {p["page_no"] for p in item.get("prov", []) if isinstance(p.get("page_no"), int)}
        current["parts"].append(value)
        current["pages"] = sorted(set(current["pages"]) | pages)
        current["doc_item_refs"].append(item.get("self_ref") or f"#/texts/{position}")
    if current is not None:
        units.append(current)
    for unit in units:
        unit["text"] = "\n".join(unit.pop("parts"))
        key = "exercise-v1:" + source + ":" + unit["exercise_id"] + ":" + unit["text"]
        unit["id"] = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return units

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    if args.input.resolve() == args.output.resolve():
        ap.error("Output must differ from input")
    doc = json.loads(args.input.read_text(encoding="utf-8"))
    report = {"schema": "exercise-units-v1", "source": str(args.input),
              "units": extract(doc, args.input.name)}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OUTPUT=" + str(args.output))

if __name__ == "__main__":
    main()
