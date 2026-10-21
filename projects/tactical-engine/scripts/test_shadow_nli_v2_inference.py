#!/usr/bin/env python3
"""Isolated orchestration tests: injected judge, no Ollama or Chroma."""
import copy
import unittest

from shadow_nli_v2_offline import prepare
from shadow_nli_v2_inference import evaluate, load_v2_instruction


class InferenceShadowTests(unittest.TestCase):
    def setUp(self):
        answer = "La squadra pressa alta [F1]."
        report = {"questions": [{"id": "q1", "answer": answer,
            "evidence": [{"label": "F1", "id": "chunk1", "text": "La squadra pressa alta."}]}]}
        claims = {"claims": [{"question_id": "q1", "claim_id": "c1",
            "text": "La squadra pressa alta", "span": answer,
            "start": 0, "end": len(answer)}]}
        self.prepared = prepare(report, claims)

    def test_canonical_v2_prompt(self):
        prompt = load_v2_instruction()
        self.assertIn("Regola decisiva:", prompt)
        self.assertIn("contradicted", prompt)

    def test_supported_and_immutable(self):
        before = copy.deepcopy(self.prepared)
        result = evaluate(self.prepared, lambda claim, evidence: "supported")
        self.assertEqual(result["claims"][0]["status"], "supported_by_cited_evidence")
        self.assertEqual(result["inference"]["completed"], 1)
        self.assertEqual(self.prepared, before)

    def test_judge_error_does_not_promote(self):
        def broken(claim, evidence):
            raise TimeoutError("model unavailable")
        result = evaluate(self.prepared, broken)
        self.assertEqual(result["claims"][0]["status"], "pending_nli")
        self.assertEqual(result["inference"]["completed"], 0)
        self.assertEqual(len(result["inference"]["errors"]), 1)

    def test_invalid_label_fails_closed(self):
        result = evaluate(self.prepared, lambda claim, evidence: "unknown")
        self.assertEqual(result["claims"][0]["status"], "pending_nli")
        self.assertEqual(len(result["inference"]["errors"]), 1)

    def test_limit_and_zero_no_calls(self):
        result = evaluate(self.prepared, lambda claim, evidence: "insufficient", max_pairs=1)
        self.assertEqual(result["inference"]["attempted"], 1)
        with self.assertRaises(ValueError):
            evaluate(self.prepared, lambda claim, evidence: "supported", max_pairs=-1)


if __name__ == "__main__":
    unittest.main()
