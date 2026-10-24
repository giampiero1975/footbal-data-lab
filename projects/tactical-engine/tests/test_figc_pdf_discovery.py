import importlib.util
from pathlib import Path
import unittest

PATH=Path(__file__).parents[1]/"scripts/figc_pdf_discovery.py"
spec=importlib.util.spec_from_file_location("figc_pdf_discovery",PATH)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class FigcDiscoveryTests(unittest.TestCase):
    def test_allowlist(self):
        self.assertTrue(m.allowed("https://www.figc.it/media/1/a.pdf"))
        self.assertFalse(m.allowed("http://figc.it/media/1/a.pdf"))
        self.assertFalse(m.allowed("https://figc.it.evil.example/a.pdf"))
    def test_classification(self):
        self.assertEqual(m.classify("modello di gioco uefa pro"),"tattica")
        self.assertEqual(m.classify("metodologia di allenamento"),"allenamenti")
        self.assertEqual(m.classify("documento amministrativo"),"review_required")
    def test_exact_queries_preserved(self):
        self.assertEqual(len(m.QUERIES),2)
        self.assertIn('"uefa pro"',m.QUERIES[0])

if __name__ == "__main__": unittest.main()
