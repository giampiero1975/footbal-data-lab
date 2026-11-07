import copy
import importlib
import json
import sys
import unittest
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import v5_tactical_semantic_support_s2_spatial_v2 as spatial
import shadow_nli_spatial_relations_v2_inference as judge


CLAIM = "La difesa bassa lascia molto spazio tra linea e porta."
EVIDENCE = "Le squadre che difendono basse tolgono spazio tra linea e porta."


def anchor(source, text, span, occurrence=0):
    start = -1
    offset = 0
    for _ in range(occurrence + 1):
        start = text.index(span, offset)
        offset = start + 1
    return {"source": source, "start": start, "end": start + len(span), "exact_span": span}


def entity(source, text, entity_id, span, status="explicit"):
    anchors = [] if status == "implicit" else [anchor(source, text, span)]
    return {"status": status, "entity_id": entity_id, "anchors": anchors}


def relation(source, text, *, subject_id, subject_span, reference_id,
             reference_span, value, value_span):
    return {
        "subject": entity(source, text, subject_id, subject_span),
        "semantic_axis": {"status": "explicit", "value": "space_availability",
                          "anchors": [anchor(source, text, "spazio")]},
        "reference": entity(source, text, reference_id, reference_span),
        "value": {"status": "explicit", "value": value,
                  "anchors": [anchor(source, text, value_span)]},
        "conditions": {"status": "absent", "items": []},
        "phase": {"status": "implicit", "value": "general", "anchors": []},
        "quantifier": {"status": "implicit", "value": "none", "literal": None,
                       "anchors": []},
        "polarity": {"status": "implicit", "value": "affirmed", "anchors": []},
    }


def witness(label="contradicted"):
    return {
        "contract_id": spatial.CONTRACT_ID,
        "contract_version": spatial.CONTRACT_VERSION,
        "label": label,
        "claim_relation": relation(
            "claim", CLAIM, subject_id="entity:low-block", subject_span="difesa bassa",
            reference_id="entity:line-goal-space", reference_span="tra linea e porta",
            value="abundant", value_span="molto spazio"),
        "evidence_relation": relation(
            "evidence", EVIDENCE, subject_id="entity:defending-low", subject_span="squadre che difendono basse",
            reference_id="entity:line-goal-space", reference_span="tra linea e porta",
            value="scarce", value_span="tolgono spazio"),
        "comparison": {
            "subject": "compatible", "semantic_axis": "same", "reference": "same",
            "value": "incompatible", "conditions": "same", "phase": "same",
            "quantifier": "same", "polarity": "same",
        },
    }


