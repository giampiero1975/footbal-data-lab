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


bridge = load("s2_nli_v2_bridge", "v5_tactical_semantic_support_s2_nli_v2_bridge.py")
s2 = load("s2_nli_v2_bridge_adapter", "v5_tactical_semantic_support_s2.py")
s1 = load("s2_nli_v2_bridge_s1", "v5_tactical_semantic_support_s1.py")


PAYLOAD = {
    "claim_id": "claim:bridge",
    "statement": "Ogni ala non esce finché la palla resta coperta.",
    "conditions": ["finché la palla resta coperta"],
    "polarity": "negated",
    "bindings": {
        "actor": "actor:ala", "task": "task:non-uscire",
        "space": "space:lato-debole", "trigger": "trigger:palla-coperta",
        "purpose": "purpose:protezione", "phase": "phase:transizione-negativa",
    },
    "evidence_ref": "F1",
    "evidence": "Quando la palla è coperta, l'ala conserva la posizione.",
}
CONFIG = {"engine": "nli-v2", "model": "injected-mock", "prompt": "canonical-v2"}


class NliV2S2BridgeTests(unittest.TestCase):
    def test_01_maps_claim_and_evidence_without_loss(self):
        calls = []
        judge = bridge.build_bridge(
            lambda claim, evidence: calls.append((claim, evidence)) or "supported",
            CONFIG)
        result = judge(PAYLOAD)
        self.assertEqual(result["label"], "supported")
        self.assertEqual(calls[0][1], PAYLOAD["evidence"])
        projected = calls[0][0]
        self.assertIn("statement=" + PAYLOAD["statement"], projected)
        self.assertIn("conditions_json=" + json.dumps(
            PAYLOAD["conditions"], ensure_ascii=False, sort_keys=True,
            separators=(",", ":")), projected)
        self.assertIn("polarity=negated", projected)
        self.assertIn("bindings_json=" + json.dumps(
            PAYLOAD["bindings"], ensure_ascii=False, sort_keys=True,
            separators=(",", ":")), projected)

    def test_02_normalises_only_the_three_historical_labels(self):
        for label in ("supported", "contradicted", "insufficient"):
            with self.subTest(label=label):
                judge = bridge.build_bridge(lambda _c, _e, value=label: value, CONFIG)
                self.assertEqual(judge(PAYLOAD)["label"], label)

    def test_03_unknown_or_malformed_results_fail_closed(self):
        outputs = ("maybe", None, {"label": "supported"},
                   {"label": "supported", "rationale": ""},
                   {"label": "supported", "rationale": "ok", "extra": True},
                   {"label": ["supported"], "rationale": "invalid label"})
        for output in outputs:
            with self.subTest(output=output):
                judge = bridge.build_bridge(lambda _c, _e, value=output: value, CONFIG)
                with self.assertRaises(bridge.BridgeContractError):
                    judge(PAYLOAD)

        rationale_judge = bridge.build_bridge(
            lambda _c, _e: {"label": "supported", "rationale": "Preserved."},
            CONFIG)
        self.assertEqual(rationale_judge(PAYLOAD)["rationale"], "Preserved.")

    def test_04_judge_exception_is_not_swallowed_by_bridge(self):
        def failure(_claim, _evidence):
            raise TimeoutError("offline simulated timeout")
        judge = bridge.build_bridge(failure, CONFIG)
        with self.assertRaises(TimeoutError):
            judge(PAYLOAD)

    def test_05_incompatible_payload_fails_before_judge(self):
        called = []
        judge = bridge.build_bridge(
            lambda *_args: called.append(True) or "supported", CONFIG)
        malformed = dict(PAYLOAD)
        malformed.pop("conditions")
        with self.assertRaises(bridge.BridgeContractError):
            judge(malformed)
        self.assertEqual(called, [])

    def test_06_configuration_and_provenance_are_preserved(self):
        judge = bridge.build_bridge(lambda _c, _e: "supported", CONFIG)
        descriptor = judge.judge_descriptor
        self.assertEqual(descriptor["name"], "shadow-nli-v2-s2-bridge")
        self.assertEqual(descriptor["config"]["nli_config"], CONFIG)
        self.assertEqual(descriptor["config"]["bridge_schema"], bridge.BRIDGE_SCHEMA)
        self.assertEqual(
            descriptor["config"]["rationale_mode"],
            "bridge_trace_only_no_semantic_rationale")

    def test_07_adapter_contains_bridge_errors_and_never_promotes(self):
        judge = bridge.build_bridge(
            lambda _c, _e: (_ for _ in ()).throw(TimeoutError("mock")), CONFIG)
        descriptor = judge.judge_descriptor
        claim = {
            "claim_id": "claim:bridge", "statement": PAYLOAD["statement"],
            "section_span": {"start": 0, "end": len(PAYLOAD["statement"])},
            "conditions": PAYLOAD["conditions"], "polarity": PAYLOAD["polarity"],
            "bindings": PAYLOAD["bindings"], "relation_refs": ["relation:1"],
            "requirement_refs": ["requirement:1"],
            "dimensions": ["actor", "task", "space", "trigger", "purpose", "phase"],
            "evidence_refs": ["F1"], "support_mode": "direct",
            "evidence_anchors": [{"evidence_ref": "F1", "exact_text": PAYLOAD["evidence"]}],
        }
        evidence = {"F1": {"text": PAYLOAD["evidence"]}}
        plan_fingerprint = "sha256:" + "1" * 64
        s1_assessment = s1.assess_claim(
            "attempt:bridge", plan_fingerprint, claim, evidence)
        record = s2.assess_claim(
            "attempt:bridge", plan_fingerprint, claim, evidence, s1_assessment,
            {"relation:1": PAYLOAD["bindings"]}, judge, descriptor)
        self.assertEqual(record["evaluation_status"], "not_evaluable")
        self.assertIn("judge_error:TimeoutError", record["reason_codes"])
        self.assertFalse(record["promotion_authorized"])

    def test_08_build_is_inert_and_does_not_call_nli(self):
        calls = []
        judge = bridge.build_bridge(
            lambda *_args: calls.append(True) or "supported", CONFIG)
        self.assertEqual(calls, [])
        self.assertTrue(callable(judge))


if __name__ == "__main__":
    unittest.main()
