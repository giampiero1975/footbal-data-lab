import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_rag_corpus_integrity_v1.py"
SPEC = importlib.util.spec_from_file_location("rag_corpus_integrity_v1", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class RagCorpusIntegrityV1Tests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.input_root = self.root / "input"
        self.input_root.mkdir()
        self.pdf = self.input_root / "docs" / "source.pdf"
        self.extraction = self.input_root / "processed" / "source.json"
        self.pdf.parent.mkdir()
        self.extraction.parent.mkdir()
        self.pdf.write_bytes(b"synthetic pdf bytes")
        self.text = "synthetic stored document"
        self.metadata = {
            "source_relative": "processed/source.json",
            "page_numbers": "[1]",
            "headings": "[\"Synthetic\"]",
        }
        self.synthetic_extraction = {
            "schema_version": "synthetic_docling_chunks_v1",
            "chunks": [{
                "chunk_id": "chunk-1",
                "document": self.text,
                "metadata": self.metadata,
                "pages": [1],
                "headings": ["Synthetic"],
            }],
        }
        self.extraction.write_text(
            json.dumps(self.synthetic_extraction, ensure_ascii=False), encoding="utf-8"
        )
        self.evidence_dir = self.input_root / "evidence"
        self.evidence_dir.mkdir()
        self.snapshot_evidence = self.evidence_dir / "snapshot.json"
        self.snapshot_evidence.write_bytes(b"synthetic consistent snapshot evidence")
        self.chunk = {
            "chunk_id": "chunk-1",
            "chunk_index": 0,
            "content_sha256": MODULE.sha256_bytes(self.text.encode("utf-8")),
            "raw_text_sha256": None,
            "metadata_sha256": MODULE.sha256_document(self.metadata),
            "pages": [1],
            "headings": ["Synthetic"],
            "source_relative": "processed/source.json",
            "chroma_presence": "present",
            "embedding_sha256": None,
            "verification_status": "verified",
        }
        pdf_hash = MODULE.sha256_file(self.pdf)
        self.document = {
            "source_ref": "source-1",
            "document_id": f"sha256:{pdf_hash}",
            "identity_evidence": {
                "basis": "current_verified",
                "evidence_ref": None,
                "evidence_sha256": None,
            },
            "original": {
                "relative_path": "docs/source.pdf",
                "size_bytes": self.pdf.stat().st_size,
                "sha256": pdf_hash,
                "verification_status": "verified",
            },
            "extraction": {
                "relative_path": "processed/source.json",
                "size_bytes": self.extraction.stat().st_size,
                "sha256": MODULE.sha256_file(self.extraction),
                "verification_status": "verified",
                "pipeline_name": "docling",
                "pipeline_version": "2",
                "docling_version": None,
                "docling_core_version": None,
                "configuration_sha256": None,
            },
            "bibliography": {"verification_status": "not_declared"},
            "rights": {"status": "unknown"},
            "chunks": [self.chunk],
        }
        self.manifest = {
            "schema_version": MODULE.SCHEMA_VERSION,
            "manifest_version": "1.0.0",
            "snapshot_id": "synthetic-snapshot-1",
            "snapshot_kind": "synthetic_fixture",
            "created_at": None,
            "created_by": "unit-test",
            "canonicalization": MODULE.CANONICALIZATION,
            "manifest_sha256": None,
            "collection": {
                "name": "synthetic-collection",
                "declared_version": "1",
                "chroma_version": None,
                "record_count": 1,
                "record_count_status": "verified",
                "inventory_completeness": "complete",
                "inventory_completeness_evidence_ref": "synthetic-inventory",
                "chunker_version": "synthetic-fixture-v1",
                "distance_metric": "cosine",
                "collection_metadata_sha256": None,
                "sorted_record_ids_sha256": None,
                "snapshot_consistency": {
                    "status": "certifiable",
                    "verification_status": "verified",
                    "method": "synthetic atomic fixture",
                    "evidence_ref": "evidence/snapshot.json",
                    "evidence_sha256": MODULE.sha256_file(self.snapshot_evidence),
                },
                "embedding": {
                    "model": None,
                    "model_digest": None,
                    "dimensions": None,
                    "vector_fingerprint_mode": "not_collected",
                },
            },
            "documents": [self.document],
            "parent_manifest_sha256": None,
            "supersedes_manifest_sha256": None,
        }
        self.snapshot = {
            "schema_version": MODULE.SNAPSHOT_SCHEMA_VERSION,
            "collection_name": "synthetic-collection",
            "records": [{"id": "chunk-1", "document": self.text, "metadata": self.metadata}],
        }

    def tearDown(self):
        self.temporary.cleanup()

    def report(self, manifest=None, snapshot=None, timestamp="2026-10-29T10:00:00Z"):
        return MODULE.verify_integrity(
            manifest or self.manifest,
            snapshot or self.snapshot,
            self.input_root,
            generated_at=timestamp,
        )

    @staticmethod
    def codes(report):
        return [item["code"] for item in report["verified_content"]["anomalies"]]

    def test_01_valid_document_chain(self):
        report = self.report()
        self.assertEqual(report["verified_content"]["integrity_status"], "verified")
        self.assertEqual(report["verified_content"]["anomalies"], [])
        self.assertEqual(report["verified_content"]["available_document_ids"], [self.document["document_id"]])

    def test_02_pdf_hash_mismatch(self):
        self.pdf.write_bytes(b"changed pdf bytes")
        report = self.report()
        self.assertIn("MISMATCH", self.codes(report))

    def test_03_inaccessible_pdf_keeps_historically_verified_identity(self):
        manifest = copy.deepcopy(self.manifest)
        history_evidence = self.evidence_dir / "history.json"
        history_evidence.write_bytes(b"synthetic historical identity evidence")
        identity = manifest["documents"][0]["identity_evidence"]
        identity.update({
            "basis": "historically_verified",
            "evidence_ref": "evidence/history.json",
            "evidence_sha256": MODULE.sha256_file(history_evidence),
        })
        manifest["documents"][0]["original"]["verification_status"] = "not_accessible"
        self.pdf.unlink()
        report = self.report(manifest)
        self.assertIn("NOT_ACCESSIBLE", self.codes(report))
        self.assertNotIn("METADATA_INCOMPLETE", self.codes(report))
        self.assertEqual(manifest["documents"][0]["document_id"], self.document["document_id"])

    def test_04_declared_hash_is_not_promoted_to_identity(self):
        manifest = copy.deepcopy(self.manifest)
        document = manifest["documents"][0]
        document["document_id"] = None
        document["identity_evidence"] = {
            "basis": "declared_only", "evidence_ref": None, "evidence_sha256": None
        }
        document["original"]["verification_status"] = "declared"
        report = self.report(manifest)
        self.assertIn("NOT_DECLARED", self.codes(report))
        self.assertNotIn("DOCUMENT_UNVERIFIED_ID_PROMOTED", str(report))

    def test_05_expected_chunk_missing(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["records"] = []
        manifest = copy.deepcopy(self.manifest)
        manifest["collection"]["record_count"] = 0
        report = self.report(manifest, snapshot)
        self.assertIn("MISSING_RECORD", self.codes(report))

    def test_06_orphan_requires_complete_inventory(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["records"].append({
            "id": "outside", "document": "outside", "metadata": self.metadata
        })
        manifest = copy.deepcopy(self.manifest)
        manifest["collection"]["record_count"] = 2
        report = self.report(manifest, snapshot)
        self.assertIn("ORPHAN_RECORD", self.codes(report))
        self.assertNotIn("UNRECONCILED_RECORD", self.codes(report))

    def test_07_partial_inventory_yields_unreconciled_record(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["records"].append({
            "id": "outside", "document": "outside", "metadata": self.metadata
        })
        manifest = copy.deepcopy(self.manifest)
        manifest["collection"]["record_count"] = 2
        manifest["collection"]["inventory_completeness"] = "partial"
        manifest["collection"]["inventory_completeness_evidence_ref"] = None
        report = self.report(manifest, snapshot)
        self.assertIn("UNRECONCILED_RECORD", self.codes(report))
        self.assertNotIn("ORPHAN_RECORD", self.codes(report))

    def test_08_duplicate_content_is_reported(self):
        manifest = copy.deepcopy(self.manifest)
        chunk = copy.deepcopy(self.chunk)
        chunk["chunk_id"] = "chunk-2"
        chunk["chunk_index"] = 1
        manifest["documents"][0]["chunks"].append(chunk)
        manifest["collection"]["record_count"] = 2
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["records"].append({
            "id": "chunk-2", "document": self.text, "metadata": self.metadata
        })
        report = self.report(manifest, snapshot)
        self.assertIn("DUPLICATE_CONTENT", self.codes(report))

    def test_09_incomplete_metadata_is_reported(self):
        snapshot = copy.deepcopy(self.snapshot)
        del snapshot["records"][0]["metadata"]["headings"]
        report = self.report(snapshot=snapshot)
        self.assertIn("METADATA_INCOMPLETE", self.codes(report))

    def test_10_unsupported_chunker_version_is_fail_closed(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["collection"]["chunker_version"] = "unknown-chunker-v99"
        report = self.report(manifest)
        self.assertIn("UNSUPPORTED_VERSION", self.codes(report))
        self.assertEqual(report["verified_content"]["integrity_status"], "not_verified")

    def test_11_technical_report_hash_ignores_timestamp(self):
        first = self.report(timestamp="2026-10-29T10:00:00Z")
        second = self.report(timestamp="2026-10-29T11:00:00Z")
        self.assertNotEqual(first["run_metadata"]["generated_at"], second["run_metadata"]["generated_at"])
        self.assertEqual(first["verified_content"], second["verified_content"])
        self.assertEqual(first["verified_content_sha256"], second["verified_content_sha256"])

    def test_12_uncertified_snapshot_is_not_certifiable(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["collection"]["snapshot_consistency"] = {
            "status": "not_certifiable", "verification_status": "not_declared",
            "method": None, "evidence_ref": None, "evidence_sha256": None
        }
        report = self.report(manifest)
        self.assertIn("SNAPSHOT_NOT_CERTIFIABLE", self.codes(report))
        self.assertEqual(report["verified_content"]["snapshot_certifiability"], "not_certifiable")

    def test_13_mutating_operations_are_refused(self):
        adapter = MODULE.ReadOnlySnapshotAdapter(self.snapshot)
        for name in MODULE.MUTATING_METHODS:
            with self.subTest(method=name):
                with self.assertRaisesRegex(RuntimeError, "READ_ONLY_ADAPTER_MUTATION_REFUSED"):
                    getattr(adapter, name)()

    def test_14_contract_artifacts_are_json_and_template_is_conservative(self):
        schema_path = ROOT / "evaluation" / "corpus_integrity" / "rag_corpus_integrity_manifest_schema_v1.json"
        template_path = ROOT / "evaluation" / "corpus_integrity" / "rag_corpus_integrity_manifest_template_v1.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        template = json.loads(template_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], MODULE.SCHEMA_VERSION)
        self.assertEqual(MODULE.validate_manifest_contract(template), [])
        self.assertEqual(template["collection"]["inventory_completeness"], "unknown")
        self.assertEqual(template["collection"]["snapshot_consistency"]["status"], "not_certifiable")

    def test_15_declared_manifest_and_record_id_hashes_are_verified(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["collection"]["sorted_record_ids_sha256"] = MODULE.sha256_document(["chunk-1"])
        manifest["manifest_sha256"] = MODULE.manifest_hash(manifest)
        self.assertEqual(self.report(manifest)["verified_content"]["integrity_status"], "verified")
        manifest["collection"]["sorted_record_ids_sha256"] = "b" * 64
        report = self.report(manifest)
        self.assertIn("MISMATCH", self.codes(report))

    def test_16_cli_writes_separate_deterministic_report(self):
        manifest_path = self.root / "manifest.json"
        snapshot_path = self.root / "snapshot.json"
        output_path = self.root / "reports" / "report.json"
        manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        snapshot_path.write_text(json.dumps(self.snapshot), encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--manifest", str(manifest_path),
                "--snapshot", str(snapshot_path),
                "--input-root", str(self.input_root),
                "--output", str(output_path),
                "--run-timestamp", "2026-10-29T10:00:00Z",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertTrue(output_path.is_file())
        report = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(report["verified_content"]["integrity_status"], "verified")
        self.assertEqual(report["run_metadata"]["generated_at"], "2026-10-29T10:00:00Z")

    def test_17_docling_to_chunk_derivation_mismatch(self):
        extraction = copy.deepcopy(self.synthetic_extraction)
        extraction["chunks"][0]["document"] = "different derived chunk"
        self.extraction.write_text(json.dumps(extraction), encoding="utf-8")
        manifest = copy.deepcopy(self.manifest)
        artifact = manifest["documents"][0]["extraction"]
        artifact["sha256"] = MODULE.sha256_file(self.extraction)
        artifact["size_bytes"] = self.extraction.stat().st_size
        report = self.report(manifest)
        self.assertIn("MISMATCH", self.codes(report))
        self.assertTrue(any(
            item["detail"] == "Docling-to-chunk content mismatch"
            for item in report["verified_content"]["anomalies"]
        ))

    def test_18_json_schema_required_types_enums_extra_properties_and_hashes(self):
        variants = []
        missing = copy.deepcopy(self.manifest)
        del missing["snapshot_id"]
        variants.append(missing)
        wrong_type = copy.deepcopy(self.manifest)
        wrong_type["collection"]["record_count"] = "one"
        variants.append(wrong_type)
        wrong_enum = copy.deepcopy(self.manifest)
        wrong_enum["collection"]["inventory_completeness"] = "maybe"
        variants.append(wrong_enum)
        extra = copy.deepcopy(self.manifest)
        extra["unexpected"] = True
        variants.append(extra)
        bad_hash = copy.deepcopy(self.manifest)
        bad_hash["documents"][0]["original"]["sha256"] = "not-a-hash"
        variants.append(bad_hash)
        for index, manifest in enumerate(variants):
            with self.subTest(variant=index):
                errors = MODULE.validate_manifest_contract(manifest)
                self.assertTrue(any(error.startswith("JSON_SCHEMA:") for error in errors), errors)

    def test_19_declared_snapshot_evidence_is_not_certifiable(self):
        manifest = copy.deepcopy(self.manifest)
        consistency = manifest["collection"]["snapshot_consistency"]
        consistency["verification_status"] = "declared"
        consistency["evidence_ref"] = "evidence/missing-snapshot.json"
        consistency["evidence_sha256"] = "a" * 64
        report = self.report(manifest)
        self.assertIn("SNAPSHOT_NOT_CERTIFIABLE", self.codes(report))

    def test_20_unresolvable_or_mismatched_historical_evidence_is_not_verified(self):
        manifest = copy.deepcopy(self.manifest)
        document = manifest["documents"][0]
        document["identity_evidence"] = {
            "basis": "historically_verified",
            "evidence_ref": "evidence/missing-history.json",
            "evidence_sha256": "a" * 64,
        }
        document["original"]["verification_status"] = "not_accessible"
        self.pdf.unlink()
        report = self.report(manifest)
        self.assertIn("NOT_ACCESSIBLE", self.codes(report))

        evidence = self.evidence_dir / "history.json"
        evidence.write_bytes(b"actual history")
        manifest["documents"][0]["identity_evidence"]["evidence_ref"] = "evidence/history.json"
        report = self.report(manifest)
        self.assertIn("MISMATCH", self.codes(report))

    def test_21_repeated_ids_remain_in_ordered_id_hash_and_are_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["records"].append(copy.deepcopy(snapshot["records"][0]))
        manifest = copy.deepcopy(self.manifest)
        manifest["collection"]["record_count"] = 2
        manifest["collection"]["sorted_record_ids_sha256"] = MODULE.sha256_document([
            "chunk-1", "chunk-1"
        ])
        report = self.report(manifest, snapshot)
        self.assertIn("METADATA_INCOMPLETE", self.codes(report))
        self.assertFalse(any(
            item["detail"] == "sorted_record_ids_sha256 mismatch"
            for item in report["verified_content"]["anomalies"]
        ))

    def test_22_real_chunker_without_exact_adapter_is_unverifiable(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["collection"]["chunker_version"] = "rag-v5-docling-hybrid-v1"
        report = self.report(manifest)
        self.assertIn("UNVERIFIABLE_RELATION", self.codes(report))
        self.assertEqual(report["verified_content"]["integrity_status"], "not_verified")


if __name__ == "__main__":
    unittest.main()
