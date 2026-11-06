import ast
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


runner = load("s2_spatial_differential_runner",
              "run_tactical_semantic_support_s2_spatial_relation_differential_v1.py")
spatial_bridge = load("s2_spatial_differential_bridge",
                      "v5_tactical_semantic_support_s2_spatial_v1_bridge.py")
FIXTURE = ROOT / "evaluation" / "tactical_semantic_support_s2_spatial_relation_differential_fixture_v1.json"
CONFIG = dict(spatial_bridge.EXPECTED_CONFIG)
CONTRACT = {
    "contract_id": "nli_spatial_relations_v1",
    "version": "1.0",
    "base_contract": "shadow_nli_v2_inference",
    "labels": ["supported", "contradicted", "insufficient"],
    "instruction_sha256": spatial_bridge.INSTRUCTION_SHA256,
    "selection": "explicit_import_only",
}


class SpatialDifferentialRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This pre-existing Windows checkout may still materialize the dataset
        # as CRLF although .gitattributes now freezes fresh checkouts to LF.
        # Exercise the runner against the canonical Git/LF bytes without
        # modifying the source dataset in place.
        cls._canonical_tmp = tempfile.TemporaryDirectory()
        cls.canonical_root = Path(cls._canonical_tmp.name)
        target = cls.canonical_root / "eval" / "claim_fidelity_gold_v1.json"
        target.parent.mkdir(parents=True)
        target.write_bytes(
            (ROOT / "eval" / "claim_fidelity_gold_v1.json")
            .read_bytes().replace(b"\r\n", b"\n"))

    @classmethod
    def tearDownClass(cls):
        cls._canonical_tmp.cleanup()

    def inputs(self):
        return runner.load_inputs(self.canonical_root, FIXTURE)

    def test_01_frozen_roles_labels_and_dataset_identity(self):
        fixture, cases, identities = self.inputs()
        self.assertEqual([case["id"] for case in cases],
                         ["q3_04", "q5_06", "q5_02"])
        self.assertEqual({case["role"] for case in cases}, runner.EXPECTED_ROLES)
        self.assertEqual([case["gold"] for case in cases],
                         ["contradicted", "contradicted", "insufficient"])
        self.assertEqual(identities["source_dataset_sha256"],
                         "sha256:8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c")
        self.assertEqual(fixture["activity_id"], runner.ACTIVITY_ID)

    def test_02_expected_labels_are_not_sent_to_the_judge(self):
        fixture, cases, identities = self.inputs()
        calls = []
        labels = iter(case["gold"] for case in cases)
        def nli(claim, evidence):
            calls.append((claim, evidence))
            return next(labels)
        bridge = spatial_bridge.build_bridge(nli, CONFIG, CONTRACT)
        report = runner.execute_cases(
            fixture, cases, identities, bridge, bridge.judge_descriptor,
            CONFIG, CONTRACT)
        self.assertEqual(len(calls), 3)
        self.assertEqual(report["planned_evaluations"], 3)
        self.assertEqual(report["attempted_evaluations"], 3)
        self.assertEqual(report["completed_evaluations"], 3)
        self.assertTrue(report["run_complete"])
        self.assertEqual(runner.report_exit_code(report), 0)
        self.assertTrue(all("expected_label" not in claim for claim, _ in calls))
        self.assertTrue(all("q3_04" not in evidence for _, evidence in calls))
        self.assertTrue(report["summary"]["all_non_promotable"])
        self.assertFalse(report["authoritative_outputs_modified"])

    def test_03_error_stops_after_one_call_and_is_not_evaluable(self):
        fixture, cases, identities = self.inputs()
        calls = []
        def broken(_claim, _evidence):
            calls.append(True)
            raise TimeoutError("offline mock timeout")
        bridge = spatial_bridge.build_bridge(broken, CONFIG, CONTRACT)
        report = runner.execute_cases(
            fixture, cases, identities, bridge, bridge.judge_descriptor,
            CONFIG, CONTRACT)
        self.assertEqual(calls, [True])
        self.assertEqual(report["attempted_evaluations"], 1)
        self.assertEqual(report["completed_evaluations"], 0)
        self.assertFalse(report["run_complete"])
        self.assertEqual(runner.report_exit_code(report), 2)
        self.assertTrue(report["stopped_early"])
        self.assertFalse(report["cases"][0]["semantic_match"])
        self.assertEqual(report["cases"][0]["s2_shadow_assessment"]["evaluation_status"],
                         "not_evaluable")

    def test_04_source_digest_and_label_changes_fail_closed(self):
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        fixture["source_dataset_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp:
            altered = Path(tmp) / "fixture.json"
            altered.write_text(json.dumps(fixture), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source_dataset_digest_mismatch"):
                runner.load_inputs(self.canonical_root, altered)
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        fixture["cases"][0]["expected_label"] = "supported"
        with tempfile.TemporaryDirectory() as tmp:
            altered = Path(tmp) / "fixture.json"
            altered.write_text(json.dumps(fixture), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "selected_case_label_mismatch"):
                runner.load_inputs(self.canonical_root, altered)

    def test_05_runner_selects_only_spatial_contract_and_has_no_v2_call(self):
        source = (SCRIPTS / "run_tactical_semantic_support_s2_spatial_relation_differential_v1.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = [node for node in ast.walk(tree) if isinstance(node, ast.Import)]
        names = {alias.name for node in imported for alias in node.names}
        self.assertIn("shadow_nli_spatial_relations_v1_inference", names)
        self.assertNotIn("shadow_nli_v2_inference", names)
        self.assertIn("v5_tactical_semantic_support_s2_spatial_v1_bridge", names)
        self.assertNotIn("v5_tactical_semantic_support_s2_nli_v2_bridge", names)
        self.assertIn("--execute", source)
        self.assertEqual(runner.MAX_CASES, 3)

    def test_06_fixture_records_only_one_equivalent_v2_result(self):
        _fixture, cases, _identities = self.inputs()
        direct = [case for case in cases
                  if case["historical_v2"].get("status") == "directly_attributable"]
        self.assertEqual([case["id"] for case in direct], ["q3_04"])
        self.assertEqual(direct[0]["historical_v2"]["observed_label"], "supported")
        self.assertTrue(all(case["historical_v2"].get("status") ==
                            "not_available_as_equivalent_artifact"
                            for case in cases[1:]))


if __name__ == "__main__":
    unittest.main()
