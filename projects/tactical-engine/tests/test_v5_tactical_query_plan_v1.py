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

    def test_offside_audit_detects_contradictory_mappings(self):
        plan = planner.analyse(
            "Trappola del fuorigioco: palla scoperta e palla inattiva, comando del leader."
        )
        answer = (
            "Su palla coperta la linea scappa; su palla scoperta sale. "
            "In seguito: su palla scoperta la linea scappa, mentre su palla coperta sale. "
            "Il leader chiama e il portiere copre; su palla inattiva si sale al momento del calcio. "
            + " La squadra protegge porta e profondità con postura coordinata." * 12
        )
        audit = planner.audit_answer(answer, plan)
        self.assertIn("covered_ball_mapped_to_drop", audit["semantic_issues"])
        self.assertIn("uncovered_ball_mapped_to_step", audit["semantic_issues"])
        self.assertFalse(audit["complete"])

    def test_offside_audit_accepts_drop_then_conditional_recovery(self):
        plan = planner.analyse(
            "Trappola del fuorigioco: palla scoperta e palla inattiva, comando del leader."
        )
        answer = (
            "Su palla scoperta la linea arretra insieme e risale soltanto dopo avere protetto la profondità. "
            "Su palla coperta sale al gesto tecnico leggibile. Il leader chiama e il portiere copre. "
            "Su palla inattiva si sale all'istante del calcio. "
            + " La squadra mantiene postura e copertura coordinate." * 20
        )
        audit = planner.audit_answer(answer, plan)
        self.assertNotIn("uncovered_ball_mapped_to_step", audit["semantic_issues"])

    def test_cross_attack_audit_rejects_defensive_phase_contamination(self):
        plan = planner.analyse(
            "Attacco su cross: primo palo, secondo palo, dischetto e fuori area."
        )
        answer = (
            "Primo palo, dischetto, secondo palo e limite area sono occupati. "
            "In difesa si usa postura semiaperta. Il portatore dà il segnale e la squadra attacca. "
            + " I giocatori coordinano corse e coperture preventive." * 15
        )
        audit = planner.audit_answer(answer, plan)
        self.assertIn("cross_attack_contaminated_by_defensive_phase", audit["semantic_issues"])
        self.assertFalse(audit["complete"])

    def test_scenario_audit_rejects_v9_contaminations(self):
        build = planner.analyse("Costruzione dal basso contro pressing alto con portiere e terzo uomo.")
        build_answer = "Il portiere crea superiorità, poi si attacca il primo palo con un cross. " * 20
        self.assertIn("build_out_contaminated_by_cross_attack",
                      planner.audit_answer(build_answer, build)["semantic_issues"])

        shift = planner.analyse("Sotto-blocco e scivolamento su cambio gioco con tempo di volo.")
        shift_answer = (
            "Il quinto scherma lo spazio di imbucata davanti alla difesa e il reparto scivola all'indietro. "
            "Il lato debole stringe, il lato forte esce e il mediano garantisce copertura. " * 15
        )
        issues = planner.audit_answer(shift_answer, shift)["semantic_issues"]
        self.assertIn("lateral_shift_mapped_to_vertical_drop", issues)
        self.assertIn("wide_defender_given_midfielder_screen", issues)

        management = planner.analyse("Sostituzioni negli ultimi 15 minuti e cambio del sistema di gioco.")
        management_answer = "Scambio simultaneo di tre giocatori con tre riserve, poi comando e copertura. " * 20
        self.assertIn("generic_triple_substitution",
                      planner.audit_answer(management_answer, management)["semantic_issues"])
        role_answer = "Due esterni difensivi entrano come centrocampisti centrali; comando e copertura. " * 20
        self.assertIn("incoherent_role_transformation",
                      planner.audit_answer(role_answer, management)["semantic_issues"])

        attack = planner.analyse("Attacco del cross con primo palo, dischetto, secondo palo e limite area.")
        numbered = "L'esterno, es. 7, serve il compagno, es. 10, al dischetto. " * 20
        self.assertIn("unsupported_rigid_player_numbers",
                      planner.audit_answer(numbered, attack)["semantic_issues"])

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


