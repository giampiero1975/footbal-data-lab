import importlib.util
from pathlib import Path
import unittest

PATH=Path(__file__).parents[1]/"scripts/v5_structural_scenario_routing_v1.py"
spec=importlib.util.spec_from_file_location("structural",PATH)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


class StructuralRoutingTests(unittest.TestCase):
    def test_extracts_formations_roles_and_principles(self):
        values=m.anchors("Nel 4-3-3 contro 3-5-2, terzino e ala attaccano l'half-space con marcatura preventiva")
        self.assertEqual(values["formations"],{"4-3-3","3-5-2"})
        self.assertEqual(values["roles"],{"terzino","ala"})
        self.assertEqual(values["principles"],{"half-space","marcatura preventiva"})

    def test_derives_synchronized_run_intent(self):
        signals=m.anchors("Se il braccetto esce sull'ala, quale movimento deve fare il terzino per andare in porta?")
        self.assertIn("movimento sincronizzato",signals["principles"])
        direct={"source":"Il sistema 4-3-3","headings":[],"text":"taglio dell'ala e inserimento del terzino nello spazio creato"}
        static={"source":"Difesa 3-5-2","headings":[],"text":"terzino e ala controllano il braccetto"}
        self.assertGreater(m.score_row(direct,signals),m.score_row(static,signals))

    def test_derives_underlap_from_geometry_without_keyword(self):
        signals=m.anchors("Ala nello half-space: quale movimento deve fare il terzino per andare in porta?")
        self.assertIn("underlap",signals["principles"])
        underlap={"source":"Catene","headings":[],"text":"Sottoposizione: il terzino attacca il corridoio interno"}
        overlap={"source":"Catene","headings":[],"text":"Il terzino corre in sovrapposizione esterna lungo la fascia"}
        self.assertGreater(m.score_row(underlap,signals),m.score_row(overlap,signals))

    def test_reserves_distinct_structurally_relevant_sources(self):
        rows=[
            {"id":"generic","source":"Principi","headings":[],"text":"ampiezza e profondità"},
            {"id":"shape","source":"4-3-3 contro 3-5-2","headings":[],"text":"il terzino e l'ala occupano il corridoio interno"},
            {"id":"chain","source":"Catene laterali","headings":[],"text":"terzino, mezzala e ala; sovrapposizione e raddoppio"},
        ]
        selected=[rows[0]]
        revised,reserved,signals=m.reserve(rows,[9,2,1],selected,"4-3-3 contro 3-5-2: terzino, mezzala e ala contro il raddoppio",3)
        self.assertEqual(set(reserved),{"shape","chain"})
        self.assertEqual({row["id"] for row in revised},{"generic","shape","chain"})
        self.assertIn("3-5-2",signals["formations"])

    def test_generic_question_is_unchanged(self):
        selected=[{"id":"a","source":"A","headings":[],"text":"testo"}]
        revised,reserved,_=m.reserve(selected,[1],selected,"Come si gioca meglio?",1)
        self.assertIs(revised,selected)
        self.assertEqual(reserved,[])


if __name__ == "__main__": unittest.main()
