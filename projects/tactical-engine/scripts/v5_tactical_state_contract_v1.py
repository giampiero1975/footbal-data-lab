#!/usr/bin/env python3
"""Deterministic Tactical State Contract v1 (no model, service or corpus I/O)."""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy

SCHEMA = "tactical_state_contract_v1"
CONTRACT_VERSION = "1.1.0"
PROVENANCE = {"explicit", "derived", "assumed", "unknown"}
SEVERITIES = {"BLOCKING", "RECOVERABLE", "QUALIFICATION_REQUIRED", "ADVISORY"}
PHASES = {"possession", "non_possession", "positive_transition", "negative_transition", "set_piece", "unknown"}
PRESENCE = {"on_field", "off_field", "unavailable", "unknown"}
EVENT_TYPES = {"substitution", "expulsion", "rotation"}
ENTITY_KINDS = {"actor_ref", "role_ref", "position_slot", "candidate_actor"}
SUBSTITUTION_MODES = {"standard_no_reentry", "rolling", "unknown"}
ASSERTION_MODES = {"question_observation", "conditional", "executable"}

FORMATION_SLOTS = {
    "4-3-3": ("gk", "rb", "rcb", "lcb", "lb", "dm", "rcm", "lcm", "rw", "cf", "lw"),
    "3-5-2": ("gk", "rcb", "cb", "lcb", "rwb", "rcm", "dm", "lcm", "lwb", "rf", "lf"),
}
SAFE_ENUM_ALIASES = {
    "in_possesso": "possession", "possesso": "possession",
    "non_possesso": "non_possession", "non possesso": "non_possession",
    "transizione_positiva": "positive_transition", "transizione positiva": "positive_transition",
    "transizione_negativa": "negative_transition", "transizione negativa": "negative_transition",
    "sostituzione": "substitution", "espulsione": "expulsion", "rotazione": "rotation",
}

GENERATION_TRANSPORT_SCHEMA = "tactical_state_generation_v1"
GENERATION_STATUSES = {"validated", "partial", "blocked", "not_evaluable"}


def generation_transport_schema():
    """Return the Ollama transport schema; the domain remains this contract."""
    domain_fields = {
        "schema": {"const": SCHEMA},
        "contract_version": {"type": "string"},
        "scenario_id": {"type": "string"},
        "question": {"type": "object"},
        "formations": {"type": "array", "items": {"type": "object"}},
        "effective_players": {"type": "object"},
        "substitution_mode": {"type": "object"},
        "actors": {"type": "array", "items": {"type": "object"}},
        "role_refs": {"type": "array", "items": {"type": "object"}},
        "position_slots": {"type": "array", "items": {"type": "object"}},
        "candidate_actors": {"type": "array", "items": {"type": "object"}},
        "events": {"type": "array", "items": {"type": "object"}},
        "phase_states": {"type": "array", "items": {"type": "object"}},
        "structural_mappings": {"type": "array", "items": {"type": "object"}},
        "constraints": {"type": "array", "items": {"type": "object"}},
        "trace": {"type": "object"},
        "scenarios": {"type": "array"},
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["applied_plan", "explanation"],
        "properties": {
            "applied_plan": {
                "type": "object",
                "required": list(domain_fields),
                "properties": domain_fields,
                "additionalProperties": True,
            },
            "explanation": {"type": "string"},
        },
    }


def parse_generation_content(raw_content):
    """Parse JSON with representation-only normalization and no semantic repair."""
    if not isinstance(raw_content, str) or not raw_content.strip():
        return None, [], [issue("empty_model_output", "BLOCKING", "transport", "Output del modello vuoto.")]
    candidate = raw_content.strip()
    changes = []
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", candidate, re.I | re.S)
    if fenced:
        candidate = fenced.group(1).strip()
        changes.append({"path": "transport", "rule_id": "strip_outer_json_fence:v1"})
    try:
        parsed = json.loads(candidate)
    except (TypeError, ValueError) as exc:
        return None, changes, [issue("invalid_generation_json", "BLOCKING", "transport", str(exc))]
    errors = []
    if not isinstance(parsed, dict):
        errors.append(issue("invalid_generation_envelope", "BLOCKING", "transport", "L'output deve essere un oggetto JSON."))
        return None, changes, errors
    if set(parsed) != {"applied_plan", "explanation"}:
        errors.append(issue("invalid_generation_fields", "BLOCKING", "transport", "Campi di trasporto mancanti o inattesi."))
    if not isinstance(parsed.get("applied_plan"), dict):
        errors.append(issue("invalid_applied_plan", "BLOCKING", "applied_plan", "Piano applicato assente o non strutturato."))
    if not isinstance(parsed.get("explanation"), str) or not parsed.get("explanation", "").strip():
        errors.append(issue("invalid_explanation", "BLOCKING", "explanation", "Spiegazione assente o vuota."))
    return parsed if not errors else None, changes, errors


