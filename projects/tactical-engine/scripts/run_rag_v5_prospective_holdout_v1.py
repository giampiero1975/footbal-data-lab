#!/usr/bin/env python3
"""Execute only a validated frozen prospective RAG V5 question set."""
import argparse
import json
import sys
from pathlib import Path
import smoke_test_rag_v5_e2e as v5

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--execute", action="store_true")
    args = p.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("status") != "frozen":
        p.error("Prospective manifest must be frozen before execution")
    rows = manifest.get("questions", [])
    if len(rows) != 10 or len({r["id"] for r in rows}) != 10:
        p.error("Expected ten distinct questions")
    if any(r.get("gold_status") != "verified" or not r.get("reviewer") for r in rows):
        p.error("Gold and independent reviewer must be verified")
    if not args.execute:
        print("READY: pass --execute to run")
        return
    if args.output.exists() or args.output.resolve() == args.manifest.resolve():
        p.error("Refusing to overwrite existing output or manifest")
    v5.QUESTIONS = [(r["id"], r["question"]) for r in rows]
    sys.argv = [v5.__file__, "--limit", "10", "--output", str(args.output)]
    v5.main()
    print("Manual independent adjudication required; no automatic 9/10 claim.")

if __name__ == "__main__":
    main()
