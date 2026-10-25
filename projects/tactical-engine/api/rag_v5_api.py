#!/usr/bin/env python3
"""Dependency-free authenticated HTTP job API for the V5 query runner."""
from __future__ import annotations

from collections import defaultdict, deque
import hmac
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time
import urllib.request
from urllib.parse import parse_qs, urlparse
import uuid

from knowledge_catalog import load_catalog, search_catalog

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_rag_v5_query.py"
PYTHON = ROOT / ".venv/bin/python"


def load_config(env=os.environ) -> dict:
    token = env.get("RAG_API_TOKEN", "")
    if len(token) < 32:
        raise RuntimeError("RAG_API_TOKEN must contain at least 32 characters")
    return {
        "token": token,
        "host": env.get("RAG_API_HOST", "127.0.0.1"),
        "port": int(env.get("RAG_API_PORT", "8088")),
        "timeout": int(env.get("RAG_API_TIMEOUT_SECONDS", "900")),
        "queue_size": int(env.get("RAG_API_QUEUE_SIZE", "8")),
        "rate_limit": int(env.get("RAG_API_RATE_LIMIT_PER_MINUTE", "10")),
        "output_dir": Path(env.get("RAG_API_OUTPUT_DIR", str(ROOT / "evaluation/api-runs"))),
        "collection": env.get("RAG_COLLECTION", "dribbling_tactics_v5_multisource"),
        "expected_count": int(env.get("RAG_EXPECTED_COUNT", "5319")),
        "chroma_path": Path(env.get("RAG_CHROMA_PATH", str(ROOT.parent.parent / "knowledge/rag/chroma"))),
    }