def validate_generation_shape(applied_plan):
    """Validate JSON container types only; domain rules stay in validate_contract()."""
    issues = []
    object_fields = ("question", "effective_players", "substitution_mode", "trace")
    object_list_fields = ("formations", "actors", "role_refs", "position_slots",
                          "candidate_actors", "events", "phase_states",
                          "structural_mappings", "constraints")
    for key in object_fields:
        if key in applied_plan and not isinstance(applied_plan[key], dict):
            issues.append(issue("invalid_nested_type", "BLOCKING", key, "È richiesto un oggetto JSON."))
    for key in object_list_fields:
        value = applied_plan.get(key)
        if value is None:
            continue
        if not isinstance(value, list):
            issues.append(issue("invalid_nested_type", "BLOCKING", key, "È richiesto un array JSON."))
            continue
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                issues.append(issue("invalid_nested_item_type", "BLOCKING", f"{key}.{index}", "È richiesto un oggetto JSON."))
    if "scenarios" in applied_plan and not isinstance(applied_plan["scenarios"], list):
        issues.append(issue("invalid_nested_type", "BLOCKING", "scenarios", "È richiesto un array JSON."))
    for index, state_item in enumerate(applied_plan.get("phase_states", []) if isinstance(applied_plan.get("phase_states", []), list) else []):
        if not isinstance(state_item, dict):
            continue
        for key in ("sequence", "formation", "effective_players", "presence_complete"):
            if key in state_item and not isinstance(state_item[key], dict):
                issues.append(issue("invalid_nested_type", "BLOCKING", f"phase_states.{index}.{key}", "È richiesto un oggetto JSON."))
        for key in ("actor_presence", "assignments"):
            if key in state_item and not isinstance(state_item[key], list):
                issues.append(issue("invalid_nested_type", "BLOCKING", f"phase_states.{index}.{key}", "È richiesto un array JSON."))
    typed_refs = {
        "events": ("out_ref", "in_ref", "subject_ref"),
        "structural_mappings": ("from_slot_ref", "to_slot_ref"),
    }
    for collection, fields in typed_refs.items():
        values = applied_plan.get(collection, [])
        if not isinstance(values, list):
            continue
        for index, item in enumerate(values):
            if not isinstance(item, dict):
                continue
            for key in fields:
                if key in item and item[key] is not None and not isinstance(item[key], dict):
                    issues.append(issue("invalid_typed_ref_shape", "BLOCKING", f"{collection}.{index}.{key}", "Il riferimento deve essere un oggetto JSON."))
    return {"schema": "tactical_generation_shape_validation_v1",
            "valid": not issues, "issues": issues}


def _domain_plan(plan):
    if isinstance(plan, dict) and isinstance(plan.get("state_contract"), dict):
        return plan["state_contract"]
    return plan if isinstance(plan, dict) else {}


def _explicit_values(plan, key):
    return {item.get("value") for item in plan.get(key, [])
            if isinstance(item, dict) and item.get("provenance") == "explicit" and item.get("value") is not None}


def _event_signature(event):
    def identifier(name):
        value = event.get(name)
        return value.get("id") if isinstance(value, dict) else None
    return (event.get("type"), identifier("out_ref"), identifier("in_ref"),
            identifier("subject_ref"), event.get("actor_label"))


def compare_question_and_applied_plan(question_plan, applied_plan):
    """Check only explicit question facts; unknown data never becomes a conflict."""
    question_plan = _domain_plan(question_plan)
    failures, missing, checked = [], [], []
    required_fields = ("schema", "contract_version", "actors", "events", "phase_states")
    for key in required_fields:
        if key not in applied_plan:
            missing.append({"code": "missing_contract_field", "path": key})
    expected_formations = _explicit_values(question_plan, "formations")
    actual_formations = _explicit_values(applied_plan, "formations")
    checked.append("explicit_formations")
    for formation in sorted(expected_formations - actual_formations):
        failures.append({"code": "explicit_formation_missing", "value": formation})
    expected_players = question_plan.get("effective_players", {})
    if expected_players.get("provenance") == "explicit":
        checked.append("effective_players")
        if applied_plan.get("effective_players", {}).get("value") != expected_players.get("value"):
            failures.append({"code": "effective_players_mismatch", "expected": expected_players.get("value")})
    expected_actors = {item.get("id") for item in question_plan.get("actors", [])
                       if item.get("provenance") == "explicit"}
    actual_actors = {item.get("id") for item in applied_plan.get("actors", [])}
    checked.append("explicit_actors")
    for actor_id in sorted(expected_actors - actual_actors):
        failures.append({"code": "explicit_actor_missing", "actor_ref": actor_id})
    actual_events = {_event_signature(item) for item in applied_plan.get("events", [])}
    for event in question_plan.get("events", []):
        if event.get("provenance") != "explicit":
            continue
        checked.append("explicit_event:" + str(event.get("event_id")))
        if _event_signature(event) not in actual_events:
            failures.append({"code": "explicit_event_mismatch", "event_id": event.get("event_id")})
    if failures:
        status = "failed"
    elif missing:
        status = "incomplete"
    else:
        status = "passed"
    return {"schema": "tactical_question_alignment_v1", "status": status,
            "checked_scope": checked, "failures": failures, "missing": missing}


def compare_plan_and_explanation(applied_plan, explanation):
    """Detect explicit structural contradictions, not general semantic equivalence."""
    text = " ".join(str(explanation or "").split()).casefold()
    failures, checked, required, unassessed = [], [], [], []
    allowed_formations = _explicit_values(applied_plan, "formations")
    final = applied_plan.get("final_formation", {})
    if isinstance(final, dict) and final.get("value"):
        required.append("final_formation")
        allowed_formations.add(final["value"])
        checked.append("final_formation")
        if final["value"].casefold() not in text:
            failures.append({"code": "final_formation_not_explained", "value": final["value"]})
    mentioned_formations = set(re.findall(r"(?<!\d)(?:[1-9]-){2,3}[1-9](?!\d)", text))
    for formation in sorted(mentioned_formations - allowed_formations):
        failures.append({"code": "explanation_formation_mismatch", "value": formation})
    actor_numbers = {match.group(1) for item in applied_plan.get("actors", [])
                     if (match := re.search(r"\b(\d{1,2})\b", str(item.get("label", ""))))}
    for number in re.findall(r"\b(?:numero|n[.°]?)\s*(\d{1,2})\b", text):
        checked.append("actor_number:" + number)
        if number not in actor_numbers:
            failures.append({"code": "explanation_unknown_actor", "number": number})
    substitutions = [item for item in applied_plan.get("events", []) if item.get("type") == "substitution"]
    entities = {item.get("id"): item for key in ("actors", "candidate_actors") for item in applied_plan.get(key, [])}
    for event in substitutions:
        out_id = (event.get("out_ref") or {}).get("id")
        in_id = (event.get("in_ref") or {}).get("id")
        out_label = str((entities.get(out_id) or {}).get("label", "")).casefold()
        in_label = str((entities.get(in_id) or {}).get("label", "")).casefold()
        relation = "substitution:" + str(event.get("event_id"))
        required.append(relation)
        checked.append(relation + ":actor_mentions")
        if out_label and in_label and not (out_label in text and in_label in text):
            failures.append({"code": "substitution_not_explained", "event_id": event.get("event_id")})
        unassessed.append(relation + ":direction_and_role_effect")
    for event in applied_plan.get("events", []):
        if event.get("type") in {"expulsion", "rotation"}:
            relation = str(event.get("type")) + ":" + str(event.get("event_id"))
            required.append(relation)
            unassessed.append(relation)
    if applied_plan.get("structural_mappings"):
        required.append("structural_mappings")
        unassessed.append("structural_mappings")
    if any(state_item.get("assignments") for state_item in applied_plan.get("phase_states", [])
           if isinstance(state_item, dict)):
        required.append("phase_assignments")
        unassessed.append("phase_assignments")
    coverage_sufficient = bool(required) and not unassessed
    if failures:
        status = "failed"
    elif not coverage_sufficient:
        status = "not_assessable"
    else:
        status = "passed"
    return {"schema": "tactical_plan_prose_alignment_v1",
            "status": status, "checked_scope": checked, "required_scope": required,
            "unassessed_scope": unassessed, "coverage_sufficient": coverage_sufficient,
            "failures": failures,
            "semantic_support_verified": False}


