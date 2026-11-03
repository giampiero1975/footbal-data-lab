#!/usr/bin/env python3
"""Offline-only generative handoff for TSC V2 operational relations."""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy

import v5_tactical_state_contract_v1 as v1
import v5_tactical_state_contract_v2 as v2


SCHEMA = "tactical_state_generation_diagnostic_v2"


def _relation_id(requirement):
    identity = {"schema": v2.SCHEMA,
                "requirement_id": requirement["requirement_id"],
                "requirement_fingerprint": requirement["fingerprint"]}
    return "relation:" + hashlib.sha256(
        v2.canonical_json(identity).encode("utf-8")).hexdigest()


def _phase_state_id(phase):
    """One stable state per canonical phase; never generation/order dependent."""
    return "state:phase:" + phase


def _result(status, reasons, **extra):
    return {"status": status, "reasons": list(dict.fromkeys(reasons)), **extra}


def prepare_generation_request(question_plan):
    """Project requirements and materialize only authorized phase states."""
    try:
        projected = v2.project_relation_requirements(question_plan)
    except ValueError as exc:
        code = str(exc)
        status = "not_evaluable" if code in {
            "relation_requirements_projection_absent",
            "incomplete_relation_requirement_projection",
        } else "blocked"
        return _result(status, [code], projected_requirements=[])
    unassessed = [item for item in projected
                  if item.get("classification") != "explicit_representable"]
    if unassessed:
        return _result("not_evaluable",
                       ["requirement_" + item.get("classification", "not_evaluable")
                        for item in unassessed],
                       projected_requirements=projected)
    base = question_plan.get("state_contract") if isinstance(question_plan, dict) else None
    if not isinstance(base, dict):
        return _result("blocked", ["invalid_state_contract"],
                       projected_requirements=projected)
    applied = v2.build_v2_plan(base)
    states = applied.get("phase_states")
    if not isinstance(states, list):
        return _result("blocked", ["invalid_phase_states"],
                       projected_requirements=projected)
    phase_to_state = {}
    state_ids = set()
    for item in states:
        if not isinstance(item, dict) or not isinstance(item.get("state_id"), str):
            return _result("blocked", ["invalid_existing_phase_state"],
                           projected_requirements=projected)
        state_ids.add(item["state_id"])
        phase = item.get("phase")
        if phase and phase != "unknown":
            if phase in phase_to_state and phase_to_state[phase] != item["state_id"]:
                return _result("not_evaluable", ["ambiguous_existing_phase_state"],
                               projected_requirements=projected)
            phase_to_state[phase] = item["state_id"]
    relations = []
    for requirement in projected:
        phase = requirement.get("phase")
        if not isinstance(phase, str) or not phase:
            return _result("not_evaluable", ["phase_not_uniquely_resolved"],
                           projected_requirements=projected)
        state_id = phase_to_state.get(phase)
        if state_id is None:
            state_id = _phase_state_id(phase)
            if state_id in state_ids:
                return _result("blocked", ["phase_state_id_collision"],
                               projected_requirements=projected)
            states.append(v1.state(state_id, phase=phase))
            state_ids.add(state_id)
            phase_to_state[phase] = state_id
        relations.append({
            "relation_id": _relation_id(requirement),
            "requirement_ref": {"id": requirement["requirement_id"],
                                "kind": "relation_requirement"},
            "requirement_fingerprint": requirement["fingerprint"],
            "actor_ref": deepcopy(requirement["actor_ref"]),
            "task": deepcopy(requirement["task"]),
            "space": deepcopy(requirement["space"]),
            "trigger": deepcopy(requirement["trigger"]),
            "purpose": deepcopy(requirement["purpose"]),
            "phase_state_ref": {"id": state_id, "kind": "phase_state"},
            "assertion_mode": "executable",
            "provenance": "explicit",
            "rule_id": None,
        })
    applied["operational_relations"] = relations
    validation = v2.validate_contract(applied, question_plan)
    if not validation["v1_structural_validation"].get("valid"):
        return _result("blocked", ["materialized_plan_invalid_v1"],
                       projected_requirements=projected, validation=validation)
    if validation["operational_coverage"].get("status") != "passed":
        return _result("blocked", ["materialized_plan_invalid_v2"],
                       projected_requirements=projected, validation=validation)
    return _result("ready", [], projected_requirements=projected,
                   authorized_applied_plan=applied,
                   mandatory_relations=relations, validation=validation)


