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


planner = load("tsc_planner_dual_output_tests", SCRIPTS / "v5_tactical_query_plan_v1.py")
dual = load("tsc_dual_output_tests", SCRIPTS / "v5_tactical_state_dual_output_v1.py")

QUESTION = "Alla perdita l'ala deve coprire il lato debole per evitare la ripartenza?"
EVIDENCE_TEXT = "Alla perdita l'ala copre il lato debole e protegge la zona preventiva."


def question_plan():
    return planner.analyse(QUESTION)


def positive_audit():
    return {"complete": True, "missing_facets": [], "missing_operational": [],
            "missing_details": [], "semantic_issues": []}


def fixture():
    plan = question_plan()
    preflight = dual.prepare_dual_output_request(plan)
    relation = preflight["authorized_applied_plan"]["operational_relations"][0]
    requirement = preflight["v2_preflight"]["projected_requirements"][0]
    claim = {
        "claim_id": "claim:1",
        "relation_refs": [relation["relation_id"]],
        "dimensions": ["actor", "task", "space", "trigger", "purpose", "phase"],
        "bindings": dual.relation_bindings(relation),
        "polarity": "affirmed",
        "evidence_refs": ["F1"],
        "support_mode": "direct",
        "evidence_anchors": [{"evidence_ref": "F1", "exact_text": EVIDENCE_TEXT}],
    }
    envelope = {
        "schema": dual.TRANSPORT_SCHEMA,
        "authorized_plan_fingerprint": preflight["authorized_plan_fingerprint"],
        "documentary_explanation": {"sections": [{
            "section_id": "section:1",
            "kind": "relation_explanation",
            "relation_refs": [relation["relation_id"]],
            "requirement_refs": [requirement["requirement_id"]],
            "text": EVIDENCE_TEXT,
            "evidence_refs": ["F1"],
            "claims": [claim],
        }]},
    }
    evidence = [{"label": "F1", "source": "fixture", "pages": [1],
                 "text": EVIDENCE_TEXT}]
    return plan, preflight, envelope, evidence


def diagnose(envelope, *, audit=None, support=None, done_reason=None):
    plan, preflight, _, evidence = fixture()
    return dual.documentary_diagnostic(
        plan, json.dumps(envelope, ensure_ascii=False), evidence,
        preflight=preflight, tactical_audit=audit or positive_audit(),
        support_assessments=support, done_reason=done_reason)


