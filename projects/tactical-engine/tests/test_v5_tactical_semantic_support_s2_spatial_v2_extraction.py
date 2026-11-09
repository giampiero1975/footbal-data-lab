import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import shadow_nli_spatial_relations_v2_inference as judge
import v5_tactical_semantic_support_s2_spatial_v2 as spatial
import v5_tactical_semantic_support_s2_spatial_v2_extraction as extraction


CLAIM = "La difesa bassa lascia molto spazio tra linea e porta."
EVIDENCE = "Le squadre che difendono basse tolgono spazio tra linea e porta."


def fragment_slot(status, value, *fragments):
    return {"status": status, "value": value,
            "selected_fragments": list(fragments)}


def relation(subject_id, subject, reference_id, reference, value, value_span):
    return {
        "subject": {"status": "explicit", "entity_id": subject_id,
                    "selected_fragments": [subject]},
        "semantic_axis": fragment_slot(
            "explicit", "space_availability", "spazio"),
        "reference": {"status": "explicit", "entity_id": reference_id,
                      "selected_fragments": [reference]},
        "value": fragment_slot("explicit", value, value_span),
        "conditions": {"status": "absent", "items": []},
        "phase": fragment_slot("implicit", "general"),
        "quantifier": {"status": "implicit", "value": "none",
                       "literal": None, "selected_fragments": []},
        "polarity": fragment_slot("implicit", "affirmed"),
    }


def valid_extraction(label="contradicted"):
    return {
        "contract_id": extraction.CONTRACT_ID,
        "contract_version": extraction.CONTRACT_VERSION,
        "label": label,
        "claim_relation": relation(
            "entity:low-block", "difesa bassa", "entity:line-goal-space",
            "tra linea e porta", "abundant", "molto spazio"),
        "evidence_relation": relation(
            "entity:defending-low", "squadre che difendono basse",
            "entity:line-goal-space", "tra linea e porta", "scarce",
            "tolgono spazio"),
        "comparison": {
            "subject": "compatible", "semantic_axis": "same",
            "reference": "same", "value": "incompatible",
            "conditions": "same", "phase": "same", "quantifier": "same",
            "polarity": "same",
        },
    }


def response(value):
    return {"done_reason": "stop", "message": {
        "content": json.dumps(value, ensure_ascii=False)}}


