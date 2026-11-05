#!/usr/bin/env python3
"""Content-addressed D3 to S2 shadow adapter with an injected semantic judge.

The adapter never starts a model, never changes S1 and never authorizes promotion.
"""
from __future__ import annotations

import hashlib
import json
import re

import v5_tactical_semantic_support_s1 as semantic_support_s1


SCHEMA = "tactical_documentary_semantic_support_shadow_v1"
VERSION = "1.0"
MODE = "shadow_only"
LABELS = {"supported", "contradicted", "insufficient"}
HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_document(value):
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _judge_identity(descriptor):
    if not isinstance(descriptor, dict) or set(descriptor) != {"kind", "name", "version", "config"}:
        return None
    if descriptor.get("kind") != "injected" or not all(
            isinstance(descriptor.get(key), str) and descriptor[key]
            for key in ("name", "version")) or not isinstance(descriptor.get("config"), dict):
        return None
    return {
        "kind": "injected",
        "name": descriptor["name"],
        "version": descriptor["version"],
        "config_sha256": digest_document(descriptor["config"]),
    }


def _base(attempt_id, plan_fingerprint, claim, s1_assessment, descriptor):
    statement = claim.get("statement") if isinstance(claim, dict) else None
    record = {
        "schema": SCHEMA,
        "version": VERSION,
        "mode": MODE,
        "promotion_authorized": False,
        "attempt_id": attempt_id,
        "plan_fingerprint": plan_fingerprint,
        "claim_id": claim.get("claim_id") if isinstance(claim, dict) else None,
        "statement_sha256": semantic_support_s1._safe_digest(statement),
        "s1_assessment_sha256": digest_document(s1_assessment) if isinstance(s1_assessment, dict) else None,
        "judge": _judge_identity(descriptor),
        "evidence": [],
        "evaluation_status": "not_evaluable",
        "aggregate_verdict": "not_evaluable",
        "reason_codes": [],
        "record_sha256": None,
    }
    return record


def _finish(record, status, verdict, reasons):
    record["evaluation_status"] = status
    record["aggregate_verdict"] = verdict
    record["reason_codes"] = list(dict.fromkeys(reasons))
    payload = dict(record)
    payload["record_sha256"] = None
    record["record_sha256"] = digest_document(payload)
    return record


def _binding_errors(claim, authoritative_bindings):
    errors = []
    relations = claim.get("relation_refs") if isinstance(claim, dict) else None
    bindings = claim.get("bindings") if isinstance(claim, dict) else None
    dimensions = claim.get("dimensions") if isinstance(claim, dict) else None
    if not isinstance(relations, list) or not relations or not all(isinstance(item, str) for item in relations):
        return ["invalid_relation_refs"]
    if not isinstance(bindings, dict) or not isinstance(dimensions, list):
        return ["invalid_claim_bindings"]
    for relation_id in relations:
        expected = authoritative_bindings.get(relation_id)
        if not isinstance(expected, dict):
            errors.append("authoritative_relation_missing")
            continue
        for dimension in set(dimensions) - {"detail"}:
            if dimension not in {"actor", "task", "space", "trigger", "purpose", "phase"}:
                errors.append("invalid_claim_dimension")
            elif bindings.get(dimension) != expected.get(dimension):
                errors.append("claim_bindings_not_authoritative")
    return errors


