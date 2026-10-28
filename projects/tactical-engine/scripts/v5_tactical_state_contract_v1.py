#!/usr/bin/env python3
"""Pure deterministic Tactical State Contract v1.

This module never calls a model or a service.  It represents what a question
actually states separately from abstract formation slots and later tactical
hypotheses.  Validation is deliberately structural: it does not prescribe a
universal tactical solution.
"""
from __future__ import annotations

import hashlib
import re
from copy import deepcopy


SCHEMA = "tactical_state_contract_v1"
CONTRACT_VERSION = "1.0.0"
PROVENANCE = {"explicit", "derived", "assumed", "unknown"}
SEVERITIES = {"BLOCKING", "RECOVERABLE", "QUALIFICATION_REQUIRED", "ADVISORY"}
PHASES = {"possession", "non_possession", "positive_transition", "negative_transition", "set_piece", "unknown"}
EVENT_TYPES = {"substitution", "expulsion", "rotation"}
ENTITY_KINDS = {"actor_ref", "role_ref", "position_slot", "candidate_actor"}

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


def value(value=None, provenance="unknown", rule_id=None):
    """Create a provenance-bearing value; unknown values are always null."""
    if provenance not in PROVENANCE:
        raise ValueError(f"invalid provenance: {provenance}")
    if provenance == "unknown":
        value = None
    result = {"value": value, "provenance": provenance}
    if rule_id is not None:
        result["rule_id"] = rule_id
    return result


def entity(identifier, kind, label, provenance, rule_id=None, availability="unknown"):
    if kind not in ENTITY_KINDS:
        raise ValueError(f"invalid entity kind: {kind}")
    result = {
        "id": identifier,
        "kind": kind,
        "label": label,
        "provenance": provenance,
        "availability": availability,
    }
    if rule_id:
        result["rule_id"] = rule_id
    return result


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.casefold()).strip("_") or "unknown"


def _formation_slots(formation, side="own"):
    return [entity(
        f"slot:{side}:{formation}:{slot}", "position_slot", slot, "derived",
        rule_id=f"formation_slots:{formation}:v1", availability="not_applicable",
    ) for slot in FORMATION_SLOTS.get(formation, ())]


def _explicit_actor_refs(question):
    refs = []
    # A shirt number is an explicit reference, not proof of name or availability.
    for number in sorted(set(re.findall(r"\b(?:numero|n\.)\s*(\d{1,2})\b", question, re.I))):
        refs.append(entity(f"actor:explicit:number:{number}", "actor_ref", f"numero {number}",
                           "explicit", availability="stated_in_scenario"))
    return refs


def _explicit_role_refs(roles):
    return [entity(f"role:explicit:{_slug(role)}", "role_ref", role, "explicit",
                   availability="not_applicable") for role in roles]


def _effective_players(question):
    match = re.search(r"\b(?:siamo|siete|squadra)\s+in\s+(10|9|8)\b|\bin\s+(10|9|8)\s+(?:uomini|giocatori)\b", question, re.I)
    if match:
        count = int(next(group for group in match.groups() if group))
        return value(count, "explicit")
    return value()


