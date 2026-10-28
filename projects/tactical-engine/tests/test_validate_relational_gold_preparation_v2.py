import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_relational_gold_preparation_v2.py"
SPEC = importlib.util.spec_from_file_location("gold_preparation_v2", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
H = "a" * 64


def annotation(annotator):
    return {"annotator_id": annotator, "created_at": "2026-10-28T10:00:00Z", "payload": {"status": "ok"}}


def ledger_record(record_id, case_id, artifact_type):
    return {
        "adjudication_record_id": record_id,
        "case_id": case_id,
        "instruction_version": "instructions-1",
        "annotated_object": {"artifact_type": artifact_type, "artifact_version": "1.0.0", "artifact_sha256": H},
        "annotation_a": annotation("annotator-a"),
        "annotation_b": annotation("annotator-b"),
        "disagreements": [],
        "adjudication_c": annotation("adjudicator-c"),
        "adjudication_rationale": "Synthetic contract fixture.",
    }


def provenance_record():
    return {
        "provenance_record_id": "prov-1",
        "author_ref": "author-pseudo-1",
        "organization_ref": "org-pseudo-1",
        "origin_cluster_id": "cluster-1",
        "acquisition": {"origin": "synthetic-fixture", "acquired_at": "2026-10-28T09:00:00Z", "method": "offline-test"},
        "transformations": [],
        "independence": {"used_in_development": False, "failure_mode_exposure": False, "screening_method": "synthetic", "screening_result": "unique"},
        "conflicts_of_interest": [],
        "rights": {
            "license_class": "synthetic-test-only",
            "allowed_uses": ["offline_contract_validation"],
            "redistribution_status": "prohibited",
            "publication_status": "metadata_only",
            "retention_policy": "synthetic-test",
            "expires_at": None,
            "revocation_status": "active",
            "rights_evidence_ref": {
                "evidence_id": "rights-1", "evidence_version": "1.0.0", "sha256": H,
                "access_class": "restricted", "custodian": "synthetic-custodian",
                "availability_check": {"status": "verified", "checked_at": "2026-10-28T09:30:00Z", "reviewer_id": "reviewer-1"},
            },
        },
    }


def gold_e_case():
    return {
        "case_id": "e-1", "question": "Synthetic question.", "source_id": "source-1",
        "provenance_record_id": "prov-1", "independence_status": "independent_frozen",
        "annotation_version": "1.0.0", "adjudication_record_id": "adj-e-1",
        "request_parts": [{"request_part_id": "part-1", "text": "Synthetic request.", "order": 0, "annotation_status": "explicit"}],
        "requirements": [{
            "requirement_id": "req-1", "request_part_id": "part-1", "requirement_type": "explicit",
            "dimensions": [], "admissible_alternatives": [], "forbidden_contradictions": [],
            "annotation_rationale": "Synthetic requirement."
        }],
        "ambiguities": [], "annotation_notes": "", "review_status": "adjudicated",
        "freeze_status": "frozen", "freeze_timestamp": "2026-10-28T11:00:00Z",
        "schema_version": "relational_gold_e_case_v2",
    }


def quality_judgements():
    judgement = {"status": "fail", "rationale": "Deliberately wrong synthetic answer.", "confidence": "high"}
    return {name: copy.deepcopy(judgement) for name in ("completeness", "relational_coherence", "tactical_correctness", "documentary_support")}


def gold_v_case(status="completed_evaluable"):
    evaluable = status == "completed_evaluable"
    case = {
        "case_id": "v-1", "attempt_id": "attempt-1", "run_id": "run-1",
        "input_reference": {"gold_e_manifest_sha256": H, "gold_e_case_id": "e-1", "path": "input-1.json", "input_sha256": H},
        "generation_configuration": {"configuration_id": "config-1", "path": "config-1.json", "configuration_sha256": H},
        "generation_result": {
            "status": status, "started_at": "2026-10-28T12:00:00Z", "completed_at": "2026-10-28T12:00:01Z",
            "elapsed_ms": 1000, "diagnostic": None if evaluable else {"code": status},
            "technical_review": {"status": "not_reviewed" if evaluable else "confirmed", "reviewer_id": None if evaluable else "reviewer-1", "reviewed_at": None if evaluable else "2026-10-28T12:05:00Z"},
        },
        "gold_e_case_id": "e-1", "gold_e_requirement_ids": ["req-1"],
        "answer": "A deliberately wrong but available answer." if evaluable else None,
        "answer_sha256": MODULE.sha256_document("A deliberately wrong but available answer.") if evaluable else None,
        "evidence": [],
        "relation_judgements": [{
            "requirement_id": "req-1", "status": "contradicted", "actor_task": "incorrect",
            "phase_trigger": "incorrect", "space": "incorrect", "purpose": "incorrect",
            "polarity": "affirmed", "team_scope": "wrong_scope", "answer_span": "wrong",
            "rationale": "Synthetic failure.", "evidence_ids": []
        }] if evaluable else [],
        "quality_judgements": quality_judgements() if evaluable else None,
        "annotation_version": "instructions-1",
        "adjudication_record_id": "adj-v-1" if evaluable else None,
        "annotation_status": "adjudicated" if evaluable else "not_applicable",
        "freeze_status": "frozen", "freeze_timestamp": "2026-10-28T13:00:00Z",
        "schema_version": "relational_gold_v_case_v2",
    }
    return case


class RelationalGoldPreparationV2Tests(unittest.TestCase):
    def setUp(self):
        self.provenance = {"schema_version": "relational_gold_provenance_registry_v2", "registry_version": "1.0.0", "status": "frozen", "records": [provenance_record()]}
        self.ledger_e = {"schema_version": "relational_gold_annotation_ledger_v2", "ledger_version": "1.0.0", "dataset_kind": "gold_e", "dataset_version": "1.0.0", "status": "frozen", "records": [ledger_record("adj-e-1", "e-1", "gold_e_case")]}
        self.ledger_v = {"schema_version": "relational_gold_annotation_ledger_v2", "ledger_version": "1.0.0", "dataset_kind": "gold_v", "dataset_version": "1.0.0", "status": "frozen", "records": [ledger_record("adj-v-1", "v-1", "gold_v_answer")]}
        self.gold_e = {"schema_version": "relational_gold_e_v2", "dataset_kind": "gold_e", "dataset_version": "1.0.0", "status": "frozen", "cases": [gold_e_case()]}
        self.gold_v = {
            "schema_version": "relational_gold_v_v2", "dataset_kind": "gold_v", "dataset_version": "1.0.0", "status": "frozen",
            "gold_e_reference": {"dataset_version": "1.0.0", "manifest_sha256": H, "freeze_status": "frozen"},
            "expected_attempt_ids": ["attempt-1"], "cases": [gold_v_case()],
        }
        self.ledger_e["records"][0]["annotated_object"]["artifact_version"] = self.gold_e["cases"][0]["annotation_version"]
        self.ledger_e["records"][0]["annotated_object"]["artifact_sha256"] = MODULE.sha256_document(MODULE.normatively_order(self.gold_e["cases"][0]))
        self.ledger_v["records"][0]["annotated_object"]["artifact_version"] = self.gold_v["cases"][0]["annotation_version"]
        self.ledger_v["records"][0]["annotated_object"]["artifact_sha256"] = MODULE.sha256_document(self.gold_v["cases"][0]["answer"])

    def _write_json(self, root, name, value):
        path = Path(root) / name
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _frozen_manifest(self, kind, dataset_name, dataset, dependencies):
        id_field = "attempt_id" if kind == "gold_v" else "case_id"
        return {
            "schema_version": "relational_gold_freeze_manifest_v2",
            "manifest_status": "frozen",
            "dataset": {"kind": kind, "version": "1.0.0", "path": dataset_name, "sha256": MODULE.sha256_document(MODULE.normatively_order(dataset))},
            "canonicalization": "RFC 8785 restricted to null, booleans, I-JSON integers, valid Unicode strings, arrays and objects; floats rejected",
            "normative_ordering": {},
            "case_count": len(dataset["cases"]),
            "cases": [{id_field: case[id_field], "sha256": MODULE.sha256_document(MODULE.normatively_order(case))} for case in dataset["cases"]],
            "dependencies": dependencies,
            "frozen_at": "2026-10-28T14:00:00Z",
            "parent_manifest_sha256": None,
            "supersedes_manifest_sha256": None,
            "immutable_after_freeze": True,
        }

    def _write_complete_freeze_bundle(self, root, duplicate_case_attempt=False):
        root = Path(root)
        self._write_json(root, "registry.json", self.provenance)
        self._write_json(root, "ledger-e.json", self.ledger_e)
        self._write_json(root, "gold-e.json", self.gold_e)
        manifest_e = self._frozen_manifest("gold_e", "gold-e.json", self.gold_e, [
            {"dependency_type": "provenance_registry", "schema_version": "relational_gold_provenance_registry_v2", "artifact_version": "1.0.0", "path": "registry.json", "sha256": MODULE.sha256_document(MODULE.normatively_order(self.provenance)), "access_class": "restricted"},
            {"dependency_type": "annotation_ledger", "schema_version": "relational_gold_annotation_ledger_v2", "artifact_version": "1.0.0", "path": "ledger-e.json", "sha256": MODULE.sha256_document(MODULE.normatively_order(self.ledger_e)), "access_class": "restricted"},
        ])
        self._write_json(root, "manifest-e.json", manifest_e)
        manifest_e_hash = MODULE.sha256_document(MODULE.normatively_order(manifest_e))

        input_doc = {"case_id": "e-1", "prompt": "synthetic"}
        config_doc = {"model": "synthetic", "temperature": 0}
        self._write_json(root, "input-1.json", input_doc)
        self._write_json(root, "config-1.json", config_doc)
        gold_v = copy.deepcopy(self.gold_v)
        gold_v["gold_e_reference"]["manifest_sha256"] = manifest_e_hash
        first = gold_v["cases"][0]
        first["input_reference"]["gold_e_manifest_sha256"] = manifest_e_hash
        first["input_reference"]["input_sha256"] = MODULE.sha256_document(MODULE.normatively_order(input_doc))
        first["generation_configuration"]["configuration_sha256"] = MODULE.sha256_document(MODULE.normatively_order(config_doc))
        ledger_v = copy.deepcopy(self.ledger_v)
        if duplicate_case_attempt:
            second = copy.deepcopy(first)
            second["attempt_id"] = "attempt-2"
            second["run_id"] = "run-2"
            second["adjudication_record_id"] = "adj-v-2"
            gold_v["cases"].append(second)
            gold_v["expected_attempt_ids"].append("attempt-2")
            second_ledger = copy.deepcopy(ledger_v["records"][0])
            second_ledger["adjudication_record_id"] = "adj-v-2"
            ledger_v["records"].append(second_ledger)
        self._write_json(root, "gold-v.json", gold_v)
        self._write_json(root, "ledger-v.json", ledger_v)
        manifest_v = self._frozen_manifest("gold_v", "gold-v.json", gold_v, [
            {"dependency_type": "gold_e_manifest", "schema_version": "relational_gold_freeze_manifest_v2", "artifact_version": "1.0.0", "path": "manifest-e.json", "sha256": manifest_e_hash, "access_class": "restricted"},
            {"dependency_type": "annotation_ledger", "schema_version": "relational_gold_annotation_ledger_v2", "artifact_version": "1.0.0", "path": "ledger-v.json", "sha256": MODULE.sha256_document(MODULE.normatively_order(ledger_v)), "access_class": "restricted"},
        ])
        manifest_v_path = self._write_json(root, "manifest-v.json", manifest_v)
        return manifest_v_path, manifest_e, gold_v, ledger_v

    def test_01_repository_contracts_are_valid_empty_and_v1_is_immutable(self):
        self.assertEqual(MODULE.validate_repository_preparation(ROOT), [])

    def test_02_rfc8785_profile_is_deterministic_and_normative_arrays_are_sorted(self):
        self.assertEqual(MODULE.canonicalize_rfc8785({"b": 1, "a": "€"}), '{"a":"€","b":1}'.encode())
        one = {"cases": [{"case_id": "z"}, {"case_id": "a"}]}
        two = {"cases": [{"case_id": "a"}, {"case_id": "z"}]}
        self.assertEqual(MODULE.sha256_document(MODULE.normatively_order(one)), MODULE.sha256_document(MODULE.normatively_order(two)))
        with self.assertRaisesRegex(ValueError, "FLOAT_NOT_ALLOWED"):
            MODULE.canonicalize_rfc8785(1.5)

    def test_03_provenance_requires_unique_ids_and_verified_available_rights(self):
        duplicate = copy.deepcopy(self.provenance)
        duplicate["records"].append(copy.deepcopy(duplicate["records"][0]))
        self.assertTrue(any(error.startswith("PROVENANCE_DUPLICATE_ID") for error in MODULE.validate_provenance_registry(duplicate, True)))
        revoked = copy.deepcopy(self.provenance)
        revoked["records"][0]["rights"]["revocation_status"] = "revoked"
        self.assertTrue(any(error.startswith("PROVENANCE_NOT_ACTIVE") for error in MODULE.validate_provenance_registry(revoked, True)))
        unavailable = copy.deepcopy(self.provenance)
        unavailable["records"][0]["rights"]["rights_evidence_ref"]["availability_check"]["status"] = "unavailable"
        self.assertTrue(any(error.startswith("RIGHTS_EVIDENCE_NOT_VERIFIED") for error in MODULE.validate_provenance_registry(unavailable, True)))
        expired = copy.deepcopy(self.provenance)
        expired["records"][0]["rights"]["expires_at"] = "2026-10-27T00:00:00Z"
        self.assertTrue(any(error.startswith("PROVENANCE_EXPIRED") for error in MODULE.validate_provenance_registry(expired, True, "2026-10-28T00:00:00Z")))

    def test_04_gold_e_resolves_provenance_request_parts_and_ledger(self):
        ledger = {item["adjudication_record_id"]: item for item in self.ledger_e["records"]}
        self.assertEqual(MODULE.validate_gold_e(self.gold_e, {"prov-1"}, ledger, True), [])
        broken = copy.deepcopy(self.gold_e)
        broken["cases"][0]["requirements"][0]["request_part_id"] = "missing"
        self.assertTrue(any(error.startswith("GOLD_E_REQUEST_PART_MISSING") for error in MODULE.validate_gold_e(broken, {"prov-1"}, ledger, True)))

    def test_05_all_expected_attempts_are_present_once(self):
        gold = {"e-1": self.gold_e["cases"][0]}
        ledger = {item["adjudication_record_id"]: item for item in self.ledger_v["records"]}
        self.assertEqual(MODULE.validate_gold_v(self.gold_v, gold, ledger, True), [])
        missing = copy.deepcopy(self.gold_v)
        missing["expected_attempt_ids"].append("attempt-2")
        self.assertIn("GOLD_V_ATTEMPT_DENOMINATOR_MISMATCH", MODULE.validate_gold_v(missing, gold, ledger, True))
        duplicate = copy.deepcopy(self.gold_v)
        duplicate["cases"].append(copy.deepcopy(duplicate["cases"][0]))
        self.assertTrue(any(error.startswith("GOLD_V_DUPLICATE_ATTEMPT") for error in MODULE.validate_gold_v(duplicate, gold, ledger, True)))

    def test_06_non_evaluable_attempts_forbid_tactical_annotations(self):
        case = gold_v_case("timeout")
        dataset = copy.deepcopy(self.gold_v)
        dataset["cases"] = [case]
        gold = {"e-1": self.gold_e["cases"][0]}
        self.assertEqual(MODULE.validate_gold_v(dataset, gold, {}, True), [])
        dataset["cases"][0]["answer"] = "fabricated"
        self.assertTrue(any(error.startswith("GOLD_V_NON_EVALUABLE_HAS_ANNOTATION") for error in MODULE.validate_gold_v(dataset, gold, {}, True)))

    def test_07_wrong_but_available_answer_remains_evaluable(self):
        gold = {"e-1": self.gold_e["cases"][0]}
        ledger = {item["adjudication_record_id"]: item for item in self.ledger_v["records"]}
        self.assertEqual(MODULE.validate_gold_v(self.gold_v, gold, ledger, True), [])
        self.assertEqual(self.gold_v["cases"][0]["quality_judgements"]["tactical_correctness"]["status"], "fail")

    def test_08_unknown_gold_e_requirement_is_rejected(self):
        broken = copy.deepcopy(self.gold_v)
        broken["cases"][0]["gold_e_requirement_ids"] = ["missing"]
        gold = {"e-1": self.gold_e["cases"][0]}
        ledger = {item["adjudication_record_id"]: item for item in self.ledger_v["records"]}
        self.assertTrue(any(error.startswith("GOLD_V_REQUIREMENT_MISSING") for error in MODULE.validate_gold_v(broken, gold, ledger, True)))

    def test_09_frozen_ledger_requires_independent_a_b_exact_object_and_c(self):
        self.assertEqual(MODULE.validate_annotation_ledger(self.ledger_e, True), [])
        broken = copy.deepcopy(self.ledger_e)
        broken["records"][0]["annotation_b"]["annotator_id"] = "annotator-a"
        broken["records"][0]["annotated_object"]["artifact_sha256"] = ""
        errors = MODULE.validate_annotation_ledger(broken, True)
        self.assertTrue(any(error.startswith("LEDGER_ANNOTATORS_NOT_INDEPENDENT") for error in errors))
        self.assertTrue(any(error.startswith("LEDGER_OBJECT_IDENTITY_INCOMPLETE") for error in errors))

    def test_10_manifest_resolves_hashes_dependencies_and_rejects_cycles(self):
        artifacts = {"gold-e.json": self.gold_e, "registry.json": self.provenance, "ledger-e.json": self.ledger_e}
        manifest = {
            "schema_version": "relational_gold_freeze_manifest_v2", "manifest_status": "frozen",
            "dataset": {"kind": "gold_e", "version": "1.0.0", "path": "gold-e.json", "sha256": MODULE.sha256_document(MODULE.normatively_order(self.gold_e))},
            "canonicalization": "RFC 8785 restricted to null, booleans, I-JSON integers, valid Unicode strings, arrays and objects; floats rejected",
            "normative_ordering": {}, "case_count": 1, "cases": [{"case_id": "e-1", "sha256": MODULE.sha256_document(MODULE.normatively_order(self.gold_e["cases"][0]))}],
            "dependencies": [
                {"dependency_type": "provenance_registry", "schema_version": "v2", "artifact_version": "1.0.0", "path": "registry.json", "sha256": MODULE.sha256_document(MODULE.normatively_order(self.provenance)), "access_class": "restricted"},
                {"dependency_type": "annotation_ledger", "schema_version": "v2", "artifact_version": "1.0.0", "path": "ledger-e.json", "sha256": MODULE.sha256_document(MODULE.normatively_order(self.ledger_e)), "access_class": "restricted"},
            ],
            "frozen_at": "2026-10-28T14:00:00Z", "parent_manifest_sha256": None, "supersedes_manifest_sha256": None, "immutable_after_freeze": True,
        }
        self.assertEqual(MODULE.validate_manifest(manifest, artifacts), [])
        bad = copy.deepcopy(manifest)
        bad["dependencies"][0]["sha256"] = H
        self.assertTrue(any(error.startswith("MANIFEST_DEPENDENCY_HASH_MISMATCH") for error in MODULE.validate_manifest(bad, artifacts)))
        graph = {"m1": {"dependencies": [{"dependency_type": "gold_e_manifest", "sha256": "m2"}]}, "m2": {"dependencies": [{"dependency_type": "gold_e_manifest", "sha256": "m1"}]}}
        self.assertEqual(MODULE.validate_manifest_graph(graph), ["MANIFEST_DEPENDENCY_CYCLE"])

    def test_11_evaluable_answer_requires_content_and_hash(self):
        broken = copy.deepcopy(self.gold_v)
        broken["cases"][0]["answer"] = ""
        broken["cases"][0]["answer_sha256"] = None
        gold = {"e-1": self.gold_e["cases"][0]}
        ledger = {item["adjudication_record_id"]: item for item in self.ledger_v["records"]}
        self.assertTrue(any(error.startswith("GOLD_V_EVALUABLE_ANSWER_MISSING") for error in MODULE.validate_gold_v(broken, gold, ledger, True)))

    def test_12_v2_contract_is_not_wired_into_runtime_or_panel(self):
        paths = [ROOT / "scripts" / "run_rag_v5_query.py", ROOT / "api" / "rag_v5_api.py"]
        for path in paths:
            if path.exists():
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("relational_gold_e_v2", text)
                self.assertNotIn("validate_relational_gold_preparation_v2", text)

    def test_13_complete_freeze_path_invokes_all_referential_validators(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_v_path, _, _, _ = self._write_complete_freeze_bundle(tmp)
            self.assertEqual(MODULE.validate_freeze_manifest_path(manifest_v_path), [])

    def test_14_gold_v_manifest_uses_attempt_id_for_multiple_attempts_of_same_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_v_path, _, _, _ = self._write_complete_freeze_bundle(tmp, duplicate_case_attempt=True)
            manifest = json.loads(manifest_v_path.read_text(encoding="utf-8"))
            self.assertEqual([item["attempt_id"] for item in manifest["cases"]], ["attempt-1", "attempt-2"])
            self.assertEqual(MODULE.validate_freeze_manifest_path(manifest_v_path), [])

    def test_15_freeze_recalculates_input_configuration_and_answer_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_v_path, _, gold_v, ledger_v = self._write_complete_freeze_bundle(tmp)
            gold_v["cases"][0]["input_reference"]["input_sha256"] = H
            gold_v["cases"][0]["generation_configuration"]["configuration_sha256"] = H
            gold_v["cases"][0]["answer_sha256"] = H
            self._write_json(tmp, "gold-v.json", gold_v)
            manifest = json.loads(manifest_v_path.read_text(encoding="utf-8"))
            manifest["dataset"]["sha256"] = MODULE.sha256_document(MODULE.normatively_order(gold_v))
            manifest["cases"][0]["sha256"] = MODULE.sha256_document(MODULE.normatively_order(gold_v["cases"][0]))
            self._write_json(tmp, "manifest-v.json", manifest)
            errors = MODULE.validate_freeze_manifest_path(manifest_v_path)
            self.assertTrue(any(error.startswith("GOLD_V_INPUT_HASH_MISMATCH") for error in errors))
            self.assertTrue(any(error.startswith("GOLD_V_CONFIGURATION_HASH_MISMATCH") for error in errors))
            self.assertTrue(any(error.startswith("GOLD_V_ANSWER_HASH_MISMATCH") for error in errors))

    def test_16_gold_e_manifest_hash_must_match_dataset_and_every_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_v_path, _, gold_v, _ = self._write_complete_freeze_bundle(tmp)
            gold_v["gold_e_reference"]["manifest_sha256"] = H
            gold_v["cases"][0]["input_reference"]["gold_e_manifest_sha256"] = "b" * 64
            self._write_json(tmp, "gold-v.json", gold_v)
            manifest = json.loads(manifest_v_path.read_text(encoding="utf-8"))
            manifest["dataset"]["sha256"] = MODULE.sha256_document(MODULE.normatively_order(gold_v))
            manifest["cases"][0]["sha256"] = MODULE.sha256_document(MODULE.normatively_order(gold_v["cases"][0]))
            self._write_json(tmp, "manifest-v.json", manifest)
            errors = MODULE.validate_freeze_manifest_path(manifest_v_path)
            self.assertIn("GOLD_V_GOLD_E_REFERENCE_MISMATCH", errors)
            self.assertTrue(any(error.startswith("GOLD_V_INPUT_MANIFEST_MISMATCH") for error in errors))

    def test_17_joint_freeze_rejects_non_frozen_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_v_path, _, _, ledger_v = self._write_complete_freeze_bundle(tmp)
            ledger_v["status"] = "annotation_in_progress"
            self._write_json(tmp, "ledger-v.json", ledger_v)
            manifest = json.loads(manifest_v_path.read_text(encoding="utf-8"))
            dependency = next(item for item in manifest["dependencies"] if item["dependency_type"] == "annotation_ledger")
            dependency["sha256"] = MODULE.sha256_document(MODULE.normatively_order(ledger_v))
            self._write_json(tmp, "manifest-v.json", manifest)
            self.assertIn("FREEZE_COMPONENT_STATE_INVALID", MODULE.validate_freeze_manifest_path(manifest_v_path))

    def test_18_cli_executes_complete_freeze_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_v_path, _, _, _ = self._write_complete_freeze_bundle(tmp)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(ROOT), "--freeze-manifest", str(manifest_v_path)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("STATUS V2_FREEZE_VALID", result.stdout)


if __name__ == "__main__":
    unittest.main()
