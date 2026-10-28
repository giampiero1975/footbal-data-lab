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
import re
import statistics
import subprocess
import threading
import time
import urllib.request
from urllib.parse import parse_qs, urlparse
import uuid

from knowledge_catalog import load_catalog, load_figc_catalog, search_catalog

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_rag_v5_query.py"
PYTHON = ROOT / ".venv/bin/python"
PANEL = ROOT / "api/knowledge_panel.html"
OPENROUTER_COPILOT = ROOT / "scripts/openrouter_tactical_copilot_v1.py"
REJECTED_TOKENS = {"replace-with-at-least-32-random-characters"}
SESSION_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def normalize_query_payload(payload: dict) -> tuple[str, dict | None]:
    """Validate the legacy request or the isolated contextual extension."""
    if not isinstance(payload, dict) or "question" not in payload:
        raise ValueError("invalid_request")
    allowed = {"question", "session_id", "case_id", "confirmed_context", "prior_job_ids"}
    if not set(payload) <= allowed:
        raise ValueError("invalid_request")
    question = " ".join(str(payload["question"]).split()) if isinstance(payload["question"], str) else ""
    if not 10 <= len(question) <= 2000:
        raise ValueError("invalid_question")
    if set(payload) == {"question"}:
        return question, None
    session_id, case_id = payload.get("session_id"), payload.get("case_id")
    if not isinstance(session_id, str) or not SESSION_ID_RE.fullmatch(session_id):
        raise ValueError("invalid_session_id")
    if not isinstance(case_id, str) or not SESSION_ID_RE.fullmatch(case_id):
        raise ValueError("invalid_case_id")
    confirmed = payload.get("confirmed_context", [])
    prior = payload.get("prior_job_ids", [])
    if (not isinstance(confirmed, list) or len(confirmed) > 20
            or any(not isinstance(item, str) or not 1 <= len(" ".join(item.split())) <= 500 for item in confirmed)):
        raise ValueError("invalid_confirmed_context")
    if (not isinstance(prior, list) or len(prior) > 20
            or any(not isinstance(item, str) or len(item) != 32 or not item.isalnum() for item in prior)):
        raise ValueError("invalid_prior_job_ids")
    context = {
        "session_id": session_id,
        "case_id": case_id,
        "confirmed_context": list(dict.fromkeys(" ".join(item.split()) for item in confirmed)),
        "prior_job_ids": list(dict.fromkeys(prior)),
    }
    return question, context


def effective_question(question: str, confirmed_context: list[str]) -> str:
    """Compose only user-confirmed facts; generated answers are never promoted."""
    if not confirmed_context:
        return question
    facts = "\n".join(f"- {item}" for item in confirmed_context)
    return ("SCENARIO CONFERMATO DALL'UTENTE (usa solo questi fatti come contesto):\n"
            f"{facts}\n\nDOMANDA ORIGINALE:\n{question}")


def classify_failure(detail: str | None, status: str = "failed") -> dict:
    """Turn noisy runner stderr into a stable, actionable API contract."""
    raw = re.sub(r"\x1b\[[0-9;]*m", "", str(detail or "")).strip()
    normalized = raw.lower()
    if status == "timed_out" or "runner timeout" in normalized:
        return {"code": "runner_timeout", "phase": "rag_generation",
                "message": "Il motore RAG non ha concluso entro il tempo massimo.",
                "action": "Riprova una volta; se ricapita, verifica Ollama e la durata del modello."}
    known = (
        ("tactical_quality_gate_failed", "quality_gate",
         "La risposta è stata generata ma respinta dal controllo tattico sperimentale.",
         "Usa il profilo pubblico senza tactical-plan oppure correggi il gate dedicato."),
        ("missing_citations", "response_validation",
         "La risposta non contiene citazioni verificabili.",
         "Controlla retrieval e prompt di citazione prima di riprovare."),
        ("invalid_citations", "response_validation",
         "La risposta cita evidenze che non appartengono al contesto recuperato.",
         "Controlla la mappatura F1–Fn e la generazione grounded."),
        ("incomplete_report", "response_validation",
         "Il runner ha prodotto un report incompleto.",
         "Apri il risultato tecnico del job e verifica indice, domande ed errori."),
        ("index count", "retrieval",
         "L'indice RAG non corrisponde alla consistenza attesa.",
         "Verifica collection, conteggio atteso e integrità dell'indice."),
        ("connection refused", "model_runtime",
         "Il servizio del modello locale non era raggiungibile.",
         "Verifica che Ollama sia attivo e che il modello configurato sia disponibile."),
    )
    for needle, phase, message, action in known:
        if needle in normalized:
            return {"code": needle.replace(" ", "_"), "phase": phase,
                    "message": message, "action": action}
    incomplete = re.search(r"INCOMPLETE:\s*([a-zA-Z0-9_-]+)", raw)
    if incomplete:
        code = incomplete.group(1).lower()
        return {"code": code, "phase": "response_validation",
                "message": f"La risposta è stata respinta dal controllo finale ({code}).",
                "action": "Consulta il report del job e correggi il controllo indicato."}
    return {"code": "runner_failed", "phase": "rag_generation",
            "message": "Il runner RAG è terminato con un errore.",
            "action": "Consulta il dettaglio tecnico autenticato e i log del servizio."}


