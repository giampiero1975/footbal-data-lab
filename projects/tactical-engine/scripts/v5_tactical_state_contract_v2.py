#!/usr/bin/env python3
"""Offline Tactical State Contract v2 operational-relations extension.

V1 remains authoritative and unchanged.  This module adds deterministic
question-requirement projection and validation only; it performs no model,
service, corpus, or filesystem I/O.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from copy import deepcopy

import v5_tactical_state_contract_v1 as v1


SCHEMA = "tactical_state_contract_v2"
CONTRACT_VERSION = "2.0.0"
REQUIREMENT_SCHEMA = "tactical_relation_requirement_projection_v1"
RELATION_SCHEMA = "tactical_operational_relation_coverage_v1"
FINGERPRINT_RULE = "relation_requirement_projection:v1"
PHASE_RULE = "phase_term_map:v1"
POSITION_RULE = "position_term_exact_match:v1"
ALLOWED_RULE_IDS = {FINGERPRINT_RULE, PHASE_RULE, POSITION_RULE}

PHASE_TERM_MAP = {
    "in possesso": "possession",
    "fase offensiva": "possession",
    "non possesso": "non_possession",
    "fase difensiva": "non_possession",
    "transizione positiva": "positive_transition",
    "alla riconquista": "positive_transition",
    "transizione negativa": "negative_transition",
    "alla perdita": "negative_transition",
}


def normalize_term(value):
    """Representation-only normalization used by term IDs and fingerprints."""
    text = unicodedata.normalize("NFC", str(value or ""))
    text = text.replace("’", "'").replace("‘", "'").replace("`", "'")
    return re.sub(r"\s+", " ", text).strip().casefold()


def term_id(value):
    normalized = normalize_term(value)
    return "term:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def explicit_term(value):
    normalized = normalize_term(value)
    return {"term_id": term_id(value), "source_term": str(value),
            "normalized_term": normalized, "provenance": "explicit",
            "rule_id": None}


def unknown_term():
    return {"term_id": None, "source_term": None, "normalized_term": None,
            "provenance": "unknown", "rule_id": None}


def canonical_json(value):
    """Canonical representation for the restricted JSON projection types."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def requirement_fingerprint(projection):
    content = {key: projection[key] for key in (
        "schema", "requirement_id", "question_part_id", "classification",
        "required_dimensions", "actor_ref", "task", "space", "trigger",
        "purpose", "phase", "extraction_provenance")}
    return "sha256:" + hashlib.sha256(
        canonical_json(content).encode("utf-8")).hexdigest()


def _unique_terms(requirement, dimension):
    values = requirement.get(dimension + "_terms", [])
    normalized = {normalize_term(value): str(value) for value in values
                  if normalize_term(value)}
    return [normalized[key] for key in sorted(normalized)]


def _entities_by_label(state_contract, keys):
    result = {}
    for key in keys:
        for item in state_contract.get(key, []):
            label = normalize_term(item.get("label"))
            if label:
                result.setdefault(label, []).append(
                    {"id": item.get("id"), "kind": item.get("kind")})
    return result


def _resolve_actor(requirement, state_contract):
    terms = _unique_terms(requirement, "actor")
    if len(terms) != 1:
        return None
    matches = _entities_by_label(
        state_contract, ("actors", "role_refs", "candidate_actors")).get(
            normalize_term(terms[0]), [])
    return matches[0] if len(matches) == 1 else None


def _resolve_phase(terms):
    phases = {PHASE_TERM_MAP.get(normalize_term(term)) for term in terms}
    if None in phases:
        return None
    return next(iter(phases)) if len(phases) == 1 else None


def _resolve_position(space_term, state_contract):
    if not space_term:
        return None
    matches = []
    expected = normalize_term(space_term)
    for item in state_contract.get("position_slots", []):
        if expected in {normalize_term(item.get("label")), normalize_term(item.get("id"))}:
            matches.append({"id": item.get("id"), "kind": "position_slot"})
    return matches[0] if len(matches) == 1 else None


