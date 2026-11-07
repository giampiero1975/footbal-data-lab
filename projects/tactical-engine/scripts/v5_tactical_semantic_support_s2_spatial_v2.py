#!/usr/bin/env python3
"""Pure offline validator for the opt-in Spatial V2 relation witness.

The module performs no I/O and never calls a model.  It validates structure,
anchors, the versioned vocabulary and internal label consistency.  It does not
resolve coreference or claim semantic correctness.
"""
from __future__ import annotations

import unicodedata


CONTRACT_ID = "nli_spatial_relations_v2"
CONTRACT_VERSION = "2.0.0"
VALIDATOR_ID = "nli_spatial_relations_v2_validator"
VALIDATOR_VERSION = "1.0.0"
LABELS = {"supported", "contradicted", "insufficient"}
STATUSES = {"explicit", "implicit", "absent", "ambiguous", "unknown"}
COMPARISONS = {"same", "compatible", "different", "incompatible", "unknown", "ambiguous"}
PHASES = {"attack", "offensive_transition", "defense", "defensive_transition",
          "set_piece", "general", "absent", "ambiguous", "unknown"}
QUANTIFIERS = {"none", "existential", "some", "many", "most", "all",
               "always", "never", "numeric", "absent", "ambiguous", "unknown"}
POLARITIES = {"affirmed", "negated", "ambiguous", "unknown"}
AXIS_VALUES = {
    "space_availability": {"abundant", "scarce", "neutral"},
    "distance_change": {"increasing", "decreasing", "stable"},
    "movement_direction": {"advancing", "retreating", "stationary"},
    "area_extent": {"expanding", "contracting", "stable"},
    "relative_position": {"ahead_of", "behind", "between", "inside", "outside", "adjacent"},
}
VALUE_SENTINELS = {"absent", "ambiguous", "unknown"}
INCOMPATIBLE_VALUES = {
    "space_availability": {frozenset(("abundant", "scarce"))},
    "distance_change": {frozenset(("increasing", "decreasing")),
                        frozenset(("increasing", "stable")),
                        frozenset(("decreasing", "stable"))},
    "movement_direction": {frozenset(("advancing", "retreating")),
                           frozenset(("advancing", "stationary")),
                           frozenset(("retreating", "stationary"))},
    "area_extent": {frozenset(("expanding", "contracting")),
                    frozenset(("expanding", "stable")),
                    frozenset(("contracting", "stable"))},
    "relative_position": {frozenset(("ahead_of", "behind")),
                          frozenset(("inside", "outside"))},
}
ROOT_KEYS = {"contract_id", "contract_version", "label", "claim_relation",
             "evidence_relation", "comparison"}
RELATION_KEYS = {"subject", "semantic_axis", "reference", "value", "conditions",
                 "phase", "quantifier", "polarity"}
COMPARISON_KEYS = set(RELATION_KEYS)


def _slot_schema(values):
    return {
        "type": "object", "additionalProperties": False,
        "required": ["status", "value", "anchors"],
        "properties": {
            "status": {"enum": sorted(STATUSES)},
            "value": {"enum": sorted(values)},
            "anchors": {"type": "array", "maxItems": 4},
        },
    }


