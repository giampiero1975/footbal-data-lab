import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
SCRIPT = SCRIPT_DIR / "validate_tactical_semantic_support_gold_s2_v1.py"
SPEC = importlib.util.spec_from_file_location("gold_s2_v1", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def fixture(frozen=True):
    source_content = "Fonte sintetica: il mediano protegge lo spazio centrale."
    evidence_text = "Il mediano protegge lo spazio centrale."
    claim_text = "Il mediano protegge lo spazio centrale."
    dataset = {
        "schema_version": MODULE.SCHEMA_VERSION,
        "dataset_version": "1.0.0",
        "status": "frozen" if frozen else "draft",
        "canonicalization_profile": MODULE.CANONICALIZATION_PROFILE,
        "independence_policy": {
            "source_disjoint_required": True,
            "document_disjoint_required": True,
            "near_duplicate_disjoint_required": True,
            "author_disjoint_required": False,
        },
        "provenance_records": [{
            "provenance_record_id": "prov-1", "source_id": "source-1",
            "document_id": "doc-1", "document_version": "1.0.0",
            "author_group_id": "author-1", "near_duplicate_cluster_id": "cluster-1",
            "source_content": source_content,
            "source_sha256": MODULE._digest_bytes(source_content.encode("utf-8")),
            "rights_status": "active", "availability_status": "verified",
        }],
        "review_ledger": [], "qa_records": [], "holder_authorizations": [],
        "cases": [], "dataset_sha256": None,
    }
    evidence = {
        "evidence_id": "F1", "provenance_record_id": "prov-1",
        "location_refs": ["p.1"], "text": evidence_text,
        "context_before": "", "context_after": "", "normalization": "utf8_nfc_lf_v1",
        "evidence_sha256": None,
    }
    claim = {
        "text": claim_text, "context": "", "conditions": [], "quantifiers": [],
        "actors": [{"actor_id": "actor:mediano", "label": "mediano"}],
        "phase": "possesso", "relation_refs": ["relation:1"],
        "requirement_refs": ["requirement:1"], "claim_sha256": None,
    }
    case = {
        "case_id": "s2-1", "case_version": "1.0.0", "split_id": "development",
        "evidence": [evidence],
        "composition": {"mode": "single_source", "declared_evidence_ids": ["F1"]},
        "claim": claim,
        "taxonomy": {"primary_category": "direct_literal_support", "cross_cutting_properties": ["single_source", "correct_actor"]},
        "gold_label": "supported" if frozen else None,
        "gold_rationale": {
            "evidence_spans": [{"evidence_id": "F1", "span": {"start": 0, "end": len(evidence_text), "text": evidence_text}}],
            "explanation": "La fonte sintetica contiene l'intero claim." if frozen else "",
            "scope_notes": "", "ambiguity": "none",
        },
        "reviews": {
            "review_a_id": "review-a" if frozen else None,
            "review_b_id": "review-b" if frozen else None,
            "disagreement_declared": False,
            "adjudication_id": None,
            "qa_d_id": "qa-d" if frozen else None,
        },
        "case_subject_sha256": None,
        "freeze": {"status": "frozen" if frozen else "draft", "case_sha256": None, "dataset_version": "1.0.0"},
        "d3_mapping": {
            "statement": claim_text, "section_text": claim_text,
            "section_span": {"start": 0, "end": len(claim_text), "text": claim_text},
            "conditions": [], "relation_refs": ["relation:1"],
            "requirement_refs": ["requirement:1"], "evidence_refs": ["F1"],
            "evidence_anchors": [{"evidence_id": "F1", "span": {"start": 0, "end": len(evidence_text), "text": evidence_text}}],
            "plan_fingerprint": "sha256:" + "1" * 64,
            "statement_sha256": MODULE._digest_bytes(claim_text.encode("utf-8")),
            "assessment_s1": None,
        },
    }
    dataset["cases"] = [case]
    finalize(dataset)
    if frozen:
        subject_hash = case["case_subject_sha256"]
        span_ref = copy.deepcopy(case["gold_rationale"]["evidence_spans"])
        for role, review_id in (("A", "review-a"), ("B", "review-b")):
            dataset["review_ledger"].append({
                "review_id": review_id, "case_id": "s2-1", "role": role,
                "reviewer_id": f"reviewer-{role.lower()}", "object_sha256": subject_hash,
                "label": "supported", "evidence_spans": copy.deepcopy(span_ref),
                "rationale": "Synthetic independent review.", "blinded_to_peer": True,
                "blinded_to_model": True, "created_at": "2026-11-05T10:00:00Z",
            })
        dataset["qa_records"] = [{
            "qa_id": "qa-d", "case_id": "s2-1", "reviewer_id": "reviewer-d",
            "object_sha256": subject_hash, "status": "pass", "checks": ["integrity"],
            "rationale": "Synthetic QA.", "created_at": "2026-11-05T11:00:00Z",
        }]
        dataset["holder_authorizations"] = [{
            "authorization_id": "auth-1", "scope": "freeze", "dataset_version": "1.0.0",
            "holder_id": "holder-1", "approved_at": "2026-11-05T12:00:00Z",
        }]
        finalize(dataset)
    return dataset


def finalize(dataset):
    for case in dataset["cases"]:
        for unit in case["evidence"]:
            unit["evidence_sha256"] = MODULE.digest_document(MODULE.evidence_payload(unit))
        case["claim"]["claim_sha256"] = MODULE.digest_document(MODULE.claim_payload(case["claim"]))
        case["case_subject_sha256"] = MODULE.digest_document(MODULE.case_subject_payload(case))
        case["freeze"]["case_sha256"] = MODULE.digest_document(MODULE.case_payload(case)) if dataset["status"] == "frozen" else None
    for review in dataset["review_ledger"]:
        case = next(item for item in dataset["cases"] if item["case_id"] == review["case_id"])
        review["object_sha256"] = case["case_subject_sha256"]
    for qa in dataset["qa_records"]:
        case = next(item for item in dataset["cases"] if item["case_id"] == qa["case_id"])
        qa["object_sha256"] = case["case_subject_sha256"]
    dataset["dataset_sha256"] = MODULE.digest_document(MODULE.dataset_payload(dataset)) if dataset["status"] == "frozen" else None


def frozen_manifest(dataset):
    return {
        "schema_version": MODULE.MANIFEST_VERSION, "manifest_status": "frozen",
        "dataset": {"path": "gold-s2.json", "version": dataset["dataset_version"], "sha256": MODULE.digest_document(MODULE.dataset_payload(dataset))},
        "canonicalization_profile": MODULE.CANONICALIZATION_PROFILE,
        "case_count": len(dataset["cases"]),
        "cases": [{"case_id": case["case_id"], "sha256": case["freeze"]["case_sha256"], "split_id": case["split_id"]} for case in dataset["cases"]],
        "dependencies": [], "frozen_at": "2026-11-05T12:00:00Z",
        "holder_authorization_id": "auth-1", "parent_manifest_sha256": None,
        "supersedes_manifest_sha256": None, "immutable_after_freeze": True,
    }


class GoldS2V1ValidatorTests(unittest.TestCase):
    def test_01_repository_draft_contracts(self):
        report = MODULE.validate_repository_contracts(ROOT)
        self.assertEqual(report.errors, [])

    def test_02_valid_synthetic_frozen_bundle(self):
        dataset = fixture()
        self.assertEqual(MODULE.validate_dataset(dataset).errors, [])
        self.assertEqual(MODULE.validate_manifest(frozen_manifest(dataset), dataset).errors, [])

    def test_03_unknown_label(self):
        dataset = fixture()
        dataset["cases"][0]["gold_label"] = "plausible"
        finalize(dataset)
        self.assertTrue(any(item.startswith("GOLD_LABEL_UNKNOWN") for item in MODULE.validate_dataset(dataset).errors))

    def test_04_unknown_category(self):
        dataset = fixture()
        dataset["cases"][0]["taxonomy"]["primary_category"] = "easy_case"
        finalize(dataset)
        self.assertTrue(any(item.startswith("PRIMARY_CATEGORY_UNKNOWN") for item in MODULE.validate_dataset(dataset).errors))

    def test_05_missing_required_field(self):
        dataset = fixture()
        del dataset["cases"][0]["claim"]["phase"]
        finalize(dataset)
        self.assertTrue(any("MISSING_FIELD:cases[0].claim.phase" in item for item in MODULE.validate_dataset(dataset).errors))

    def test_06_wrong_type(self):
        dataset = fixture()
        dataset["cases"][0]["claim"]["conditions"] = {}
        finalize(dataset)
        self.assertTrue(any(item.startswith("TYPE_ARRAY_REQUIRED:cases[0].claim.conditions") for item in MODULE.validate_dataset(dataset).errors))

    def test_07_duplicate_case_id(self):
        dataset = fixture(frozen=False)
        dataset["cases"].append(copy.deepcopy(dataset["cases"][0]))
        self.assertIn("DUPLICATE_CASE_ID:s2-1", MODULE.validate_dataset(dataset).errors)

    def test_08_unicode_span_mismatch(self):
        dataset = fixture()
        dataset["cases"][0]["gold_rationale"]["evidence_spans"][0]["span"]["end"] -= 1
        finalize(dataset)
        self.assertTrue(any(item.startswith("SPAN_TEXT_MISMATCH") for item in MODULE.validate_dataset(dataset).errors))

    def test_09_digest_mismatch(self):
        dataset = fixture()
        dataset["cases"][0]["claim"]["claim_sha256"] = "sha256:" + "0" * 64
        dataset["dataset_sha256"] = MODULE.digest_document(MODULE.dataset_payload(dataset))
        self.assertIn("CLAIM_HASH_MISMATCH:s2-1", MODULE.validate_dataset(dataset).errors)

    def test_10_missing_source_reference(self):
        dataset = fixture()
        dataset["cases"][0]["evidence"][0]["provenance_record_id"] = "missing"
        finalize(dataset)
        self.assertTrue(any(item.startswith("PROVENANCE_REF_UNRESOLVED") for item in MODULE.validate_dataset(dataset).errors))

    def test_11_unresolved_review_ledger(self):
        dataset = fixture()
        dataset["cases"][0]["reviews"]["review_a_id"] = "missing"
        finalize(dataset)
        self.assertIn("FROZEN_REVIEW_A_UNRESOLVED:s2-1", MODULE.validate_dataset(dataset).errors)

    def test_12_split_source_contamination(self):
        dataset = fixture(frozen=False)
        second = copy.deepcopy(dataset["cases"][0])
        second["case_id"] = "s2-2"
        second["split_id"] = "calibration"
        dataset["cases"].append(second)
        finalize(dataset)
        self.assertTrue(any(item.startswith("SPLIT_CONTAMINATION:source_id") for item in MODULE.validate_dataset(dataset).errors))

    def test_13_declared_near_duplicate_contamination(self):
        dataset = fixture(frozen=False)
        second_prov = copy.deepcopy(dataset["provenance_records"][0])
        second_prov.update({"provenance_record_id": "prov-2", "source_id": "source-2", "document_id": "doc-2"})
        dataset["provenance_records"].append(second_prov)
        second = copy.deepcopy(dataset["cases"][0])
        second["case_id"] = "s2-2"
        second["split_id"] = "holdout"
        second["evidence"][0]["provenance_record_id"] = "prov-2"
        dataset["cases"].append(second)
        finalize(dataset)
        self.assertTrue(any(item.startswith("SPLIT_CONTAMINATION:near_duplicate_cluster_id") for item in MODULE.validate_dataset(dataset).errors))

    def test_14_frozen_incomplete(self):
        dataset = fixture()
        dataset["review_ledger"] = []
        finalize(dataset)
        errors = MODULE.validate_dataset(dataset).errors
        self.assertIn("FROZEN_REVIEW_A_UNRESOLVED:s2-1", errors)
        self.assertIn("FROZEN_REVIEW_B_UNRESOLVED:s2-1", errors)

    def test_15_frozen_without_holder_authorization(self):
        dataset = fixture()
        dataset["holder_authorizations"] = []
        finalize(dataset)
        self.assertIn("FROZEN_HOLDER_AUTHORIZATION_REQUIRED", MODULE.validate_dataset(dataset).errors)

    def test_16_incoherent_d3_mapping(self):
        dataset = fixture()
        dataset["cases"][0]["d3_mapping"]["statement"] = "Un altro claim."
        finalize(dataset)
        self.assertTrue(any(item.startswith("D3_STATEMENT_CLAIM_MISMATCH") for item in MODULE.validate_dataset(dataset).errors))

    def test_17_unverifiable_source_hash_is_not_promoted(self):
        dataset = fixture(frozen=False)
        dataset["provenance_records"][0]["source_content"] = None
        report = MODULE.validate_dataset(dataset)
        self.assertEqual(report.errors, [])
        self.assertIn("SOURCE_HASH_UNVERIFIABLE:prov-1", report.unverifiable)
        dataset["status"] = "frozen"
        finalize(dataset)
        self.assertIn("FROZEN_SOURCE_HASH_UNVERIFIABLE:prov-1", MODULE.validate_dataset(dataset).errors)

    def test_18_multisource_must_be_declared(self):
        dataset = fixture(frozen=False)
        second_prov = copy.deepcopy(dataset["provenance_records"][0])
        second_prov.update({"provenance_record_id": "prov-2", "source_id": "source-2", "document_id": "doc-2", "near_duplicate_cluster_id": "cluster-2"})
        dataset["provenance_records"].append(second_prov)
        second_evidence = copy.deepcopy(dataset["cases"][0]["evidence"][0])
        second_evidence.update({"evidence_id": "F2", "provenance_record_id": "prov-2"})
        dataset["cases"][0]["evidence"].append(second_evidence)
        dataset["cases"][0]["composition"]["declared_evidence_ids"].append("F2")
        finalize(dataset)
        self.assertIn("MULTI_SOURCE_NOT_DECLARED:cases[0]", MODULE.validate_dataset(dataset).errors)


if __name__ == "__main__":
    unittest.main()
