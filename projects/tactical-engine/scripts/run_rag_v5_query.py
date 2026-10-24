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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True, type=validate_question)
    parser.add_argument("--request-id", required=True, type=validate_request_id)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--legacy-profile", action="store_true")
    parser.add_argument("--collection", default="dribbling_tactics_v5_multisource")
    parser.add_argument("--expected-count", type=int, default=5319)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"output exists; refusing overwrite: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    locked.select_runtime()
    import smoke_test_rag_v5_e2e as v5

    v5.QUESTIONS = [(args.request_id, args.question)]
    argv = [v5.__file__, "--limit", "8", "--output", str(args.output),
            "--collection", args.collection, "--expected-count", str(args.expected_count)]
    if not args.legacy_profile:
        argv.extend([
            "--source-aware", "--exercise-candidate", "--priority-exact",
            "--targeted-coverage", "--heading-routing",
        ])
    sys.argv = argv
    v5.main()
    report = json.loads(args.output.read_text(encoding="utf-8"))
    if len(report.get("questions", [])) != 1 or report.get("error") or not report.get("index_unchanged"):
        raise SystemExit("INCOMPLETE: inspect report")
    print(f"QUERY COMPLETE request_id={args.request_id}", flush=True)


if __name__ == "__main__":
    main()
