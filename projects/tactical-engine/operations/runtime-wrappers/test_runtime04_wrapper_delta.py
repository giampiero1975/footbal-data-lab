"""New offline tests of the embedded verifier, never of the wrapper runtime."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
sys.path.insert(0, str(PROJECT / "scripts"))
import v5_tactical_semantic_support_s2_spatial_v2_extraction as extraction
from prepare_runtime04_wrapper import (
    ORIGINAL, OUTPUT, DIFF, ORIGINAL_SHA256, BASELINE, adapted_bytes,
)


def python_blocks(data):
    return re.findall(r"<<'PY'\n(.*?)^PY$", data.decode(), re.M | re.S)


def verifier(data):
    return next(block for block in python_blocks(data)
                if "def require_diagnostic_provenance(" in block)


def existing_fixture_helpers():
    # Reuse fixture data/helpers only. Do not import or run the historical suite.
    source = PROJECT / "tests/test_v5_tactical_semantic_support_s2_spatial_v2_extraction.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    names = {"CLAIM", "EVIDENCE", "fragment_slot", "relation", "valid_extraction"}
    nodes = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name in names) or
             (isinstance(node, ast.Assign) and any(
                 isinstance(t, ast.Name) and t.id in names for t in node.targets))]
    assert len(nodes) == 5
    namespace = {"extraction": extraction}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), "exec"), namespace)
    return namespace


FIXTURE = existing_fixture_helpers()


class Runtime04WrapperDeltaTests(unittest.TestCase):
    def valid(self):
        return FIXTURE["valid_extraction"]()

    def semantic(self):
        value = self.valid()
        value["claim_relation"]["value"]["value"] = "between"
        return value

    def verify(self, value, *, original=False, mutate=None, gold="contradicted"):
        claim, evidence = FIXTURE["CLAIM"], FIXTURE["EVIDENCE"]
        result = extraction.materialize_extraction(value, claim, evidence)
        records = {
            "input.json": {"claim": claim, "evidence": evidence, "gold_label": gold},
            "config.json": {"contract_id": extraction.CONTRACT_ID,
                            "contract_version": extraction.CONTRACT_VERSION,
                            "promotion_authorized": False},
            "result.json": result,
            "generation_record.json": {"transport_calls": 1, "transport_attempted": True,
                                       "response_received": True, "generation_completed": True,
                                       "promotion_authorized": False},
            "transport_state.json": {"transport_calls": 1, "attempted": True,
                                     "response_received": True, "generation_completed": True},
            "raw_response.json": {"done_reason": "stop", "message": {
                "content": json.dumps(value, ensure_ascii=False)}},
            "extraction.json": value,
            "provenance.json": copy.deepcopy(result["localization"]),
        }
        if result["witness"] is not None:
            records["witness.json"] = result["witness"]
        if result["validation"] is not None:
            records["validation.json"] = result["validation"]
        if mutate:
            mutate(records)
        with tempfile.TemporaryDirectory(prefix="runtime04-verifier-only-") as directory:
            artifact = Path(directory)
            for name, payload in records.items():
                (artifact / name).write_text(json.dumps(payload), encoding="utf-8")
            code = compile(verifier((ORIGINAL if original else OUTPUT).read_bytes()),
                           "<embedded-verifier-only>", "exec")
            with mock.patch.object(sys, "argv", ["verifier-only", str(PROJECT), directory]), \
                    mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")), \
                    mock.patch.object(subprocess, "Popen", side_effect=AssertionError("process forbidden")):
                exec(code, {"__name__": "__verifier_only__"})
            return json.loads((artifact / "decision.json").read_text())

    def test_original_and_complete_allowlisted_delta(self):
        before, after = ORIGINAL.read_bytes(), OUTPUT.read_bytes()
        self.assertEqual(len(before), 45964)
        self.assertEqual(hashlib.sha256(before).hexdigest(), ORIGINAL_SHA256)
        self.assertEqual(adapted_bytes(before), after)
        self.assertEqual(after.count(b"spatial-v2-extraction-locator-q3-04-runtime-04"), 3)
        for forbidden in (b"runtime-03", b"spatial-v2-extraction-locator-db3ad66"):
            self.assertNotIn(forbidden, after)
        self.assertIn(BASELINE.encode(), after)
        for path, blob in {
            "shadow_nli_spatial_relations_v2_inference.py": "8ac93d07341e1079ee3ca6ff98327a8391b7ab5f",
            "v5_tactical_semantic_support_s2_spatial_v2_extraction.py": "1a64827b26fb30758773049eedeb342a2bb826b2",
        }.items():
            actual = subprocess.check_output([
                "git", "rev-parse", BASELINE + ":projects/tactical-engine/scripts/" + path
            ], text=True).strip()
            self.assertEqual(actual, blob)
            self.assertIn(blob.encode(), after)
        self.assertEqual(subprocess.check_output([
            "git", "diff", BASELINE, "--", "projects/tactical-engine/scripts"
        ]), b"")
        import difflib
        expected = "".join(difflib.unified_diff(
            before.decode().splitlines(keepends=True), after.decode().splitlines(keepends=True),
            fromfile=ORIGINAL.name, tofile=OUTPUT.name,
        )).encode()
        self.assertEqual(DIFF.read_bytes(), expected)

    def test_launcher_and_remote_body_bash_syntax_only(self):
        data = OUTPUT.read_bytes()
        lines = data.splitlines(keepends=True)
        self.assertEqual(lines[0], b"ssh football-vps 'bash -s' <<'BASH'\n")
        self.assertEqual(lines[-1], b"BASH\n")
        self.assertEqual(data.count(b"\nBASH\n"), 1)
        bash = Path(r"C:\Program Files\Git\bin\bash.exe")
        self.assertTrue(bash.is_file())
        for label, content in (("launcher", data), ("remote body", b"".join(lines[1:-1]))):
            result = subprocess.run([str(bash), "--noprofile", "--norc", "-n"],
                                    input=content, capture_output=True)
            self.assertEqual(result.returncode, 0, label + ": " + result.stderr.decode())

    def test_all_embedded_python_blocks_compile_without_execution(self):
        old, new = python_blocks(ORIGINAL.read_bytes()), python_blocks(OUTPUT.read_bytes())
        self.assertGreater(len(new), 0)
        self.assertEqual(len(old), len(new))
        for index, block in enumerate(new):
            compile(block, "<embedded-python-" + str(index) + ">", "exec")
        self.assertEqual(sum(a != b for a, b in zip(old, new)), 2)

    def test_generation_lock_timeouts_and_finalization_unchanged(self):
        before, after = ORIGINAL.read_text(), OUTPUT.read_text()
        self.assertEqual(before[before.index("PHASE='bootstrap'"):before.index("# 5. SINGOLA GENERAZIONE")].replace("runtime-03", "runtime-04"),
                         after[after.index("PHASE='bootstrap'"):after.index("# 5. SINGOLA GENERAZIONE")])
        for block_old, block_new in zip(python_blocks(ORIGINAL.read_bytes()), python_blocks(OUTPUT.read_bytes())):
            if "def require_diagnostic_provenance(" not in block_old:
                self.assertEqual(block_old.replace("runtime-03", "runtime-04"), block_new)
        for text in ("timeout --signal=TERM --kill-after=15s 450s", "max_tokens=2048",
                     "q3_04_timeout_360=True", "extraction_locator=True",
                     "spatial-v2-extraction-locator.lock", "readonly MODEL='qwen3.5:9b'",
                     "readonly PYTHON='/usr/bin/python3'", "transport_calls != 1"):
            self.assertEqual(before.count(text), after.count(text))
            self.assertGreater(after.count(text), 0)
        self.assertEqual(before[before.index('decision_read_rc=$?'):], after[after.index('decision_read_rc=$?'):])

    def test_four_verifier_paths_are_distinct(self):
        schema = self.valid(); del schema["label"]
        localization = self.valid(); localization["claim_relation"]["subject"]["selected_fragments"] = ["missing"]
        cases = [(schema, "fail_closed_extraction_schema", 80),
                 (self.semantic(), "fail_closed_extraction_semantic", 80),
                 (localization, "fail_closed_localization", 80),
                 (self.valid(), "completed_evaluated_semantic_match", 0)]
        for value, classification, code in cases:
            with self.subTest(classification=classification):
                result = self.verify(value)
                self.assertEqual(result["classification"], classification)
                self.assertEqual(result["wrapper_exit_code"], code)
                self.assertFalse(result["promotion_authorized"])
                if code == 80:
                    self.assertIsNone(result["observed_label"])
                    self.assertIsNone(result["semantic_match"])

    def test_original_verifier_rejects_the_new_boundary(self):
        with self.assertRaisesRegex(ValueError, "localization reason code invalid"):
            self.verify(self.semantic(), original=True)
        result = self.verify(self.semantic())
        self.assertEqual(result["reason_codes"], ["E_EXTRACTION_SEMANTIC_INCONSISTENT"])
        self.assertEqual(result["evaluation_status"], "not_evaluable")

    def test_semantic_comparison_boundary_uses_versioned_details(self):
        value = self.valid(); value["comparison"]["value"] = "same"
        self.assertIn("E_EXTRACTION_COMPARISON_INCONSISTENT", [
            item["code"] for item in extraction.extraction_semantic_errors(value)])
        self.assertEqual(self.verify(value)["classification"], "fail_closed_extraction_semantic")

    def test_semantic_wrong_reason_is_rejected(self):
        def mutate(records):
            records["result.json"]["reason_codes"] = ["E_EXTRACTION_LOCALIZATION_NOT_UNIQUE"]
        with self.assertRaisesRegex(ValueError, "reason code invalid"):
            self.verify(self.semantic(), mutate=mutate)

    def test_semantic_missing_or_changed_details_are_rejected(self):
        for details in (None, [], [{"code": "invented", "path": "comparison"}]):
            with self.subTest(details=details):
                def mutate(records):
                    records["result.json"]["details"] = details
                with self.assertRaisesRegex(ValueError, "semantic diagnostics"):
                    self.verify(self.semantic(), mutate=mutate)

    def test_semantic_localization_records_or_provenance_tampering_rejected(self):
        for field, value in (("records", [{"side": "claim"}]),
                             ("extraction_sha256", "0" * 64),
                             ("record_sha256", "0" * 64)):
            with self.subTest(field=field):
                def mutate(records):
                    records["result.json"]["localization"][field] = value
                    records["provenance.json"][field] = value
                with self.assertRaises(ValueError):
                    self.verify(self.semantic(), mutate=mutate)

    def test_semantic_witness_or_validation_injection_is_rejected(self):
        for name in ("witness", "validation"):
            for artifact in (False, True):
                with self.subTest(name=name, artifact=artifact):
                    def mutate(records):
                        if artifact:
                            records[name + ".json"] = {}
                        else:
                            records["result.json"][name] = {}
                    with self.assertRaises(ValueError):
                        self.verify(self.semantic(), mutate=mutate)

    def test_semantic_promotion_or_evaluated_status_is_rejected(self):
        for name in ("config.json", "result.json", "generation_record.json"):
            with self.subTest(name=name):
                def mutate(records):
                    records[name]["promotion_authorized"] = True
                with self.assertRaisesRegex(ValueError, "promotion invariant"):
                    self.verify(self.semantic(), mutate=mutate)
        def mutate(records):
            records["result.json"]["evaluation_status"] = "evaluated"
        with self.assertRaisesRegex(ValueError, "semantic-invalid extraction was promoted"):
            self.verify(self.semantic(), mutate=mutate)

    def test_valid_witness_gold_mismatch_is_not_repaired(self):
        result = self.verify(self.valid(), gold="supported")
        self.assertEqual(result["wrapper_exit_code"], 81)
        self.assertEqual(result["classification"], "completed_evaluated_semantic_mismatch")
        self.assertEqual(result["observed_label"], "contradicted")
        self.assertFalse(result["semantic_match"])
        self.assertFalse(result["promotion_authorized"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
