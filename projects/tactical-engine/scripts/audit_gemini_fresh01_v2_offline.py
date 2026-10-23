#!/usr/bin/env python3
"""Offline source-anchored audit of retained Gemini v2 review; no API calls."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import review_rag_v5_gemini as client

def quote_matches(quote, source):
    if not isinstance(quote, str) or not quote.strip():
        return False
    text = " ".join(source.split())
    pieces = re.split(r"\s*\.\.\.\s*", " ".join(quote.split()))
    if any(len(p.strip()) < 8 for p in pieces):
        return False
    offset = 0
    for piece in pieces:
        pos = text.find(piece, offset)
        if pos < 0:
            return False
        offset = pos + len(piece)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--source-bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report_bytes = args.report.read_bytes()
    report = json.loads(report_bytes)
    bundle_bytes = args.source_bundle.read_bytes()
    bundle = json.loads(bundle_bytes)
    assert report["question_id"] == bundle["question_id"] == "fresh_01"
    assert report["source_bundle_sha256"] == hashlib.sha256(bundle_bytes).hexdigest()
    assert report["status"] == "BLOCCATO"
    review = report["raw_review"]
    assert review["id"] == "fresh_01"
    manifest = json.loads(client.MANIFEST.read_text(encoding="utf-8"))
    row = next(q for q in manifest["questions"] if q["id"] == "fresh_01")
    docs = client.validate_bundle(bundle, row)
    required = row["mandatory_claims"] + row["forbidden_claims"]
    covered = {check["claim"] for check in review["checks"]}
    assert all(claim in covered for claim in required), "INCOMPLETE_CLAIM_COVERAGE"
    findings = []
    for check in review["checks"]:
        assert isinstance(check.get("supported"), bool)
        evidence = check.get("evidence", [])
        if review["decision"] == "PASS":
            assert check["supported"] and evidence, "UNSUPPORTED_PASS"
        for ev in evidence:
            sources = [d for d in docs if str(d["page"]) == str(ev.get("page")) and d["source_file_id"] == ev.get("source_file_id")]
            valid = any(quote_matches(ev.get("quote"), d["text"]) for d in sources)
            findings.append({"page": ev.get("page"), "quote": ev.get("quote"), "verified": valid})
    passed = bool(findings) and all(x["verified"] for x in findings)
    output = {"question_id": "fresh_01", "source_report_sha256": hashlib.sha256(report_bytes).hexdigest(),
              "source_bundle_sha256": hashlib.sha256(bundle_bytes).hexdigest(),
              "raw_gemini_decision": review["decision"],
              "status": "VALIDATO" if passed else "BLOCCATO",
              "evidence_count": len(findings), "findings": findings,
              "method": "ordered literal spans; only explicit ellipses may skip source text; whitespace normalized",
              "api_requests": 0}
    client.atomic_write(args.output, output)
    print("REPORT", args.output, "STATUS", output["status"], "EVIDENCE", len(findings), "API_REQUESTS=0")
    if not passed:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
