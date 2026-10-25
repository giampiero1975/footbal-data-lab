#!/usr/bin/env python3
"""Opt-in Groq Free external reviewer adapter. Dry-run unless --execute."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

from review_runtime_series_gemini_v1 import PROMPT, extract_case, validate_review

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-120b"
RETRYABLE = {429, 500, 502, 503, 504}
STOP = {400, 401, 403}
LIMITS = {"requests_per_day": 1000, "tokens_per_day": 200000, "tokens_per_minute": 8000}

REVIEW_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["reviews", "series_limitations"],
    "properties": {
        "reviews": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "score", "verdict", "strengths", "structural_errors", "evidence_issues", "minimum_fix"],
            "properties": {
                "id": {"type": "string"}, "score": {"type": "number", "minimum": 0, "maximum": 10},
                "verdict": {"type": "string", "enum": ["PASS", "REVISIONE"]},
                "strengths": {"type": "array", "items": {"type": "string"}},
                "structural_errors": {"type": "array", "items": {"type": "string"}},
                "evidence_issues": {"type": "array", "items": {"type": "string"}},
                "minimum_fix": {"type": "string"},
            }}},
        "series_limitations": {"type": "array", "items": {"type": "string"}},
    },
}


def prepare_cases(paths: list[Path]) -> tuple[list[dict], dict[str, str]]:
    cases = [extract_case(path) for path in paths]
    runtime_ids = [case["id"] for case in cases]
    if len(runtime_ids) != len(set(runtime_ids)):
        raise ValueError("DUPLICATE_RUNTIME_ID")
    mapping = {}
    for number, case in enumerate(cases, 1):
        if case.get("invalid_citation_ids"):
            raise ValueError("INPUT_HAS_INVALID_CITATIONS")
        available = {str(item.get("label", "")).lstrip("F") for item in case["evidence"]}
        if any(str(value).lstrip("F") not in available for value in case.get("citation_ids", [])):
            raise ValueError("INPUT_CITATION_NOT_IN_EVIDENCE")
        short_id = f"case_{number:02d}"; mapping[short_id] = case["id"]
        case["runtime_id"] = case["id"]; case["id"] = short_id
    return cases, mapping


def build_request(cases: list[dict], model: str = DEFAULT_MODEL) -> dict:
    return {
        "model": model, "temperature": 0, "n": 1, "stream": False,
        "messages": [{"role": "system", "content": PROMPT},
                     {"role": "user", "content": json.dumps({"cases": cases}, ensure_ascii=False)}],
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "football_data_lab_external_review", "strict": True, "schema": REVIEW_SCHEMA}},
    }


def validate_response(payload: dict, ids: list[str]) -> dict:
    content = payload["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    rows = validate_review(parsed, ids)
    return {"reviews": rows, "series_limitations": parsed.get("series_limitations", [])}


def http_policy(status: int, retry_after: str | None = None) -> dict:
    if status == 200: return {"action": "accept", "delay_seconds": 0}
    if status in RETRYABLE:
        try: delay = max(1, min(3600, int(float(retry_after or "30"))))
        except ValueError: delay = 30
        return {"action": "retry", "delay_seconds": delay}
    return {"action": "stop", "delay_seconds": 0}


def quota_allowed(ledger: dict, day: str, estimated_tokens: int, limits: dict = LIMITS) -> bool:
    row = ledger.get(day, {})
    return (int(row.get("requests", 0)) + 1 <= limits["requests_per_day"] and
            int(row.get("tokens", 0)) + estimated_tokens <= limits["tokens_per_day"] and
            estimated_tokens <= limits["tokens_per_minute"])


def pending_ids(all_ids: list[str], state: dict) -> list[str]:
    completed = set(state.get("completed_ids", []))
    return [case_id for case_id in all_ids if case_id not in completed]


def atomic_new(path: Path, payload: dict) -> None:
    if path.exists(): raise SystemExit(f"REFUSING_OVERWRITE: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); tmp.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+", type=Path); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL); parser.add_argument("--estimated-tokens", type=int, default=2850)
    parser.add_argument("--execute", action="store_true"); parser.add_argument("--confirm-free-tier", action="store_true")
    args = parser.parse_args(); cases, mapping = prepare_cases(args.reports); request = build_request(cases, args.model)
    meta = {"schema": "groq_free_reviewer_report_v1", "provider": "groq", "model": args.model,
            "case_count": len(cases), "runtime_case_map": mapping,
            "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(),
            "payload_sha256": hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest(),
            "network_called": False, "pipeline_writes": False, "index_writes": False}
    if not args.execute:
        atomic_new(args.output, {**meta, "status": "VALIDATO", "result": "OFFLINE_PREFLIGHT_PASS"})
        print("OFFLINE_PREFLIGHT_PASS API_REQUESTS=0"); return
    if not args.confirm_free_tier: raise SystemExit("FREE_TIER_CONFIRMATION_REQUIRED")
    key = os.environ.get("GROQ_API_KEY", "")
    if not key: raise SystemExit("GROQ_API_KEY_MISSING")
    day = dt.datetime.now(dt.timezone.utc).date().isoformat(); ledger_path = ROOT / "evaluation/.groq_free_ledger.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    if not quota_allowed(ledger, day, args.estimated_tokens): raise SystemExit("LOCAL_DAILY_BUDGET_EXHAUSTED")
    req = urllib.request.Request(ENDPOINT, data=json.dumps(request).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                                          "User-Agent": "football-data-lab-groq-reviewer/1.0"})
    started = dt.datetime.now(dt.timezone.utc)
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            payload = json.loads(response.read()); status = response.status
        validated = validate_response(payload, list(mapping))
        usage = payload.get("usage", {}); used_tokens = int(usage.get("total_tokens", args.estimated_tokens))
        ledger[day] = {"requests": int(ledger.get(day, {}).get("requests", 0)) + 1,
                       "tokens": int(ledger.get(day, {}).get("tokens", 0)) + used_tokens}
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
        atomic_new(args.output, {**meta, "network_called": True, "status": "ESEGUITO", "http_status": status,
            "elapsed_seconds": (dt.datetime.now(dt.timezone.utc)-started).total_seconds(), "usage": usage, **validated})
    except urllib.error.HTTPError as exc:
        policy = http_policy(exc.code, exc.headers.get("retry-after"))
        raw_error = exc.read().decode(errors="replace")[:1000]
        try:
            error_payload = json.loads(raw_error)
            error_message = str(error_payload.get("error", {}).get("message", "http_error"))[:500]
            error_type = str(error_payload.get("error", {}).get("type", type(exc).__name__))[:100]
        except (json.JSONDecodeError, AttributeError, TypeError):
            error_message = " ".join(raw_error.split())[:500] or "empty_http_error"
            error_type = type(exc).__name__
        atomic_new(args.output, {**meta, "network_called": True, "status": "BLOCCATO",
                                 "http_status": exc.code, "policy": policy, "error_type": error_type,
                                 "error_message": error_message.replace(key, "[REDACTED]")})
        raise SystemExit(2)


if __name__ == "__main__": main()
