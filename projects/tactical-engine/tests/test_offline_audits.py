"""Offline smoke tests: standard library only, no Chroma/Ollama or VPS needed."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeCollection:
    name = "fake"
    metadata = {"hnsw:space": "cosine"}
    configuration = {"hnsw": {"space": "cosine"}}

    def count(self):
        return 3

    def get(self, *, limit=100, offset=0, include=None):
        if "embeddings" in (include or []):
            return {"embeddings": [[1.0, 0.0], [0.6, 0.8], [0.0, 1.0]][:limit]}
        ids = ["a", "b", "c"][offset:offset + limit]
        return {"ids": ids, "metadatas": [{"source": "A"}, {"source": "A"}, {"source": "B"}][offset:offset + limit]}


class FakeClient:
    def get_collection(self, name):
        if name == "missing":
            raise KeyError(name)
        return FakeCollection()


class OfflineAudits(unittest.TestCase):
    def test_audit_collection_norms_and_sources(self):
        with patch.dict(sys.modules, {"chromadb": types.ModuleType("chromadb")}):
            module = load_script("audit_v4_runtime")
        result = module.inspect_collection(FakeClient(), "fake")
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["source_counts"], {"A": 2, "B": 1})
        self.assertEqual(result["embedding_sample"]["dimensions"], [2])
        self.assertLess(result["embedding_sample"]["max_abs_deviation_from_unit"], 1e-6)
        self.assertEqual(module.inspect_collection(FakeClient(), "missing")["status"], "unavailable")

    def test_inventory_detects_import_and_write(self):
        module = load_script("audit_script_dependencies")
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "sample.py"
            file.write_text("import test_prompt_fedelta_dribbling_v4_corretto as v4\nfrom pathlib import Path\nPath('x').write_text('hi')\n")
            info = module.scan(file)
            self.assertIn("test_prompt_fedelta_dribbling_v4_corretto", info["imports"])
            self.assertTrue(any(w["call"] == "write_text" for w in info["possible_mutations"]))

    def test_benchmark_rejects_missing_db_before_chroma_access(self):
        chroma = types.ModuleType("chromadb")
        def unexpected(*args, **kwargs):
            raise AssertionError("Chroma must not be opened")
        chroma.PersistentClient = unexpected
        embeddings = types.ModuleType("llama_index.embeddings.ollama")
        embeddings.OllamaEmbedding = object
        with patch.dict(sys.modules, {
            "chromadb": chroma,
            "llama_index": types.ModuleType("llama_index"),
            "llama_index.embeddings": types.ModuleType("llama_index.embeddings"),
            "llama_index.embeddings.ollama": embeddings,
        }):
            module = load_script("benchmark_qwen_query_instruction")
            with patch.object(sys, "argv", ["benchmark", "--db", "/path/that/does/not/exist"]):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as cm:
                        module.main()
            self.assertEqual(cm.exception.code, 2)

    def test_script_syntax(self):
        for path in SCRIPTS.glob("*.py"):
            with self.subTest(path=path.name):
                compile(path.read_bytes(), str(path), "exec")


if __name__ == "__main__":
    unittest.main()
