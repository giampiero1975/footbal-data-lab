#!/usr/bin/env python3
"""Pure extraction contract and deterministic locator for Spatial V2.

The model-facing contract contains literal fragments but no source or offsets.
This module performs no I/O and never calls a model. It materializes a regular
Spatial V2 witness only when every fragment occurs exactly once on its
structurally assigned side, then delegates final authority to the unchanged
Spatial V2 validator.
"""
from __future__ import annotations

import hashlib
import json

import v5_tactical_semantic_support_s2_spatial_v2 as spatial_v2


CONTRACT_ID = "nli_spatial_relations_v2_extraction"
CONTRACT_VERSION = "1.0.0"
LOCATOR_ID = "nli_spatial_relations_v2_literal_locator"
LOCATOR_VERSION = "1.0.0"


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def digest_document(value):
    return "sha256:" + hashlib.sha256(
        canonical_json(value).encode("utf-8")).hexdigest()


def digest_text(value):
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _fragments_schema(maximum=4):
    return {
        "type": "array", "maxItems": maximum, "uniqueItems": True,
        "items": {"type": "string", "minLength": 1},
    }


def _slot_schema(values, maximum=4):
    return {
        "type": "object", "additionalProperties": False,
        "required": ["status", "value", "selected_fragments"],
        "properties": {
            "status": {"enum": sorted(spatial_v2.STATUSES)},
            "value": {"enum": sorted(values)},
            "selected_fragments": _fragments_schema(maximum),
        },
    }


def _described(schema, description):
    value = dict(schema)
    value["description"] = description
    return value


ENTITY_EXTRACTION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["status", "entity_id", "selected_fragments"],
    "properties": {
        "status": {"enum": sorted(spatial_v2.STATUSES)},
        "entity_id": {"type": "string"},
        "selected_fragments": _fragments_schema(),
    },
}
CONDITIONS_EXTRACTION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["status", "items"],
    "properties": {
        "status": {"enum": sorted(spatial_v2.STATUSES)},
        "items": {
            "type": "array", "maxItems": 8,
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["condition_id", "status", "selected_fragments"],
                "properties": {
                    "condition_id": {"type": "string"},
                    "status": {"enum": ["explicit", "ambiguous"]},
                    "selected_fragments": _fragments_schema(),
                },
            },
        },
    },
}
QUANTIFIER_EXTRACTION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["status", "value", "literal", "selected_fragments"],
    "properties": {
        "status": {"enum": sorted(spatial_v2.STATUSES)},
        "value": {"enum": sorted(spatial_v2.QUANTIFIERS)},
        "literal": {"type": ["string", "null"], "maxLength": 64},
        "selected_fragments": _fragments_schema(2),
    },
}
RELATION_EXTRACTION_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": sorted(spatial_v2.RELATION_KEYS),
    "properties": {
        "subject": _described(
            ENTITY_EXTRACTION_SCHEMA,
            "Actor or entity whose spatial relation is asserted on this side."),
        "semantic_axis": _described(_slot_schema(
            set(spatial_v2.AXIS_VALUES) | spatial_v2.VALUE_SENTINELS),
            "Versioned Spatial V2 semantic dimension; value must be compatible with it."),
        "reference": _described(
            ENTITY_EXTRACTION_SCHEMA,
            "Referent of the spatial relation on this same side, never text from the opposite side."),
        "value": _described(_slot_schema(
            set().union(*spatial_v2.AXIS_VALUES.values()) |
            spatial_v2.VALUE_SENTINELS),
            "Value asserted for semantic_axis; only the versioned axis value set is allowed."),
        "conditions": _described(
            CONDITIONS_EXTRACTION_SCHEMA,
            "Conditions that delimit the relation on this side."),
        "phase": _described(
            _slot_schema(spatial_v2.PHASES),
            "Tactical phase explicitly or implicitly assigned on this side."),
        "quantifier": _described(
            QUANTIFIER_EXTRACTION_SCHEMA,
            "Quantity or frequency scope of the relation on this side."),
        "polarity": _described(
            _slot_schema(spatial_v2.POLARITIES, 2),
            "Affirmed or negated polarity of the relation on this side."),
    },
}
EXTRACTION_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "urn:football-data-lab:nli-spatial-relations-v2-extraction:1.0.0",
    "type": "object", "additionalProperties": False,
    "required": sorted(spatial_v2.ROOT_KEYS),
    "properties": {
        "contract_id": {"const": CONTRACT_ID},
        "contract_version": {"const": CONTRACT_VERSION},
        "label": {"enum": sorted(spatial_v2.LABELS)},
        "claim_relation": {
            "$ref": "#/$defs/relation",
            "description": "Relation extracted only from the claim (AFFERMAZIONE).",
        },
        "evidence_relation": {
            "$ref": "#/$defs/relation",
            "description": "Relation extracted only from the evidence (FONTE).",
        },
        "comparison": {"$ref": "#/$defs/comparison"},
    },
    "$defs": {
        "relation": RELATION_EXTRACTION_SCHEMA,
        "comparison": {
            "type": "object", "additionalProperties": False,
            "required": sorted(spatial_v2.COMPARISON_KEYS),
            "properties": {
                key: {"enum": sorted(spatial_v2.COMPARISONS)}
                for key in spatial_v2.COMPARISON_KEYS
            },
        },
    },
}


