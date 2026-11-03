#!/usr/bin/env python3
"""Offline-testable D3 handoff: authoritative TSC V2 plan plus documentary prose."""
from __future__ import annotations

import hashlib
import json
import unicodedata

import v5_tactical_state_generation_v2 as generation_v2
import v5_tactical_semantic_support_s1 as semantic_support_s1


TRANSPORT_SCHEMA = "tactical_state_documentary_explanation_v1"
DIAGNOSTIC_SCHEMA = "tactical_state_dual_output_diagnostic_v1"
SECTION_KINDS = {"relation_explanation", "conditional_detail", "scenario_detail", "uncertainty"}
DIMENSIONS = {"actor", "task", "space", "trigger", "purpose", "phase", "detail"}
POLARITIES = {"affirmed", "negated", "conditional", "uncertain"}
SUPPORT_MODES = {"direct", "bounded_inference", "uncertainty"}
MAX_SECTIONS = 64
MAX_CLAIMS_PER_SECTION = 32
MAX_TOTAL_CLAIMS = 256
MAX_REFS_PER_SECTION = 64
MAX_EVIDENCE_PER_CLAIM = 8
MAX_SECTION_CHARS = 12000
MAX_TOTAL_CHARS = 32000


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def plan_fingerprint(plan):
    return "sha256:" + hashlib.sha256(canonical_json(plan).encode("utf-8")).hexdigest()


def _term_id(relation, dimension):
    if dimension == "space":
        return ((relation.get("space") or {}).get("term") or {}).get("term_id")
    return (relation.get(dimension) or {}).get("term_id")


def relation_bindings(relation):
    return {
        "actor": (relation.get("actor_ref") or {}).get("id"),
        "task": _term_id(relation, "task"),
        "space": _term_id(relation, "space"),
        "trigger": _term_id(relation, "trigger"),
        "purpose": _term_id(relation, "purpose"),
        "phase": (relation.get("phase_state_ref") or {}).get("id"),
    }


def render_canonical_relations(plan):
    """Render the authoritative plan without accepting model-authored plan text."""
    rendered = []
    for relation in plan.get("operational_relations", []):
        relation_id = relation["relation_id"]
        phase = generation_v2.applied_plan_state_phase(
            plan, relation["phase_state_ref"]["id"])
        rendered.append({
            "relation_id": relation_id,
            "rendered_lines": [
                f"[REL {relation_id}]",
                f"Attore: {relation['actor_ref']['id']}",
                f"Compito: {relation['task']['source_term']}",
                f"Spazio: {relation['space']['term']['source_term']}",
                f"Trigger: {relation['trigger']['source_term']}",
                f"Finalità: {relation['purpose']['source_term']}",
                f"Fase: {phase}",
            ],
        })
    return rendered


def prepare_dual_output_request(question_plan):
    preflight = generation_v2.prepare_generation_request(question_plan)
    if preflight.get("status") != "ready":
        return {"status": preflight.get("status", "not_evaluable"),
                "reasons": preflight.get("reasons", []), "v2_preflight": preflight}
    plan = preflight["authorized_applied_plan"]
    return {
        "status": "ready",
        "reasons": [],
        "v2_preflight": preflight,
        "authorized_applied_plan": plan,
        "authorized_plan_fingerprint": plan_fingerprint(plan),
        "canonical_relations": render_canonical_relations(plan),
    }


