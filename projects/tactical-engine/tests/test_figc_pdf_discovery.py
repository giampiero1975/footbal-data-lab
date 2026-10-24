import importlib.util
from pathlib import Path
import unittest
import tempfile
import json

PATH=Path(__file__).parents[1]/"scripts/figc_pdf_discovery.py"
spec=importlib.util.spec_from_file_location("figc_pdf_discovery",PATH)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class FigcDiscoveryTests(unittest.TestCase):
    def test_allowlist(self):
        self.assertTrue(m.allowed("https://www.figc.it/media/1/a.pdf"))
        self.assertTrue(m.allowed("https://api.figc.atexcloud.io/file-delivery-service/version/x/a.pdf"))
        self.assertFalse(m.allowed("http://figc.it/media/1/a.pdf"))
        self.assertFalse(m.allowed("https://figc.it.evil.example/a.pdf"))
    def test_classification(self):
        self.assertEqual(m.classify("modello di gioco uefa pro"),"tattica")
        self.assertEqual(m.classify("metodologia di allenamento"),"allenamenti")
        self.assertEqual(m.classify("documento amministrativo"),"review_required")
    def test_exact_queries_preserved(self):
        self.assertEqual(len(m.QUERIES),2)
        self.assertIn('"uefa pro"',m.QUERIES[0])
    def test_known_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.pdf"; p.write_bytes(b"%PDF-test")
            found=m.known_hashes([Path(d)])
            self.assertEqual(found[m.hashlib.sha256(b"%PDF-test").hexdigest()],str(p))
    def test_catalog_merge_preserves_first_seen(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"catalog.json"
            row={"sha256":"abc","url":"https://figc.it/media/a.pdf","status":"verified"}
            m.update_catalog(p,[row],[],"2026-01-01T00:00:00+00:00")
            m.update_catalog(p,[{**row,"status":"duplicate_existing"}],[],"2026-01-02T00:00:00+00:00")
            saved=json.loads(p.read_text(encoding="utf-8"))["documents"]["abc"]
            self.assertEqual(saved["first_seen"],"2026-01-01T00:00:00+00:00")
            self.assertEqual(saved["last_seen"],"2026-01-02T00:00:00+00:00")
            self.assertEqual(saved["status"],"duplicate_existing")

if __name__ == "__main__": unittest.main()
