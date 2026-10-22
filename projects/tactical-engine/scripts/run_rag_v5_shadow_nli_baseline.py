#!/usr/bin/env python3
"""Reproducible, non-destructive RAG V5 baseline -> NLI V2 shadow run.

Uses the previously reviewed 15 exact answer spans; validates every offset against
the local baseline, prepares claim/evidence pairs, then calls the existing shadow
NLI V2 runner. Does not alter Chroma, the baseline, or production RAG.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from shadow_nli_v2_offline import prepare

SPECS = [
    ("q2", "q2_c01", 1360, 1549),
    ("q3", "q3_c01", 190, 378),
    ("q3", "q3_c02", 380, 501),
    ("q3", "q3_c03", 559, 790),
    ("q3", "q3_c04", 791, 953),
    ("q3", "q3_c05", 1799, 1982),
    ("q3", "q3_c06", 1983, 2118),
    ("q5", "q5_c01", 123, 302),
    ("q5", "q5_c02", 307, 481),
    ("q5", "q5_c03", 486, 671),
    ("q5", "q5_c04", 701, 990),
    ("q5", "q5_c05", 995, 1298),
    ("q5", "q5_c06", 1303, 1593),
    ("q5", "q5_c07", 1598, 1793),
    ("q5", "q5_c08", 1798, 2006),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_baseline_20261022.json"))
    parser.add_argument("--prepared", type=Path, default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_prepared_20261022.json"))
    parser.add_argument("--output", type=Path, default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_nli_results_20261022.json"))
    parser.add_argument("--max-pairs", type=int, default=20)
    parser.add_argument("--execute", action="store_true", help="Explicitly authorize Ollama inference")
    args = parser.parse_args()
    if not args.execute:
        parser.error("Pass --execute to enable model inference")
    if not 1 <= args.max_pairs <= 20:
        parser.error("--max-pairs must be between 1 and 20")
    source, prepared_path, output = (p.resolve() for p in (args.source, args.prepared, args.output))
    if len({source, prepared_path, output}) != 3:
        parser.error("Input, prepared and output paths must be distinct")
    if prepared_path.exists() or output.exists():
        parser.error("Refusing to overwrite existing prepared/output file")
    report = json.loads(source.read_text(encoding="utf-8"))
    questions = {q["id"]: q for q in report["questions"]}
    annotations = {"claims": []}
    for qid, cid, start, end in SPECS:
        answer = questions[qid]["answer"]
        span = answer[start:end]
        if end > len(answer) or not re.search(r"\[F[1-9][0-9]*\]", span):
            raise ValueError(f"Invalid or uncited span {qid}/{cid}")
        text = re.sub(r"\[F[1-9][0-9]*\]", "", span)
        text = " ".join(text.split()).strip(" .;:,!?")
        annotations["claims"].append({
            "question_id": qid, "claim_id": cid, "start": start,
            "end": end, "span": span, "text": text,
        })
    prepared = prepare(report, annotations)
    pairs = sum(len(c["pairs"]) for c in prepared["claims"])
    if len(prepared["claims"]) != 15 or pairs != 20:
        raise ValueError(f"Unexpected counts: {len(prepared['claims'])} claims, {pairs} pairs")
    prepared_path.parent.mkdir(parents=True, exist_ok=True)
    with prepared_path.open("x", encoding="utf-8") as stream:
        json.dump(prepared, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(f"PREPARATION_OK 15 claims 20 pairs: {prepared_path}", flush=True)
    command = [
        sys.executable, str(Path(__file__).with_name("shadow_nli_v2_inference.py")),
        "--prepared", str(prepared_path), "--output", str(output),
        "--max-pairs", str(args.max_pairs), "--execute",
    ]
    subprocess.run(command, check=True)
    print(f"REPORT {output}", flush=True)


if __name__ == "__main__":
    main()