class SpatialV2ValidatorTests(unittest.TestCase):
    def test_01_q3_04_shape_is_representable_not_semantically_verified(self):
        result = spatial.validate_spatial_v2(witness(), CLAIM, EVIDENCE)
        self.assertEqual(result["technical_status"], "valid")
        self.assertEqual(result["derived_label"], "contradicted")
        self.assertTrue(result["comparison_verified"])
        self.assertFalse(result["semantic_compatibility_verified"])

    def test_02_root_shape_identity_and_extra_fields_fail_closed(self):
        mutations = []
        for key in spatial.ROOT_KEYS:
            value = witness(); value.pop(key); mutations.append(value)
        value = witness(); value["extra"] = True; mutations.append(value)
        value = witness(); value["contract_version"] = "2.0.1"; mutations.append(value)
        for value in mutations:
            with self.subTest(keys=value.keys()):
                self.assertEqual(spatial.validate_spatial_v2(value, CLAIM, EVIDENCE)["technical_status"], "not_evaluable")

    def test_03_axis_value_binding_accepts_stable_only_for_approved_axes(self):
        for axis in ("distance_change", "area_extent"):
            value = witness("supported")
            for side in ("claim_relation", "evidence_relation"):
                value[side]["semantic_axis"]["value"] = axis
                value[side]["value"]["value"] = "stable"
            value["comparison"]["value"] = "same"
            self.assertEqual(spatial.validate_spatial_v2(value, CLAIM, EVIDENCE)["technical_status"], "valid")
        invalid = witness()
        invalid["claim_relation"]["value"]["value"] = "stable"
        result = spatial.validate_spatial_v2(invalid, CLAIM, EVIDENCE)
        self.assertIn("E_AXIS_VALUE_INCOMPATIBLE", result["error_codes"])

    def test_04_claim_unknown_is_not_evaluable_evidence_unknown_is_insufficient(self):
        claim_unknown = witness()
        claim_unknown["claim_relation"]["value"] = {"status": "unknown", "value": "unknown", "anchors": []}
        claim_unknown["comparison"]["value"] = "unknown"
        self.assertEqual(spatial.validate_spatial_v2(claim_unknown, CLAIM, EVIDENCE)["derived_label"], None)
        evidence_unknown = witness("insufficient")
        evidence_unknown["evidence_relation"]["value"] = {"status": "unknown", "value": "unknown", "anchors": []}
        evidence_unknown["comparison"]["value"] = "unknown"
        result = spatial.validate_spatial_v2(evidence_unknown, CLAIM, EVIDENCE)
        self.assertEqual((result["technical_status"], result["derived_label"]), ("valid", "insufficient"))

    def test_05_status_sentinels_and_claim_absent_fail_closed(self):
        value = witness()
        value["claim_relation"]["subject"] = {"status": "absent", "entity_id": "entity:absent", "anchors": []}
        value["comparison"]["subject"] = "unknown"
        result = spatial.validate_spatial_v2(value, CLAIM, EVIDENCE)
        self.assertIn("E_STATUS_VALUE_INCONSISTENT", result["error_codes"])

    def test_06_unicode_nfc_and_exact_offsets(self):
        decomposed = unicodedata.normalize("NFD", "È " + CLAIM)
        result = spatial.validate_spatial_v2(witness(), decomposed, EVIDENCE)
        self.assertEqual(result["error_codes"], ["E_TEXT_NOT_NFC"])
        invalid = witness(); invalid["claim_relation"]["subject"]["anchors"][0]["end"] += 1
        self.assertIn("E_ANCHOR_INVALID", spatial.validate_spatial_v2(invalid, CLAIM, EVIDENCE)["error_codes"])

    def test_07_duplicate_anchor_rejected_overlap_allowed(self):
        duplicate = witness()
        first = duplicate["claim_relation"]["value"]["anchors"][0]
        duplicate["claim_relation"]["value"]["anchors"].append(copy.deepcopy(first))
        self.assertIn("E_ANCHOR_ORDER_OR_DUPLICATE", spatial.validate_spatial_v2(duplicate, CLAIM, EVIDENCE)["error_codes"])
        overlap = witness()
        overlap["claim_relation"]["value"]["anchors"].append(anchor("claim", CLAIM, "spazio"))
        overlap["claim_relation"]["value"]["anchors"].sort(key=lambda row: (row["start"], row["end"], row["exact_span"]))
        self.assertEqual(spatial.validate_spatial_v2(overlap, CLAIM, EVIDENCE)["technical_status"], "valid")

    def test_08_conditions_and_phase_are_deterministic(self):
        invalid = witness()
        invalid["claim_relation"]["conditions"] = {"status": "explicit", "items": []}
        self.assertIn("E_STATUS_VALUE_INCONSISTENT", spatial.validate_spatial_v2(invalid, CLAIM, EVIDENCE)["error_codes"])
        phase = witness("insufficient")
        phase["evidence_relation"]["phase"] = {"status": "explicit", "value": "defense",
                                                "anchors": [anchor("evidence", EVIDENCE, "difendono")]}
        phase["comparison"]["phase"] = "different"
        self.assertEqual(spatial.validate_spatial_v2(phase, CLAIM, EVIDENCE)["derived_label"], "insufficient")

    def test_09_quantifier_strength_and_numeric_literal(self):
        claim = "Alcune squadre lasciano spazio tra linea e porta."
        evidence = "Tutte le squadre lasciano spazio tra linea e porta."
        value = witness("supported")
        # Re-anchor all text-dependent fields by using the original relation helper.
        value["claim_relation"] = relation("claim", claim, subject_id="entity:teams", subject_span="squadre",
                                             reference_id="entity:line-goal-space", reference_span="tra linea e porta",
                                             value="abundant", value_span="spazio")
        value["evidence_relation"] = relation("evidence", evidence, subject_id="entity:teams", subject_span="squadre",
                                                reference_id="entity:line-goal-space", reference_span="tra linea e porta",
                                                value="abundant", value_span="spazio")
        value["claim_relation"]["quantifier"] = {"status": "explicit", "value": "some", "literal": None,
                                                    "anchors": [anchor("claim", claim, "Alcune")]}
        value["evidence_relation"]["quantifier"] = {"status": "explicit", "value": "all", "literal": None,
                                                       "anchors": [anchor("evidence", evidence, "Tutte")]}
        value["comparison"].update(subject="same", value="same", quantifier="compatible")
        self.assertEqual(spatial.validate_spatial_v2(value, claim, evidence)["derived_label"], "supported")
        value["claim_relation"]["quantifier"] = {"status": "explicit", "value": "numeric", "literal": None,
                                                    "anchors": [anchor("claim", claim, "Alcune")]}
        self.assertIn("E_STATUS_VALUE_INCONSISTENT", spatial.validate_spatial_v2(value, claim, evidence)["error_codes"])

    def test_10_polarity_and_comparison_incoherence(self):
        value = witness()
        value["comparison"]["value"] = "same"
        result = spatial.validate_spatial_v2(value, CLAIM, EVIDENCE)
        self.assertIn("E_COMPARISON_INCONSISTENT", result["error_codes"])

        evidence = "Le squadre che difendono basse non lasciano molto spazio tra linea e porta."
        negated = witness("contradicted")
        negated["evidence_relation"] = relation(
            "evidence", evidence, subject_id="entity:defending-low",
            subject_span="squadre che difendono basse", reference_id="entity:line-goal-space",
            reference_span="tra linea e porta", value="abundant", value_span="molto spazio")
        negated["evidence_relation"]["polarity"] = {
            "status": "explicit", "value": "negated",
            "anchors": [anchor("evidence", evidence, "non")],
        }
        negated["comparison"].update(value="same", polarity="incompatible")
        self.assertEqual(spatial.validate_spatial_v2(negated, CLAIM, evidence)["derived_label"], "contradicted")

        different_axis = witness("insufficient")
        different_axis["evidence_relation"]["semantic_axis"]["value"] = "area_extent"
        different_axis["evidence_relation"]["value"]["value"] = "contracting"
        different_axis["comparison"].update(semantic_axis="different", value="incompatible")
        self.assertIn("E_COMPARISON_INCONSISTENT",
                      spatial.validate_spatial_v2(different_axis, CLAIM, EVIDENCE)["error_codes"])

    def test_10b_value_incompatibility_comes_only_from_normative_matrix(self):
        # The baseline incorrectly accepted incompatible for both neutral pairs.
        for left, right in (("abundant", "neutral"), ("scarce", "neutral")):
            value = witness("contradicted")
            value["claim_relation"]["value"]["value"] = left
            value["evidence_relation"]["value"]["value"] = right
            value["comparison"]["value"] = "incompatible"
            with self.subTest(left=left, right=right):
                result = spatial.validate_spatial_v2(value, CLAIM, EVIDENCE)
                self.assertEqual(result["technical_status"], "not_evaluable")
                self.assertIn("E_COMPARISON_INCONSISTENT", result["error_codes"])

        normative = witness("contradicted")
        self.assertEqual(spatial.validate_spatial_v2(normative, CLAIM, EVIDENCE)["derived_label"], "contradicted")
        same = witness("supported")
        same["evidence_relation"]["value"]["value"] = "abundant"
        same["comparison"]["value"] = "same"
        self.assertEqual(spatial.validate_spatial_v2(same, CLAIM, EVIDENCE)["derived_label"], "supported")

    def test_11_label_mismatch_is_not_corrected(self):
        result = spatial.validate_spatial_v2(witness("supported"), CLAIM, EVIDENCE)
        self.assertEqual(result["technical_status"], "not_evaluable")
        self.assertEqual(result["derived_label"], "contradicted")
        self.assertEqual(result["model_label"], "supported")
        self.assertIn("E_LABEL_WITNESS_MISMATCH", result["error_codes"])

    def test_12_valid_insufficient_and_supported(self):
        insufficient = witness("insufficient")
        insufficient["evidence_relation"]["value"] = {"status": "absent", "value": "absent", "anchors": []}
        insufficient["comparison"]["value"] = "unknown"
        self.assertEqual(spatial.validate_spatial_v2(insufficient, CLAIM, EVIDENCE)["technical_status"], "valid")
        supported = witness("supported")
        supported["evidence_relation"]["value"]["value"] = "abundant"
        supported["comparison"]["value"] = "same"
        self.assertEqual(spatial.validate_spatial_v2(supported, CLAIM, EVIDENCE)["derived_label"], "supported")


