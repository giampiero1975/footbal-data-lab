#!/usr/bin/env python3
"""Build isolated, auditable H09 figure-text evidence records from H08 candidates.

No production index writes. No use of offline gold labels. Every record keeps
source paragraph text and figure provenance, never inferred tactical meaning.
"""
import argparse
import hashlib
import json
from pathlib import Path


def build(h08, source_id):
    paragraphs = {p.get("ref"): p for p in h08.get("paragraphs", []) if p.get("ref")}
    caption_refs = {c.get("ref") for f in h08.get("figures", [])
                    for c in f.get("caption", []) if c.get("ref")}
    records = []
    excluded = {"unlabeled": 0, "no_explicit_link": 0, "caption_link": 0,
                "missing_text": 0, "duplicate": 0}
    seen = set()
    for f in h08.get("figures", []):
        ids = f.get("figure_ids_from_caption") or []
        if len(ids) != 1:
            excluded["unlabeled"] += 1
            continue
        links = f.get("paragraph_candidates") or []
        if not links:
            excluded["no_explicit_link"] += 1
        for link in links:
            ref = link.get("paragraph_ref")
            if ref in caption_refs:
                excluded["caption_link"] += 1
                continue
            p = paragraphs.get(ref)
            if not p or not (p.get("text") or "").strip():
                excluded["missing_text"] += 1
                continue
            if (link.get("reason") != "explicit_figure_reference"
                    or ids[0] not in (p.get("mentions") or [])):
                excluded["missing_text"] += 1
                continue
            key = (f.get("figure_index"), ref)
            if key in seen:
                excluded["duplicate"] += 1
                continue
            seen.add(key)
            stable = hashlib.sha256(
                json.dumps([source_id, *key], ensure_ascii=False).encode("utf-8")
            ).hexdigest()[:20]
            records.append({
                "id": "h09-" + stable,
                "source_id": source_id,
                "figure_index": f.get("figure_index"),
                "figure_id": ids[0],
                "figure_page": f.get("page"),
                "image": f.get("image"),
                "figure_ref": f.get("self_ref"),
                "caption_source": f.get("caption_source", "unknown"),
                "captions": f.get("caption", []),
                "paragraph_ref": ref,
                "paragraph_page": p.get("page"),
                "paragraph_label": p.get("label"),
                "text": p["text"],
                "link_type": "explicit_figure_reference",
                "validation": "candidate_unverified",
            })
    return {
        "schema_version": "h09.0.1",
        "source_id": source_id,
        "policy": "Offline candidates only; explicit text references; no inferred visual or tactical semantics.",
        "records": records,
        "counts": {"figures": len(h08.get("figures", [])),
                   "evidence_records": len(records), "excluded": excluded},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--h08", required=True, type=Path)
    ap.add_argument("--source-id", required=True)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    if not args.h08.is_file():
        ap.error("H08 input not found")
    if args.output.resolve() == args.h08.resolve():
        ap.error("Output cannot overwrite H08 input")
    result = build(json.loads(args.h08.read_text(encoding="utf-8")), args.source_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
