import copy
import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


bridge = load("s2_spatial_v1_bridge", "v5_tactical_semantic_support_s2_spatial_v1_bridge.py")
s2 = load("s2_spatial_v1_adapter", "v5_tactical_semantic_support_s2.py")
s1 = load("s2_spatial_v1_s1", "v5_tactical_semantic_support_s1.py")

CONFIG = copy.deepcopy(bridge.EXPECTED_CONFIG)
CONTRACT = {
    "contract_id": "nli_spatial_relations_v1",
    "version": "1.0",
    "base_contract": "shadow_nli_v2_inference",
    "labels": ["supported", "contradicted", "insufficient"],
    "instruction_sha256": bridge.INSTRUCTION_SHA256,
    "selection": "explicit_import_only",
}
PAYLOAD = {
    "claim_id": "claim:spatial",
    "statement": "La linea toglie spazio tra difesa e porta.",
    "conditions": [],
    "polarity": "affirmed",
    "bindings": {},
    "evidence_ref": "F1",
    "evidence": "La difesa bassa toglie spazio tra linea e porta.",
}


class SpatialV1BridgeTests(unittest.TestCase):
    def test_01_build_is_inert_and_descriptor_is_spatial(self):
        calls = []
        adapter = bridge.build_bridge(
            lambda *_args: calls.append(True) or "supported", CONFIG, CONTRACT)
        self.assertEqual(calls, [])
        value = adapter.judge_descriptor
        self.assertEqual(value["name"], "shadow-nli-spatial-v1-s2-bridge")
        self.assertEqual(value["config"]["declared_callable_identity"],
                         "shadow_nli_spatial_relations_v1_inference.judge_pair")
        self.assertEqual(value["config"]["runtime_callable_authentication"],
                         "not_performed_by_bridge")
        self.assertNotIn("nli_contract", value["config"])

    def test_02_defensive_copies_protect_provenance(self):
        config, contract = copy.deepcopy(CONFIG), copy.deepcopy(CONTRACT)
        adapter = bridge.build_bridge(lambda *_: "supported", config, contract)
        expected = adapter.judge_descriptor
        config["model"] = "altered"
        contract["contract_id"] = "altered"
        exposed = adapter.judge_descriptor
        exposed["config"]["nli_config"]["model"] = "altered-again"
        self.assertEqual(adapter.judge_descriptor, expected)

    def test_03_invalid_config_and_contract_fail_at_construction(self):
        mutations = []
        for key in CONFIG:
            value = copy.deepcopy(CONFIG)
            value.pop(key)
            mutations.append((value, CONTRACT))
        extra = copy.deepcopy(CONFIG); extra["extra"] = True
        mutations.append((extra, CONTRACT))
        for key, value in (("timeout_seconds_per_call", True),
                           ("temperature", False), ("retry", 0),
                           ("model", ["qwen3.5:9b"])):
            altered = copy.deepcopy(CONFIG); altered[key] = value
            mutations.append((altered, CONTRACT))
        wrong = copy.deepcopy(CONFIG); wrong["max_tokens"] = 2048
        mutations.append((wrong, CONTRACT))
        missing = copy.deepcopy(CONTRACT); missing.pop("base_contract")
        mutations.append((CONFIG, missing))
        unexpected = copy.deepcopy(CONTRACT); unexpected["extra"] = True
        mutations.append((CONFIG, unexpected))
        bad_digest = copy.deepcopy(CONTRACT); bad_digest["instruction_sha256"] = "sha256:" + "0" * 64
        mutations.append((CONFIG, bad_digest))
        for config, contract in mutations:
            with self.subTest(config=config, contract=contract):
                with self.assertRaises(bridge.BridgeContractError):
                    bridge.build_bridge(lambda *_: "supported", config, contract)

    def test_04_projection_and_evidence_are_unchanged(self):
        calls = []
        adapter = bridge.build_bridge(
            lambda claim, evidence: calls.append((claim, evidence)) or "supported",
            CONFIG, CONTRACT)
        adapter(PAYLOAD)
        historical = __import__("v5_tactical_semantic_support_s2_nli_v2_bridge")
        self.assertEqual(calls, [(historical.project_claim(PAYLOAD), PAYLOAD["evidence"])])

    def test_05_labels_and_technical_notice(self):
        for label in ("supported", "contradicted", "insufficient"):
            with self.subTest(label=label):
                adapter = bridge.build_bridge(
                    lambda *_args, value=label: value, CONFIG, CONTRACT)
                result = adapter(PAYLOAD)
                self.assertEqual(result, {"label": label,
                                          "rationale": bridge.TECHNICAL_NOTICE})
                self.assertIn("not verdict rationale", result["rationale"])
                self.assertNotIn("NLI V2 returned", result["rationale"])

    def test_06_malformed_outputs_fail_closed(self):
        for output in (None, "maybe", ["supported"],
                       {"label": "supported", "rationale": "invented"}):
            with self.subTest(output=output):
                adapter = bridge.build_bridge(
                    lambda *_args, value=output: value, CONFIG, CONTRACT)
                with self.assertRaises(bridge.BridgeContractError):
                    adapter(PAYLOAD)

    def test_07_s2_contains_errors_and_never_promotes(self):
        def failure(*_args):
            raise TimeoutError("offline mock")
        adapter = bridge.build_bridge(failure, CONFIG, CONTRACT)
        claim = {
            "claim_id": PAYLOAD["claim_id"], "statement": PAYLOAD["statement"],
            "conditions": [], "polarity": "affirmed", "bindings": {},
            "relation_refs": ["relation:1"], "requirement_refs": ["requirement:1"],
            "dimensions": ["detail"], "evidence_refs": ["F1"],
            "support_mode": "direct",
            "evidence_anchors": [{"evidence_ref": "F1", "exact_text": PAYLOAD["evidence"]}],
        }
        evidence = {"F1": {"text": PAYLOAD["evidence"]}}
        fingerprint = "sha256:" + "1" * 64
        s1_record = s1.assess_claim("attempt:spatial", fingerprint, claim, evidence)
        record = s2.assess_claim(
            "attempt:spatial", fingerprint, claim, evidence, s1_record,
            {"relation:1": {}}, adapter, adapter.judge_descriptor)
        self.assertEqual(record["evaluation_status"], "not_evaluable")
        self.assertIn("judge_error:TimeoutError", record["reason_codes"])
        self.assertFalse(record["promotion_authorized"])

    def test_08_config_and_record_digests_are_independently_reproducible(self):
        adapter = bridge.build_bridge(lambda *_: "supported", CONFIG, CONTRACT)
        descriptor = adapter.judge_descriptor
        expected_config = "sha256:" + hashlib.sha256(
            json.dumps(descriptor["config"], ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")).encode("utf-8")).hexdigest()
        self.assertEqual(s2._judge_identity(descriptor)["config_sha256"], expected_config)
        claim = {
            "claim_id": PAYLOAD["claim_id"], "statement": PAYLOAD["statement"],
            "conditions": [], "polarity": "affirmed", "bindings": {},
            "relation_refs": ["relation:1"], "requirement_refs": ["requirement:1"],
            "dimensions": ["detail"], "evidence_refs": ["F1"],
            "support_mode": "direct",
            "evidence_anchors": [{"evidence_ref": "F1", "exact_text": PAYLOAD["evidence"]}],
        }
        evidence = {"F1": {"text": PAYLOAD["evidence"]}}
        fingerprint = "sha256:" + "2" * 64
        s1_record = s1.assess_claim("attempt:digest", fingerprint, claim, evidence)
        record = s2.assess_claim(
            "attempt:digest", fingerprint, claim, evidence, s1_record,
            {"relation:1": {}}, adapter, descriptor)
        payload = copy.deepcopy(record)
        payload["record_sha256"] = None
        expected_record = "sha256:" + hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")).encode("utf-8")).hexdigest()
        self.assertEqual(record["record_sha256"], expected_record)
        self.assertEqual(record["evidence"][0]["judge_rationale"],
                         bridge.TECHNICAL_NOTICE)
        self.assertFalse(record["promotion_authorized"])


if __name__ == "__main__":
    unittest.main()
