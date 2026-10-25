import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "generator", ROOT / "scripts/generate_coverciano_100_gemini_v1.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def valid_rows():
    rows = []
    for number in range(1, 101):
        rows.append({
            "id": f"coverciano_{number:03d}",
            "category": generator.CATEGORIES[(number - 1) // 10],
            "difficulty": 3 + number % 3,
            "question": (f"Scenario tattico originale numero {number}: descrivi sistema, fase, tempo, "
                         "punteggio, vincoli, compiti individuali e movimenti collettivi necessari "
                         "per risolvere una situazione complessa senza sostituzioni."),
            "hidden_rubric": {"constraints": ["vincolo"], "expected_points": ["punto"],
                              "critical_errors": ["errore"]},
        })
    return rows


class GeneratorTests(unittest.TestCase):
    def test_accepts_exact_balanced_manifest(self):
        self.assertEqual(len(generator.validate(valid_rows())), 100)

    def test_rejects_duplicate_or_unbalanced_manifest(self):
        rows = valid_rows(); rows[1]["question"] = rows[0]["question"]
        with self.assertRaises(ValueError):
            generator.validate(rows)
        rows = valid_rows(); rows[-1]["category"] = generator.CATEGORIES[0]
        with self.assertRaises(ValueError):
            generator.validate(rows)


if __name__ == "__main__":
    unittest.main()