class RelationalAuditDifferentialTests(unittest.TestCase):
    def requirement(self, **overrides):
        item = {
            "requirement_id": "negative_transition_cover",
            "required_dimensions": ["actor", "phase", "task", "space", "trigger", "purpose"],
            "actor_terms": ["centrale"],
            "phase_terms": ["transizione negativa"],
            "task_terms": ["copre"],
            "space_terms": ["profondità"],
            "trigger_terms": ["alla perdita"],
            "purpose_terms": ["per impedire"],
        }
        item.update(overrides)
        return item

    def test_lexical_coverage_without_clause_relation_is_not_sufficient(self):
        answer = ("Il centrale è importante. In transizione negativa serve equilibrio. "
                  "La squadra copre. La profondità è decisiva. Alla perdita si reagisce. "
                  "Questo avviene per impedire la ripartenza.")
        audit = planner.audit_relations(answer, [self.requirement()])
        self.assertFalse(audit["requirements"][0]["satisfied"])
        self.assertIn("relation_not_demonstrated", audit["requirements"][0]["issue_codes"])

    def test_analyse_creates_non_prescriptive_subproblem_envelopes(self):
        plan = planner.analyse(
            "In transizione negativa, come proteggi la profondità e quando ripieghi?"
        )
        self.assertTrue(plan["relation_requirements"])
        requirement = plan["relation_requirements"][0]
        self.assertIn("phase", requirement["required_dimensions"])
        self.assertNotIn("actor_terms", requirement)
        self.assertEqual(requirement["task_terms"], ["proteg"])
        self.assertEqual(requirement["specificity"], "underspecified")

    def test_correct_role_and_task_in_wrong_phase_are_distinguished(self):
        answer = "In possesso, alla perdita il centrale copre la profondità per impedire la ripartenza."
        audit = planner.audit_relations(answer, [self.requirement()])
        self.assertIn("wrong_phase_for_task", audit["requirements"][0]["issue_codes"])

    def test_task_assigned_to_wrong_actor_is_distinguished(self):
        answer = "In transizione negativa, alla perdita l'ala copre la profondità per impedire la ripartenza."
        audit = planner.audit_relations(answer, [self.requirement()])
        self.assertIn("wrong_actor_for_task", audit["requirements"][0]["issue_codes"])

    def test_generic_preventive_does_not_satisfy_operational_relation(self):
        requirement = self.requirement(task_terms=["marca"], space_terms=["centravanti"])
        answer = "In transizione negativa la squadra mantiene una buona preventiva e resta equilibrata."
        audit = planner.audit_relations(answer, [requirement])
        self.assertFalse(audit["requirements"][0]["satisfied"])

    def test_one_complete_subproblem_does_not_hide_an_omitted_one(self):
        first = self.requirement()
        second = self.requirement(requirement_id="weak_side", actor_terms=["esterno"],
                                  task_terms=["stringe"], space_terms=["lato debole"],
                                  trigger_terms=["al cambio gioco"], purpose_terms=["per proteggere"])
        answer = ("In transizione negativa, alla perdita il centrale copre la profondità "
                  "per impedire la ripartenza.")
        audit = planner.audit_relations(answer, [first, second])
        self.assertTrue(audit["requirements"][0]["satisfied"])
        self.assertFalse(audit["requirements"][1]["satisfied"])

    def test_formally_valid_but_irrelevant_citation_is_reported(self):
        requirement = self.requirement(evidence_terms=["marcatura preventiva"])
        answer = ("In transizione negativa, alla perdita il centrale copre la profondità "
                  "per impedire la ripartenza [F1].")
        evidence = [{"id": "F1", "topic": "tecnica del dribbling", "text": "guida della palla"}]
        audit = planner.audit_relations(answer, [requirement], evidence)
        result = audit["requirements"][0]
        self.assertTrue(result["satisfied"])
        self.assertEqual(result["citation_status"], "formally_valid_but_irrelevant")
        self.assertFalse(result["semantic_support_verified"])

    def test_negated_required_relation_is_not_satisfied(self):
        answer = ("In transizione negativa, alla perdita il centrale non copre la profondità "
                  "per impedire la ripartenza.")
        result = planner.audit_relations(answer, [self.requirement()])["requirements"][0]
        self.assertFalse(result["satisfied"])
        self.assertIn("required_relation_negated", result["issue_codes"])

    def test_second_actor_cannot_borrow_first_actor_identity(self):
        answer = ("In transizione negativa il centrale resta largo, mentre l'ala copre la profondità "
                  "alla perdita per impedire la ripartenza.")
        result = planner.audit_relations(answer, [self.requirement()])["requirements"][0]
        self.assertFalse(result["satisfied"])
        self.assertIn("actor_task_link_not_demonstrated", result["issue_codes"])

    def test_anaphoric_adjacent_sentence_window_preserves_relation(self):
        requirement = self.requirement(task_terms=["accorc"])
        answer = ("Alla perdita, in transizione negativa, il centrale accorcia immediatamente verso la profondità. "
                  "In questo modo protegge la linea per impedire la ripartenza avversaria.")
        result = planner.audit_relations(answer, [requirement])["requirements"][0]
        self.assertTrue(result["satisfied"])
        self.assertTrue(result["matched_clause_id"].startswith("window:"))

    def test_automatic_overlapping_subproblems_remain_underspecified(self):
        plan = planner.analyse(
            "Come proteggi la profondità? Inoltre come proteggi il lato debole?"
        )
        answer = "La squadra protegge lo spazio quando serve per evitare rischi."
        audit = planner.audit_relations(answer, plan["relation_requirements"])
        self.assertEqual(len(audit["requirements"]), 2)
        self.assertTrue(all(not item["satisfied"] for item in audit["requirements"]))
        self.assertTrue(all("requirement_underspecified" in item["issue_codes"]
                            for item in audit["requirements"]))

    def test_comitative_inciso_preserves_grammatical_head(self):
        answer = ("In transizione negativa, alla perdita il centrale, insieme all'ala, "
                  "copre la profondità per impedire la ripartenza.")
        result = planner.audit_relations(answer, [self.requirement()])["requirements"][0]
        self.assertTrue(result["satisfied"])

    def test_explicit_postverbal_subject_is_linked(self):
        answer = ("In transizione negativa, alla perdita, a coprire la profondità è il centrale, "
                  "mentre l'ala resta alta per impedire la ripartenza.")
        result = planner.audit_relations(answer, [self.requirement()])["requirements"][0]
        self.assertTrue(result["satisfied"])

    def test_indefinite_pronoun_does_not_select_one_of_two_actors(self):
        requirement = self.requirement(required_dimensions=["actor", "task", "space"])
        answer = ("Il centrale e l'ala si coordinano: uno copre la profondità "
                  "mentre l'altro accorcia.")
        result = planner.audit_relations(answer, [requirement])["requirements"][0]
        self.assertFalse(result["satisfied"])
        self.assertIn("actor_task_association_ambiguous", result["issue_codes"])

    def test_risky_behaviour_negation_is_diagnostically_ambiguous(self):
        requirement = self.requirement(required_dimensions=["actor", "task", "space"],
                                       task_terms=["copre"])
        answer = "Alla perdita il centrale non lascia scoperta la profondità."
        result = planner.audit_relations(answer, [requirement])["requirements"][0]
        self.assertFalse(result["satisfied"])
        self.assertEqual(result["polarity_status"], "AMBIGUOUS")

    def test_modal_negation_is_diagnostically_ambiguous(self):
        requirement = self.requirement(required_dimensions=["actor", "task", "space"],
                                       task_terms=["copre"])
        answer = "Alla perdita il centrale non deve mai abbandonare la copertura della profondità."
        result = planner.audit_relations(answer, [requirement])["requirements"][0]
        self.assertFalse(result["satisfied"])
        self.assertEqual(result["polarity_status"], "AMBIGUOUS")

    def test_multipart_requirements_keep_open_and_explicit_parts_independent(self):
        plan = planner.analyse(
            "Come organizzi la copertura preventiva contro una ripartenza centrale? "
            "Inoltre, alla perdita come copre la profondità il centrale?"
        )
        self.assertEqual(len(plan["relation_requirements"]), 2)
        self.assertEqual(plan["relation_requirements"][0]["requirement_type"], "open")
        self.assertEqual(plan["relation_requirements"][1]["requirement_type"], "explicit")
        self.assertNotIn("actor_terms", plan["relation_requirements"][0])
        self.assertEqual(plan["relation_requirements"][1]["actor_terms"], ["centrale"])

    def test_overlapping_task_terms_become_independent_atoms(self):
        plan = planner.analyse("Come copre e accorcia il centrale in profondità?")
        requirements = plan["relation_requirements"]
        self.assertEqual(len(requirements), 2)
        self.assertEqual({tuple(item["task_terms"]) for item in requirements},
                         {("copr",), ("accorc",)})
        self.assertEqual(len({item["requirement_id"] for item in requirements}), 2)

    def test_open_requirement_accepts_concrete_answer_relation(self):
        requirement = {
            "requirement_id": "open:preventive",
            "requirement_type": "open",
            "required_dimensions": ["actor", "task", "space", "trigger"],
        }
        answer = "Alla perdita il mediano copre la profondità."
        result = planner.audit_relations(answer, [requirement])["requirements"][0]
        self.assertTrue(result["satisfied"])

    def test_open_requirement_rejects_generic_lexical_answer(self):
        requirement = {
            "requirement_id": "open:preventive",
            "requirement_type": "open",
            "required_dimensions": ["actor", "task", "space", "trigger"],
        }
        answer = "La copertura preventiva è importante per l'equilibrio generale."
        result = planner.audit_relations(answer, [requirement])["requirements"][0]
        self.assertFalse(result["satisfied"])


if __name__ == "__main__":
    unittest.main()
