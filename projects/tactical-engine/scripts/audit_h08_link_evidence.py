#!/usr/bin/env python3
"""Read-only H08 evidence audit: inspect linked paragraphs and unl inked figure 15 context."""
import argparse
import json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report", type=Path)
    ap.add_argument("--focus", nargs="*", default=["15/a", "15/b", "17"])
    args = ap.parse_args()
    data = json.loads(args.report.read_text(encoding="utf-8"))
    paragraphs = {p["ref"]: p for p in data["paragraphs"]}
    for fig in data["figures"]:
        ids = fig["figure_ids_from_caption"]
        if not ids:
            continue
        print("\nFIGURE", fig["figure_index"], "ids", ids, "page", fig["page"],
              "caption_source", fig.get("caption_source"), "links", len(fig["paragraph_candidates"]))
        for link in fig["paragraph_candidates"]:
            p = paragraphs.get(link["paragraph_ref"], {})
            print(" LINK", link["paragraph_ref"], "page", p.get("page"),
                  "label", p.get("label"), "mentions", p.get("mentions"),
                  "text", (p.get("text") or "")[:650])
        if any(i in args.focus for i in ids):
            for p in data["paragraphs"]:
                if p.get("page") == fig["page"] and p.get("label") not in ("caption", "page-header", "page-footer", "section_header"):
                    print(" CONTEXT_NOT_LINKED", p.get("ref"), "mentions", p.get("mentions"),
                          "text", (p.get("text") or "")[:500])
    print("\nNOTE: Context is NOT a figure link. No semantic validation performed.")

if __name__ == "__main__":
    main()