def generation_transport_schema():
    """JSON Schema used only for the model-authored documentary envelope."""
    string_array = {"type": "array", "maxItems": MAX_REFS_PER_SECTION,
                    "uniqueItems": True, "items": {"type": "string", "minLength": 1}}
    evidence_array = {"type": "array", "minItems": 1,
                      "maxItems": MAX_EVIDENCE_PER_CLAIM, "uniqueItems": True,
                      "items": {"type": "string", "pattern": "^F[1-9][0-9]*$"}}
    anchor = {"type": "object", "additionalProperties": False,
              "required": ["evidence_ref", "exact_text"],
              "properties": {"evidence_ref": {"type": "string", "pattern": "^F[1-9][0-9]*$"},
                             "exact_text": {"type": "string", "minLength": 1}}}
    claim = {"type": "object", "additionalProperties": False,
             "required": ["claim_id", "statement", "section_span", "conditions",
                          "relation_refs", "requirement_refs", "dimensions", "bindings",
                          "polarity", "evidence_refs", "support_mode", "evidence_anchors"],
             "properties": {
                 "claim_id": {"type": "string", "minLength": 1},
                 "statement": {"type": "string", "minLength": 1},
                 "section_span": {
                     "type": "object", "additionalProperties": False,
                     "required": ["start", "end"],
                     "properties": {"start": {"type": "integer", "minimum": 0},
                                    "end": {"type": "integer", "minimum": 1}}},
                 "conditions": {"type": "array", "uniqueItems": True,
                                "items": {"type": "string", "minLength": 1}},
                 "relation_refs": {**string_array, "minItems": 1},
                 "requirement_refs": {**string_array, "minItems": 1},
                 "dimensions": {"type": "array", "minItems": 1, "uniqueItems": True,
                                "items": {"enum": sorted(DIMENSIONS)}},
                 "bindings": {"type": "object", "additionalProperties": False,
                              "properties": {name: {"type": "string", "minLength": 1}
                                             for name in sorted(DIMENSIONS - {"detail"})}},
                 "polarity": {"enum": sorted(POLARITIES)},
                 "evidence_refs": evidence_array,
                 "support_mode": {"enum": sorted(SUPPORT_MODES)},
                 "evidence_anchors": {"type": "array", "maxItems": MAX_EVIDENCE_PER_CLAIM,
                                      "items": anchor},
             }}
    section = {"type": "object", "additionalProperties": False,
               "required": ["section_id", "kind", "relation_refs", "requirement_refs",
                            "text", "evidence_refs", "claims"],
               "properties": {
                   "section_id": {"type": "string", "minLength": 1},
                   "kind": {"enum": sorted(SECTION_KINDS)},
                   "relation_refs": string_array,
                   "requirement_refs": string_array,
                   "text": {"type": "string", "minLength": 1, "maxLength": MAX_SECTION_CHARS},
                   "evidence_refs": {"type": "array", "maxItems": 8, "uniqueItems": True,
                                     "items": {"type": "string", "pattern": "^F[1-9][0-9]*$"}},
                   "claims": {"type": "array", "minItems": 1,
                              "maxItems": MAX_CLAIMS_PER_SECTION, "items": claim},
               }}
    return {"type": "object", "additionalProperties": False,
            "required": ["schema", "authorized_plan_fingerprint", "documentary_explanation"],
            "properties": {
                "schema": {"const": TRANSPORT_SCHEMA},
                "authorized_plan_fingerprint": {"type": "string",
                                                "pattern": "^sha256:[0-9a-f]{64}$"},
                "documentary_explanation": {
                    "type": "object", "additionalProperties": False,
                    "required": ["sections"],
                    "properties": {"sections": {"type": "array", "minItems": 1,
                                                "maxItems": MAX_SECTIONS, "items": section}}},
            }}


def parse_documentary_content(raw_content):
    if not isinstance(raw_content, str) or not raw_content.strip():
        return None, ["empty_documentary_envelope"]
    try:
        parsed = json.loads(raw_content)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, ["invalid_documentary_json"]
    return (parsed, []) if isinstance(parsed, dict) else (None, ["invalid_documentary_envelope"])


def _unique_string_list(value, minimum=0, maximum=MAX_REFS_PER_SECTION):
    return (isinstance(value, list) and minimum <= len(value) <= maximum and
            all(isinstance(item, str) and item for item in value) and len(value) == len(set(value)))


def _nfc_lines(value):
    return unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n")


def _audit_positive(audit):
    if not isinstance(audit, dict) or audit.get("complete") is not True:
        return False
    return not any(audit.get(key) for key in (
        "missing_facets", "missing_operational", "missing_details", "semantic_issues"))