def generation_transport_schema():
    envelope = deepcopy(v1.generation_transport_schema())
    plan = envelope["properties"]["applied_plan"]
    plan["properties"]["schema"] = {"const": v2.SCHEMA}
    plan["properties"]["contract_version"] = {"const": v2.CONTRACT_VERSION}
    plan["properties"]["operational_relations"] = v2.operational_relation_schema()
    plan["required"] = list(dict.fromkeys(plan["required"] + ["operational_relations"]))
    return envelope


def parse_generation_content(raw_content):
    return v1.parse_generation_content(raw_content)


def _canonical_blocks(applied_plan, explanation, evidence_ids):
    if not isinstance(applied_plan, dict):
        return {"status": "failed", "required_scope": [], "checked_scope": [],
                "failures": [{"code": "invalid_canonical_applied_plan"}],
                "unassessed_scope": []}
    relations = applied_plan.get("operational_relations")
    if not isinstance(relations, list):
        return {"status": "failed", "required_scope": [], "checked_scope": [],
                "failures": [{"code": "invalid_canonical_relations_container"}],
                "unassessed_scope": []}
    lines = explanation.splitlines() if isinstance(explanation, str) else []
    blocks, index, failures = [], 0, []
    required_scope = []
    for relation_index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            failures.append({"code": "invalid_canonical_relation_shape",
                             "index": relation_index})
            continue
        relation_id = relation.get("relation_id")
        actor_ref = relation.get("actor_ref")
        task = relation.get("task")
        space = relation.get("space")
        trigger = relation.get("trigger")
        purpose = relation.get("purpose")
        phase_ref = relation.get("phase_state_ref")
        display_values = (
            isinstance(relation_id, str) and bool(relation_id),
            isinstance(actor_ref, dict) and isinstance(actor_ref.get("id"), str),
            isinstance(task, dict) and isinstance(task.get("source_term"), str),
            isinstance(space, dict) and isinstance(space.get("term"), dict) and
            isinstance(space["term"].get("source_term"), str),
            isinstance(trigger, dict) and isinstance(trigger.get("source_term"), str),
            isinstance(purpose, dict) and isinstance(purpose.get("source_term"), str),
            isinstance(phase_ref, dict) and isinstance(phase_ref.get("id"), str),
        )
        if not all(display_values):
            failures.append({"code": "invalid_canonical_relation_shape",
                             "index": relation_index})
            continue
        required_scope.append(relation_id)
        expected = [
            f"[REL {relation_id}]", f"Attore: {actor_ref['id']}",
            f"Compito: {task['source_term']}", f"Spazio: {space['term']['source_term']}",
            f"Trigger: {trigger['source_term']}", f"Finalità: {purpose['source_term']}",
            f"Fase: {applied_plan_state_phase(applied_plan, phase_ref['id'])}",
        ]
        if lines[index:index + len(expected)] != expected:
            failures.append({"code": "canonical_relation_block_mismatch",
                             "relation_id": relation_id})
            continue
        index += len(expected)
        if index >= len(lines) or not lines[index].startswith("Evidenze: "):
            failures.append({"code": "canonical_evidence_line_missing",
                             "relation_id": relation_id})
            continue
        cited = [token[1:-1] for token in lines[index][10:].split()
                 if token.startswith("[F") and token.endswith("]")]
        if not cited or any(item not in evidence_ids for item in cited):
            failures.append({"code": "invalid_canonical_evidence_id",
                             "relation_id": relation_id})
        index += 1
        if index < len(lines) and lines[index] == "":
            index += 1
        blocks.append(relation_id)
    if index != len(lines):
        failures.append({"code": "noncanonical_free_prose"})
    status = "failed" if failures else "passed" if relations else "not_assessable"
    return {"status": status, "required_scope": required_scope,
            "checked_scope": blocks, "failures": failures,
            "unassessed_scope": [] if relations else ["no_operational_relations"]}