def generation_diagnostic(question_plan, raw_content, done_reason=None, tactical_audit=None,
                          transport_error=None):
    """Compose four independent controls and a fail-closed promotion decision."""
    normalizations = []
    if transport_error:
        transport_issues = [issue("generation_transport_error", "BLOCKING", "transport", str(transport_error))]
        parsed = None
    else:
        parsed, normalizations, transport_issues = parse_generation_content(raw_content)
    if done_reason == "length":
        transport_issues.append(issue("generation_truncated", "BLOCKING", "transport", "Output troncato dal limite di generazione."))
    if parsed is None or transport_issues:
        structural = {"schema": "tactical_state_validation_v1", "valid": False,
                      "issues": transport_issues, "counts": {level: sum(x["severity"] == level for x in transport_issues) for level in SEVERITIES}}
        question_alignment = {"schema": "tactical_question_alignment_v1", "status": "not_assessable", "checked_scope": [], "failures": [], "missing": []}
        prose_alignment = {"schema": "tactical_plan_prose_alignment_v1", "status": "not_assessable", "checked_scope": [], "required_scope": [], "unassessed_scope": [], "coverage_sufficient": False, "failures": [], "semantic_support_verified": False}
        audit = tactical_audit or {"status": "not_assessable"}
        status = "not_evaluable"
        explanation = ""
        applied_plan = None
    else:
        applied_plan, explanation = parsed["applied_plan"], parsed["explanation"].strip()
        try:
            shape_validation = validate_generation_shape(applied_plan)
            if not shape_validation["valid"]:
                raise TypeError("; ".join(f"{item['path']}: {item['message']}" for item in shape_validation["issues"]))
            applied_plan, contract_changes = normalize_contract(applied_plan)
            normalizations.extend(contract_changes)
            structural = validate_contract(applied_plan)
            question_alignment = compare_question_and_applied_plan(question_plan, applied_plan)
            prose_alignment = compare_plan_and_explanation(applied_plan, explanation)
            audit = tactical_audit or {"status": "not_assessable"}
            audit_passed = audit.get("complete") is True
            demonstrated_failure = (not structural["valid"]
                                    or question_alignment["status"] in {"failed", "incomplete"}
                                    or prose_alignment["status"] == "failed"
                                    or audit.get("complete") is False)
            mandatory_unassessed = (question_alignment["status"] == "not_assessable"
                                    or prose_alignment["status"] == "not_assessable"
                                    or audit.get("complete") is None)
            status = "blocked" if demonstrated_failure else "not_evaluable" if mandatory_unassessed else "validated" if audit_passed else "not_evaluable"
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            shape_issues = (shape_validation.get("issues", []) if "shape_validation" in locals() else [])
            if not shape_issues:
                shape_issues = [issue("invalid_contract_shape", "BLOCKING", "applied_plan", str(exc))]
            structural = {"schema": "tactical_state_validation_v1", "valid": False,
                          "issues": shape_issues,
                          "counts": {level: sum(item["severity"] == level for item in shape_issues) for level in SEVERITIES}}
            question_alignment = {"schema": "tactical_question_alignment_v1", "status": "not_assessable", "checked_scope": [], "failures": [], "missing": []}
            prose_alignment = {"schema": "tactical_plan_prose_alignment_v1", "status": "not_assessable", "checked_scope": [], "required_scope": [], "unassessed_scope": [], "coverage_sufficient": False, "failures": [], "semantic_support_verified": False}
            audit = tactical_audit or {"status": "not_assessable"}
            status = "not_evaluable"
    controls = {"structural_validity": structural,
                "question_compatibility": question_alignment,
                "plan_prose_alignment": prose_alignment,
                "tactical_documentary_audit": audit}
    passed = [name for name, result in controls.items()
              if result.get("valid") is True or result.get("status") == "passed" or result.get("complete") is True]
    failed = [name for name, result in controls.items()
              if result.get("valid") is False or result.get("status") in {"failed", "incomplete"}
              or result.get("complete") is False]
    unassessed = [name for name, result in controls.items()
                  if result.get("status") == "not_assessable"]
    reasons = [item["code"] for item in structural.get("issues", []) if item.get("severity") == "BLOCKING"]
    reasons.extend(item["code"] for item in question_alignment.get("failures", []))
    reasons.extend(item["code"] for item in question_alignment.get("missing", []))
    reasons.extend(item["code"] for item in prose_alignment.get("failures", []))
    if prose_alignment.get("status") == "not_assessable":
        reasons.append("plan_prose_alignment_not_assessable")
    if question_alignment.get("status") == "not_assessable":
        reasons.append("question_compatibility_not_assessable")
    if audit.get("complete") is None:
        reasons.append("tactical_documentary_audit_not_assessable")
    if audit.get("complete") is False:
        reasons.append("tactical_documentary_audit_failed")
    return {"transport_schema": GENERATION_TRANSPORT_SCHEMA,
            "raw_model_content": raw_content if isinstance(raw_content, str) else "",
            "parsed_output": parsed, "applied_plan": applied_plan,
            "normalizations": normalizations, "controls": controls,
            "overall_status": status, "passed_scope": passed,
            "failed_scope": failed, "unassessed_scope": unassessed,
            "reasons": list(dict.fromkeys(reasons)),
            "promoted_answer": explanation if status == "validated" else ""}