ANCHOR_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["source", "start", "end", "exact_span"],
    "properties": {
        "source": {"enum": ["claim", "evidence"]},
        "start": {"type": "integer", "minimum": 0},
        "end": {"type": "integer", "minimum": 1},
        "exact_span": {"type": "string", "minLength": 1},
    },
}
ENTITY_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["status", "entity_id", "anchors"],
    "properties": {
        "status": {"enum": sorted(STATUSES)},
        "entity_id": {"type": "string", "pattern": r"^entity:[a-z0-9][a-z0-9._-]{0,63}$"},
        "anchors": {"type": "array", "items": ANCHOR_SCHEMA, "maxItems": 4},
    },
}
CONDITIONS_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["status", "items"],
    "properties": {
        "status": {"enum": sorted(STATUSES)},
        "items": {"type": "array", "maxItems": 8, "items": {
            "type": "object", "additionalProperties": False,
            "required": ["condition_id", "status", "anchors"],
            "properties": {
                "condition_id": {"type": "string", "pattern": r"^condition:[a-z0-9][a-z0-9._-]{0,63}$"},
                "status": {"enum": ["explicit", "ambiguous"]},
                "anchors": {"type": "array", "items": ANCHOR_SCHEMA, "minItems": 1, "maxItems": 4},
            },
        }},
    },
}
PHASE_SCHEMA = _slot_schema(PHASES)
QUANTIFIER_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["status", "value", "literal", "anchors"],
    "properties": {
        "status": {"enum": sorted(STATUSES)},
        "value": {"enum": sorted(QUANTIFIERS)},
        "literal": {"type": ["string", "null"], "maxLength": 64},
        "anchors": {"type": "array", "items": ANCHOR_SCHEMA, "maxItems": 2},
    },
}
POLARITY_SCHEMA = _slot_schema(POLARITIES)
RELATION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": sorted(RELATION_KEYS),
    "properties": {
        "subject": ENTITY_SCHEMA,
        "semantic_axis": _slot_schema(set(AXIS_VALUES) | VALUE_SENTINELS),
        "reference": ENTITY_SCHEMA,
        "value": _slot_schema(set().union(*AXIS_VALUES.values()) | VALUE_SENTINELS),
        "conditions": CONDITIONS_SCHEMA,
        "phase": PHASE_SCHEMA,
        "quantifier": QUANTIFIER_SCHEMA,
        "polarity": POLARITY_SCHEMA,
    },
    "allOf": [{
        "if": {"properties": {"semantic_axis": {"properties": {"value": {"const": axis}}}}},
        "then": {"properties": {"value": {"properties": {"value": {"enum": sorted(values)}}}}},
    } for axis, values in AXIS_VALUES.items()],
}


SPATIAL_V2_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "urn:football-data-lab:nli-spatial-relations-v2:2.0.0",
    "type": "object", "additionalProperties": False,
    "required": sorted(ROOT_KEYS),
    "properties": {
        "contract_id": {"const": CONTRACT_ID},
        "contract_version": {"const": CONTRACT_VERSION},
        "label": {"enum": sorted(LABELS)},
        "claim_relation": {"$ref": "#/$defs/relation"},
        "evidence_relation": {"$ref": "#/$defs/relation"},
        "comparison": {"$ref": "#/$defs/comparison"},
    },
    "$defs": {
        "anchor": ANCHOR_SCHEMA,
        "entity": ENTITY_SCHEMA,
        "axis": _slot_schema(set(AXIS_VALUES) | VALUE_SENTINELS),
        "value": _slot_schema(set().union(*AXIS_VALUES.values()) | VALUE_SENTINELS),
        "conditions": CONDITIONS_SCHEMA,
        "phase": PHASE_SCHEMA,
        "quantifier": QUANTIFIER_SCHEMA,
        "polarity": POLARITY_SCHEMA,
        "relation": RELATION_SCHEMA,
        "comparison": {
            "type": "object", "additionalProperties": False,
            "required": sorted(COMPARISON_KEYS),
            "properties": {key: {"enum": sorted(COMPARISONS)} for key in COMPARISON_KEYS},
        },
    },
}


def _result(status="not_evaluable", derived=None, model=None, comparison=False,
            semantic=False, errors=()):
    return {
        "validator_id": VALIDATOR_ID,
        "validator_version": VALIDATOR_VERSION,
        "technical_status": status,
        "derived_label": derived,
        "model_label": model,
        "comparison_verified": comparison,
        "semantic_compatibility_verified": semantic,
        "error_codes": list(dict.fromkeys(errors)),
    }


