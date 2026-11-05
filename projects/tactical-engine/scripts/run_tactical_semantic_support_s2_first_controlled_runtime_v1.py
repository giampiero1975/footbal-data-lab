#!/usr/bin/env python3
"""Single opt-in S2/NLI V2 bridge diagnostic over three frozen cases.

No retrieval, Chroma, API, panel or production state is accessed.  The runner
does nothing unless --execute is supplied and never retries a judge call.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import v5_tactical_semantic_support_s1 as s1
import v5_tactical_semantic_support_s2 as s2
import v5_tactical_semantic_support_s2_nli_v2_bridge as bridge_v1


FIXTURE_SCHEMA = "tactical_semantic_support_s2_first_controlled_runtime_fixture_v1"
REPORT_SCHEMA = "tactical_semantic_support_s2_first_controlled_runtime_report_v1"
EXPECTED_LABELS = {"supported", "contradicted", "insufficient"}
MAX_CASES = 3


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def digest_bytes(value):
    return "sha256:" + hashlib.sha256(value).hexdigest()


def digest_document(value):
    return digest_bytes(canonical_json(value).encode("utf-8"))


def load_inputs(root, fixture_path):
    fixture_bytes = fixture_path.read_bytes()
    fixture = json.loads(fixture_bytes.decode("utf-8"))
    if fixture.get("schema") != FIXTURE_SCHEMA:
        raise ValueError("unexpected_fixture_schema")
    selected = fixture.get("cases")
    if not isinstance(selected, list) or len(selected) != MAX_CASES:
        raise ValueError("exactly_three_cases_required")
    ids = [item.get("case_id") for item in selected if isinstance(item, dict)]
    if len(ids) != MAX_CASES or len(set(ids)) != MAX_CASES:
        raise ValueError("invalid_or_duplicate_case_ids")
    expected = [item.get("expected_label") for item in selected]
    if set(expected) != EXPECTED_LABELS:
        raise ValueError("one_case_per_label_required")
    source_rel = fixture.get("source_dataset")
    if not isinstance(source_rel, str) or not source_rel:
        raise ValueError("invalid_source_dataset")
    source_path = root / source_rel
    source_bytes = source_path.read_bytes()
    observed = hashlib.sha256(source_bytes).hexdigest()
    if observed != fixture.get("source_dataset_sha256"):
        raise ValueError("source_dataset_digest_mismatch")
    source = json.loads(source_bytes.decode("utf-8"))
    by_id = {case.get("id"): case for case in source.get("cases", [])
             if isinstance(case, dict)}
    cases = []
    for selection in selected:
        case = by_id.get(selection["case_id"])
        if not isinstance(case, dict):
            raise ValueError("selected_case_missing")
        if case.get("gold") != selection["expected_label"]:
            raise ValueError("selected_case_label_mismatch")
        if not all(isinstance(case.get(key), str) and case[key]
                   for key in ("claim", "evidence", "source")):
            raise ValueError("selected_case_content_invalid")
        cases.append({**copy.deepcopy(case),
                      "selection_reason": selection.get("selection_reason")})
    return fixture, cases, {
        "fixture_sha256": digest_bytes(fixture_bytes),
        "source_dataset_sha256": "sha256:" + observed,
    }


def _claim(case):
    statement = case["claim"]
    return {
        "claim_id": "claim:" + case["id"],
        "statement": statement,
        "section_span": {"start": 0, "end": len(statement)},
        "conditions": [],
        "relation_refs": ["relation:diagnostic:" + case["id"]],
        "requirement_refs": ["requirement:diagnostic:" + case["id"]],
        "dimensions": ["detail"],
        "bindings": {},
        "polarity": "affirmed",
        "evidence_refs": ["evidence:" + case["id"]],
        "support_mode": "direct",
        "evidence_anchors": [{
            "evidence_ref": "evidence:" + case["id"],
            "exact_text": case["evidence"],
        }],
    }


def execute_cases(fixture, cases, identities, judge, judge_descriptor,
                  runtime_config):
    plan_fingerprint = digest_document({
        "activity_id": fixture["activity_id"],
        "fixture_sha256": identities["fixture_sha256"],
        "case_ids": [case["id"] for case in cases],
    })
    report = {
        "schema": REPORT_SCHEMA,
        "activity_id": fixture["activity_id"],
        "mode": "shadow_only",
        "promotion_authorized": False,
        "plan_fingerprint": plan_fingerprint,
        "input_identities": identities,
        "runtime_config": runtime_config,
        "maximum_inferences": MAX_CASES,
        "actual_inferences": 0,
        "stopped_early": False,
        "cases": [],
        "summary": {},
        "limitations": [
            "Three reused diagnostic cases are not an independent benchmark",
            "Semantic accuracy is not estimable from this run",
            "S2 results cannot modify S1, overall status or promoted answer",
        ],
    }
    for case in cases:
        claim = _claim(case)
        evidence_ref = claim["evidence_refs"][0]
        evidence = {evidence_ref: {
            "text": case["evidence"], "source": case["source"],
            "page": case.get("page"),
        }}
        attempt_id = "attempt:s2-first-controlled:" + case["id"]
        s1_assessment = s1.assess_claim(
            attempt_id, plan_fingerprint, claim, evidence)
        before = s1.canonical_json(s1_assessment)
        s2_record = s2.assess_claim(
            attempt_id, plan_fingerprint, claim, evidence, s1_assessment,
            {claim["relation_refs"][0]: {}}, judge, judge_descriptor)
        report["actual_inferences"] += 1
        after = s1.canonical_json(s1_assessment)
        observed = s2_record.get("aggregate_verdict")
        row = {
            "case_id": case["id"],
            "source": case["source"],
            "page": case.get("page"),
            "claim": case["claim"],
            "evidence": case["evidence"],
            "selection_reason": case["selection_reason"],
            "expected_label": case["gold"],
            "label_provenance": fixture["label_provenance"],
            "s1_assessment": s1_assessment,
            "s1_unchanged": before == after,
            "s2_shadow_assessment": s2_record,
            "technical_pass": (
                s2_record.get("evaluation_status") == "evaluated" and
                s2_record.get("promotion_authorized") is False and
                before == after
            ),
            "semantic_match": observed == case["gold"],
        }
        report["cases"].append(row)
        if s2_record.get("evaluation_status") != "evaluated":
            report["stopped_early"] = True
            break
    report["summary"] = {
        "technical_passes": sum(bool(row["technical_pass"])
                                for row in report["cases"]),
        "semantic_matches": sum(bool(row["semantic_match"])
                                for row in report["cases"]),
        "completed_cases": len(report["cases"]),
        "all_s1_unchanged": all(row["s1_unchanged"] for row in report["cases"]),
        "all_non_promotable": all(
            row["s2_shadow_assessment"].get("promotion_authorized") is False
            for row in report["cases"]),
    }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        parser.error("real inference disabled: explicit --execute required")
    if args.timeout < 1 or args.max_tokens < 1:
        parser.error("invalid runtime limits")
    if not args.fixtures.is_file():
        parser.error("fixture file missing")
    if not args.output.parent.is_dir() or args.output.exists():
        parser.error("output parent missing or output already exists")
    # The historical NLI module imports its runtime dependency (pydantic).
    # Keep deterministic fixture validation and mock tests independent from it.
    import shadow_nli_v2_inference as nli_v2
    root = Path(__file__).resolve().parents[1]
    fixture, cases, identities = load_inputs(root, args.fixtures.resolve())
    runtime_config = {
        "judge": "shadow_nli_v2_inference.judge_pair",
        "model": args.model,
        "ollama_url": args.ollama_url,
        "timeout_seconds_per_call": args.timeout,
        "max_tokens": args.max_tokens,
        "temperature": 0,
        "num_ctx": 4096,
        "retry": False,
    }
    def call(claim, evidence):
        return nli_v2.judge_pair(
            claim, evidence, model=args.model, ollama_url=args.ollama_url,
            timeout=args.timeout, max_tokens=args.max_tokens)
    bridge = bridge_v1.build_bridge(call, runtime_config)
    report = execute_cases(
        fixture, cases, identities, bridge, bridge.judge_descriptor,
        runtime_config)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    if report["stopped_early"]:
        raise SystemExit(2)
    raise SystemExit(0)


if __name__ == "__main__":
    main()
