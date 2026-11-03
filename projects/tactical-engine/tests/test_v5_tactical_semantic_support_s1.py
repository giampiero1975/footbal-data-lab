import importlib.util
import json
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


planner = load("tsc_planner_s1_tests", SCRIPTS / "v5_tactical_query_plan_v1.py")
dual = load("tsc_dual_s1_tests", SCRIPTS / "v5_tactical_state_dual_output_v1.py")
s1 = load("tsc_s1_tests", SCRIPTS / "v5_tactical_semantic_support_s1.py")

QUESTION = "Alla perdita l'ala deve coprire il lato debole per evitare la ripartenza?"
TEXT = "Alla perdita l'ala copre il lato debole."


def positive_audit():
    return {"complete": True, "missing_facets": [], "missing_operational": [],
            "missing_details": [], "semantic_issues": []}


def fixture(text=TEXT, statement=TEXT):
    question_plan = planner.analyse(QUESTION)
    preflight = dual.prepare_dual_output_request(question_plan)
    relation = preflight["authorized_applied_plan"]["operational_relations"][0]
    requirement = preflight["v2_preflight"]["projected_requirements"][0]
    claim = {
        "claim_id": "claim:s1", "statement": statement,
        "section_span": {"start": 0, "end": len(s1.normalize_text(statement))},
        "conditions": [], "relation_refs": [relation["relation_id"]],
        "requirement_refs": [requirement["requirement_id"]],
        "dimensions": ["actor", "task", "space", "trigger", "purpose", "phase"],
        "bindings": dual.relation_bindings(relation), "polarity": "affirmed",
        "evidence_refs": ["F1"], "support_mode": "direct",
        "evidence_anchors": [{"evidence_ref": "F1", "exact_text": statement}],
    }
    envelope = {
        "schema": dual.TRANSPORT_SCHEMA,
        "authorized_plan_fingerprint": preflight["authorized_plan_fingerprint"],
        "documentary_explanation": {"sections": [{
            "section_id": "section:s1", "kind": "relation_explanation",
            "relation_refs": [relation["relation_id"]],
            "requirement_refs": [requirement["requirement_id"]], "text": text,
            "evidence_refs": ["F1"], "claims": [claim],
        }]},
    }
    evidence = [{"label": "F1", "text": statement, "source": "fixture"}]
    return question_plan, preflight, envelope, evidence


def diagnose(envelope, question_plan, preflight, evidence, audit=None):
    return dual.documentary_diagnostic(
        question_plan, json.dumps(envelope, ensure_ascii=False), evidence,
        preflight=preflight, tactical_audit=audit or positive_audit(),
        attempt_id="attempt:s1")


