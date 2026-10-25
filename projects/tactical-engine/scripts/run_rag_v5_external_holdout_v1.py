#!/usr/bin/env python3
"""Execute a pre-frozen external V5 holdout without weakening the locked runner."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import run_rag_v5_locked_candidate_v2 as locked


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--expected-sha256",required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--collection",default="dribbling_tactics_v5_multisource_drive11_candidate_v1")
    p.add_argument("--expected-count",type=int,default=6196)
    p.add_argument("--execute",action="store_true")
    a=p.parse_args()
    data=a.manifest.read_bytes(); digest=hashlib.sha256(data).hexdigest()
    if digest != a.expected_sha256: p.error(f"manifest hash mismatch: {digest}")
    manifest=json.loads(data); rows=manifest.get("questions",[])
    if manifest.get("status") != "frozen_before_generation" or len(rows)<5 or len({x["id"] for x in rows}) != len(rows):
        p.error("manifest must be frozen with at least five distinct questions")
    required={"id","question","source","evidence_ids","pages","mandatory_claims","forbidden_claims"}
    if any(not required.issubset(row) for row in rows): p.error("incomplete holdout row")
    if a.output.exists(): p.error("output exists; refusing overwrite")
    print(f"EXTERNAL_LOCK_OK sha256={digest} questions={len(rows)}",flush=True)
    if not a.execute: return
    locked.select_runtime()
    import smoke_test_rag_v5_e2e as v5
    v5.QUESTIONS=[(x["id"],x["question"]) for x in rows]
    sys.argv=[v5.__file__,"--limit","8","--output",str(a.output),"--collection",a.collection,
              "--expected-count",str(a.expected_count),"--source-aware","--exercise-candidate",
              "--priority-exact","--targeted-coverage","--heading-routing"]
    v5.main()
    report=json.loads(a.output.read_text(encoding="utf-8"))
    if len(report.get("questions",[])) != len(rows) or report.get("error") or not report.get("index_unchanged"):
        raise SystemExit("INCOMPLETE: do not adjudicate")
    print(f"EXTERNAL_COMPLETE {len(rows)}/{len(rows)}",flush=True)


if __name__ == "__main__": main()
