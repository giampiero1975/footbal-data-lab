#!/usr/bin/env python3
"""Offline deterministic validator for the Gold S2 V1 contract.

The validator checks structure, references, content-addressed identity and declared
split isolation.  It never infers or assigns a semantic label.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from validate_relational_gold_preparation_v2 import canonicalize_rfc8785


SCHEMA_VERSION = "tactical_semantic_support_gold_s2_v1"
MANIFEST_VERSION = "tactical_semantic_support_gold_s2_manifest_v1"
CANONICALIZATION_PROFILE = "gold_s2_rfc8785_nfc_v1"
LABELS = {"supported", "contradicted", "insufficient"}
SPLITS = {"development", "calibration", "holdout", "adversarial"}
PRIMARY_CATEGORIES = {
    "direct_literal_support", "faithful_paraphrase", "partial_or_missing_support",
    "explicit_incompatibility", "valid_multi_source_support",
    "invalid_multi_source_composition", "context_dependent",
    "terminological_ambiguity",
}
CROSS_PROPERTIES = {
    "negation", "universal_or_absolute_quantifier", "restricted_quantifier",
    "necessary_condition", "sufficient_condition", "omitted_condition",
    "correct_causality", "inverted_causality", "correct_actor", "wrong_actor",
    "correct_phase", "wrong_phase", "scope_or_generalization",
    "complex_tactical_relation", "multi_proposition_adversarial",
    "minimal_contrast", "single_source", "multi_source",
    "terminological_ambiguity", "document_context_dependency",
}
HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    unverifiable: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def extend(self, other: "ValidationReport") -> None:
        self.errors.extend(other.errors)
        self.unverifiable.extend(other.unverifiable)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("ROOT_NOT_OBJECT")
    return value


def _nfc_lf(value: str) -> str:
    return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))


def _digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def digest_document(value: Any) -> str:
    return _digest_bytes(canonicalize_rfc8785(normatively_order_s2(value)))


def normatively_order_s2(value: Any) -> Any:
    document = copy.deepcopy(value)
    ordering = {
        "provenance_records": "provenance_record_id", "review_ledger": "review_id",
        "qa_records": "qa_id", "holder_authorizations": "authorization_id",
        "cases": "case_id", "evidence": "evidence_id", "conditions": "condition_id",
        "quantifiers": "quantifier_id", "actors": "actor_id",
        "evidence_spans": None, "location_refs": None, "relation_refs": None,
        "requirement_refs": None, "declared_evidence_ids": None,
        "cross_cutting_properties": None, "checks": None, "evidence_refs": None,
        "evidence_anchors": None, "dependencies": None,
    }

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            for child in node.values():
                visit(child)
            for name, key in ordering.items():
                items = node.get(name)
                if not isinstance(items, list):
                    continue
                if key:
                    items.sort(key=lambda item: str(item.get(key, "")) if isinstance(item, dict) else str(item))
                elif name in {"evidence_spans", "evidence_anchors"}:
                    items.sort(key=lambda item: (str(item.get("evidence_id", "")), item.get("span", {}).get("start", -1)) if isinstance(item, dict) else (str(item), -1))
                elif name == "dependencies":
                    items.sort(key=lambda item: canonicalize_rfc8785(item) if isinstance(item, dict) else str(item).encode())
                else:
                    items.sort(key=str)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(document)
    return document


def evidence_payload(unit: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidence_id": unit.get("evidence_id"),
        "provenance_record_id": unit.get("provenance_record_id"),
        "location_refs": unit.get("location_refs"),
        "text": _nfc_lf(unit.get("text", "")) if isinstance(unit.get("text"), str) else unit.get("text"),
        "context_before": _nfc_lf(unit.get("context_before", "")) if isinstance(unit.get("context_before"), str) else unit.get("context_before"),
        "context_after": _nfc_lf(unit.get("context_after", "")) if isinstance(unit.get("context_after"), str) else unit.get("context_after"),
        "normalization": unit.get("normalization"),
    }


def claim_payload(claim: dict[str, Any]) -> dict[str, Any]:
    payload = {key: copy.deepcopy(claim.get(key)) for key in (
        "text", "context", "conditions", "quantifiers", "actors", "phase",
        "relation_refs", "requirement_refs",
    )}
    for key in ("text", "context"):
        if isinstance(payload[key], str):
            payload[key] = _nfc_lf(payload[key])
    return payload


def case_subject_payload(case: dict[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(case.get(key)) for key in (
        "case_id", "case_version", "split_id", "evidence", "composition", "claim", "taxonomy",
    )}


def case_payload(case: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(case)
    payload.pop("case_subject_sha256", None)
    freeze = payload.get("freeze")
    if isinstance(freeze, dict):
        freeze.pop("case_sha256", None)
    return payload


def dataset_payload(dataset: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(dataset)
    payload.pop("dataset_sha256", None)
    return payload


def _valid_hash(value: Any) -> bool:
    return isinstance(value, str) and HASH_RE.fullmatch(value) is not None


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def _shape(report: ValidationReport, value: Any, required: set[str], optional: set[str], path: str) -> bool:
    if not isinstance(value, dict):
        report.errors.append(f"TYPE_OBJECT_REQUIRED:{path}")
        return False
    missing = required - set(value)
    extra = set(value) - required - optional
    report.errors.extend(f"MISSING_FIELD:{path}.{name}" for name in sorted(missing))
    report.errors.extend(f"ADDITIONAL_PROPERTY:{path}.{name}" for name in sorted(extra))
    return not missing


def _id(report: ValidationReport, value: Any, path: str, nullable: bool = False) -> bool:
    if nullable and value is None:
        return True
    if not isinstance(value, str) or not value.strip():
        report.errors.append(f"INVALID_ID:{path}")
        return False
    return True


def _hash(report: ValidationReport, value: Any, path: str, nullable: bool = False) -> bool:
    if nullable and value is None:
        return True
    if not _valid_hash(value):
        report.errors.append(f"INVALID_SHA256:{path}")
        return False
    return True


def _span(report: ValidationReport, ref: Any, text: str, path: str) -> None:
    if not _shape(report, ref, {"start", "end", "text"}, set(), path):
        return
    start, end, quoted = ref.get("start"), ref.get("end"), ref.get("text")
    if isinstance(start, bool) or not isinstance(start, int) or isinstance(end, bool) or not isinstance(end, int):
        report.errors.append(f"SPAN_OFFSET_TYPE:{path}")
        return
    if start < 0 or end < start or end > len(text):
        report.errors.append(f"SPAN_OUT_OF_RANGE:{path}")
        return
    if not isinstance(quoted, str) or text[start:end] != quoted:
        report.errors.append(f"SPAN_TEXT_MISMATCH:{path}")


def _validate_evidence_span_refs(report: ValidationReport, refs: Any, evidence: dict[str, str], path: str) -> None:
    if not isinstance(refs, list):
        report.errors.append(f"TYPE_ARRAY_REQUIRED:{path}")
        return
    for index, item in enumerate(refs):
        item_path = f"{path}[{index}]"
        if not _shape(report, item, {"evidence_id", "span"}, set(), item_path):
            continue
        evidence_id = item.get("evidence_id")
        if evidence_id not in evidence:
            report.errors.append(f"EVIDENCE_REF_UNRESOLVED:{item_path}")
            continue
        _span(report, item.get("span"), evidence[evidence_id], f"{item_path}.span")


def _validate_provenance(report: ValidationReport, records: Any, frozen: bool) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        report.errors.append("TYPE_ARRAY_REQUIRED:provenance_records")
        return {}
    result: dict[str, dict[str, Any]] = {}
    required = {"provenance_record_id", "source_id", "document_id", "document_version", "author_group_id", "near_duplicate_cluster_id", "source_content", "source_sha256", "rights_status", "availability_status"}
    for index, record in enumerate(records):
        path = f"provenance_records[{index}]"
        if not _shape(report, record, required, set(), path):
            continue
        record_id = record.get("provenance_record_id")
        _id(report, record_id, f"{path}.provenance_record_id")
        for name in ("source_id", "document_id", "document_version"):
            _id(report, record.get(name), f"{path}.{name}")
        _id(report, record.get("author_group_id"), f"{path}.author_group_id", True)
        _id(report, record.get("near_duplicate_cluster_id"), f"{path}.near_duplicate_cluster_id", True)
        _hash(report, record.get("source_sha256"), f"{path}.source_sha256")
        if record.get("rights_status") not in {"active", "revoked", "unknown"}:
            report.errors.append(f"PROVENANCE_RIGHTS_STATUS_INVALID:{path}")
        if record.get("availability_status") not in {"verified", "unavailable", "unknown"}:
            report.errors.append(f"PROVENANCE_AVAILABILITY_STATUS_INVALID:{path}")
        content = record.get("source_content")
        if content is None:
            report.unverifiable.append(f"SOURCE_HASH_UNVERIFIABLE:{record_id}")
            if frozen:
                report.errors.append(f"FROZEN_SOURCE_HASH_UNVERIFIABLE:{record_id}")
        elif not isinstance(content, str):
            report.errors.append(f"SOURCE_CONTENT_TYPE:{path}")
        elif _digest_bytes(content.encode("utf-8")) != record.get("source_sha256"):
            report.errors.append(f"SOURCE_HASH_MISMATCH:{record_id}")
        if frozen and (record.get("rights_status") != "active" or record.get("availability_status") != "verified"):
            report.errors.append(f"FROZEN_PROVENANCE_NOT_VERIFIED:{record_id}")
        if isinstance(record_id, str):
            if record_id in result:
                report.errors.append(f"DUPLICATE_PROVENANCE_ID:{record_id}")
            else:
                result[record_id] = record
    return result


def _validate_condition_items(report: ValidationReport, items: Any, path: str, kind: str) -> None:
    if not isinstance(items, list):
        report.errors.append(f"TYPE_ARRAY_REQUIRED:{path}")
        return
    id_name = {"condition": "condition_id", "quantifier": "quantifier_id", "actor": "actor_id"}[kind]
    required = {
        "condition": {"condition_id", "text", "assertion"},
        "quantifier": {"quantifier_id", "text", "scope"},
        "actor": {"actor_id", "label"},
    }[kind]
    ids: list[str] = []
    for index, item in enumerate(items):
        item_path = f"{path}[{index}]"
        if not _shape(report, item, required, set(), item_path):
            continue
        if _id(report, item.get(id_name), f"{item_path}.{id_name}"):
            ids.append(item[id_name])
        for name in required - {id_name}:
            if not isinstance(item.get(name), str) or not item[name]:
                report.errors.append(f"INVALID_STRING:{item_path}.{name}")
        if kind == "condition" and item.get("assertion") not in {"explicit", "inferred", "unknown"}:
            report.errors.append(f"CONDITION_ASSERTION_INVALID:{item_path}")
    for duplicate in _duplicates(ids):
        report.errors.append(f"DUPLICATE_{kind.upper()}_ID:{duplicate}")


def _validate_case_shape(report: ValidationReport, case: Any, index: int, provenance: dict[str, dict[str, Any]], frozen: bool) -> None:
    path = f"cases[{index}]"
    required = {"case_id", "case_version", "split_id", "evidence", "composition", "claim", "taxonomy", "gold_label", "gold_rationale", "reviews", "case_subject_sha256", "freeze"}
    if not _shape(report, case, required, {"d3_mapping"}, path):
        return
    for name in ("case_id", "case_version"):
        _id(report, case.get(name), f"{path}.{name}")
    if case.get("split_id") not in SPLITS:
        report.errors.append(f"SPLIT_UNKNOWN:{path}")
    evidence_list = case.get("evidence")
    evidence_text: dict[str, str] = {}
    provenance_ids: list[str] = []
    if not isinstance(evidence_list, list) or not evidence_list:
        report.errors.append(f"EVIDENCE_REQUIRED:{path}")
        evidence_list = []
    evidence_ids: list[str] = []
    evidence_required = {"evidence_id", "provenance_record_id", "location_refs", "text", "context_before", "context_after", "normalization", "evidence_sha256"}
    for e_index, unit in enumerate(evidence_list):
        e_path = f"{path}.evidence[{e_index}]"
        if not _shape(report, unit, evidence_required, set(), e_path):
            continue
        evidence_id = unit.get("evidence_id")
        if _id(report, evidence_id, f"{e_path}.evidence_id"):
            evidence_ids.append(evidence_id)
        provenance_id = unit.get("provenance_record_id")
        if provenance_id not in provenance:
            report.errors.append(f"PROVENANCE_REF_UNRESOLVED:{e_path}")
        elif isinstance(provenance_id, str):
            provenance_ids.append(provenance_id)
        locations = unit.get("location_refs")
        if not isinstance(locations, list) or not locations or not all(isinstance(item, str) and item for item in locations):
            report.errors.append(f"LOCATION_REFS_INVALID:{e_path}")
        text = unit.get("text")
        if not isinstance(text, str) or not text:
            report.errors.append(f"EVIDENCE_TEXT_INVALID:{e_path}")
            text = ""
        elif text != _nfc_lf(text):
            report.errors.append(f"EVIDENCE_NOT_NFC_LF:{e_path}")
        for name in ("context_before", "context_after"):
            value = unit.get(name)
            if not isinstance(value, str) or value != _nfc_lf(value):
                report.errors.append(f"EVIDENCE_CONTEXT_INVALID:{e_path}.{name}")
        if unit.get("normalization") != "utf8_nfc_lf_v1":
            report.errors.append(f"EVIDENCE_NORMALIZATION_INVALID:{e_path}")
        _hash(report, unit.get("evidence_sha256"), f"{e_path}.evidence_sha256")
        if digest_document(evidence_payload(unit)) != unit.get("evidence_sha256"):
            report.errors.append(f"EVIDENCE_HASH_MISMATCH:{evidence_id}")
        if isinstance(evidence_id, str):
            evidence_text[evidence_id] = text
    for duplicate in _duplicates(evidence_ids):
        report.errors.append(f"DUPLICATE_EVIDENCE_ID:{duplicate}")

    composition = case.get("composition")
    if _shape(report, composition, {"mode", "declared_evidence_ids"}, set(), f"{path}.composition"):
        mode = composition.get("mode")
        declared = composition.get("declared_evidence_ids")
        if mode not in {"single_source", "multi_source"} or not isinstance(declared, list) or set(declared) != set(evidence_ids):
            report.errors.append(f"EVIDENCE_COMPOSITION_INVALID:{path}")
        if len(set(provenance_ids)) > 1 and mode != "multi_source":
            report.errors.append(f"MULTI_SOURCE_NOT_DECLARED:{path}")
        if len(set(provenance_ids)) <= 1 and mode != "single_source":
            report.errors.append(f"SINGLE_SOURCE_MODE_MISMATCH:{path}")

    claim = case.get("claim")
    claim_required = {"text", "context", "conditions", "quantifiers", "actors", "phase", "relation_refs", "requirement_refs", "claim_sha256"}
    if _shape(report, claim, claim_required, set(), f"{path}.claim"):
        for name in ("text", "context", "phase"):
            value = claim.get(name)
            if not isinstance(value, str) or (name != "context" and not value) or value != _nfc_lf(value):
                report.errors.append(f"CLAIM_STRING_INVALID:{path}.claim.{name}")
        _validate_condition_items(report, claim.get("conditions"), f"{path}.claim.conditions", "condition")
        _validate_condition_items(report, claim.get("quantifiers"), f"{path}.claim.quantifiers", "quantifier")
        _validate_condition_items(report, claim.get("actors"), f"{path}.claim.actors", "actor")
        for name in ("relation_refs", "requirement_refs"):
            values = claim.get(name)
            if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values):
                report.errors.append(f"CLAIM_REFS_INVALID:{path}.claim.{name}")
        _hash(report, claim.get("claim_sha256"), f"{path}.claim.claim_sha256")
        if digest_document(claim_payload(claim)) != claim.get("claim_sha256"):
            report.errors.append(f"CLAIM_HASH_MISMATCH:{case.get('case_id')}")

    taxonomy = case.get("taxonomy")
    if _shape(report, taxonomy, {"primary_category", "cross_cutting_properties"}, set(), f"{path}.taxonomy"):
        if taxonomy.get("primary_category") not in PRIMARY_CATEGORIES:
            report.errors.append(f"PRIMARY_CATEGORY_UNKNOWN:{path}")
        properties = taxonomy.get("cross_cutting_properties")
        if not isinstance(properties, list) or any(not isinstance(value, str) or value not in CROSS_PROPERTIES for value in properties):
            report.errors.append(f"CROSS_PROPERTY_UNKNOWN:{path}")
        elif len(set(properties)) != len(properties):
            report.errors.append(f"CROSS_PROPERTY_DUPLICATE:{path}")
    label = case.get("gold_label")
    if label is not None and label not in LABELS:
        report.errors.append(f"GOLD_LABEL_UNKNOWN:{path}")
    if frozen and label not in LABELS:
        report.errors.append(f"FROZEN_GOLD_LABEL_REQUIRED:{path}")

    rationale = case.get("gold_rationale")
    if _shape(report, rationale, {"evidence_spans", "explanation", "scope_notes", "ambiguity"}, set(), f"{path}.gold_rationale"):
        _validate_evidence_span_refs(report, rationale.get("evidence_spans"), evidence_text, f"{path}.gold_rationale.evidence_spans")
        for name in ("explanation", "scope_notes"):
            if not isinstance(rationale.get(name), str):
                report.errors.append(f"RATIONALE_STRING_INVALID:{path}.{name}")
        if rationale.get("ambiguity") not in {"none", "declared", "not_adjudicable"}:
            report.errors.append(f"RATIONALE_AMBIGUITY_INVALID:{path}")
        if frozen and not rationale.get("explanation"):
            report.errors.append(f"FROZEN_RATIONALE_REQUIRED:{path}")

    _hash(report, case.get("case_subject_sha256"), f"{path}.case_subject_sha256", not frozen)
    if case.get("case_subject_sha256") is not None and digest_document(case_subject_payload(case)) != case.get("case_subject_sha256"):
        report.errors.append(f"CASE_SUBJECT_HASH_MISMATCH:{case.get('case_id')}")
    freeze = case.get("freeze")
    if _shape(report, freeze, {"status", "case_sha256", "dataset_version"}, set(), f"{path}.freeze"):
        if freeze.get("status") not in {"draft", "frozen"}:
            report.errors.append(f"CASE_FREEZE_STATUS_INVALID:{path}")
        if freeze.get("dataset_version") is None:
            report.errors.append(f"CASE_DATASET_VERSION_REQUIRED:{path}")
        _hash(report, freeze.get("case_sha256"), f"{path}.freeze.case_sha256", not frozen)
        if freeze.get("case_sha256") is not None and digest_document(case_payload(case)) != freeze.get("case_sha256"):
            report.errors.append(f"CASE_HASH_MISMATCH:{case.get('case_id')}")
        if frozen and freeze.get("status") != "frozen":
            report.errors.append(f"FROZEN_CASE_STATUS_REQUIRED:{path}")
    if "d3_mapping" in case and case.get("d3_mapping") is not None:
        _validate_d3_mapping(report, case["d3_mapping"], case, evidence_text, path)


def _validate_d3_mapping(report: ValidationReport, mapping: Any, case: dict[str, Any], evidence: dict[str, str], path: str) -> None:
    required = {"statement", "section_text", "section_span", "conditions", "relation_refs", "requirement_refs", "evidence_refs", "evidence_anchors", "plan_fingerprint", "statement_sha256", "assessment_s1"}
    if not _shape(report, mapping, required, set(), f"{path}.d3_mapping"):
        return
    statement, section = mapping.get("statement"), mapping.get("section_text")
    if not isinstance(statement, str) or statement != case.get("claim", {}).get("text"):
        report.errors.append(f"D3_STATEMENT_CLAIM_MISMATCH:{path}")
    if not isinstance(section, str) or section != _nfc_lf(section):
        report.errors.append(f"D3_SECTION_INVALID:{path}")
        section = ""
    _span(report, mapping.get("section_span"), section, f"{path}.d3_mapping.section_span")
    span = mapping.get("section_span")
    if isinstance(span, dict) and isinstance(span.get("start"), int) and isinstance(span.get("end"), int) and 0 <= span["start"] <= span["end"] <= len(section) and section[span["start"]:span["end"]] != statement:
        report.errors.append(f"D3_SECTION_STATEMENT_MISMATCH:{path}")
    for name in ("conditions", "relation_refs", "requirement_refs"):
        if mapping.get(name) != case.get("claim", {}).get(name):
            report.errors.append(f"D3_CLAIM_MAPPING_MISMATCH:{path}:{name}")
    refs = mapping.get("evidence_refs")
    if not isinstance(refs, list) or set(refs) != set(evidence):
        report.errors.append(f"D3_EVIDENCE_REFS_MISMATCH:{path}")
    _validate_evidence_span_refs(report, mapping.get("evidence_anchors"), evidence, f"{path}.d3_mapping.evidence_anchors")
    _hash(report, mapping.get("plan_fingerprint"), f"{path}.d3_mapping.plan_fingerprint")
    _hash(report, mapping.get("statement_sha256"), f"{path}.d3_mapping.statement_sha256")
    if isinstance(statement, str) and _digest_bytes(_nfc_lf(statement).encode("utf-8")) != mapping.get("statement_sha256"):
        report.errors.append(f"D3_STATEMENT_HASH_MISMATCH:{path}")
    assessment = mapping.get("assessment_s1")
    if assessment is not None:
        if not _shape(report, assessment, {"content", "sha256"}, set(), f"{path}.d3_mapping.assessment_s1"):
            return
        _hash(report, assessment.get("sha256"), f"{path}.d3_mapping.assessment_s1.sha256")
        if assessment.get("content") is None:
            report.unverifiable.append(f"S1_ASSESSMENT_HASH_UNVERIFIABLE:{case.get('case_id')}")
        elif not isinstance(assessment.get("content"), dict) or digest_document(assessment["content"]) != assessment.get("sha256"):
            report.errors.append(f"S1_ASSESSMENT_HASH_MISMATCH:{path}")


def _validate_reviews(report: ValidationReport, dataset: dict[str, Any], frozen: bool) -> None:
    cases = {case.get("case_id"): case for case in dataset.get("cases", []) if isinstance(case, dict) and isinstance(case.get("case_id"), str)}
    ledger = dataset.get("review_ledger")
    qa_records = dataset.get("qa_records")
    if not isinstance(ledger, list) or not isinstance(qa_records, list):
        return
    review_map: dict[str, dict[str, Any]] = {}
    review_required = {"review_id", "case_id", "role", "reviewer_id", "object_sha256", "label", "evidence_spans", "rationale", "blinded_to_peer", "blinded_to_model", "created_at"}
    for index, record in enumerate(ledger):
        path = f"review_ledger[{index}]"
        if not _shape(report, record, review_required, set(), path):
            continue
        review_id = record.get("review_id")
        if not _id(report, review_id, f"{path}.review_id"):
            continue
        if review_id in review_map:
            report.errors.append(f"DUPLICATE_REVIEW_ID:{review_id}")
        review_map[review_id] = record
        case = cases.get(record.get("case_id"))
        if case is None:
            report.errors.append(f"REVIEW_CASE_UNRESOLVED:{review_id}")
            continue
        if record.get("role") not in {"A", "B", "C"} or record.get("label") not in LABELS:
            report.errors.append(f"REVIEW_ENUM_INVALID:{review_id}")
        _id(report, record.get("reviewer_id"), f"{path}.reviewer_id")
        _hash(report, record.get("object_sha256"), f"{path}.object_sha256")
        if record.get("object_sha256") != case.get("case_subject_sha256"):
            report.errors.append(f"REVIEW_OBJECT_HASH_MISMATCH:{review_id}")
        evidence = {unit.get("evidence_id"): unit.get("text", "") for unit in case.get("evidence", []) if isinstance(unit, dict)}
        _validate_evidence_span_refs(report, record.get("evidence_spans"), evidence, f"{path}.evidence_spans")
        if not isinstance(record.get("rationale"), str) or not record.get("rationale"):
            report.errors.append(f"REVIEW_RATIONALE_REQUIRED:{review_id}")
        if record.get("blinded_to_model") is not True or record.get("blinded_to_peer") is not True:
            report.errors.append(f"REVIEW_BLINDING_REQUIRED:{review_id}")

    qa_map: dict[str, dict[str, Any]] = {}
    qa_required = {"qa_id", "case_id", "reviewer_id", "object_sha256", "status", "checks", "rationale", "created_at"}
    for index, record in enumerate(qa_records):
        path = f"qa_records[{index}]"
        if not _shape(report, record, qa_required, set(), path):
            continue
        qa_id = record.get("qa_id")
        if not _id(report, qa_id, f"{path}.qa_id"):
            continue
        if qa_id in qa_map:
            report.errors.append(f"DUPLICATE_QA_ID:{qa_id}")
        qa_map[qa_id] = record
        case = cases.get(record.get("case_id"))
        if case is None:
            report.errors.append(f"QA_CASE_UNRESOLVED:{qa_id}")
            continue
        if record.get("object_sha256") != case.get("case_subject_sha256"):
            report.errors.append(f"QA_OBJECT_HASH_MISMATCH:{qa_id}")
        if record.get("status") not in {"pass", "fail"}:
            report.errors.append(f"QA_STATUS_INVALID:{qa_id}")
        if not isinstance(record.get("checks"), list) or not record["checks"]:
            report.errors.append(f"QA_CHECKS_REQUIRED:{qa_id}")

    for case_id, case in cases.items():
        reviews = case.get("reviews")
        if not _shape(report, reviews, {"review_a_id", "review_b_id", "disagreement_declared", "adjudication_id", "qa_d_id"}, set(), f"case:{case_id}.reviews"):
            continue
        if not frozen:
            continue
        a, b, c, d = (reviews.get(name) for name in ("review_a_id", "review_b_id", "adjudication_id", "qa_d_id"))
        if a not in review_map or review_map.get(a, {}).get("role") != "A":
            report.errors.append(f"FROZEN_REVIEW_A_UNRESOLVED:{case_id}")
        if b not in review_map or review_map.get(b, {}).get("role") != "B":
            report.errors.append(f"FROZEN_REVIEW_B_UNRESOLVED:{case_id}")
        labels_disagree = review_map.get(a, {}).get("label") != review_map.get(b, {}).get("label")
        if labels_disagree and reviews.get("disagreement_declared") is not True:
            report.errors.append(f"REVIEW_DISAGREEMENT_NOT_DECLARED:{case_id}")
        if labels_disagree or reviews.get("disagreement_declared") is True:
            if c not in review_map or review_map.get(c, {}).get("role") != "C":
                report.errors.append(f"FROZEN_ADJUDICATION_UNRESOLVED:{case_id}")
            elif review_map[c].get("label") != case.get("gold_label"):
                report.errors.append(f"ADJUDICATION_LABEL_MISMATCH:{case_id}")
        elif review_map.get(a, {}).get("label") != case.get("gold_label"):
            report.errors.append(f"CONSENSUS_LABEL_MISMATCH:{case_id}")
        if d not in qa_map or qa_map.get(d, {}).get("status") != "pass":
            report.errors.append(f"FROZEN_QA_D_REQUIRED:{case_id}")


def _validate_split_isolation(report: ValidationReport, dataset: dict[str, Any]) -> None:
    provenance = {record.get("provenance_record_id"): record for record in dataset.get("provenance_records", []) if isinstance(record, dict)}
    policy = dataset.get("independence_policy", {})
    dimensions = [
        ("source_id", "source_disjoint_required"),
        ("document_id", "document_disjoint_required"),
        ("near_duplicate_cluster_id", "near_duplicate_disjoint_required"),
        ("author_group_id", "author_disjoint_required"),
    ]
    observed: dict[tuple[str, str], set[str]] = {}
    for case in dataset.get("cases", []):
        if not isinstance(case, dict) or case.get("split_id") not in SPLITS:
            continue
        for unit in case.get("evidence", []):
            record = provenance.get(unit.get("provenance_record_id")) if isinstance(unit, dict) else None
            if not record:
                continue
            for field_name, policy_name in dimensions:
                value = record.get(field_name)
                if value is None:
                    if policy.get(policy_name) is True:
                        report.unverifiable.append(f"SPLIT_{field_name.upper()}_UNVERIFIABLE:{case.get('case_id')}")
                    continue
                observed.setdefault((field_name, str(value)), set()).add(case["split_id"])
    for (field_name, value), splits in observed.items():
        policy_name = next(name for field, name in dimensions if field == field_name)
        if policy.get(policy_name) is True and len(splits) > 1:
            report.errors.append(f"SPLIT_CONTAMINATION:{field_name}:{value}:{','.join(sorted(splits))}")


def validate_dataset(dataset: dict[str, Any]) -> ValidationReport:
    report = ValidationReport()
    required = {"schema_version", "dataset_version", "status", "canonicalization_profile", "independence_policy", "provenance_records", "review_ledger", "qa_records", "holder_authorizations", "cases", "dataset_sha256"}
    if not _shape(report, dataset, required, set(), "dataset"):
        return report
    if dataset.get("schema_version") != SCHEMA_VERSION:
        report.errors.append("SCHEMA_VERSION_INCOMPATIBLE")
    _id(report, dataset.get("dataset_version"), "dataset.dataset_version")
    frozen = dataset.get("status") == "frozen"
    if dataset.get("status") not in {"draft", "frozen"}:
        report.errors.append("DATASET_STATUS_INVALID")
    if dataset.get("canonicalization_profile") != CANONICALIZATION_PROFILE:
        report.errors.append("CANONICALIZATION_PROFILE_INCOMPATIBLE")
    policy = dataset.get("independence_policy")
    if _shape(report, policy, {"source_disjoint_required", "document_disjoint_required", "near_duplicate_disjoint_required", "author_disjoint_required"}, set(), "independence_policy"):
        for name, value in policy.items():
            if not isinstance(value, bool):
                report.errors.append(f"INDEPENDENCE_POLICY_TYPE:{name}")
    provenance = _validate_provenance(report, dataset.get("provenance_records"), frozen)
    cases = dataset.get("cases")
    if not isinstance(cases, list):
        report.errors.append("TYPE_ARRAY_REQUIRED:cases")
        cases = []
    case_ids: list[str] = []
    for index, case in enumerate(cases):
        _validate_case_shape(report, case, index, provenance, frozen)
        if isinstance(case, dict) and isinstance(case.get("case_id"), str):
            case_ids.append(case["case_id"])
            if isinstance(case.get("freeze"), dict) and case["freeze"].get("dataset_version") != dataset.get("dataset_version"):
                report.errors.append(f"CASE_DATASET_VERSION_MISMATCH:{case['case_id']}")
    for duplicate in _duplicates(case_ids):
        report.errors.append(f"DUPLICATE_CASE_ID:{duplicate}")
    _validate_reviews(report, dataset, frozen)
    _validate_split_isolation(report, dataset)

    authorizations = dataset.get("holder_authorizations")
    authorization_ids: list[str] = []
    if not isinstance(authorizations, list):
        report.errors.append("TYPE_ARRAY_REQUIRED:holder_authorizations")
        authorizations = []
    for index, item in enumerate(authorizations):
        path = f"holder_authorizations[{index}]"
        if not _shape(report, item, {"authorization_id", "scope", "dataset_version", "holder_id", "approved_at"}, set(), path):
            continue
        if _id(report, item.get("authorization_id"), f"{path}.authorization_id"):
            authorization_ids.append(item["authorization_id"])
        if item.get("scope") != "freeze" or item.get("dataset_version") != dataset.get("dataset_version"):
            report.errors.append(f"HOLDER_AUTHORIZATION_SCOPE_INVALID:{path}")
        _id(report, item.get("holder_id"), f"{path}.holder_id")
        _id(report, item.get("approved_at"), f"{path}.approved_at")
    for duplicate in _duplicates(authorization_ids):
        report.errors.append(f"DUPLICATE_AUTHORIZATION_ID:{duplicate}")
    if frozen and not authorizations:
        report.errors.append("FROZEN_HOLDER_AUTHORIZATION_REQUIRED")

    _hash(report, dataset.get("dataset_sha256"), "dataset.dataset_sha256", not frozen)
    if dataset.get("dataset_sha256") is not None and digest_document(dataset_payload(dataset)) != dataset.get("dataset_sha256"):
        report.errors.append("DATASET_HASH_MISMATCH")
    return report


def validate_manifest(manifest: dict[str, Any], dataset: dict[str, Any]) -> ValidationReport:
    report = ValidationReport()
    required = {"schema_version", "manifest_status", "dataset", "canonicalization_profile", "case_count", "cases", "dependencies", "frozen_at", "holder_authorization_id", "parent_manifest_sha256", "supersedes_manifest_sha256", "immutable_after_freeze"}
    if not _shape(report, manifest, required, set(), "manifest"):
        return report
    if manifest.get("schema_version") != MANIFEST_VERSION:
        report.errors.append("MANIFEST_SCHEMA_VERSION_INCOMPATIBLE")
    frozen = manifest.get("manifest_status") == "frozen"
    if manifest.get("manifest_status") not in {"draft", "frozen"}:
        report.errors.append("MANIFEST_STATUS_INVALID")
    if manifest.get("canonicalization_profile") != CANONICALIZATION_PROFILE:
        report.errors.append("MANIFEST_CANONICALIZATION_PROFILE_INCOMPATIBLE")
    dataset_ref = manifest.get("dataset")
    if _shape(report, dataset_ref, {"path", "version", "sha256"}, set(), "manifest.dataset"):
        if dataset_ref.get("version") != dataset.get("dataset_version"):
            report.errors.append("MANIFEST_DATASET_VERSION_MISMATCH")
        _hash(report, dataset_ref.get("sha256"), "manifest.dataset.sha256", not frozen)
        if dataset_ref.get("sha256") is not None and dataset_ref["sha256"] != digest_document(dataset_payload(dataset)):
            report.errors.append("MANIFEST_DATASET_HASH_MISMATCH")
    cases = dataset.get("cases", []) if isinstance(dataset.get("cases"), list) else []
    manifest_cases = manifest.get("cases")
    if not isinstance(manifest_cases, list):
        report.errors.append("TYPE_ARRAY_REQUIRED:manifest.cases")
        manifest_cases = []
    if manifest.get("case_count") != len(cases) or len(manifest_cases) != len(cases):
        report.errors.append("MANIFEST_CASE_COUNT_MISMATCH")
    expected = {case.get("case_id"): (case.get("freeze", {}).get("case_sha256"), case.get("split_id")) for case in cases if isinstance(case, dict)}
    observed: dict[str, tuple[Any, Any]] = {}
    for index, item in enumerate(manifest_cases):
        path = f"manifest.cases[{index}]"
        if not _shape(report, item, {"case_id", "sha256", "split_id"}, set(), path):
            continue
        case_id = item.get("case_id")
        if case_id in observed:
            report.errors.append(f"MANIFEST_DUPLICATE_CASE:{case_id}")
        observed[case_id] = (item.get("sha256"), item.get("split_id"))
    if observed != expected:
        report.errors.append("MANIFEST_CASE_SET_OR_HASH_MISMATCH")
    for name in ("parent_manifest_sha256", "supersedes_manifest_sha256"):
        _hash(report, manifest.get(name), f"manifest.{name}", True)
    if frozen:
        if dataset.get("status") != "frozen" or manifest.get("frozen_at") is None or manifest.get("immutable_after_freeze") is not True:
            report.errors.append("FROZEN_MANIFEST_PRECONDITIONS_MISSING")
        authorization_id = manifest.get("holder_authorization_id")
        ids = {item.get("authorization_id") for item in dataset.get("holder_authorizations", []) if isinstance(item, dict)}
        if authorization_id not in ids:
            report.errors.append("MANIFEST_HOLDER_AUTHORIZATION_UNRESOLVED")
    return report


def validate_repository_contracts(root: Path) -> ValidationReport:
    report = ValidationReport()
    annotation_root = root / "evaluation" / "annotations"
    expected = {
        "tactical_semantic_support_gold_s2_schema_v1.json",
        "tactical_semantic_support_gold_s2_freeze_manifest_schema_v1.json",
        "tactical_semantic_support_gold_s2_template_v1.json",
        "tactical_semantic_support_gold_s2_freeze_manifest_template_v1.json",
    }
    for name in expected:
        try:
            load_json(annotation_root / name)
        except Exception as exc:  # deterministic boundary for malformed artifacts
            report.errors.append(f"REPOSITORY_ARTIFACT_INVALID:{name}:{type(exc).__name__}")
    if report.errors:
        return report
    dataset = load_json(annotation_root / "tactical_semantic_support_gold_s2_template_v1.json")
    manifest = load_json(annotation_root / "tactical_semantic_support_gold_s2_freeze_manifest_template_v1.json")
    report.extend(validate_dataset(dataset))
    report.extend(validate_manifest(manifest, dataset))
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if args.dataset:
        dataset = load_json(args.dataset)
        report = validate_dataset(dataset)
        if args.manifest:
            report.extend(validate_manifest(load_json(args.manifest), dataset))
    else:
        report = validate_repository_contracts(args.repository_root)
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
