#!/usr/bin/env python3
"""Static checks for empty relational Gold E/Gold V preparation artifacts.

This validator is intentionally standard-library only.  It verifies the
preparation contract and rejects populated templates; it does not validate
human annotations or run the tactical engine.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


GOLD_E_CASE_FIELDS = {
    "case_id", "question", "source_id", "source_provenance",
    "independence_status", "annotation_version", "annotator_id",
    "reviewer_id", "request_parts", "requirements", "ambiguities",
    "annotation_notes", "review_status", "freeze_status",
    "freeze_timestamp", "schema_version",
}
GOLD_V_CASE_FIELDS = {
    "case_id", "gold_e_case_id", "gold_e_requirement_ids", "question",
    "answer", "answer_provenance", "source_id", "source_provenance", "independence_status",
    "annotation_version", "annotator_id", "reviewer_id", "evidence",
    "relation_judgements", "completeness", "relational_coherence",
    "tactical_correctness", "documentary_support", "ambiguities",
    "annotation_notes", "review_status", "freeze_status",
    "freeze_timestamp", "schema_version",
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def validate_schema(document: dict, kind: str) -> list[str]:
    errors: list[str] = []
    expected_version = f"relational_gold_{kind}_v1"
    if document.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(f"{kind}: JSON Schema draft must be 2020-12")
    if document.get("properties", {}).get("schema_version", {}).get("const") != expected_version:
        errors.append(f"{kind}: wrong schema version const")
    case = document.get("$defs", {}).get("case", {})
    required = set(case.get("required", []))
    expected = GOLD_E_CASE_FIELDS if kind == "e" else GOLD_V_CASE_FIELDS
    missing = sorted(expected - required)
    if missing:
        errors.append(f"{kind}: missing required case fields: {', '.join(missing)}")
    if case.get("additionalProperties") is not False:
        errors.append(f"{kind}: case must reject undeclared properties")
    return errors


def validate_template(document: dict, kind: str) -> list[str]:
    errors: list[str] = []
    expected_version = f"relational_gold_{kind}_v1"
    expected_kind = f"gold_{kind}"
    if document.get("schema_version") != expected_version:
        errors.append(f"{kind}: template schema_version mismatch")
    if document.get("dataset_kind") != expected_kind:
        errors.append(f"{kind}: template dataset_kind mismatch")
    if document.get("status") != "template":
        errors.append(f"{kind}: template status must be template")
    if document.get("cases") != []:
        errors.append(f"{kind}: template must contain zero cases")
    if kind == "v":
        reference = document.get("gold_e_reference", {})
        if reference.get("freeze_status") != "not_available":
            errors.append("v: empty template cannot claim a frozen Gold E")
        if reference.get("manifest_sha256") is not None:
            errors.append("v: empty template cannot contain a Gold E hash")
    return errors


def validate_manifest(document: dict) -> list[str]:
    errors: list[str] = []
    if document.get("schema_version") != "relational_gold_freeze_manifest_v1":
        errors.append("manifest: wrong schema version")
    if document.get("manifest_status") != "draft":
        errors.append("manifest: preparation template must remain draft")
    if document.get("case_count") != 0 or document.get("cases") != []:
        errors.append("manifest: preparation template must contain zero cases")
    if document.get("dataset_sha256") is not None or document.get("frozen_at") is not None:
        errors.append("manifest: draft cannot claim dataset hash or freeze timestamp")
    if document.get("immutable_after_freeze") is not True:
        errors.append("manifest: immutability declaration must be true")
    separation = document.get("development_separation", {})
    if separation.get("screening_result") != "not_run":
        errors.append("manifest: empty preparation cannot claim screening")
    return errors


def validate_all(schema_e: Path, schema_v: Path, template_e: Path,
                 template_v: Path, manifest: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_schema(load_json(schema_e), "e"))
    errors.extend(validate_schema(load_json(schema_v), "v"))
    errors.extend(validate_template(load_json(template_e), "e"))
    errors.extend(validate_template(load_json(template_v), "v"))
    errors.extend(validate_manifest(load_json(manifest)))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema-e", required=True, type=Path)
    parser.add_argument("--schema-v", required=True, type=Path)
    parser.add_argument("--template-e", required=True, type=Path)
    parser.add_argument("--template-v", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    errors = validate_all(args.schema_e, args.schema_v, args.template_e,
                          args.template_v, args.manifest)
    if errors:
        print("STATUS BLOCKED")
        for error in errors:
            print("BLOCKER", error)
        raise SystemExit(1)
    print("STATUS PREPARATION_VALID")
    print("CASES 0")
    print("INDEPENDENT_BENCHMARK BLOCKED")


if __name__ == "__main__":
    main()
