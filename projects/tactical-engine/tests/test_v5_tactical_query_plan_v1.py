import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("planner", ROOT / "scripts/v5_tactical_query_plan_v1.py")
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)


class TacticalQueryPlanTests(unittest.TestCase):
    CASES = [
        ("Transizione negativa: quando riaggressione immediata e quando ripiegamento? Valuta preventiva, zona e palla coperta o scoperta.", {"negative_transition", "prevention", "offside"}),
        ("Costruzione dal basso contro pressione uomo su uomo: rotazioni, liberazione spazi, terzo uomo, rischio e portiere.", {"possession", "third_man", "goalkeeper"}),
        ("Come difendere la porta su cross laterale: postura dei centrali, duello, traiettoria e coordinazione col portiere?", {"non_possession", "box", "goalkeeper"}),
        ("Scaglionamento offensivo contro blocco medio-basso: cinque corridoi, superiorità socio-affettiva e marcature preventive.", {"possession", "non_possession", "prevention", "five_lanes", "relational_superiority"}),
        ("Nel blocco medio-basso descrivi sotto-blocco e scivolamento sul cambio di gioco, lato debole e mediano.", {"non_possession", "width"}),
        ("In transizione negativa confronta contro-pressing orientato sull'uomo e sulle linee di passaggio con preventiva e ripiegamento.", {"negative_transition", "prevention"}),
        ("Come occupare la zona di rifinitura tra le linee con trequartisti, ali dentro e terzo uomo?", {"possession", "inside_space", "third_man"}),
        ("Costruzione alta contro blocco basso 5-4-1: cambio gioco, uno contro uno e occupazione area su cross.", {"possession", "non_possession", "width", "box"}),
        ("Come organizzi la trappola del fuorigioco su palla coperta o scoperta e quali comandi dà il leader?", {"non_possession", "offside", "communication"}),
        ("Quali sostituzioni e cambi di sistema preservano il vantaggio, considerando comunicazione, impatto emotivo ed equilibrio?", {"prevention", "substitutions", "communication", "psychology"}),
    ]

    def test_extracts_multiple_requested_facets(self):
        plan = planner.analyse(
            "Nel 4-3-3 descrivi costruzione dal basso contro pressione: ruolo del portiere, terzo uomo e marcatura preventiva."
        )
        self.assertIn("possession", plan["facets"])
        self.assertIn("goalkeeper", plan["facets"])
        self.assertIn("third_man", plan["facets"])
        self.assertIn("prevention", plan["facets"])
        self.assertEqual(plan["formations"], ["4-3-3"])

    def test_phase_adjustment_penalises_opposite_only(self):
        plan = planner.analyse("Come organizzi la fase di possesso e la costruzione?")
        attack = {"source": "a", "text": "fase di possesso costruzione e sviluppo", "headings": []}
        defence = {"source": "b", "text": "fase di non possesso blocco e difesa", "headings": []}
        self.assertGreater(planner.phase_adjustment(attack, plan), 0)
        self.assertLess(planner.phase_adjustment(defence, plan), 0)

    def test_diversification_excludes_opposite_only_evidence(self):
        plan = planner.analyse("In fase di possesso descrivi la costruzione e il portiere")
        rows = [
            {"id": "attack", "source": "a", "text": "costruzione in fase di possesso con portiere", "headings": []},
            {"id": "defence", "source": "d", "text": "fase di non possesso difesa e marcatura", "headings": []},
        ]
        revised, _, _ = planner.diversify(rows, [1, 9], rows[::-1], plan, 2)
        self.assertEqual([row["id"] for row in revised], ["attack"])

    def test_diversifies_facets_and_preserves_limit(self):
        plan = planner.analyse("Costruzione: portiere, terzo uomo e ampiezza")
        rows = [
            {"id": "generic", "source": "g", "text": "costruzione", "headings": []},
            {"id": "gk", "source": "p", "text": "portiere in costruzione", "headings": []},
            {"id": "third", "source": "t", "text": "terzo uomo", "headings": []},
            {"id": "wide", "source": "w", "text": "ampiezza e corsia laterale", "headings": []},
        ]
        revised, reserved, covered = planner.diversify(rows, [9, 2, 1, 0], [rows[0]], plan, 4)
        self.assertEqual(len(revised), 4)
        self.assertTrue({"goalkeeper", "third_man", "width"}.issubset(covered))
        self.assertEqual(set(reserved), {"gk", "third", "wide", "generic"})

    def test_contract_requires_operational_geometry(self):
        contract = planner.generation_contract(planner.analyse("Come difendi e quando ripieghi?"))
        for token in ("CHI", "COSA", "DOVE", "QUANDO", "PERCHE", "COPERTURA"):
            self.assertIn(token, contract)
        self.assertIn("squadra propria e avversario", contract)
        self.assertIn("non introdurre perdita", planner.generation_contract(
            planner.analyse("Descrivi la costruzione in fase di possesso")))

    def test_answer_audit_exposes_missing_facets(self):
        plan = planner.analyse("In costruzione descrivi portiere, terzo uomo e marcatura preventiva")
        audit = planner.audit_answer(
            "Il portiere serve il centrale quando la punta esce, così da creare spazio.", plan
        )
        self.assertIn("third_man", audit["missing_facets"])
        self.assertIn("prevention", audit["missing_facets"])
        self.assertFalse(audit["complete"])

    def test_negative_transition_audit_requires_decision_details(self):
        plan = planner.analyse("Come gestisci la transizione negativa e la marcatura preventiva?")
        audit = planner.audit_answer(
            "I giocatori vicini creano densità nella zona e mantengono la preventiva.", plan
        )
        self.assertIn("covered_or_uncovered_ball", audit["missing_details"])
        self.assertFalse(audit["complete"])
        queries = planner.retrieval_queries("Come gestisci la transizione negativa?", plan)
        self.assertTrue(any("palla coperta" in query and "marcatura preventiva" in query for query in queries))

    def test_frozen_ten_case_facets_are_not_silently_omitted(self):
        for question, expected in self.CASES:
            with self.subTest(question=question):
                self.assertTrue(expected.issubset(set(planner.analyse(question)["facets"])))

    def test_recognises_generic_scenarios_without_benchmark_ids(self):
        samples = {
            "build_out": "Costruzione dal basso contro pressing alto: portiere e terzo uomo.",
            "cross_defence": "Protezione della porta su cross con postura e portiere.",
            "lateral_shift": "Scivolamento del reparto dopo un cambio gioco.",
            "counterpress_deadline": "Nel contro-pressing qual e il tempo massimo?",
            "offside_trap": "Trappola del fuorigioco su palla inattiva.",
            "game_management": "Sostituzioni negli ultimi 15 minuti per difendere il vantaggio.",
        }
        for expected, question in samples.items():
            with self.subTest(expected=expected):
                self.assertIn(expected, planner.analyse(question)["scenarios"])

    def test_offside_audit_rejects_unsafe_generic_answer(self):
        plan = planner.analyse(
            "Trappola del fuorigioco: differenza tra palla scoperta e palla inattiva, comando del leader."
        )
        audit = planner.audit_answer(
            "Il leader dà il comando e la linea sale su palla scoperta; su palla inattiva resta alta.", plan
        )
        self.assertIn("uncovered_ball_drop", audit["missing_details"])
        self.assertIn("leader_and_keeper", audit["missing_details"])
        self.assertFalse(audit["complete"])

    def test_scenario_query_is_prioritised(self):
        plan = planner.analyse("Scivolamento del reparto su cambio gioco con mediano e lato debole.")
        queries = planner.retrieval_queries("Scivolamento del reparto su cambio gioco.", plan)
        self.assertIn("tempo volo", queries[1])
        self.assertIn("mediano schermo", queries[1])

    def test_scenario_exact_anchors_are_bounded(self):
        plan = planner.analyse(
            "Contro-pressing: indica il tempo massimo e la marcatura preventiva."
        )
        anchors = planner.retrieval_anchors(plan)
        self.assertIn("regola dei cinque secondi", anchors)
        self.assertLessEqual(len(anchors), 4)

    def test_lateral_shift_uses_discriminating_document_phrases(self):
        plan = planner.analyse("Scivolamento difensivo su cambio gioco.")
        anchors = planner.retrieval_anchors(plan)
        self.assertIn("punto critico è il tempo di volo", anchors)
        self.assertNotIn("tempo di volo", anchors)

    def test_anchor_reservation_keeps_semantic_order_and_source_diversity(self):
        rows = [
            {"id": "a", "source": "one"},
            {"id": "b", "source": "one"},
            {"id": "c", "source": "two"},
            {"id": "d", "source": "base"},
        ]
        revised, reserved = planner.reserve_anchor_candidates(
            rows, [8, 9, 7, 10], [rows[3], rows[0]], ["a", "b", "c"], 3
        )
        self.assertEqual(reserved, ["b", "c"])
        self.assertEqual([row["id"] for row in revised], ["b", "c", "d"])


if __name__ == "__main__":
    unittest.main()