def _events(question, actors, roles):
    events = []
    actor_by_number = {item["label"].split()[-1]: item["id"] for item in actors}
    # Conservative: only parse explicit number-to-number substitutions.
    for index, match in enumerate(re.finditer(
            r"(?:esce|togli(?:e|ere)?)\s+(?:il\s+)?(?:numero\s+)?(\d{1,2}).{0,35}?(?:entra|inserisc(?:e|o|i))\s+(?:il\s+)?(?:numero\s+)?(\d{1,2})",
            question, re.I), 1):
        out_no, in_no = match.groups()
        out_id = actor_by_number.get(out_no, f"actor:explicit:number:{out_no}")
        in_id = actor_by_number.get(in_no, f"actor:explicit:number:{in_no}")
        events.append({"id": f"event:substitution:{index}", "type": "substitution",
                       "phase": "unknown", "out_actor": out_id, "in_actor": in_id,
                       "cardinality_delta": 0, "provenance": "explicit"})
    expulsion = re.search(r"(?:espuls[oa]|cartellino rosso)(?:\s+(?:al|per il|del))?\s*(numero\s+\d{1,2}|[a-zà-ù ]{3,30})?", question, re.I)
    if expulsion:
        label = (expulsion.group(1) or "attore non identificato").strip()
        number = re.search(r"\d{1,2}", label)
        actor_id = actor_by_number.get(number.group() if number else "") if number else None
        events.append({"id": "event:expulsion:1", "type": "expulsion", "phase": "unknown",
                       "actor": actor_id, "actor_label": label, "cardinality_delta": -1,
                       "affects_current_count": None, "provenance": "explicit"})
    # Do not guess a rotation from generic tactical verbs. Record it only when
    # both an explicit actor reference and a movement verb are present.
    for number, verb in re.findall(r"(?:numero|n\.)\s*(\d{1,2}).{0,25}?\b(si\s+abbassa|si\s+alza|stringe|si\s+allarga)\b", question, re.I):
        events.append({"id": f"event:rotation:{len(events)+1}", "type": "rotation",
                       "phase": "unknown", "actor": actor_by_number[number],
                       "movement": verb.casefold(), "cardinality_delta": 0,
                       "provenance": "explicit"})
    return events


def build_question_plan(question, formations=None, roles=None, scenarios=None):
    """Build the deterministic plan used by ``analyse``.

    Formation slots express topology only.  Their ``occupant`` is intentionally
    absent: a formation name cannot prove player identity or availability.
    """
    text = " ".join(question.split())
    formations = list(formations or [])
    roles = list(roles or [])
    actors = _explicit_actor_refs(text)
    role_refs = _explicit_role_refs(roles)
    slots = []
    for formation in formations:
        slots.extend(_formation_slots(formation))
    events = _events(text, actors, roles)
    return {
        "schema": SCHEMA,
        "contract_version": CONTRACT_VERSION,
        "scenario_id": "scenario:" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
        "question": value(text, "explicit"),
        "formations": [value(item, "explicit") for item in formations],
        "effective_players": _effective_players(text),
        "actors": actors,
        "role_refs": role_refs,
        "position_slots": slots,
        "candidate_actors": [],
        "events": events,
        "phase_states": [],
        "constraints": [],
        "trace": {
            "job_id": value(), "response_sha256": value(), "model_version": value(),
            "contract_version": value(CONTRACT_VERSION, "derived", "contract_version:v1"),
            "classified_errors": [], "evaluation": value(),
            "candidate_correction": value(), "validated_correction": value(),
        },
        "scenarios": list(scenarios or []),
    }


def normalize_contract(plan):
    """Apply only safe lexical normalizations and report every change."""
    normalized = deepcopy(plan)
    changes = []
    for state in normalized.get("phase_states", []):
        phase = state.get("phase")
        if phase in SAFE_ENUM_ALIASES:
            state["phase"] = SAFE_ENUM_ALIASES[phase]
            changes.append({"path": f"phase_states.{state.get('id', '?')}.phase",
                            "from": phase, "to": state["phase"], "rule_id": "safe_phase_alias:v1"})
    for event in normalized.get("events", []):
        event_type = event.get("type")
        if event_type in SAFE_ENUM_ALIASES:
            event["type"] = SAFE_ENUM_ALIASES[event_type]
            changes.append({"path": f"events.{event.get('id', '?')}.type",
                            "from": event_type, "to": event["type"], "rule_id": "safe_event_alias:v1"})
    return normalized, changes


def issue(code, severity, path, message):
    if severity not in SEVERITIES:
        raise ValueError(severity)
    return {"code": code, "severity": severity, "path": path, "message": message}