def value(item=None, provenance="unknown", rule_id=None):
    if provenance not in PROVENANCE:
        raise ValueError(f"invalid provenance: {provenance}")
    if provenance == "unknown":
        item = None
    result = {"value": item, "provenance": provenance}
    if rule_id is not None:
        result["rule_id"] = rule_id
    return result


def ref(identifier, kind):
    return {"id": identifier, "kind": kind}


def entity(identifier, kind, label, provenance, rule_id=None, availability="unknown",
           team=None, team_provenance="unknown", team_rule_id=None):
    if kind not in ENTITY_KINDS:
        raise ValueError(f"invalid entity kind: {kind}")
    result = {"id": identifier, "kind": kind, "label": label,
              "provenance": provenance, "availability": availability,
              "team": value(team, team_provenance, team_rule_id)}
    if rule_id is not None:
        result["rule_id"] = rule_id
    return result


def presence(actor_ref, status="unknown", provenance="unknown", rule_id=None):
    return {"actor_ref": actor_ref, "status": value(status, provenance, rule_id)}


def state(state_id, sequence=None, sequence_provenance="unknown", phase="unknown",
          actor_presence=None, assignments=None, formation=None, effective_players=None,
          presence_complete=False):
    sequence_value = value(sequence, sequence_provenance,
                           "explicit_state_order:v1" if sequence_provenance == "derived" else None)
    return {
        "state_id": state_id, "sequence": sequence_value, "phase": phase,
        "actor_presence": list(actor_presence or []), "assignments": list(assignments or []),
        "formation": formation or value(), "effective_players": effective_players or value(),
        "presence_complete": value(bool(presence_complete), "explicit") if presence_complete else value(),
        "provenance": "explicit",
    }


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.casefold()).strip("_") or "unknown"


def _formation_slots(formation, side="own"):
    return [entity(f"slot:{side}:{formation}:{slot}", "position_slot", slot, "derived",
                   rule_id=f"formation_slots:{formation}:v1", availability="not_applicable",
                   team=side, team_provenance="derived", team_rule_id="formation_side:v1")
            for slot in FORMATION_SLOTS.get(formation, ())]


def _explicit_actor_refs(question):
    numbers = set(re.findall(r"\b(?:numero|n\.)\s*(\d{1,2})\b", question, re.I))
    for pattern in (
            r"(?:esce|togli(?:e|ere)?)\s+(?:il\s+)?(\d{1,2})\b",
            r"(?:entra|inserisc(?:e|o|i))\s+(?:il\s+)?(\d{1,2})\b"):
        numbers.update(re.findall(pattern, question, re.I))
    return [entity(f"actor:explicit:number:{number}", "actor_ref", f"numero {number}",
                   "explicit", availability="unknown")
            for number in sorted(numbers)]


def _explicit_role_refs(roles):
    return [entity(f"role:explicit:{_slug(role)}", "role_ref", role, "explicit",
                   availability="not_applicable") for role in roles]


def _effective_players(question):
    match = re.search(r"\b(?:siamo|siete|squadra)\s+in\s+(10|9|8)\b|\bin\s+(10|9|8)\s+(?:uomini|giocatori)\b", question, re.I)
    if match:
        return value(int(next(group for group in match.groups() if group)), "explicit")
    return value()


def _events(question, actors):
    events = []
    actor_by_number = {item["label"].split()[-1]: item["id"] for item in actors}
    for index, match in enumerate(re.finditer(
            r"(?:esce|togli(?:e|ere)?)\s+(?:il\s+)?(?:numero\s+)?(\d{1,2}).{0,35}?(?:entra|inserisc(?:e|o|i))\s+(?:il\s+)?(?:numero\s+)?(\d{1,2})",
            question, re.I), 1):
        outgoing, incoming = match.groups()
        events.append({"event_id": f"event:substitution:{index}", "type": "substitution",
                       "from_state_id": None, "to_state_id": None,
                       "out_ref": ref(actor_by_number[outgoing], "actor_ref"),
                       "in_ref": ref(actor_by_number[incoming], "actor_ref"),
                       "assertion_mode": "question_observation", "cardinality_delta": 0,
                       "provenance": "explicit"})
    expulsion_match = re.search(r"(?:espuls[oa]|cartellino rosso)(?:\s+(?:al|per il|del))?\s*(numero\s+\d{1,2})?", question, re.I)
    if expulsion_match:
        label = (expulsion_match.group(1) or "attore non identificato").strip()
        number = re.search(r"\d{1,2}", label)
        actor_id = actor_by_number.get(number.group()) if number else None
        events.append({"event_id": "event:expulsion:1", "type": "expulsion",
                       "from_state_id": None, "to_state_id": None,
                       "subject_ref": ref(actor_id, "actor_ref") if actor_id else None,
                       "actor_label": label, "team": value(), "temporal_relation": value(),
                       "assertion_mode": "question_observation", "cardinality_delta": -1,
                       "provenance": "explicit"})
    for number, movement in re.findall(
            r"(?:numero|n\.)\s*(\d{1,2}).{0,25}?\b(si\s+abbassa|si\s+alza|stringe|si\s+allarga)\b",
            question, re.I):
        events.append({"event_id": f"event:rotation:{len(events)+1}", "type": "rotation",
                       "from_state_id": None, "to_state_id": None,
                       "subject_ref": ref(actor_by_number[number], "actor_ref"),
                       "movement": value(movement.casefold(), "explicit"),
                       "assertion_mode": "question_observation", "cardinality_delta": 0,
                       "provenance": "explicit"})
    return events