def _exact_dict(value, keys):
    return type(value) is dict and set(value) == keys


def _valid_entity_id(value):
    if type(value) is not str or not value.startswith("entity:") or len(value) > 71:
        return False
    tail = value[7:]
    return bool(tail) and tail[0].isalnum() and all(ch.islower() or ch.isdigit() or ch in "._-" for ch in tail)


def _anchor_errors(anchors, source_name, text):
    if type(anchors) is not list or len(anchors) > 4:
        return ["E_SCHEMA_INVALID"]
    errors, previous, seen = [], None, set()
    for anchor in anchors:
        keys = {"source", "start", "end", "exact_span"}
        if not _exact_dict(anchor, keys):
            errors.append("E_SCHEMA_INVALID"); continue
        source, start, end, span = (anchor.get("source"), anchor.get("start"),
                                    anchor.get("end"), anchor.get("exact_span"))
        if (source != source_name or type(start) is not int or type(end) is not int or
                type(span) is not str or not span or start < 0 or end <= start or end > len(text) or
                text[start:end] != span or unicodedata.normalize("NFC", span) != span):
            errors.append("E_ANCHOR_INVALID"); continue
        key = (start, end, span)
        if key in seen or (previous is not None and key < previous):
            errors.append("E_ANCHOR_ORDER_OR_DUPLICATE")
        seen.add(key); previous = key
    return errors


def _entity_errors(slot, side, text, is_claim):
    if not _exact_dict(slot, {"status", "entity_id", "anchors"}):
        return ["E_SCHEMA_INVALID"]
    status, entity_id, anchors = slot["status"], slot["entity_id"], slot["anchors"]
    errors = _anchor_errors(anchors, side, text)
    if status not in STATUSES or not _valid_entity_id(entity_id):
        return errors + ["E_SCHEMA_INVALID"]
    sentinel = "entity:" + status
    allowed = ((status == "explicit" and 1 <= len(anchors) <= 4 and entity_id not in
                {"entity:absent", "entity:ambiguous", "entity:unknown"}) or
               (status == "implicit" and len(anchors) == 0 and entity_id not in
                {"entity:absent", "entity:ambiguous", "entity:unknown"}) or
               (status == "absent" and not is_claim and len(anchors) == 0 and entity_id == sentinel) or
               (status == "ambiguous" and 1 <= len(anchors) <= 4 and entity_id == sentinel) or
               (status == "unknown" and len(anchors) == 0 and entity_id == sentinel))
    if not allowed:
        errors.append("E_STATUS_VALUE_INCONSISTENT")
    return errors


def _value_slot_errors(slot, side, text, family, is_claim, axis=None):
    if not _exact_dict(slot, {"status", "value", "anchors"}):
        return ["E_SCHEMA_INVALID"]
    status, value, anchors = slot["status"], slot["value"], slot["anchors"]
    errors = _anchor_errors(anchors, side, text)
    if status not in STATUSES or type(value) is not str:
        return errors + ["E_SCHEMA_INVALID"]
    semantic_values = set(AXIS_VALUES) if family == "axis" else set().union(*AXIS_VALUES.values())
    allowed = ((status == "explicit" and value in semantic_values and 1 <= len(anchors) <= 4) or
               (status == "absent" and not is_claim and value == "absent" and len(anchors) == 0) or
               (status == "ambiguous" and value == "ambiguous" and 1 <= len(anchors) <= 4) or
               (status == "unknown" and value == "unknown" and len(anchors) == 0))
    if status == "implicit" or not allowed:
        errors.append("E_STATUS_VALUE_INCONSISTENT")
    if family == "value" and status == "explicit" and axis in AXIS_VALUES and value not in AXIS_VALUES[axis]:
        errors.append("E_AXIS_VALUE_INCOMPATIBLE")
    return errors