def load_config(env=os.environ) -> dict:
    token = env.get("RAG_API_TOKEN", "")
    if len(token) < 32 or token in REJECTED_TOKENS:
        raise RuntimeError("RAG_API_TOKEN must contain at least 32 characters")
    return {
        "token": token,
        "host": env.get("RAG_API_HOST", "127.0.0.1"),
        "port": int(env.get("RAG_API_PORT", "8088")),
        "timeout": int(env.get("RAG_API_TIMEOUT_SECONDS", "900")),
        "queue_size": int(env.get("RAG_API_QUEUE_SIZE", "8")),
        "rate_limit": int(env.get("RAG_API_RATE_LIMIT_PER_MINUTE", "10")),
        "auth_failure_limit": int(env.get("RAG_API_AUTH_FAILURES_PER_MINUTE", "20")),
        "output_dir": Path(env.get("RAG_API_OUTPUT_DIR", str(ROOT / "evaluation/api-runs"))),
        "collection": env.get("RAG_COLLECTION", "dribbling_tactics_v5_multisource"),
        "expected_count": int(env.get("RAG_EXPECTED_COUNT", "5319")),
        "evidence_limit": int(env.get("RAG_API_EVIDENCE_LIMIT", "8")),
        "max_output_tokens": int(env.get("RAG_API_MAX_OUTPUT_TOKENS", "0")),
        "model": env.get("RAG_API_MODEL", "qwen3.5:9b"),
        "context_window": int(env.get("RAG_API_CONTEXT_WINDOW", "8192")),
        "keep_alive": env.get("RAG_API_KEEP_ALIVE", ""),
        "chroma_path": Path(env.get("RAG_CHROMA_PATH", str(ROOT.parent.parent / "knowledge/rag/chroma"))),
        "figc_catalog_path": Path(env.get("RAG_FIGC_CATALOG_PATH", str(ROOT.parent.parent / "knowledge/candidates/figc-discovery/catalog.json"))),
        "openrouter_copilot_enabled": env.get("RAG_OPENROUTER_COPILOT_ENABLED", "0").lower() in {"1", "true", "yes"},
        "openrouter_copilot_models": [model.strip() for model in env.get(
            "RAG_OPENROUTER_COPILOT_MODELS",
            "openai/gpt-oss-120b,google/gemini-3.8-flash,openai/gpt-6.1-sol",
        ).split(",") if model.strip()],
        "openrouter_copilot_timeout": int(env.get("RAG_OPENROUTER_COPILOT_TIMEOUT_SECONDS", "240")),
    }


def summarize_openrouter_usage(report: dict) -> dict:
    """Expose only bounded accounting fields returned by OpenRouter."""
    totals = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    cost = 0.0
    providers: list[str] = []
    for row in report.get("passes", []):
        usage = row.get("usage", {}) if isinstance(row, dict) else {}
        for key in totals:
            value = usage.get(key, 0)
            if isinstance(value, (int, float)):
                totals[key] += int(value)
        value = usage.get("cost", 0)
        if isinstance(value, (int, float)):
            cost += float(value)
        provider = row.get("provider") if isinstance(row, dict) else None
        if isinstance(provider, str) and provider and provider not in providers:
            providers.append(provider)
    return {**totals, "cost_usd": round(cost, 8), "route_providers": providers}