def _failure(code, **details):
    return {"code": code, **details}


def documentary_diagnostic(question_plan, raw_content, evidence, *, preflight=None,
                           tactical_audit=None, done_reason=None,
                           transport_error=None, attempt_id="offline"):
    """Validate D3 deterministically; unknown semantic support stays not_evaluable."""
    preflight = preflight or prepare_dual_output_request(question_plan)
    base = {"schema": DIAGNOSTIC_SCHEMA, "overall_status": preflight.get("status", "not_evaluable"),
            "promoted_answer": "", "raw_model_content": raw_content,
            "authorized_applied_plan": preflight.get("authorized_applied_plan"),
            "authorized_plan_fingerprint": preflight.get("authorized_plan_fingerprint"),
            "canonical_relations": preflight.get("canonical_relations", []),
            "reasons": list(preflight.get("reasons", [])),
            "controls": {"preflight": preflight}}
    if preflight.get("status") != "ready":
        return base
    if transport_error is not None:
        base.update(overall_status="not_evaluable", reasons=["transport_error"])
        return base
    parsed, parse_errors = parse_documentary_content(raw_content)
    if parse_errors:
        base.update(overall_status="not_evaluable", reasons=parse_errors)
        return base

    failures, unassessed, checked = [], [], []
    expected_top = {"schema", "authorized_plan_fingerprint", "documentary_explanation"}
    if set(parsed) != expected_top or parsed.get("schema") != TRANSPORT_SCHEMA:
        failures.append(_failure("invalid_documentary_envelope_shape"))
    if parsed.get("authorized_plan_fingerprint") != preflight["authorized_plan_fingerprint"]:
        failures.append(_failure("authorized_plan_fingerprint_mismatch"))
    documentary = parsed.get("documentary_explanation")
    if not isinstance(documentary, dict) or set(documentary) != {"sections"}:
        failures.append(_failure("invalid_documentary_explanation_shape"))
        sections = []
    else:
        sections = documentary.get("sections")
        if not isinstance(sections, list) or not 1 <= len(sections) <= MAX_SECTIONS:
            failures.append(_failure("invalid_documentary_section_cardinality"))
            sections = []

    plan = preflight["authorized_applied_plan"]
    relation_by_id = {item["relation_id"]: item for item in plan.get("operational_relations", [])}
    requirement_ids = {item["requirement_id"] for item in preflight["v2_preflight"].get(
        "projected_requirements", []) if isinstance(item.get("requirement_id"), str)}
    evidence_by_id = {str(item.get("label") or f"F{index}"): item
                      for index, item in enumerate(evidence, 1)}
    section_ids, claim_ids, covered_relations, covered_requirements = set(), set(), set(), set()
    referenced_relations, referenced_requirements = set(), set()
    claim_count, total_chars = 0, 0
    generated_assessments = []

    for section_index, section in enumerate(sections):
        path = f"sections.{section_index}"
        required = {"section_id", "kind", "relation_refs", "requirement_refs",
                    "text", "evidence_refs", "claims"}
        if not isinstance(section, dict) or set(section) != required:
            failures.append(_failure("invalid_documentary_section_shape", path=path))
            continue
        section_id = section["section_id"]
        if not isinstance(section_id, str) or not section_id or section_id in section_ids:
            failures.append(_failure("invalid_or_duplicate_section_id", path=path))
        else:
            section_ids.add(section_id)
        if section["kind"] not in SECTION_KINDS:
            failures.append(_failure("invalid_documentary_section_kind", path=path))
        relation_refs, requirement_refs = section["relation_refs"], section["requirement_refs"]
        if not _unique_string_list(relation_refs):
            failures.append(_failure("invalid_relation_refs", path=path))
            relation_refs = []
        if not _unique_string_list(requirement_refs):
            failures.append(_failure("invalid_requirement_refs", path=path))
            requirement_refs = []
        unknown_relations = sorted(set(relation_refs) - set(relation_by_id))
        unknown_requirements = sorted(set(requirement_refs) - requirement_ids)
        if unknown_relations:
            failures.append(_failure("unknown_documentary_relation_ref", path=path,
                                     refs=unknown_relations))
        if unknown_requirements:
            failures.append(_failure("unknown_documentary_requirement_ref", path=path,
                                     refs=unknown_requirements))
        referenced_relations.update(set(relation_refs) & set(relation_by_id))
        referenced_requirements.update(set(requirement_refs) & requirement_ids)
        text = section["text"]
        if not isinstance(text, str) or not 1 <= len(text) <= MAX_SECTION_CHARS:
            failures.append(_failure("invalid_documentary_text", path=path))
            text = ""
        total_chars += len(text)
        normalized_text = semantic_support_s1.normalize_text(text) if text else ""
        section_spans = []
        if not _unique_string_list(section["evidence_refs"], maximum=8):
            failures.append(_failure("invalid_section_evidence_refs", path=path))
        elif set(section["evidence_refs"]) - set(evidence_by_id):
            failures.append(_failure("unknown_section_evidence_ref", path=path))
        claims = section["claims"]
        if not isinstance(claims, list) or not 1 <= len(claims) <= MAX_CLAIMS_PER_SECTION:
            failures.append(_failure("invalid_claim_cardinality", path=path))
            continue
        claim_count += len(claims)
        section_has_conclusive_claim = False
        for claim_index, claim in enumerate(claims):
            claim_path = f"{path}.claims.{claim_index}"
            claim_required = {"claim_id", "statement", "section_span", "conditions",
                              "requirement_refs",
                              "relation_refs", "dimensions", "bindings",
                              "polarity", "evidence_refs", "support_mode", "evidence_anchors"}
            if not isinstance(claim, dict) or set(claim) != claim_required:
                failures.append(_failure("invalid_documentary_claim_shape", path=claim_path))
                continue
            claim_id = claim["claim_id"]
            if not isinstance(claim_id, str) or not claim_id or claim_id in claim_ids:
                failures.append(_failure("invalid_or_duplicate_claim_id", path=claim_path))
                continue
            claim_ids.add(claim_id)
            statement = claim["statement"]
            span = claim["section_span"]
            conditions = claim["conditions"]
            valid_statement = isinstance(statement, str) and bool(statement)
            valid_span = (isinstance(span, dict) and set(span) == {"start", "end"} and
                          isinstance(span.get("start"), int) and not isinstance(span.get("start"), bool) and
                          isinstance(span.get("end"), int) and not isinstance(span.get("end"), bool) and
                          0 <= span["start"] < span["end"] <= len(normalized_text))
            if not valid_statement or not valid_span:
                failures.append(_failure("invalid_claim_statement_span", claim_id=claim_id))
            elif normalized_text[span["start"]:span["end"]] != semantic_support_s1.normalize_text(statement):
                failures.append(_failure("statement_span_mismatch", claim_id=claim_id))
            else:
                section_spans.append((span["start"], span["end"], claim_id))
            if not _unique_string_list(conditions):
                failures.append(_failure("invalid_claim_conditions", claim_id=claim_id))
                conditions = []
            elif valid_statement and any(
                    semantic_support_s1.normalize_text(item) not in semantic_support_s1.normalize_text(statement)
                    for item in conditions):
                failures.append(_failure("claim_condition_not_in_statement", claim_id=claim_id))
            claim_relations = claim["relation_refs"]
            claim_requirements = claim["requirement_refs"]
            dimensions = claim["dimensions"]
            if not _unique_string_list(claim_relations, minimum=1) or set(claim_relations) - set(relation_by_id):
                failures.append(_failure("invalid_claim_relation_refs", claim_id=claim_id))
                claim_relations = []
            if (not _unique_string_list(claim_requirements, minimum=1) or
                    set(claim_requirements) - requirement_ids or
                    not set(claim_requirements) <= set(requirement_refs)):
                failures.append(_failure("invalid_claim_requirement_refs", claim_id=claim_id))
                claim_requirements = []
            if (not _unique_string_list(dimensions, minimum=1, maximum=len(DIMENSIONS)) or
                    not set(dimensions) <= DIMENSIONS):
                failures.append(_failure("invalid_claim_dimensions", claim_id=claim_id))
                dimensions = []
            bindings = claim["bindings"]
            if not isinstance(bindings, dict) or set(bindings) - (DIMENSIONS - {"detail"}) or not all(
                    isinstance(value, str) and value for value in bindings.values()):
                failures.append(_failure("invalid_claim_bindings", claim_id=claim_id))
                bindings = {}
            for relation_id in claim_relations:
                expected = relation_bindings(relation_by_id[relation_id])
                for dimension in set(dimensions) - {"detail"}:
                    if bindings.get(dimension) != expected.get(dimension):
                        failures.append(_failure(f"documentary_{dimension}_mismatch",
                                                 claim_id=claim_id, relation_id=relation_id))
            if claim["polarity"] not in POLARITIES:
                failures.append(_failure("invalid_claim_polarity", claim_id=claim_id))
            elif claim["polarity"] == "negated":
                failures.append(_failure("documentary_relation_negated", claim_id=claim_id))
            elif claim["polarity"] in {"conditional", "uncertain"}:
                unassessed.append(_failure("documentary_polarity_not_conclusive", claim_id=claim_id))
            claim_evidence = claim["evidence_refs"]
            if (not _unique_string_list(claim_evidence, minimum=1,
                                        maximum=MAX_EVIDENCE_PER_CLAIM) or
                    set(claim_evidence) - set(evidence_by_id)):
                failures.append(_failure("invalid_claim_evidence_refs", claim_id=claim_id))
                claim_evidence = []
            support_mode = claim["support_mode"]
            anchors = claim["evidence_anchors"]
            if support_mode not in SUPPORT_MODES or not isinstance(anchors, list) or len(anchors) > MAX_EVIDENCE_PER_CLAIM:
                failures.append(_failure("invalid_claim_support", claim_id=claim_id))
                continue
            if support_mode == "direct":
                if not anchors:
                    failures.append(_failure("direct_claim_anchor_missing", claim_id=claim_id))
                for anchor in anchors:
                    if not isinstance(anchor, dict) or set(anchor) != {"evidence_ref", "exact_text"}:
                        failures.append(_failure("invalid_evidence_anchor_shape", claim_id=claim_id))
                        continue
                    evidence_ref, exact = anchor["evidence_ref"], anchor["exact_text"]
                    source = evidence_by_id.get(evidence_ref)
                    if (evidence_ref not in claim_evidence or not isinstance(exact, str) or not exact or
                            source is None or _nfc_lines(exact) not in _nfc_lines(str(source.get("text", "")))):
                        failures.append(_failure("evidence_anchor_mismatch", claim_id=claim_id,
                                                 evidence_ref=evidence_ref))
                assessment = semantic_support_s1.assess_claim(
                    attempt_id, preflight["authorized_plan_fingerprint"], claim, evidence_by_id)
                generated_assessments.append(assessment)
                assessment_errors = semantic_support_s1.verify_assessment(
                    assessment, attempt_id, preflight["authorized_plan_fingerprint"],
                    claim, evidence_by_id)
                if assessment_errors:
                    failures.extend(_failure(code, claim_id=claim_id)
                                    for code in assessment_errors)
                elif assessment["aggregate_verdict"] == "unsupported":
                    failures.append(_failure("documentary_claim_unsupported", claim_id=claim_id))
                elif assessment["aggregate_verdict"] != "supported":
                    unassessed.append(_failure(
                        "semantic_support_not_evaluable", claim_id=claim_id,
                        reason_codes=assessment["reason_codes"]))
            elif support_mode == "bounded_inference":
                unassessed.append(_failure("bounded_inference_not_evaluable", claim_id=claim_id))
            else:
                unassessed.append(_failure("uncertainty_does_not_cover_requirement", claim_id=claim_id))
            if support_mode != "uncertainty" and claim["polarity"] == "affirmed":
                covered_relations.update(claim_relations)
                section_has_conclusive_claim = True
        ordered_spans = sorted(section_spans)
        for left, right in zip(ordered_spans, ordered_spans[1:]):
            if right[0] < left[1]:
                failures.append(_failure("incompatible_claim_span_overlap",
                                         claim_ids=[left[2], right[2]]))
        uncovered = [index for index, char in enumerate(normalized_text)
                     if not char.isspace() and not any(start <= index < end
                                                      for start, end, _ in section_spans)]
        if uncovered:
            unassessed.append(_failure("substantive_prose_coverage_not_evaluable",
                                       section_id=section_id))
        if section["kind"] != "uncertainty" and section_has_conclusive_claim:
            covered_requirements.update(requirement_refs)

    if claim_count > MAX_TOTAL_CLAIMS:
        failures.append(_failure("total_claim_cardinality_exceeded"))
    if total_chars > MAX_TOTAL_CHARS:
        failures.append(_failure("total_documentary_text_exceeded"))
    for relation_id in sorted(set(relation_by_id) - covered_relations):
        target = unassessed if relation_id in referenced_relations else failures
        target.append(_failure("documentary_relation_not_conclusively_covered"
                               if relation_id in referenced_relations else
                               "documentary_relation_omitted", relation_id=relation_id))
    for requirement_id in sorted(requirement_ids - covered_requirements):
        target = unassessed if requirement_id in referenced_requirements else failures
        target.append(_failure("documentary_requirement_not_conclusively_covered"
                               if requirement_id in referenced_requirements else
                               "documentary_requirement_omitted", requirement_id=requirement_id))

    prose = "\n\n".join(section.get("text", "") for section in sections
                         if isinstance(section, dict) and isinstance(section.get("text"), str))
    audit = tactical_audit if isinstance(tactical_audit, dict) else {
        "status": "not_assessable", "complete": False}
    if not _audit_positive(audit):
        negative = any(audit.get(key) for key in (
            "missing_facets", "missing_operational", "missing_details", "semantic_issues"))
        (failures if negative else unassessed).append(
            _failure("tactical_documentary_audit_failed" if negative else
                     "tactical_documentary_audit_not_assessable"))
    if done_reason == "length":
        unassessed.append(_failure("generation_truncated_length"))

    controls = {
        "preflight": preflight,
        "documentary_structure_and_coherence": {
            "status": "failed" if failures else "not_assessable" if unassessed else "passed",
            "checked_scope": sorted(checked), "failures": failures,
            "unassessed_scope": unassessed,
            "covered_relations": sorted(covered_relations),
            "covered_requirements": sorted(covered_requirements),
        },
        "tactical_documentary_audit": audit,
        "semantic_support_assessments": generated_assessments,
    }
    status = "blocked" if failures else "not_evaluable" if unassessed else "validated"
    reasons = [item["code"] for item in failures + unassessed]
    base.update(overall_status=status, promoted_answer=prose if status == "validated" else "",
                reasons=list(dict.fromkeys(reasons)), controls=controls,
                parsed_envelope=parsed, documentary_explanation=documentary,
                documentary_prose=prose, done_reason=done_reason)
    return base


def build_documentary_prompt(question, preflight, evidence):
    """Pure prompt builder; callers own the single transport invocation."""
    return {
        "system": (
            "Restituisci esclusivamente tactical_state_documentary_explanation_v1. "
            "Non rigenerare il piano. Usa soltanto relation, requirement ed evidence ID forniti. "
            "Ogni claim deve dichiarare bindings, polarità e supporto. Nessun retry o repair."),
        "user": canonical_json({
            "question": question,
            "authorized_plan_fingerprint": preflight["authorized_plan_fingerprint"],
            "canonical_relations": preflight["canonical_relations"],
            "projected_requirements": preflight["v2_preflight"].get("projected_requirements", []),
            "evidence": evidence,
        }),
    }