def applied_plan_state_phase(plan, state_id):
    phase_states = plan.get("phase_states", []) if isinstance(plan, dict) else []
    if not isinstance(phase_states, list):
        return "unknown"
    matches = [item.get("phase") for item in phase_states
               if isinstance(item, dict) and item.get("state_id") == state_id]
    return matches[0] if len(matches) == 1 else "unknown"


def generation_diagnostic(question_plan, raw_content, evidence_ids,
                          done_reason=None, tactical_audit=None,
                          transport_error=None, preflight=None):
    preflight = preflight or prepare_generation_request(question_plan)
    empty = {"overall_status": preflight["status"], "promoted_answer": "",
             "raw_model_content": raw_content, "reasons": preflight["reasons"],
             "controls": {"preflight": preflight}}
    if preflight["status"] != "ready" or transport_error is not None:
        if transport_error is not None:
            empty["overall_status"] = "not_evaluable"
            empty["reasons"] = ["transport_error"]
        return empty
    parsed, normalizations, parse_errors = parse_generation_content(raw_content)
    if parse_errors or not isinstance(parsed, dict):
        empty.update(overall_status="not_evaluable", reasons=parse_errors or ["invalid_envelope"],
                     normalizations=normalizations)
        return empty
    plan = parsed.get("applied_plan")
    explanation = parsed.get("explanation")
    structural = v2.validate_contract(plan, question_plan)
    question = v1.compare_question_and_applied_plan(question_plan, plan)
    operational = structural["operational_coverage"]
    alignment = _canonical_blocks(plan if isinstance(plan, dict) else {}, explanation, set(evidence_ids))
    audit = tactical_audit if isinstance(tactical_audit, dict) else {
        "status": "not_assessable", "complete": False}
    controls = {"preflight": preflight, "structural_v1_v2": structural,
                "question_compatibility": question, "operational_coverage": operational,
                "plan_prose_alignment": alignment, "tactical_documentary_audit": audit}
    audit_status = audit.get("status")
    audit_negative_details = any(audit.get(key) for key in (
        "missing_facets", "missing_operational", "missing_details", "semantic_issues"))
    audit_explicit_negative = audit_status not in {None, "not_assessable"}
    audit_positive = (audit.get("complete") is True and not audit_negative_details and
                      audit_status is None)
    demonstrated = (not structural.get("valid") or question.get("status") == "failed" or
                    operational.get("status") == "failed" or alignment["status"] == "failed" or
                    audit_explicit_negative or audit_negative_details)
    unassessed = (question.get("status") in {"incomplete", "not_assessable"} or
                  operational.get("status") == "not_assessable" or
                  alignment["status"] == "not_assessable" or not audit_positive)
    truncated = done_reason == "length"
    status = "blocked" if demonstrated else "not_evaluable" if unassessed else "validated"
    if truncated and status == "validated":
        status = "not_evaluable"
    reasons = []
    for value in controls.values():
        for key in ("failures", "missing", "unassessed_scope"):
            for item in value.get(key, []) if isinstance(value, dict) else []:
                reasons.append(item.get("code") if isinstance(item, dict) else str(item))
    if audit_explicit_negative:
        reasons.append("tactical_documentary_audit_negative")
    if audit_negative_details:
        reasons.append("tactical_documentary_audit_failed")
    if not audit_positive and not (audit_explicit_negative or audit_negative_details):
        reasons.append("tactical_documentary_audit_not_assessable")
    if truncated:
        reasons.append("generation_truncated_length")
    promoted = explanation if status == "validated" else ""
    return {"schema": SCHEMA, "overall_status": status, "promoted_answer": promoted,
            "raw_model_content": raw_content, "normalizations": normalizations,
            "done_reason": done_reason, "reasons": list(dict.fromkeys(filter(None, reasons))),
            "controls": controls, "parsed_envelope": parsed}