class State:
    def __init__(self, config: dict):
        self.config = config
        self.jobs: dict[str, dict] = {}
        self.lock = threading.Lock()
        self.requests = defaultdict(deque)
        self.queue: queue.Queue[str] = queue.Queue(maxsize=config["queue_size"])
        self.knowledge_catalog: dict | None = None
        config["output_dir"].mkdir(parents=True, exist_ok=True)
        config["output_dir"].chmod(0o700)

    def authorized(self, header: str | None) -> bool:
        return bool(header and header.startswith("Bearer ") and hmac.compare_digest(header[7:], self.config["token"]))

    def rate_allowed(self, client: str) -> bool:
        now = time.monotonic()
        with self.lock:
            values = self.requests[client]
            while values and now - values[0] >= 60:
                values.popleft()
            if len(values) >= self.config["rate_limit"]:
                return False
            values.append(now)
            return True

    def submit(self, question: str) -> dict:
        job_id = uuid.uuid4().hex
        job = {"id": job_id, "status": "queued", "created_at": int(time.time())}
        request_path = self.config["output_dir"] / f"{job_id}.request.json"
        temporary_path = self.config["output_dir"] / f".{job_id}.request.tmp"
        temporary_path.write_text(
            json.dumps({"id": job_id, "question": question}, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        os.replace(temporary_path, request_path)
        with self.lock:
            self.jobs[job_id] = job
        try:
            self.queue.put_nowait(job_id)
        except queue.Full:
            with self.lock:
                del self.jobs[job_id]
            request_path.unlink(missing_ok=True)
            raise
        return dict(job)

    def worker(self) -> None:
        while True:
            job_id = self.queue.get()
            try:
                request_path = self.config["output_dir"] / f"{job_id}.request.json"
                output_path = self.config["output_dir"] / f"{job_id}.result.json"
                request = json.loads(request_path.read_text(encoding="utf-8"))
                with self.lock:
                    self.jobs[job_id].update(status="running", started_at=int(time.time()))
                command = [str(PYTHON), str(RUNNER), "--question", request["question"], "--request-id", job_id,
                           "--output", str(output_path), "--collection", self.config["collection"],
                           "--expected-count", str(self.config["expected_count"])]
                try:
                    result = subprocess.run(command, cwd=ROOT.parent.parent, capture_output=True, text=True, timeout=self.config["timeout"])
                    status = "succeeded" if result.returncode == 0 and output_path.exists() else "failed"
                    detail = result.stderr[-2000:] if status == "failed" else None
                except subprocess.TimeoutExpired:
                    status, detail = "timed_out", "runner timeout"
            except Exception as exc:
                status, detail = "failed", f"worker error: {type(exc).__name__}: {exc}"
            finally:
                with self.lock:
                    self.jobs[job_id].update(status=status, finished_at=int(time.time()))
                    if detail:
                        self.jobs[job_id]["error"] = detail
                self.queue.task_done()

    def catalog(self) -> dict:
        with self.lock:
            if self.knowledge_catalog is None:
                self.knowledge_catalog = load_catalog(self.config["chroma_path"], self.config["collection"])
            return self.knowledge_catalog


class Handler(BaseHTTPRequestHandler):
    server_version = "FootballRAG/1"

    @property
    def state(self) -> State:
        return self.server.state  # type: ignore[attr-defined]

    def log_message(self, fmt, *args):
        print(json.dumps({"event": "http", "client": self.client_address[0], "message": fmt % args}), flush=True)

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def authenticated(self, apply_rate_limit: bool = False) -> bool:
        if not self.state.authorized(self.headers.get("Authorization")):
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
            return False
        if apply_rate_limit and not self.state.rate_allowed(self.client_address[0]):
            self.send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "rate_limited"})
            return False
        return True

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/healthz":
            self.send_json(HTTPStatus.OK, {"status": "ok"})
            return
        if not self.authenticated():
            return
        if parsed.path == "/readyz":
            ready = PYTHON.exists() and RUNNER.exists() and self.state.worker_thread.is_alive()
            try:
                urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2).close()
            except Exception:
                ready = False
            self.send_json(HTTPStatus.OK if ready else HTTPStatus.SERVICE_UNAVAILABLE, {"status": "ready" if ready else "not_ready"})
            return
        if parsed.path == "/v1/knowledge/stats":
            catalog = self.state.catalog()
            self.send_json(HTTPStatus.OK, {key: value for key, value in catalog.items() if key not in {"documents", "chunks"}})
            return
        if parsed.path == "/v1/knowledge/documents":
            query = parse_qs(parsed.query)
            try:
                offset = max(0, int(query.get("offset", ["0"])[0]))
                limit = min(100, max(1, int(query.get("limit", ["25"])[0])))
            except ValueError:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_pagination"}); return
            catalog = self.state.catalog(); documents = catalog["documents"]
            self.send_json(HTTPStatus.OK, {"total": len(documents), "offset": offset, "limit": limit,
                                           "items": documents[offset:offset+limit]})
            return
        if parsed.path == "/v1/knowledge/search":
            query = parse_qs(parsed.query)
            text = " ".join(query.get("q", [""])[0].split())
            try:
                limit = min(50, max(1, int(query.get("limit", ["20"])[0])))
            except ValueError:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_limit"}); return
            if not 2 <= len(text) <= 200:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_query"}); return
            items = search_catalog(self.state.catalog(), text, limit)
            self.send_json(HTTPStatus.OK, {"query": text, "total": len(items), "items": items})
            return
        prefix = "/v1/jobs/"
        if parsed.path.startswith(prefix):
            job_id = parsed.path[len(prefix):]
            if not job_id.isalnum() or len(job_id) != 32:
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                return
            with self.state.lock:
                job = dict(self.state.jobs.get(job_id, {}))
            if not job:
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                return
            if job["status"] == "succeeded":
                result_path = self.state.config["output_dir"] / f"{job_id}.result.json"
                job["result"] = json.loads(result_path.read_text(encoding="utf-8"))
            self.send_json(HTTPStatus.OK, job)
            return
        self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/v1/query":
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        if not self.authenticated(apply_rate_limit=True):
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if not 1 <= length <= 16384:
            self.send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "invalid_body_size"})
            return
        try:
            payload = json.loads(self.rfile.read(length))
            question = " ".join(payload["question"].split())
            if set(payload) != {"question"} or not 10 <= len(question) <= 2000:
                raise ValueError
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_request"})
            return
        try:
            job = self.state.submit(question)
        except queue.Full:
            self.send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "queue_full"})
            return
        self.send_json(HTTPStatus.ACCEPTED, job)


def main() -> None:
    os.umask(0o077)
    config = load_config()
    state = State(config)
    state.worker_thread = threading.Thread(target=state.worker, daemon=True, name="rag-worker")
    state.worker_thread.start()
    server = ThreadingHTTPServer((config["host"], config["port"]), Handler)
    server.state = state  # type: ignore[attr-defined]
    print(json.dumps({"event": "startup", "host": config["host"], "port": config["port"]}), flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
