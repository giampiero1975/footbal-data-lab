#!/usr/bin/env python3
"""Offline regression checks for H09 citation ID normalization."""
import unittest
from compare_h09_generation_focus_ab import normalize_id, validate_citations

class CitationTests(unittest.TestCase):
    def test_supported_forms(self):
        for raw,expected in [("FIGURA 15/a","15/a"),("15/a","15/a"),("fig. 15\\b",None),("FIGURA 17","17"),("fig. 20","20"),(" 21 ","21")]:
            self.assertEqual(normalize_id(raw),expected)
    def test_reject_unrelated(self):
        context=[{"figure_id":"15/a"},{"figure_id":"17"}]
        self.assertEqual(validate_citations(["FIGURA 15/a"],context),(True,["15/a"]))
        self.assertFalse(validate_citations(["FIGURA 99"],context)[0])
        self.assertFalse(validate_citations([],context)[0])
        self.assertFalse(validate_citations(["15/a e 17"],context)[0])

if __name__=="__main__":unittest.main()
