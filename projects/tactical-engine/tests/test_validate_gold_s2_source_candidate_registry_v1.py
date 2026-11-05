import copy
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_gold_s2_source_candidate_registry_v1.py"
SPEC = importlib.util.spec_from_file_location("candidate_registry_v1", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def evidence(evidence_id, evidence_type):
    return {
        "evidence_id": evidence_id,
        "evidence_type": evidence_type,
        "digest": "sha256:" + "1" * 64,
        "verified": True,
        "reviewer_id": "reviewer:evidence",
        "verified_at": "2026-11-05T12:00:00Z",
    }


def registry_fixture(decision="eligible_holdout", split="holdout"):
    records = [evidence(f"e:{kind}", kind) for kind in (
        "identity", "provenance", "digest", "rights", "retention",
        "exposure", "independence", "decision",
    )]
    candidate = {
        "candidate_id": "candidate:synthetic-1",
        "source_id": "source:synthetic-1",
        "title": "Synthetic tactical source",
        "author": [{"name": "Synthetic Author", "authority_id": "author:1"}],
        "organization": {"name": "Synthetic Organization", "authority_id": "org:1"},
        "version": {"edition": "1", "date": "2026-01-01", "language": "it", "document_id": "document:1", "version_id": "version:1"},
        "provenance": {"channel": "commissioned", "origin_ref": "synthetic:test-only", "chain_status": "verified", "evidence_refs": ["e:provenance"]},
        "digest": {"algorithm": "sha256", "value": "sha256:" + "2" * 64, "verification_status": "verified_bytes", "evidence_ref": "e:digest"},
        "rights_evidence": [
            {"evidence_id": "e:rights", "scope": scope, "status": "verified", "expires_at": None, "revoked_at": None, "reviewer_id": "reviewer:rights"}
            for scope in ("retention", "annotation", "publication")
        ],
        "retention_policy": {"policy_id": "retention:1", "status": "verified", "evidence_refs": ["e:retention"]},
        "annotation_permission": "verified",
        "publication_permission": "verified",
        "historical_exposure": [{"system": "all-declared-systems", "dataset": "all-declared-datasets", "status": "verified_absent", "evidence_refs": ["e:exposure"]}],
        "independence": {"source_disjoint": "pass", "document_disjoint": "pass", "version_disjoint": "pass", "author_disjoint": "pass", "evidence_refs": ["e:independence"]},
        "duplicate_cluster": "duplicate:1",
        "author_cluster": "author-cluster:1",
        "proposed_split": split,
        "eligibility_decision": decision,
        "evidence_refs": ["e:identity", "e:decision"],
        "reviewer": "reviewer:decision",
        "decision_date": "2026-11-05",
        "decision_rationale": "Synthetic positive fixture.",
        "gold_s2_provenance_record_id": "prov:future-1",
    }
    return {
        "schema_version": MODULE.SCHEMA_VERSION,
        "registry_version": "1.0.0",
        "status": "draft",
        "policy": {
            "approval_status": "approved",
            "known_corpus_exclusion": "approved",
            "known_web_exclusion": "approved",
            "author_disjoint_policy": "absolute",
            "rights_custodian_id": "custodian:1",
            "retention_policy_approved": True,
            "publication_policy_approved": True,
            "acquisition_authorized": True,
        },
        "evidence_records": records,
        "candidates": [candidate],
    }


class CandidateRegistryV1Tests(unittest.TestCase):
    def errors(self, registry):
        return MODULE.validate_registry(registry).errors

    def test_01_empty_repository_template_is_valid(self):
        report = MODULE.validate_repository_contracts(ROOT)
        self.assertEqual(report.errors, [])

    def test_02_positive_synthetic_candidate(self):
        self.assertEqual(self.errors(registry_fixture()), [])

    def test_03_duplicate_candidate_id(self):
        value = registry_fixture()
        second = copy.deepcopy(value["candidates"][0])
        second["source_id"] = "source:2"
        second["version"]["document_id"] = "document:2"
        second["version"]["version_id"] = "version:2"
        value["candidates"].append(second)
        self.assertIn("DUPLICATE_CANDIDATE_ID:candidate:synthetic-1", self.errors(value))

    def test_04_missing_evidence_reference(self):
        value = registry_fixture()
        value["candidates"][0]["provenance"]["evidence_refs"] = ["missing"]
        self.assertTrue(any(item.startswith("EVIDENCE_REF_UNRESOLVED") for item in self.errors(value)))

    def test_05_malformed_digest(self):
        value = registry_fixture()
        value["candidates"][0]["digest"]["value"] = "not-a-sha256"
        self.assertTrue(any(item.startswith("SHA256_INVALID") for item in self.errors(value)))

    def test_06_declared_digest_is_not_verified(self):
        value = registry_fixture()
        value["candidates"][0]["digest"]["verification_status"] = "declared_only"
        report = MODULE.validate_registry(value)
        self.assertTrue(any(item.startswith("DIGEST_NOT_VERIFIED") for item in report.errors))
        self.assertTrue(any(item.startswith("DIGEST_NOT_BYTE_VERIFIED") for item in report.unverifiable))

    def test_07_missing_rights_scope(self):
        value = registry_fixture()
        value["candidates"][0]["rights_evidence"] = value["candidates"][0]["rights_evidence"][:1]
        self.assertTrue(any(item.startswith("RIGHTS_SCOPES_NOT_VERIFIED") for item in self.errors(value)))

    def test_08_expired_or_revoked_rights(self):
        for status in ("expired", "revoked"):
            value = registry_fixture()
            value["candidates"][0]["rights_evidence"][1]["status"] = status
            self.assertTrue(any(item.startswith("RIGHTS_SCOPES_NOT_VERIFIED") for item in self.errors(value)))

    def test_09_empty_exposure_ledger_is_not_absence(self):
        value = registry_fixture()
        value["candidates"][0]["historical_exposure"] = []
        report = MODULE.validate_registry(value)
        self.assertTrue(any(item.startswith("EXPOSURE_NOT_CLEARED") for item in report.errors))
        self.assertTrue(any(item.startswith("EXPOSURE_LEDGER_EMPTY") for item in report.unverifiable))

    def test_10_verified_exposure_blocks_holdout(self):
        value = registry_fixture()
        value["candidates"][0]["historical_exposure"][0]["status"] = "verified_exposed"
        self.assertTrue(any(item.startswith("EXPOSURE_NOT_CLEARED") for item in self.errors(value)))

    def test_11_duplicate_cluster_conflict(self):
        value = registry_fixture(decision="eligible_development", split="development")
        second = copy.deepcopy(value["candidates"][0])
        second.update({"candidate_id": "candidate:2", "source_id": "source:2", "eligibility_decision": "eligible_holdout", "proposed_split": "holdout"})
        second["version"].update({"document_id": "document:2", "version_id": "version:2"})
        value["candidates"].append(second)
        self.assertIn("DUPLICATE_CLUSTER_SPLIT_CONFLICT:duplicate:1", self.errors(value))

    def test_12_author_policy_not_approved(self):
        value = registry_fixture()
        value["policy"]["author_disjoint_policy"] = "not_approved"
        self.assertTrue(any(item.startswith("AUTHOR_POLICY_NOT_APPROVED") for item in self.errors(value)))

    def test_13_policy_blocks_all_promotions(self):
        value = registry_fixture(decision="eligible_development", split="development")
        value["policy"]["approval_status"] = "not_approved"
        value["policy"]["acquisition_authorized"] = False
        self.assertTrue(any(item.startswith("POLICY_NOT_APPROVED_FOR_PROMOTION") for item in self.errors(value)))

    def test_14_undue_holdout_promotion(self):
        value = registry_fixture()
        value["candidates"][0]["independence"]["document_disjoint"] = "unknown"
        self.assertTrue(any(item.startswith("INDEPENDENCE_NOT_VERIFIED") for item in self.errors(value)))

    def test_15_missing_reviewer(self):
        value = registry_fixture()
        value["candidates"][0]["reviewer"] = None
        self.assertTrue(any(item.startswith("DECISION_ATTRIBUTION_REQUIRED") for item in self.errors(value)))

    def test_16_decision_without_evidence(self):
        value = registry_fixture()
        value["candidates"][0]["evidence_refs"] = []
        self.assertTrue(any(item.startswith("DECISION_ATTRIBUTION_REQUIRED") for item in self.errors(value)))

    def test_17_gold_s2_compatibility_is_pre_case_reference(self):
        value = registry_fixture()
        candidate = value["candidates"][0]
        self.assertTrue(candidate["gold_s2_provenance_record_id"].startswith("prov:"))
        self.assertEqual(self.errors(value), [])


if __name__ == "__main__":
    unittest.main()
