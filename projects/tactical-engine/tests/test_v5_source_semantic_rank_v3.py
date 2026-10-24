"""Offline tests for inspectable V5 semantic source ranking."""
import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "v5_source_semantic_rank_v3.py"


def load_module():
    spec = importlib.util.spec_from_file_location("v5_source_semantic_rank_v3", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeReranker:
    def predict(self, pairs, batch_size, show_progress_bar):
        self.pairs = pairs
        return [0.25, 0.75]


class SemanticSourceRankingTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.rows = [
            {"source": "Manuale_A", "headings": ["4-3-3"], "text": "a"},
            {"source": "Manuale_A", "headings": ["4-4-2"], "text": "b"},
            {"source": "Manuale_B", "headings": ["3-5-2"], "text": "c"},
            {"source": "Manuale_B", "headings": ["3-4-2-1"], "text": "d"},
            {"source": "Other", "headings": ["4-3-3", "4-4-2"], "text": "ignored"},
        ]

    def test_ranking_is_sorted_and_inspectable(self):
        reranker = FakeReranker()
        ranking = self.module.semantic_source_ranking("domanda", self.rows, reranker)
        self.assertEqual([item["source"] for item in ranking], ["Manuale_B", "Manuale_A"])
        self.assertEqual(ranking[0]["score"], 0.75)
        self.assertEqual(ranking[0]["formations"], ["3-4-2-1", "3-5-2"])
        self.assertEqual(ranking[0]["profile_excerpt_count"], 2)

    def test_score_api_remains_compatible(self):
        scores = self.module.semantic_source_scores("domanda", self.rows, FakeReranker())
        self.assertEqual(scores, {"Manuale_B": 0.75, "Manuale_A": 0.25})


if __name__ == "__main__":
    unittest.main()
