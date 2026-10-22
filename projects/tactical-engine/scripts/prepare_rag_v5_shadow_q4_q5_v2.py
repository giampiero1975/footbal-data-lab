#!/usr/bin/env python3
"""Prepare Q4/Q5 diagnostic claims from baseline V2; no inference or index writes."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from shadow_nli_v2_offline import prepare

source = ROOT / "evaluation/reports/rag_v5_shadow_baseline_20261022_v2.json"
coordinates = ROOT / "evaluation/annotations/rag_v5_shadow_claims_q4_q5_v2.json"
output = ROOT / "evaluation/reports/rag_v5_shadow_nli_q4_q5_prepared_v2.json"

report = json.loads(source.read_text(encoding="utf-8"))
spec = json.loads(coordinates.read_text(encoding="utf-8"))
questions = {q["id"]: q for q in report["questions"]}
claims = []
for item in spec["claims"]:
    qid = item["question_id"]
    answer = questions[qid]["answer"]
    start, end = item["start"], item["end"]
    span = answer[start:end]
    citations = re.findall(r"\[F([1-9][0-9]*)\]", span)
    if not citations:
        raise ValueError(f"No citations in {item['claim_id']}")
    claim = " ".join(re.sub(r"\[F[1-9][0-9]*\]", "", span).split()).strip(" .;:,!?")
    claims.append({**item, "span": span, "text": claim})
prepared = prepare(report, {"claims": claims})
if len(prepared["claims"]) != 10 or sum(len(c["pairs"]) for c in prepared["claims"]) != 13:
    raise ValueError("Unexpected number of diagnostic claims/pairs")
with output.open("x", encoding="utf-8") as f:
    json.dump(prepared, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("PREPARAZIONE OK; claim: 10; coppie NLI: 13; report:", output)
