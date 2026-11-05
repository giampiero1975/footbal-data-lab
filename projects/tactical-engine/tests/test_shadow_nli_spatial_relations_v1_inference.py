import ast
import hashlib
import importlib.util
import io
import json
import sys
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load():
    spec = importlib.util.spec_from_file_location(
        "shadow_nli_spatial_relations_v1_inference",
        SCRIPTS / "shadow_nli_spatial_relations_v1_inference.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


contract = load()


class Response:
    def __init__(self, value):
        self.stream = io.StringIO(json.dumps(value))

    def __enter__(self):
        return self.stream

    def __exit__(self, *_args):
        return False


class FakeVerdict:
    @classmethod
    def model_validate_json(cls, content):
        value = json.loads(content)
        if set(value) != {"label"} or value["label"] not in contract.LABELS:
            raise ValueError("invalid verdict")
        return types.SimpleNamespace(label=value["label"])


class SpatialRelationsContractTests(unittest.TestCase):
    def test_01_contract_is_versioned_and_explicit_only(self):
        self.assertEqual(contract.CONTRACT_ID, "nli_spatial_relations_v1")
        self.assertEqual(contract.CONTRACT_VERSION, "1.0")
        self.assertEqual(contract.LABELS,
                         ("supported", "contradicted", "insufficient"))
        self.assertEqual(contract.descriptor()["selection"],
                         "explicit_import_only")

    def test_02_instruction_requires_relational_identity_and_direction(self):
        text = contract.INSTRUCTION
        for required in ("soggetto", "riferimento spaziale",
                         "direzione della relazione", "condizioni",
                         "fase o tempo di gioco", "stessa relazione"):
            self.assertIn(required, text)
        self.assertIn("anche senza una negazione grammaticale esplicita", text)
        self.assertIn("non sono una blacklist lessicale", text)

    def test_03_insufficient_is_not_promoted_to_contradiction(self):
        text = contract.INSTRUCTION
        self.assertIn("la semplice assenza di conferma non è una contraddizione",
                      text)
        self.assertIn("la fonte tace sulla relazione, scegli insufficient", text)
        self.assertIn("parole comuni", text)

    def test_04_q3_04_is_only_a_motivating_input_not_a_hardcoded_label(self):
        gold = json.loads((ROOT / "eval" / "claim_fidelity_gold_v1.json")
                          .read_text(encoding="utf-8"))
        case = next(item for item in gold["cases"] if item["id"] == "q3_04")
        prompt = contract.build_prompt(case["claim"], case["evidence"])
        self.assertIn(case["claim"], prompt)
        self.assertIn(case["evidence"], prompt)
        self.assertNotIn("q3_04", prompt)
        self.assertNotIn("expected_label", prompt)

    def test_05_v2_instruction_and_default_routing_are_unchanged(self):
        path = SCRIPTS / "benchmark_direct_three_label_nli_v2.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        instruction = next(
            ast.literal_eval(node.value) for node in tree.body
            if isinstance(node, ast.Assign)
            and isinstance(node.targets[0], ast.Attribute)
            and node.targets[0].attr == "INSTRUCTION")
        self.assertEqual(
            hashlib.sha256(instruction.encode("utf-8")).hexdigest(),
            "e7ce58bb021029f12b57ba306c8c0181a658f2a330bdbd0a2f83e0148129efdb")
        for filename in (
                "shadow_nli_v2_inference.py",
                "v5_tactical_semantic_support_s2_nli_v2_bridge.py",
                "run_tactical_semantic_support_s2_first_controlled_runtime_v1.py"):
            self.assertNotIn(contract.CONTRACT_ID,
                             (SCRIPTS / filename).read_text(encoding="utf-8"))

    def test_06_transport_remains_structured_and_fail_closed_with_mocks(self):
        fake_module = types.ModuleType("shadow_nli_v2_inference")
        fake_module.SCHEMA = {
            "type": "object", "required": ["label"],
            "properties": {"label": {"enum": list(contract.LABELS)}}}
        fake_module.Verdict = FakeVerdict
        success = {"done_reason": "stop",
                   "message": {"content": '{"label":"contradicted"}'}}
        with mock.patch.dict(sys.modules,
                             {"shadow_nli_v2_inference": fake_module}), \
                mock.patch.object(contract.urllib.request, "urlopen",
                                  return_value=Response(success)):
            self.assertEqual(contract.judge_pair("claim", "evidence"),
                             "contradicted")
        incomplete = {"done_reason": "length",
                      "message": {"content": '{"label":"supported"}'}}
        with mock.patch.dict(sys.modules,
                             {"shadow_nli_v2_inference": fake_module}), \
                mock.patch.object(contract.urllib.request, "urlopen",
                                  return_value=Response(incomplete)):
            with self.assertRaisesRegex(RuntimeError, "output incomplete"):
                contract.judge_pair("claim", "evidence")


if __name__ == "__main__":
    unittest.main()