class DualOutputDeterministicTests(unittest.TestCase):
    def test_fingerprint_and_rendering_are_deterministic(self):
        first = dual.prepare_dual_output_request(question_plan())
        second = dual.prepare_dual_output_request(question_plan())
        self.assertEqual(first["authorized_plan_fingerprint"], second["authorized_plan_fingerprint"])
        self.assertEqual(first["canonical_relations"], second["canonical_relations"])
        self.assertEqual(first["canonical_relations"][0]["rendered_lines"][0],
                         "[REL " + first["canonical_relations"][0]["relation_id"] + "]")

    def test_transport_schema_does_not_allow_model_authored_plan(self):
        schema = dual.generation_transport_schema()
        self.assertNotIn("applied_plan", schema["properties"])
        self.assertNotIn("canonical_relations", schema["properties"])
        self.assertEqual(schema["properties"]["schema"]["const"], dual.TRANSPORT_SCHEMA)

    def test_supported_direct_claim_can_validate_offline(self):
        _, _, envelope, _ = fixture()
        result = diagnose(envelope, support={"claim:1": "supported"})
        self.assertEqual(result["overall_status"], "validated")
        self.assertEqual(result["promoted_answer"], EVIDENCE_TEXT)

    def test_anchor_alone_never_promotes_semantic_support(self):
        _, _, envelope, _ = fixture()
        result = diagnose(envelope)
        self.assertEqual(result["overall_status"], "not_evaluable")
        self.assertEqual(result["promoted_answer"], "")
        self.assertIn("semantic_support_not_evaluable", result["reasons"])

    def test_bounded_inference_is_not_evaluable(self):
        _, _, envelope, _ = fixture()
        claim = envelope["documentary_explanation"]["sections"][0]["claims"][0]
        claim["support_mode"] = "bounded_inference"
        claim["evidence_anchors"] = []
        result = diagnose(envelope, support={"claim:1": "supported"})
        self.assertEqual(result["overall_status"], "not_evaluable")
        self.assertIn("bounded_inference_not_evaluable", result["reasons"])

    def test_fingerprint_mismatch_is_blocked(self):
        _, _, envelope, _ = fixture()
        envelope["authorized_plan_fingerprint"] = "sha256:" + "0" * 64
        result = diagnose(envelope, support={"claim:1": "supported"})
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("authorized_plan_fingerprint_mismatch", result["reasons"])

    def test_malformed_and_truncated_transport_are_not_promoted(self):
        plan, preflight, envelope, evidence = fixture()
        malformed = dual.documentary_diagnostic(plan, "{", evidence, preflight=preflight)
        self.assertEqual(malformed["overall_status"], "not_evaluable")
        truncated = dual.documentary_diagnostic(
            plan, json.dumps(envelope), evidence, preflight=preflight,
            tactical_audit=positive_audit(), support_assessments={"claim:1": "supported"},
            done_reason="length")
        self.assertEqual(truncated["overall_status"], "not_evaluable")
        self.assertEqual(truncated["promoted_answer"], "")

    def test_section_and_total_cardinality_are_fail_closed(self):
        _, _, envelope, _ = fixture()
        envelope["documentary_explanation"]["sections"] = [
            deepcopy(envelope["documentary_explanation"]["sections"][0])
            for _ in range(dual.MAX_SECTIONS + 1)]
        result = diagnose(envelope, support={"claim:1": "supported"})
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("invalid_documentary_section_cardinality", result["reasons"])

    def test_unknown_and_duplicate_references_are_blocked(self):
        _, _, envelope, _ = fixture()
        section = envelope["documentary_explanation"]["sections"][0]
        section["relation_refs"] = ["relation:unknown", "relation:unknown"]
        result = diagnose(envelope, support={"claim:1": "supported"})
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("invalid_relation_refs", result["reasons"])

    def test_duplicate_claim_id_is_blocked(self):
        _, _, envelope, _ = fixture()
        claims = envelope["documentary_explanation"]["sections"][0]["claims"]
        claims.append(deepcopy(claims[0]))
        result = diagnose(envelope, support={"claim:1": "supported"})
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("invalid_or_duplicate_claim_id", result["reasons"])

    def test_each_normative_dimension_mismatch_is_blocked(self):
        for dimension in ("actor", "task", "space", "trigger", "purpose", "phase"):
            with self.subTest(dimension=dimension):
                _, _, envelope, _ = fixture()
                envelope["documentary_explanation"]["sections"][0]["claims"][0][
                    "bindings"][dimension] = "wrong"
                result = diagnose(envelope, support={"claim:1": "supported"})
                self.assertEqual(result["overall_status"], "blocked")
                self.assertIn(f"documentary_{dimension}_mismatch", result["reasons"])

    def test_negative_and_uncertain_polarity_are_distinct(self):
        _, _, negative, _ = fixture()
        negative["documentary_explanation"]["sections"][0]["claims"][0]["polarity"] = "negated"
        self.assertEqual(diagnose(negative)["overall_status"], "blocked")
        _, _, uncertain, _ = fixture()
        uncertain["documentary_explanation"]["sections"][0]["claims"][0]["polarity"] = "uncertain"
        self.assertEqual(diagnose(uncertain)["overall_status"], "not_evaluable")

    def test_invalid_citation_and_anchor_are_blocked(self):
        _, _, envelope, _ = fixture()
        claim = envelope["documentary_explanation"]["sections"][0]["claims"][0]
        claim["evidence_refs"] = ["F9"]
        claim["evidence_anchors"] = [{"evidence_ref": "F9", "exact_text": "missing"}]
        result = diagnose(envelope, support={"claim:1": "supported"})
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("invalid_claim_evidence_refs", result["reasons"])
        self.assertIn("evidence_anchor_mismatch", result["reasons"])

    def test_relation_omission_is_blocked(self):
        _, _, envelope, _ = fixture()
        section = envelope["documentary_explanation"]["sections"][0]
        section["relation_refs"] = []
        section["claims"][0]["relation_refs"] = []
        result = diagnose(envelope)
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("documentary_relation_omitted", result["reasons"])

    def test_negative_audit_is_blocked_and_positive_is_not_sufficient(self):
        _, _, envelope, _ = fixture()
        negative = positive_audit()
        negative["complete"] = False
        negative["missing_details"] = ["field_zone"]
        result = diagnose(envelope, audit=negative, support={"claim:1": "supported"})
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("tactical_documentary_audit_failed", result["reasons"])
        no_support = diagnose(envelope, audit=positive_audit())
        self.assertEqual(no_support["overall_status"], "not_evaluable")


class DualOutputWrapperTests(unittest.TestCase):
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
        return load("tsc_smoke_dual_output_tests", SCRIPTS / "smoke_test_rag_v5_e2e.py")

    def test_wrapper_calls_transport_once_and_never_sends_plan_as_model_output(self):
        smoke = self._load_smoke()
        plan, preflight, envelope, evidence = fixture()
        response = {"message": {"content": json.dumps(envelope)}, "done_reason": "stop"}
        with patch.object(smoke, "_ollama_chat_once", return_value=response) as transport, \
             patch.object(smoke, "tactical_audit_answer", return_value=positive_audit()):
            answer, stats, diagnostic = smoke.chat_tactical_state_v2_dual_output_once(
                "mock", QUESTION, evidence, 1, plan)
        self.assertEqual(transport.call_count, 1)
        payload = transport.call_args.args[0]
        self.assertNotIn("applied_plan", payload["format"]["properties"])
        self.assertNotIn("canonical_relations", payload["format"]["properties"])
        self.assertEqual(stats["repair_reasons"], [])
        self.assertEqual(answer, "")
        self.assertEqual(diagnostic["overall_status"], "not_evaluable")

    def test_new_flag_is_opt_in_and_report_validation_isolated(self):
        query = load("tsc_query_dual_output_tests", SCRIPTS / "run_rag_v5_query.py")
        self.assertNotIn("--tactical-state-contract-v2-dual-output", query.DEFAULT_PROFILE_FLAGS)
        report = {"index_unchanged": True, "questions": [{
            "tactical_state_contract_v2": {"overall_status": "validated"},
            "invalid_citation_ids": [], "has_any_citation": True}]}
        with self.assertRaisesRegex(RuntimeError, "tactical_state_contract_v2_dual_output_missing"):
            query.validate_report(report, require_tactical_state_contract_v2_dual_output=True)


if __name__ == "__main__":
    unittest.main()
