import importlib.util
import json
import sys
import tempfile
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


runner = load("s2_first_controlled_runner",
              "run_tactical_semantic_support_s2_first_controlled_runtime_v1.py")
bridge_v1 = load("s2_first_controlled_bridge",
                 "v5_tactical_semantic_support_s2_nli_v2_bridge.py")
FIXTURE = ROOT / "evaluation" / "tactical_semantic_support_s2_first_controlled_runtime_fixture_v1.json"


class FirstControlledS2RunnerTests(unittest.TestCase):
    def inputs(self):
        return runner.load_inputs(ROOT, FIXTURE)

    def test_01_fixture_is_content_addressed_and_balanced(self):
        fixture, cases, identities = self.inputs()
        self.assertEqual(len(cases), 3)
        self.assertEqual({case["gold"] for case in cases},
                         {"supported", "contradicted", "insufficient"})
        self.assertTrue(identities["fixture_sha256"].startswith("sha256:"))
        self.assertEqual(
            identities["source_dataset_sha256"],
            "sha256:8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c")
        self.assertEqual(fixture["activity_id"],
                         "RD-TSC-V2-D3-S2-FIRST-CONTROLLED-RUNTIME-01")

    def test_02_three_mock_calls_traverse_bridge_and_never_promote(self):
        fixture, cases, identities = self.inputs()
        labels = iter(case["gold"] for case in cases)
        calls = []
        def nli(claim, evidence):
            calls.append((claim, evidence))
            return next(labels)
        bridge = bridge_v1.build_bridge(nli, {"model": "mock", "retry": False})
        report = runner.execute_cases(
            fixture, cases, identities, bridge, bridge.judge_descriptor,
            {"model": "mock", "retry": False})
        self.assertEqual(len(calls), 3)
        self.assertEqual(report["actual_inferences"], 3)
        self.assertEqual(report["summary"]["technical_passes"], 3)
        self.assertEqual(report["summary"]["semantic_matches"], 3)
        self.assertTrue(report["summary"]["all_s1_unchanged"])
        self.assertTrue(report["summary"]["all_non_promotable"])
        self.assertTrue(all("S2_CLAIM_V1" in call[0] for call in calls))

    def test_03_error_is_fail_closed_and_stops_without_retry(self):
        fixture, cases, identities = self.inputs()
        calls = []
        def broken(_claim, _evidence):
            calls.append(True)
            raise TimeoutError("offline mock timeout")
        bridge = bridge_v1.build_bridge(
            broken, {"model": "mock", "retry": False})
        report = runner.execute_cases(
            fixture, cases, identities, bridge, bridge.judge_descriptor,
            {"model": "mock", "retry": False})
        self.assertEqual(calls, [True])
        self.assertEqual(report["actual_inferences"], 1)
        self.assertTrue(report["stopped_early"])
        row = report["cases"][0]
        self.assertEqual(
            row["s2_shadow_assessment"]["evaluation_status"],
            "not_evaluable")
        self.assertFalse(row["s2_shadow_assessment"]["promotion_authorized"])

    def test_04_source_digest_mismatch_blocks_before_judge(self):
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        fixture["source_dataset_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp:
            altered = Path(tmp) / "fixture.json"
            altered.write_text(json.dumps(fixture), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source_dataset_digest_mismatch"):
                runner.load_inputs(ROOT, altered)


if __name__ == "__main__":
    unittest.main()
