#!/usr/bin/env python3
"""Opt-in three-case shadow diagnostic for nli_spatial_relations_v1.

The runner is inert on import, never calls NLI V2, never retries, and cannot
promote an answer.  Real inference requires the explicit --execute flag.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import v5_tactical_semantic_support_s1 as s1
import v5_tactical_semantic_support_s2 as s2
import v5_tactical_semantic_support_s2_spatial_v1_bridge as spatial_bridge


FIXTURE_SCHEMA = "tactical_semantic_support_s2_spatial_relation_differential_fixture_v1"
REPORT_SCHEMA = "tactical_semantic_support_s2_spatial_relation_differential_report_v1"
ACTIVITY_ID = "RD-TSC-V2-D3-S2-SPATIAL-RELATION-DIFFERENTIAL-01"
EXPECTED_ROLES = {"known_regression", "distinct_inverse", "insufficient_guard"}
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
    if fixture.get("schema") != FIXTURE_SCHEMA or fixture.get("activity_id") != ACTIVITY_ID:
        raise ValueError("unexpected_fixture_identity")
    selected = fixture.get("cases")
    if not isinstance(selected, list) or len(selected) != MAX_CASES:
        raise ValueError("exactly_three_cases_required")
    if not all(isinstance(item, dict) for item in selected):
        raise ValueError("invalid_case_selection")
    ids = [item.get("case_id") for item in selected]
    if not all(isinstance(item, str) and item for item in ids) or len(set(ids)) != MAX_CASES:
        raise ValueError("invalid_or_duplicate_case_ids")
    if {item.get("role") for item in selected} != EXPECTED_ROLES:
        raise ValueError("one_case_per_role_required")
    if not all(item.get("expected_label") in EXPECTED_LABELS for item in selected):
        raise ValueError("invalid_expected_label")
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
                      "role": selection["role"],
                      "selection_reason": selection.get("selection_reason"),
                      "historical_v2": copy.deepcopy(selection.get("historical_v2"))})
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
        "relation_refs": ["relation:spatial-differential:" + case["id"]],
        "requirement_refs": ["requirement:spatial-differential:" + case["id"]],
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
                  runtime_config, contract_descriptor):
    if len(cases) != MAX_CASES:
        raise ValueError("exactly_three_cases_required")
    plan_fingerprint = digest_document({
        "activity_id": fixture["activity_id"],
        "fixture_sha256": identities["fixture_sha256"],
        "case_ids": [case["id"] for case in cases],
        "contract": contract_descriptor,
    })
    report = {
        "schema": REPORT_SCHEMA,
        "activity_id": fixture["activity_id"],
        "mode": "shadow_only",
        "promotion_authorized": False,
        "authoritative_outputs_modified": False,
        "plan_fingerprint": plan_fingerprint,
        "input_identities": identities,
        "contract": contract_descriptor,
        "runtime_config": runtime_config,
        "planned_evaluations": MAX_CASES,
        "attempted_evaluations": 0,
        "completed_evaluations": 0,
        "run_complete": False,
        "stopped_early": False,
        "cases": [],
        "summary": {},
        "limitations": [
            "q3_04 is a known lexically exposed regression, not independent evidence",
            "Three diagnostic cases cannot establish general semantic accuracy",
            "Only q3_04 has a directly attributable historical V2 runtime result",
            "S2 results cannot modify S1, overall status or promoted answer",
        ],
    }
    for case in cases:
        report["attempted_evaluations"] += 1
        claim = _claim(case)
        evidence_ref = claim["evidence_refs"][0]
        evidence = {evidence_ref: {
            "text": case["evidence"], "source": case["source"],
            "page": case.get("page"),
        }}
        attempt_id = "attempt:s2-spatial-differential:" + case["id"]
        s1_assessment = s1.assess_claim(
            attempt_id, plan_fingerprint, claim, evidence)
        before = s1.canonical_json(s1_assessment)
        s2_record = s2.assess_claim(
            attempt_id, plan_fingerprint, claim, evidence, s1_assessment,
            {claim["relation_refs"][0]: {}}, judge, judge_descriptor)
        after = s1.canonical_json(s1_assessment)
        observed = s2_record.get("aggregate_verdict")
        report["cases"].append({
            "case_id": case["id"],
            "role": case["role"],
            "source": case["source"],
            "page": case.get("page"),
            "claim": case["claim"],
            "evidence": case["evidence"],
            "selection_reason": case["selection_reason"],
            "expected_label": case["gold"],
            "label_provenance": fixture["label_provenance"],
            "historical_v2": case["historical_v2"],
            "s1_assessment": s1_assessment,
            "s1_unchanged": before == after,
            "s2_shadow_assessment": s2_record,
            "technical_pass": (
                s2_record.get("evaluation_status") == "evaluated" and
                s2_record.get("promotion_authorized") is False and
                before == after
            ),
            "semantic_match": (
                s2_record.get("evaluation_status") == "evaluated" and
                observed == case["gold"]
            ),
        })
        if s2_record.get("evaluation_status") != "evaluated":
            report["stopped_early"] = True
            break
        report["completed_evaluations"] += 1
    report["run_complete"] = (
        not report["stopped_early"] and
        report["attempted_evaluations"] == MAX_CASES and
        report["completed_evaluations"] == MAX_CASES and
        len(report["cases"]) == MAX_CASES
    )
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


def report_exit_code(report):
    return 0 if isinstance(report, dict) and report.get("run_complete") is True else 2


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
    if args.timeout != 180 or args.max_tokens != 1024:
        parser.error("approved runtime limits must remain 180/1024")
    if not args.fixtures.is_file():
        parser.error("fixture file missing")
    if not args.output.parent.is_dir() or args.output.exists() or args.output.is_symlink():
        parser.error("output parent missing or output already exists")
    import shadow_nli_spatial_relations_v1_inference as spatial_nli
    root = Path(__file__).resolve().parents[1]
    fixture, cases, identities = load_inputs(root, args.fixtures.resolve())
    contract_descriptor = spatial_nli.descriptor()
    runtime_config = {
        "judge": "shadow_nli_spatial_relations_v1_inference.judge_pair",
        "model": args.model,
        "ollama_url": args.ollama_url,
        "timeout_seconds_per_call": args.timeout,
        "max_tokens": args.max_tokens,
        "temperature": 0,
        "num_ctx": 4096,
        "think": False,
        "retry": False,
        "repair": False,
    }
    def call(claim, evidence):
        return spatial_nli.judge_pair(
            claim, evidence, model=args.model, ollama_url=args.ollama_url,
            timeout=args.timeout, max_tokens=args.max_tokens)
    bridge = spatial_bridge.build_bridge(
        call, runtime_config, contract_descriptor)
    report = execute_cases(
        fixture, cases, identities, bridge, bridge.judge_descriptor,
        runtime_config, contract_descriptor)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    raise SystemExit(report_exit_code(report))


if __name__ == "__main__":
    main()
