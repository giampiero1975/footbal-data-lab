#!/usr/bin/env python3
"""Strict shadow review of existing runtime RAG reports through Gemini REST.

This script never runs the RAG and never writes Chroma. It sends only the
question, answer and already selected evidence of each supplied report.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_MODELS = ("gemini-3.1-flash-lite", "gemini-3.6-flash", "gemini-3.8-flash")
DEFAULT_MODEL = "gemini-3.6-flash"

PROMPT = """Sei un revisore tattico esterno severo e indipendente. Valuta ogni
risposta RAG da 0.0 a 10.0. Non premiare il tono, il lessico o la presenza di
citazioni se la geometria sul campo e sbagliata. Controlla: rispetto dei vincoli
della domanda, coerenza di moduli e ruoli, fase di gioco, lato palla/lato debole,
superiorita/coperture, pertinenza delle evidenze e contraddizioni interne.
Le evidenze sono il contesto realmente ricevuto dal RAG: segnala se sono
insufficienti o fuori fase. Non riscrivere una risposta celebrativa e non
arrotondare i voti verso l'alto. Restituisci SOLO JSON con questo schema:
{"reviews":[{"id":"...","score":0.0,"verdict":"PASS|REVISIONE",
"strengths":["..."],"structural_errors":["..."],
"evidence_issues":["..."],"minimum_fix":"..."}],
"series_limitations":["..."]}. PASS richiede score >= 8.0 e nessun errore
strutturale grave. Non calcolare la media: viene calcolata localmente.
"""


def load_env() -> None:
    path = ROOT / ".env"
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("GEMINI_API_KEY="):
            value = line.split("=", 1)[1].strip().strip("'\"")
            if value:
                os.environ.setdefault("GEMINI_API_KEY", value)
            return


def atomic_write(path: Path, payload: dict) -> None:
    if path.exists():
        raise SystemExit(f"REFUSING_OVERWRITE: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    try:
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(path)
    finally:
        if tmp.exists():
            tmp.unlink()


def extract_case(path: Path) -> dict:
    raw = path.read_bytes()
    report = json.loads(raw)
    questions = report.get("questions", [])
    if len(questions) != 1:
        raise SystemExit(f"EXPECTED_ONE_QUESTION: {path}")
    row = questions[0]
    if not row.get("question") or not row.get("answer"):
        raise SystemExit(f"MISSING_QUESTION_OR_ANSWER: {path}")
    evidence = []
    for item in row.get("evidence", []):
        evidence.append({key: item.get(key) for key in
                         ("label", "source", "pages", "headings", "text")})
    return {
        "id": row.get("id") or path.stem,
        "report_file": path.name,
        "report_sha256": hashlib.sha256(raw).hexdigest(),
        "question": row["question"],
        "answer": row["answer"],
        "citation_ids": row.get("citation_ids", []),
        "invalid_citation_ids": row.get("invalid_citation_ids", []),
        "evidence": evidence,
    }


def validate_review(review: dict, ids: list[str]) -> list[dict]:
    rows = review.get("reviews")
    if not isinstance(rows, list) or len(rows) != len(ids):
        raise ValueError("INCOMPLETE_REVIEW_COUNT")
    got = [row.get("id") for row in rows]
    if sorted(got) != sorted(ids):
        raise ValueError("REVIEW_ID_MISMATCH")
    for row in rows:
        score = row.get("score")
        if not isinstance(score, (int, float)) or not 0 <= float(score) <= 10:
            raise ValueError("INVALID_SCORE")
        if row.get("verdict") not in ("PASS", "REVISIONE"):
            raise ValueError("INVALID_VERDICT")
        if (float(score) >= 8) != (row["verdict"] == "PASS"):
            raise ValueError("SCORE_VERDICT_MISMATCH")
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("reports", type=Path, nargs="+")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--model", choices=ALLOWED_MODELS, default=DEFAULT_MODEL)
    ap.add_argument("--max-daily-requests", type=int, default=10)
    ap.add_argument("--confirm-free-tier", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cases = [extract_case(path) for path in args.reports]
    runtime_ids = [row["id"] for row in cases]
    if len(set(runtime_ids)) != len(runtime_ids):
        raise SystemExit("DUPLICATE_CASE_ID")
    case_map = {}
    for number, row in enumerate(cases, 1):
        short_id = f"case_{number:02d}"
        case_map[short_id] = row["id"]
        row["runtime_id"] = row["id"]
        row["id"] = short_id
    ids = list(case_map)
    meta = {"model": args.model, "cases": len(cases), "case_ids": ids,
            "runtime_case_map": case_map,
            "rag_executed": False, "index_writes": False}
    if args.dry_run:
        print(json.dumps({"preflight": "PASS", **meta}, indent=2))
        return
    if not args.confirm_free_tier:
        raise SystemExit("FREE_TIER_CONFIRMATION_REQUIRED")
    load_env()
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        raise SystemExit("GEMINI_API_KEY_MISSING")
    ledger = ROOT / "evaluation/.gemini_review_request_ledger.json"
    used = json.loads(ledger.read_text(encoding="utf-8")) if ledger.exists() else {}
    now = dt.datetime.now(dt.timezone.utc)
    day = now.astimezone(ZoneInfo("America/Los_Angeles")).date().isoformat()
    count = max(int(used.get(now.date().isoformat(), 0)), int(used.get("PT:" + day, 0)))
    if count >= args.max_daily_requests:
        raise SystemExit("LOCAL_DAILY_BUDGET_EXHAUSTED")
    used["PT:" + day] = count + 1
    ledger.write_text(json.dumps(used, indent=2), encoding="utf-8")
    request = {
        "system_instruction": {"parts": [{"text": PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": json.dumps(
            {"cases": cases}, ensure_ascii=False)}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
    }
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{args.model}:generateContent"
    req = urllib.request.Request(endpoint, data=json.dumps(request).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    output = {**meta, "generated_at_utc": now.isoformat(),
              "input_reports": [{"file": c["report_file"], "sha256": c["report_sha256"]} for c in cases]}
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            payload = json.loads(response.read())
        text = "".join(part.get("text", "") for part in payload["candidates"][0]["content"]["parts"])
        parsed = json.loads(text)
        output["raw_review"] = parsed
        output["raw_response_sha256"] = hashlib.sha256(text.encode()).hexdigest()
        rows = validate_review(parsed, ids)
        scores = [float(row["score"]) for row in rows]
        output.update({"status": "ESEGUITO", "reviews": rows,
                       "average_score": round(sum(scores) / len(scores), 3),
                       "pass_count": sum(score >= 8 for score in scores),
                       "target_average": 8.0,
                       "target_reached": sum(scores) / len(scores) >= 8,
                       "series_limitations": parsed.get("series_limitations", []),
                       "usage_metadata": payload.get("usageMetadata", {}),
                       })
    except (urllib.error.HTTPError, urllib.error.URLError, KeyError, ValueError,
            json.JSONDecodeError) as exc:
        output.update({"status": "BLOCCATO", "error_type": type(exc).__name__,
                       "http_status": getattr(exc, "code", None),
                       "reason": str(exc)[:300].replace(key, "[REDACTED]")})
    atomic_write(args.output, output)
    print("REPORT", args.output, "STATUS", output["status"])
    if output["status"] != "ESEGUITO":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
