#!/usr/bin/env python3
"""Run one arbitrary question through the integrated V5 pipeline."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import run_rag_v5_locked_candidate_v2 as locked


def validate_question(value: str) -> str:
    value = " ".join(value.split())
    if not 10 <= len(value) <= 2000:
        raise argparse.ArgumentTypeError("question length must be 10..2000 characters")
    return value


def validate_request_id(value: str) -> str:
    if not re.fullmatch(r"[a-zA-Z0-9_-]{8,64}", value):
        raise argparse.ArgumentTypeError("invalid request id")
    return value


def validate_report(report: dict) -> None:
    questions = report.get("questions", [])
    if len(questions) != 1 or report.get("error") or not report.get("index_unchanged"):
        raise RuntimeError("incomplete_report")
    item = questions[0]
    if item.get("invalid_citation_ids"):
        raise RuntimeError("invalid_citations")
    if not item.get("has_any_citation"):
        raise RuntimeError("missing_citations")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True, type=validate_question)
    parser.add_argument("--request-id", required=True, type=validate_request_id)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--legacy-profile", action="store_true")
    parser.add_argument("--collection", default="dribbling_tactics_v5_multisource")
    parser.add_argument("--expected-count", type=int, default=5319)
    parser.add_argument("--evidence-limit", type=int, choices=range(4, 9), default=8)
    parser.add_argument("--max-output-tokens", type=int, default=0)
    args = parser.parse_args()
    if args.max_output_tokens and not 128 <= args.max_output_tokens <= 4096:
        parser.error("max-output-tokens must be 0 or between 128 and 4096")
    if args.output.exists():
        parser.error(f"output exists; refusing overwrite: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    locked.select_runtime()
    import smoke_test_rag_v5_e2e as v5

    v5.QUESTIONS = [(args.request_id, args.question)]
    argv = [v5.__file__, "--limit", str(args.evidence_limit), "--output", str(args.output),
            "--collection", args.collection, "--expected-count", str(args.expected_count)]
    if args.max_output_tokens:
        argv.extend(["--num-predict", str(args.max_output_tokens)])
    if not args.legacy_profile:
        argv.extend([
            "--source-aware", "--exercise-candidate", "--priority-exact",
            "--targeted-coverage", "--heading-routing",
        ])
    sys.argv = argv
    v5.main()
    report = json.loads(args.output.read_text(encoding="utf-8"))
    try:
        validate_report(report)
    except RuntimeError as exc:
        raise SystemExit(f"INCOMPLETE: {exc}") from exc
    print(f"QUERY COMPLETE request_id={args.request_id}", flush=True)


if __name__ == "__main__":
    main()
