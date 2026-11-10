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


REPRESENTATION_REVISION = "status-correlated-01"


def _fragments_schema(maximum=4, minimum=0):
    return {
        "type": "array", "minItems": minimum, "maxItems": maximum, "uniqueItems": True,
        "items": {"type": "string", "minLength": 1},
    }


def _object_schema(properties):
    return {
        "type": "object", "additionalProperties": False,
        "required": list(properties), "properties": properties,
    }


def _slot_schema(values, maximum=4, *, implicit=None, absent=True,
                 numeric_literal=False):
    """Complete alternatives, never properties mixed with anyOf or if/then."""
    concrete = set(values) - {"absent", "ambiguous", "unknown", "none"}
    branches = []

    def branch(status, allowed, minimum, limit, literal=None):
        properties = {"status": {"enum": [status]},
                      "value": {"enum": sorted(allowed)}}
        if numeric_literal:
            properties["literal"] = literal or {"type": "null"}
        properties["selected_fragments"] = _fragments_schema(limit, minimum)
        return _object_schema(properties)

    if numeric_literal:
        branches.append(branch("explicit", concrete - {"numeric"}, 1, maximum))
        branches.append(branch("explicit", {"numeric"}, 1, maximum,
                               {"type": "string", "minLength": 1, "maxLength": 64}))
    elif concrete:
        branches.append(branch("explicit", concrete, 1, maximum))
    if implicit is not None:
        branches.append(branch("implicit", {implicit}, 0, 0))
    if absent:
        branches.append(branch("absent", {"absent"}, 0, 0))
    branches.extend([branch("ambiguous", {"ambiguous"}, 1, maximum),
                     branch("unknown", {"unknown"}, 0, 0)])
    return {"anyOf": branches}


def _described(schema, description):
    value = dict(schema)
    value["description"] = description
    return value


def _entity_schema():
    branches = []
    for status, minimum, maximum in (("explicit", 1, 4), ("implicit", 0, 0),
                                      ("absent", 0, 0), ("ambiguous", 1, 4),
                                      ("unknown", 0, 0)):
        identity = ({"type": "string", "minLength": 8, "maxLength": 71,
                     "pattern": "^entity:.+$"}
                    if status in {"explicit", "implicit"}
                    else {"enum": ["entity:" + status]})
        branches.append(_object_schema({
            "status": {"enum": [status]}, "entity_id": identity,
            "selected_fragments": _fragments_schema(maximum, minimum)}))
    return {"anyOf": branches}


def _conditions_schema():
    item = _object_schema({"condition_id": {"type": "string", "minLength": 10},
                           "status": {"enum": ["explicit", "ambiguous"]},
                           "selected_fragments": _fragments_schema(4, 1)})
    return {"anyOf": [_object_schema({
        "status": {"enum": [status]},
        "items": {"type": "array", "minItems": minimum, "maxItems": maximum,
                  "items": item}})
        for status, minimum, maximum in (("explicit", 1, 8), ("absent", 0, 0),
                                         ("ambiguous", 1, 8), ("unknown", 0, 0))]}


