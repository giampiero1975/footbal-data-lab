import importlib.util
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("contract", ROOT / "scripts/v5_tactical_state_contract_v1.py")
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)
planner_spec = importlib.util.spec_from_file_location("planner_with_contract", ROOT / "scripts/v5_tactical_query_plan_v1.py")
planner = importlib.util.module_from_spec(planner_spec)
planner_spec.loader.exec_module(planner)


class TacticalStateContractTests(unittest.TestCase):
    def test_analyse_is_the_single_planning_entrypoint(self):
        plan = planner.analyse("Nel 4-3-3 il numero 11 agisce da ala.")
        self.assertEqual(plan["state_contract"]["schema"], contract.SCHEMA)
        self.assertEqual(plan["state_contract"]["question"]["provenance"], "explicit")

    def test_explicit_player_is_not_formation_slot(self):
        plan = contract.build_question_plan("Nel 4-3-3 il numero 11 stringe dentro.", ["4-3-3"], ["ala"])
        self.assertEqual(plan["actors"][0]["kind"], "actor_ref")
        self.assertTrue(all(slot["kind"] == "position_slot" for slot in plan["position_slots"]))
        self.assertNotIn(plan["actors"][0]["id"], {slot["id"] for slot in plan["position_slots"]})

    def test_unknowns_are_not_promoted_to_facts(self):
        plan = contract.build_question_plan("Come modifichi il 4-3-3?", ["4-3-3"])
        self.assertEqual(plan["effective_players"], {"value": None, "provenance": "unknown"})
        self.assertEqual(plan["candidate_actors"], [])
        self.assertTrue(all("occupant" not in slot for slot in plan["position_slots"]))

    def test_coherent_substitution_preserves_cardinality(self):
        plan = contract.build_question_plan("Esce il numero 11 ed entra il numero 5. Siamo in 10.", [], [])
        validation = contract.validate_contract(plan)
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["effective_players_after_events"], 10)

    def test_exited_player_cannot_be_reused(self):
        plan = contract.build_question_plan("Il numero 11 e il numero 5.")
        plan["events"] = [
            {"id": "e1", "type": "substitution", "phase": "unknown", "out_actor": plan["actors"][1]["id"],
             "in_actor": plan["actors"][0]["id"], "cardinality_delta": 0, "provenance": "explicit"},
            {"id": "e2", "type": "rotation", "phase": "possession", "actor": plan["actors"][1]["id"],
             "cardinality_delta": 0, "provenance": "assumed"},
        ]
        validation = contract.validate_contract(plan)
        self.assertIn("invalid_rotation_actor", {item["code"] for item in validation["issues"]})
        self.assertFalse(validation["valid"])

    def test_rotation_does_not_change_cardinality(self):
        plan = contract.build_question_plan("Siamo in 10 e il numero 11 si abbassa.")
        validation = contract.validate_contract(plan)
        self.assertEqual(validation["effective_players_after_events"], 10)
        self.assertTrue(validation["valid"])

    def test_expulsion_reduces_known_cardinality(self):
        plan = contract.build_question_plan("Siamo in 10 e il numero 4 è in campo.")
        plan["events"] = [{"id": "e1", "type": "expulsion", "phase": "unknown",
                           "actor": plan["actors"][0]["id"], "cardinality_delta": -1,
                           "affects_current_count": True, "provenance": "explicit"}]
        validation = contract.validate_contract(plan)
        self.assertEqual(validation["effective_players_after_events"], 9)

    def test_roles_can_differ_between_phases(self):
        plan = contract.build_question_plan("Il numero 11 cambia compito.")
        actor = plan["actors"][0]["id"]
        plan["phase_states"] = [
            {"id": "p1", "phase": "possession", "assignments": [{"actor": actor, "slot": "lw"}]},
            {"id": "p2", "phase": "non_possession", "assignments": [{"actor": actor, "slot": "lm"}]},
        ]
        self.assertTrue(contract.validate_contract(plan)["valid"])

    def test_simultaneous_incompatible_assignments_are_blocking(self):
        plan = contract.build_question_plan("Il numero 11 cambia compito.")
        actor = plan["actors"][0]["id"]
        plan["phase_states"] = [{"id": "p1", "phase": "possession", "assignments": [
            {"actor": actor, "slot": "lw"}, {"actor": actor, "slot": "cf"}]}]
        validation = contract.validate_contract(plan)
        self.assertIn("simultaneous_incompatible_assignment", {i["code"] for i in validation["issues"]})

    def test_433_to_352_checks_relations_without_prescribing_solution(self):
        plan = contract.build_question_plan("Passo dal 4-3-3 al 3-5-2.", ["3-5-2", "4-3-3"])
        plan["final_formation"] = contract.value("3-5-2", "explicit")
        subjects = [slot["id"] for slot in plan["position_slots"] if ":4-3-3:" in slot["id"]]
        plan["phase_states"] = [{"id": "final", "phase": "possession", "formation": "3-5-2",
                                 "assignments": [{"subject": subject, "slot": slot}
                                                 for subject, slot in zip(subjects, contract.FORMATION_SLOTS["3-5-2"])]}]
        validation = contract.validate_contract(plan)
        self.assertTrue(validation["valid"])
        self.assertNotIn("incomplete_final_geometry", {i["code"] for i in validation["issues"]})

    def test_incomplete_formation_geometry_requires_qualification(self):
        plan = contract.build_question_plan("Passo dal 4-3-3 al 3-5-2.", ["3-5-2", "4-3-3"])
        plan["final_formation"] = contract.value("3-5-2", "explicit")
        subject = next(slot["id"] for slot in plan["position_slots"] if ":4-3-3:" in slot["id"])
        plan["phase_states"] = [{"id": "final", "phase": "possession", "formation": "3-5-2",
                                 "assignments": [{"subject": subject, "slot": "gk"}]}]
        validation = contract.validate_contract(plan)
        self.assertTrue(validation["valid"])
        self.assertIn("incomplete_final_geometry", {i["code"] for i in validation["issues"]})

    def test_safe_normalization_and_arbitrary_value_rejection(self):
        plan = contract.build_question_plan("Caso tattico.")
        plan["phase_states"] = [{"id": "p1", "phase": "non possesso", "assignments": []}]
        normalized, changes = contract.normalize_contract(plan)
        self.assertEqual(normalized["phase_states"][0]["phase"], "non_possession")
        self.assertEqual(changes[0]["rule_id"], "safe_phase_alias:v1")
        plan["phase_states"][0]["phase"] = "fase inventata"
        self.assertIn("invalid_phase", {i["code"] for i in contract.validate_contract(plan)["issues"]})

    def test_candidate_availability_is_qualified(self):
        plan = contract.build_question_plan("Serve un cambio.")
        plan["candidate_actors"] = [contract.entity("candidate:cb:1", "candidate_actor", "un centrale",
                                                             "assumed", availability="unknown")]
        validation = contract.validate_contract(plan)
        self.assertIn("candidate_availability_unknown", {i["code"] for i in validation["issues"]})
        self.assertTrue(validation["valid"])

    def test_partial_render_keeps_valid_facts_and_qualifies_error(self):
        plan = contract.build_question_plan("Nel 4-3-3 il numero 11 cambia ruolo.", ["4-3-3"])
        actor = plan["actors"][0]["id"]
        plan["phase_states"] = [{"id": "p", "phase": "possession", "assignments": [
            {"actor": actor, "slot": "lw"}, {"actor": actor, "slot": "cf"}]}]
        rendered = contract.render_validated_structure(plan)
        self.assertIn("Sistema dichiarato: 4-3-3", rendered)
        self.assertIn("Struttura non validabile integralmente", rendered)

    def test_renderer_does_not_add_players_or_availability(self):
        plan = contract.build_question_plan("Come modifichi il 4-3-3?", ["4-3-3"])
        rendered = contract.render_validated_structure(plan)
        self.assertNotIn("numero", rendered.casefold())
        self.assertNotIn("panchina", rendered.casefold())
        self.assertIn("posizioni astratte", rendered)

    def test_derived_values_require_rule_id(self):
        plan = contract.build_question_plan("Caso tattico.")
        plan["effective_players"] = contract.value(10, "derived")
        self.assertIn("derived_without_rule", {i["code"] for i in contract.validate_contract(plan)["issues"]})

    def test_trace_is_ready_without_creating_a_feedback_archive(self):
        trace = contract.build_question_plan("Caso tattico.")["trace"]
        self.assertEqual(set(trace), {"job_id", "response_sha256", "model_version", "contract_version",
                                     "classified_errors", "evaluation", "candidate_correction", "validated_correction"})
        self.assertEqual(trace["job_id"]["provenance"], "unknown")


if __name__ == "__main__":
    unittest.main()
