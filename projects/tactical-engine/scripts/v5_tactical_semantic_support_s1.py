#!/usr/bin/env python3
"""Deterministic S1 support for exact, continuous, atomic documentary claims."""
from __future__ import annotations

import hashlib
import json
import unicodedata


SCHEMA = "tactical_documentary_support_assessment_v1"
VERSION = "1.0"
ASSESSOR_NAME = "s1_exact_atomic"
ASSESSOR_VERSION = "1.0"
REASON_SUPPORTED = "exact_atomic_statement"
ALLOWED_ASSESSORS = {("deterministic", ASSESSOR_NAME, ASSESSOR_VERSION)}
CONFIG = {
    "normalization": ["NFC", "CRLF_TO_LF", "CR_TO_LF"],
    "span_units": "unicode_code_points_on_normalized_section",
    "span_interval": "half_open",
    "supported_class": "single_continuous_exact_anchor_equal_to_evidence_unit",
    "negative_rules": [],
}


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def normalize_text(value):
    if not isinstance(value, str):
        return None
    return unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n")


def digest_text(value):
    normalized = normalize_text(value)
    if normalized is None:
        raise TypeError("text must be a string")
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _safe_digest(value):
    return digest_text(value) if isinstance(value, str) else None


def config_fingerprint():
    return "sha256:" + hashlib.sha256(canonical_json(CONFIG).encode("utf-8")).hexdigest()


def _assessment(attempt_id, plan_fingerprint, claim, evidence_rows, verdict, reasons):
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "attempt_id": attempt_id,
        "plan_fingerprint": plan_fingerprint,
        "claim_id": claim.get("claim_id"),
        "statement_sha256": _safe_digest(claim.get("statement")),
        "evidence": evidence_rows,
        "aggregate_verdict": verdict,
        "reason_codes": list(dict.fromkeys(reasons)),
        "assessor": {"kind": "deterministic", "name": ASSESSOR_NAME,
                     "version": ASSESSOR_VERSION,
                     "config_sha256": config_fingerprint()},
    }


def assess_claim(attempt_id, plan_fingerprint, claim, evidence_by_id):
    """Assess only the exact-anchor class; all other classes are not_evaluable."""
    statement = normalize_text(claim.get("statement")) if isinstance(claim, dict) else None
    refs = claim.get("evidence_refs") if isinstance(claim, dict) else None
    anchors = claim.get("evidence_anchors") if isinstance(claim, dict) else None
    mode = claim.get("support_mode") if isinstance(claim, dict) else None
    reasons, rows = [], []
    if (not isinstance(attempt_id, str) or not attempt_id or
            not isinstance(plan_fingerprint, str) or not plan_fingerprint.startswith("sha256:")):
        reasons.append("invalid_assessment_identity")
    if not statement:
        reasons.append("invalid_atomic_statement")
    if mode != "direct":
        reasons.append("support_mode_outside_s1")
    if not isinstance(refs, list) or len(refs) != 1 or not all(isinstance(x, str) for x in refs):
        reasons.append("non_atomic_evidence_set")
        refs = []
    if not isinstance(anchors, list) or len(anchors) != 1 or not isinstance(anchors[0], dict):
        reasons.append("non_atomic_anchor_set")
        anchors = []
    if anchors and refs:
        anchor = anchors[0]
        if set(anchor) != {"evidence_ref", "exact_text"} or anchor.get("evidence_ref") != refs[0]:
            reasons.append("anchor_reference_mismatch")
        evidence = evidence_by_id.get(refs[0])
        exact = normalize_text(anchor.get("exact_text"))
        evidence_text = normalize_text((evidence or {}).get("text"))
        evidence_digest = _safe_digest((evidence or {}).get("text"))
        verdict = "not_evaluable"
        row_reasons = []
        if evidence is None:
            row_reasons.append("evidence_not_found")
        elif not exact or exact not in evidence_text:
            row_reasons.append("anchor_not_found")
        elif statement != exact:
            row_reasons.append("statement_not_exact_anchor")
        elif exact != evidence_text:
            # S1 has no independent condition/quantifier extractor. Requiring the
            # whole normalized evidence unit prevents promotion of a context-free
            # substring that may have omitted a governing condition or quantifier.
            row_reasons.append("evidence_scope_exceeds_atomic_statement")
        elif reasons:
            row_reasons.extend(reasons)
        else:
            verdict = "supported"
            row_reasons.append(REASON_SUPPORTED)
        rows.append({"evidence_ref": refs[0], "evidence_sha256": evidence_digest,
                     "verdict": verdict, "reason_codes": list(dict.fromkeys(row_reasons))})
        reasons.extend(row_reasons)
    else:
        for ref in refs:
            evidence = evidence_by_id.get(ref)
            rows.append({"evidence_ref": ref,
                         "evidence_sha256": _safe_digest((evidence or {}).get("text")),
                         "verdict": "not_evaluable", "reason_codes": reasons[:]})
    aggregate = "supported" if rows and all(row["verdict"] == "supported" for row in rows) else "not_evaluable"
    return _assessment(attempt_id, plan_fingerprint, claim, rows, aggregate, reasons)


