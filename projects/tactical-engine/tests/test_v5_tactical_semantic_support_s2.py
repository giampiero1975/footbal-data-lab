import importlib.util
import json
import sys
import unittest
from copy import deepcopy
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


planner = load("s2_shadow_planner", "v5_tactical_query_plan_v1.py")
dual = load("s2_shadow_dual", "v5_tactical_state_dual_output_v1.py")
s1 = load("s2_shadow_s1", "v5_tactical_semantic_support_s1.py")
s2 = load("s2_shadow_adapter", "v5_tactical_semantic_support_s2.py")

QUESTION = "Alla perdita l'ala deve coprire il lato debole per evitare la ripartenza?"
EVIDENCE = "Alla perdita l'ala copre il lato debole."
PARAPHRASE = "Quando perde palla, l'esterno protegge il versante opposto."
DESCRIPTOR = {"kind": "injected", "name": "mock-three-label", "version": "1",
              "config": {"labels": ["supported", "contradicted", "insufficient"]}}


def positive_audit():
    return {"complete": True, "missing_facets": [], "missing_operational": [],
            "missing_details": [], "semantic_issues": []}


def fixture(statement=PARAPHRASE, evidence_text=EVIDENCE):
    question_plan = planner.analyse(QUESTION)
    preflight = dual.prepare_dual_output_request(question_plan)
    relation = preflight["authorized_applied_plan"]["operational_relations"][0]
    requirement = preflight["v2_preflight"]["projected_requirements"][0]
    claim = {
        "claim_id": "claim:s2-shadow", "statement": statement,
        "section_span": {"start": 0, "end": len(statement)}, "conditions": [],
        "relation_refs": [relation["relation_id"]],
        "requirement_refs": [requirement["requirement_id"]],
        "dimensions": ["actor", "task", "space", "trigger", "purpose", "phase"],
        "bindings": dual.relation_bindings(relation), "polarity": "affirmed",
        "evidence_refs": ["F1"], "support_mode": "direct",
        "evidence_anchors": [{"evidence_ref": "F1", "exact_text": evidence_text}],
    }
    envelope = {
        "schema": dual.TRANSPORT_SCHEMA,
        "authorized_plan_fingerprint": preflight["authorized_plan_fingerprint"],
        "documentary_explanation": {"sections": [{
            "section_id": "section:s2", "kind": "relation_explanation",
            "relation_refs": [relation["relation_id"]],
            "requirement_refs": [requirement["requirement_id"]],
            "text": statement, "evidence_refs": ["F1"], "claims": [claim],
        }]},
    }
    evidence = [{"label": "F1", "text": evidence_text, "source": "synthetic"}]
    return question_plan, preflight, envelope, evidence


def diagnose(judge=None, descriptor=DESCRIPTOR, **fixture_kwargs):
    plan, preflight, envelope, evidence = fixture(**fixture_kwargs)
    result = dual.documentary_diagnostic(
        plan, json.dumps(envelope, ensure_ascii=False), evidence,
        preflight=preflight, tactical_audit=positive_audit(), attempt_id="attempt:s2",
        semantic_support_s2_judge=judge,
        semantic_support_s2_judge_descriptor=descriptor if judge else None)
    return result, plan, preflight, envelope, evidence


