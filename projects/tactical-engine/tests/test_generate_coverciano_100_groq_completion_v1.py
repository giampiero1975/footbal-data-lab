import importlib.util, json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("gen", ROOT / "scripts/generate_coverciano_100_groq_completion_v1.py")
gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)


def row(number, category, text=None):
    unique = " ".join(f"elemento{number}x{i}" for i in range(35))
    return {"id": f"coverciano_{number:03d}", "category": category, "difficulty": 4,
            "question": text or ("Scenario tattico concreto con spazi tempi ruoli vincoli e richiesta tecnica " + unique),
            "hidden_rubric": {"constraints": ["c"], "expected_points": ["e"], "critical_errors": ["x"]}}


class GroqGeneratorOfflineTests(unittest.TestCase):
    def test_request_preserves_ids_and_strict_schema(self):
        request = gen.build_request("blocco_difensivo", 1, [row(1, "costruzione")])
        self.assertTrue(request["response_format"]["json_schema"]["strict"])
        self.assertIn("coverciano_051", request["messages"][0]["content"])
        self.assertIn("existing_questions_read_only", request["messages"][1]["content"])
        body = json.loads(request["messages"][1]["content"])
        self.assertLessEqual(len(body["existing_questions_read_only"][0]["question_prefix"]), 160)

    def test_parse_accepts_five_and_rejects_wrong_ids(self):
        rows = [row(n, "blocco_difensivo") for n in range(51, 56)]
        payload = {"choices": [{"message": {"content": json.dumps({"questions": rows})}}]}
        self.assertEqual(len(gen.parse_response(payload, "blocco_difensivo", 1, [])), 5)
        rows[0]["id"] = "wrong"
        payload = {"choices": [{"message": {"content": json.dumps({"questions": rows})}}]}
        with self.assertRaises(ValueError): gen.parse_response(payload, "blocco_difensivo", 1, [])

    def test_near_duplicate_fails_closed(self):
        a = row(51, "blocco_difensivo"); b = row(1, "costruzione", a["question"])
        with self.assertRaises(ValueError): gen.validate_no_duplicates([a], [b])

    def test_inventory_preserves_existing_chunks(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp); category = "costruzione"
            data = {"model": "gemini-3.6-flash", "questions": [row(n, category) for n in range(1, 11)]}
            (path / f"coverciano_{category}_v1.json").write_text(json.dumps(data), encoding="utf-8")
            inv = gen.inventory(path)
            self.assertEqual(inv["question_count"], 10)
            self.assertIn(category, inv["complete_categories"])
            self.assertNotIn(category, inv["missing_categories"])


if __name__ == "__main__": unittest.main()
