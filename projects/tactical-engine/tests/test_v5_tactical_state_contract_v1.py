import importlib.util
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("contract", ROOT / "scripts/v5_tactical_state_contract_v1.py")
contract = importlib.util.module_from_spec(spec); spec.loader.exec_module(contract)
planner_spec = importlib.util.spec_from_file_location("planner_with_contract", ROOT / "scripts/v5_tactical_query_plan_v1.py")
planner = importlib.util.module_from_spec(planner_spec); planner_spec.loader.exec_module(planner)


def codes(validation, severity=None):
    return {item["code"] for item in validation["issues"] if severity is None or item["severity"] == severity}


def actors(plan):
    return {item["label"].split()[-1]: item["id"] for item in plan["actors"]}


def known_presence(actor_id, status):
    return contract.presence(contract.ref(actor_id, "actor_ref"), status, "explicit")


def substitution(out_id, in_id, source="s1", target="s2", mode="question_observation"):
    return {"event_id": "sub:1", "type": "substitution", "from_state_id": source, "to_state_id": target,
            "out_ref": contract.ref(out_id, "actor_ref"), "in_ref": contract.ref(in_id, "actor_ref"),
            "assertion_mode": mode, "cardinality_delta": 0, "provenance": "explicit"}


def rotation(actor_id, source="s1", target="s2"):
    return {"event_id": "rot:1", "type": "rotation", "from_state_id": source, "to_state_id": target,
            "subject_ref": contract.ref(actor_id, "actor_ref"), "movement": contract.value("si abbassa", "explicit"),
            "assertion_mode": "question_observation", "cardinality_delta": 0, "provenance": "explicit"}


