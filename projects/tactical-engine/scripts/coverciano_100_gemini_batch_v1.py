#!/usr/bin/env python3
"""Submit and retrieve the Gemini Batch job for the Coverciano-100 manifest."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts/generate_coverciano_100_gemini_v1.py"


def generator_module():
    spec = importlib.util.spec_from_file_location("coverciano_generator", GENERATOR)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def key() -> str:
    path = ROOT / ".env"
    if path.is_file():
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.strip().startswith("GEMINI_API_KEY="):
                os.environ.setdefault("GEMINI_API_KEY", raw.split("=", 1)[1].strip().strip("'\"")); break
    value = os.environ.get("GEMINI_API_KEY", "")
    if not value: raise SystemExit("GEMINI_API_KEY_MISSING")
    return value


def request_json(url: str, api_key: str, payload: dict | None = None) -> dict:
    request = urllib.request.Request(url, data=json.dumps(payload).encode() if payload else None,
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST" if payload else "GET")
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:1000]
        raise SystemExit(f"BATCH_HTTP_{exc.code}: {detail.replace(api_key, '[REDACTED]')}")


def write_new(path: Path, payload: dict) -> None:
    if path.exists(): raise SystemExit(f"REFUSING_OVERWRITE: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def prompt_request(module) -> dict:
    system = f"""Sei una commissione d'esame tattico per allenatori di livello UEFA Pro.
Genera esattamente 100 tracce originali, realistiche e difficili. Distribuisci
esattamente 10 domande per ciascuna categoria: {', '.join(module.CATEGORIES)}.
Ogni domanda descrive scenario, sistemi, fase, tempo/punteggio e vincoli e
richiede compiti e geometrie concrete. Difficulty 3, 4 o 5. SOLO JSON:
{{"questions":[{{"id":"coverciano_001","category":"...","difficulty":4,
"question":"...","hidden_rubric":{{"constraints":["..."],"expected_points":["..."],
"critical_errors":["..."]}}}}]}}. ID ordinati fino a coverciano_100.
Rubrica nascosta separata e nessuna domanda equivalente."""
    return {"contents": [{"role": "user", "parts": [{"text": module.BASE_PROMPT}]}],
            "system_instruction": {"parts": [{"text": system}]},
            "generation_config": {"temperature": 0.7, "responseMimeType": "application/json", "maxOutputTokens": 60000}}


def main() -> None:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="action", required=True)
    submit = sub.add_parser("submit"); submit.add_argument("--model", default="gemini-3.6-flash")
    submit.add_argument("--job-output", type=Path, required=True)
    status = sub.add_parser("status"); status.add_argument("--job-file", type=Path, required=True)
    status.add_argument("--status-output", type=Path, required=True)
    status.add_argument("--manifest-output", type=Path)
    args = parser.parse_args(); module = generator_module(); api_key = key()
    if args.action == "submit":
        payload = {"batch": {"display_name": "football-data-lab-coverciano-100-v1",
            "input_config": {"requests": {"requests": [{"request": prompt_request(module),
                                                           "metadata": {"key": "coverciano-100-v1"}}]}}}}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{args.model}:batchGenerateContent"
        response = request_json(url, api_key, payload)
        report = {"schema": "coverciano_gemini_batch_job_v1", "submitted_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                  "model": args.model, "base_prompt": module.BASE_PROMPT, "name": response.get("name"), "response": response}
        if not report["name"]: raise SystemExit("BATCH_NAME_MISSING")
        write_new(args.job_output, report); print(json.dumps({"name": report["name"], "model": args.model}))
        return
    job = json.loads(args.job_file.read_text(encoding="utf-8")); name = job["name"]
    response = request_json(f"https://generativelanguage.googleapis.com/v1beta/{name}", api_key)
    write_new(args.status_output, response)
    state = response.get("state", "UNKNOWN"); print(json.dumps({"name": name, "state": state}))
    if state != "JOB_STATE_SUCCEEDED" or not args.manifest_output: return
    inline = response["dest"]["inlinedResponses"][0]
    text = "".join(part.get("text", "") for part in inline["response"]["candidates"][0]["content"]["parts"])
    rows = module.validate(json.loads(text).get("questions"))
    manifest = {"schema": "coverciano_gemini_question_manifest_v1", "status": "ESEGUITO",
        "transport": "Gemini Batch API", "batch_name": name, "model": job["model"], "base_prompt": module.BASE_PROMPT,
        "question_count": 100, "categories": {c: sum(r["category"] == c for r in rows) for c in module.CATEGORIES},
        "questions_sha256": hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        "questions": rows}
    write_new(args.manifest_output, manifest)


if __name__ == "__main__": main()
