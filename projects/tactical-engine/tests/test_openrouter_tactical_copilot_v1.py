import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load_module():
    path = ROOT / "scripts/openrouter_tactical_copilot_v1.py"
    spec = importlib.util.spec_from_file_location("openrouter_tactical_copilot_v1", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mod = load_module()


class OpenRouterCopilotTests(unittest.TestCase):
    def case(self, folder: Path) -> Path:
        path = folder / "case.json"
        path.write_text(json.dumps({"questions": [{
            "id": "case_01", "question": "Come attacchi un blocco basso?",
            "answer": "Creo ampiezza [F1].", "invalid_citation_ids": [],
            "has_any_citation": True, "evidence": [{"label": "F1", "text": "Ampiezza."}],
        }]}), encoding="utf-8")
        return path

    def test_request_uses_one_router_with_ordered_fallbacks(self):
        request = mod.strict_request("prompt", {"cases": []}, {"type": "object"},
                                     "schema", mod.DEFAULT_MODELS)
        self.assertEqual(request["model"], mod.DEFAULT_MODELS[0])
        self.assertEqual(request["models"], mod.DEFAULT_MODELS)
        self.assertTrue(request["provider"]["allow_fallbacks"])
        self.assertTrue(request["provider"]["require_parameters"])
        self.assertEqual(request["provider"]["data_collection"], "deny")

    def test_case_cardinality_is_enforced_in_both_passes(self):
        cases = [{"id": "case_01", "question": "Q", "answer": "A", "evidence": []}]
        request1 = mod.build_pass1(cases, mod.DEFAULT_MODELS)
        reviews = request1["response_format"]["json_schema"]["schema"]["properties"]["reviews"]
        self.assertEqual((reviews["minItems"], reviews["maxItems"]), (1, 1))
        pass1 = {"reviews": [{"id": "case_01", "findings": []}]}
        request2 = mod.build_pass2(cases, pass1, mod.DEFAULT_MODELS)
        revised = request2["response_format"]["json_schema"]["schema"]["properties"]["revised_answers"]
        self.assertEqual((revised["minItems"], revised["maxItems"]), (1, 1))

    def test_offline_preflight_makes_no_network_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp); output = folder / "preflight.json"
            with mock.patch.object(mod, "call_openrouter") as network:
                mod.preflight([self.case(folder)], output, mod.DEFAULT_MODELS)
            network.assert_not_called()
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "VALIDATO")
            self.assertFalse(report["network_called"])

    def test_execute_requires_openrouter_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            with mock.patch.dict(os.environ, {}, clear=True):
                with self.assertRaisesRegex(SystemExit, "OPENROUTER_API_KEY_MISSING"):
                    mod.execute([self.case(folder)], folder / "out.json", mod.DEFAULT_MODELS)

    def test_failure_report_does_not_persist_prompt_or_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "failure.json"
            mod.write_failure(output, mod.DEFAULT_MODELS, "OPENROUTER_HTTP_429")
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertFalse(report["contains_prompt_or_evidence"])
            self.assertNotIn("messages", report)


if __name__ == "__main__":
    unittest.main()