class SemanticSupportS1Tests(unittest.TestCase):
    def test_exact_atomic_claim_is_supported_and_content_addressed(self):
        question_plan, preflight, envelope, evidence = fixture()
        result = diagnose(envelope, question_plan, preflight, evidence)
        self.assertEqual(result["overall_status"], "validated")
        assessment = result["controls"]["semantic_support_assessments"][0]
        self.assertEqual(assessment["aggregate_verdict"], "supported")
        self.assertEqual(assessment["attempt_id"], "attempt:s1")
        self.assertEqual(assessment["plan_fingerprint"], preflight["authorized_plan_fingerprint"])
        self.assertEqual(s1.verify_assessment(
            assessment, "attempt:s1", preflight["authorized_plan_fingerprint"],
            envelope["documentary_explanation"]["sections"][0]["claims"][0],
            {"F1": evidence[0]}), [])

    def test_paraphrase_quantifier_and_partial_evidence_are_not_evaluable(self):
        for statement in ("L'ala copre il lato debole.",
                          "Alla perdita l'ala copre sempre il lato debole.",
                          "Alla perdita l'ala copre il lato debole e protegge la porta."):
            with self.subTest(statement=statement):
                claim = {"claim_id": "c", "statement": statement,
                         "evidence_refs": ["F1"], "support_mode": "direct",
                         "evidence_anchors": [{"evidence_ref": "F1", "exact_text": statement}]}
                assessment = s1.assess_claim(
                    "a", "sha256:" + "1" * 64, claim, {"F1": {"text": TEXT}})
                self.assertEqual(assessment["aggregate_verdict"], "not_evaluable")

    def test_composite_and_multi_source_claims_are_not_evaluable(self):
        question_plan, preflight, envelope, evidence = fixture()
        claim = envelope["documentary_explanation"]["sections"][0]["claims"][0]
        claim["evidence_refs"] = ["F1", "F2"]
        claim["evidence_anchors"].append({"evidence_ref": "F2", "exact_text": TEXT})
        evidence.append({"label": "F2", "text": TEXT})
        result = diagnose(envelope, question_plan, preflight, evidence)
        self.assertEqual(result["overall_status"], "not_evaluable")

    def test_no_negative_rule_means_opposite_claim_is_not_evaluable_not_unsupported(self):
        claim = {"claim_id": "c", "statement": "L'ala non copre.",
                 "evidence_refs": ["F1"], "support_mode": "direct",
                 "evidence_anchors": [{"evidence_ref": "F1", "exact_text": "L'ala copre."}]}
        assessment = s1.assess_claim("a", "sha256:" + "1" * 64, claim,
                                     {"F1": {"text": "L'ala copre."}})
        self.assertEqual(assessment["aggregate_verdict"], "not_evaluable")
        self.assertNotEqual(assessment["aggregate_verdict"], "unsupported")

    def test_condition_or_quantifier_omission_is_not_promoted(self):
        for evidence_text, statement in (
                ("Se la palla è scoperta. L'ala copre.", "L'ala copre."),
                ("L'ala copre. Sempre.", "L'ala copre.")):
            with self.subTest(evidence=evidence_text):
                claim = {"claim_id": "c", "statement": statement,
                         "evidence_refs": ["F1"], "support_mode": "direct",
                         "evidence_anchors": [{"evidence_ref": "F1", "exact_text": statement}]}
                assessment = s1.assess_claim(
                    "a", "sha256:" + "1" * 64, claim, {"F1": {"text": evidence_text}})
                self.assertEqual(assessment["aggregate_verdict"], "not_evaluable")

    def test_statement_span_mismatch_and_overlap_are_blocked(self):
        question_plan, preflight, envelope, evidence = fixture()
        claim = envelope["documentary_explanation"]["sections"][0]["claims"][0]
        claim["section_span"] = {"start": 1, "end": len(TEXT)}
        result = diagnose(envelope, question_plan, preflight, evidence)
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("statement_span_mismatch", result["reasons"])

        question_plan, preflight, envelope, evidence = fixture()
        duplicate = deepcopy(envelope["documentary_explanation"]["sections"][0]["claims"][0])
        duplicate["claim_id"] = "claim:s1:2"
        envelope["documentary_explanation"]["sections"][0]["claims"].append(duplicate)
        result = diagnose(envelope, question_plan, preflight, evidence)
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("incompatible_claim_span_overlap", result["reasons"])

    def test_uncovered_substantive_prose_is_not_evaluable(self):
        question_plan, preflight, envelope, evidence = fixture(text=TEXT + " Extra.")
        result = diagnose(envelope, question_plan, preflight, evidence)
        self.assertEqual(result["overall_status"], "not_evaluable")
        self.assertIn("substantive_prose_coverage_not_evaluable", result["reasons"])

    def test_unicode_nfc_span_uses_normalized_code_points(self):
        composed = "Caffè"
        decomposed = "Caffe\u0300"
        question_plan, preflight, envelope, evidence = fixture(text=decomposed, statement=composed)
        evidence[0]["text"] = decomposed
        envelope["documentary_explanation"]["sections"][0]["claims"][0][
            "evidence_anchors"][0]["exact_text"] = composed
        result = diagnose(envelope, question_plan, preflight, evidence)
        self.assertEqual(result["overall_status"], "validated")

    def test_tampered_addresses_assessor_and_verdict_are_rejected(self):
        question_plan, preflight, envelope, evidence = fixture()
        claim = envelope["documentary_explanation"]["sections"][0]["claims"][0]
        evidence_by_id = {"F1": evidence[0]}
        original = s1.assess_claim("attempt:s1", preflight["authorized_plan_fingerprint"],
                                   claim, evidence_by_id)
        mutations = [
            ("statement", lambda item: item.update(statement_sha256="sha256:" + "0" * 64)),
            ("plan", lambda item: item.update(plan_fingerprint="sha256:" + "0" * 64)),
            ("evidence", lambda item: item["evidence"][0].update(
                evidence_sha256="sha256:" + "0" * 64)),
            ("assessor", lambda item: item["assessor"].update(name="model")),
            ("verdict", lambda item: item.update(aggregate_verdict="unsupported")),
        ]
        for name, mutate in mutations:
            with self.subTest(name=name):
                record = deepcopy(original)
                mutate(record)
                self.assertTrue(s1.verify_assessment(
                    record, "attempt:s1", preflight["authorized_plan_fingerprint"],
                    claim, evidence_by_id))

    def test_model_authored_assessment_field_is_rejected(self):
        question_plan, preflight, envelope, evidence = fixture()
        envelope["documentary_explanation"]["sections"][0]["claims"][0][
            "support_assessment"] = {"aggregate_verdict": "supported"}
        result = diagnose(envelope, question_plan, preflight, evidence)
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("invalid_documentary_claim_shape", result["reasons"])

    def test_malformed_statement_is_blocked_without_checker_exception(self):
        question_plan, preflight, envelope, evidence = fixture()
        envelope["documentary_explanation"]["sections"][0]["claims"][0][
            "statement"] = ["not", "text"]
        result = diagnose(envelope, question_plan, preflight, evidence)
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("invalid_claim_statement_span", result["reasons"])

    def test_negative_documentary_audit_blocks_positive_s1(self):
        question_plan, preflight, envelope, evidence = fixture()
        audit = positive_audit()
        audit["complete"] = False
        audit["semantic_issues"] = ["unsupported_detail"]
        result = diagnose(envelope, question_plan, preflight, evidence, audit=audit)
        self.assertEqual(result["overall_status"], "blocked")
        self.assertIn("tactical_documentary_audit_failed", result["reasons"])


if __name__ == "__main__":
    unittest.main()