def build_question_plan(question, formations=None, roles=None, scenarios=None):
    text = " ".join(question.split())
    formations, roles = list(formations or []), list(roles or [])
    actors = _explicit_actor_refs(text)
    slots = [slot for formation in formations for slot in _formation_slots(formation)]
    initial_presence = [presence(ref(actor["id"], "actor_ref")) for actor in actors]
    effective = _effective_players(text)
    return {
        "schema": SCHEMA, "contract_version": CONTRACT_VERSION,
        "scenario_id": "scenario:" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
        "question": value(text, "explicit"),
        "formations": [value(item, "explicit") for item in formations],
        "effective_players": effective, "substitution_mode": value(),
        "actors": actors, "role_refs": _explicit_role_refs(roles),
        "position_slots": slots, "candidate_actors": [],
        "events": _events(text, actors),
        "phase_states": [state("state:initial", actor_presence=initial_presence, effective_players=effective)],
        "structural_mappings": [], "constraints": [],
        "trace": {"job_id": value(), "response_sha256": value(), "model_version": value(),
                  "contract_version": value(CONTRACT_VERSION, "derived", "contract_version:v1"),
                  "classified_errors": [], "evaluation": value(),
                  "candidate_correction": value(), "validated_correction": value()},
        "scenarios": list(scenarios or []),
    }


def normalize_contract(plan):
    normalized, changes = deepcopy(plan), []
    for item in normalized.get("phase_states", []):
        phase = item.get("phase")
        if phase in SAFE_ENUM_ALIASES:
            item["phase"] = SAFE_ENUM_ALIASES[phase]
            changes.append({"path": f"phase_states.{item.get('state_id', '?')}.phase",
                            "from": phase, "to": item["phase"], "rule_id": "safe_phase_alias:v1"})
    for event in normalized.get("events", []):
        event_type = event.get("type")
        if event_type in SAFE_ENUM_ALIASES:
            event["type"] = SAFE_ENUM_ALIASES[event_type]
            changes.append({"path": f"events.{event.get('event_id', '?')}.type",
                            "from": event_type, "to": event["type"], "rule_id": "safe_event_alias:v1"})
    return normalized, changes


def issue(code, severity, path, message):
    return {"code": code, "severity": severity, "path": path, "message": message}


def _walk_provenance(node, path, issues):
    if isinstance(node, dict):
        provenance = node.get("provenance")
        if provenance is not None:
            if provenance not in PROVENANCE:
                issues.append(issue("invalid_provenance", "BLOCKING", path, "Provenienza non valida."))
            elif provenance == "derived" and not node.get("rule_id"):
                issues.append(issue("derived_without_rule", "BLOCKING", path, "Dato derivato privo di rule_id."))
            elif provenance == "unknown" and "value" in node and node.get("value") is not None:
                issues.append(issue("unknown_has_value", "BLOCKING", path, "Un dato unknown non può avere un valore."))
        for key, child in node.items():
            _walk_provenance(child, f"{path}.{key}" if path else key, issues)
    elif isinstance(node, list):
        for index, child in enumerate(node):
            _walk_provenance(child, f"{path}.{index}", issues)


def _resolve(reference, entities, allowed, path, issues):
    if not isinstance(reference, dict) or set(reference) != {"id", "kind"}:
        issues.append(issue("invalid_typed_ref", "BLOCKING", path, "Riferimento tipizzato incompleto.")); return None
    item = entities.get(reference.get("id"))
    if not item:
        issues.append(issue("unknown_reference", "BLOCKING", path, "Entità inesistente.")); return None
    if reference.get("kind") != item.get("kind"):
        issues.append(issue("reference_kind_mismatch", "BLOCKING", path, "Kind incompatibile con l'entità.")); return None
    if reference.get("kind") not in allowed:
        issues.append(issue("reference_kind_not_allowed", "BLOCKING", path, "Tipo non ammesso nel riferimento.")); return None
    return item


def _presence_maps(states, entities, issues):
    result = {}
    for s_index, state_item in enumerate(states):
        current = {}
        for p_index, entry in enumerate(state_item.get("actor_presence", [])):
            path = f"phase_states.{s_index}.actor_presence.{p_index}"
            actor = _resolve(entry.get("actor_ref"), entities, {"actor_ref", "candidate_actor"}, path, issues)
            status = entry.get("status", {})
            actual = status.get("value") or "unknown"
            if actual not in PRESENCE:
                issues.append(issue("invalid_presence", "BLOCKING", path, "Presenza non valida."))
            actor_id = (actor or {}).get("id")
            if actor_id in current:
                issues.append(issue("duplicate_presence", "BLOCKING", path, "Presenza duplicata nello stato."))
            if actor_id:
                current[actor_id] = actual
        result[state_item.get("state_id")] = current
    return result


