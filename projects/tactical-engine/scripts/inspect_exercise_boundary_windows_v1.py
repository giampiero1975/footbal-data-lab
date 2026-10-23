#!/usr/bin/env python3
"""Inspect four selected Docling text ranges without modifying inputs."""
import argparse
import json
from pathlib import Path

WINDOWS = (
    ("Allegati_2832014181753.json", 465, 472),
    ("Allegati_2832014181753.json", 442, 462),
    ("smarcamento_marcamento.json", 108, 124),
    ("la_punta_centrale_Gritti.json", 286, 292),
)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    if a.output.exists():
        ap.error("Output exists")
    rows = []
    for source, first, last in WINDOWS:
        texts = json.loads((a.root / source).read_text(encoding="utf-8"))["texts"]
        if len(texts) <= last:
            ap.error("Source shorter than expected")
        items = []
        for i in range(first, last + 1):
            element = texts[i]
            value = " ".join(str(element.get("text") or "").split())
            pages = sorted({p["page_no"] for p in element.get("prov", [])
                            if isinstance(p, dict) and isinstance(p.get("page_no"), int)})
            items.append({"ref": element.get("self_ref") or f"#/texts/{i}",
                          "label": element.get("label"), "pages": pages,
                          "length": len(value), "excerpt": value[:160]})
        rows.append({"source": source, "range": [first, last],
                     "items": items, "decision": "review_required"})
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("x", encoding="utf-8") as f:
        json.dump({"schema": "exercise-boundary-windows-v1", "windows": rows},
                  f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"WINDOWS={len(rows)} REPORT={a.output}")

if __name__ == "__main__":
    main()