def validate_contract(plan):
    """Validate identities, event sequence, cardinality and phase relations."""
    issues = []
    if plan.get("schema") != SCHEMA:
        issues.append(issue("invalid_schema", "BLOCKING", "schema", "Schema non riconosciuto."))
    entities = []
    for key in ("actors", "role_refs", "position_slots", "candidate_actors"):
        entities.extend(plan.get(key, []))
    ids = [item.get("id") for item in entities]
    if len(ids) != len(set(ids)):
        issues.append(issue("duplicate_entity_id", "BLOCKING", "entities", "Identificativi duplicati."))
    actor_ids = {item["id"] for item in plan.get("actors", []) if item.get("id")}
    candidate_ids = {item["id"] for item in plan.get("candidate_actors", []) if item.get("id")}
    for item in entities:
        if item.get("kind") not in ENTITY_KINDS:
            issues.append(issue("invalid_entity_kind", "BLOCKING", item.get("id", "entities"), "Tipo entità non valido."))
        if item.get("provenance") not in PROVENANCE:
            issues.append(issue("invalid_provenance", "BLOCKING", item.get("id", "entities"), "Provenienza non valida."))
        if item.get("kind") == "candidate_actor" and item.get("availability") not in {"explicitly_available", "confirmed"}:
            issues.append(issue("candidate_availability_unknown", "QUALIFICATION_REQUIRED", item.get("id", "candidate"),
                                "La disponibilità del candidato non è confermata."))
    for key in ("question", "effective_players", "formations"):
        values = plan.get(key, []) if key == "formations" else [plan.get(key, {})]
        for index, item in enumerate(values):
            if item.get("provenance") not in PROVENANCE:
                issues.append(issue("invalid_provenance", "BLOCKING", f"{key}.{index}", "Provenienza non valida."))
            if item.get("provenance") == "derived" and not item.get("rule_id"):
                issues.append(issue("derived_without_rule", "BLOCKING", f"{key}.{index}", "Dato derivato privo di rule_id."))
    active = set(actor_ids)
    exited = set()
    count_info = plan.get("effective_players", {})
    count = count_info.get("value") if count_info.get("provenance") != "unknown" else None
    for index, event in enumerate(plan.get("events", [])):
        path = f"events.{index}"
        kind = event.get("type")
        if kind not in EVENT_TYPES:
            issues.append(issue("invalid_event_type", "BLOCKING", path, "Tipo evento non valido.")); continue
        if event.get("provenance") not in PROVENANCE:
            issues.append(issue("invalid_provenance", "BLOCKING", path, "Provenienza evento non valida."))
        expected_delta = {"substitution": 0, "rotation": 0, "expulsion": -1}[kind]
        if event.get("cardinality_delta") != expected_delta:
            issues.append(issue("invalid_cardinality_delta", "BLOCKING", path, "Variazione numerica incompatibile con l'evento."))
        if kind == "substitution":
            outgoing, incoming = event.get("out_actor"), event.get("in_actor")
            if not outgoing or not incoming or outgoing == incoming:
                issues.append(issue("invalid_substitution", "BLOCKING", path, "Entrante e uscente devono essere distinti e identificati."))
                continue
            if outgoing in exited:
                issues.append(issue("actor_reused_after_exit", "BLOCKING", path, "Il giocatore era già uscito."))
            if incoming in exited:
                issues.append(issue("exited_actor_reentered", "BLOCKING", path, "Un giocatore uscito viene riutilizzato."))
            if incoming not in actor_ids | candidate_ids:
                issues.append(issue("incoming_actor_unresolved", "QUALIFICATION_REQUIRED", path, "Disponibilità dell'entrante non dimostrata."))
            exited.add(outgoing); active.discard(outgoing); active.add(incoming)
        elif kind == "rotation":
            actor = event.get("actor")
            if not actor or actor in exited:
                issues.append(issue("invalid_rotation_actor", "BLOCKING", path, "Rotazione assegnata a un attore assente o uscito."))
        else:
            actor = event.get("actor")
            if actor and actor in exited:
                issues.append(issue("actor_reused_after_exit", "BLOCKING", path, "Attore già rimosso dallo stato."))
            if actor:
                exited.add(actor); active.discard(actor)
            if count is not None and event.get("affects_current_count") is True:
                count -= 1
    assignments = {}
    for s_index, state in enumerate(plan.get("phase_states", [])):
        phase = state.get("phase", "unknown")
        if phase not in PHASES:
            issues.append(issue("invalid_phase", "BLOCKING", f"phase_states.{s_index}.phase", "Fase non valida."))
        for a_index, assignment in enumerate(state.get("assignments", [])):
            subject, slot = assignment.get("actor") or assignment.get("subject"), assignment.get("slot")
            key = (phase, subject)
            if subject and subject not in set(ids):
                issues.append(issue("unknown_assignment_actor", "BLOCKING",
                                    f"phase_states.{s_index}.assignments.{a_index}",
                                    "L'assegnazione riferisce un'entità non dichiarata."))
            if subject in exited:
                issues.append(issue("assignment_after_exit", "BLOCKING", f"phase_states.{s_index}.assignments.{a_index}",
                                    "Un attore uscito riceve un compito successivo."))
            if subject and slot and key in assignments and assignments[key] != slot:
                issues.append(issue("simultaneous_incompatible_assignment", "BLOCKING",
                                    f"phase_states.{s_index}.assignments.{a_index}",
                                    "Lo stesso attore occupa due slot simultanei nella stessa fase."))
            if subject and slot:
                assignments[key] = slot
    final_formation = plan.get("final_formation")
    if final_formation and final_formation.get("value") in FORMATION_SLOTS:
        target = final_formation["value"]
        final_assignments = [a for s in plan.get("phase_states", []) if s.get("formation") == target
                             for a in s.get("assignments", [])]
        occupied = [a.get("slot") for a in final_assignments if a.get("slot")]
        if len(occupied) != len(set(occupied)):
            issues.append(issue("duplicate_final_slot", "BLOCKING", "phase_states", "Due attori occupano lo stesso slot finale."))
        invalid = set(occupied) - set(FORMATION_SLOTS[target])
        if invalid:
            issues.append(issue("slot_outside_final_formation", "BLOCKING", "phase_states", "Slot incompatibile con il sistema finale."))
        if final_assignments and len(final_assignments) != len(FORMATION_SLOTS[target]):
            issues.append(issue("incomplete_final_geometry", "QUALIFICATION_REQUIRED", "phase_states",
                                "La geometria finale dichiarata non è ricostruita integralmente."))
    blocking = [item for item in issues if item["severity"] == "BLOCKING"]
    return {"schema": "tactical_state_validation_v1", "valid": not blocking,
            "effective_players_after_events": count, "issues": issues,
            "counts": {severity: sum(i["severity"] == severity for i in issues) for severity in SEVERITIES}}


