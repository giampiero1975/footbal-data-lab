import importlib.util, json, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"scripts"))
spec=importlib.util.spec_from_file_location("groq",ROOT/"scripts/groq_free_reviewer_v1.py")
groq=importlib.util.module_from_spec(spec); spec.loader.exec_module(groq)

def review(case_id="case_01",score=8.0,verdict="PASS"):
    return {"reviews":[{"id":case_id,"score":score,"verdict":verdict,"strengths":["ok"],
        "structural_errors":[],"evidence_issues":[],"minimum_fix":"nessuna"}],"series_limitations":[]}

class GroqOfflineTests(unittest.TestCase):
    def test_strict_schema_and_frozen_prompt(self):
        request=groq.build_request([{"id":"case_01"}])
        self.assertTrue(request["response_format"]["json_schema"]["strict"])
        self.assertFalse(groq.REVIEW_SCHEMA["additionalProperties"])
        self.assertEqual(request["messages"][0]["content"],groq.PROMPT)
    def test_200_parser_and_semantic_gates(self):
        payload={"choices":[{"message":{"content":json.dumps(review())}}]}
        self.assertEqual(groq.validate_response(payload,["case_01"])["reviews"][0]["score"],8.0)
        for bad in (review("wrong"),review(score=11),review(score=7,verdict="PASS")):
            with self.assertRaises(ValueError): groq.validate_response({"choices":[{"message":{"content":json.dumps(bad)}}]},["case_01"])
    def test_http_policy(self):
        self.assertEqual(groq.http_policy(200)["action"],"accept")
        self.assertEqual(groq.http_policy(429,"17"),{"action":"retry","delay_seconds":17})
        self.assertEqual(groq.http_policy(503)["action"],"retry")
        for status in (400,401,403): self.assertEqual(groq.http_policy(status)["action"],"stop")
    def test_quota_hard_stop(self):
        limits={"requests_per_day":2,"tokens_per_day":100,"tokens_per_minute":60}
        self.assertTrue(groq.quota_allowed({},"2026-10-25",50,limits))
        self.assertFalse(groq.quota_allowed({"2026-10-25":{"requests":2,"tokens":0}},"2026-10-25",1,limits))
        self.assertFalse(groq.quota_allowed({},"2026-10-25",61,limits))
    def test_resume_skips_completed_ids(self):
        self.assertEqual(groq.pending_ids(["case_01","case_02"],{"completed_ids":["case_01"]}),["case_02"])
    def test_invalid_input_citations_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"case.json"; path.write_text(json.dumps({"questions":[{"id":"x","question":"q","answer":"a",
                "citation_ids":["2"],"invalid_citation_ids":[],"evidence":[{"label":"F1","text":"t"}]}]}))
            with self.assertRaises(ValueError): groq.prepare_cases([path])

if __name__=="__main__": unittest.main()