def _timeline(states, events, issues):
    state_ids = [item.get("state_id") for item in states]
    if None in state_ids or len(state_ids) != len(set(state_ids)):
        issues.append(issue("invalid_state_id", "BLOCKING", "phase_states", "State ID mancanti o duplicati."))
    known, sequence = set(state_ids), {}
    for index, item in enumerate(states):
        seq = item.get("sequence", {})
        if seq.get("provenance") != "unknown":
            if not isinstance(seq.get("value"), int):
                issues.append(issue("invalid_sequence", "BLOCKING", f"phase_states.{index}.sequence", "Sequence non intera."))
            else:
                sequence[item.get("state_id")] = seq["value"]
    edges = []
    for index, event in enumerate(events):
        source, target = event.get("from_state_id"), event.get("to_state_id")
        if source is None and target is None:
            continue
        if source not in known or target not in known or source == target:
            issues.append(issue("invalid_event_edge", "BLOCKING", f"events.{index}", "Arco temporale non valido.")); continue
        if source in sequence and target in sequence and sequence[target] <= sequence[source]:
            issues.append(issue("non_increasing_timeline", "BLOCKING", f"events.{index}", "Sequenza temporale contraddetta."))
        edges.append((source, target, index))
    graph = {item: [] for item in known}
    for source, target, _ in edges:
        graph[source].append(target)
    visiting, visited = set(), set()
    def visit(node):
        if node in visiting:
            return False
        if node in visited:
            return True
        visiting.add(node)
        if not all(visit(child) for child in graph.get(node, [])):
            return False
        visiting.remove(node); visited.add(node); return True
    if not all(visit(node) for node in graph):
        issues.append(issue("timeline_cycle", "BLOCKING", "events", "Timeline ciclica."))
    return edges, graph


def _reachable(graph, source, target):
    """Return True only for a demonstrated directed path in the partial order."""
    if source is None or target is None:
        return False
    pending, visited = [source], set()
    while pending:
        node = pending.pop()
        if node == target:
            return True
        if node in visited:
            continue
        visited.add(node)
        pending.extend(graph.get(node, []))
    return False


def _unknown_severity(event):
    return "BLOCKING" if event.get("assertion_mode") == "executable" else "QUALIFICATION_REQUIRED"


def _check_status(actual, expected, event, path, issues, code):
    if actual in {None, "unknown"}:
        issues.append(issue(code + "_unknown", _unknown_severity(event), path, "Precondizione di presenza non verificata."))
    elif actual not in expected:
        issues.append(issue(code, "BLOCKING", path, "Presenza incompatibile con l'evento."))


