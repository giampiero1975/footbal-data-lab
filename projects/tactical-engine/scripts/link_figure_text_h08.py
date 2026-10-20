#!/usr/bin/env python3
"""H08: offline, conservative links between Docling figures and source text.
Reads existing Docling JSON and image manifest; never modifies source files or indexes.
"""
import argparse
import json
import re
from pathlib import Path

REF = re.compile(r"(?i)\b(?:fig(?:ura|ure|g)?\.?|schema|diagramma)\s*(?:n\.?\s*)?(\d{1,3}(?:\s*[/.-]\s*[a-z])?)\b")


def figure_id(value):
    return re.sub(r"\s+", "", value.lower()).replace(".", "/")


def page_of(item):
    return next((p.get("page_no") for p in item.get("prov", [])
                 if isinstance(p, dict) and isinstance(p.get("page_no"), int)), None)


def build(doc, manifest):
    texts = doc.get("texts", [])
    by_ref = {t.get("self_ref"): t for t in texts if isinstance(t, dict) and t.get("self_ref")}
    paragraphs = []
    for t in texts:
        if not isinstance(t, dict) or not isinstance(t.get("text"), str) or not t["text"].strip():
            continue
        paragraphs.append({
            "ref": t.get("self_ref"), "page": page_of(t),
            "label": str(t.get("label", "")).lower(), "text": t["text"],
            "mentions": sorted({figure_id(m) for m in REF.findall(t["text"])})
        })
    figures = []
    # Geometric recovery is allowed only for an explicit figure label, on the
    # same page, immediately below a single picture (BOTTOMLEFT coordinates).
    claimed = {str(x.get("$ref") if isinstance(x, dict) else x)
               for m in manifest for x in m.get("captions", [])}
    def bbox_of(t):
        for prov in t.get("prov", []):
            if isinstance(prov, dict) and isinstance(prov.get("bbox"), dict):
                return prov["bbox"]
        return None
    proposals = {}
    for t in texts:
        if not isinstance(t, dict) or t.get("self_ref") in claimed:
            continue
        raw = (t.get("text") or "").strip()
        if not REF.fullmatch(raw):
            continue
        tb = bbox_of(t)
        if not tb or tb.get("coord_origin", "BOTTOMLEFT") != "BOTTOMLEFT":
            continue
        matches = []
        for m in manifest:
            pb = m.get("bbox") or {}
            if (page_of(t) != m.get("page") or
                    pb.get("coord_origin", "BOTTOMLEFT") != "BOTTOMLEFT"):
                continue
            try:
                # Docling picture bounds can include a label at either edge.
                distance = min(abs(float(pb["b"]) - float(tb["t"])),
                               abs(float(pb["b"]) - float(tb["b"])),
                               abs(float(pb["t"]) - float(tb["t"])),
                               abs(float(pb["t"]) - float(tb["b"])))
                horizontal = float(pb["l"]) - 55 <= float(tb["l"]) <= float(pb["r"])
            except (KeyError, ValueError, TypeError):
                continue
            if horizontal and distance <= 25:
                matches.append((m.get("figure_index"), distance))
        matches.sort(key=lambda x: x[1])
        if matches and (len(matches) == 1 or matches[1][1] - matches[0][1] >= 8):
            proposals.setdefault(matches[0][0], []).append(t)
    for item in manifest:
        captions = []
        for raw in item.get("captions", []):
            ref = raw.get("$ref") if isinstance(raw, dict) else raw
            t = by_ref.get(ref)
            if t:
                captions.append({"ref": ref, "text": t.get("text", "")})
        recovered = proposals.get(item.get("figure_index"), [])
        if not captions and len(recovered) == 1:
            t = recovered[0]
            captions.append({"ref": t["self_ref"], "text": t["text"]})
        ids = sorted({figure_id(m) for c in captions for m in REF.findall(c["text"])})
        links = []
        caption_refs = {c["ref"] for c in captions}
        for paragraph in paragraphs:
            if paragraph["ref"] in caption_refs or paragraph["page"] is None:
                continue
            exact = bool(set(ids) & set(paragraph["mentions"]))
            if not exact:
                continue
            reason, status = "explicit_figure_reference", "candidate"
            links.append({"paragraph_ref": paragraph["ref"], "page": paragraph["page"],
                          "reason": reason, "status": status})
        figures.append({
            "figure_index": item.get("figure_index"), "self_ref": item.get("self_ref"),
            "page": item.get("page"), "image": item.get("file"),
            "caption": captions, "figure_ids_from_caption": ids,
            "caption_source": "docling" if item.get("captions") else
                              "geometry_candidate" if captions else "missing",
            "paragraph_candidates": links, "status": "candidates_only" if ids else "requires_review"
        })
    return {"schema_version": "h08.0.1",
            "policy": "No inferred tactical semantics; links are candidates, not verified evidence.",
            "figures": figures, "paragraphs": paragraphs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docling-json", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    for path in (args.docling_json, args.manifest):
        if not path.is_file():
            parser.error(f"Missing input: {path}")
    if args.output.resolve() in (args.docling_json.resolve(), args.manifest.resolve()):
        parser.error("Output must not overwrite inputs")
    result = build(json.loads(args.docling_json.read_text(encoding="utf-8")),
                   json.loads(args.manifest.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"figures": len(result["figures"]), "output": str(args.output)}))


if __name__ == "__main__":
    main()