def _conditions_errors(slot, side, text):
    if not _exact_dict(slot, {"status", "items"}) or type(slot.get("items")) is not list:
        return ["E_SCHEMA_INVALID"]
    status, items, errors, ids = slot.get("status"), slot["items"], [], []
    if status not in STATUSES or status == "implicit" or len(items) > 8:
        errors.append("E_STATUS_VALUE_INCONSISTENT")
    expected_nonempty = status in {"explicit", "ambiguous"}
    if bool(items) != expected_nonempty:
        errors.append("E_STATUS_VALUE_INCONSISTENT")
    for item in items:
        if not _exact_dict(item, {"condition_id", "status", "anchors"}):
            errors.append("E_SCHEMA_INVALID"); continue
        cid, item_status = item["condition_id"], item["status"]
        if type(cid) is not str or not cid.startswith("condition:") or item_status not in {"explicit", "ambiguous"}:
            errors.append("E_SCHEMA_INVALID")
        ids.append(cid)
        anchor_errors = _anchor_errors(item["anchors"], side, text)
        errors.extend(anchor_errors)
        if not 1 <= len(item["anchors"]) <= 4:
            errors.append("E_STATUS_VALUE_INCONSISTENT")
    if len(ids) != len(set(ids)):
        errors.append("E_DUPLICATE_LOCAL_ID")
    if status == "ambiguous" and items and not any(item.get("status") == "ambiguous" for item in items if isinstance(item, dict)):
        errors.append("E_STATUS_VALUE_INCONSISTENT")
    return errors


def _phase_errors(slot, side, text):
    if not _exact_dict(slot, {"status", "value", "anchors"}):
        return ["E_SCHEMA_INVALID"]
    status, value, anchors = slot["status"], slot["value"], slot["anchors"]
    errors = _anchor_errors(anchors, side, text)
    allowed = ((status == "explicit" and value in PHASES - {"absent", "ambiguous", "unknown"} and 1 <= len(anchors) <= 4) or
               (status == "implicit" and value == "general" and len(anchors) == 0) or
               (status == "absent" and value == "absent" and len(anchors) == 0) or
               (status == "ambiguous" and value == "ambiguous" and 1 <= len(anchors) <= 4) or
               (status == "unknown" and value == "unknown" and len(anchors) == 0))
    if status not in STATUSES or value not in PHASES or not allowed:
        errors.append("E_STATUS_VALUE_INCONSISTENT")
    return errors


def _quantifier_errors(slot, side, text):
    keys = {"status", "value", "literal", "anchors"}
    if not _exact_dict(slot, keys):
        return ["E_SCHEMA_INVALID"]
    status, value, literal, anchors = slot["status"], slot["value"], slot["literal"], slot["anchors"]
    errors = _anchor_errors(anchors, side, text)
    explicit_values = QUANTIFIERS - {"none", "absent", "ambiguous", "unknown"}
    allowed = ((status == "explicit" and value in explicit_values and 1 <= len(anchors) <= 2) or
               (status == "implicit" and value == "none" and len(anchors) == 0) or
               (status == "absent" and value == "absent" and len(anchors) == 0) or
               (status == "ambiguous" and value == "ambiguous" and 1 <= len(anchors) <= 2) or
               (status == "unknown" and value == "unknown" and len(anchors) == 0))
    if status not in STATUSES or value not in QUANTIFIERS or not allowed:
        errors.append("E_STATUS_VALUE_INCONSISTENT")
    if value == "numeric":
        if type(literal) is not str or not literal:
            errors.append("E_STATUS_VALUE_INCONSISTENT")
    elif literal is not None:
        errors.append("E_STATUS_VALUE_INCONSISTENT")
    return errors