def project_relation_requirements(question_plan):
    """Return a stable projection; only explicit representable rows are mandatory."""
    if not isinstance(question_plan, dict):
        raise ValueError("invalid_question_plan")
    if "relation_requirements" not in question_plan:
        raise ValueError("relation_requirements_projection_absent")
    requirements = question_plan["relation_requirements"]
    state_contract = question_plan.get("state_contract")
    if not isinstance(requirements, list) or not isinstance(state_contract, dict):
        raise ValueError("invalid_relation_requirements_projection")
    requirement_ids = []
    allowed_dimensions = {"actor", "task", "space", "trigger", "purpose", "phase"}
    for requirement in requirements:
        if not isinstance(requirement, dict):
            raise ValueError("invalid_relation_requirement")
        requirement_id = requirement.get("requirement_id")
        if not isinstance(requirement_id, str) or not requirement_id.strip():
            raise ValueError("missing_requirement_id")
        requirement_type = requirement.get("requirement_type")
        specificity = requirement.get("specificity")
        required_dimensions = requirement.get("required_dimensions")
        if (not isinstance(requirement.get("question_part_id"), str) or
                not requirement["question_part_id"].strip() or
                not isinstance(requirement_type, str) or
                requirement_type not in {"explicit", "open", "inferred", "ambiguous"} or
                not isinstance(specificity, str) or
                specificity not in {"explicit_relation", "underspecified"} or
                not isinstance(required_dimensions, list) or
                any(not isinstance(item, str) or item not in allowed_dimensions
                    for item in required_dimensions)):
            raise ValueError("incomplete_relation_requirement_projection")
        requirement_ids.append(requirement_id)
    if len(requirement_ids) != len(set(requirement_ids)):
        raise ValueError("duplicate_requirement_id")
    projected = []
    for requirement in requirements:
        actor_ref = _resolve_actor(requirement, state_contract)
        task_terms = _unique_terms(requirement, "task")
        space_terms = _unique_terms(requirement, "space")
        trigger_terms = _unique_terms(requirement, "trigger")
        purpose_terms = _unique_terms(requirement, "purpose")
        phase_terms = _unique_terms(requirement, "phase")
        required = sorted(set(requirement.get("required_dimensions", [])))
        explicit = (requirement.get("requirement_type") == "explicit" and
                    requirement.get("specificity") == "explicit_relation")
        dimensions = {
            "actor": actor_ref is not None,
            "task": len(task_terms) == 1,
            "space": len(space_terms) == 1,
            "trigger": len(trigger_terms) == 1,
            "purpose": len(purpose_terms) == 1,
            "phase": len(phase_terms) == 1 and _resolve_phase(phase_terms) is not None,
        }
        representable = all(dimensions.get(name, False) for name in required)
        declared_type = requirement.get("requirement_type")
        classification = (
            "inferred" if declared_type == "inferred" else
            "ambiguous" if declared_type == "ambiguous" else
            "explicit_representable" if explicit and representable else
            "explicit_not_representable" if explicit else
            "underspecified" if requirement.get("specificity") == "underspecified" else
            "not_evaluable")
        space_term = explicit_term(space_terms[0]) if len(space_terms) == 1 else unknown_term()
        projection = {
            "schema": REQUIREMENT_SCHEMA,
            "requirement_id": requirement.get("requirement_id"),
            "question_part_id": requirement.get("question_part_id"),
            "classification": classification,
            "required_dimensions": required,
            "actor_ref": actor_ref,
            "task": explicit_term(task_terms[0]) if len(task_terms) == 1 else unknown_term(),
            "space": {"term": space_term,
                      "position_ref": _resolve_position(space_terms[0], state_contract)
                      if len(space_terms) == 1 else None},
            "trigger": explicit_term(trigger_terms[0]) if len(trigger_terms) == 1 else unknown_term(),
            "purpose": explicit_term(purpose_terms[0]) if len(purpose_terms) == 1 else unknown_term(),
            "phase": _resolve_phase(phase_terms),
            "extraction_provenance": {"provenance": "derived", "rule_id": FINGERPRINT_RULE},
        }
        projection["fingerprint"] = requirement_fingerprint(projection)
        projected.append(projection)
    return projected


