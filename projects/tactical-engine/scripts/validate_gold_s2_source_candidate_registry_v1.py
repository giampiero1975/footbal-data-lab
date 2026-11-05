#!/usr/bin/env python3
"""Deterministic, offline validator for the Gold S2 candidate registry.

This module validates declarations and referenced evidence.  It does not acquire
sources, interpret licences, or decide whether a legal permission is sufficient.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "gold_s2_source_candidate_registry_v1"
ELIGIBILITY = {
    "eligible_development", "eligible_calibration", "eligible_holdout",
    "eligible_adversarial", "ineligible", "blocked_unknown",
}
SPLIT_FOR_DECISION = {
    "eligible_development": "development",
    "eligible_calibration": "calibration",
    "eligible_holdout": "holdout",
    "eligible_adversarial": "adversarial",
}
SENSITIVE_SPLITS = {"calibration", "holdout", "adversarial"}
HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    unverifiable: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("ROOT_NOT_OBJECT")
    return value


def _object(report: ValidationReport, value: Any, required: set[str], optional: set[str], path: str) -> bool:
    if not isinstance(value, dict):
        report.errors.append(f"TYPE_OBJECT_REQUIRED:{path}")
        return False
    for name in sorted(required - set(value)):
        report.errors.append(f"MISSING_FIELD:{path}.{name}")
    for name in sorted(set(value) - required - optional):
        report.errors.append(f"UNEXPECTED_FIELD:{path}.{name}")
    return not (required - set(value))


def _array(report: ValidationReport, value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        report.errors.append(f"TYPE_ARRAY_REQUIRED:{path}")
        return []
    return value


def _text(report: ValidationReport, value: Any, path: str, nullable: bool = False) -> bool:
    if nullable and value is None:
        return True
    if not isinstance(value, str) or not value.strip():
        report.errors.append(f"NONEMPTY_STRING_REQUIRED:{path}")
        return False
    return True


def _enum(report: ValidationReport, value: Any, allowed: set[Any], path: str) -> bool:
    if not isinstance(value, (str, type(None))) or value not in allowed:
        report.errors.append(f"ENUM_INVALID:{path}")
        return False
    return True


def _hash(report: ValidationReport, value: Any, path: str, nullable: bool = False) -> bool:
    if nullable and value is None:
        return True
    if not isinstance(value, str) or HASH_RE.fullmatch(value) is None:
        report.errors.append(f"SHA256_INVALID:{path}")
        return False
    return True


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    repeated: set[str] = set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return repeated


def _evidence_refs(report: ValidationReport, refs: Any, evidence: dict[str, dict[str, Any]], path: str, require: bool = False) -> list[str]:
    items = _array(report, refs, path)
    valid: list[str] = []
    if require and not items:
        report.errors.append(f"EVIDENCE_REQUIRED:{path}")
    for index, ref in enumerate(items):
        if not _text(report, ref, f"{path}[{index}]"):
            continue
        valid.append(ref)
        if ref not in evidence:
            report.errors.append(f"EVIDENCE_REF_UNRESOLVED:{path}[{index}]:{ref}")
    return valid


def _validate_policy(report: ValidationReport, value: Any) -> dict[str, Any]:
    required = {"approval_status", "known_corpus_exclusion", "known_web_exclusion", "author_disjoint_policy", "rights_custodian_id", "retention_policy_approved", "publication_policy_approved", "acquisition_authorized"}
    if not _object(report, value, required, set(), "policy"):
        return value if isinstance(value, dict) else {}
    _enum(report, value.get("approval_status"), {"approved", "not_approved"}, "policy.approval_status")
    for name in ("known_corpus_exclusion", "known_web_exclusion"):
        _enum(report, value.get(name), {"approved", "not_approved", "unknown"}, f"policy.{name}")
    _enum(report, value.get("author_disjoint_policy"), {"absolute", "stratified", "not_approved"}, "policy.author_disjoint_policy")
    _text(report, value.get("rights_custodian_id"), "policy.rights_custodian_id", nullable=True)
    for name in ("retention_policy_approved", "publication_policy_approved", "acquisition_authorized"):
        if not isinstance(value.get(name), bool):
            report.errors.append(f"TYPE_BOOLEAN_REQUIRED:policy.{name}")
    return value


def _validate_evidence(report: ValidationReport, records: Any) -> dict[str, dict[str, Any]]:
    required = {"evidence_id", "evidence_type", "digest", "verified", "reviewer_id", "verified_at"}
    result: dict[str, dict[str, Any]] = {}
    ids: list[str] = []
    for index, item in enumerate(_array(report, records, "evidence_records")):
        path = f"evidence_records[{index}]"
        if not _object(report, item, required, set(), path):
            continue
        evidence_id = item.get("evidence_id")
        if _text(report, evidence_id, f"{path}.evidence_id"):
            ids.append(evidence_id)
            result.setdefault(evidence_id, item)
        _enum(report, item.get("evidence_type"), {"identity", "provenance", "digest", "rights", "retention", "exposure", "independence", "decision"}, f"{path}.evidence_type")
        _hash(report, item.get("digest"), f"{path}.digest")
        if not isinstance(item.get("verified"), bool):
            report.errors.append(f"TYPE_BOOLEAN_REQUIRED:{path}.verified")
        _text(report, item.get("reviewer_id"), f"{path}.reviewer_id", nullable=True)
        _text(report, item.get("verified_at"), f"{path}.verified_at", nullable=True)
        if item.get("verified") and (not item.get("reviewer_id") or not item.get("verified_at")):
            report.errors.append(f"VERIFIED_EVIDENCE_ATTRIBUTION_REQUIRED:{path}")
    for duplicate in sorted(_duplicates(ids)):
        report.errors.append(f"DUPLICATE_EVIDENCE_ID:{duplicate}")
    return result


def _candidate_shape(report: ValidationReport, item: Any, path: str) -> bool:
    required = {"candidate_id", "source_id", "title", "author", "organization", "version", "provenance", "digest", "rights_evidence", "retention_policy", "annotation_permission", "publication_permission", "historical_exposure", "independence", "duplicate_cluster", "author_cluster", "proposed_split", "eligibility_decision", "evidence_refs", "reviewer", "decision_date", "decision_rationale", "gold_s2_provenance_record_id"}
    return _object(report, item, required, set(), path)


def _validate_candidate(report: ValidationReport, item: dict[str, Any], path: str, evidence: dict[str, dict[str, Any]], policy: dict[str, Any]) -> None:
    for name in ("candidate_id", "source_id", "title"):
        _text(report, item.get(name), f"{path}.{name}")
    authors = _array(report, item.get("author"), f"{path}.author")
    if not authors:
        report.errors.append(f"AUTHOR_REQUIRED:{path}")
    for index, author in enumerate(authors):
        apath = f"{path}.author[{index}]"
        if _object(report, author, {"name", "authority_id"}, set(), apath):
            _text(report, author.get("name"), f"{apath}.name")
            _text(report, author.get("authority_id"), f"{apath}.authority_id", nullable=True)
    organization = item.get("organization")
    if _object(report, organization, {"name", "authority_id"}, set(), f"{path}.organization"):
        _text(report, organization.get("name"), f"{path}.organization.name")
        _text(report, organization.get("authority_id"), f"{path}.organization.authority_id", nullable=True)
    version = item.get("version")
    if _object(report, version, {"edition", "date", "language", "document_id", "version_id"}, set(), f"{path}.version"):
        for name in ("edition", "date", "language", "document_id", "version_id"):
            _text(report, version.get(name), f"{path}.version.{name}")

    provenance = item.get("provenance")
    if _object(report, provenance, {"channel", "origin_ref", "chain_status", "evidence_refs"}, set(), f"{path}.provenance"):
        _text(report, provenance.get("channel"), f"{path}.provenance.channel")
        _text(report, provenance.get("origin_ref"), f"{path}.provenance.origin_ref")
        _enum(report, provenance.get("chain_status"), {"verified", "unknown"}, f"{path}.provenance.chain_status")
        _evidence_refs(report, provenance.get("evidence_refs"), evidence, f"{path}.provenance.evidence_refs", True)

    digest = item.get("digest")
    if _object(report, digest, {"algorithm", "value", "verification_status", "evidence_ref"}, set(), f"{path}.digest"):
        if digest.get("algorithm") != "sha256":
            report.errors.append(f"DIGEST_ALGORITHM_INVALID:{path}")
        _hash(report, digest.get("value"), f"{path}.digest.value", nullable=True)
        _enum(report, digest.get("verification_status"), {"verified_bytes", "declared_only", "unknown"}, f"{path}.digest.verification_status")
        ref = digest.get("evidence_ref")
        _text(report, ref, f"{path}.digest.evidence_ref", nullable=True)
        if ref is not None and ref not in evidence:
            report.errors.append(f"EVIDENCE_REF_UNRESOLVED:{path}.digest.evidence_ref:{ref}")
        if digest.get("verification_status") == "verified_bytes":
            if digest.get("value") is None or ref is None or not evidence.get(ref, {}).get("verified"):
                report.errors.append(f"DIGEST_VERIFICATION_EVIDENCE_REQUIRED:{path}")
        elif digest.get("value") is not None:
            report.unverifiable.append(f"DIGEST_NOT_BYTE_VERIFIED:{item.get('candidate_id', path)}")

    rights = _array(report, item.get("rights_evidence"), f"{path}.rights_evidence")
    scopes: dict[str, str] = {}
    for index, right in enumerate(rights):
        rpath = f"{path}.rights_evidence[{index}]"
        if not _object(report, right, {"evidence_id", "scope", "status", "expires_at", "revoked_at", "reviewer_id"}, set(), rpath):
            continue
        ref = right.get("evidence_id")
        _text(report, ref, f"{rpath}.evidence_id")
        if isinstance(ref, str) and ref not in evidence:
            report.errors.append(f"EVIDENCE_REF_UNRESOLVED:{rpath}.evidence_id:{ref}")
        scope = right.get("scope")
        status = right.get("status")
        _enum(report, scope, {"retention", "annotation", "publication"}, f"{rpath}.scope")
        _enum(report, status, {"verified", "denied", "expired", "revoked", "unknown"}, f"{rpath}.status")
        _text(report, right.get("reviewer_id"), f"{rpath}.reviewer_id", nullable=True)
        _text(report, right.get("expires_at"), f"{rpath}.expires_at", nullable=True)
        _text(report, right.get("revoked_at"), f"{rpath}.revoked_at", nullable=True)
        if isinstance(scope, str):
            if scope in scopes:
                report.errors.append(f"DUPLICATE_RIGHTS_SCOPE:{path}:{scope}")
            scopes[scope] = status
        if status == "verified" and (not right.get("reviewer_id") or not evidence.get(ref, {}).get("verified")):
            report.errors.append(f"RIGHTS_VERIFICATION_ATTRIBUTION_REQUIRED:{rpath}")

    retention = item.get("retention_policy")
    if _object(report, retention, {"policy_id", "status", "evidence_refs"}, set(), f"{path}.retention_policy"):
        _text(report, retention.get("policy_id"), f"{path}.retention_policy.policy_id", nullable=True)
        _enum(report, retention.get("status"), {"verified", "denied", "unknown"}, f"{path}.retention_policy.status")
        _evidence_refs(report, retention.get("evidence_refs"), evidence, f"{path}.retention_policy.evidence_refs")
    _enum(report, item.get("annotation_permission"), {"verified", "denied", "unknown"}, f"{path}.annotation_permission")
    _enum(report, item.get("publication_permission"), {"verified", "denied", "unknown"}, f"{path}.publication_permission")

    exposure = _array(report, item.get("historical_exposure"), f"{path}.historical_exposure")
    if not exposure:
        report.unverifiable.append(f"EXPOSURE_LEDGER_EMPTY:{item.get('candidate_id', path)}")
    exposure_statuses: list[str] = []
    for index, entry in enumerate(exposure):
        epath = f"{path}.historical_exposure[{index}]"
        if not _object(report, entry, {"system", "dataset", "status", "evidence_refs"}, set(), epath):
            continue
        _text(report, entry.get("system"), f"{epath}.system")
        _text(report, entry.get("dataset"), f"{epath}.dataset")
        if _enum(report, entry.get("status"), {"verified_exposed", "verified_absent", "unknown"}, f"{epath}.status"):
            exposure_statuses.append(entry["status"])
        _evidence_refs(report, entry.get("evidence_refs"), evidence, f"{epath}.evidence_refs", True)

    independence = item.get("independence")
    independence_values: dict[str, Any] = {}
    if _object(report, independence, {"source_disjoint", "document_disjoint", "version_disjoint", "author_disjoint", "evidence_refs"}, set(), f"{path}.independence"):
        for name in ("source_disjoint", "document_disjoint", "version_disjoint"):
            _enum(report, independence.get(name), {"pass", "fail", "unknown"}, f"{path}.independence.{name}")
        _enum(report, independence.get("author_disjoint"), {"pass", "fail", "unknown", "not_applicable"}, f"{path}.independence.author_disjoint")
        _evidence_refs(report, independence.get("evidence_refs"), evidence, f"{path}.independence.evidence_refs")
        independence_values = independence
    for name in ("duplicate_cluster", "author_cluster", "reviewer", "decision_date", "decision_rationale", "gold_s2_provenance_record_id"):
        _text(report, item.get(name), f"{path}.{name}", nullable=True)
    proposed_split = item.get("proposed_split")
    _enum(report, proposed_split, {"development", "calibration", "holdout", "adversarial", None}, f"{path}.proposed_split")
    decision = item.get("eligibility_decision")
    _enum(report, decision, ELIGIBILITY, f"{path}.eligibility_decision")
    decision_refs = _evidence_refs(report, item.get("evidence_refs"), evidence, f"{path}.evidence_refs")

    if decision in SPLIT_FOR_DECISION:
        expected_split = SPLIT_FOR_DECISION[decision]
        if proposed_split != expected_split:
            report.errors.append(f"ELIGIBILITY_SPLIT_MISMATCH:{path}")
        if policy.get("approval_status") != "approved" or not policy.get("acquisition_authorized"):
            report.errors.append(f"POLICY_NOT_APPROVED_FOR_PROMOTION:{path}")
        if not policy.get("rights_custodian_id") or not policy.get("retention_policy_approved") or not policy.get("publication_policy_approved"):
            report.errors.append(f"POLICY_PREREQUISITES_MISSING:{path}")
        if provenance.get("chain_status") != "verified" if isinstance(provenance, dict) else True:
            report.errors.append(f"PROVENANCE_NOT_VERIFIED:{path}")
        if not isinstance(digest, dict) or digest.get("verification_status") != "verified_bytes":
            report.errors.append(f"DIGEST_NOT_VERIFIED:{path}")
        if any(scopes.get(scope) != "verified" for scope in ("retention", "annotation", "publication")):
            report.errors.append(f"RIGHTS_SCOPES_NOT_VERIFIED:{path}")
        if not isinstance(retention, dict) or retention.get("status") != "verified":
            report.errors.append(f"RETENTION_NOT_VERIFIED:{path}")
        if item.get("annotation_permission") != "verified" or item.get("publication_permission") != "verified":
            report.errors.append(f"PERMISSIONS_NOT_VERIFIED:{path}")
        if not item.get("reviewer") or not item.get("decision_date") or not item.get("decision_rationale") or not decision_refs:
            report.errors.append(f"DECISION_ATTRIBUTION_REQUIRED:{path}")
        if not independence_values or any(independence_values.get(name) != "pass" for name in ("source_disjoint", "document_disjoint", "version_disjoint")):
            report.errors.append(f"INDEPENDENCE_NOT_VERIFIED:{path}")
        if expected_split in SENSITIVE_SPLITS:
            if not exposure or any(status != "verified_absent" for status in exposure_statuses):
                report.errors.append(f"EXPOSURE_NOT_CLEARED:{path}")
            if policy.get("author_disjoint_policy") == "not_approved":
                report.errors.append(f"AUTHOR_POLICY_NOT_APPROVED:{path}")
            elif independence_values.get("author_disjoint") not in {"pass", "not_applicable"}:
                report.errors.append(f"AUTHOR_INDEPENDENCE_NOT_VERIFIED:{path}")
            if policy.get("known_corpus_exclusion") != "approved" or policy.get("known_web_exclusion") != "approved":
                report.errors.append(f"KNOWN_SOURCE_EXCLUSION_NOT_APPROVED:{path}")
        if item.get("gold_s2_provenance_record_id") is None:
            report.unverifiable.append(f"FUTURE_GOLD_LINK_NOT_ASSIGNED:{item.get('candidate_id', path)}")
    elif decision in {"ineligible", "blocked_unknown"}:
        if not item.get("reviewer") or not item.get("decision_date") or not item.get("decision_rationale") or not decision_refs:
            report.errors.append(f"DECISION_ATTRIBUTION_REQUIRED:{path}")


def validate_registry(registry: dict[str, Any]) -> ValidationReport:
    report = ValidationReport()
    required = {"schema_version", "registry_version", "status", "policy", "evidence_records", "candidates"}
    if not _object(report, registry, required, set(), "registry"):
        return report
    if registry.get("schema_version") != SCHEMA_VERSION:
        report.errors.append("SCHEMA_VERSION_INCOMPATIBLE")
    _text(report, registry.get("registry_version"), "registry.registry_version")
    if registry.get("status") != "draft":
        report.errors.append("REGISTRY_STATUS_INVALID")
    policy = _validate_policy(report, registry.get("policy"))
    evidence = _validate_evidence(report, registry.get("evidence_records"))
    candidates = _array(report, registry.get("candidates"), "candidates")
    ids: dict[str, list[str]] = {"candidate_id": [], "source_id": [], "document_id": [], "version_id": []}
    cluster_splits: dict[str, set[str]] = {}
    author_splits: dict[str, set[str]] = {}
    for index, item in enumerate(candidates):
        path = f"candidates[{index}]"
        if not _candidate_shape(report, item, path):
            continue
        _validate_candidate(report, item, path, evidence, policy)
        for name in ("candidate_id", "source_id"):
            if isinstance(item.get(name), str) and item[name]:
                ids[name].append(item[name])
        version = item.get("version")
        if isinstance(version, dict):
            for name in ("document_id", "version_id"):
                if isinstance(version.get(name), str) and version[name]:
                    ids[name].append(version[name])
        split = item.get("proposed_split")
        cluster = item.get("duplicate_cluster")
        author_cluster = item.get("author_cluster")
        if isinstance(split, str) and isinstance(cluster, str):
            cluster_splits.setdefault(cluster, set()).add(split)
        if isinstance(split, str) and isinstance(author_cluster, str):
            author_splits.setdefault(author_cluster, set()).add(split)
    for name, values in ids.items():
        for duplicate in sorted(_duplicates(values)):
            report.errors.append(f"DUPLICATE_{name.upper()}:{duplicate}")
    for cluster, splits in sorted(cluster_splits.items()):
        if len(splits) > 1:
            report.errors.append(f"DUPLICATE_CLUSTER_SPLIT_CONFLICT:{cluster}")
    if policy.get("author_disjoint_policy") == "absolute":
        for cluster, splits in sorted(author_splits.items()):
            if len(splits) > 1:
                report.errors.append(f"AUTHOR_CLUSTER_SPLIT_CONFLICT:{cluster}")
    return report


def validate_repository_contracts(root: Path) -> ValidationReport:
    report = ValidationReport()
    base = root / "evaluation" / "annotations"
    for name in ("gold_s2_source_candidate_registry_schema_v1.json", "gold_s2_source_candidate_registry_template_v1.json"):
        try:
            load_json(base / name)
        except Exception as exc:
            report.errors.append(f"REPOSITORY_ARTIFACT_INVALID:{name}:{type(exc).__name__}")
    if report.errors:
        return report
    return validate_registry(load_json(base / "gold_s2_source_candidate_registry_template_v1.json"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = validate_registry(load_json(args.registry)) if args.registry else validate_repository_contracts(args.repository_root)
    print("STATUS", "VALID" if report.passed else "INVALID")
    print("ERRORS", len(report.errors))
    print("UNVERIFIABLE", len(report.unverifiable))
    for item in report.errors:
        print("ERROR", item)
    for item in report.unverifiable:
        print("UNVERIFIABLE_ITEM", item)
    raise SystemExit(0 if report.passed else 2)


if __name__ == "__main__":
    main()