class State:
    def __init__(self, config: dict):
        self.config = config
        self.jobs: dict[str, dict] = {}
        self.lock = threading.RLock()
        self.requests = defaultdict(deque)
        self.auth_failures = defaultdict(deque)
        self.queue: queue.Queue[str] = queue.Queue(maxsize=config["queue_size"])
        self.knowledge_catalog: dict | None = None
        self.started_at = int(time.time())
        self.metrics_path = config["output_dir"] / "metrics.json"
        self.events_path = config["output_dir"] / "events.jsonl"
        self.metrics = self._load_metrics()
        config["output_dir"].mkdir(parents=True, exist_ok=True)
        config["output_dir"].chmod(0o700)
        self._persist_metrics()
        self.record_event("service_started", started_at=self.started_at)

    def record_event(self, event: str, **fields) -> None:
        allowed = {key: value for key, value in fields.items() if key in {
            "job_id", "status", "duration_seconds", "reason", "started_at",
            "phase", "error_code",
        }}
        row = {"timestamp": int(time.time()), "event": event, **allowed}
        with self.lock:
            with self.events_path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(row, sort_keys=True) + "\n")
            self.events_path.chmod(0o600)

    def recent_events(self, limit: int = 30) -> list[dict]:
        try:
            lines = self.events_path.read_text(encoding="utf-8").splitlines()[-limit:]
        except OSError:
            return []
        events = []
        for line in lines:
            try:
                value = json.loads(line)
                if isinstance(value, dict):
                    events.append(value)
            except json.JSONDecodeError:
                continue
        return list(reversed(events))

    def _load_metrics(self) -> dict:
        default = {"schema":"rag_api_metrics_v1","accepted":0,"succeeded":0,"failed":0,"timed_out":0,"durations_seconds":[]}
        try:
            saved = json.loads(self.metrics_path.read_text(encoding="utf-8"))
            return {**default, **saved}
        except (FileNotFoundError, json.JSONDecodeError, OSError, TypeError):
            return default

    def _persist_metrics(self) -> None:
        temporary = self.metrics_path.with_name(f".{self.metrics_path.name}.tmp")
        temporary.write_text(json.dumps(self.metrics,sort_keys=True)+"\n",encoding="utf-8")
        os.replace(temporary,self.metrics_path)

    def metrics_snapshot(self) -> dict:
        with self.lock:
            durations=list(self.metrics["durations_seconds"])
            current=defaultdict(int)
            for job in self.jobs.values(): current[job["status"]]+=1
            ordered=sorted(durations)
            def percentile(fraction):
                if not ordered: return None
                return ordered[min(len(ordered)-1,round((len(ordered)-1)*fraction))]
            feedback = {"total": 0, "helpful": 0, "not_helpful": 0}
            for path in self.config["output_dir"].glob("*.feedback.json"):
                try:
                    value = json.loads(path.read_text(encoding="utf-8"))
                    helpful = value["helpful"]
                    if not isinstance(helpful, bool):
                        continue
                    feedback["total"] += 1
                    feedback["helpful" if helpful else "not_helpful"] += 1
                except (OSError, KeyError, TypeError, json.JSONDecodeError):
                    continue
            return {
                "schema":"rag_api_observability_v1",
                "started_at":self.started_at,
                "uptime_seconds":max(0,int(time.time())-self.started_at),
                "worker_alive":bool(getattr(self,"worker_thread",None) and self.worker_thread.is_alive()),
                "queue_depth":self.queue.qsize(),"queue_capacity":self.queue.maxsize,
                "current_jobs":dict(current),
                "cumulative":{k:self.metrics[k] for k in ("accepted","succeeded","failed","timed_out")},
                "duration_samples":len(durations),
                "duration_seconds":{"min":min(durations) if durations else None,"median":statistics.median(durations) if durations else None,
                                    "p95":percentile(.95),"max":max(durations) if durations else None},
                "catalog_loaded":self.knowledge_catalog is not None,
                "collection":self.config["collection"],"expected_count":self.config["expected_count"],
                "openrouter_copilot_enabled":self.config["openrouter_copilot_enabled"],
                "feedback":feedback,
            }

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

    def auth_failure_allowed(self, client: str) -> bool:
        now = time.monotonic()
        with self.lock:
            values = self.auth_failures[client]
            while values and now - values[0] >= 60:
                values.popleft()
            if len(values) >= self.config["auth_failure_limit"]:
                return False
            values.append(now)
            return True

    def submit(self, question: str, context: dict | None = None) -> dict:
        job_id = uuid.uuid4().hex
        job = {"id": job_id, "status": "queued", "created_at": int(time.time())}
        context = context or None
        if context:
            for prior_id in context["prior_job_ids"]:
                with self.lock:
                    prior_job = dict(self.jobs.get(prior_id, {}))
                prior_job = prior_job or self.persisted_job(prior_id)
                if not prior_job or prior_job.get("status") != "succeeded":
                    raise RuntimeError("prior_job_not_succeeded")
                if (prior_job.get("session_id") != context["session_id"]
                        or prior_job.get("case_id") != context["case_id"]):
                    raise RuntimeError("prior_job_context_mismatch")
            job.update(session_id=context["session_id"], case_id=context["case_id"])
        request_path = self.config["output_dir"] / f"{job_id}.request.json"
        temporary_path = self.config["output_dir"] / f".{job_id}.request.tmp"
        request = {"id": job_id, "question": question}
        if context:
            request.update({
                "schema": "rag_api_contextual_request_v1",
                **context,
                "effective_question": effective_question(question, context["confirmed_context"]),
                "context_policy": "authenticated_client_declared_context",
                "context_provenance": "client_declared",
            })
        temporary_path.write_text(
            json.dumps(request, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        os.replace(temporary_path, request_path)
        with self.lock:
            self.jobs[job_id] = job
            self._persist_job_state(job_id)
        try:
            self.queue.put_nowait(job_id)
        except queue.Full:
            with self.lock:
                del self.jobs[job_id]
            request_path.unlink(missing_ok=True)
            raise
        with self.lock:
            self.metrics["accepted"] += 1
            self._persist_metrics()
        self.record_event("job_accepted", job_id=job_id, status="queued")
        return dict(job)

    def _persist_job_state(self, job_id: str) -> None:
        """Persist lifecycle metadata without duplicating question or answer text."""
        job = self.jobs[job_id]
        allowed = {key: job[key] for key in (
            "id", "status", "created_at", "started_at", "finished_at", "failure",
            "openrouter_copilot", "session_id", "case_id",
        ) if key in job}
        path = self.config["output_dir"] / f"{job_id}.job.json"
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_text(json.dumps(allowed, ensure_ascii=False, sort_keys=True) + "\n",
                             encoding="utf-8")
        os.replace(temporary, path)
        path.chmod(0o600)

    def persisted_job(self, job_id: str) -> dict | None:
        """Reconstruct successful and failed jobs from private files after restart."""
        request_path = self.config["output_dir"] / f"{job_id}.request.json"
        result_path = self.config["output_dir"] / f"{job_id}.result.json"
        state_path = self.config["output_dir"] / f"{job_id}.job.json"
        if not request_path.exists():
            return None
        try:
            request = json.loads(request_path.read_text(encoding="utf-8"))
            saved = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
        except (OSError, json.JSONDecodeError, TypeError):
            return None
        if not saved and not result_path.exists():
            legacy_event = next((event for event in self.recent_events(10000)
                                 if event.get("job_id") == job_id
                                 and event.get("event") == "job_finished"), None)
            if not legacy_event:
                return None
            legacy_status = legacy_event.get("status", "failed")
            saved = {"status": legacy_status,
                     "finished_at": legacy_event.get("timestamp", int(request_path.stat().st_mtime))}
            if legacy_status != "succeeded":
                saved["failure"] = classify_failure(legacy_event.get("reason"), legacy_status)
        status = saved.get("status", "succeeded" if result_path.exists() else "failed")
        job = {"id": job_id, "status": status,
               "created_at": int(request_path.stat().st_mtime),
               "started_at": int(request_path.stat().st_mtime),
               "finished_at": int(saved.get("finished_at", (
                   state_path if state_path.exists() else
                   result_path if result_path.exists() else request_path
               ).stat().st_mtime)),
               "question": request.get("question", ""),
               "recovered_after_restart": True}
        for key in ("schema", "session_id", "case_id", "confirmed_context", "prior_job_ids",
                    "effective_question", "context_policy", "context_provenance"):
            if key in request:
                job[key] = request[key]
        job.update({key: value for key, value in saved.items() if key not in {"id", "question", "result"}})
        if status == "succeeded" and result_path.exists():
            try:
                job["result"] = json.loads(result_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, TypeError):
                return None
        copilot_path = self.config["output_dir"] / f"{job_id}.openrouter-copilot.json"
        if copilot_path.exists():
            try:
                report = json.loads(copilot_path.read_text(encoding="utf-8"))
                if report.get("status") == "ESEGUITO":
                    review = report["pass1"]["reviews"][0]
                    revised = report["pass2"]["revised_answers"][0]
                    job["openrouter_copilot"] = {"status": "verified", "model": report.get("model"),
                        "provider": report.get("provider", "openrouter"),
                        **summarize_openrouter_usage(report),
                        "score": review.get("score"), "verdict": review.get("verdict"),
                        "confirmed_points": review.get("confirmed_points", []),
                        "findings": review.get("findings", []),
                        "improvement_plan": review.get("improvement_plan", []),
                        "retrieval_needs": review.get("retrieval_needs", []),
                        "checks": report["pass2"].get("checks", []),
                        "revised_answer": revised.get("answer", ""),
                        "unresolved_findings": revised.get("unresolved_findings", []),
                        "elapsed_seconds": report.get("elapsed_seconds")}
                else:
                    job["openrouter_copilot"] = {"status": "unavailable",
                        "model": report.get("model", self.config["openrouter_copilot_models"][0]),
                        "provider": "openrouter",
                        "reason": report.get("reason", "openrouter_copilot_failed")}
            except (OSError, KeyError, TypeError, json.JSONDecodeError):
                job["openrouter_copilot"] = {"status": "unavailable",
                    "model": self.config["openrouter_copilot_models"][0], "provider": "openrouter",
                    "reason": "openrouter_copilot_invalid_result"}
        feedback = self.feedback_for_job(job_id)
        if feedback is not None:
            job["feedback"] = feedback
        return job

    def session_snapshot(self, session_id: str, offset: int = 0, limit: int = 20) -> dict:
        """Rebuild one session from existing job files; no parallel archive."""
        if not isinstance(session_id, str) or not SESSION_ID_RE.fullmatch(session_id):
            raise ValueError("invalid_session_id")
        if not isinstance(offset, int) or offset < 0 or not isinstance(limit, int) or not 1 <= limit <= 50:
            raise ValueError("invalid_pagination")
        matched = []
        for path in self.config["output_dir"].glob("*.request.json"):
            try:
                request = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, TypeError):
                continue
            if request.get("session_id") != session_id:
                continue
            job_id = request.get("id", "")
            if isinstance(job_id, str) and len(job_id) == 32 and job_id.isalnum():
                matched.append((int(path.stat().st_mtime), job_id))
        matched.sort(key=lambda item: (item[0], item[1]))
        items = []
        for _, job_id in matched[offset:offset + limit]:
            job = self.persisted_job(job_id)
            if job:
                items.append({key: job[key] for key in (
                    "id", "status", "created_at", "started_at", "finished_at",
                    "session_id", "case_id", "failure",
                ) if key in job} | {"has_feedback": "feedback" in job})
        return {"schema": "rag_api_session_v1", "session_id": session_id,
                "items": items, "total": len(matched), "offset": offset, "limit": limit,
                "context_policy": "authenticated_client_declared_context",
                "access_model": "single_operator_shared_token"}

    def recent_jobs(self, limit: int = 20) -> list[dict]:
        paths = list(self.config["output_dir"].glob("*.job.json"))
        known = {path.name.removesuffix(".job.json") for path in paths}
        paths.extend(path for path in self.config["output_dir"].glob("*.result.json")
                     if path.name.removesuffix(".result.json") not in known)
        known.update(path.name.removesuffix(".result.json") for path in paths
                     if path.name.endswith(".result.json"))
        paths.extend(path for path in self.config["output_dir"].glob("*.request.json")
                     if path.name.removesuffix(".request.json") not in known)
        paths = sorted(paths,
                       key=lambda path: path.stat().st_mtime, reverse=True)
        jobs = []
        for path in paths:
            job_id = (path.name.removesuffix(".job.json").removesuffix(".result.json")
                      .removesuffix(".request.json"))
            if len(job_id) == 32 and job_id.isalnum():
                job = self.persisted_job(job_id)
                if job:
                    jobs.append(job)
            if len(jobs) >= limit:
                break
        return jobs

    def recent_completed_jobs(self, limit: int = 20) -> list[dict]:
        """Backward-compatible alias; history now includes failed jobs too."""
        return self.recent_jobs(limit)

    def run_openrouter_copilot(self, job_id: str, result_path: Path) -> dict:
        """Run the opt-in two-pass copilot; never make the RAG result depend on it."""
        models = self.config["openrouter_copilot_models"]
        model = models[0]
        if not self.config["openrouter_copilot_enabled"]:
            return {"status": "disabled", "model": model, "provider": "openrouter"}
        output = self.config["output_dir"] / f"{job_id}.openrouter-copilot.json"
        command = [str(PYTHON), str(OPENROUTER_COPILOT), str(result_path),
                   "--output", str(output), "--models", ",".join(models), "--execute"]
        self.record_event("openrouter_copilot_started", job_id=job_id, status="running")
        try:
            process = subprocess.run(command, cwd=ROOT.parent.parent, capture_output=True, text=True,
                                     timeout=self.config["openrouter_copilot_timeout"])
            report = json.loads(output.read_text(encoding="utf-8")) if output.exists() else {}
            if process.returncode == 0 and report.get("status") == "ESEGUITO":
                review = report["pass1"]["reviews"][0]
                revised = report["pass2"]["revised_answers"][0]
                summary = {"status": "verified", "model": report.get("model", model),
                    "provider": report.get("provider", "openrouter"),
                    **summarize_openrouter_usage(report),
                    "score": review.get("score"), "verdict": review.get("verdict"),
                    "confirmed_points": review.get("confirmed_points", []),
                    "findings": review.get("findings", []),
                    "improvement_plan": review.get("improvement_plan", []),
                    "retrieval_needs": review.get("retrieval_needs", []),
                    "checks": report["pass2"].get("checks", []),
                    "revised_answer": revised.get("answer", ""),
                    "unresolved_findings": revised.get("unresolved_findings", []),
                    "elapsed_seconds": report.get("elapsed_seconds"),
                    "review_file": output.name}
                self.record_event("openrouter_copilot_finished", job_id=job_id, status="verified")
                return summary
            reason = report.get("reason") or "openrouter_copilot_failed"
        except subprocess.TimeoutExpired:
            reason = "openrouter_copilot_timeout"
        except (OSError, KeyError, ValueError, json.JSONDecodeError):
            reason = "openrouter_copilot_invalid_result"
        self.record_event("openrouter_copilot_finished", job_id=job_id, status="unavailable", reason=reason)
        return {"status": "unavailable", "model": model, "provider": "openrouter", "reason": reason}

    def worker(self) -> None:
        while True:
            job_id = self.queue.get()
            try:
                request_path = self.config["output_dir"] / f"{job_id}.request.json"
                output_path = self.config["output_dir"] / f"{job_id}.result.json"
                request = json.loads(request_path.read_text(encoding="utf-8"))
                with self.lock:
                    self.jobs[job_id].update(status="running", started_at=int(time.time()))
                    self._persist_job_state(job_id)
                self.record_event("job_running", job_id=job_id, status="running")
                command = [str(PYTHON), str(RUNNER), "--question", request.get("effective_question", request["question"]), "--request-id", job_id,
                           "--output", str(output_path), "--collection", self.config["collection"],
                           "--expected-count", str(self.config["expected_count"]),
                           "--evidence-limit", str(self.config["evidence_limit"]),
                           "--max-output-tokens", str(self.config["max_output_tokens"]),
                           "--model", self.config["model"],
                           "--context-window", str(self.config["context_window"])]
                if self.config["keep_alive"]:
                    command.extend(["--keep-alive", self.config["keep_alive"]])
                try:
                    result = subprocess.run(command, cwd=ROOT.parent.parent, capture_output=True, text=True, timeout=self.config["timeout"])
                    status = "succeeded" if result.returncode == 0 and output_path.exists() else "failed"
                    detail = result.stderr[-2000:] if status == "failed" else None
                    if status == "succeeded":
                        if self.config["openrouter_copilot_enabled"]:
                            with self.lock:
                                self.jobs[job_id]["status"] = "reviewing"
                            self._persist_job_state(job_id)
                            copilot = self.run_openrouter_copilot(job_id, output_path)
                        else:
                            copilot = {"status": "disabled", "provider": "openrouter"}
                        with self.lock:
                            self.jobs[job_id]["openrouter_copilot"] = copilot
                except subprocess.TimeoutExpired:
                    status, detail = "timed_out", "runner timeout"
            except Exception as exc:
                status, detail = "failed", f"worker error: {type(exc).__name__}: {exc}"
            finally:
                with self.lock:
                    self.jobs[job_id].update(status=status, finished_at=int(time.time()))
                    if detail:
                        failure = classify_failure(detail, status)
                        self.jobs[job_id]["failure"] = failure
                        self.jobs[job_id]["error"] = failure["message"]
                    self._persist_job_state(job_id)
                    self.metrics[status] += 1
                    duration=max(0,self.jobs[job_id]["finished_at"]-self.jobs[job_id].get("started_at",self.jobs[job_id]["created_at"]))
                    self.metrics["durations_seconds"]=(self.metrics["durations_seconds"]+[duration])[-200:]
                    self._persist_metrics()
                failure = self.jobs[job_id].get("failure", {})
                reason = failure.get("code")
                self.record_event("job_finished", job_id=job_id, status=status,
                                  duration_seconds=duration, reason=reason,
                                  error_code=failure.get("code"), phase=failure.get("phase"))
                self.queue.task_done()

    def catalog(self) -> dict:
        with self.lock:
            if self.knowledge_catalog is None:
                self.knowledge_catalog = load_catalog(self.config["chroma_path"], self.config["collection"])
            return self.knowledge_catalog

    def record_feedback(self, job_id: str, helpful: bool) -> dict:
        with self.lock:
            job = self.jobs.get(job_id)
        if job is None:
            job = self.persisted_job(job_id)
        if job is None:
            raise KeyError(job_id)
        if job["status"] != "succeeded":
            raise RuntimeError("job_not_succeeded")
        feedback = {
            "schema": "rag_api_feedback_v1",
            "job_id": job_id,
            "helpful": helpful,
            "created_at": int(time.time()),
        }
        path = self.config["output_dir"] / f"{job_id}.feedback.json"
        # One current vote per job. Concurrent updates are serialized and the
        # last completed call wins while each visible write remains atomic.
        with self.lock:
            temporary = path.with_name(f".{path.name}.tmp")
            temporary.write_text(json.dumps(feedback, sort_keys=True) + "\n", encoding="utf-8")
            os.replace(temporary, path)
            path.chmod(0o600)
        return feedback

    def feedback_for_job(self, job_id: str) -> dict | None:
        """Load one validated feedback sidecar without creating another archive."""
        path = self.config["output_dir"] / f"{job_id}.feedback.json"
        if not path.exists():
            return None
        try:
            feedback = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, TypeError):
            return None
        if (feedback.get("schema") != "rag_api_feedback_v1"
                or feedback.get("job_id") != job_id
                or not isinstance(feedback.get("helpful"), bool)):
            return None
        return feedback


