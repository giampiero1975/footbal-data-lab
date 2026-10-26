#!/usr/bin/env python3
"""Apply reviewed editorial decisions to the FIGC catalog atomically."""
from __future__ import annotations
import argparse, json, os, tempfile
from pathlib import Path


def apply(catalog_path: Path, decisions_path: Path) -> int:
    catalog=json.loads(catalog_path.read_text(encoding="utf-8"))
    decisions=json.loads(decisions_path.read_text(encoding="utf-8"))
    allowed={"candidate_tactical","exclude_tactical"}
    for row in decisions["decisions"]:
        digest=row["sha256"]
        if digest not in catalog.get("documents",{}):
            raise ValueError(f"unknown sha256: {digest}")
        if row["decision"] not in allowed:
            raise ValueError(f"invalid decision: {row['decision']}")
        catalog["documents"][digest].update({
            "editorial_decision":row["decision"],
            "editorial_reason":row["reason"],
            "editorial_reviewed_at":decisions["reviewed_at"],
            "editorial_review":decisions["schema"],
        })
    fd,tmp=tempfile.mkstemp(prefix=f".{catalog_path.name}.",dir=catalog_path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as stream:
            json.dump(catalog,stream,ensure_ascii=False,indent=2,sort_keys=True); stream.write("\n")
        os.replace(tmp,catalog_path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
    return len(decisions["decisions"])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog",type=Path,required=True)
    parser.add_argument("--decisions",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps({"updated":apply(args.catalog,args.decisions)}))


if __name__=="__main__": main()
