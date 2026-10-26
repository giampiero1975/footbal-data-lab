#!/usr/bin/env python3
"""Two-pass tactical copilot routed through one OpenRouter API key.

The tactical contract and fail-closed validators are reused from the frozen
Groq experiment.  This module owns the active transport and never calls Groq
or Gemini directly.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request

from groq_tactical_copilot_v2 import (
    PASS1_PROMPT, PASS1_SCHEMA, PASS2_PROMPT, PASS2_SCHEMA, atomic_new,
    normalize_pass1, normalize_pass2, prepare_inputs, validate_pass1,
    validate_pass2,
)

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODELS = [
    "openai/gpt-oss-120b",
    "google/gemini-3.8-flash",
    "openai/gpt-6.1-sol",
]


def strict_request(prompt: str, body: dict, schema: dict, name: str,
                   models: list[str]) -> dict:
    if not models:
        raise ValueError("OPENROUTER_MODEL_LIST_EMPTY")
    request = {
        "model": models[0],
        "models": models,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(body, ensure_ascii=False)},
        ],
        "response_format": {"type": "json_schema", "json_schema": {
            "name": name, "strict": True, "schema": schema,
        }},
        "provider": {
            "allow_fallbacks": True,
            "require_parameters": True,
            "data_collection": "deny",
        },
    }
    if models[0].startswith("openai/gpt-6"):
        request["reasoning"] = {"effort": "high"}
    else:
        request["temperature"] = 0.1
    return request


def build_pass1(cases: list[dict], models: list[str]) -> dict:
    minimal = [{"id": c["id"], "question": c["question"], "answer": c["answer"]}
               for c in cases]
    schema = json.loads(json.dumps(PASS1_SCHEMA))
    schema["properties"]["reviews"].update(
        {"minItems": len(cases), "maxItems": len(cases)})
    prompt = PASS1_PROMPT + (
        f" Restituisci esattamente {len(cases)} elemento/i in reviews, uno per ogni "
        "caso ricevuto, senza aggiungere o omettere casi.")
    return strict_request(prompt, {"cases": minimal}, schema,
                          "openrouter_tactical_copilot_pass1_v1", models)


def build_pass2(cases: list[dict], pass1: dict, models: list[str]) -> dict:
    by_id = {row["id"]: row for row in pass1["reviews"]}
    body = {"cases": [{"id": c["id"], "question": c["question"],
                        "original_answer": c["answer"],
                        "replacement_answer": by_id[c["id"]]["replacement_answer"],
                        "improvement_plan": by_id[c["id"]]["improvement_plan"],
                        "findings": by_id[c["id"]]["findings"],
                        "evidence": c["evidence"]} for c in cases]}
    schema = json.loads(json.dumps(PASS2_SCHEMA))
    schema["properties"]["revised_answers"].update(
        {"minItems": len(cases), "maxItems": len(cases)})
    return strict_request(PASS2_PROMPT, body, schema,
                          "openrouter_tactical_copilot_pass2_v1", models)


def call_openrouter(request: dict, key: str, timeout: int = 180) -> tuple[dict, float]:
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(request).encode(), method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "football-data-lab-openrouter-copilot/1.0",
            "HTTP-Referer": "https://football-lab.byoursite.com",
            "X-Title": "FOOTBALL-DATA-LAB",
        },
    )
    started = dt.datetime.now(dt.timezone.utc)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = json.loads(response.read())
    return payload, (dt.datetime.now(dt.timezone.utc) - started).total_seconds()


def parsed_content(payload: dict) -> dict:
    return json.loads(payload["choices"][0]["message"]["content"])


def redacted_failure_reason(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        return f"OPENROUTER_HTTP_{exc.code}"
    if isinstance(exc, urllib.error.URLError):
        return "OPENROUTER_NETWORK_ERROR"
    if isinstance(exc, TimeoutError):
        return "OPENROUTER_TIMEOUT"
    if isinstance(exc, ValueError) and re.fullmatch(r"(PASS[12]|OPENROUTER)_[A-Z0-9_]+", str(exc)):
        return str(exc)
    if isinstance(exc, (json.JSONDecodeError, KeyError, TypeError, ValueError)):
        return "OPENROUTER_INVALID_STRUCTURED_RESPONSE"
    return "OPENROUTER_UNEXPECTED_ERROR"


def write_failure(output: Path, models: list[str], reason: str) -> None:
    atomic_new(output, {
        "schema": "openrouter_tactical_copilot_runtime_v1",
        "status": "BLOCCATO", "provider": "openrouter", "model": models[0],
        "requested_models": models, "reason": reason, "network_called": True,
        "rag_executed": False, "index_writes": False,
        "contains_prompt_or_evidence": False,
    })


def execute(paths: list[Path], output: Path, models: list[str]) -> None:
    cases, mapping = prepare_inputs(paths)
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        raise SystemExit("OPENROUTER_API_KEY_MISSING")
    req1 = build_pass1(cases, models)
    payload1, elapsed1 = call_openrouter(req1, key)
    pass1, notes1 = normalize_pass1(parsed_content(payload1), list(mapping))
    pass1 = validate_pass1(pass1, list(mapping))
    req2 = build_pass2(cases, pass1, models)
    payload2, elapsed2 = call_openrouter(req2, key)
    pass2, notes2 = normalize_pass2(parsed_content(payload2), cases, pass1)
    pass2 = validate_pass2(pass2, cases, pass1)
    actual_models = [payload1.get("model", models[0]), payload2.get("model", models[0])]
    actual_providers = [payload1.get("provider"), payload2.get("provider")]
    atomic_new(output, {
        "schema": "openrouter_tactical_copilot_runtime_v1", "status": "ESEGUITO",
        "provider": "openrouter", "model": actual_models[-1],
        "requested_models": models, "actual_models": actual_models,
        "actual_providers": actual_providers, "runtime_case_map": mapping,
        "network_called": True, "rag_executed": False, "index_writes": False,
        "elapsed_seconds": round(elapsed1 + elapsed2, 3),
        "mechanical_normalizations": notes1 + notes2,
        "passes": [
            {"elapsed_seconds": elapsed1, "usage": payload1.get("usage", {}),
             "model": actual_models[0], "provider": actual_providers[0]},
            {"elapsed_seconds": elapsed2, "usage": payload2.get("usage", {}),
             "model": actual_models[1], "provider": actual_providers[1]},
        ],
        "pass1": pass1, "pass2": pass2,
    })


def preflight(paths: list[Path], output: Path, models: list[str]) -> None:
    cases, mapping = prepare_inputs(paths)
    request1 = build_pass1(cases, models)
    synthetic = {"reviews": [{
        "id": c["id"], "score": 0, "verdict": "REVISIONE",
        "answered_parts": [], "missing_parts": [], "digressions": [],
        "confirmed_points": [], "findings": [], "improvement_plan": [],
        "replacement_answer": "Preflight placeholder operativo. " * 20,
        "retrieval_needs": [],
    } for c in cases], "limitations": []}
    validate_pass1(synthetic, list(mapping))
    request2 = build_pass2(cases, synthetic, models)
    atomic_new(output, {
        "schema": "openrouter_tactical_copilot_preflight_v1", "status": "VALIDATO",
        "provider": "openrouter", "requested_models": models,
        "case_count": len(cases), "runtime_case_map": mapping,
        "pass1_payload_sha256": hashlib.sha256(json.dumps(request1, sort_keys=True).encode()).hexdigest(),
        "pass2_payload_sha256": hashlib.sha256(json.dumps(request2, sort_keys=True).encode()).hexdigest(),
        "network_called": False, "rag_executed": False, "index_writes": False,
        "result": "OFFLINE_PREFLIGHT_PASS",
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS))
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    models = [value.strip() for value in args.models.split(",") if value.strip()]
    if not args.execute:
        preflight(args.reports, args.output, models)
        print("OFFLINE_PREFLIGHT_PASS API_REQUESTS=0")
        return
    try:
        execute(args.reports, args.output, models)
    except SystemExit:
        raise
    except Exception as exc:
        reason = redacted_failure_reason(exc)
        write_failure(args.output, models, reason)
        raise SystemExit(reason) from None
    print("COPILOT_COMPLETE")


if __name__ == "__main__":
    main()