def _polarity_errors(slot, side, text):
    if not _exact_dict(slot, {"status", "value", "anchors"}):
        return ["E_SCHEMA_INVALID"]
    status, value, anchors = slot["status"], slot["value"], slot["anchors"]
    errors = _anchor_errors(anchors, side, text)
    allowed = ((status == "explicit" and value == "negated" and 1 <= len(anchors) <= 2) or
               (status == "implicit" and value == "affirmed" and len(anchors) == 0) or
               (status == "ambiguous" and value == "ambiguous" and 1 <= len(anchors) <= 2) or
               (status == "unknown" and value == "unknown" and len(anchors) == 0))
    if status not in STATUSES or value not in POLARITIES or not allowed:
        errors.append("E_STATUS_VALUE_INCONSISTENT")
    return errors


def _relation_errors(relation, side, text, is_claim):
    if not _exact_dict(relation, RELATION_KEYS):
        return ["E_SCHEMA_INVALID"]
    errors = []
    errors.extend(_entity_errors(relation["subject"], side, text, is_claim))
    errors.extend(_entity_errors(relation["reference"], side, text, is_claim))
    errors.extend(_value_slot_errors(relation["semantic_axis"], side, text, "axis", is_claim))
    axis = relation["semantic_axis"].get("value") if isinstance(relation["semantic_axis"], dict) else None
    errors.extend(_value_slot_errors(relation["value"], side, text, "value", is_claim, axis))
    errors.extend(_conditions_errors(relation["conditions"], side, text))
    errors.extend(_phase_errors(relation["phase"], side, text))
    errors.extend(_quantifier_errors(relation["quantifier"], side, text))
    errors.extend(_polarity_errors(relation["polarity"], side, text))
    return errors


def _expected_comparison(dimension, claim_slot, evidence_slot):
    cstatus, estatus = claim_slot.get("status"), evidence_slot.get("status")
    if dimension == "conditions":
        if cstatus == "ambiguous" or estatus == "ambiguous":
            return {"ambiguous"}
        if cstatus == "unknown" or estatus == "unknown":
            return {"unknown"}
        cids = [item.get("condition_id") for item in claim_slot.get("items", [])]
        eids = [item.get("condition_id") for item in evidence_slot.get("items", [])]
        return {"same"} if cids == eids else {"different"}
    if cstatus == "ambiguous" or estatus == "ambiguous":
        return {"ambiguous"}
    if cstatus in {"absent", "unknown"} or estatus in {"absent", "unknown"}:
        return {"unknown"}
    if dimension in {"subject", "reference"}:
        if claim_slot.get("entity_id") == evidence_slot.get("entity_id"):
            return {"same"}
        return {"compatible", "different"}
    cvalue, evalue = claim_slot.get("value"), evidence_slot.get("value")
    if cvalue == evalue:
        return {"same"}
    if dimension == "value":
        axis = None
        return {"different", "incompatible"}  # narrowed by caller with axis
    if dimension == "polarity" and {cvalue, evalue} == {"affirmed", "negated"}:
        return {"incompatible"}
    if dimension == "quantifier":
        return _quantifier_comparison(evalue, cvalue, evidence_slot.get("literal"), claim_slot.get("literal"))
    return {"different"}


def _quantifier_comparison(evidence, claim, evidence_literal=None, claim_literal=None):
    if evidence == claim:
        if evidence != "numeric" or evidence_literal == claim_literal:
            return {"same"}
        return {"different"}
    strength = {"existential": 0, "some": 1, "many": 2, "most": 3, "all": 4}
    if evidence in strength and claim in strength:
        return {"compatible"} if strength[evidence] >= strength[claim] else {"different"}
    if {evidence, claim} == {"always", "never"}:
        return {"incompatible"}
    return {"different"}