class Handler(BaseHTTPRequestHandler):
    server_version = "FootballRAG/1"

    @property
    def state(self) -> State:
        return self.server.state  # type: ignore[attr-defined]

    def log_message(self, fmt, *args):
        status = args[1] if len(args) > 1 else None
        print(json.dumps({"event": "http", "client": self.client_address[0], "method": self.command,
                          "path": urlparse(self.path).path, "status": status}), flush=True)

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, path: Path) -> None:
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(body)

    def authenticated(self, apply_rate_limit: bool = False) -> bool:
        if not self.state.authorized(self.headers.get("Authorization")):
            allowed = self.state.auth_failure_allowed(self.client_address[0])
            self.send_json(HTTPStatus.UNAUTHORIZED if allowed else HTTPStatus.TOO_MANY_REQUESTS,
                           {"error": "unauthorized" if allowed else "auth_rate_limited"})
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
        if parsed.path in {"/panel", "/panel/"}:
            self.send_html(PANEL)
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
        if parsed.path == "/v1/metrics":
            self.send_json(HTTPStatus.OK, self.state.metrics_snapshot())
            return
        if parsed.path == "/v1/events":
            query = parse_qs(parsed.query)
            try:
                limit = min(100, max(1, int(query.get("limit", ["30"])[0])))
            except ValueError:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_limit"}); return
            self.send_json(HTTPStatus.OK, {"schema": "rag_api_events_v1", "items": self.state.recent_events(limit)})
            return
        if parsed.path == "/v1/jobs/recent":
            query = parse_qs(parsed.query)
            try:
                limit = min(50, max(1, int(query.get("limit", ["20"])[0])))
            except ValueError:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_limit"}); return
            self.send_json(HTTPStatus.OK, {"schema": "rag_api_recent_jobs_v1",
                                           "items": self.state.recent_completed_jobs(limit)})
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
        if parsed.path == "/v1/knowledge/figc":
            catalog = load_figc_catalog(self.state.config["figc_catalog_path"])
            self.send_json(HTTPStatus.OK, {**catalog, "total": len(catalog["documents"]),
                                           "error_count": len(catalog["errors"])})
            return
        if parsed.path == "/v1/knowledge/search":
            if not self.state.rate_allowed(self.client_address[0]):
                self.send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "rate_limited"}); return
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
        session_prefix = "/v1/sessions/"
        if parsed.path.startswith(session_prefix):
            session_id = parsed.path[len(session_prefix):]
            try:
                query = parse_qs(parsed.query)
                offset = int(query.get("offset", ["0"])[0])
                limit = int(query.get("limit", ["20"])[0])
                snapshot = self.state.session_snapshot(session_id, offset, limit)
            except ValueError:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_session_request"}); return
            self.send_json(HTTPStatus.OK, snapshot)
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
                job = self.state.persisted_job(job_id)
                if job:
                    self.send_json(HTTPStatus.OK, job)
                    return
                request_path = self.state.config["output_dir"] / f"{job_id}.request.json"
                if request_path.exists():
                    self.state.record_event("job_unavailable", job_id=job_id, reason="service_restart")
                    self.send_json(HTTPStatus.GONE, {"error": "job_lost_after_restart"})
                    return
                self.state.record_event("job_unavailable", job_id=job_id, reason="unknown_job")
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                return
            if job["status"] == "succeeded":
                result_path = self.state.config["output_dir"] / f"{job_id}.result.json"
                job["result"] = json.loads(result_path.read_text(encoding="utf-8"))
            feedback = self.state.feedback_for_job(job_id)
            if feedback is not None:
                job["feedback"] = feedback
            self.send_json(HTTPStatus.OK, job)
            return
        self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self):
        if self.path not in {"/v1/query", "/v1/feedback"}:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        if not self.authenticated(apply_rate_limit=True):
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        maximum = 1024 if self.path == "/v1/feedback" else 16384
        if not 1 <= length <= maximum:
            self.send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "invalid_body_size"})
            return
        if self.path == "/v1/feedback":
            try:
                payload = json.loads(self.rfile.read(length))
                if set(payload) != {"job_id", "helpful"} or not isinstance(payload["helpful"], bool):
                    raise ValueError
                job_id = payload["job_id"]
                if not isinstance(job_id, str) or len(job_id) != 32 or not job_id.isalnum():
                    raise ValueError
                feedback = self.state.record_feedback(job_id, payload["helpful"])
            except (ValueError, TypeError, json.JSONDecodeError):
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_request"}); return
            except KeyError:
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"}); return
            except RuntimeError:
                self.send_json(HTTPStatus.CONFLICT, {"error": "job_not_succeeded"}); return
            self.send_json(HTTPStatus.OK, feedback)
            return
        try:
            payload = json.loads(self.rfile.read(length))
            question, context = normalize_query_payload(payload)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_request"})
            return
        try:
            job = self.state.submit(question, context)
        except queue.Full:
            self.send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "queue_full"})
            return
        except RuntimeError as exc:
            if str(exc) in {"prior_job_not_succeeded", "prior_job_context_mismatch"}:
                self.send_json(HTTPStatus.CONFLICT, {"error": str(exc)})
                return
            raise
        self.send_json(HTTPStatus.ACCEPTED, job)


class BoundedHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 32

    def __init__(self, address, handler, max_connections=32, read_timeout=15):
        self._slots = threading.BoundedSemaphore(max_connections)
        self._read_timeout = read_timeout
        super().__init__(address, handler)

    def process_request(self, request, client_address):
        if not self._slots.acquire(blocking=False):
            request.close(); return
        try:
            request.settimeout(self._read_timeout)
            super().process_request(request, client_address)
        except Exception:
            self._slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._slots.release()


def main() -> None:
    os.umask(0o077)
    config = load_config()
    state = State(config)
    state.worker_thread = threading.Thread(target=state.worker, daemon=True, name="rag-worker")
    state.worker_thread.start()
    server = BoundedHTTPServer((config["host"], config["port"]), Handler)
    server.state = state  # type: ignore[attr-defined]
    print(json.dumps({"event": "startup", "host": config["host"], "port": config["port"]}), flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
