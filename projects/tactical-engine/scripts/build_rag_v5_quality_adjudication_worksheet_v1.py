#!/usr/bin/env python3
"""Prepare a non-destructive, offline atomic-claim review worksheet for RAG V5 holdout.

No Ollama, Chroma or production calls. Never overwrites existing reports.
Human reviewer must split claims and inspect evidence; this script does not score quality.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def build(data, digest):
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("Expected nonempty questions list")
    seen = set()
    rows = []
    for item in questions:
        qid = item["id"]
        if qid in seen:
            raise ValueError(f"Duplicate question id: {qid}")
        seen.add(qid)
        evidence = item.get("evidence", [])
        lookup = {x["label"]: x for x in evidence}
        if len(lookup) != len(evidence):
            raise ValueError(f"Duplicate evidence label: {qid}")
        cited = sorted(set(re.findall(r"\[F\d+\]", item["answer"])))
        missing = [c for c in cited if c[1:-1] not in lookup]
        rows.append({
            "question_id": qid,
            "question": item["question"],
            "answer": item["answer"],
            "citation_labels_used": cited,
            "missing_citation_labels": missing,
            "evidence": [
                {"label": e["label"], "source": e.get("canonical_source", e.get("source")),
                 "pages": e.get("pages"), "text": e.get("text", "")}
                for e in evidence
            ],
            "atomic_claims": [],
            "adherence": "non_verificato",
            "fidelity": "non_verificato",
            "tactical_precision": "non_verificato",
            "decision": "review",
            "reviewer_notes": "",
        })
    return {
        "schema": "rag_v5_quality_adjudication_worksheet_v1",
        "input_sha256": digest,
        "status": "unscored_review_template",
        "warning": "No automatic quality score; manual atomic-claim adjudication required.",
        "questions": rows,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    if a.input.resolve() == a.output.resolve():
        p.error("Input and output must differ")
    raw = a.input.read_bytes()
    report = build(json.loads(raw), hashlib.sha256(raw).hexdigest())
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("x", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"WORKSHEET_OK questions={len(report['questions'])} output={a.output}")


if __name__ == "__main__":
    main()