def validate_contract(plan):
    issues = []
    if plan.get("schema") != SCHEMA:
        issues.append(issue("invalid_schema", "BLOCKING", "schema", "Schema non riconosciuto."))
    _walk_provenance(plan, "", issues)
    entity_items = [item for key in ("actors", "role_refs", "position_slots", "candidate_actors") for item in plan.get(key, [])]
    ids = [item.get("id") for item in entity_items]
    if None in ids or len(ids) != len(set(ids)):
        issues.append(issue("duplicate_entity_id", "BLOCKING", "entities", "ID mancanti o duplicati."))
    entities = {item.get("id"): item for item in entity_items if item.get("id")}
    for item in entity_items:
        if item.get("kind") not in ENTITY_KINDS:
            issues.append(issue("invalid_entity_kind", "BLOCKING", item.get("id", "entities"), "Tipo entità non valido."))
        if item.get("kind") == "candidate_actor" and item.get("availability") not in {"explicitly_available", "confirmed"}:
            issues.append(issue("candidate_availability_unknown", "QUALIFICATION_REQUIRED", item.get("id", "candidate"), "Disponibilità non confermata."))
    mode = plan.get("substitution_mode", {}).get("value") or "unknown"
    if mode not in SUBSTITUTION_MODES:
        issues.append(issue("invalid_substitution_mode", "BLOCKING", "substitution_mode", "Modalità sostituzioni non valida."))
    states, events = plan.get("phase_states", []), plan.get("events", [])
    edges, timeline_graph = _timeline(states, events, issues)
    presence_by_state = _presence_maps(states, entities, issues)
    state_by_id = {item.get("state_id"): item for item in states}
    for index, event in enumerate(events):
        path, kind = f"events.{index}", event.get("type")
        if kind not in EVENT_TYPES:
            issues.append(issue("invalid_event_type", "BLOCKING", path, "Tipo evento non valido.")); continue
        if event.get("assertion_mode") not in ASSERTION_MODES:
            issues.append(issue("invalid_assertion_mode", "BLOCKING", path, "Assertion mode non valido."))
        if event.get("cardinality_delta") != {"substitution": 0, "rotation": 0, "expulsion": -1}[kind]:
            issues.append(issue("invalid_cardinality_delta", "BLOCKING", path, "Delta incompatibile."))
        source, target = event.get("from_state_id"), event.get("to_state_id")
        before, after = presence_by_state.get(source, {}), presence_by_state.get(target, {})
        if not source or not target:
            issues.append(issue("event_temporality_unknown", _unknown_severity(event), path, "Evento senza due stati ordinabili."))
        if kind == "substitution":
            outgoing = _resolve(event.get("out_ref"), entities, {"actor_ref", "candidate_actor"}, path + ".out_ref", issues)
            incoming = _resolve(event.get("in_ref"), entities, {"actor_ref", "candidate_actor"}, path + ".in_ref", issues)
            out_id, in_id = (outgoing or {}).get("id"), (incoming or {}).get("id")
            if out_id and out_id == in_id:
                issues.append(issue("invalid_substitution", "BLOCKING", path, "Entrante e uscente coincidono."))
            if source and target and out_id and in_id:
                _check_status(before.get(out_id), {"on_field"}, event, path, issues, "outgoing_not_on_field")
                _check_status(before.get(in_id), {"off_field"}, event, path, issues, "incoming_not_off_field")
                _check_status(after.get(out_id), {"off_field"}, event, path, issues, "outgoing_effect_missing")
                _check_status(after.get(in_id), {"on_field"}, event, path, issues, "incoming_effect_missing")
        elif kind == "rotation":
            actor = _resolve(event.get("subject_ref"), entities, {"actor_ref", "candidate_actor"}, path + ".subject_ref", issues)
            actor_id = (actor or {}).get("id")
            if source and target and actor_id:
                _check_status(before.get(actor_id), {"on_field"}, event, path, issues, "rotation_actor_not_present")
                _check_status(after.get(actor_id), {"on_field"}, event, path, issues, "rotation_actor_missing_after")
        else:
            actor = _resolve(event.get("subject_ref"), entities, {"actor_ref", "candidate_actor"}, path + ".subject_ref", issues) if event.get("subject_ref") else None
            team = event.get("team", {}).get("value")
            if team not in {"own", "opponent", None}:
                issues.append(issue("invalid_team", "BLOCKING", path, "Squadra non valida."))
            if team is None:
                issues.append(issue("expulsion_team_unknown", _unknown_severity(event), path, "Squadra espulsione ignota."))
            actor_id = (actor or {}).get("id")
            actor_team = ((actor or {}).get("team") or {}).get("value")
            if actor and team and actor_team and actor_team != team:
                issues.append(issue("expulsion_actor_team_mismatch", "BLOCKING", path,
                                    "La squadra dell'attore contraddice quella dell'evento."))
            elif actor and team and actor_team is None:
                issues.append(issue("expulsion_actor_team_unknown", _unknown_severity(event), path,
                                    "La squadra dell'attore espulso non è verificata."))
            if team == "own" and source and target and actor_id:
                _check_status(before.get(actor_id), {"on_field"}, event, path, issues, "expelled_actor_not_present")
                _check_status(after.get(actor_id), {"unavailable"}, event, path, issues, "expulsion_effect_missing")
    substitutions = [(index, event) for index, event in enumerate(events) if event.get("type") == "substitution"]
    for earlier_index, earlier in substitutions:
        exited_actor = (earlier.get("out_ref") or {}).get("id")
        for later_index, later in substitutions:
            if earlier_index == later_index or exited_actor != (later.get("in_ref") or {}).get("id"):
                continue
            if _reachable(timeline_graph, earlier.get("to_state_id"), later.get("from_state_id")):
                severity = "BLOCKING" if mode == "standard_no_reentry" else "QUALIFICATION_REQUIRED" if mode == "unknown" else None
                if severity:
                    issues.append(issue("actor_reentry", severity, f"events.{later_index}",
                                        "Rientro incompatibile o non verificabile."))
            elif (mode != "rolling_reentry_allowed"
                  and not _reachable(timeline_graph, later.get("to_state_id"), earlier.get("from_state_id"))):
                issues.append(issue("actor_reentry_order_unknown", "QUALIFICATION_REQUIRED",
                                    f"events.{later_index}",
                                    "Il possibile rientro non è verificabile nella timeline parziale."))
    for s_index, state_item in enumerate(states):
        if state_item.get("phase", "unknown") not in PHASES:
            issues.append(issue("invalid_phase", "BLOCKING", f"phase_states.{s_index}.phase", "Fase non valida."))
        subjects, positions = set(), set()
        for a_index, assignment in enumerate(state_item.get("assignments", [])):
            path = f"phase_states.{s_index}.assignments.{a_index}"
            subject = _resolve(assignment.get("subject_ref"), entities, {"actor_ref", "candidate_actor"}, path, issues)
            position = _resolve(assignment.get("position_ref"), entities, {"position_slot"}, path, issues)
            if assignment.get("role_ref") is not None:
                _resolve(assignment.get("role_ref"), entities, {"role_ref"}, path, issues)
            subject_id, position_id = (subject or {}).get("id"), (position or {}).get("id")
            if subject_id in subjects:
                issues.append(issue("duplicate_actor_assignment", "BLOCKING", path, "Attore duplicato nello stato."))
            if position_id in positions:
                issues.append(issue("duplicate_position_assignment", "BLOCKING", path, "Slot duplicato nello stato."))
            subjects.add(subject_id); positions.add(position_id)
            status = presence_by_state.get(state_item.get("state_id"), {}).get(subject_id)
            if subject_id and status in {"off_field", "unavailable"}:
                issues.append(issue("assignment_actor_not_on_field", "BLOCKING", path, "Attore assegnato ma non in campo."))
            elif subject_id and status in {None, "unknown"}:
                issues.append(issue("assignment_presence_unknown", "QUALIFICATION_REQUIRED", path, "Presenza non verificata."))
        if state_item.get("presence_complete", {}).get("value") is True:
            effective = state_item.get("effective_players", {}).get("value")
            present_count = sum(status == "on_field" for status in presence_by_state.get(state_item.get("state_id"), {}).values())
            if effective is not None and present_count != effective:
                issues.append(issue("complete_presence_cardinality_mismatch", "BLOCKING",
                                    f"phase_states.{s_index}",
                                    "L'elenco completo dei presenti non coincide con la cardinalità dichiarata."))
    mapping_from, mapping_to = set(), set()
    for index, mapping in enumerate(plan.get("structural_mappings", [])):
        path = f"structural_mappings.{index}"
        source = _resolve(mapping.get("from_slot_ref"), entities, {"position_slot"}, path, issues)
        target = _resolve(mapping.get("to_slot_ref"), entities, {"position_slot"}, path, issues)
        source_id, target_id = (source or {}).get("id"), (target or {}).get("id")
        if source_id in mapping_from or target_id in mapping_to:
            issues.append(issue("non_unique_structural_mapping", "BLOCKING", path, "Mapping non uno-a-uno."))
        mapping_from.add(source_id); mapping_to.add(target_id)
    final_formation = plan.get("final_formation", {})
    target_name = final_formation.get("value") if isinstance(final_formation, dict) else None
    if target_name in FORMATION_SLOTS and plan.get("structural_mappings"):
        expected_targets = {f"slot:own:{target_name}:{slot}" for slot in FORMATION_SLOTS[target_name]}
        if mapping_to != expected_targets:
            issues.append(issue("incomplete_final_geometry", "QUALIFICATION_REQUIRED", "structural_mappings",
                                "La geometria astratta finale non è ricostruita integralmente."))
    edge_events = {}
    for source, target, index in edges:
        edge_events.setdefault((source, target), []).append(events[index])
    for (source, target), linked in edge_events.items():
        before_state, after_state = state_by_id[source], state_by_id[target]
        before_assignments = {(item.get("subject_ref") or {}).get("id"): (item.get("position_ref") or {}).get("id")
                              for item in before_state.get("assignments", [])}
        after_assignments = {(item.get("subject_ref") or {}).get("id"): (item.get("position_ref") or {}).get("id")
                             for item in after_state.get("assignments", [])}
        mapping = {(item.get("from_slot_ref") or {}).get("id"): (item.get("to_slot_ref") or {}).get("id")
                   for item in plan.get("structural_mappings", [])}
        if mapping and before_assignments and after_assignments:
            for actor_id in set(before_assignments) & set(after_assignments):
                source_slot, target_slot = before_assignments.get(actor_id), after_assignments.get(actor_id)
                if source_slot is None or target_slot is None or source_slot not in mapping:
                    issues.append(issue("assignment_continuity_incomplete", "QUALIFICATION_REQUIRED",
                                        f"{source}->{target}", "Assegnazioni concrete insufficienti per ricostruire la trasformazione."))
                elif mapping.get(source_slot) != target_slot:
                    issues.append(issue("assignment_mapping_mismatch", "BLOCKING", f"{source}->{target}",
                                        "La posizione finale dell'attore contraddice il mapping strutturale dichiarato."))
        if (before_state.get("presence_complete", {}).get("value") is True
                and after_state.get("presence_complete", {}).get("value") is True):
            expected = {actor for actor, status in presence_by_state[source].items() if status == "on_field"}
            for event in linked:
                if event.get("type") == "substitution":
                    expected.discard((event.get("out_ref") or {}).get("id")); expected.add((event.get("in_ref") or {}).get("id"))
                elif event.get("type") == "expulsion" and event.get("team", {}).get("value") == "own":
                    expected.discard((event.get("subject_ref") or {}).get("id"))
            actual = {actor for actor, status in presence_by_state[target].items() if status == "on_field"}
            if expected != actual:
                issues.append(issue("actor_continuity_mismatch", "BLOCKING", f"{source}->{target}", "Continuità attori incoerente."))
    transition_deltas = {}
    for source, target, index in edges:
        event = events[index]
        delta = -1 if event.get("type") == "expulsion" and event.get("team", {}).get("value") == "own" else 0
        transition_deltas[(source, target)] = transition_deltas.get((source, target), 0) + delta
    for (source, target), delta in transition_deltas.items():
        before_count = state_by_id[source].get("effective_players", {}).get("value")
        after_count = state_by_id[target].get("effective_players", {}).get("value")
        if before_count is not None and after_count is not None and after_count != before_count + delta:
            issues.append(issue("cardinality_mismatch", "BLOCKING", f"{source}->{target}",
                                "Cardinalità incoerente con il delta aggregato della transizione."))
    blocking = [item for item in issues if item["severity"] == "BLOCKING"]
    return {"schema": "tactical_state_validation_v1", "valid": not blocking, "issues": issues,
            "counts": {level: sum(item["severity"] == level for item in issues) for level in SEVERITIES}}