class OriginalContractRegressionTests(unittest.TestCase):
    """The original 17 cases, adapted only where schema changes are intentional."""

    def test_analyse_is_the_single_planning_entrypoint(self):
        plan = planner.analyse("Nel 4-3-3 il numero 11 agisce da ala.")
        self.assertEqual(plan["state_contract"]["schema"], contract.SCHEMA)
        self.assertEqual(plan["state_contract"]["question"]["provenance"], "explicit")

    def test_explicit_player_is_not_formation_slot(self):
        plan = contract.build_question_plan("Nel 4-3-3 il numero 11 stringe dentro.", ["4-3-3"], ["ala"])
        self.assertEqual(plan["actors"][0]["kind"], "actor_ref")
        self.assertTrue(all(slot["kind"] == "position_slot" for slot in plan["position_slots"]))

    def test_unknowns_are_not_promoted_to_facts(self):
        plan = contract.build_question_plan("Come modifichi il 4-3-3?", ["4-3-3"])
        self.assertEqual(plan["effective_players"], {"value": None, "provenance": "unknown"})
        self.assertTrue(all(item["status"]["provenance"] == "unknown" for item in plan["phase_states"][0]["actor_presence"]))

    def test_coherent_substitution_preserves_cardinality(self):
        plan = contract.build_question_plan("Il numero 11 e il numero 5. Siamo in 10.")
        ids = actors(plan); plan["events"] = [substitution(ids["11"], ids["5"])]
        plan["phase_states"] = [
            contract.state("s1", actor_presence=[known_presence(ids["11"], "on_field"), known_presence(ids["5"], "off_field")], effective_players=contract.value(10, "explicit")),
            contract.state("s2", actor_presence=[known_presence(ids["11"], "off_field"), known_presence(ids["5"], "on_field")], effective_players=contract.value(10, "explicit"))]
        self.assertTrue(contract.validate_contract(plan)["valid"])

    def test_exited_player_cannot_be_reused(self):
        plan = contract.build_question_plan("Il numero 11 e il numero 5."); ids = actors(plan)
        plan["substitution_mode"] = contract.value("standard_no_reentry", "explicit")
        first = substitution(ids["11"], ids["5"]); second = substitution(ids["5"], ids["11"], "s2", "s3")
        second["event_id"] = "sub:2"; plan["events"] = [first, second]
        plan["phase_states"] = [
            contract.state("s1", actor_presence=[known_presence(ids["11"], "on_field"), known_presence(ids["5"], "off_field")]),
            contract.state("s2", actor_presence=[known_presence(ids["11"], "off_field"), known_presence(ids["5"], "on_field")]),
            contract.state("s3", actor_presence=[known_presence(ids["11"], "on_field"), known_presence(ids["5"], "off_field")])]
        self.assertIn("actor_reentry", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_rotation_does_not_change_cardinality(self):
        plan = contract.build_question_plan("Siamo in 10 e il numero 11 si abbassa."); actor = actors(plan)["11"]
        plan["events"] = [rotation(actor)]
        plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(actor, "on_field")], effective_players=contract.value(10, "explicit")),
                                contract.state("s2", actor_presence=[known_presence(actor, "on_field")], effective_players=contract.value(10, "explicit"))]
        self.assertTrue(contract.validate_contract(plan)["valid"])

    def test_expulsion_reduces_known_cardinality(self):
        plan = contract.build_question_plan("Siamo in 10 e il numero 4 è in campo."); actor = actors(plan)["4"]
        plan["events"] = [{"event_id": "red:1", "type": "expulsion", "from_state_id": "s1", "to_state_id": "s2",
                           "subject_ref": contract.ref(actor, "actor_ref"), "team": contract.value("own", "explicit"),
                           "temporal_relation": contract.value("between_states", "explicit"), "assertion_mode": "question_observation",
                           "cardinality_delta": -1, "provenance": "explicit"}]
        plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(actor, "on_field")], effective_players=contract.value(10, "explicit")),
                                contract.state("s2", actor_presence=[known_presence(actor, "unavailable")], effective_players=contract.value(9, "explicit"))]
        self.assertTrue(contract.validate_contract(plan)["valid"])

    def test_roles_can_differ_between_phases(self):
        plan = contract.build_question_plan("Il numero 11 cambia compito.", ["4-3-3"]); actor = actors(plan)["11"]
        lw = next(x["id"] for x in plan["position_slots"] if x["label"] == "lw")
        plan["phase_states"] = [contract.state("s1", phase="possession", actor_presence=[known_presence(actor, "on_field")],
                                                       assignments=[{"subject_ref": contract.ref(actor, "actor_ref"), "position_ref": contract.ref(lw, "position_slot"), "provenance": "explicit"}]),
                                contract.state("s2", phase="non_possession", actor_presence=[known_presence(actor, "on_field")])]
        self.assertTrue(contract.validate_contract(plan)["valid"])

    def test_simultaneous_incompatible_assignments_are_blocking(self):
        plan = contract.build_question_plan("Il numero 11 cambia compito.", ["4-3-3"]); actor = actors(plan)["11"]
        slots = plan["position_slots"][:2]
        plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(actor, "on_field")], assignments=[
            {"subject_ref": contract.ref(actor, "actor_ref"), "position_ref": contract.ref(slots[0]["id"], "position_slot"), "provenance": "explicit"},
            {"subject_ref": contract.ref(actor, "actor_ref"), "position_ref": contract.ref(slots[1]["id"], "position_slot"), "provenance": "explicit"}])]
        self.assertIn("duplicate_actor_assignment", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_433_to_352_checks_relations_without_prescribing_solution(self):
        plan = contract.build_question_plan("Passo dal 4-3-3 al 3-5-2.", ["4-3-3", "3-5-2"])
        sources = [x for x in plan["position_slots"] if ":4-3-3:" in x["id"]]; targets = [x for x in plan["position_slots"] if ":3-5-2:" in x["id"]]
        plan["final_formation"] = contract.value("3-5-2", "explicit")
        plan["structural_mappings"] = [{"from_slot_ref": contract.ref(a["id"], "position_slot"), "to_slot_ref": contract.ref(b["id"], "position_slot"), "provenance": "explicit"} for a, b in zip(sources, targets)]
        self.assertTrue(contract.validate_contract(plan)["valid"])

    def test_incomplete_formation_geometry_requires_qualification(self):
        plan = contract.build_question_plan("Passo dal 4-3-3 al 3-5-2.", ["4-3-3", "3-5-2"])
        source = next(x for x in plan["position_slots"] if ":4-3-3:" in x["id"]); target = next(x for x in plan["position_slots"] if ":3-5-2:" in x["id"])
        plan["final_formation"] = contract.value("3-5-2", "explicit")
        plan["structural_mappings"] = [{"from_slot_ref": contract.ref(source["id"], "position_slot"), "to_slot_ref": contract.ref(target["id"], "position_slot"), "provenance": "explicit"}]
        self.assertIn("incomplete_final_geometry", codes(contract.validate_contract(plan), "QUALIFICATION_REQUIRED"))

    def test_safe_normalization_and_arbitrary_value_rejection(self):
        plan = contract.build_question_plan("Caso tattico."); plan["phase_states"][0]["phase"] = "non possesso"
        normalized, changes = contract.normalize_contract(plan)
        self.assertEqual(normalized["phase_states"][0]["phase"], "non_possession"); self.assertTrue(changes)
        plan["phase_states"][0]["phase"] = "fase inventata"
        self.assertIn("invalid_phase", codes(contract.validate_contract(plan)))

    def test_candidate_availability_is_qualified(self):
        plan = contract.build_question_plan("Serve un cambio.")
        plan["candidate_actors"] = [contract.entity("candidate:cb:1", "candidate_actor", "un centrale", "assumed")]
        self.assertIn("candidate_availability_unknown", codes(contract.validate_contract(plan), "QUALIFICATION_REQUIRED"))

    def test_partial_render_keeps_valid_facts_and_qualifies_error(self):
        plan = contract.build_question_plan("Nel 4-3-3 il numero 11 cambia ruolo.", ["4-3-3"])
        plan["events"] = [{"event_id": "bad", "type": "rotation", "from_state_id": None, "to_state_id": None,
                           "subject_ref": contract.ref(actors(plan)["11"], "actor_ref"), "movement": contract.value("si alza", "explicit"),
                           "assertion_mode": "executable", "cardinality_delta": 0, "provenance": "explicit"}]
        rendered = contract.render_validated_structure(plan)
        self.assertTrue(rendered.startswith("ELEMENTI BLOCCATI")); self.assertIn("Sistemi dichiarati: 4-3-3", rendered)

    def test_renderer_does_not_add_players_or_availability(self):
        rendered = contract.render_validated_structure(contract.build_question_plan("Come modifichi il 4-3-3?", ["4-3-3"]))
        self.assertNotIn("panchina", rendered.casefold()); self.assertIn("posizioni astratte", rendered)

    def test_derived_values_require_rule_id(self):
        plan = contract.build_question_plan("Caso tattico."); plan["effective_players"] = contract.value(10, "derived")
        self.assertIn("derived_without_rule", codes(contract.validate_contract(plan)))

    def test_trace_is_ready_without_creating_a_feedback_archive(self):
        trace = contract.build_question_plan("Caso tattico.")["trace"]
        self.assertEqual(trace["job_id"]["provenance"], "unknown")


class DifferentialCorrectionTests(unittest.TestCase):
    def setUp(self):
        self.plan = contract.build_question_plan("Il numero 11 e il numero 5.")
        self.ids = actors(self.plan); self.plan["events"] = []

    def test_01_mentioned_actor_stays_unknown(self):
        self.assertEqual(self.plan["phase_states"][0]["actor_presence"][0]["status"]["provenance"], "unknown")

    def test_02_outgoing_proven_off_field_blocks(self):
        self.plan["events"] = [substitution(self.ids["11"], self.ids["5"])]
        self.plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(self.ids["11"], "off_field"), known_presence(self.ids["5"], "off_field")]),
                                     contract.state("s2", actor_presence=[known_presence(self.ids["11"], "off_field"), known_presence(self.ids["5"], "on_field")])]
        self.assertIn("outgoing_not_on_field", codes(contract.validate_contract(self.plan), "BLOCKING"))

    def test_03_incoming_already_on_field_blocks(self):
        self.plan["events"] = [substitution(self.ids["11"], self.ids["5"])]
        self.plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(self.ids["11"], "on_field"), known_presence(self.ids["5"], "on_field")]),
                                     contract.state("s2", actor_presence=[known_presence(self.ids["11"], "off_field"), known_presence(self.ids["5"], "on_field")])]
        self.assertIn("incoming_not_off_field", codes(contract.validate_contract(self.plan), "BLOCKING"))

    def test_04_unknown_precondition_is_qualified(self):
        self.plan["events"] = [substitution(self.ids["11"], self.ids["5"])]
        self.plan["phase_states"] = [contract.state("s1"), contract.state("s2")]
        self.assertIn("outgoing_not_on_field_unknown", codes(contract.validate_contract(self.plan), "QUALIFICATION_REQUIRED"))

    def test_05_unknown_precondition_executable_blocks(self):
        self.plan["events"] = [substitution(self.ids["11"], self.ids["5"], mode="executable")]
        self.plan["phase_states"] = [contract.state("s1"), contract.state("s2")]
        self.assertIn("outgoing_not_on_field_unknown", codes(contract.validate_contract(self.plan), "BLOCKING"))

    def test_06_same_phase_successive_states_are_allowed(self):
        actor = self.ids["11"]
        self.plan["phase_states"] = [contract.state("s1", phase="possession", actor_presence=[known_presence(actor, "on_field")]),
                                     contract.state("s2", phase="possession", actor_presence=[known_presence(actor, "on_field")])]
        self.assertTrue(contract.validate_contract(self.plan)["valid"])

    def test_07_reverse_sequence_blocks(self):
        actor = self.ids["11"]; self.plan["events"] = [rotation(actor)]
        self.plan["phase_states"] = [contract.state("s1", 2, "explicit", actor_presence=[known_presence(actor, "on_field")]),
                                     contract.state("s2", 1, "explicit", actor_presence=[known_presence(actor, "on_field")])]
        self.assertIn("non_increasing_timeline", codes(contract.validate_contract(self.plan), "BLOCKING"))

    def test_08_cycle_blocks(self):
        actor = self.ids["11"]; one = rotation(actor); two = rotation(actor, "s2", "s1"); two["event_id"] = "rot:2"
        self.plan["events"] = [one, two]
        self.plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(actor, "on_field")]), contract.state("s2", actor_presence=[known_presence(actor, "on_field")])]
        self.assertIn("timeline_cycle", codes(contract.validate_contract(self.plan), "BLOCKING"))

    def test_09_unordered_event_is_not_invented(self):
        event = substitution(self.ids["11"], self.ids["5"], None, None); self.plan["events"] = [event]
        self.assertIn("event_temporality_unknown", codes(contract.validate_contract(self.plan), "QUALIFICATION_REQUIRED"))

    def test_10_subject_kind_mismatch_blocks(self):
        plan = contract.build_question_plan("Il numero 11 nel 4-3-3.", ["4-3-3"]); actor = actors(plan)["11"]; slot = plan["position_slots"][0]["id"]
        plan["phase_states"][0]["assignments"] = [{"subject_ref": contract.ref(actor, "position_slot"), "position_ref": contract.ref(slot, "position_slot"), "provenance": "explicit"}]
        self.assertIn("reference_kind_mismatch", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_11_slot_cannot_be_concrete_actor(self):
        plan = contract.build_question_plan("4-3-3.", ["4-3-3"]); slot = plan["position_slots"][0]["id"]
        plan["phase_states"][0]["assignments"] = [{"subject_ref": contract.ref(slot, "position_slot"), "position_ref": contract.ref(slot, "position_slot"), "provenance": "explicit"}]
        self.assertIn("reference_kind_not_allowed", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_12_duplicate_actor_in_final_state_blocks(self):
        plan = contract.build_question_plan("Il numero 11 nel 3-5-2.", ["3-5-2"]); actor = actors(plan)["11"]; slots = plan["position_slots"][:2]
        plan["phase_states"] = [contract.state("final", actor_presence=[known_presence(actor, "on_field")], assignments=[
            {"subject_ref": contract.ref(actor, "actor_ref"), "position_ref": contract.ref(slots[0]["id"], "position_slot"), "provenance": "explicit"},
            {"subject_ref": contract.ref(actor, "actor_ref"), "position_ref": contract.ref(slots[1]["id"], "position_slot"), "provenance": "explicit"}])]
        self.assertIn("duplicate_actor_assignment", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_13_complete_membership_detects_lost_actor(self):
        self.plan["events"] = [rotation(self.ids["11"])]
        self.plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(self.ids["11"], "on_field"), known_presence(self.ids["5"], "on_field")], presence_complete=True),
                                     contract.state("s2", actor_presence=[known_presence(self.ids["11"], "on_field"), known_presence(self.ids["5"], "off_field")], presence_complete=True)]
        self.assertIn("actor_continuity_mismatch", codes(contract.validate_contract(self.plan), "BLOCKING"))

    def test_14_complete_membership_detects_unjustified_entrant(self):
        self.plan["events"] = [rotation(self.ids["11"])]
        self.plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(self.ids["11"], "on_field"), known_presence(self.ids["5"], "off_field")], presence_complete=True),
                                     contract.state("s2", actor_presence=[known_presence(self.ids["11"], "on_field"), known_presence(self.ids["5"], "on_field")], presence_complete=True)]
        self.assertIn("actor_continuity_mismatch", codes(contract.validate_contract(self.plan), "BLOCKING"))

    def test_15_derived_nested_entity_requires_rule(self):
        self.plan["actors"][0]["provenance"] = "derived"; self.plan["actors"][0].pop("rule_id", None)
        self.assertIn("derived_without_rule", codes(contract.validate_contract(self.plan), "BLOCKING"))

    def test_16_derived_nested_assignment_requires_rule(self):
        plan = contract.build_question_plan("Il numero 11 nel 4-3-3.", ["4-3-3"]); actor = actors(plan)["11"]; slot = plan["position_slots"][0]["id"]
        plan["phase_states"][0]["assignments"] = [{"subject_ref": contract.ref(actor, "actor_ref"), "position_ref": contract.ref(slot, "position_slot"), "provenance": "derived"}]
        self.assertIn("derived_without_rule", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_17_opponent_expulsion_preserves_own_count(self):
        actor = self.ids["11"]
        self.plan["events"] = [{"event_id": "red", "type": "expulsion", "from_state_id": "s1", "to_state_id": "s2", "subject_ref": contract.ref(actor, "actor_ref"), "team": contract.value("opponent", "explicit"), "temporal_relation": contract.value("between_states", "explicit"), "assertion_mode": "question_observation", "cardinality_delta": -1, "provenance": "explicit"}]
        self.plan["phase_states"] = [contract.state("s1", effective_players=contract.value(10, "explicit")), contract.state("s2", effective_players=contract.value(10, "explicit"))]
        self.assertNotIn("cardinality_mismatch", codes(contract.validate_contract(self.plan)))

    def test_18_unknown_expulsion_team_is_qualified(self):
        plan = contract.build_question_plan("Espulso il numero 11."); validation = contract.validate_contract(plan)
        self.assertIn("expulsion_team_unknown", codes(validation, "QUALIFICATION_REQUIRED"))

    def test_19_own_expulsion_decrements_once(self):
        actor = self.ids["11"]
        self.plan["events"] = [{"event_id": "red", "type": "expulsion", "from_state_id": "s1", "to_state_id": "s2", "subject_ref": contract.ref(actor, "actor_ref"), "team": contract.value("own", "explicit"), "temporal_relation": contract.value("between_states", "explicit"), "assertion_mode": "question_observation", "cardinality_delta": -1, "provenance": "explicit"}]
        self.plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(actor, "on_field")], effective_players=contract.value(10, "explicit")), contract.state("s2", actor_presence=[known_presence(actor, "unavailable")], effective_players=contract.value(9, "explicit"))]
        self.assertNotIn("cardinality_mismatch", codes(contract.validate_contract(self.plan)))

    def test_20_wrong_expulsion_count_blocks(self):
        self.test_19_own_expulsion_decrements_once()
        self.plan["phase_states"][1]["effective_players"] = contract.value(8, "explicit")
        self.assertIn("cardinality_mismatch", codes(contract.validate_contract(self.plan), "BLOCKING"))

    def test_21_renderer_omits_blocked_event(self):
        self.plan["events"] = [substitution(self.ids["11"], self.ids["5"], None, None, "executable")]
        rendered = contract.render_validated_structure(self.plan)
        self.assertTrue(rendered.startswith("ELEMENTI BLOCCATI")); self.assertNotIn("Sostituzione:", rendered)

    def test_22_renderer_keeps_independent_fact(self):
        plan = contract.build_question_plan("Nel 4-3-3 esce il numero 11 ed entra il numero 5.", ["4-3-3"])
        plan["events"][0]["assertion_mode"] = "executable"
        rendered = contract.render_validated_structure(plan)
        self.assertIn("Sistemi dichiarati: 4-3-3", rendered); self.assertNotIn("Sostituzione:", rendered)

    def test_23_abstract_433_to_352_is_valid_without_players(self):
        plan = contract.build_question_plan("Dal 4-3-3 al 3-5-2.", ["4-3-3", "3-5-2"])
        sources = [x for x in plan["position_slots"] if ":4-3-3:" in x["id"]]; targets = [x for x in plan["position_slots"] if ":3-5-2:" in x["id"]]
        plan["final_formation"] = contract.value("3-5-2", "explicit")
        plan["structural_mappings"] = [{"from_slot_ref": contract.ref(a["id"], "position_slot"), "to_slot_ref": contract.ref(b["id"], "position_slot"), "provenance": "explicit"} for a, b in zip(sources, targets)]
        self.assertTrue(contract.validate_contract(plan)["valid"])

    def test_24_complete_concrete_transition_is_valid(self):
        question = "Dal 4-3-3 al 3-5-2 con " + ", ".join(f"numero {number}" for number in range(1, 12))
        plan = contract.build_question_plan(question, ["4-3-3", "3-5-2"])
        actor_ids = [item["id"] for item in plan["actors"]]
        source_slots = [item for item in plan["position_slots"] if ":4-3-3:" in item["id"]]
        target_slots = [item for item in plan["position_slots"] if ":3-5-2:" in item["id"]]
        before_presence = [known_presence(actor, "on_field") for actor in actor_ids]
        after_presence = [known_presence(actor, "on_field") for actor in actor_ids]
        before_assignments = [{"subject_ref": contract.ref(actor, "actor_ref"),
                               "position_ref": contract.ref(slot["id"], "position_slot"),
                               "provenance": "explicit"} for actor, slot in zip(actor_ids, source_slots)]
        after_assignments = [{"subject_ref": contract.ref(actor, "actor_ref"),
                              "position_ref": contract.ref(slot["id"], "position_slot"),
                              "provenance": "explicit"} for actor, slot in zip(actor_ids, target_slots)]
        plan["events"] = [rotation(actor_ids[0])]
        plan["phase_states"] = [
            contract.state("s1", phase="possession", actor_presence=before_presence,
                           assignments=before_assignments, formation=contract.value("4-3-3", "explicit"),
                           effective_players=contract.value(11, "explicit"), presence_complete=True),
            contract.state("s2", phase="possession", actor_presence=after_presence,
                           assignments=after_assignments, formation=contract.value("3-5-2", "explicit"),
                           effective_players=contract.value(11, "explicit"), presence_complete=True)]
        self.assertTrue(contract.validate_contract(plan)["valid"])


