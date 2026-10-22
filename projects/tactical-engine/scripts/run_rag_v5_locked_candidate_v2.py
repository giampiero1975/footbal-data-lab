#!/usr/bin/env python3
"""Read-only V5 locked-candidate execution. No claim of independent gold approval."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA256 = "f0d36bc5b35ddcfd42bfef234db2380db6a684a9b81fb9cd19ab75bea81755c0"
DEFAULT_MANIFEST = ROOT / "evaluation/rag_v5_independent_candidate_v2.json"
DEFAULT_OUTPUT = ROOT / "evaluation/rag_v5_candidate_v2_runtime_report.json"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--execute", action="store_true")
    p.add_argument("--approved-gold", action="store_true", help="Only if independent review has approved the locked SHA")
    args = p.parse_args()
    data = args.manifest.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        p.error(f"Manifest hash mismatch: {digest}; expected {EXPECTED_SHA256}")
    manifest = json.loads(data)
    rows = manifest["questions"]
    if len(rows) != 10 or len({x["id"] for x in rows}) != 10:
        p.error("Exactly ten distinct questions required")
    if args.output.exists():
        p.error(f"Output exists; refusing overwrite: {args.output}")
    if args.approved_gold and (manifest.get("status") != "frozen" or
        any(not q.get("reviewer") for q in rows)):
        p.error("Gold is not independently approved; cannot use --approved-gold")
    print(f"LOCK_OK sha256={digest} questions={len(rows)} mode=diagnostic_unreviewed", flush=True)
    if not args.execute:
        print("READY: pass --execute to generate the read-only diagnostic report", flush=True)
        return
    import smoke_test_rag_v5_e2e as v5
    v5.QUESTIONS = [(x["id"], x["question"]) for x in rows]
    # --limit refers to retrieved evidence count, not the number of questions.
    sys.argv = [v5.__file__, "--limit", "8", "--output", str(args.output)]
    v5.main()
    report = json.loads(args.output.read_text(encoding="utf-8"))
    if len(report.get("questions", [])) != 10 or report.get("error") or not report.get("index_unchanged"):
        raise SystemExit("INCOMPLETE: inspect report, do not claim certification")
    print("DIAGNOSTIC COMPLETE: 10/10 generated; independent gold and blind adjudication still pending", flush=True)

if __name__ == "__main__":
    main()
