import importlib.util
import json
import sys
import types
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v1 = load("tsc_v1_generation_v2_tests", SCRIPTS / "v5_tactical_state_contract_v1.py")
v2 = load("tsc_v2_generation_v2_tests", SCRIPTS / "v5_tactical_state_contract_v2.py")
planner = load("tsc_planner_generation_v2_tests", SCRIPTS / "v5_tactical_query_plan_v1.py")
generation = load("tsc_generation_v2_tests", SCRIPTS / "v5_tactical_state_generation_v2.py")

QUESTION = "Alla perdita l'ala deve coprire il lato debole per evitare la ripartenza?"


def question_plan():
    return planner.analyse(QUESTION)


class TacticalStateGenerationV2Tests(unittest.TestCase):
    def test_explicit_negative_transition_materializes_valid_state(self):
        result = generation.prepare_generation_request(question_plan())
        self.assertEqual(result["status"], "ready")
        states = result["authorized_applied_plan"]["phase_states"]
        materialized = [s for s in states if s["phase"] == "negative_transition"]
        self.assertEqual(len(materialized), 1)
        self.assertEqual(materialized[0]["state_id"], "state:phase:negative_transition")
        self.assertTrue(result["validation"]["v1_structural_validation"]["valid"])

    def test_same_normative_input_has_same_state_id(self):
        first = generation.prepare_generation_request(question_plan())
        second = generation.prepare_generation_request(question_plan())
        self.assertEqual(first["mandatory_relations"][0]["phase_state_ref"],
                         second["mandatory_relations"][0]["phase_state_ref"])

    def test_compatible_requirements_share_one_phase_state(self):
        plan = question_plan()
        duplicate = deepcopy(plan["relation_requirements"][0])
        duplicate["requirement_id"] += ":second"
        duplicate["question_part_id"] += ":second"
        plan["relation_requirements"].append(duplicate)
        result = generation.prepare_generation_request(plan)
        self.assertEqual(result["status"], "ready")
        states = [s for s in result["authorized_applied_plan"]["phase_states"]
                  if s["phase"] == "negative_transition"]
        self.assertEqual(len(states), 1)
        self.assertEqual(len(result["mandatory_relations"]), 2)

    def test_ambiguous_phase_stops_before_transport(self):
        plan = question_plan()
        plan["relation_requirements"][0]["phase_terms"] = ["alla perdita", "fase aliena"]
        result = generation.prepare_generation_request(plan)
        self.assertEqual(result["status"], "not_evaluable")
        self.assertNotIn("authorized_applied_plan", result)

    def test_materialized_phase_reference_is_resolved(self):
        result = generation.prepare_generation_request(question_plan())
        coverage = v2.validate_operational_relations(
            question_plan(), result["authorized_applied_plan"])
        self.assertEqual(coverage["status"], "passed")

    def test_divergent_phase_is_fail_closed(self):
        result = generation.prepare_generation_request(question_plan())
        candidate = deepcopy(result["authorized_applied_plan"])
        target = result["mandatory_relations"][0]["phase_state_ref"]["id"]
        next(s for s in candidate["phase_states"] if s["state_id"] == target)["phase"] = "possession"
        self.assertEqual(v2.validate_operational_relations(question_plan(), candidate)["status"], "failed")

    def test_v1_invalid_materialization_is_not_promoted(self):
        plan = question_plan()
        plan["state_contract"]["phase_states"] = "invalid"
        result = generation.prepare_generation_request(plan)
        self.assertEqual(result["status"], "blocked")

    def test_question_plan_is_not_mutated(self):
        plan = question_plan()
        before = deepcopy(plan)
        generation.prepare_generation_request(plan)
        self.assertEqual(plan, before)

    def test_malformed_projection_is_zero_call_preflight(self):
        plan = question_plan()
        plan["relation_requirements"][0].pop("requirement_id")
        result = generation.prepare_generation_request(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertNotIn("authorized_applied_plan", result)

    def test_transport_schema_reuses_v2_relation_schema(self):
        schema = generation.generation_transport_schema()
        applied = schema["properties"]["applied_plan"]
        self.assertEqual(applied["properties"]["schema"]["const"], v2.SCHEMA)
        self.assertEqual(applied["properties"]["operational_relations"],
                         v2.operational_relation_schema())


class WrapperCompatibilityTests(unittest.TestCase):
    @staticmethod
    def _load_smoke():
        chromadb = types.ModuleType("chromadb")
        chromadb.PersistentClient = object
        sys.modules.setdefault("chromadb", chromadb)
        embeddings = types.ModuleType("llama_index.embeddings.ollama")
        embeddings.OllamaEmbedding = object
        sys.modules.setdefault("llama_index", types.ModuleType("llama_index"))
        sys.modules.setdefault("llama_index.embeddings", types.ModuleType("llama_index.embeddings"))
        sys.modules["llama_index.embeddings.ollama"] = embeddings
        transformers = types.ModuleType("sentence_transformers")
        transformers.CrossEncoder = object
        sys.modules.setdefault("sentence_transformers", transformers)
        return load("tsc_smoke_generation_v2_tests", SCRIPTS / "smoke_test_rag_v5_e2e.py")

    def test_v2_path_calls_transport_once_and_never_repairs(self):
        smoke = self._load_smoke()
        plan = question_plan()
        preflight = generation.prepare_generation_request(plan)
        relation = preflight["mandatory_relations"][0]
        phase = generation.applied_plan_state_phase(
            preflight["authorized_applied_plan"], relation["phase_state_ref"]["id"])
        explanation = "\n".join([
            f"[REL {relation['relation_id']}]", f"Attore: {relation['actor_ref']['id']}",
            f"Compito: {relation['task']['source_term']}",
            f"Spazio: {relation['space']['term']['source_term']}",
            f"Trigger: {relation['trigger']['source_term']}",
            f"Finalità: {relation['purpose']['source_term']}", f"Fase: {phase}",
            "Evidenze: [F1]",
        ])
        raw = json.dumps({"applied_plan": preflight["authorized_applied_plan"],
                          "explanation": explanation}, ensure_ascii=False)
        response = {"message": {"content": raw}, "done_reason": "stop"}
        evidence = [{"source": "fixture", "pages": [1], "text": "fixture"}]
        with patch.object(smoke, "_ollama_chat_once", return_value=response) as transport, \
             patch.object(smoke, "tactical_audit_answer", return_value={"status": "passed", "complete": True}):
            _, stats, _ = smoke.chat_tactical_state_v2_once(
                "mock", QUESTION, evidence, 1, plan)
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(stats["repair_reasons"], [])

    def test_default_profile_does_not_enable_v2(self):
        query = load("tsc_query_generation_v2_tests", SCRIPTS / "run_rag_v5_query.py")
        self.assertNotIn("--tactical-state-contract-v2", query.DEFAULT_PROFILE_FLAGS)

    def test_v1_diagnostic_cannot_satisfy_v2_requirement(self):
        query = load("tsc_query_generation_v2_tests_2", SCRIPTS / "run_rag_v5_query.py")
        report = {"index_unchanged": True, "questions": [{
            "tactical_state_contract": {"overall_status": "validated"},
            "invalid_citation_ids": [], "has_any_citation": True}]}
        with self.assertRaisesRegex(RuntimeError, "tactical_state_contract_v2_missing"):
            query.validate_report(report, require_tactical_state_contract_v2=True)


if __name__ == "__main__":
    unittest.main()
