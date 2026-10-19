import unittest
from audit_citazioni_glerean_v4 import citations
class CitationAuditTests(unittest.TestCase):
 def test_stable_ignores_pages(self):
  self.assertEqual(citations("FONTE [GLEREAN-C018], pagina [11]", "stable"),["[GLEREAN-C018]"])
 def test_numeric_ignores_pages(self):
  self.assertEqual(citations("FONTE [1], pagina [11] e [2]", "numeric"),["[1]","[2]"])
 def test_stable_invalid_is_detectable(self):
  self.assertEqual(citations("[GLEREAN-C999]","stable"),["[GLEREAN-C999]"])
if __name__=="__main__": unittest.main()