def render_validated_structure(plan, validation=None):
    """Render only facts already contained in the plan, qualifying uncertainty."""
    validation = validation or validate_contract(plan)
    lines = []
    formations = [item["value"] for item in plan.get("formations", []) if item.get("value")]
    if formations:
        lines.append("Sistema dichiarato: " + ", ".join(formations) + ".")
    actors = [item["label"] for item in plan.get("actors", [])]
    if actors:
        lines.append("Attori esplicitamente citati: " + ", ".join(actors) + ".")
    if plan.get("position_slots"):
        lines.append("Gli slot di formazione sono posizioni astratte e non dimostrano identità o disponibilità dei giocatori.")
    for event in plan.get("events", []):
        if event.get("type") == "substitution":
            lines.append(f"Sostituzione dichiarata: {event.get('out_actor')} → {event.get('in_actor')}.")
        elif event.get("type") == "expulsion":
            lines.append(f"Espulsione dichiarata: {event.get('actor_label') or event.get('actor') or 'attore non identificato'}.")
        elif event.get("type") == "rotation":
            lines.append(f"Rotazione dichiarata: {event.get('actor')} ({event.get('movement', 'movimento non specificato')}).")
    qualifications = [item["message"] for item in validation["issues"] if item["severity"] == "QUALIFICATION_REQUIRED"]
    blocking = [item["message"] for item in validation["issues"] if item["severity"] == "BLOCKING"]
    if blocking:
        lines.append("Struttura non validabile integralmente: " + " ".join(blocking))
    if qualifications:
        lines.append("Informazioni da qualificare: " + " ".join(qualifications))
    if not lines:
        lines.append("Nessuna informazione strutturale esplicita disponibile.")
    return "\n".join(lines)