def _comparison_errors(witness):
    comparison = witness.get("comparison")
    if not _exact_dict(comparison, COMPARISON_KEYS) or any(value not in COMPARISONS for value in comparison.values()):
        return ["E_SCHEMA_INVALID"]
    claim, evidence, errors = witness["claim_relation"], witness["evidence_relation"], []
    for dimension in COMPARISON_KEYS:
        allowed = _expected_comparison(dimension, claim[dimension], evidence[dimension])
        if dimension == "value" and not allowed.intersection({"unknown", "ambiguous"}):
            claim_axis = claim["semantic_axis"].get("value")
            evidence_axis = evidence["semantic_axis"].get("value")
            if claim_axis != evidence_axis:
                allowed = {"different"}
            else:
                pair = frozenset((claim["value"].get("value"), evidence["value"].get("value")))
                if pair in INCOMPATIBLE_VALUES.get(claim_axis, set()):
                    allowed = {"incompatible"}
                elif claim["value"].get("value") == evidence["value"].get("value"):
                    allowed = {"same"}
                else:
                    allowed = {"different"}
        if comparison[dimension] not in allowed:
            errors.append("E_COMPARISON_INCONSISTENT")
    return errors


def _claim_target_invalid(claim):
    return any(claim[key].get("status") in {"absent", "unknown", "ambiguous"}
               for key in ("subject", "reference", "semantic_axis", "value"))


def _derive_label(witness):
    claim, evidence, comparison = (witness["claim_relation"], witness["evidence_relation"], witness["comparison"])
    if _claim_target_invalid(claim):
        return None, "E_RELATION_NOT_COMPARABLE"
    if any(evidence[key].get("status") in {"absent", "unknown", "ambiguous"}
           for key in ("subject", "reference", "semantic_axis", "value")):
        return "insufficient", None
    if any(comparison[key] in {"unknown", "ambiguous", "different"}
           for key in ("subject", "semantic_axis", "reference", "conditions", "phase")):
        return "insufficient", None
    if comparison["value"] == "incompatible" or comparison["polarity"] == "incompatible":
        return "contradicted", None
    if comparison["quantifier"] in {"different", "unknown", "ambiguous"}:
        return "insufficient", None
    if comparison["value"] in {"same", "compatible"} and comparison["polarity"] == "same" and comparison["quantifier"] in {"same", "compatible"}:
        return "supported", None
    return "insufficient", None


def validate_spatial_v2(witness, claim_text, evidence_text):
    """Validate one witness without mutation, I/O, model calls or fallback."""
    model_label = witness.get("label") if isinstance(witness, dict) else None
    if type(claim_text) is not str or type(evidence_text) is not str:
        return _result(model=model_label, errors=["E_SCHEMA_INVALID"])
    if unicodedata.normalize("NFC", claim_text) != claim_text or unicodedata.normalize("NFC", evidence_text) != evidence_text:
        return _result(model=model_label, errors=["E_TEXT_NOT_NFC"])
    if not _exact_dict(witness, ROOT_KEYS):
        return _result(model=model_label, errors=["E_SCHEMA_INVALID"])
    if witness["contract_id"] != CONTRACT_ID or witness["contract_version"] != CONTRACT_VERSION:
        return _result(model=model_label, errors=["E_IDENTITY_INVALID"])
    if model_label not in LABELS:
        return _result(model=model_label, errors=["E_SCHEMA_INVALID"])
    errors = _relation_errors(witness["claim_relation"], "claim", claim_text, True)
    errors += _relation_errors(witness["evidence_relation"], "evidence", evidence_text, False)
    if errors:
        return _result(model=model_label, errors=errors)
    errors = _comparison_errors(witness)
    if errors:
        return _result(model=model_label, errors=errors)
    derived, derivation_error = _derive_label(witness)
    if derivation_error:
        return _result(model=model_label, comparison=True, errors=[derivation_error])
    if derived != model_label:
        return _result(derived=derived, model=model_label, comparison=True,
                       errors=["E_LABEL_WITNESS_MISMATCH"])
    uses_compatible = witness["comparison"]["subject"] == "compatible" or witness["comparison"]["reference"] == "compatible"
    return _result("valid", derived, model_label, True, not uses_compatible, [])