class SemanticSupportS2ShadowTests(unittest.TestCase):
    def shadow(self, result):
        return result["controls"]["semantic_support_s2_shadow"][0]

    def test_01_paraphrase_supported_only_in_shadow_without_promotion(self):
        result, *_ = diagnose(lambda _: {"label": "supported", "rationale": "Equivalent paraphrase."})
        record = self.shadow(result)
        self.assertEqual(record["aggregate_verdict"], "supported")
        self.assertFalse(record["promotion_authorized"])
        self.assertEqual(result["overall_status"], "not_evaluable")
        self.assertEqual(result["promoted_answer"], "")
        self.assertEqual(result["controls"]["semantic_support_assessments"][0]["aggregate_verdict"], "not_evaluable")

    def test_02_explicit_contradiction_is_diagnostic_only(self):
        result, *_ = diagnose(lambda _: {"label": "contradicted", "rationale": "Negation conflicts."},
                              statement="Alla perdita l'ala non copre il lato debole.")
        record = self.shadow(result)
        self.assertEqual(record["aggregate_verdict"], "contradicted")
        self.assertFalse(record["promotion_authorized"])
        self.assertEqual(result["overall_status"], "not_evaluable")

    def test_03_omitted_condition_or_quantifier_is_insufficient(self):
        for statement in ("L'ala copre il lato debole.",
                          "Alla perdita l'ala copre sempre il lato debole."):
            with self.subTest(statement=statement):
                result, *_ = diagnose(
                    lambda _: {"label": "insufficient", "rationale": "Scope is not entailed."},
                    statement=statement,
                    evidence_text="Se la palla è scoperta, alla perdita l'ala copre il lato debole.")
                self.assertEqual(self.shadow(result)["aggregate_verdict"], "insufficient")
                self.assertEqual(result["promoted_answer"], "")

    def test_04_actor_or_phase_binding_mismatch_prevents_judge_call(self):
        plan, preflight, envelope, evidence = fixture()
        claim = envelope["documentary_explanation"]["sections"][0]["claims"][0]
        for dimension in ("actor", "phase"):
            with self.subTest(dimension=dimension):
                altered = deepcopy(claim)
                altered["bindings"][dimension] = "tampered"
                evidence_map = {"F1": evidence[0]}
                assessment = s1.assess_claim("attempt:s2", preflight["authorized_plan_fingerprint"],
                                             altered, evidence_map)
                called = []
                record = s2.assess_claim(
                    "attempt:s2", preflight["authorized_plan_fingerprint"], altered,
                    evidence_map, assessment,
                    {relation["relation_id"]: dual.relation_bindings(relation)
                     for relation in preflight["authorized_applied_plan"]["operational_relations"]},
                    lambda payload: called.append(payload), DESCRIPTOR)
                self.assertEqual(record["evaluation_status"], "not_evaluable")
                self.assertIn("claim_bindings_not_authoritative", record["reason_codes"])
                self.assertEqual(called, [])

    def test_05_tampered_fingerprint_or_evidence_digest_fails_closed(self):
        plan, preflight, envelope, evidence = fixture()
        claim = envelope["documentary_explanation"]["sections"][0]["claims"][0]
        evidence_map = {"F1": evidence[0]}
        assessment = s1.assess_claim("attempt:s2", preflight["authorized_plan_fingerprint"],
                                     claim, evidence_map)
        bindings = {relation["relation_id"]: dual.relation_bindings(relation)
                    for relation in preflight["authorized_applied_plan"]["operational_relations"]}
        judge = lambda _: {"label": "supported", "rationale": "mock"}
        fingerprint_record = s2.assess_claim(
            "attempt:s2", "sha256:" + "0" * 64, claim, evidence_map,
            assessment, bindings, judge, DESCRIPTOR)
        self.assertEqual(fingerprint_record["evaluation_status"], "not_evaluable")
        self.assertIn("support_assessment_plan_mismatch", fingerprint_record["reason_codes"])
        tampered = deepcopy(evidence_map)
        tampered["F1"]["text"] += " Altered."
        digest_record = s2.assess_claim(
            "attempt:s2", preflight["authorized_plan_fingerprint"], claim,
            tampered, assessment, bindings, judge, DESCRIPTOR)
        self.assertEqual(digest_record["evaluation_status"], "not_evaluable")
        self.assertIn("support_evidence_digest_mismatch", digest_record["reason_codes"])

        valid = s2.assess_claim(
            "attempt:s2", preflight["authorized_plan_fingerprint"], claim,
            evidence_map, assessment, bindings, judge, DESCRIPTOR)
        self.assertEqual(s2.verify_assessment(
            valid, "attempt:s2", preflight["authorized_plan_fingerprint"], claim,
            evidence_map, assessment, bindings, DESCRIPTOR), [])
        altered_record = deepcopy(valid)
        altered_record["evidence"][0]["judge_rationale"] = "tampered"
        self.assertIn("s2_shadow_record_digest_mismatch", s2.verify_assessment(
            altered_record, "attempt:s2", preflight["authorized_plan_fingerprint"],
            claim, evidence_map, assessment, bindings, DESCRIPTOR))

    def test_06_malformed_result_and_judge_exception_are_not_evaluable(self):
        judges = (
            lambda _: {"label": "maybe", "rationale": "invalid"},
            lambda _: (_ for _ in ()).throw(RuntimeError("offline mock failure")),
        )
        for judge in judges:
            with self.subTest(judge=judge):
                result, *_ = diagnose(judge)
                record = self.shadow(result)
                self.assertEqual(record["evaluation_status"], "not_evaluable")
                self.assertEqual(record["aggregate_verdict"], "not_evaluable")
                self.assertFalse(record["promotion_authorized"])

    def test_07_conflicting_multi_evidence_has_no_majority_fallback(self):
        plan, preflight, envelope, evidence = fixture()
        claim = envelope["documentary_explanation"]["sections"][0]["claims"][0]
        claim["evidence_refs"] = ["F1", "F2"]
        claim["evidence_anchors"].append({"evidence_ref": "F2", "exact_text": EVIDENCE})
        evidence.append({"label": "F2", "text": EVIDENCE, "source": "synthetic-2"})
        envelope["documentary_explanation"]["sections"][0]["evidence_refs"].append("F2")
        labels = iter(("supported", "contradicted"))
        result = dual.documentary_diagnostic(
            plan, json.dumps(envelope, ensure_ascii=False), evidence,
            preflight=preflight, tactical_audit=positive_audit(), attempt_id="attempt:s2",
            semantic_support_s2_judge=lambda _: {"label": next(labels), "rationale": "mock"},
            semantic_support_s2_judge_descriptor=DESCRIPTOR)
        record = self.shadow(result)
        self.assertEqual(record["aggregate_verdict"], "conflicting")
        self.assertIn("conflicting_evidence_no_majority", record["reason_codes"])
        self.assertFalse(record["promotion_authorized"])

    def test_08_disabled_adapter_preserves_legacy_result(self):
        plan, preflight, envelope, evidence = fixture(statement=EVIDENCE)
        args = (plan, json.dumps(envelope, ensure_ascii=False), evidence)
        kwargs = {"preflight": preflight, "tactical_audit": positive_audit(),
                  "attempt_id": "attempt:s2"}
        implicit = dual.documentary_diagnostic(*args, **kwargs)
        explicit = dual.documentary_diagnostic(
            *args, **kwargs, semantic_support_s2_judge=None,
            semantic_support_s2_judge_descriptor=None)
        self.assertEqual(implicit, explicit)
        self.assertNotIn("semantic_support_s2_shadow", implicit["controls"])
        self.assertEqual(implicit["overall_status"], "validated")
        self.assertEqual(implicit["promoted_answer"], EVIDENCE)


if __name__ == "__main__":
    unittest.main()