def verify_assessment(record, attempt_id, plan_fingerprint, claim, evidence_by_id):
    """Verify provenance and all content addresses before an assessment is consumed."""
    errors = []
    required = {"schema", "version", "attempt_id", "plan_fingerprint", "claim_id",
                "statement_sha256", "evidence", "aggregate_verdict", "reason_codes", "assessor"}
    if not isinstance(record, dict) or set(record) != required:
        return ["invalid_support_assessment_shape"]
    if record.get("schema") != SCHEMA or record.get("version") != VERSION:
        errors.append("invalid_support_assessment_identity")
    if record.get("attempt_id") != attempt_id:
        errors.append("support_assessment_attempt_mismatch")
    if record.get("plan_fingerprint") != plan_fingerprint:
        errors.append("support_assessment_plan_mismatch")
    if record.get("claim_id") != claim.get("claim_id"):
        errors.append("support_assessment_claim_mismatch")
    if record.get("statement_sha256") != _safe_digest(claim.get("statement")):
        errors.append("support_assessment_statement_digest_mismatch")
    assessor = record.get("assessor")
    if (not isinstance(assessor, dict) or set(assessor) != {"kind", "name", "version", "config_sha256"} or
            (assessor.get("kind"), assessor.get("name"), assessor.get("version")) not in ALLOWED_ASSESSORS or
            assessor.get("config_sha256") != config_fingerprint()):
        errors.append("support_assessor_not_authorized")
    evidence_rows = record.get("evidence")
    if not isinstance(evidence_rows, list):
        errors.append("invalid_support_evidence_rows")
    else:
        seen = set()
        for row in evidence_rows:
            if not isinstance(row, dict) or set(row) != {"evidence_ref", "evidence_sha256", "verdict", "reason_codes"}:
                errors.append("invalid_support_evidence_row")
                continue
            ref = row.get("evidence_ref")
            if ref in seen:
                errors.append("duplicate_support_evidence_ref")
            seen.add(ref)
            evidence = evidence_by_id.get(ref)
            if evidence is None or row.get("evidence_sha256") != _safe_digest(evidence.get("text")):
                errors.append("support_evidence_digest_mismatch")
            if row.get("verdict") not in {"supported", "unsupported", "not_evaluable"}:
                errors.append("invalid_support_evidence_verdict")
    if record.get("aggregate_verdict") not in {"supported", "unsupported", "not_evaluable"}:
        errors.append("invalid_support_aggregate_verdict")
    if not isinstance(record.get("reason_codes"), list) or not all(
            isinstance(item, str) and item for item in record["reason_codes"]):
        errors.append("invalid_support_reason_codes")
    expected = assess_claim(attempt_id, plan_fingerprint, claim, evidence_by_id)
    if canonical_json(record) != canonical_json(expected):
        errors.append("support_assessment_content_mismatch")
    return list(dict.fromkeys(errors))
