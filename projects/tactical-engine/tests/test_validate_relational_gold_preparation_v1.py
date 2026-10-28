import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_relational_gold_preparation_v1.py"
SPEC = importlib.util.spec_from_file_location("gold_preparation", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
ANNOTATIONS = ROOT / "evaluation" / "annotations"


class RelationalGoldPreparationTests(unittest.TestCase):
    def test_repository_artifacts_are_valid_and_empty(self):
        errors = MODULE.validate_all(
            ANNOTATIONS / "relational_gold_e_schema_v1.json",
            ANNOTATIONS / "relational_gold_v_schema_v1.json",
            ANNOTATIONS / "relational_gold_e_template_v1.json",
            ANNOTATIONS / "relational_gold_v_template_v1.json",
            ANNOTATIONS / "relational_gold_freeze_manifest_template_v1.json",
        )
        self.assertEqual(errors, [])

    def test_populated_gold_e_template_is_rejected(self):
        document = json.loads((ANNOTATIONS / "relational_gold_e_template_v1.json").read_text())
        document["cases"] = [{"case_id": "not-authorized"}]
        self.assertIn("e: template must contain zero cases", MODULE.validate_template(document, "e"))

    def test_gold_v_cannot_claim_unavailable_gold_e_as_frozen(self):
        document = json.loads((ANNOTATIONS / "relational_gold_v_template_v1.json").read_text())
        document["gold_e_reference"]["freeze_status"] = "frozen"
        self.assertIn("v: empty template cannot claim a frozen Gold E", MODULE.validate_template(document, "v"))

    def test_draft_manifest_cannot_claim_freeze(self):
        document = json.loads((ANNOTATIONS / "relational_gold_freeze_manifest_template_v1.json").read_text())
        document["dataset_sha256"] = "a" * 64
        self.assertIn("manifest: draft cannot claim dataset hash or freeze timestamp", MODULE.validate_manifest(document))

    def test_schema_requires_independence_and_four_separate_gold_v_judgements(self):
        schema_e = json.loads((ANNOTATIONS / "relational_gold_e_schema_v1.json").read_text())
        schema_v = json.loads((ANNOTATIONS / "relational_gold_v_schema_v1.json").read_text())
        self.assertIn("independence_status", schema_e["$defs"]["case"]["required"])
        required_v = set(schema_v["$defs"]["case"]["required"])
        self.assertTrue({"completeness", "relational_coherence", "tactical_correctness", "documentary_support"} <= required_v)


if __name__ == "__main__":
    unittest.main()
