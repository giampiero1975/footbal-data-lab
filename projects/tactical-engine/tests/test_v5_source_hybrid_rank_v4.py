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

    def test_consolidation_reservation_keeps_conditions_and_tradeoff(self):
        module=load_module("v5_targeted_coverage_v1")
        candidate_rows=[
            {"id":"noise","source":"Other","headings":[],"fingerprint":"n"},
            {"id":"conditions","source":module.MANUAL,"headings":["Quando è opportuno"],"fingerprint":"c"},
            {"id":"tradeoff","source":module.MANUAL,"headings":["Pro e contro"],"fingerprint":"t"},
        ]
        selected,promoted=module.reserve_consolidation(
            candidate_rows,[10.0,0.2,0.1],{},
            "Quando consolidare anziché accelerare dopo la riconquista?",3
        )
        self.assertEqual(promoted,["conditions","tradeoff"])
        self.assertEqual([row["id"] for row in selected[:2]],promoted)

    def test_consolidation_filter_omits_defensive_phase(self):
        module=load_module("v5_targeted_coverage_v1")
        candidate_rows=[
            {"id":"conditions","source":module.MANUAL,"text":"palla non controllata"},
            {"id":"choice","source":module.MANUAL,"text":"consolidare se il recuperatore è pressato"},
            {"id":"defence","source":module.MANUAL,"text":"pressione organizzata e riconquista del territorio"},
            {"id":"foreign","source":"Other","text":"consolidare la difesa"},
        ]
        kept,excluded=module.filter_consolidation_context(
            "Consolidare anziché accelerare dopo la riconquista?",candidate_rows,["conditions"]
        )
        self.assertEqual([row["id"] for row in kept],["conditions","choice"])
        self.assertEqual(excluded,["defence","foreign"])

    def test_targeting_uses_question_concepts_not_locked_id(self):
        module=load_module("v5_targeted_coverage_v1")
        question="Confrontando Ussia e il manuale interno, quali condizioni favoriscono la pressione dopo la perdita?"
        self.assertEqual(module.target("arbitrary_id",question),(module.USSIA,17))
        self.assertEqual(module.target("fresh_03","Cosa dice il manuale interno sui moduli?"),(None,None))


class ScopedGuidanceTests(unittest.TestCase):
    def setUp(self):
        import types
        from unittest.mock import patch
        fake_modules = {
            "chromadb": types.ModuleType("chromadb"),
            "llama_index": types.ModuleType("llama_index"),
            "llama_index.embeddings": types.ModuleType("llama_index.embeddings"),
            "llama_index.embeddings.ollama": types.ModuleType("llama_index.embeddings.ollama"),
            "sentence_transformers": types.ModuleType("sentence_transformers"),
        }
        fake_modules["llama_index.embeddings.ollama"].OllamaEmbedding = object
        fake_modules["sentence_transformers"].CrossEncoder = object
        self.patch = patch.dict(sys.modules, fake_modules)
        self.patch.start()
        self.module = load_module("smoke_test_rag_v5_e2e")

    def tearDown(self):
        self.patch.stop()

    def test_post_loss_guidance_separates_general_pressing(self):
        guidance = self.module.scoped_guidance(
            "Quali condizioni favoriscono la pressione dopo la perdita?"
        )
        self.assertIn("riaggressione immediata dopo perdita", guidance)
        self.assertIn("non usare fuorigioco", guidance)

    def test_unrelated_question_has_no_guidance(self):
        self.assertEqual(self.module.scoped_guidance("Come creare ampiezza?"), "")

    def test_lateral_zone_guidance_requires_complete_prudent_attribution(self):
        guidance = self.module.scoped_guidance(
            "Perché sono rischiosi i laterali nella zona B e che ruolo ha la pressione a invito?"
        )
        self.assertIn("playmaker braccati", guidance)
        self.assertIn("non attribuire il pericolo all'avversario", guidance.casefold())
        self.assertIn("divieto universale", guidance)

    def test_qualitative_efficacy_guidance_requires_comparative_limit(self):
        guidance=self.module.scoped_guidance(
            "Quale limite ha l'affermazione sulla maggiore efficacia della zona alta?"
        )
        self.assertIn("giudizio qualitativo",guidance)
        self.assertIn("misure o percentuali",guidance)
        self.assertIn("non sostituire",guidance.casefold())

    def test_post_loss_context_omits_general_pressing(self):
        rows = [
            {"id": "promoted", "text": "pressione individuale e collettiva"},
            {"id": "manual", "text": "palla persa vicino e copertura preventiva"},
            {"id": "offside", "text": "pressing alto e fuorigioco"},
            {"id": "throw", "text": "rimessa laterale"},
        ]
        kept, excluded = self.module.filter_post_loss_context(
            "pressione dopo la perdita", rows, ["promoted"]
        )
        self.assertEqual([row["id"] for row in kept], ["promoted", "manual"])
        self.assertEqual(excluded, ["offside", "throw"])

    def test_named_source_context_omits_foreign_taxonomy(self):
        rows = [
            {"id": "fos", "source": "manovre_offensive_vari_sistemi_gioco_Foscarini", "text": "zona B mediana"},
            {"id": "ind", "source": "palle_inattive_Indiani", "text": "zona B area di porta"},
        ]
        kept, excluded = self.module.filter_named_source_context(
            "Perché Foscarini considera rischiosa la zona B?", rows
        )
        self.assertEqual([row["id"] for row in kept], ["fos"])
        self.assertEqual(excluded, ["ind"])

    def test_named_source_context_preserves_comparisons(self):
        rows = [
            {"id": "ussia", "source": "Transizioni.Ussia", "text": "pressione"},
            {"id": "manual", "source": "Manuale", "text": "copertura"},
        ]
        kept, excluded = self.module.filter_named_source_context(
            "Confrontando Ussia e il manuale interno, quali condizioni valgono?", rows
        )
        self.assertEqual(kept, rows)
        self.assertEqual(excluded, [])


if __name__ == "__main__":
    unittest.main()
