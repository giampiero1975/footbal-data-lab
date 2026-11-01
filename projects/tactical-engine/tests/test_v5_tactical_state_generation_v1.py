import importlib.util
import json
import sys
import types
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contract = load("tsc_generation_contract", SCRIPTS / "v5_tactical_state_contract_v1.py")
query = load("tsc_generation_query", SCRIPTS / "run_rag_v5_query.py")


def applied_plan(question="Come organizzi il 4-3-3?"):
    return contract.build_question_plan(question, ["4-3-3"])


def envelope(plan=None, explanation="Nel 4-3-3 mantengo equilibrio e copertura [F1]."):
    return json.dumps({"applied_plan": plan or applied_plan(), "explanation": explanation}, ensure_ascii=False)


def complete_audit():
    return {"complete": True, "missing_facets": [], "missing_operational": [],
            "missing_details": [], "semantic_issues": []}


class ContractGenerationTests(unittest.TestCase):
    def test_transport_reuses_domain_schema(self):
        schema = contract.generation_transport_schema()
        self.assertEqual(schema["properties"]["applied_plan"]["properties"]["schema"]["const"], contract.SCHEMA)
        self.assertEqual(set(schema["required"]), {"applied_plan", "explanation"})
        self.assertIn("phase_states", schema["properties"]["applied_plan"]["required"])

    def test_json_fence_is_representation_only_normalization(self):
        parsed, changes, errors = contract.parse_generation_content("```json\n" + envelope() + "\n```")
        self.assertFalse(errors)
        self.assertEqual(parsed["applied_plan"]["schema"], contract.SCHEMA)
        self.assertEqual(changes[0]["rule_id"], "strip_outer_json_fence:v1")

    def test_malformed_json_is_not_evaluable_and_raw_is_kept(self):
        diagnostic = contract.generation_diagnostic(applied_plan(), "{broken")
        self.assertEqual(diagnostic["overall_status"], "not_evaluable")
        self.assertEqual(diagnostic["promoted_answer"], "")
        self.assertEqual(diagnostic["raw_model_content"], "{broken")

    def test_malformed_contract_shape_is_not_evaluable(self):
        plan = applied_plan()
        plan["actors"] = "not-an-array"
        diagnostic = contract.generation_diagnostic(applied_plan(), envelope(plan), tactical_audit=complete_audit())
        self.assertEqual(diagnostic["overall_status"], "not_evaluable")
        self.assertIn("invalid_contract_shape", diagnostic["reasons"])

    def test_normalization_never_changes_actor_or_event_content(self):
        plan = applied_plan("Nel 4-3-3 il numero 11 stringe.")
        before_actors, before_events = deepcopy(plan["actors"]), deepcopy(plan["events"])
        plan["phase_states"][0]["phase"] = "non possesso"
        normalized, changes = contract.normalize_contract(plan)
        self.assertEqual(normalized["actors"], before_actors)
        self.assertEqual(normalized["events"], before_events)
        self.assertEqual(changes[0]["rule_id"], "safe_phase_alias:v1")

    def test_incomplete_plan_is_blocked(self):
        plan = applied_plan()
        del plan["phase_states"]
        diagnostic = contract.generation_diagnostic(applied_plan(), envelope(plan), tactical_audit=complete_audit())
        self.assertEqual(diagnostic["overall_status"], "blocked")
        self.assertIn("question_compatibility", diagnostic["failed_scope"])
        self.assertEqual(diagnostic["promoted_answer"], "")

    def test_structural_contradiction_is_blocked(self):
        plan = applied_plan("Nel 4-3-3 il numero 11 stringe.")
        plan["actors"].append(deepcopy(plan["actors"][0]))
        diagnostic = contract.generation_diagnostic(plan, envelope(plan), tactical_audit=complete_audit())
        self.assertEqual(diagnostic["overall_status"], "blocked")
        self.assertIn("structural_validity", diagnostic["failed_scope"])

    def test_question_plan_mismatch_is_distinct(self):
        question = applied_plan()
        candidate = contract.build_question_plan("Come organizzi il 3-5-2?", ["3-5-2"])
        diagnostic = contract.generation_diagnostic(question, envelope(candidate, "Nel 3-5-2 proteggo il centro [F1]."), tactical_audit=complete_audit())
        self.assertEqual(diagnostic["controls"]["question_compatibility"]["status"], "failed")
        self.assertEqual(diagnostic["overall_status"], "blocked")

    def test_prose_formation_mismatch_is_distinct(self):
        plan = applied_plan()
        diagnostic = contract.generation_diagnostic(plan, envelope(plan, "Nel 3-5-2 proteggo il centro [F1]."), tactical_audit=complete_audit())
        self.assertEqual(diagnostic["controls"]["plan_prose_alignment"]["status"], "failed")
        self.assertEqual(diagnostic["promoted_answer"], "")

    def test_truncation_is_not_evaluable(self):
        diagnostic = contract.generation_diagnostic(applied_plan(), envelope(), done_reason="length", tactical_audit=complete_audit())
        self.assertEqual(diagnostic["overall_status"], "not_evaluable")
        self.assertIn("generation_truncated", diagnostic["reasons"])

    def test_audit_failure_does_not_hide_other_passes(self):
        audit = {"complete": False, "missing_facets": ["transition"], "missing_operational": [],
                 "missing_details": [], "semantic_issues": []}
        diagnostic = contract.generation_diagnostic(applied_plan(), envelope(), tactical_audit=audit)
        self.assertEqual(diagnostic["overall_status"], "blocked")
        self.assertIn("structural_validity", diagnostic["passed_scope"])
        self.assertIn("tactical_documentary_audit", diagnostic["failed_scope"])

    def test_validated_promotes_only_explanation(self):
        diagnostic = contract.generation_diagnostic(applied_plan(), envelope(), tactical_audit=complete_audit())
        self.assertEqual(diagnostic["overall_status"], "validated")
        self.assertEqual(diagnostic["promoted_answer"], "Nel 4-3-3 mantengo equilibrio e copertura [F1].")


class SingleCallPathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if "chromadb" not in sys.modules:
            sys.modules["chromadb"] = types.ModuleType("chromadb")
        if "llama_index" not in sys.modules:
            llama_index = types.ModuleType("llama_index")
            embeddings = types.ModuleType("llama_index.embeddings")
            ollama = types.ModuleType("llama_index.embeddings.ollama")
            ollama.OllamaEmbedding = type("OllamaEmbedding", (), {})
            sys.modules.update({"llama_index": llama_index,
                                "llama_index.embeddings": embeddings,
                                "llama_index.embeddings.ollama": ollama})
        if "sentence_transformers" not in sys.modules:
            sentence_transformers = types.ModuleType("sentence_transformers")
            sentence_transformers.CrossEncoder = type("CrossEncoder", (), {})
            sys.modules["sentence_transformers"] = sentence_transformers
        cls.smoke = load("tsc_generation_smoke", SCRIPTS / "smoke_test_rag_v5_e2e.py")
        cls.evidence = [{"source": "Fonte", "pages": "1", "text": "Principio documentato."}]
        cls.plan = applied_plan()

    def response(self, content, done_reason="stop"):
        return {"message": {"content": content}, "done_reason": done_reason, "eval_count": 10}

    def test_success_uses_exactly_one_transport_call(self):
        with patch.object(self.smoke, "_ollama_chat_once", return_value=self.response(envelope())) as call, \
             patch.object(self.smoke, "tactical_audit_answer", return_value=complete_audit()):
            answer, stats, diagnostic = self.smoke.chat_tactical_state_once(
                "model", "Come organizzi il 4-3-3?", self.evidence, 10, self.plan)
        self.assertEqual(call.call_count, 1)
        self.assertEqual(diagnostic["overall_status"], "validated")
        self.assertTrue(stats["quality_gate_passed"])
        self.assertTrue(answer)

    def test_failed_audit_never_repairs(self):
        audit = {"complete": False, "missing_facets": ["x"], "missing_operational": [],
                 "missing_details": [], "semantic_issues": []}
        with patch.object(self.smoke, "_ollama_chat_once", return_value=self.response(envelope())) as call, \
             patch.object(self.smoke, "tactical_audit_answer", return_value=audit):
            answer, _, diagnostic = self.smoke.chat_tactical_state_once(
                "model", "Come organizzi il 4-3-3?", self.evidence, 10, self.plan)
        self.assertEqual(call.call_count, 1)
        self.assertEqual(answer, "")
        self.assertEqual(diagnostic["overall_status"], "blocked")

    def test_truncation_never_repairs(self):
        with patch.object(self.smoke, "_ollama_chat_once", return_value=self.response(envelope(), "length")) as call, \
             patch.object(self.smoke, "tactical_audit_answer", return_value=complete_audit()):
            answer, _, diagnostic = self.smoke.chat_tactical_state_once(
                "model", "Come organizzi il 4-3-3?", self.evidence, 10, self.plan)
        self.assertEqual(call.call_count, 1)
        self.assertEqual(answer, "")
        self.assertEqual(diagnostic["overall_status"], "not_evaluable")

    def test_timeout_never_retries(self):
        with patch.object(self.smoke, "_ollama_chat_once", side_effect=URLError("timeout")) as call:
            answer, _, diagnostic = self.smoke.chat_tactical_state_once(
                "model", "Come organizzi il 4-3-3?", self.evidence, 10, self.plan)
        self.assertEqual(call.call_count, 1)
        self.assertEqual(answer, "")
        self.assertEqual(diagnostic["overall_status"], "not_evaluable")


class LegacyCompatibilityTests(unittest.TestCase):
    def legacy_report(self):
        return {"questions": [{"answer": "Risposta [F1]", "citation_ids": ["1"],
                                "invalid_citation_ids": [], "has_any_citation": True,
                                "tactical_plan": None}], "index_unchanged": True}

    def test_legacy_report_contract_is_unchanged(self):
        query.validate_report(self.legacy_report())

    def test_blocked_contract_is_not_a_completed_query(self):
        report = self.legacy_report()
        report["questions"][0]["answer"] = ""
        report["questions"][0]["tactical_state_contract"] = {"overall_status": "blocked"}
        with self.assertRaisesRegex(RuntimeError, "tactical_state_contract_blocked"):
            query.validate_report(report, require_tactical_state_contract=True)

    def test_default_profile_does_not_enable_either_tactical_gate(self):
        self.assertNotIn("--tactical-state-contract", query.DEFAULT_PROFILE_FLAGS)
        self.assertNotIn("--tactical-plan", query.DEFAULT_PROFILE_FLAGS)


if __name__ == "__main__":
    unittest.main()
