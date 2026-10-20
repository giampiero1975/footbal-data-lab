#!/usr/bin/env python3
"""Read-only figure candidates from existing Docling manifests and source page metadata."""
import argparse
import json
from pathlib import Path

ROOT = Path("/opt/football-data-lab/knowledge/processed")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="formations-and-systems/334_principi_Glerean.pdf")
    p.add_argument("--page-from", type=int, default=7)
    p.add_argument("--page-to", type=int, default=13)
    args = p.parse_args()
    source = Path(args.source)
    if source.is_absolute() or ".." in source.parts or source.suffix.lower() != ".pdf":
        p.error("Expected relative PDF source")
    base = ROOT / source.parent / source.stem
    manifest = base.parent / (base.name + "_images") / "images.json"
    items = json.loads(manifest.read_text(encoding="utf-8"))
    rows = []
    for item in items:
        page = item.get("page")
        if not isinstance(page, int) or not args.page_from <= page <= args.page_to:
            continue
        bbox = item.get("bbox", {})
        width = abs(float(bbox.get("r", 0)) - float(bbox.get("l", 0)))
        height = abs(float(bbox.get("t", 0)) - float(bbox.get("b", 0)))
        rows.append({"figure_index": item.get("figure_index"), "page": page,
                     "image": item.get("file"), "width_pt": round(width, 1),
                     "height_pt": round(height, 1), "caption_refs": item.get("captions", [])})
    print(json.dumps({"source": args.source, "page_range": [args.page_from, args.page_to],
                      "candidates": rows}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