def operational_relation_schema():
    """Return the exact JSON-schema fragment used for generated V2 relations."""
    typed_ref = {"type": "object", "additionalProperties": False,
                 "required": ["id", "kind"],
                 "properties": {"id": {"type": "string", "minLength": 1},
                                "kind": {"enum": ["actor_ref", "role_ref", "candidate_actor",
                                                    "position_slot", "phase_state",
                                                    "relation_requirement"]}}}
    term = {"type": "object", "additionalProperties": False,
            "required": ["term_id", "source_term", "normalized_term", "provenance", "rule_id"],
            "properties": {
                "term_id": {"type": ["string", "null"]},
                "source_term": {"type": ["string", "null"]},
                "normalized_term": {"type": ["string", "null"]},
                "provenance": {"enum": sorted(v1.PROVENANCE)},
                "rule_id": {"type": ["string", "null"]}}}
    relation = {"type": "object", "additionalProperties": False,
                "required": ["relation_id", "requirement_ref", "requirement_fingerprint",
                             "actor_ref", "task", "space", "trigger", "purpose",
                             "phase_state_ref", "assertion_mode", "provenance", "rule_id"],
                "properties": {
                    "relation_id": {"type": "string", "minLength": 1},
                    "requirement_ref": typed_ref,
                    "requirement_fingerprint": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"},
                    "actor_ref": typed_ref,
                    "task": term,
                    "space": {"type": "object", "additionalProperties": False,
                              "required": ["term", "position_ref"],
                              "properties": {"term": term,
                                             "position_ref": {"type": ["object", "null"]}}},
                    "trigger": term, "purpose": term,
                    "phase_state_ref": typed_ref,
                    "assertion_mode": {"enum": sorted(v1.ASSERTION_MODES)},
                    "provenance": {"enum": sorted(v1.PROVENANCE)},
                    "rule_id": {"type": ["string", "null"]}}}
    return {"type": "array", "items": relation}


def build_v2_plan(v1_plan, operational_relations=None):
    plan = deepcopy(v1_plan)
    plan["schema"] = SCHEMA
    plan["contract_version"] = CONTRACT_VERSION
    plan["operational_relations"] = list(operational_relations or [])
    return plan


def _term_matches(actual, expected):
    if not isinstance(actual, dict) or not isinstance(expected, dict):
        return False
    if expected.get("provenance") == "unknown":
        return actual.get("provenance") == "unknown" and actual.get("term_id") is None
    source = actual.get("source_term")
    if normalize_term(source) != actual.get("normalized_term"):
        return False
    if term_id(source) != actual.get("term_id"):
        return False
    return actual.get("term_id") == expected.get("term_id") and actual.get("provenance") in {"explicit", "derived"}


def _typed_ref_error(value, allowed_kinds):
    if not isinstance(value, dict) or set(value) != {"id", "kind"}:
        return True
    kind = value.get("kind")
    return (not isinstance(value.get("id"), str) or not value["id"].strip() or
            not isinstance(kind, str) or kind not in allowed_kinds)


def _term_errors(value, path):
    required = {"term_id", "source_term", "normalized_term", "provenance", "rule_id"}
    if not isinstance(value, dict) or set(value) != required:
        return [{"code": "invalid_operational_term_shape", "path": path}]
    provenance = value.get("provenance")
    rule_id = value.get("rule_id")
    if not isinstance(provenance, str) or provenance not in v1.PROVENANCE:
        return [{"code": "invalid_operational_term_provenance", "path": path}]
    if provenance == "unknown":
        if any(value.get(key) is not None for key in ("term_id", "source_term", "normalized_term", "rule_id")):
            return [{"code": "invalid_unknown_operational_term", "path": path}]
        return []
    if not all(isinstance(value.get(key), str) and value[key]
               for key in ("term_id", "source_term", "normalized_term")):
        return [{"code": "invalid_operational_term_value", "path": path}]
    if normalize_term(value["source_term"]) != value["normalized_term"] or term_id(value["source_term"]) != value["term_id"]:
        return [{"code": "invalid_operational_term_identity", "path": path}]
    if provenance == "derived":
        if not isinstance(rule_id, str) or rule_id not in ALLOWED_RULE_IDS:
            return [{"code": "invalid_operational_term_rule", "path": path}]
    elif rule_id is not None:
        return [{"code": "unexpected_operational_term_rule", "path": path}]
    return []