class ConsolidatedRemediationTests(unittest.TestCase):
    """Seven non-equivalent cases found after the v1.1 independent review."""

    def test_25_two_own_expulsions_aggregate_transition_delta(self):
        plan = contract.build_question_plan("Numero 4 e numero 5 espulsi.")
        ids = actors(plan)
        plan["actors"][0]["team"] = contract.value("own", "explicit")
        plan["actors"][1]["team"] = contract.value("own", "explicit")
        plan["events"] = []
        for index, actor in enumerate((ids["4"], ids["5"]), 1):
            plan["events"].append({"event_id": f"red:{index}", "type": "expulsion",
                "from_state_id": "s1", "to_state_id": "s2",
                "subject_ref": contract.ref(actor, "actor_ref"),
                "team": contract.value("own", "explicit"),
                "temporal_relation": contract.value("between_states", "explicit"),
                "assertion_mode": "question_observation", "cardinality_delta": -1,
                "provenance": "explicit"})
        plan["phase_states"] = [
            contract.state("s1", actor_presence=[known_presence(ids["4"], "on_field"), known_presence(ids["5"], "on_field")],
                           effective_players=contract.value(11, "explicit")),
            contract.state("s2", actor_presence=[known_presence(ids["4"], "unavailable"), known_presence(ids["5"], "unavailable")],
                           effective_players=contract.value(9, "explicit"))]
        self.assertNotIn("cardinality_mismatch", codes(contract.validate_contract(plan)))

    def test_26_reentry_is_independent_of_event_serialization(self):
        plan = contract.build_question_plan("Numero 11 e numero 5.")
        ids = actors(plan); plan["substitution_mode"] = contract.value("standard_no_reentry", "explicit")
        first = substitution(ids["11"], ids["5"], "s1", "s2")
        second = substitution(ids["5"], ids["11"], "s2", "s3"); second["event_id"] = "sub:2"
        plan["events"] = [second, first]
        plan["phase_states"] = [
            contract.state("s1", actor_presence=[known_presence(ids["11"], "on_field"), known_presence(ids["5"], "off_field")]),
            contract.state("s2", actor_presence=[known_presence(ids["11"], "off_field"), known_presence(ids["5"], "on_field")]),
            contract.state("s3", actor_presence=[known_presence(ids["11"], "on_field"), known_presence(ids["5"], "off_field")])]
        self.assertIn("actor_reentry", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_27_global_cycle_hides_involved_events_from_renderer(self):
        plan = contract.build_question_plan("Numero 11 si abbassa.")
        actor = actors(plan)["11"]
        first = rotation(actor, "s1", "s2")
        second = rotation(actor, "s2", "s1"); second["event_id"] = "rot:2"
        plan["events"] = [first, second]
        plan["phase_states"] = [
            contract.state("s1", actor_presence=[known_presence(actor, "on_field")]),
            contract.state("s2", actor_presence=[known_presence(actor, "on_field")])]
        rendered = contract.render_validated_structure(plan)
        self.assertIn("Timeline ciclica", rendered)
        self.assertNotIn("Rotazione:", rendered)

    def test_28_edge_to_missing_state_returns_structured_issue(self):
        plan = contract.build_question_plan("Numero 11 si abbassa.")
        actor = actors(plan)["11"]
        plan["events"] = [rotation(actor, "state:initial", "missing")]
        validation = contract.validate_contract(plan)
        self.assertIn("invalid_event_edge", codes(validation, "BLOCKING"))

    def test_29_bare_numbers_in_substitution_are_registered(self):
        plan = contract.build_question_plan("Esce il 7, entra il 9.")
        self.assertEqual({item["label"] for item in plan["actors"]}, {"numero 7", "numero 9"})
        self.assertEqual(len(plan["events"]), 1)
        self.assertNotIn("unknown_reference", codes(contract.validate_contract(plan)))

    def test_30_complete_presence_must_match_cardinality(self):
        plan = contract.build_question_plan("Numero 11, siamo in 10.")
        actor = actors(plan)["11"]
        plan["phase_states"] = [contract.state("s1", actor_presence=[known_presence(actor, "on_field")],
                                               effective_players=contract.value(10, "explicit"), presence_complete=True)]
        self.assertIn("complete_presence_cardinality_mismatch", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_31_concrete_assignment_must_follow_declared_mapping(self):
        plan = contract.build_question_plan("Numero 11, dal 4-3-3 al 3-5-2.", ["4-3-3", "3-5-2"])
        actor = actors(plan)["11"]
        source = next(item for item in plan["position_slots"] if item["id"].endswith(":lw"))
        correct_target = next(item for item in plan["position_slots"] if item["id"].endswith(":lf"))
        wrong_target = next(item for item in plan["position_slots"] if item["id"].endswith(":rf"))
        plan["structural_mappings"] = [{"from_slot_ref": contract.ref(source["id"], "position_slot"),
                                        "to_slot_ref": contract.ref(correct_target["id"], "position_slot"),
                                        "provenance": "explicit"}]
        plan["events"] = [rotation(actor, "s1", "s2")]
        plan["phase_states"] = [
            contract.state("s1", actor_presence=[known_presence(actor, "on_field")], presence_complete=True,
                           effective_players=contract.value(1, "explicit"), assignments=[{
                               "subject_ref": contract.ref(actor, "actor_ref"),
                               "position_ref": contract.ref(source["id"], "position_slot"), "provenance": "explicit"}]),
            contract.state("s2", actor_presence=[known_presence(actor, "on_field")], presence_complete=True,
                           effective_players=contract.value(1, "explicit"), assignments=[{
                               "subject_ref": contract.ref(actor, "actor_ref"),
                               "position_ref": contract.ref(wrong_target["id"], "position_slot"), "provenance": "explicit"}])]
        self.assertIn("assignment_mapping_mismatch", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_32_partial_presence_does_not_hide_concrete_mapping_contradiction(self):
        plan = contract.build_question_plan("Numero 11, dal 4-3-3 al 3-5-2.", ["4-3-3", "3-5-2"])
        actor = actors(plan)["11"]
        source = next(item for item in plan["position_slots"] if item["id"].endswith(":lw"))
        correct_target = next(item for item in plan["position_slots"] if item["id"].endswith(":lf"))
        wrong_target = next(item for item in plan["position_slots"] if item["id"].endswith(":rf"))
        plan["structural_mappings"] = [{"from_slot_ref": contract.ref(source["id"], "position_slot"),
                                        "to_slot_ref": contract.ref(correct_target["id"], "position_slot"),
                                        "provenance": "explicit"}]
        plan["events"] = [rotation(actor, "s1", "s2")]
        plan["phase_states"] = [
            contract.state("s1", actor_presence=[known_presence(actor, "on_field")], assignments=[{
                "subject_ref": contract.ref(actor, "actor_ref"),
                "position_ref": contract.ref(source["id"], "position_slot"), "provenance": "explicit"}]),
            contract.state("s2", actor_presence=[known_presence(actor, "on_field")], assignments=[{
                "subject_ref": contract.ref(actor, "actor_ref"),
                "position_ref": contract.ref(wrong_target["id"], "position_slot"), "provenance": "explicit"}])]
        self.assertIn("assignment_mapping_mismatch", codes(contract.validate_contract(plan), "BLOCKING"))

    def test_33_unordered_possible_reentry_is_qualified_not_invented(self):
        plan = contract.build_question_plan("Numero 11 e numero 5.")
        ids = actors(plan); plan["substitution_mode"] = contract.value("standard_no_reentry", "explicit")
        first = substitution(ids["11"], ids["5"], "s1", "s2")
        second = substitution(ids["5"], ids["11"], "s3", "s4"); second["event_id"] = "sub:2"
        plan["events"] = [first, second]
        plan["phase_states"] = [contract.state(name) for name in ("s1", "s2", "s3", "s4")]
        validation = contract.validate_contract(plan)
        self.assertNotIn("actor_reentry", codes(validation, "BLOCKING"))
        self.assertIn("actor_reentry_order_unknown", codes(validation, "QUALIFICATION_REQUIRED"))


if __name__ == "__main__":
    unittest.main()
