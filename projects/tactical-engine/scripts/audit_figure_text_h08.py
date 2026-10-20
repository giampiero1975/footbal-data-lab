#!/usr/bin/env python3
"""Read-only summary of H08 figure-text candidate links."""
import argparse
import json
from collections import Counter
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("report", type=Path)
    a = p.parse_args()
    data = json.loads(a.report.read_text(encoding="utf-8"))
    rows = []
    for fig in data.get("figures", []):
        counts = Counter(link.get("reason") for link in fig.get("paragraph_candidates", []))
        rows.append({
            "index": fig.get("figure_index"), "page": fig.get("page"),
            "caption_ids": fig.get("figure_ids_from_caption", []),
            "captions": len(fig.get("caption", [])),
            "explicit_links": counts["explicit_figure_reference"],
            "same_page_unverified": counts["same_page_only"],
            "status": fig.get("status")
        })
    print(json.dumps({
        "figures": len(rows),
        "with_caption": sum(bool(x["captions"]) for x in rows),
        "with_figure_id": sum(bool(x["caption_ids"]) for x in rows),
        "with_explicit_link": sum(x["explicit_links"] > 0 for x in rows),
        "explicit_links_total": sum(x["explicit_links"] for x in rows),
        "same_page_unverified_total": sum(x["same_page_unverified"] for x in rows),
        "rows": rows
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