ENTITY_EXTRACTION_SCHEMA = _entity_schema()
CONDITIONS_EXTRACTION_SCHEMA = _conditions_schema()
QUANTIFIER_EXTRACTION_SCHEMA = _slot_schema(
    spatial_v2.QUANTIFIERS, 2, implicit="none", numeric_literal=True)
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
            _slot_schema(spatial_v2.PHASES, implicit="general"),
            "Tactical phase explicitly or implicitly assigned on this side."),
        "quantifier": _described(
            QUANTIFIER_EXTRACTION_SCHEMA,
            "Quantity or frequency scope of the relation on this side."),
        "polarity": _described(
            _slot_schema({"negated", "ambiguous", "unknown"}, 2,
                         implicit="affirmed", absent=False),
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
        "representation_revision": REPRESENTATION_REVISION,
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


def _representation_errors(relation, side):
    """Check status/content correlations without locating or inventing anchors.

    These predicates preserve the final Spatial V2 rules. Cross-slot semantics
    and literal localization remain separate, unchanged gates.
    """
    errors = []
    is_claim = side == "claim_relation"

    def reject(field):
        errors.append({"code": "E_EXTRACTION_STATUS_CONTENT_INCONSISTENT",
                       "path": side + "." + field})

    for field in ("subject", "reference"):
        slot = relation[field]
        status, identity, count = slot["status"], slot["entity_id"], len(slot["selected_fragments"])
        concrete = identity not in {"entity:absent", "entity:ambiguous", "entity:unknown"}
        allowed = ((status == "explicit" and concrete and 1 <= count <= 4) or
                   (status == "implicit" and concrete and count == 0) or
                   (status == "absent" and not is_claim and identity == "entity:absent" and count == 0) or
                   (status == "ambiguous" and identity == "entity:ambiguous" and 1 <= count <= 4) or
                   (status == "unknown" and identity == "entity:unknown" and count == 0))
        if not spatial_v2._valid_entity_id(identity) or not allowed:
            reject(field)

    semantic_values = {
        "semantic_axis": set(spatial_v2.AXIS_VALUES),
        "value": set().union(*spatial_v2.AXIS_VALUES.values()),
        "phase": spatial_v2.PHASES - {"absent", "ambiguous", "unknown"},
        "quantifier": spatial_v2.QUANTIFIERS - {"none", "absent", "ambiguous", "unknown"},
        "polarity": {"negated"},
    }
    implicit_values = {"phase": "general", "quantifier": "none", "polarity": "affirmed"}
    for field, values in semantic_values.items():
        slot = relation[field]
        status, value, count = slot["status"], slot["value"], len(slot["selected_fragments"])
        maximum = 2 if field in {"quantifier", "polarity"} else 4
        absent_allowed = field != "polarity" and (field not in {"semantic_axis", "value"} or not is_claim)
        allowed = ((status == "explicit" and value in values and 1 <= count <= maximum) or
                   (status == "implicit" and field in implicit_values and value == implicit_values[field] and count == 0) or
                   (status == "absent" and absent_allowed and value == "absent" and count == 0) or
                   (status == "ambiguous" and value == "ambiguous" and 1 <= count <= maximum) or
                   (status == "unknown" and value == "unknown" and count == 0))
        if field == "quantifier":
            literal = slot["literal"]
            allowed = allowed and ((value == "numeric" and type(literal) is str and bool(literal)) or
                                   (value != "numeric" and literal is None))
        if not allowed:
            reject(field)

    conditions = relation["conditions"]
    status, items = conditions["status"], conditions["items"]
    if (status == "implicit" or bool(items) != (status in {"explicit", "ambiguous"}) or
            (status == "ambiguous" and not any(item["status"] == "ambiguous" for item in items))):
        reject("conditions")
    identities = []
    for index, item in enumerate(items):
        identities.append(item["condition_id"])
        if (not item["condition_id"].startswith("condition:") or
                not 1 <= len(item["selected_fragments"]) <= 4):
            reject("conditions.items." + str(index))
    if len(identities) != len(set(identities)):
        reject("conditions.items")
    return errors


def extraction_handoff_instructions():
    """Normative opt-in instructions; no case text, Gold or model invocation."""
    matrix = {axis: sorted(values) for axis, values in sorted(spatial_v2.AXIS_VALUES.items())}
    incompatible = {axis: sorted(sorted(pair) for pair in pairs)
                    for axis, pairs in sorted(spatial_v2.INCOMPATIBLE_VALUES.items())}
    return """Classifica l'affermazione rispetto alla sola fonte. Restituisci esclusivamente nli_spatial_relations_v2_extraction 1.0.0.
Grounding separato: claim_relation usa soltanto l'AFFERMAZIONE; evidence_relation soltanto la FONTE. subject e l'attore, reference il referente spaziale nello stesso lato. Ogni selected_fragment e letterale, non vuoto e non parafrasato; non spostarlo fra lati. Non produrre offset, start/end o source: il locator side-bound resta letterale e non ripara frammenti mancanti o ripetuti.
STATI E CONTENUTO, prima di qualsiasi confronto:
explicit: informazione affermata nel testo di quel lato, con frammenti che la ancorano. implicit: informazione consentita dal contratto senza frammenti, non una licenza per inventare. absent: assenza rappresentata dalla sentinella, distinta da unknown. ambiguous: informazione presente ma ambigua, con frammenti. unknown: informazione non determinabile, senza contenuto concreto o frammenti; non trasformare l'incertezza in certezza per soddisfare lo schema.
Entita subject/reference: explicit usa entity_id concreto valido entity:<identificatore> e 1-4 frammenti; implicit usa ID concreto e zero frammenti; ambiguous usa entity:ambiguous e 1-4 frammenti; unknown usa entity:unknown e zero frammenti; absent usa entity:absent e zero frammenti solo nel lato evidence. Gli identificatori concreti non sono le sentinelle, hanno al massimo 71 caratteri; il suffisso inizia con lettera minuscola o cifra e contiene solo lettere minuscole, cifre, punti, trattini o underscore.
Asse e valore: explicit usa valore del vocabolario e 1-4 frammenti; ambiguous usa value=ambiguous e 1-4 frammenti; unknown usa value=unknown e zero frammenti; absent usa value=absent e zero frammenti solo nel lato evidence. implicit non e ammesso per asse o valore.
Phase: explicit usa fase concreta e 1-4 frammenti; implicit usa general e zero frammenti; absent/unknown usano la rispettiva sentinella e zero frammenti; ambiguous usa ambiguous e 1-4 frammenti.
Quantifier: explicit usa quantificatore concreto diverso da none e 1-2 frammenti; numeric richiede literal non vuoto (massimo 64 caratteri), negli altri casi literal=null. implicit usa none e zero frammenti; absent/unknown usano la propria sentinella e zero frammenti; ambiguous usa ambiguous e 1-2 frammenti.
Polarity: explicit usa negated e 1-2 frammenti; implicit usa affirmed e zero frammenti; ambiguous usa ambiguous e 1-2 frammenti; unknown usa unknown e zero frammenti. absent non e ammesso. Una riduzione quantitativa non e automaticamente una negazione grammaticale.
Conditions: absent/unknown hanno items=[]; explicit/ambiguous hanno 1-8 item distinti. Ogni item usa condition_id con prefisso condition:, status explicit o ambiguous e 1-4 frammenti. Un contenitore ambiguous richiede almeno un item ambiguous; un item ambiguous non cambia automaticamente il contenitore explicit in ambiguous. implicit non e ammesso.
DIMENSIONI: space_availability misura quanta disponibilita offre la regione identificata: abundant e ampia, scarce e limitata/ridotta, neutral richiede una disponibilita neutra affermata, non assenza di informazione. relative_position descrive la posizione di una entita rispetto al referente, non la quantita disponibile. movement_direction riguarda il moto dell'attore; l'avanzamento consentito in una regione non dimostra disponibilita in un'altra. Seleziona grounding del valore da ciascun lato senza trasferire significati fra regioni.
MATRICE ASSE-VALORI: """ + json.dumps(matrix, sort_keys=True) + """
COPPIE DI VALORI INCOMPATIBILI VERSIONATE: """ + json.dumps(incompatible, sort_keys=True) + """
COMPARISON: precedenza degli stati su ID e valori. Per conditions, se un contenitore e ambiguous il confronto e ambiguous; altrimenti se uno e unknown e unknown; solo dopo confronta gli elenchi ordinati condition_id (uguali=same, diversi=different). Per ogni altra dimensione, ambiguous prevale; altrimenti uno stato absent o unknown richiede comparison=unknown, anche quando ID o valori sono stringhe uguali. Non correggere a posteriori il contenuto per ottenere un confronto favorevole.
Solo con stati confrontabili: semantic_axis con valore uguale richiede same, con valore diverso different. subject/reference con ID identici richiedono same, con ID diversi ammettono compatible o different; compatible resta una dichiarazione shadow, non una prova indipendente di coreferenza. Per value, assi differenti richiedono different; sullo stesso asse coppie nella tabella richiedono incompatible, valori uguali same e altri valori different. Polarity affirmed/negated richiede incompatible; valori uguali same. Phase confrontabile uguale richiede same, diversa different.
Quantifier confrontabile: valori uguali richiedono same, salvo numeric con literal diversi che richiede different. La scala existential < some < many < most < all ammette compatible solo quando la forza evidence e almeno quella claim, altrimenti different. always/never richiede incompatible; gli altri valori diversi different. Non usare compatible come sostituto generico di unknown.
LABEL proposta: il contratto non puo valutare un target claim subject/reference/asse/value unknown o ambiguous; preserva l'incertezza senza inventare valori. Un target evidence non determinabile o subject/reference/asse/conditions/phase different, unknown o ambiguous non dimostra supporto. Su relazioni confrontabili value o polarity incompatible deriva contradicted; altrimenti quantifier non confrontabile rende insufficient; supported richiede value same/compatible, polarity same e quantifier same/compatible. La label deve rispettare tutte le precedenze, non solo l'uguaglianza dei valori.
Non normalizzare o riscrivere label, comparison, status o frammenti. Nessun repair o fallback. Il precontrollo e il validatore finale restano fail-closed; JSON conforme non prova correttezza semantica. Rispondi soltanto con JSON conforme allo schema di estrazione."""


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
        previous_errors = len(errors)
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
        if len(errors) == previous_errors:
            errors += _representation_errors(relation, side)
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