def descriptor():
    return {
        "contract_id": CONTRACT_ID, "version": CONTRACT_VERSION,
        "locator_id": LOCATOR_ID, "locator_version": LOCATOR_VERSION,
        "selection": "explicit_opt_in_only",
        "matching": "literal_unique_on_structurally_assigned_side",
        "normalization": False, "fuzzy_matching": False, "repair": False,
        "promotion_authorized": False,
    }


def _exact_dict(value, keys):
    return type(value) is dict and set(value) == keys


def _fragments_valid(value, maximum):
    return (type(value) is list and len(value) <= maximum and
            all(type(item) is str and bool(item) for item in value) and
            len(value) == len(set(value)))


def _slot_shape_errors(slot, path, values, maximum=4):
    keys = {"status", "value", "selected_fragments"}
    if not _exact_dict(slot, keys):
        return [{"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path}]
    errors = []
    if type(slot["status"]) is not str or slot["status"] not in spatial_v2.STATUSES:
        errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path + ".status"})
    if type(slot["value"]) is not str or slot["value"] not in values:
        errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path + ".value"})
    if not _fragments_valid(slot["selected_fragments"], maximum):
        errors.append({"code": "E_EXTRACTION_FRAGMENT_INVALID", "path": path + ".selected_fragments"})
    return errors


def _entity_shape_errors(slot, path):
    keys = {"status", "entity_id", "selected_fragments"}
    if not _exact_dict(slot, keys):
        return [{"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path}]
    errors = []
    if type(slot["status"]) is not str or slot["status"] not in spatial_v2.STATUSES:
        errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path + ".status"})
    if type(slot["entity_id"]) is not str:
        errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path + ".entity_id"})
    if not _fragments_valid(slot["selected_fragments"], 4):
        errors.append({"code": "E_EXTRACTION_FRAGMENT_INVALID", "path": path + ".selected_fragments"})
    return errors