def _relation_shape_errors(relation, index):
    required = {"relation_id", "requirement_ref", "requirement_fingerprint", "actor_ref",
                "task", "space", "trigger", "purpose", "phase_state_ref",
                "assertion_mode", "provenance", "rule_id"}
    path = f"operational_relations.{index}"
    if not isinstance(relation, dict) or set(relation) != required:
        return [{"code": "invalid_operational_relation_shape", "path": path}]
    errors = []
    if not isinstance(relation["relation_id"], str) or not relation["relation_id"].strip():
        errors.append({"code": "invalid_operational_relation_id", "path": path})
    if _typed_ref_error(relation["requirement_ref"], {"relation_requirement"}):
        errors.append({"code": "invalid_requirement_ref", "path": path})
    if (not isinstance(relation["requirement_fingerprint"], str) or
            re.fullmatch(r"sha256:[0-9a-f]{64}", relation["requirement_fingerprint"]) is None):
        errors.append({"code": "invalid_requirement_fingerprint", "path": path})
    if _typed_ref_error(relation["actor_ref"], {"actor_ref", "role_ref", "candidate_actor"}):
        errors.append({"code": "invalid_actor_ref", "path": path})
    if _typed_ref_error(relation["phase_state_ref"], {"phase_state"}):
        errors.append({"code": "invalid_phase_state_ref", "path": path})
    for name in ("task", "trigger", "purpose"):
        errors.extend(_term_errors(relation[name], f"{path}.{name}"))
    space = relation["space"]
    if not isinstance(space, dict) or set(space) != {"term", "position_ref"}:
        errors.append({"code": "invalid_operational_space_shape", "path": f"{path}.space"})
    else:
        errors.extend(_term_errors(space["term"], f"{path}.space.term"))
        if space["position_ref"] is not None and _typed_ref_error(space["position_ref"], {"position_slot"}):
            errors.append({"code": "invalid_position_ref", "path": f"{path}.space.position_ref"})
    assertion_mode = relation["assertion_mode"]
    if not isinstance(assertion_mode, str) or assertion_mode not in v1.ASSERTION_MODES:
        errors.append({"code": "invalid_operational_assertion_mode", "path": path})
    provenance, rule_id = relation["provenance"], relation["rule_id"]
    if not isinstance(provenance, str) or provenance not in v1.PROVENANCE:
        errors.append({"code": "invalid_operational_relation_provenance", "path": path})
    elif provenance == "derived":
        if not isinstance(rule_id, str) or rule_id not in ALLOWED_RULE_IDS:
            errors.append({"code": "operational_relation_unknown_rule", "path": path})
    elif rule_id is not None:
        errors.append({"code": "unexpected_operational_relation_rule", "path": path})
    return errors


