#!/usr/bin/env python3
"""Read-only body sampling for a fixed Docling heading report."""
import argparse
import json
from pathlib import Path

SOURCES = ("smarcamento_marcamento.json", "la_punta_centrale_Gritti.json", "Allegati_2832014181753.json")

def summary(item, index):
    pages = sorted({p["page_no"] for p in item.get("prov", []) if isinstance(p, dict) and isinstance(p.get("page_no"), int)})
    value = " ".join(str(item.get("text") or "").split())
    return {"ref": item.get("self_ref") or f"#/texts/{index}", "label": item.get("label"),
            "pages": pages, "length": len(value), "excerpt": value[:100]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--headings", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    a = ap.parse_args()
    if a.output.exists():
        ap.error("Output exists")
    known = json.loads(a.headings.read_text(encoding="utf-8"))
    if known.get("schema") != "exercise-heading-context-v1" or known.get("candidate_count") != 22:
        ap.error("Unexpected heading report")
    if set(known.get("sources", [])) != set(SOURCES):
        ap.error("Unexpected sources")
    result = []
    for source in SOURCES:
        texts = json.loads((a.root / source).read_text(encoding="utf-8"))["texts"]
        refs = [row["candidate"]["ref"] for row in known["items"] if row["source"] == source]
        for ref in refs:
            prefix = "#/texts/"
            if not ref.startswith(prefix) or not ref[len(prefix):].isdigit():
                ap.error("Invalid Docling reference")
            start = int(ref[len(prefix):])
            if start >= len(texts) or texts[start].get("label") not in ("title", "section_header"):
                ap.error("Invalid heading item")
            stop = next((i for i in range(start + 1, len(texts))
                         if texts[i].get("label") in ("title", "section_header")), len(texts))
            indices = [i for i in range(start + 1, stop) if texts[i].get("text")]
            sample = sorted(set(indices[:2] + indices[-2:]))
            result.append({"source": source, "heading": summary(texts[start], start),
                           "next_heading_ref": f"#/texts/{stop}" if stop < len(texts) else None,
                           "intermediate_count": len(indices),
                           "samples": [summary(texts[i], i) for i in sample],
                           "decision": "review_required"})
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps({"schema": "exercise-body-context-v1", "count": len(result),
                                    "items": result}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"INSPECTED={len(result)} REPORT={a.output}")

if __name__ == "__main__":
    main()