def render_validated_structure(plan, validation=None):
    validation = validation or validate_contract(plan)
    blocking = [item for item in validation["issues"] if item["severity"] == "BLOCKING"]
    qualified = [item for item in validation["issues"] if item["severity"] == "QUALIFICATION_REQUIRED"]
    lines = []
    if blocking:
        lines.append("ELEMENTI BLOCCATI: " + " ".join(item["message"] for item in blocking))
    formations = [item["value"] for item in plan.get("formations", []) if item.get("value")]
    if formations:
        lines.append("FATTI VALIDATI — Sistemi dichiarati: " + ", ".join(formations) + ".")
    actors = [item["label"] for item in plan.get("actors", [])]
    if actors:
        lines.append("FATTI VALIDATI — Attori citati (presenza non implicita): " + ", ".join(actors) + ".")
    if plan.get("position_slots"):
        lines.append("FATTI VALIDATI — Gli slot sono posizioni astratte, non identità o disponibilità.")
    blocked_events = {int(item["path"].split(".")[1]) for item in blocking if re.match(r"events\.\d+", item["path"])}
    if any(item["path"] == "events" for item in blocking):
        blocked_events.update(range(len(plan.get("events", []))))
    for item in blocking:
        if "->" not in item["path"]:
            continue
        source, target = item["path"].split("->", 1)
        blocked_events.update(index for index, event in enumerate(plan.get("events", []))
                              if event.get("from_state_id") == source and event.get("to_state_id") == target)
    for index, event in enumerate(plan.get("events", [])):
        if index in blocked_events:
            continue
        prefix = "INFORMAZIONE QUALIFICATA" if any(item["path"].startswith(f"events.{index}") for item in qualified) else "FATTO VALIDATO"
        if event.get("type") == "substitution":
            lines.append(f"{prefix} — Sostituzione: {(event.get('out_ref') or {}).get('id')} → {(event.get('in_ref') or {}).get('id')}.")
        elif event.get("type") == "expulsion":
            lines.append(f"{prefix} — Espulsione: {event.get('actor_label') or (event.get('subject_ref') or {}).get('id') or 'attore non identificato'}.")
        elif event.get("type") == "rotation":
            lines.append(f"{prefix} — Rotazione: {(event.get('subject_ref') or {}).get('id')}.")
    if qualified:
        lines.append("LIMITI DA QUALIFICARE: " + " ".join(item["message"] for item in qualified))
    return "\n".join(lines) if lines else "Nessuna informazione strutturale esplicita disponibile."
