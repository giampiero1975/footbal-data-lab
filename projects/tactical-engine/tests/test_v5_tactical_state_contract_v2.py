import importlib.util
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v1 = load("tsc_v1_for_v2_tests", SCRIPTS / "v5_tactical_state_contract_v1.py")
planner = load("tsc_planner_for_v2_tests", SCRIPTS / "v5_tactical_query_plan_v1.py")
v2 = load("tsc_v2_tests", SCRIPTS / "v5_tactical_state_contract_v2.py")


QUESTION = "Alla perdita l'ala deve coprire il lato debole per evitare la ripartenza?"


def question_plan():
    plan = planner.analyse(QUESTION)
    # The current planner treats this literal relation as explicit.
    return plan


def relation_fixture(plan):
    projected = v2.project_relation_requirements(plan)
    required = next(item for item in projected if item["classification"] == "explicit_representable")
    state = deepcopy(plan["state_contract"])
    state["phase_states"][0]["state_id"] = "state:negative_transition"
    state["phase_states"][0]["phase"] = "negative_transition"
    v2_plan = v2.build_v2_plan(state)
    relation = {
        "relation_id": "relation:negative_transition:wing:0",
        "requirement_ref": {"id": required["requirement_id"], "kind": "relation_requirement"},
        "requirement_fingerprint": required["fingerprint"],
        "actor_ref": deepcopy(required["actor_ref"]),
        "task": deepcopy(required["task"]),
        "space": deepcopy(required["space"]),
        "trigger": deepcopy(required["trigger"]),
        "purpose": deepcopy(required["purpose"]),
        "phase_state_ref": {"id": "state:negative_transition", "kind": "phase_state"},
        "assertion_mode": "executable", "provenance": "explicit", "rule_id": None,
    }
    v2_plan["operational_relations"] = [relation]
    return v2_plan, relation, required


class OperationalRelationsV2Tests(unittest.TestCase):
    def test_v1_identity_and_schema_remain_unchanged(self):
        self.assertEqual(v1.SCHEMA, "tactical_state_contract_v1")
        self.assertEqual(v1.CONTRACT_VERSION, "1.1.0")
        self.assertNotIn("operational_relations", v1.generation_transport_schema()["properties"]["applied_plan"]["properties"])

    def test_projection_fingerprint_is_stable_and_content_sensitive(self):
        first = v2.project_relation_requirements(question_plan())
        second = v2.project_relation_requirements(question_plan())
        self.assertEqual(first, second)
        changed = deepcopy(first[0])
        changed["task"] = v2.explicit_term("ripiegare")
        self.assertNotEqual(v2.requirement_fingerprint(first[0]), v2.requirement_fingerprint(changed))

    def test_explicit_relation_is_represented(self):
        plan = question_plan()
        candidate, _, _ = relation_fixture(plan)
        result = v2.validate_operational_relations(plan, candidate)
        self.assertEqual(result["status"], "passed")
        self.assertFalse(result["failures"])

    def test_explicit_relation_omission_is_blocking_failure(self):
        plan = question_plan()
        candidate, _, required = relation_fixture(plan)
        candidate["operational_relations"] = []
        result = v2.validate_operational_relations(plan, candidate)
        self.assertEqual(result["status"], "failed")
        self.assertIn(required["requirement_id"], result["checked_scope"])
        self.assertIn("explicit_operational_requirement_omitted",
                      [item["code"] for item in result["failures"]])

    def test_id_only_cannot_cover_changed_task(self):
        plan = question_plan()
        candidate, relation, _ = relation_fixture(plan)
        relation["task"] = v2.explicit_term("ripiegare")
        result = v2.validate_operational_relations(plan, candidate)
        self.assertIn("operational_task_mismatch", [item["code"] for item in result["failures"]])

    def test_fingerprint_mismatch_is_rejected(self):
        plan = question_plan()
        candidate, relation, _ = relation_fixture(plan)
        relation["requirement_fingerprint"] = "sha256:" + "0" * 64
        result = v2.validate_operational_relations(plan, candidate)
        self.assertIn("requirement_fingerprint_mismatch", [item["code"] for item in result["failures"]])

    def test_unknown_mandatory_trigger_is_rejected(self):
        plan = question_plan()
        candidate, relation, required = relation_fixture(plan)
        self.assertIn("trigger", required["required_dimensions"])
        relation["trigger"] = v2.unknown_term()
        result = v2.validate_operational_relations(plan, candidate)
        self.assertIn("operational_trigger_mismatch", [item["code"] for item in result["failures"]])

    def test_open_requirement_is_not_promoted_to_mandatory(self):
        plan = planner.analyse("Come deve comportarsi la squadra alla perdita?")
        projected = v2.project_relation_requirements(plan)
        self.assertTrue(projected)
        self.assertTrue(all(item["classification"] == "underspecified" for item in projected))
        candidate = v2.build_v2_plan(plan["state_contract"])
        result = v2.validate_operational_relations(plan, candidate)
        self.assertEqual(result["status"], "not_assessable")
        self.assertFalse(result["failures"])

    def test_ambiguous_requirement_is_unassessed(self):
        plan = question_plan()
        plan["relation_requirements"][0]["requirement_type"] = "ambiguous"
        projected = v2.project_relation_requirements(plan)
        self.assertEqual(projected[0]["classification"], "ambiguous")
        candidate = v2.build_v2_plan(plan["state_contract"])
        result = v2.validate_operational_relations(plan, candidate)
        self.assertEqual(result["status"], "not_assessable")
        self.assertFalse(result["failures"])

    def test_inferred_requirement_is_informational(self):
        plan = question_plan()
        plan["relation_requirements"][0]["requirement_type"] = "inferred"
        projected = v2.project_relation_requirements(plan)
        self.assertEqual(projected[0]["classification"], "inferred")
        candidate = v2.build_v2_plan(plan["state_contract"])
        result = v2.validate_operational_relations(plan, candidate)
        self.assertEqual(result["status"], "not_assessable")
        self.assertFalse(result["failures"])

    def test_actor_and_phase_mismatches_are_rejected(self):
        plan = question_plan()
        candidate, relation, _ = relation_fixture(plan)
        relation["actor_ref"] = {"id": "role:missing", "kind": "role_ref"}
        relation["phase_state_ref"] = {"id": "state:missing", "kind": "phase_state"}
        result = v2.validate_operational_relations(plan, candidate)
        codes = [item["code"] for item in result["failures"]]
        self.assertIn("operational_actor_mismatch", codes)
        self.assertIn("operational_phase_mismatch", codes)

    def test_duplicate_requirement_coverage_is_rejected(self):
        plan = question_plan()
        candidate, relation, _ = relation_fixture(plan)
        duplicate = deepcopy(relation)
        duplicate["relation_id"] = "relation:negative_transition:wing:1"
        candidate["operational_relations"].append(duplicate)
        result = v2.validate_operational_relations(plan, candidate)
        self.assertIn("duplicate_requirement_coverage", [item["code"] for item in result["failures"]])

    def test_unknown_requirement_reference_is_rejected(self):
        plan = question_plan()
        candidate, relation, _ = relation_fixture(plan)
        relation["requirement_ref"]["id"] = "question_part:missing"
        result = v2.validate_operational_relations(plan, candidate)
        self.assertIn("unknown_relation_requirement", [item["code"] for item in result["failures"]])


if __name__ == "__main__":
    unittest.main()
