#!/usr/bin/env python3
"""Read-only audit of frozen NLI evidence and canonical V2 prompt.

No Ollama calls, production mutations or overwrite of existing reports.
"""
import argparse
import hashlib
import json
from pathlib import Path
from shadow_nli_v2_inference import load_v2_instruction

def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_baseline_20261022.json"))
    p.add_argument("--output", type=Path, default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_evidence_audit_v1_20261022.json"))
    a = p.parse_args()
    if a.output.exists() or a.source.resolve() == a.output.resolve():
        p.error("Refusing overwrite")
    data = json.loads(a.source.read_text(encoding="utf-8"))
    questions = {q["id"]: q for q in data["questions"]}
    instruction = load_v2_instruction()
    cases = []
    for qid, sid in (("q3", "F1"), ("q3", "F3"), ("q5", "F1"), ("q2", "F2")):
        item = next(e for e in questions[qid]["evidence"] if e["label"] == sid)
        evidence = item["text"]
        cases.append({"question_id": qid, "source_id": sid, "evidence": evidence,
                      "evidence_sha256": sha(evidence), "chars": len(evidence),
                      "prompt_plus_evidence_chars": len(instruction) + len(evidence)})
    report = {"schema": "shadow_nli_evidence_audit_v1", "mode": "read_only",
              "canonical_instruction": instruction,
              "canonical_instruction_sha256": sha(instruction),
              "num_ctx_configured": 4096,
              "note": "Character counts do not prove token-context fit; check tokenizer and Ollama context separately.",
              "evidence": cases}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("x", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("AUDIT", a.output, "instruction_sha256", sha(instruction))
    for item in cases:
        print(item["question_id"], item["source_id"], item["chars"], item["evidence_sha256"])

if __name__ == "__main__":
    main()