class SpatialV2JudgeTests(unittest.TestCase):
    def test_13_import_is_inert_and_descriptor_is_opt_in(self):
        module = importlib.reload(judge)
        self.assertEqual(module.descriptor()["selection"], "explicit_import_only")
        self.assertFalse(module.descriptor()["retry"])
        self.assertFalse(module.descriptor()["repair"])
        self.assertFalse(module.descriptor()["fallback"])

    def test_14_exactly_one_mock_transport_call(self):
        calls = []
        def transport(url, payload, timeout):
            calls.append((url, payload, timeout))
            return {"done_reason": "stop", "message": {"content": json.dumps(witness())}}
        result = judge.judge_pair(CLAIM, EVIDENCE, transport=transport)
        self.assertEqual(len(calls), 1)
        self.assertEqual(result["evaluation_status"], "evaluated")
        self.assertFalse(result["promotion_authorized"])
        self.assertEqual(calls[0][1]["format"]["$id"], spatial.SPATIAL_V2_SCHEMA["$id"])

    def test_15_invalid_witness_is_not_evaluable_without_retry(self):
        calls = []
        def transport(_url, _payload, _timeout):
            calls.append(True)
            return {"done_reason": "stop", "message": {"content": json.dumps({"label": "supported"})}}
        result = judge.judge_pair(CLAIM, EVIDENCE, transport=transport)
        self.assertEqual(len(calls), 1)
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        self.assertIsNone(result["label"])
        self.assertFalse(result["promotion_authorized"])

    def test_16_operational_errors_are_structured_without_retry(self):
        cases = [
            (lambda *_: (_ for _ in ()).throw(TimeoutError("offline mock")), "E_JUDGE_TIMEOUT"),
            (lambda *_: (_ for _ in ()).throw(ConnectionError("offline mock")), "E_JUDGE_TRANSPORT"),
            (lambda *_: {"done_reason": "length", "message": {"content": "{}"}}, "E_JUDGE_RESPONSE_INCOMPLETE"),
            (lambda *_: {"done_reason": "stop", "message": {}}, "E_JUDGE_RESPONSE_MISSING"),
            (lambda *_: {"done_reason": "stop", "message": {"content": "not-json"}}, "E_JUDGE_JSON_INVALID"),
        ]
        for operation, code in cases:
            calls = []
            def transport(*args, operation=operation):
                calls.append(args)
                return operation(*args)
            with self.subTest(code=code):
                result = judge.judge_pair(CLAIM, EVIDENCE, transport=transport)
                self.assertEqual(len(calls), 1)
                self.assertEqual(result["evaluation_status"], "not_evaluable")
                self.assertIsNone(result["label"])
                self.assertFalse(result["promotion_authorized"])
                self.assertEqual(result["validation"]["error_codes"], [code])

    def test_17_programming_errors_remain_exceptions(self):
        def programming_error(*_args):
            raise TypeError("bad injected transport implementation")
        with self.assertRaises(TypeError):
            judge.judge_pair(CLAIM, EVIDENCE, transport=programming_error)


if __name__ == "__main__":
    unittest.main()