def assess_claim(attempt_id, plan_fingerprint, claim, evidence_by_id, s1_assessment,
                 authoritative_bindings, judge, judge_descriptor):
    """Produce a non-authoritative shadow record; every uncertainty fails closed."""
    record = _base(attempt_id, plan_fingerprint, claim, s1_assessment, judge_descriptor)
    reasons = []
    if not isinstance(attempt_id, str) or not attempt_id:
        reasons.append("invalid_attempt_id")
    if not isinstance(plan_fingerprint, str) or HASH_RE.fullmatch(plan_fingerprint) is None:
        reasons.append("invalid_plan_fingerprint")
    if not isinstance(claim, dict) or not isinstance(claim.get("statement"), str) or not claim["statement"]:
        reasons.append("invalid_claim")
    if not isinstance(evidence_by_id, dict):
        reasons.append("invalid_evidence_map")
        evidence_by_id = {}
    if not isinstance(authoritative_bindings, dict):
        reasons.append("invalid_authoritative_bindings")
        authoritative_bindings = {}
    if not callable(judge):
        reasons.append("invalid_injected_judge")
    if record["judge"] is None:
        reasons.append("invalid_judge_descriptor")
    if isinstance(claim, dict) and isinstance(s1_assessment, dict):
        reasons.extend(semantic_support_s1.verify_assessment(
            s1_assessment, attempt_id, plan_fingerprint, claim, evidence_by_id))
    else:
        reasons.append("missing_s1_assessment")
    if isinstance(claim, dict):
        reasons.extend(_binding_errors(claim, authoritative_bindings))
    refs = claim.get("evidence_refs") if isinstance(claim, dict) else None
    if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref for ref in refs):
        reasons.append("invalid_evidence_refs")
        refs = []
    elif len(refs) != len(set(refs)):
        reasons.append("duplicate_evidence_refs")
    for ref in refs:
        evidence = evidence_by_id.get(ref)
        if not isinstance(evidence, dict) or not isinstance(evidence.get("text"), str):
            reasons.append("evidence_not_found_or_invalid")
            continue
        record["evidence"].append({
            "evidence_ref": ref,
            "evidence_sha256": semantic_support_s1.digest_text(evidence["text"]),
            "judge_label": None,
            "judge_rationale": None,
            "status": "not_evaluable",
            "reason_codes": [],
        })
    if reasons:
        return _finish(record, "not_evaluable", "not_evaluable", reasons)

    failed = False
    for row in record["evidence"]:
        evidence = evidence_by_id[row["evidence_ref"]]
        try:
            verdict = judge({
                "claim_id": claim["claim_id"],
                "statement": claim["statement"],
                "conditions": claim.get("conditions", []),
                "polarity": claim.get("polarity"),
                "bindings": claim.get("bindings", {}),
                "evidence_ref": row["evidence_ref"],
                "evidence": evidence["text"],
            })
        except Exception as exc:  # injected boundary must never escape
            row["reason_codes"] = ["judge_error:" + type(exc).__name__]
            failed = True
            continue
        if (not isinstance(verdict, dict) or set(verdict) != {"label", "rationale"} or
                verdict.get("label") not in LABELS or
                not isinstance(verdict.get("rationale"), str) or not verdict["rationale"].strip()):
            row["reason_codes"] = ["malformed_judge_result"]
            failed = True
            continue
        row.update(judge_label=verdict["label"], judge_rationale=verdict["rationale"],
                   status="evaluated", reason_codes=[])
    if failed:
        return _finish(record, "not_evaluable", "not_evaluable", [
            code for row in record["evidence"] for code in row["reason_codes"]])

    labels = {row["judge_label"] for row in record["evidence"]}
    if labels == {"supported"}:
        aggregate = "supported"
    elif labels == {"contradicted"}:
        aggregate = "contradicted"
    elif "supported" in labels and "contradicted" in labels:
        aggregate = "conflicting"
    else:
        aggregate = "insufficient"
    reason = "conflicting_evidence_no_majority" if aggregate == "conflicting" else "shadow_judgement_complete"
    return _finish(record, "evaluated", aggregate, [reason])


def verify_assessment(record, attempt_id, plan_fingerprint, claim, evidence_by_id,
                      s1_assessment, authoritative_bindings, judge_descriptor):
    """Verify identity and content addresses without invoking the judge again."""
    errors = []
    required = {"schema", "version", "mode", "promotion_authorized", "attempt_id",
                "plan_fingerprint", "claim_id", "statement_sha256",
                "s1_assessment_sha256", "judge", "evidence", "evaluation_status",
                "aggregate_verdict", "reason_codes", "record_sha256"}
    if not isinstance(record, dict) or set(record) != required:
        return ["invalid_s2_shadow_assessment_shape"]
    if record.get("schema") != SCHEMA or record.get("version") != VERSION or record.get("mode") != MODE:
        errors.append("invalid_s2_shadow_assessment_identity")
    if record.get("promotion_authorized") is not False:
        errors.append("s2_shadow_promotion_forbidden")
    if record.get("attempt_id") != attempt_id or record.get("plan_fingerprint") != plan_fingerprint:
        errors.append("s2_shadow_provenance_mismatch")
    if record.get("claim_id") != claim.get("claim_id") or record.get("statement_sha256") != semantic_support_s1._safe_digest(claim.get("statement")):
        errors.append("s2_shadow_claim_mismatch")
    if record.get("s1_assessment_sha256") != digest_document(s1_assessment):
        errors.append("s2_shadow_s1_digest_mismatch")
    if record.get("judge") != _judge_identity(judge_descriptor):
        errors.append("s2_shadow_judge_mismatch")
    expected_rows = []
    for ref in claim.get("evidence_refs", []):
        evidence = evidence_by_id.get(ref)
        expected_rows.append((ref, semantic_support_s1._safe_digest((evidence or {}).get("text"))))
    observed = [(row.get("evidence_ref"), row.get("evidence_sha256"))
                for row in record.get("evidence", []) if isinstance(row, dict)]
    if observed != expected_rows:
        errors.append("s2_shadow_evidence_digest_mismatch")
    if _binding_errors(claim, authoritative_bindings):
        errors.append("s2_shadow_binding_mismatch")
    payload = dict(record)
    payload["record_sha256"] = None
    if record.get("record_sha256") != digest_document(payload):
        errors.append("s2_shadow_record_digest_mismatch")
    return list(dict.fromkeys(errors))
