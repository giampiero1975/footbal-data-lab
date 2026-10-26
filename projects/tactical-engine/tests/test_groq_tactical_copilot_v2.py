import importlib.util, json, sys, unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("copilot", ROOT / "scripts/groq_tactical_copilot_v2.py")
copilot = importlib.util.module_from_spec(spec); spec.loader.exec_module(copilot)


def cases():
    return [{"id": "case_01", "question": "q", "answer": "a",
             "evidence": [{"label": "F1", "text": "e"}]}]


def pass1():
    return {"reviews": [{"id": "case_01", "score": 7, "verdict": "REVISIONE",
        "answered_parts": ["x"], "missing_parts": [], "digressions": [], "confirmed_points": [],
        "findings": [{"finding_id": "f01", "kind": "POSSIBILE_LACUNA", "claim": "c",
                      "why": "w", "priority": 1, "needs_document_check": True}],
        "improvement_plan": ["m"], "retrieval_needs": ["r"]}], "limitations": []}


def pass2():
    return {"checks": [{"id": "case_01", "finding_id": "f01", "classification": "SUPPORTATO",
                         "evidence_labels": ["F1"], "rationale": "ok"}],
            "revised_answers": [{"id": "case_01", "answer": "Correzione [F1].",
                                  "applied_findings": ["f01"], "unresolved_findings": []}],
            "limitations": []}


class CopilotOfflineTests(unittest.TestCase):
    def test_pass1_excludes_evidence(self):
        request = copilot.build_pass1(cases())
        self.assertNotIn("evidence", request["messages"][1]["content"])
        self.assertTrue(request["response_format"]["json_schema"]["strict"])

    def test_pass1_semantic_gates(self):
        self.assertEqual(copilot.validate_pass1(pass1(), ["case_01"])["reviews"][0]["score"], 7)
        bad = pass1(); bad["reviews"][0]["verdict"] = "PASS"
        with self.assertRaises(ValueError): copilot.validate_pass1(bad, ["case_01"])

    def test_duplicate_findings_fail(self):
        bad = pass1(); bad["reviews"][0]["findings"] *= 2
        with self.assertRaises(ValueError): copilot.validate_pass1(bad, ["case_01"])

    def test_pass2_contains_evidence_and_findings(self):
        request = copilot.build_pass2(cases(), pass1())
        body = json.loads(request["messages"][1]["content"])
        self.assertEqual(body["cases"][0]["evidence"][0]["label"], "F1")
        self.assertEqual(body["cases"][0]["findings"][0]["finding_id"], "f01")

    def test_pass2_software_validates_labels(self):
        good = pass2()
        self.assertEqual(copilot.validate_pass2(good, cases(), pass1())["checks"][0]["classification"], "SUPPORTATO")
        bad = json.loads(json.dumps(good)); bad["checks"][0]["evidence_labels"] = ["F9"]
        with self.assertRaises(ValueError): copilot.validate_pass2(bad, cases(), pass1())

    def test_pass2_requires_complete_finding_coverage(self):
        with self.assertRaises(ValueError): copilot.validate_pass2({"checks": [], "limitations": []}, cases(), pass1())

    def test_revised_answer_citation_and_partition_fail_closed(self):
        bad = pass2(); bad["revised_answers"][0]["answer"] = "Inventata [F9]."
        with self.assertRaises(ValueError): copilot.validate_pass2(bad, cases(), pass1())

    def test_failure_reasons_are_redacted(self):
        http = urllib.error.HTTPError("https://example.invalid", 503, "secret body", {}, None)
        self.assertEqual(copilot.redacted_failure_reason(http), "GROQ_HTTP_503")
        self.assertEqual(copilot.redacted_failure_reason(ValueError("raw model content")),
                         "GROQ_INVALID_STRUCTURED_RESPONSE")

    def test_failure_report_contains_no_payload(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "failure.json"
            copilot.write_failure(output, "model", "GROQ_HTTP_429")
            saved = json.loads(output.read_text())
        self.assertEqual(saved["reason"], "GROQ_HTTP_429")
        self.assertFalse(saved["contains_prompt_or_evidence"])
        self.assertNotIn("cases", saved)
        bad = pass2(); bad["revised_answers"][0]["unresolved_findings"] = ["f01"]
        with self.assertRaises(ValueError): copilot.validate_pass2(bad, cases(), pass1())


if __name__ == "__main__": unittest.main()