def _conditions_shape_errors(slot, path):
    if not _exact_dict(slot, {"status", "items"}):
        return [{"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path}]
    errors = []
    if type(slot["status"]) is not str or slot["status"] not in spatial_v2.STATUSES:
        errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path + ".status"})
    if type(slot["items"]) is not list or len(slot["items"]) > 8:
        return errors + [{"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path + ".items"}]
    for index, item in enumerate(slot["items"]):
        item_path = f"{path}.items[{index}]"
        if not _exact_dict(item, {"condition_id", "status", "selected_fragments"}):
            errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": item_path})
            continue
        if (type(item["condition_id"]) is not str or
                type(item["status"]) is not str or
                item["status"] not in {"explicit", "ambiguous"}):
            errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": item_path})
        if not _fragments_valid(item["selected_fragments"], 4):
            errors.append({"code": "E_EXTRACTION_FRAGMENT_INVALID", "path": item_path + ".selected_fragments"})
    return errors


def _quantifier_shape_errors(slot, path):
    keys = {"status", "value", "literal", "selected_fragments"}
    if not _exact_dict(slot, keys):
        return [{"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path}]
    errors = _slot_shape_errors(
        {key: slot[key] for key in ("status", "value", "selected_fragments")},
        path, spatial_v2.QUANTIFIERS, 2)
    if slot["literal"] is not None and type(slot["literal"]) is not str:
        errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path + ".literal"})
    elif type(slot["literal"]) is str and len(slot["literal"]) > 64:
        errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": path + ".literal"})
    return errors


def extraction_shape_errors(extraction):
    if not _exact_dict(extraction, spatial_v2.ROOT_KEYS):
        return [{"code": "E_EXTRACTION_SCHEMA_INVALID", "path": "$"}]
    errors = []
    if (extraction.get("contract_id") != CONTRACT_ID or
            extraction.get("contract_version") != CONTRACT_VERSION):
        errors.append({"code": "E_EXTRACTION_IDENTITY_INVALID", "path": "$"})
    if (type(extraction.get("label")) is not str or
            extraction["label"] not in spatial_v2.LABELS):
        errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": "label"})
    comparison = extraction.get("comparison")
    if (not _exact_dict(comparison, spatial_v2.COMPARISON_KEYS) or
            any(type(value) is not str or value not in spatial_v2.COMPARISONS
                for value in comparison.values())):
        errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": "comparison"})
    for side in ("claim_relation", "evidence_relation"):
        relation = extraction.get(side)
        if not _exact_dict(relation, spatial_v2.RELATION_KEYS):
            errors.append({"code": "E_EXTRACTION_SCHEMA_INVALID", "path": side})
            continue
        errors += _entity_shape_errors(relation["subject"], side + ".subject")
        errors += _slot_shape_errors(relation["semantic_axis"], side + ".semantic_axis",
                                     set(spatial_v2.AXIS_VALUES) |
                                     spatial_v2.VALUE_SENTINELS)
        errors += _entity_shape_errors(relation["reference"], side + ".reference")
        errors += _slot_shape_errors(relation["value"], side + ".value",
                                     set().union(*spatial_v2.AXIS_VALUES.values()) |
                                     spatial_v2.VALUE_SENTINELS)
        errors += _conditions_shape_errors(relation["conditions"], side + ".conditions")
        errors += _slot_shape_errors(relation["phase"], side + ".phase", spatial_v2.PHASES)
        errors += _quantifier_shape_errors(relation["quantifier"], side + ".quantifier")
        errors += _slot_shape_errors(relation["polarity"], side + ".polarity",
                                     spatial_v2.POLARITIES, 2)
    return errors


def extraction_semantic_errors(extraction):
    """Apply versioned Spatial V2 semantic rules before literal localization."""
    errors = []
    for side in ("claim_relation", "evidence_relation"):
        relation = extraction[side]
        axis_slot, value_slot = relation["semantic_axis"], relation["value"]
        axis, value = axis_slot["value"], value_slot["value"]
        if (axis_slot["status"] == "explicit" and
                value_slot["status"] == "explicit" and
                axis in spatial_v2.AXIS_VALUES and
                value not in spatial_v2.AXIS_VALUES[axis]):
            errors.append({
                "code": "E_EXTRACTION_AXIS_VALUE_INCOMPATIBLE",
                "path": side + ".value", "semantic_axis": axis,
                "value": value,
            })
    # Reuse the versioned final-validator comparison rules verbatim.  This is
    # an early fail-closed boundary only; validate_spatial_v2 remains final.
    if "E_COMPARISON_INCONSISTENT" in spatial_v2._comparison_errors(extraction):
        errors.append({
            "code": "E_EXTRACTION_COMPARISON_INCONSISTENT",
            "path": "comparison",
        })
    return errors


def _occurrences(text, fragment):
    positions, offset = [], 0
    while True:
        position = text.find(fragment, offset)
        if position < 0:
            return positions
        positions.append(position)
        offset = position + 1


def _localize_fragments(fragments, side, text, field_id, records):
    anchors, failed = [], False
    text_sha256 = digest_text(text)
    for index, fragment in enumerate(fragments):
        positions = _occurrences(text, fragment)
        unique = len(positions) == 1
        start = positions[0] if unique else None
        end = start + len(fragment) if unique else None
        record = {
            "field_id": f"{field_id}.selected_fragments[{index}]",
            "side": side, "source_text_sha256": text_sha256,
            "selected_fragment": fragment,
            "occurrence_count": len(positions), "start": start, "end": end,
            "result": ("localized" if unique else
                       "missing" if not positions else "ambiguous"),
        }
        records.append(record)
        if not unique:
            failed = True
            continue
        anchor = {"source": side, "start": start, "end": end,
                  "exact_span": fragment}
        if text[start:end] != fragment:
            record["result"] = "slice_mismatch"
            failed = True
            continue
        anchors.append(anchor)
    return anchors, failed


def _materialize_relation(relation, side, text, records):
    failed = False

    def localized(slot, field):
        nonlocal failed
        anchors, slot_failed = _localize_fragments(
            slot["selected_fragments"], side, text,
            f"{side}_relation.{field}", records)
        failed = failed or slot_failed
        return anchors

    output = {}
    for field in ("subject", "reference"):
        slot = relation[field]
        output[field] = {
            "status": slot["status"], "entity_id": slot["entity_id"],
            "anchors": localized(slot, field),
        }
    for field in ("semantic_axis", "value", "phase", "polarity"):
        slot = relation[field]
        output[field] = {
            "status": slot["status"], "value": slot["value"],
            "anchors": localized(slot, field),
        }
    quantifier = relation["quantifier"]
    output["quantifier"] = {
        "status": quantifier["status"], "value": quantifier["value"],
        "literal": quantifier["literal"],
        "anchors": localized(quantifier, "quantifier"),
    }
    conditions = relation["conditions"]
    output["conditions"] = {"status": conditions["status"], "items": []}
    for index, item in enumerate(conditions["items"]):
        anchors, item_failed = _localize_fragments(
            item["selected_fragments"], side, text,
            f"{side}_relation.conditions.items[{index}]", records)
        failed = failed or item_failed
        output["conditions"]["items"].append({
            "condition_id": item["condition_id"], "status": item["status"],
            "anchors": anchors,
        })
    return output, failed


def _provenance(extraction, claim_text, evidence_text, records, status):
    value = {
        "contract_id": CONTRACT_ID, "contract_version": CONTRACT_VERSION,
        "locator_id": LOCATOR_ID, "locator_version": LOCATOR_VERSION,
        "extraction_sha256": digest_document(extraction),
        "source_text_sha256": {
            "claim": digest_text(claim_text),
            "evidence": digest_text(evidence_text),
        },
        "status": status, "records": records, "record_sha256": None,
    }
    value["record_sha256"] = digest_document(value)
    return value


def boundary_failure(code, *, extraction=None, claim_text="", evidence_text="",
                     details=()):
    safe_extraction = extraction if isinstance(extraction, dict) else {}
    safe_claim = claim_text if isinstance(claim_text, str) else ""
    safe_evidence = evidence_text if isinstance(evidence_text, str) else ""
    return {
        "evaluation_status": "not_evaluable", "witness": None,
        "validation": None,
        "localization": _provenance(
            safe_extraction, safe_claim, safe_evidence, [], "not_evaluable"),
        "reason_codes": [code], "details": list(details),
        "promotion_authorized": False,
    }


def materialize_extraction(extraction, claim_text, evidence_text):
    """Materialize and validate without mutation, I/O, models or fallback."""
    if type(claim_text) is not str or type(evidence_text) is not str:
        return boundary_failure("E_EXTRACTION_TEXT_INVALID", extraction=extraction)
    shape_errors = extraction_shape_errors(extraction)
    if shape_errors:
        return boundary_failure(
            "E_EXTRACTION_SCHEMA_INVALID", extraction=extraction,
            claim_text=claim_text, evidence_text=evidence_text,
            details=shape_errors)
    semantic_errors = extraction_semantic_errors(extraction)
    if semantic_errors:
        return boundary_failure(
            "E_EXTRACTION_SEMANTIC_INCONSISTENT", extraction=extraction,
            claim_text=claim_text, evidence_text=evidence_text,
            details=semantic_errors)
    records = []
    claim_relation, claim_failed = _materialize_relation(
        extraction["claim_relation"], "claim", claim_text, records)
    evidence_relation, evidence_failed = _materialize_relation(
        extraction["evidence_relation"], "evidence", evidence_text, records)
    if claim_failed or evidence_failed:
        return {
            "evaluation_status": "not_evaluable", "witness": None,
            "validation": None,
            "localization": _provenance(
                extraction, claim_text, evidence_text, records,
                "not_evaluable"),
            "reason_codes": ["E_EXTRACTION_LOCALIZATION_NOT_UNIQUE"],
            "details": [], "promotion_authorized": False,
        }
    witness = {
        "contract_id": spatial_v2.CONTRACT_ID,
        "contract_version": spatial_v2.CONTRACT_VERSION,
        "label": extraction["label"],
        "claim_relation": claim_relation,
        "evidence_relation": evidence_relation,
        "comparison": dict(extraction["comparison"]),
    }
    validation = spatial_v2.validate_spatial_v2(
        witness, claim_text, evidence_text)
    valid = validation["technical_status"] == "valid"
    return {
        "evaluation_status": "evaluated" if valid else "not_evaluable",
        "witness": witness, "validation": validation,
        "localization": _provenance(
            extraction, claim_text, evidence_text, records, "materialized"),
        "reason_codes": [] if valid else list(validation["error_codes"]),
        "details": [], "promotion_authorized": False,
    }


def verify_materialization(result, extraction, claim_text, evidence_text):
    """Recompute the pure result; any altered provenance fails closed."""
    try:
        expected = materialize_extraction(
            extraction, claim_text, evidence_text)
        return [] if canonical_json(result) == canonical_json(expected) else [
            "E_EXTRACTION_PROVENANCE_MISMATCH"]
    except (TypeError, ValueError, KeyError):
        return ["E_EXTRACTION_PROVENANCE_MISMATCH"]