class SpatialV2ExtractionLocatorTests(unittest.TestCase):
    def test_01_unique_fragments_materialize_and_validate(self):
        result = extraction.materialize_extraction(
            valid_extraction(), CLAIM, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "evaluated")
        self.assertEqual(result["validation"]["technical_status"], "valid")
        self.assertFalse(result["promotion_authorized"])
        anchors = result["witness"]["claim_relation"]["subject"]["anchors"]
        self.assertEqual(anchors, [{
            "source": "claim", "start": CLAIM.index("difesa bassa"),
            "end": CLAIM.index("difesa bassa") + len("difesa bassa"),
            "exact_span": "difesa bassa",
        }])
        self.assertEqual(
            extraction.verify_materialization(
                result, valid_extraction(), CLAIM, EVIDENCE), [])

    def test_02_missing_fragment_is_not_evaluable(self):
        value = valid_extraction()
        value["claim_relation"]["subject"]["selected_fragments"] = ["assente"]
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        self.assertIsNone(result["witness"])
        self.assertEqual(result["localization"]["records"][0]["result"], "missing")

    def test_03_repeated_fragment_is_not_evaluable_without_first_match(self):
        repeated = CLAIM.replace("spazio", "spazio spazio")
        result = extraction.materialize_extraction(
            valid_extraction(), repeated, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        records = result["localization"]["records"]
        spatial_axis = next(row for row in records if
                            row["field_id"] ==
                            "claim_relation.semantic_axis.selected_fragments[0]")
        self.assertEqual(spatial_axis["occurrence_count"], 2)
        self.assertEqual(spatial_axis["result"], "ambiguous")
        self.assertIsNone(spatial_axis["start"])

    def test_04_opposite_side_fragment_is_not_evaluable(self):
        value = valid_extraction()
        value["claim_relation"]["subject"]["selected_fragments"] = [
            "squadre che difendono basse"]
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        row = result["localization"]["records"][0]
        self.assertEqual(row["side"], "claim")
        self.assertEqual(row["occurrence_count"], 0)
        self.assertEqual(row["result"], "missing")

    def test_05_valid_fragment_does_not_repair_status_value(self):
        value = valid_extraction()
        value["claim_relation"]["polarity"] = fragment_slot(
            "explicit", "affirmed", "lascia")
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        self.assertIsNotNone(result["witness"])
        self.assertIn("E_STATUS_VALUE_INCONSISTENT", result["reason_codes"])

    def test_06_valid_fragment_does_not_repair_label_comparison(self):
        result = extraction.materialize_extraction(
            valid_extraction("supported"), CLAIM, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        self.assertIn("E_LABEL_WITNESS_MISMATCH", result["reason_codes"])

    def test_07_unicode_and_punctuation_use_literal_code_points(self):
        claim = CLAIM.replace("difesa", "difésa")
        value = valid_extraction()
        value["claim_relation"]["subject"]["selected_fragments"] = [
            "difésa bassa"]
        result = extraction.materialize_extraction(value, claim, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "evaluated")
        anchor = result["witness"]["claim_relation"]["subject"]["anchors"][0]
        self.assertEqual(claim[anchor["start"]:anchor["end"]], "difésa bassa")

    def test_08_default_path_keeps_legacy_schema_and_result(self):
        calls = []

        def transport(url, payload, timeout):
            calls.append((url, payload, timeout))
            materialized = extraction.materialize_extraction(
                valid_extraction(), CLAIM, EVIDENCE)
            return response(materialized["witness"])

        result = judge.judge_pair(CLAIM, EVIDENCE, transport=transport)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1]["format"], spatial.SPATIAL_V2_SCHEMA)
        self.assertIn(judge.INSTRUCTION, calls[0][1]["messages"][1]["content"])
        self.assertEqual(result["evaluation_status"], "evaluated")
        self.assertNotIn("localization", result)

    def test_09_altered_provenance_fails_verification(self):
        value = valid_extraction()
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        altered = copy.deepcopy(result)
        altered["localization"]["source_text_sha256"]["claim"] = "sha256:" + "0" * 64
        self.assertEqual(extraction.verify_materialization(
            altered, value, CLAIM, EVIDENCE),
            ["E_EXTRACTION_PROVENANCE_MISMATCH"])

    def test_10_extraction_schema_has_no_model_generated_location_fields(self):
        forbidden = {"source", "start", "end", "anchors", "exact_span"}

        def keys(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    yield key
                    yield from keys(item)
            elif isinstance(value, list):
                for item in value:
                    yield from keys(item)

        self.assertFalse(forbidden.intersection(keys(extraction.EXTRACTION_SCHEMA)))
        self.assertIn("selected_fragments", set(keys(extraction.EXTRACTION_SCHEMA)))

    def test_11_opt_in_mock_uses_extraction_once_without_repair(self):
        calls = []

        def transport(url, payload, timeout):
            calls.append((url, payload, timeout))
            return response(valid_extraction())

        result = judge.judge_pair(
            CLAIM, EVIDENCE, transport=transport, extraction_locator=True)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1]["format"], extraction.EXTRACTION_SCHEMA)
        prompt = calls[0][1]["messages"][1]["content"]
        self.assertNotIn(" start ", prompt)
        self.assertIn("reference e il referente spaziale", prompt)
        self.assertIn("space_availability={abundant,scarce,neutral}", prompt)
        self.assertIn("claim_relation descrive esclusivamente l'AFFERMAZIONE", prompt)
        self.assertIn("evidence_relation descrive esclusivamente la FONTE", prompt)
        self.assertIn("supported richiede", prompt)
        self.assertEqual(result["evaluation_status"], "evaluated")
        descriptor = judge.extraction_descriptor()
        self.assertTrue(descriptor["single_generation"])
        self.assertFalse(descriptor["retry"])
        self.assertFalse(descriptor["repair"])
        self.assertFalse(descriptor["fallback"])

    def test_12_parse_shape_and_transport_errors_fail_closed(self):
        cases = [
            lambda url, payload, timeout: {
                "done_reason": "stop", "message": {"content": "{"}},
            lambda url, payload, timeout: response({"wrong": True}),
        ]
        for transport in cases:
            with self.subTest(transport=transport):
                result = judge.judge_pair(
                    CLAIM, EVIDENCE, transport=transport,
                    extraction_locator=True)
                self.assertEqual(result["evaluation_status"], "not_evaluable")
                self.assertIsNone(result["witness"])
                self.assertFalse(result["promotion_authorized"])

    def test_13_axis_value_mismatch_stops_before_locator(self):
        value = valid_extraction()
        value["claim_relation"]["value"]["value"] = "between"
        value["claim_relation"]["reference"]["selected_fragments"] = [
            "frammento del lato opposto"]
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        self.assertEqual(result["reason_codes"], [
            "E_EXTRACTION_SEMANTIC_INCONSISTENT"])
        self.assertIn("E_EXTRACTION_AXIS_VALUE_INCOMPATIBLE",
                      {item["code"] for item in result["details"]})
        self.assertEqual(result["localization"]["records"], [])
        self.assertIsNone(result["witness"])
        self.assertFalse(result["promotion_authorized"])

    def test_14_same_comparison_rejects_incompatible_quantifiers(self):
        value = valid_extraction()
        value["claim_relation"]["quantifier"].update(
            {"status": "explicit", "value": "many", "literal": None,
             "selected_fragments": ["molto"]})
        value["evidence_relation"]["quantifier"].update(
            {"status": "explicit", "value": "some", "literal": None,
             "selected_fragments": ["squadre"]})
        value["comparison"]["quantifier"] = "same"
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        self.assertIn("E_EXTRACTION_COMPARISON_INCONSISTENT",
                      {item["code"] for item in result["details"]})
        self.assertEqual(result["localization"]["records"], [])
        self.assertFalse(result["promotion_authorized"])

    def test_15_runtime_03_extraction_replay_fails_semantic_precheck(self):
        value = valid_extraction("supported")
        for side in ("claim_relation", "evidence_relation"):
            value[side]["value"]["value"] = "between"
        value["claim_relation"]["reference"]["selected_fragments"] = [
            "squadre che difendono basse"]
        value["claim_relation"]["subject"]["entity_id"] = "entity:s1"
        value["evidence_relation"]["subject"]["entity_id"] = "entity:s2"
        value["claim_relation"]["reference"]["entity_id"] = "entity:r1"
        value["evidence_relation"]["reference"]["entity_id"] = "entity:r2"
        value["claim_relation"]["conditions"] = {
            "status": "explicit", "items": [{
                "condition_id": "condition:c1", "status": "explicit",
                "selected_fragments": ["difesa bassa"],
            }]}
        value["evidence_relation"]["conditions"] = {
            "status": "explicit", "items": [{
                "condition_id": "condition:c2", "status": "explicit",
                "selected_fragments": ["difendono basse"],
            }]}
        value["claim_relation"]["quantifier"].update(
            {"status": "explicit", "value": "many", "literal": None,
             "selected_fragments": ["molto"]})
        value["evidence_relation"]["quantifier"].update(
            {"status": "explicit", "value": "some", "literal": None,
             "selected_fragments": ["squadre"]})
        value["comparison"].update({
            "subject": "same", "reference": "same", "value": "same",
            "conditions": "same", "quantifier": "same"})
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        codes = {item["code"] for item in result["details"]}
        self.assertEqual(result["reason_codes"], [
            "E_EXTRACTION_SEMANTIC_INCONSISTENT"])
        self.assertIn("E_EXTRACTION_AXIS_VALUE_INCOMPATIBLE", codes)
        self.assertIn("E_EXTRACTION_COMPARISON_INCONSISTENT", codes)
        self.assertEqual(result["localization"]["records"], [])
        self.assertIsNone(result["witness"])

    def test_16_different_referents_are_insufficient_not_contradicted(self):
        value = valid_extraction("insufficient")
        value["evidence_relation"]["reference"]["entity_id"] = (
            "entity:different-space")
        value["comparison"]["reference"] = "different"
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "evaluated")
        self.assertEqual(result["validation"]["derived_label"], "insufficient")
        self.assertNotEqual(result["validation"]["derived_label"], "contradicted")
        self.assertFalse(result["promotion_authorized"])


if __name__ == "__main__":
    unittest.main()
