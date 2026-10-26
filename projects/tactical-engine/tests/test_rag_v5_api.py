import importlib.util
import json
from pathlib import Path
import queue
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "api"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


api = load("rag_v5_api", ROOT / "api/rag_v5_api.py")
query = load("run_rag_v5_query", ROOT / "scripts/run_rag_v5_query.py")


class ApiTests(unittest.TestCase):
    def config(self, output):
        return api.load_config({
            "RAG_API_TOKEN": "x" * 32,
            "RAG_API_OUTPUT_DIR": str(output),
            "RAG_API_QUEUE_SIZE": "1",
            "RAG_API_RATE_LIMIT_PER_MINUTE": "2",
        })

    def test_token_required_and_constant_time_auth_contract(self):
        with self.assertRaises(RuntimeError):
            api.load_config({"RAG_API_TOKEN": "short"})
        with self.assertRaises(RuntimeError):
            api.load_config({"RAG_API_TOKEN": "replace-with-at-least-32-random-characters"})
        with tempfile.TemporaryDirectory() as tmp:
            state = api.State(self.config(Path(tmp)))
            self.assertTrue(state.authorized("Bearer " + "x" * 32))
            self.assertFalse(state.authorized("Bearer wrong"))
            self.assertFalse(state.authorized(None))

    def test_invalid_auth_attempts_are_bounded_separately(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.config(Path(tmp)); config["auth_failure_limit"] = 2
            state = api.State(config)
            self.assertTrue(state.auth_failure_allowed("127.0.0.1"))
            self.assertTrue(state.auth_failure_allowed("127.0.0.1"))
            self.assertFalse(state.auth_failure_allowed("127.0.0.1"))
            self.assertTrue(state.rate_allowed("127.0.0.1"))

    def test_http_log_drops_query_string_and_message(self):
        handler = object.__new__(api.Handler)
        handler.client_address = ("127.0.0.1", 1234)
        handler.command = "GET"; handler.path = "/v1/knowledge/search?q=secret-tactic"
        with mock.patch("builtins.print") as output:
            handler.log_message('"%s" %s %s', handler.path, "200", "1")
        logged = output.call_args.args[0]
        self.assertIn('"path": "/v1/knowledge/search"', logged)
        self.assertNotIn("secret-tactic", logged)

    def test_rate_limit_and_bounded_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = api.State(self.config(Path(tmp)))
            self.assertTrue(state.rate_allowed("127.0.0.1"))
            self.assertTrue(state.rate_allowed("127.0.0.1"))
            self.assertFalse(state.rate_allowed("127.0.0.1"))
            job = state.submit("Questa domanda tattica è abbastanza lunga?")
            self.assertEqual(job["status"], "queued")
            with self.assertRaises(queue.Full):
                state.submit("Questa seconda domanda riempie la coda?")

    def test_query_input_validation(self):
        self.assertEqual(query.validate_question("  domanda   tattica valida  "), "domanda tattica valida")
        with self.assertRaises(Exception):
            query.validate_question("corta")
        self.assertEqual(query.validate_request_id("abcd1234"), "abcd1234")
        with self.assertRaises(Exception):
            query.validate_request_id("../invalid")

    def test_query_report_fails_closed_on_citations(self):
        good={"questions":[{"invalid_citation_ids":[],"has_any_citation":True}],"index_unchanged":True}
        query.validate_report(good)
        for item in (
            {"invalid_citation_ids":["10"],"has_any_citation":True},
            {"invalid_citation_ids":[],"has_any_citation":False},
        ):
            with self.assertRaises(RuntimeError):
                query.validate_report({"questions":[item],"index_unchanged":True})

    def test_performance_profile_defaults_are_locked_compatible(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.config(Path(tmp))
            self.assertEqual(config["evidence_limit"], 8)
            self.assertEqual(config["max_output_tokens"], 0)

    def test_performance_profile_is_forwarded_to_runner(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = api.load_config({
                "RAG_API_TOKEN": "x" * 32,
                "RAG_API_OUTPUT_DIR": tmp,
                "RAG_API_EVIDENCE_LIMIT": "6",
                "RAG_API_MAX_OUTPUT_TOKENS": "700",
                "RAG_API_MODEL": "qwen3.5:4b",
                "RAG_API_CONTEXT_WINDOW": "4096",
                "RAG_API_KEEP_ALIVE": "30m",
            })
            self.assertEqual(config["evidence_limit"], 6)
            self.assertEqual(config["max_output_tokens"], 700)
            self.assertEqual(config["model"], "qwen3.5:4b")
            self.assertEqual(config["context_window"], 4096)
            self.assertEqual(config["keep_alive"], "30m")

    def test_gemini_review_is_opt_in_and_uses_stable_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.config(Path(tmp))
            self.assertFalse(config["gemini_review_enabled"])
            self.assertEqual(config["gemini_review_model"], "gemini-3.6-flash")
            enabled = api.load_config({
                "RAG_API_TOKEN": "x" * 32,
                "RAG_API_OUTPUT_DIR": tmp,
                "RAG_GEMINI_REVIEW_ENABLED": "true",
                "RAG_GEMINI_REVIEW_DAILY_LIMIT": "250",
            })
            self.assertTrue(enabled["gemini_review_enabled"])
            self.assertEqual(enabled["gemini_review_daily_limit"], 250)

    def test_gemini_review_returns_bounded_verified_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            config = self.config(output); config["gemini_review_enabled"] = True
            state = api.State(config)
            result_path = output / ("a" * 32 + ".result.json")
            result_path.write_text('{"questions":[]}', encoding="utf-8")
            report = {
                "status": "ESEGUITO", "model": "gemini-3.6-flash",
                "reviews": [{"id": "case_01", "score": 8.5, "verdict": "PASS",
                             "strengths": ["coerente"], "structural_errors": [],
                             "evidence_issues": [], "minimum_fix": "nessuna"}],
            }
            def reviewer(command, **kwargs):
                review_path = Path(command[command.index("--output") + 1])
                review_path.write_text(json.dumps(report), encoding="utf-8")
                return mock.Mock(returncode=0, stderr="")
            with mock.patch.object(api.subprocess, "run", side_effect=reviewer):
                summary = state.run_gemini_review("a" * 32, result_path)
            self.assertEqual(summary["status"], "verified")
            self.assertEqual(summary["score"], 8.5)
            self.assertNotIn("raw_review", summary)

    def test_catalog_is_loaded_once(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(api, "load_catalog", return_value={"documents":[],"chunks":[]}) as loader:
            state = api.State(self.config(Path(tmp)))
            self.assertIs(state.catalog(), state.catalog())
            loader.assert_called_once()

    def test_panel_has_no_embedded_secret(self):
        panel = (ROOT / "api/knowledge_panel.html").read_text(encoding="utf-8")
        self.assertIn("/v1/knowledge/stats", panel)
        self.assertIn("/v1/query", panel)
        self.assertIn("result.questions", panel)
        self.assertIn("allDocuments", panel)
        self.assertIn("/v1/metrics", panel)
        self.assertIn("Qualità operativa", panel)
        self.assertIn("Cronologia della sessione", panel)
        self.assertIn("item.evidence", panel)
        self.assertIn("done_reason", panel)
        self.assertIn("askButton", panel)
        self.assertIn("/v1/feedback", panel)
        self.assertIn("exportMarkdown", panel)
        self.assertIn("<details", panel)
        self.assertIn("Come usare il pannello", panel)
        self.assertIn('id="askButton" disabled', panel)
        self.assertIn('id="searchButton" disabled', panel)
        self.assertIn("r.status===401", panel)
        self.assertIn("setConnected(true)", panel)
        self.assertIn("Biblioteca PDF", panel)
        self.assertIn("libraryCategory", panel)
        self.assertIn("renderLibrary", panel)
        self.assertIn("estratti indicizzati", panel)
        self.assertIn("/v1/events", panel)
        self.assertIn("Registro diagnostico", panel)
        self.assertIn("Revisione indipendente Gemini", panel)
        self.assertIn("job.gemini_review", panel)
        self.assertIn("mai token, chiavi o PDF completi", panel)
        self.assertNotIn("RAG_API_TOKEN", panel)

    def test_feedback_is_bounded_to_succeeded_job_without_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = api.State(self.config(Path(tmp)))
            job_id = "a" * 32
            state.jobs[job_id] = {"id": job_id, "status": "succeeded", "question": "non salvare"}
            feedback = state.record_feedback(job_id, True)
            self.assertTrue(feedback["helpful"])
            stored = (Path(tmp) / f"{job_id}.feedback.json").read_text(encoding="utf-8")
            self.assertNotIn("non salvare", stored)
            self.assertNotIn("question", stored)
            snapshot = state.metrics_snapshot()
            self.assertEqual(snapshot["feedback"], {"total": 1, "helpful": 1, "not_helpful": 0})
            state.record_feedback(job_id, False)
            self.assertEqual(state.metrics_snapshot()["feedback"], {"total": 1, "helpful": 0, "not_helpful": 1})
            with self.assertRaises(KeyError):
                state.record_feedback("b" * 32, False)

    def test_metrics_are_persisted_without_question_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = api.State(self.config(Path(tmp)))
            state.worker_thread = mock.Mock(); state.worker_thread.is_alive.return_value = True
            state.submit("Questa domanda sensibile non deve finire nelle metriche")
            snapshot=state.metrics_snapshot()
            self.assertEqual(snapshot["cumulative"]["accepted"],1)
            self.assertEqual(snapshot["queue_depth"],1)
            stored=(Path(tmp)/"metrics.json").read_text(encoding="utf-8")
            self.assertNotIn("sensibile",stored)

    def test_empty_metrics_file_exists_at_startup(self):
        with tempfile.TemporaryDirectory() as tmp:
            api.State(self.config(Path(tmp)))
            stored=Path(tmp)/"metrics.json"
            self.assertTrue(stored.exists())
            self.assertEqual(json.loads(stored.read_text())["accepted"],0)

    def test_privacy_safe_event_log_filters_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            state=api.State(self.config(Path(tmp)))
            state.record_event("job_finished",job_id="a"*32,status="failed",reason="runner_failed",
                               question="private question",token="private token",detail="private output")
            events=state.recent_events(10)
            self.assertEqual(events[0]["event"],"job_finished")
            stored=(Path(tmp)/"events.jsonl").read_text(encoding="utf-8")
            self.assertNotIn("private question",stored)
            self.assertNotIn("private token",stored)
            self.assertNotIn("private output",stored)
            self.assertIn("runner_failed",stored)

    def test_http_server_is_bounded(self):
        self.assertEqual(api.BoundedHTTPServer.request_queue_size, 32)
        self.assertTrue(api.BoundedHTTPServer.daemon_threads)


if __name__ == "__main__":
    unittest.main()
