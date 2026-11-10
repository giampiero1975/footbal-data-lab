"""New delta only: correlated status/content handoff after immutable runtime-04.

Recorded before execution: old 37/37 and wrapper 13 tests are not invoked.
New cases cover status branches, schema/shape correspondence, real runtime-04
rejection before localization, normative mock payload and frozen legacy parity.
The schema checker below interprets only the transport subset: it is NOT a
complete JSON Schema validator or a test of the deployed backend compiler.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import socket
import subprocess
import sys
import types
import unittest
from unittest import mock

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "scripts"))
import shadow_nli_spatial_relations_v2_inference as judge
import v5_tactical_semantic_support_s2_spatial_v2_extraction as extraction
import v5_tactical_semantic_support_s2_spatial_v2 as spatial

FROZEN = "8fca97fdf596d00f14987c5527694056d382e802"
CLAIM = "Il reparto offre ampiezza abbondante nel corridoio."
EVIDENCE = "Il reparto offre ampiezza ridotta nel corridoio."


def slot(status, value, *fragments):
    return {"status": status, "value": value, "selected_fragments": list(fragments)}


def relation(value, fragment):
    return {
        "subject": {"status": "explicit", "entity_id": "entity:unit",
                    "selected_fragments": ["Il reparto"]},
        "reference": {"status": "explicit", "entity_id": "entity:lane",
                      "selected_fragments": ["nel corridoio"]},
        "semantic_axis": slot("explicit", "space_availability", "ampiezza"),
        "value": slot("explicit", value, fragment),
        "conditions": {"status": "absent", "items": []},
        "phase": slot("implicit", "general"),
        "quantifier": {**slot("implicit", "none"), "literal": None},
        "polarity": slot("implicit", "affirmed"),
    }


def frame():
    return {"contract_id": extraction.CONTRACT_ID,
            "contract_version": extraction.CONTRACT_VERSION, "label": "contradicted",
            "claim_relation": relation("abundant", "abbondante"),
            "evidence_relation": relation("scarce", "ridotta"),
            "comparison": {key: "incompatible" if key == "value" else "same"
                           for key in spatial.COMPARISON_KEYS}}


def uncertain():
    value = frame(); value["label"] = "insufficient"
    for side in ("claim_relation", "evidence_relation"):
        for name in ("subject", "reference"):
            value[side][name] = {"status": "unknown", "entity_id": "entity:unknown",
                                 "selected_fragments": []}
        for name in ("semantic_axis", "value", "phase", "polarity"):
            value[side][name] = slot("unknown", "unknown")
        value[side]["quantifier"] = {**slot("unknown", "unknown"), "literal": None}
        value[side]["conditions"] = {"status": "unknown", "items": []}
    value["comparison"] = dict.fromkeys(spatial.COMPARISON_KEYS, "unknown")
    return value


def schema_accepts(schema, value, root=None):
    """Independent, domain-free interpreter for the explicitly used subset."""
    root = schema if root is None else root
    if "$ref" in schema:
        target = root
        for part in schema["$ref"][2:].split("/"):
            target = target[part]
        return schema_accepts(target, value, root)
    if "anyOf" in schema:
        return any(schema_accepts(branch, value, root) for branch in schema["anyOf"])
    if "const" in schema and value != schema["const"]:
        return False
    if "enum" in schema and value not in schema["enum"]:
        return False
    kind = schema.get("type")
    if kind == "null": return value is None
    if kind == "string":
        return (isinstance(value, str) and len(value) >= schema.get("minLength", 0)
                and len(value) <= schema.get("maxLength", float("inf"))
                and ("pattern" not in schema or re.search(schema["pattern"], value) is not None))
    if kind == "array":
        return (isinstance(value, list) and len(value) >= schema.get("minItems", 0)
                and len(value) <= schema.get("maxItems", float("inf"))
                and (not schema.get("uniqueItems") or len({json.dumps(x, sort_keys=True) for x in value}) == len(value))
                and all(schema_accepts(schema["items"], x, root) for x in value))
    if kind == "object":
        properties = schema["properties"]
        return (isinstance(value, dict) and set(schema.get("required", [])).issubset(value)
                and (schema.get("additionalProperties") is not False or set(value).issubset(properties))
                and all(schema_accepts(properties[k], v, root) for k, v in value.items() if k in properties))
    return True


class StatusContractDeltaTests(unittest.TestCase):
    def assert_rejected_without_mutation(self, value, *, claim=CLAIM, evidence=EVIDENCE):
        original = copy.deepcopy(value)
        with mock.patch.object(extraction, "_localize_fragments", side_effect=AssertionError("locator must not run")):
            result = extraction.materialize_extraction(value, claim, evidence)
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        self.assertFalse(result["promotion_authorized"])
        self.assertIsNone(result["witness"])
        self.assertIsNone(result["validation"])
        self.assertEqual(result["localization"]["records"], [])
        self.assertEqual(value, original)
        return result

    def test_unknown_legitimate_preserved_without_inventing_concrete_values(self):
        value = uncertain(); original = copy.deepcopy(value)
        self.assertEqual(extraction.extraction_shape_errors(value), [])
        self.assertEqual(extraction.extraction_semantic_errors(value), [])
        self.assertTrue(schema_accepts(extraction.EXTRACTION_SCHEMA, value))
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        self.assertFalse(result["promotion_authorized"])
        self.assertEqual(result["evaluation_status"], "not_evaluable")
        self.assertEqual(value, original)

    def test_legitimate_unknown_phase_can_remain_insufficient(self):
        value = frame(); value["label"] = "insufficient"
        for side in ("claim_relation", "evidence_relation"):
            value[side]["phase"] = slot("unknown", "unknown")
        value["comparison"]["phase"] = "unknown"
        # Unknown phase has precedence over the otherwise incompatible values.
        self.assertTrue(schema_accepts(extraction.EXTRACTION_SCHEMA, value))
        result = extraction.materialize_extraction(value, CLAIM, EVIDENCE)
        self.assertEqual(result["evaluation_status"], "evaluated")
        self.assertEqual(result["validation"]["derived_label"], "insufficient")
        self.assertFalse(result["promotion_authorized"])

    def test_unknown_concrete_id_value_or_fragments_rejected(self):
        for field, change in (("subject", {"entity_id": "entity:unit"}),
                              ("value", {"value": "abundant"}),
                              ("reference", {"selected_fragments": ["nel corridoio"]})):
            with self.subTest(field=field):
                value = uncertain(); value["claim_relation"][field].update(change)
                self.assertFalse(schema_accepts(extraction.EXTRACTION_SCHEMA, value))
                result = self.assert_rejected_without_mutation(value)
                self.assertEqual(result["reason_codes"], ["E_EXTRACTION_SCHEMA_INVALID"])
                self.assertIn("E_EXTRACTION_STATUS_CONTENT_INCONSISTENT", [r["code"] for r in result["details"]])

    def test_unknown_precedes_identical_ids_and_values_comparison(self):
        value = uncertain(); value["comparison"] = dict.fromkeys(spatial.COMPARISON_KEYS, "same")
        self.assertEqual(extraction.extraction_shape_errors(value), [])
        result = self.assert_rejected_without_mutation(value)
        self.assertEqual(result["reason_codes"], ["E_EXTRACTION_SEMANTIC_INCONSISTENT"])
        self.assertEqual(result["details"], [{"code": "E_EXTRACTION_COMPARISON_INCONSISTENT", "path": "comparison"}])

    def test_conditions_container_and_item_status_are_distinct(self):
        item = {"condition_id": "condition:lane", "status": "ambiguous",
                "selected_fragments": ["nel corridoio"]}
        for status in ("explicit", "ambiguous"):
            value = frame()
            value["claim_relation"]["conditions"] = {"status": status, "items": [item]}
            self.assertEqual(extraction.extraction_shape_errors(value), [])
            self.assertTrue(schema_accepts(extraction.EXTRACTION_SCHEMA, value))
            expected = {"same"} if status == "explicit" else {"ambiguous"}
            self.assertEqual(spatial._expected_comparison("conditions", value["claim_relation"]["conditions"],
                                                        value["claim_relation"]["conditions"]), expected)
        value = frame(); value["claim_relation"]["conditions"] = {"status": "unknown", "items": [item]}
        self.assertFalse(schema_accepts(extraction.EXTRACTION_SCHEMA, value))
        self.assert_rejected_without_mutation(value)

    def test_conditions_residual_constraints_are_deterministic(self):
        # contains/unique IDs are not delegated to a grammar with uncertain support.
        for mode in ("no_ambiguous_child", "duplicate_ids", "bad_prefix"):
            with self.subTest(mode=mode):
                value = frame(); item = {"condition_id": "condition:lane", "status": "explicit",
                                         "selected_fragments": ["nel corridoio"]}
                items = [item]; status = "ambiguous" if mode == "no_ambiguous_child" else "explicit"
                if mode == "duplicate_ids": items = [item, copy.deepcopy(item)]
                if mode == "bad_prefix": item["condition_id"] = "not-a-condition-id"
                value["claim_relation"]["conditions"] = {"status": status, "items": items}
                self.assertTrue(schema_accepts(extraction.EXTRACTION_SCHEMA, value))
                self.assert_rejected_without_mutation(value)

    def test_state_family_branches_match_final_rules_without_locator_changes(self):
        cases = [("phase", slot("implicit", "general"), True),
                 ("phase", slot("implicit", "unknown"), False),
                 ("polarity", slot("implicit", "affirmed"), True),
                 ("polarity", slot("unknown", "affirmed"), False),
                 ("semantic_axis", slot("implicit", "space_availability"), False),
                 ("value", slot("absent", "absent"), False)]
        for field, payload, valid in cases:
            with self.subTest(field=field, payload=payload):
                value = frame(); value["claim_relation"][field] = payload
                self.assertEqual(not extraction.extraction_shape_errors(value), valid)
        value = frame(); value["evidence_relation"]["value"] = slot("absent", "absent")
        self.assertEqual(extraction.extraction_shape_errors(value), [])

    def test_quantifier_literal_and_implicit_sentinel_are_correlated(self):
        for literal, good in ((None, False), ("", False), ("2", True)):
            value = frame(); value["claim_relation"]["quantifier"] = {**slot("explicit", "numeric", "Il reparto"), "literal": literal}
            self.assertEqual(schema_accepts(extraction.EXTRACTION_SCHEMA, value), good)
            self.assertEqual(not extraction.extraction_shape_errors(value), good)
        value = frame(); value["claim_relation"]["quantifier"]["literal"] = "2"
        self.assert_rejected_without_mutation(value)

    def test_mock_payload_contains_normative_rules_without_gold_or_cross_side_rewrite(self):
        calls = []
        def transport(url, payload, timeout):
            calls.append((url, copy.deepcopy(payload), timeout))
            return {"done_reason": "stop", "message": {"content": json.dumps(uncertain())}}
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            judge.judge_pair(CLAIM, EVIDENCE, extraction_locator=True, transport=transport)
        self.assertEqual(len(calls), 1)
        payload = calls[0][1]; prompt = payload["messages"][1]["content"]
        self.assertEqual(payload["format"], extraction.EXTRACTION_SCHEMA)
        self.assertIn("precedenza degli stati su ID e valori", prompt)
        for text in ("entity:unknown", "items=[]", "implicit usa general", "literal=null",
                     "compatible resta una dichiarazione shadow", "abundant", "scarce",
                     "Non normalizzare o riscrivere", "Grounding separato"):
            self.assertIn(text, prompt)
        self.assertNotIn("q3_04", prompt)
        self.assertNotIn("gold_label", prompt)
        self.assertTrue(prompt.endswith("\n\nFONTE:\n" + EVIDENCE + "\n\nAFFERMAZIONE:\n" + CLAIM))
        self.assertEqual(payload["options"], {"temperature": 0, "num_predict": 2048, "num_ctx": 4096})
        self.assertFalse(payload["think"])

    def test_frozen_legacy_payload_result_and_functions_are_identical(self):
        source = subprocess.check_output(["git", "show", FROZEN + ":projects/tactical-engine/scripts/shadow_nli_spatial_relations_v2_inference.py"]).decode()
        old = types.ModuleType("frozen_legacy_judge")
        exec(compile(source, "<frozen-legacy>", "exec"), old.__dict__)
        witness = extraction.materialize_extraction(frame(), CLAIM, EVIDENCE)["witness"]
        payloads = []
        def transport(url, payload, timeout):
            payloads.append((url, payload, timeout))
            return {"done_reason": "stop", "message": {"content": json.dumps(witness)}}
        a = old.judge_pair(CLAIM, EVIDENCE, transport=transport)
        b = judge.judge_pair(CLAIM, EVIDENCE, transport=transport)
        self.assertEqual(payloads[0], payloads[1]); self.assertEqual(a, b)
        self.assertEqual(old.INSTRUCTION, judge.INSTRUCTION)
        def functions(text):
            return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(text).body if isinstance(n, ast.FunctionDef)}
        old_functions = functions(source); new_functions = functions(Path(judge.__file__).read_text())
        self.assertEqual(old_functions, new_functions)

    def test_runtime04_replay_originals_immutable_and_earlier_fail_closed(self):
        root = PROJECT / "evaluation/runtime04_execution_01"
        metadata = json.loads((root / "metadata/collection-verification.json").read_bytes())
        before = {name: hashlib.sha256((root / "artifacts" / name).read_bytes()).hexdigest()
                  for name in metadata["files"]}
        self.assertEqual(before, {name: v["sha256"] for name, v in metadata["files"].items()})
        raw = json.loads((root / "artifacts/raw_response.json").read_bytes())
        value = json.loads(raw["message"]["content"])
        self.assertEqual(value, json.loads((root / "artifacts/extraction.json").read_bytes()))
        self.assertFalse(schema_accepts(extraction.EXTRACTION_SCHEMA, value))
        original_input = json.loads((root / "artifacts/input.json").read_bytes())
        result = self.assert_rejected_without_mutation(
            value, claim=original_input["claim"], evidence=original_input["evidence"])
        self.assertEqual(result["reason_codes"], ["E_EXTRACTION_SCHEMA_INVALID"])
        self.assertEqual(value["label"], "supported")
        self.assertEqual({name: hashlib.sha256((root / "artifacts" / name).read_bytes()).hexdigest()
                          for name in metadata["files"]}, before)

    def test_schema_subset_is_finite_serializable_and_reference_safe(self):
        schema = json.loads(json.dumps(extraction.EXTRACTION_SCHEMA))
        forbidden = {"if", "then", "else", "not", "contains", "dependentSchemas", "allOf", "default"}
        def visit(node):
            if isinstance(node, dict):
                self.assertFalse(forbidden.intersection(node))
                if "anyOf" in node:
                    self.assertNotIn("properties", node)
                    self.assertTrue(node["anyOf"])
                if "$ref" in node:
                    self.assertTrue(node["$ref"].startswith("#/$defs/"))
                for child in node.values(): visit(child)
            elif isinstance(node, list):
                for child in node: visit(child)
        visit(schema)
        self.assertTrue(schema_accepts(schema, frame()))
        self.assertTrue(schema_accepts(schema, uncertain()))

    def test_normative_matrix_is_versioned_and_explicit_about_axis_identity(self):
        # New post-review coverage: no rerun of the other twelve unaffected tests.
        prompt = extraction.extraction_handoff_instructions()
        self.assertIn("semantic_axis con valore uguale richiede same, con valore diverso different", prompt)
        self.assertEqual(prompt, judge.EXTRACTION_INSTRUCTION)
        for axis, pairs in spatial.INCOMPATIBLE_VALUES.items():
            self.assertIn(json.dumps(axis), prompt)
            for pair in pairs:
                self.assertIn(json.dumps(sorted(pair)), prompt)

    def test_no_duplicate_definitions_or_correlation_passes(self):
        # Review correction: source duplicates removed; rerun only this new suite.
        source = (PROJECT / "scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py").read_text()
        tree = ast.parse(source)
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
        self.assertEqual(len(functions), len({n.name for n in functions}))
        shape = next(n for n in functions if n.name == "extraction_shape_errors")
        calls = [n for n in ast.walk(shape) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id == "_representation_errors"]
        self.assertEqual(len(calls), 1)

    def test_new_representation_checks_match_final_slot_predicates(self):
        # New independent oracle for the delta: bounded status/content combinations,
        # real literal anchors, final predicates unchanged; no historical suite run.
        def projected(payload, side):
            output = {k: copy.deepcopy(v) for k, v in payload.items() if k != "selected_fragments"}
            fragments = payload["selected_fragments"]
            text = " ".join(fragments)
            output["anchors"] = [{"source": side, "start": text.index(f),
                                  "end": text.index(f) + len(f), "exact_span": f}
                                 for f in fragments]
            return output, text
        cases = 0
        for side in ("claim_relation", "evidence_relation"):
            origin = "claim" if side == "claim_relation" else "evidence"
            for status in sorted(spatial.STATUSES):
                for count in (0, 1, 4):
                    fragments = ["p" + str(i) for i in range(count)]
                    for identity in ("entity:unit", "entity:unknown", "entity:ambiguous",
                                     "entity:absent", "entity:äx", "bad"):
                        payload = {"status": status, "entity_id": identity, "selected_fragments": fragments}
                        value = frame(); value[side]["subject"] = payload
                        final, text = projected(payload, origin)
                        expected = not spatial._entity_errors(final, origin, text, side == "claim_relation")
                        self.assertEqual(not extraction.extraction_shape_errors(value), expected,
                                         (side, status, count, identity))
                        cases += 1
                samples = {"semantic_axis": ["space_availability", "unknown", "ambiguous", "absent"],
                           "value": ["abundant", "unknown", "ambiguous", "absent"],
                           "phase": ["attack", "general", "unknown", "ambiguous", "absent"],
                           "quantifier": ["many", "numeric", "none", "unknown", "ambiguous", "absent"],
                           "polarity": ["affirmed", "negated", "unknown", "ambiguous"]}
                for field, values in samples.items():
                    for content in values:
                        for count in (0, 1, 2):
                            for literal in ((None, "2") if field == "quantifier" else (None,)):
                                payload = slot(status, content, *["p" + str(i) for i in range(count)])
                                if field == "quantifier": payload["literal"] = literal
                                value = frame(); value[side][field] = payload
                                final, text = projected(payload, origin)
                                if field in {"semantic_axis", "value"}:
                                    errors = spatial._value_slot_errors(final, origin, text,
                                        "axis" if field == "semantic_axis" else "value",
                                        side == "claim_relation", "space_availability")
                                else:
                                    errors = getattr(spatial, "_" + field + "_errors")(final, origin, text)
                                self.assertEqual(not extraction.extraction_shape_errors(value), not errors,
                                                 (side, field, status, content, count, literal))
                                cases += 1
        self.assertGreater(cases, 1000)

    def test_critical_code_and_evidence_invariants_are_unchanged(self):
        path = "projects/tactical-engine/scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py"
        old = ast.parse(subprocess.check_output(["git", "show", FROZEN + ":" + path]).decode())
        new = ast.parse((PROJECT / "scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py").read_text())
        def funcs(tree): return {n.name: ast.dump(n, include_attributes=False) for n in tree.body if isinstance(n, ast.FunctionDef)}
        for name in ("_occurrences", "_localize_fragments", "_materialize_relation", "_provenance",
                     "materialize_extraction", "extraction_semantic_errors", "verify_materialization", "boundary_failure"):
            self.assertEqual(funcs(old)[name], funcs(new)[name], name)
        self.assertEqual(subprocess.check_output(["git", "diff", FROZEN, "--",
                         "projects/tactical-engine/scripts/v5_tactical_semantic_support_s2_spatial_v2.py",
                         "projects/tactical-engine/eval", "projects/tactical-engine/evaluation/runtime04_execution_01",
                         "projects/tactical-engine/api", "projects/tactical-engine/operations"]), b"")


if __name__ == "__main__":
    unittest.main(verbosity=2)
