"""Offline tests for coverage-aware V5 source selection."""
import importlib.util
from pathlib import Path
import sys
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def load_module(name):
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeReranker:
    def __init__(self, scores):
        self.scores = scores

    def predict(self, pairs, batch_size, show_progress_bar):
        return self.scores


def rows():
    result = []
    for source, formations in {
        "Manuale_A": ["4-2-3-1", "4-3-3", "4-4-2"],
        "Manuale_B": ["3-4-2-1", "3-5-2", "4-3-3", "4-4-2"],
        "Manuale_C": ["3-4-2-1", "3-5-2", "4-2-3-1", "4-3-3", "4-4-2"],
    }.items():
        result.extend({"source": source, "headings": [f], "text": f"testo {f}"} for f in formations)
    return result


class HybridSourceSelectionTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module("v5_source_hybrid_rank_v4")

    def test_prefers_coverage_inside_semantic_margin(self):
        source, trace = self.module.select_source(
            "domanda", rows(), FakeReranker([0.0, -1.2, -2.0])
        )
        self.assertEqual(source, "Manuale_B")
        self.assertTrue(trace[1]["competitive"])
        self.assertFalse(trace[2]["competitive"])

    def test_does_not_trade_away_large_semantic_gap(self):
        source, trace = self.module.select_source(
            "domanda", rows(), FakeReranker([0.0, -1.6, -2.0])
        )
        self.assertEqual(source, "Manuale_A")
        self.assertFalse(trace[1]["competitive"])

    def test_tie_keeps_better_semantic_score(self):
        candidate_rows = [row for row in rows() if row["source"] != "Manuale_A"]
        source, _ = self.module.select_source(
            "domanda", candidate_rows, FakeReranker([0.2, 0.1])
        )
        self.assertEqual(source, "Manuale_C")


if __name__ == "__main__":
    unittest.main()
