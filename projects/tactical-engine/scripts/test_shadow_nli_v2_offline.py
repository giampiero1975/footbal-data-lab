#!/usr/bin/env python3
"""Pure offline contract tests: no Ollama, Chroma, or production imports."""
import copy
import unittest
from shadow_nli_v2_offline import prepare, apply_verdicts

class ShadowOfflineTests(unittest.TestCase):
    def setUp(self):
        self.answer = "Pressing alto [F1]. Il pressing garantisce ogni recupero [F2]. Nota [F9]. Senza fonte."
        self.report = {"questions": [{"id": "q1", "answer": self.answer,
            "evidence": [{"label": "F1", "id": "a", "text": "La squadra pressa alta."},
                         {"label": "F2", "id": "b", "text": "Il pressing non garantisce il recupero."}]}]}

    def claim(self, cid, span):
        start = self.answer.index(span)
        return {"question_id": "q1", "claim_id": cid, "text": span,
                "span": span, "start": start, "end": start + len(span)}

    def test_statuses_and_source_immutability(self):
        original = copy.deepcopy(self.report)
        out = prepare(self.report, {"claims": [
            self.claim("a", "Pressing alto [F1]."),
            self.claim("b", "Il pressing garantisce ogni recupero [F2]."),
            self.claim("c", "Nota [F9]."),
            self.claim("d", "Senza fonte.")]})
        self.assertEqual(self.report, original)
        self.assertEqual([c["status"] for c in out["claims"]],
                         ["pending_nli", "pending_nli", "invalid_citation", "no_citation"])
        self.assertIsNone(out["claims"][0]["pairs"][0]["nli_label"])

    def test_verdict_replay_does_not_mutate_prepared(self):
        out = prepare(self.report, {"claims": [self.claim("b", "Il pressing garantisce ogni recupero [F2].")]})
        pair = out["claims"][0]["pairs"][0]
        result = apply_verdicts(out, {"verdicts": [{"question_id": "q1", "claim_id": "b",
            "source_id": "F2", "source_text_hash": pair["source_text_hash"],
            "nli_label": "contradicted"}]})
        self.assertEqual(result["claims"][0]["status"], "contradicted_by_cited_evidence")
        self.assertEqual(out["claims"][0]["status"], "pending_nli")

    def test_bad_hash_and_span_fail_closed(self):
        out = prepare(self.report, {"claims": [self.claim("a", "Pressing alto [F1].")]})
        with self.assertRaises(ValueError):
            apply_verdicts(out, {"verdicts": [{"question_id": "q1", "claim_id": "a",
                "source_id": "F1", "source_text_hash": "bad", "nli_label": "supported"}]})
        bad = self.claim("a", "Pressing alto [F1].")
        bad["start"] += 1
        with self.assertRaises(ValueError):
            prepare(self.report, {"claims": [bad]})

    def test_mismatched_claim_text_and_boolean_offsets_fail_closed(self):
        bad = self.claim("a", "Pressing alto [F1].")
        bad["text"] = "Il pressing garantisce ogni recupero"
        with self.assertRaises(ValueError):
            prepare(self.report, {"claims": [bad]})
        bad = self.claim("a", "Pressing alto [F1].")
        bad["start"] = True
        with self.assertRaises(ValueError):
            prepare(self.report, {"claims": [bad]})

    def test_multisource_conflict_requires_review(self):
        answer = "Azione combinata [F1] [F2]."
        report = copy.deepcopy(self.report)
        report["questions"][0]["answer"] = answer
        out = prepare(report, {"claims": [{"question_id": "q1", "claim_id": "a",
            "text": "Azione combinata", "span": answer, "start": 0, "end": len(answer)}]})
        verdicts = {"verdicts": [{"question_id": "q1", "claim_id": "a",
            "source_id": p["source_id"], "source_text_hash": p["source_text_hash"],
            "nli_label": label} for p, label in zip(out["claims"][0]["pairs"],
                                                   ["supported", "contradicted"])]}
        self.assertEqual(apply_verdicts(out, verdicts)["claims"][0]["status"],
                         "conflicting_evidence_review")

if __name__ == "__main__":
    unittest.main()
