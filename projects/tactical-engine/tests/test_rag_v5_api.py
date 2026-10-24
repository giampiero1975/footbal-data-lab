import importlib.util
from pathlib import Path
import queue
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


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
        with tempfile.TemporaryDirectory() as tmp:
            state = api.State(self.config(Path(tmp)))
            self.assertTrue(state.authorized("Bearer " + "x" * 32))
            self.assertFalse(state.authorized("Bearer wrong"))
            self.assertFalse(state.authorized(None))

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


if __name__ == "__main__":
    unittest.main()
