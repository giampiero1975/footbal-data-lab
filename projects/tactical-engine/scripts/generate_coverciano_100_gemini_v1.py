#!/usr/bin/env python3
"""Generate and freeze 100 Coverciano-style tactical questions with Gemini."""
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

ROOT = Path(__file__).resolve().parents[1]
MODEL = "gemini-3.6-flash"
BASE_PROMPT = "fammi 100 domande da commissione all'esame da allenatore a coverciano sulla tattica"
CATEGORIES = (
    "costruzione", "sviluppo_rifinitura", "transizione_positiva",
    "transizione_negativa", "pressing", "blocco_difensivo",
    "gestione_partita", "palle_inattive", "adattamenti_strutturali",
    "metodologia_allenamento",
)


def load_key() -> str:
    path = ROOT / ".env"
    if path.is_file():
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.strip().startswith("GEMINI_API_KEY="):
                os.environ.setdefault("GEMINI_API_KEY", raw.split("=", 1)[1].strip().strip("'\""))
                break
    return os.environ.get("GEMINI_API_KEY", "")


def validate(rows: object) -> list[dict]:
    if not isinstance(rows, list) or len(rows) != 100:
        raise ValueError("EXPECTED_EXACTLY_100_QUESTIONS")
    ids, normalized = set(), set()
    counts = {category: 0 for category in CATEGORIES}
    for number, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ValueError("INVALID_ROW")
        expected_id = f"coverciano_{number:03d}"
        if row.get("id") != expected_id or expected_id in ids:
            raise ValueError("INVALID_OR_DUPLICATE_ID")
        ids.add(expected_id)
        category = row.get("category")
        if category not in counts:
            raise ValueError("INVALID_CATEGORY")
        counts[category] += 1
        question = " ".join(str(row.get("question", "")).split())
        key = re.sub(r"[^a-z0-9]+", " ", question.casefold()).strip()
        if len(question) < 120 or key in normalized:
            raise ValueError("SHORT_OR_DUPLICATE_QUESTION")
        normalized.add(key)
        if row.get("difficulty") not in (3, 4, 5):
            raise ValueError("INVALID_DIFFICULTY")
        rubric = row.get("hidden_rubric")
        if not isinstance(rubric, dict) or not all(isinstance(rubric.get(field), list) and rubric[field]
                                                   for field in ("constraints", "expected_points", "critical_errors")):
            raise ValueError("INVALID_RUBRIC")
    if set(counts.values()) != {10}:
        raise ValueError("UNBALANCED_CATEGORIES")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--confirm-gemini-generation", action="store_true")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"REFUSING_OVERWRITE: {args.output}")
    if not args.confirm_gemini_generation:
        raise SystemExit("GEMINI_GENERATION_CONFIRMATION_REQUIRED")
    key = load_key()
    if not key:
        raise SystemExit("GEMINI_API_KEY_MISSING")
    system = f"""Sei una commissione d'esame tattico per allenatori di livello UEFA Pro.
Genera esattamente 100 tracce originali, realistiche e difficili. Distribuisci
esattamente 10 domande per ciascuna categoria: {', '.join(CATEGORIES)}.
Ogni domanda deve descrivere scenario, sistemi, fase, tempo/punteggio e vincoli;
deve richiedere compiti e geometrie concrete, non definizioni astratte. Evita
domande equivalenti. Difficulty deve essere 3, 4 o 5. Restituisci SOLO JSON:
{{"questions":[{{"id":"coverciano_001","category":"...","difficulty":4,
"question":"...","hidden_rubric":{{"constraints":["..."],
"expected_points":["..."],"critical_errors":["..."]}}}}]}}.
Gli ID devono andare in ordine da coverciano_001 a coverciano_100. La rubrica
non deve suggerire la risposta nel testo della domanda."""
    request = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": BASE_PROMPT}]}],
        "generationConfig": {"temperature": 0.7, "responseMimeType": "application/json", "maxOutputTokens": 60000},
    }
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    req = urllib.request.Request(endpoint, data=json.dumps(request).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    started = dt.datetime.now(dt.timezone.utc)
    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            payload = json.loads(response.read())
        text = "".join(part.get("text", "") for part in payload["candidates"][0]["content"]["parts"])
        parsed = json.loads(text)
        rows = validate(parsed.get("questions"))
    except (urllib.error.HTTPError, urllib.error.URLError, KeyError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"GENERATION_FAILED: {type(exc).__name__}: {str(exc)[:300].replace(key, '[REDACTED]')}")
    report = {
        "schema": "coverciano_gemini_question_manifest_v1",
        "status": "ESEGUITO",
        "model": MODEL,
        "base_prompt": BASE_PROMPT,
        "generated_at_utc": started.isoformat(),
        "question_count": len(rows),
        "categories": {category: sum(row["category"] == category for row in rows) for category in CATEGORIES},
        "questions_sha256": hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        "usage_metadata": payload.get("usageMetadata", {}),
        "questions": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(f".{args.output.name}.tmp.{os.getpid()}")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(args.output)
    print(json.dumps({key: report[key] for key in ("status", "model", "question_count", "categories", "questions_sha256")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
