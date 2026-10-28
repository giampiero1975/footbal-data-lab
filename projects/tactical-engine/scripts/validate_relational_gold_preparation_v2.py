#!/usr/bin/env python3
"""Offline validation for relational Gold E/Gold V v2 contracts.

The module is standard-library only.  It validates empty repository templates,
cross-artifact references in synthetic fixtures, freeze preconditions and a
restricted RFC 8785 profile.  It never runs the tactical engine or populates a
gold dataset.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ANNOTATIONS = Path(__file__).resolve().parents[1] / "evaluation" / "annotations"
SHA256_RE = "0123456789abcdef"
MAX_IJSON_INTEGER = 9007199254740991

V1_HASHES = {
    "evaluation/annotations/relational_gold_e_schema_v1.json": "79e6f4fc63936409a2cd1fc2d210dc80f2f97e4f7980cbc97f15a44872b03bf7",
    "evaluation/annotations/relational_gold_e_template_v1.json": "2b9ea4be5f7ef6ffafda6b87fb402f3ff9c76832e91ad78da2de2fe0d63af247",
    "evaluation/annotations/relational_gold_v_schema_v1.json": "d29495df218610dab66b4f55c7d240916226ef0cb407b0751b0edf55e89d9d96",
    "evaluation/annotations/relational_gold_v_template_v1.json": "a9850a6695ef0d589930d72fa6d55b1a36133de7c0ecf28fbbc84aa55d80d680",
    "evaluation/annotations/relational_gold_freeze_manifest_template_v1.json": "9669f11970aa64f29337cabc6587b1cf6d7181c21cb773a57a9d241989597c7e",
    "scripts/validate_relational_gold_preparation_v1.py": "e0673e3edf13d04c627ebe75250c4c2e1fcb6273863f7845bee85acef30d65cc",
    "tests/test_validate_relational_gold_preparation_v1.py": "345e9ee73b7b6f17be45b9b84ae9f80b8d3544a708e17fb04dc2e9d1eb303090",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def _valid_unicode(value: str) -> bool:
    return not any(0xD800 <= ord(char) <= 0xDFFF for char in value)


def _utf16_sort_key(value: str) -> bytes:
    if not _valid_unicode(value):
        raise ValueError("RFC8785_INVALID_UNICODE")
    return value.encode("utf-16-be")


def canonicalize_rfc8785(value: Any) -> bytes:
    """Canonicalize the I-JSON subset used by v2.

    RFC 8785 sorting and string serialization are implemented directly.
    Floats are deliberately rejected because the v2 contracts use integer
    durations and categorical confidence, avoiding cross-runtime number
    serialization ambiguity.
    """
    if value is None:
        return b"null"
    if value is True:
        return b"true"
    if value is False:
        return b"false"
    if isinstance(value, int):
        if abs(value) > MAX_IJSON_INTEGER:
            raise ValueError("RFC8785_INTEGER_OUT_OF_IJSON_RANGE")
        return str(value).encode("ascii")
    if isinstance(value, float):
        raise ValueError("RFC8785_FLOAT_NOT_ALLOWED_BY_GOLD_V2_PROFILE")
    if isinstance(value, str):
        if not _valid_unicode(value):
            raise ValueError("RFC8785_INVALID_UNICODE")
        return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if isinstance(value, list):
        return b"[" + b",".join(canonicalize_rfc8785(item) for item in value) + b"]"
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("RFC8785_OBJECT_KEYS_MUST_BE_STRINGS")
        items = []
        for key in sorted(value, key=_utf16_sort_key):
            items.append(canonicalize_rfc8785(key) + b":" + canonicalize_rfc8785(value[key]))
        return b"{" + b",".join(items) + b"}"
    raise ValueError(f"RFC8785_UNSUPPORTED_TYPE:{type(value).__name__}")


def sha256_document(value: Any) -> str:
    return hashlib.sha256(canonicalize_rfc8785(value)).hexdigest()


def normatively_order(value: Any) -> Any:
    """Return a copy with only set-like arrays sorted by their normative ID."""
    document = copy.deepcopy(value)

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            for child in node.values():
                visit(child)
            ordering = {
                "cases": "case_id",
                "requirements": "requirement_id",
                "request_parts": "request_part_id",
                "records": None,
                "dependencies": None,
                "expected_attempt_ids": None,
                "gold_e_requirement_ids": None,
                "evidence_ids": None,
            }
            for name, key in ordering.items():
                items = node.get(name)
                if not isinstance(items, list):
                    continue
                if name == "records":
                    candidate_keys = ("provenance_record_id", "adjudication_record_id")
                    items.sort(key=lambda item: next((str(item.get(k, "")) for k in candidate_keys if isinstance(item, dict) and k in item), ""))
                elif name == "dependencies":
                    items.sort(key=lambda item: (item.get("dependency_type", ""), item.get("artifact_version", ""), item.get("sha256", "")))
                elif key:
                    items.sort(key=lambda item: str(item.get(key, "")) if isinstance(item, dict) else str(item))
                else:
                    items.sort(key=str)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(document)
    return document


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    return {value for value in values if value in seen or seen.add(value)}


def _datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_provenance_registry(document: dict[str, Any], frozen: bool = False, as_of: str | None = None) -> list[str]:
    errors: list[str] = []
    records = document.get("records", [])
    ids = [item.get("provenance_record_id") for item in records if isinstance(item, dict)]
    if duplicate := _duplicates([item for item in ids if isinstance(item, str)]):
        errors.append(f"PROVENANCE_DUPLICATE_ID:{sorted(duplicate)[0]}")
    for record in records:
        record_id = record.get("provenance_record_id", "<missing>")
        rights = record.get("rights", {})
        evidence = rights.get("rights_evidence_ref", {})
        required = {"evidence_id", "evidence_version", "sha256", "access_class", "custodian", "availability_check"}
        if not required <= set(evidence):
            errors.append(f"RIGHTS_EVIDENCE_INCOMPLETE:{record_id}")
        if frozen:
            if rights.get("revocation_status") != "active":
                errors.append(f"PROVENANCE_NOT_ACTIVE:{record_id}")
            if as_of and rights.get("expires_at") and _datetime(rights["expires_at"]) <= _datetime(as_of):
                errors.append(f"PROVENANCE_EXPIRED:{record_id}")
            availability = evidence.get("availability_check", {})
            if availability.get("status") != "verified" or not availability.get("checked_at") or not availability.get("reviewer_id"):
                errors.append(f"RIGHTS_EVIDENCE_NOT_VERIFIED:{record_id}")
    return errors


def validate_annotation_ledger(document: dict[str, Any], frozen: bool = False) -> list[str]:
    errors: list[str] = []
    records = document.get("records", [])
    ids = [item.get("adjudication_record_id") for item in records if isinstance(item, dict)]
    if duplicate := _duplicates([item for item in ids if isinstance(item, str)]):
        errors.append(f"LEDGER_DUPLICATE_ID:{sorted(duplicate)[0]}")
    if frozen:
        for record in records:
            record_id = record.get("adjudication_record_id", "<missing>")
            required = {"case_id", "instruction_version", "annotated_object", "annotation_a", "annotation_b", "disagreements", "adjudication_c", "adjudication_rationale"}
            if not required <= set(record):
                errors.append(f"LEDGER_ADJUDICATION_INCOMPLETE:{record_id}")
                continue
            annotated = record.get("annotated_object", {})
            if not annotated.get("artifact_version") or not annotated.get("artifact_sha256"):
                errors.append(f"LEDGER_OBJECT_IDENTITY_INCOMPLETE:{record_id}")
            if record.get("annotation_a", {}).get("annotator_id") == record.get("annotation_b", {}).get("annotator_id"):
                errors.append(f"LEDGER_ANNOTATORS_NOT_INDEPENDENT:{record_id}")
            if not record.get("adjudication_rationale"):
                errors.append(f"LEDGER_RATIONALE_EMPTY:{record_id}")
    return errors


def validate_gold_e(document: dict[str, Any], provenance_ids: set[str], ledger: dict[str, dict[str, Any]], frozen: bool = False) -> list[str]:
    errors: list[str] = []
    cases = document.get("cases", [])
    case_ids = [case.get("case_id") for case in cases]
    if duplicate := _duplicates([item for item in case_ids if isinstance(item, str)]):
        errors.append(f"GOLD_E_DUPLICATE_CASE:{sorted(duplicate)[0]}")
    for case in cases:
        case_id = case.get("case_id", "<missing>")
        if case.get("provenance_record_id") not in provenance_ids:
            errors.append(f"GOLD_E_PROVENANCE_MISSING:{case_id}")
        part_ids = [part.get("request_part_id") for part in case.get("request_parts", [])]
        if duplicate := _duplicates([item for item in part_ids if isinstance(item, str)]):
            errors.append(f"GOLD_E_DUPLICATE_REQUEST_PART:{case_id}:{sorted(duplicate)[0]}")
        requirement_ids = [req.get("requirement_id") for req in case.get("requirements", [])]
        if duplicate := _duplicates([item for item in requirement_ids if isinstance(item, str)]):
            errors.append(f"GOLD_E_DUPLICATE_REQUIREMENT:{case_id}:{sorted(duplicate)[0]}")
        for requirement in case.get("requirements", []):
            if requirement.get("request_part_id") not in part_ids:
                errors.append(f"GOLD_E_REQUEST_PART_MISSING:{case_id}:{requirement.get('requirement_id')}")
        if frozen:
            ledger_id = case.get("adjudication_record_id")
            record = ledger.get(ledger_id)
            if not record or record.get("case_id") != case_id:
                errors.append(f"GOLD_E_LEDGER_MISSING:{case_id}")
            else:
                annotated = record.get("annotated_object", {})
                if annotated.get("artifact_type") != "gold_e_case" or annotated.get("artifact_version") != case.get("annotation_version") or annotated.get("artifact_sha256") != sha256_document(normatively_order(case)):
                    errors.append(f"GOLD_E_LEDGER_OBJECT_MISMATCH:{case_id}")
    return errors


def validate_gold_v(document: dict[str, Any], gold_e: dict[str, dict[str, Any]], ledger: dict[str, dict[str, Any]], frozen: bool = False) -> list[str]:
    errors: list[str] = []
    cases = document.get("cases", [])
    attempt_ids = [case.get("attempt_id") for case in cases]
    if duplicate := _duplicates([item for item in attempt_ids if isinstance(item, str)]):
        errors.append(f"GOLD_V_DUPLICATE_ATTEMPT:{sorted(duplicate)[0]}")
    expected = set(document.get("expected_attempt_ids", []))
    actual = {item for item in attempt_ids if isinstance(item, str)}
    if expected != actual:
        errors.append("GOLD_V_ATTEMPT_DENOMINATOR_MISMATCH")
    for case in cases:
        case_id = case.get("case_id", "<missing>")
        gold_e_case_id = case.get("gold_e_case_id")
        gold_case = gold_e.get(gold_e_case_id)
        if not gold_case:
            errors.append(f"GOLD_V_GOLD_E_CASE_MISSING:{case_id}")
            continue
        if case.get("input_reference", {}).get("gold_e_case_id") != gold_e_case_id:
            errors.append(f"GOLD_V_INPUT_CASE_MISMATCH:{case_id}")
        valid_requirements = {item.get("requirement_id") for item in gold_case.get("requirements", [])}
        if not set(case.get("gold_e_requirement_ids", [])) <= valid_requirements:
            errors.append(f"GOLD_V_REQUIREMENT_MISSING:{case_id}")
        evidence_ids = [item.get("evidence_id") for item in case.get("evidence", [])]
        if duplicate := _duplicates([item for item in evidence_ids if isinstance(item, str)]):
            errors.append(f"GOLD_V_DUPLICATE_EVIDENCE:{case_id}:{sorted(duplicate)[0]}")
        for judgement in case.get("relation_judgements", []):
            if judgement.get("requirement_id") not in valid_requirements:
                errors.append(f"GOLD_V_JUDGEMENT_REQUIREMENT_MISSING:{case_id}")
            if not set(judgement.get("evidence_ids", [])) <= set(evidence_ids):
                errors.append(f"GOLD_V_EVIDENCE_MISSING:{case_id}")
        status = case.get("generation_result", {}).get("status")
        evaluable = status == "completed_evaluable"
        if not case.get("run_id") or not case.get("input_reference", {}).get("input_sha256") or not case.get("generation_configuration", {}).get("configuration_sha256"):
            errors.append(f"GOLD_V_ATTEMPT_PROVENANCE_INCOMPLETE:{case_id}")
        if evaluable:
            if not isinstance(case.get("answer"), str) or not case.get("answer", "").strip() or not case.get("answer_sha256"):
                errors.append(f"GOLD_V_EVALUABLE_ANSWER_MISSING:{case_id}")
            if frozen:
                expected_quality = {"completeness", "relational_coherence", "tactical_correctness", "documentary_support"}
                if not case.get("relation_judgements") or set(case.get("quality_judgements") or {}) != expected_quality:
                    errors.append(f"GOLD_V_EVALUABLE_ANNOTATION_MISSING:{case_id}")
                ledger_id = case.get("adjudication_record_id")
                record = ledger.get(ledger_id)
                if not record or record.get("case_id") != case_id:
                    errors.append(f"GOLD_V_LEDGER_MISSING:{case_id}")
                else:
                    annotated = record.get("annotated_object", {})
                    if annotated.get("artifact_type") != "gold_v_answer" or annotated.get("artifact_version") != case.get("annotation_version") or annotated.get("artifact_sha256") != sha256_document(case.get("answer")):
                        errors.append(f"GOLD_V_LEDGER_OBJECT_MISMATCH:{case_id}")
            if case.get("generation_result", {}).get("diagnostic") is not None:
                errors.append(f"GOLD_V_EVALUABLE_DIAGNOSTIC_PRESENT:{case_id}")
        else:
            artificial = case.get("answer") is not None or case.get("answer_sha256") is not None or bool(case.get("relation_judgements")) or case.get("quality_judgements") is not None or case.get("adjudication_record_id") is not None
            if artificial:
                errors.append(f"GOLD_V_NON_EVALUABLE_HAS_ANNOTATION:{case_id}")
            if case.get("annotation_status") != "not_applicable":
                errors.append(f"GOLD_V_NON_EVALUABLE_ANNOTATION_STATUS:{case_id}")
            if frozen and case.get("generation_result", {}).get("technical_review", {}).get("status") != "confirmed":
                errors.append(f"GOLD_V_TECHNICAL_REVIEW_MISSING:{case_id}")
            if not isinstance(case.get("generation_result", {}).get("diagnostic"), dict):
                errors.append(f"GOLD_V_TECHNICAL_DIAGNOSTIC_MISSING:{case_id}")
    return errors


def validate_manifest(document: dict[str, Any], artifacts: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    status = document.get("manifest_status")
    dataset = document.get("dataset", {})
    if status == "draft":
        if dataset.get("sha256") is not None or document.get("frozen_at") is not None:
            errors.append("MANIFEST_DRAFT_CLAIMS_FREEZE")
        return errors
    path = dataset.get("path")
    if path not in artifacts or sha256_document(normatively_order(artifacts[path])) != dataset.get("sha256"):
        errors.append("MANIFEST_DATASET_HASH_MISMATCH")
    dependencies = document.get("dependencies", [])
    dep_types = [dep.get("dependency_type") for dep in dependencies]
    required = {"provenance_registry", "annotation_ledger"} if dataset.get("kind") == "gold_e" else {"gold_e_manifest", "annotation_ledger"}
    if set(dep_types) != required:
        errors.append("MANIFEST_DEPENDENCY_SET_INVALID")
    for dependency in dependencies:
        dep_path = dependency.get("path")
        if dep_path not in artifacts or sha256_document(normatively_order(artifacts[dep_path])) != dependency.get("sha256"):
            errors.append(f"MANIFEST_DEPENDENCY_HASH_MISMATCH:{dependency.get('dependency_type')}")
    if document.get("case_count") != len(document.get("cases", [])):
        errors.append("MANIFEST_CASE_COUNT_MISMATCH")
    if path in artifacts:
        dataset_cases = {case.get("case_id"): case for case in artifacts[path].get("cases", [])}
        manifest_cases = {case.get("case_id"): case for case in document.get("cases", [])}
        if set(dataset_cases) != set(manifest_cases):
            errors.append("MANIFEST_CASE_SET_MISMATCH")
        else:
            for case_id, case in dataset_cases.items():
                if sha256_document(normatively_order(case)) != manifest_cases[case_id].get("sha256"):
                    errors.append(f"MANIFEST_CASE_HASH_MISMATCH:{case_id}")
    return errors


def validate_manifest_graph(manifests: dict[str, dict[str, Any]]) -> list[str]:
    edges: dict[str, list[str]] = {}
    for digest, manifest in manifests.items():
        edges[digest] = [dep.get("sha256") for dep in manifest.get("dependencies", []) if dep.get("dependency_type") == "gold_e_manifest" and dep.get("sha256") in manifests]
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(child) for child in edges.get(node, [])):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return ["MANIFEST_DEPENDENCY_CYCLE"] if any(visit(node) for node in edges) else []


def validate_repository_preparation(root: Path) -> list[str]:
    errors: list[str] = []
    expected = {
        "relational_gold_provenance_registry_template_v2.json": ("schema_version", "relational_gold_provenance_registry_v2", "records"),
        "relational_gold_annotation_ledger_template_v2.json": ("schema_version", "relational_gold_annotation_ledger_v2", "records"),
        "relational_gold_e_template_v2.json": ("schema_version", "relational_gold_e_v2", "cases"),
        "relational_gold_v_template_v2.json": ("schema_version", "relational_gold_v_v2", "cases"),
        "relational_gold_freeze_manifest_template_v2.json": ("schema_version", "relational_gold_freeze_manifest_v2", "cases"),
    }
    for filename, (field, version, empty_field) in expected.items():
        document = load_json(ANNOTATIONS / filename)
        if document.get(field) != version:
            errors.append(f"TEMPLATE_VERSION_MISMATCH:{filename}")
        if document.get(empty_field) != []:
            errors.append(f"TEMPLATE_NOT_EMPTY:{filename}")
    for schema_name, version in {
        "relational_gold_provenance_registry_schema_v2.json": "relational_gold_provenance_registry_v2",
        "relational_gold_annotation_ledger_schema_v2.json": "relational_gold_annotation_ledger_v2",
        "relational_gold_e_schema_v2.json": "relational_gold_e_v2",
        "relational_gold_v_schema_v2.json": "relational_gold_v_v2",
        "relational_gold_freeze_manifest_schema_v2.json": "relational_gold_freeze_manifest_v2",
    }.items():
        schema = load_json(ANNOTATIONS / schema_name)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"SCHEMA_DRAFT_MISMATCH:{schema_name}")
        if schema.get("properties", {}).get("schema_version", {}).get("const") != version:
            errors.append(f"SCHEMA_VERSION_MISMATCH:{schema_name}")
    for relative, expected_hash in V1_HASHES.items():
        actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        if actual != expected_hash:
            errors.append(f"V1_ARTIFACT_CHANGED:{relative}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_repository_preparation(args.root)
    if errors:
        print("STATUS BLOCKED")
        for error in errors:
            print("BLOCKER", error)
        raise SystemExit(1)
    print("STATUS V2_PREPARATION_VALID")
    print("CASES 0")
    print("INFERENCE NOT_RUN")
    print("INDEPENDENT_GOLD BLOCKED")


if __name__ == "__main__":
    main()
