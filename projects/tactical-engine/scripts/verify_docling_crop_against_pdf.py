#!/usr/bin/env python3
"""Read-only crop localization: match an existing Docling PNG to its original PDF page.

Uses installed PyMuPDF/Pillow, performs no conversion, model call, or index write.
"""
import argparse
import json
from pathlib import Path

import fitz
from PIL import Image, ImageChops, ImageStat

ROOT = Path("/opt/football-data-lab")
PROCESSED = ROOT / "knowledge/processed"
SOURCES = ROOT / "knowledge/sources"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="formations-and-systems/334_principi_Glerean.pdf")
    p.add_argument("--figure-index", type=int, default=17)
    args = p.parse_args()
    rel = Path(args.source)
    if rel.is_absolute() or ".." in rel.parts or rel.suffix.lower() != ".pdf":
        p.error("Expected relative PDF source path")
    base = PROCESSED / rel.parent / rel.stem
    manifest = base.parent / (base.name + "_images") / "images.json"
    figures = json.loads(manifest.read_text(encoding="utf-8"))
    entry = next((x for x in figures if x.get("figure_index") == args.figure_index), None)
    if entry is None:
        p.error("Figure not found")
    filename = entry["file"]
    if Path(filename).name != filename:
        p.error("Unsafe image name")
    picture = Image.open(manifest.parent / filename).convert("RGB")
    doc = fitz.open(SOURCES / rel)
    page = doc[int(entry["page"]) - 1]
    bbox = entry["bbox"]
    l, t, rr, b = (float(bbox[k]) for k in ("l", "t", "r", "b"))
    if bbox.get("coord_origin", "BOTTOMLEFT") == "BOTTOMLEFT":
        bounds = fitz.Rect(l, page.rect.height - t, rr, page.rect.height - b)
    elif bbox.get("coord_origin") == "TOPLEFT":
        bounds = fitz.Rect(l, t, rr, b)
    else:
        p.error("Unsupported coordinate origin")
    bounds = bounds.normalize()
    if bounds.is_empty or bounds.is_infinite:
        p.error("Invalid bounding box")
    bounds = bounds & page.rect
    candidates = []
    for clip in (bounds,):
        pix = page.get_pixmap(clip=clip, matrix=fitz.Matrix(2, 2), alpha=False)
        rendered = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        target = picture.resize((256, 256))
        sample = rendered.resize((256, 256))
        diff = ImageChops.difference(target, sample)
        mean = sum(ImageStat.Stat(diff).mean) / 3
        candidates.append({"clip": list(clip), "mean_rgb_difference": round(mean, 2),
                           "pixel_dimensions_match": picture.size == rendered.size,
                           "exact_pixel_match": picture.size == rendered.size and ImageChops.difference(picture, rendered).getbbox() is None})
    print(json.dumps({"source": args.source, "figure_index": args.figure_index,
                      "page": entry["page"], "image": filename,
                      "image_pixels": list(picture.size), "bbox": entry["bbox"],
                      "candidate_crops": candidates,
                      "note": "Lower difference suggests matching orientation; resize and rasterization differences prevent exact equality."},
                     ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()