def validate_operational_relations(question_plan, applied_plan):
    """Validate V2 structure and exact coverage without semantic similarity."""
    failures, unassessed, checked = [], [], []
    if not isinstance(applied_plan, dict):
        return {"schema": RELATION_SCHEMA, "status": "failed", "checked_scope": [],
                "failures": [{"code": "invalid_applied_plan"}], "unassessed_scope": [],
                "projected_requirements": []}
    if applied_plan.get("schema") != SCHEMA or applied_plan.get("contract_version") != CONTRACT_VERSION:
        failures.append({"code": "invalid_v2_identity"})
    relations = applied_plan.get("operational_relations")
    if not isinstance(relations, list):
        failures.append({"code": "invalid_operational_relations_container"})
        relations = []
    for index, relation in enumerate(relations):
        failures.extend(_relation_shape_errors(relation, index))
    relation_ids = [item.get("relation_id") for item in relations
                    if isinstance(item, dict) and
                    isinstance(item.get("relation_id"), str) and
                    item["relation_id"].strip()]
    if len(relation_ids) != len(relations) or len(relation_ids) != len(set(relation_ids)):
        failures.append({"code": "duplicate_operational_relation_id"})
    if not isinstance(question_plan, dict) or "relation_requirements" not in question_plan:
        unassessed.append({"code": "relation_requirements_projection_absent"})
        projected = []
        projection_complete = False
    else:
        try:
            projected = project_relation_requirements(question_plan)
            projection_complete = True
        except ValueError as exc:
            target = (unassessed if str(exc) == "incomplete_relation_requirement_projection"
                      else failures)
            target.append({"code": str(exc)})
            projected = []
            projection_complete = False
    requirements = {item["requirement_id"]: item for item in projected}
    by_requirement = {}
    for index, relation in enumerate(relations):
        if _relation_shape_errors(relation, index):
            continue
        ref = relation.get("requirement_ref")
        req_id = ref.get("id") if isinstance(ref, dict) and ref.get("kind") == "relation_requirement" else None
        if req_id not in requirements:
            failures.append({"code": "unknown_relation_requirement", "index": index})
            continue
        by_requirement.setdefault(req_id, []).append(relation)
    state_by_id = {item.get("state_id"): item for item in applied_plan.get("phase_states", [])
                   if isinstance(item, dict)}
    entities = {item.get("id"): item for key in ("actors", "role_refs", "candidate_actors")
                for item in applied_plan.get(key, []) if isinstance(item, dict)}
    positions = {item.get("id"): item for item in applied_plan.get("position_slots", [])
                 if isinstance(item, dict)}
    for req_id, candidates in by_requirement.items():
        for relation in candidates:
            actor_ref = relation["actor_ref"]
            entity = entities.get(actor_ref["id"])
            if entity is None or entity.get("kind") != actor_ref["kind"]:
                failures.append({"code": "unresolved_operational_actor_ref", "requirement_id": req_id})
            phase_ref = relation["phase_state_ref"]
            if phase_ref["id"] not in state_by_id:
                failures.append({"code": "unresolved_operational_phase_state_ref", "requirement_id": req_id})
            position_ref = relation["space"]["position_ref"]
            if position_ref is not None:
                position = positions.get(position_ref["id"])
                if position is None or position.get("kind") != "position_slot":
                    failures.append({"code": "unresolved_operational_position_ref", "requirement_id": req_id})
    for requirement in projected:
        req_id = requirement["requirement_id"]
        classification = requirement["classification"]
        candidates = by_requirement.get(req_id, [])
        if classification != "explicit_representable":
            unassessed.append({"requirement_id": req_id, "classification": classification})
            continue
        checked.append(req_id)
        if not candidates:
            failures.append({"code": "explicit_operational_requirement_omitted", "requirement_id": req_id})
            continue
        if len(candidates) != 1:
            failures.append({"code": "duplicate_requirement_coverage", "requirement_id": req_id})
            continue
        relation = candidates[0]
        if relation.get("requirement_fingerprint") != requirement["fingerprint"]:
            failures.append({"code": "requirement_fingerprint_mismatch", "requirement_id": req_id})
        actor_ref = relation.get("actor_ref") or {}
        if actor_ref != requirement["actor_ref"]:
            failures.append({"code": "operational_actor_mismatch", "requirement_id": req_id})
        for dimension in ("task", "trigger", "purpose"):
            if dimension in requirement["required_dimensions"] and not _term_matches(relation.get(dimension), requirement[dimension]):
                failures.append({"code": f"operational_{dimension}_mismatch", "requirement_id": req_id})
        if "space" in requirement["required_dimensions"]:
            actual_space = relation.get("space") or {}
            if not _term_matches(actual_space.get("term"), requirement["space"]["term"]):
                failures.append({"code": "operational_space_mismatch", "requirement_id": req_id})
            expected_position = requirement["space"].get("position_ref")
            if expected_position is not None and actual_space.get("position_ref") != expected_position:
                failures.append({"code": "operational_position_mismatch", "requirement_id": req_id})
        phase_ref = relation.get("phase_state_ref") or {}
        state = state_by_id.get(phase_ref.get("id")) if phase_ref.get("kind") == "phase_state" else None
        if "phase" in requirement["required_dimensions"] and (state is None or state.get("phase") != requirement["phase"]):
            failures.append({"code": "operational_phase_mismatch", "requirement_id": req_id})
        if relation.get("provenance") in {"assumed", "unknown"}:
            failures.append({"code": "operational_relation_unverified_provenance", "requirement_id": req_id})
    if projection_complete and not projected:
        checked.append("verified_no_explicit_requirements")
    status = "failed" if failures else "not_assessable" if unassessed else "passed"
    return {"schema": RELATION_SCHEMA, "status": status,
            "checked_scope": checked, "failures": failures,
            "unassessed_scope": unassessed, "projected_requirements": projected}


def validate_contract(plan, question_plan=None):
    """Reuse every V1 rule, then validate the isolated V2 extension."""
    v1_view = deepcopy(plan)
    v1_view["schema"] = v1.SCHEMA
    v1_view.pop("operational_relations", None)
    structural = v1.validate_contract(v1_view)
    coverage = (validate_operational_relations(question_plan, plan)
                if question_plan is not None else
                {"schema": RELATION_SCHEMA, "status": "not_assessable",
                 "checked_scope": [], "failures": [], "unassessed_scope": [
                     {"code": "question_plan_required"}]})
    return {"schema": "tactical_state_validation_v2",
            "valid": structural["valid"] and coverage["status"] == "passed",
            "v1_structural_validation": structural,
            "operational_coverage": coverage}
