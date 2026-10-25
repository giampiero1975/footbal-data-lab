#!/usr/bin/env python3
"""Complete only missing Coverciano-100 categories with Groq Free.

Offline by default. Network generation requires both --execute and an explicit
Free Tier confirmation. Existing chunks are read-only and never overwritten.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import urllib.error
import urllib.request

from groq_free_reviewer_v1 import quota_allowed

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gemini_chunks", ROOT / "scripts/generate_coverciano_100_chunked_gemini_v1.py")
CHUNKS = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(CHUNKS)
BASE = CHUNKS.BASE
ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-120b"
LIMITS = {"requests_per_day": 1000, "tokens_per_day": 200000, "tokens_per_minute": 8000}


def read_chunks(directory: Path) -> dict[str, dict]:
    result = {}
    for category in BASE.CATEGORIES:
        path = directory / f"coverciano_{category}_v1.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        start = BASE.CATEGORIES.index(category) * 10 + 1
        CHUNKS.validate_part(data.get("questions"), category, start, 10)
        result[category] = data
    return result


def inventory(directory: Path) -> dict:
    complete = read_chunks(directory)
    return {"complete_categories": list(complete),
            "missing_categories": [c for c in BASE.CATEGORIES if c not in complete],
            "question_count": sum(len(v["questions"]) for v in complete.values())}


def normalized(text: str) -> set[str]:
    return set(re.sub(r"[^a-z0-9à-ÿ]+", " ", text.casefold()).split())


def similarity(left: str, right: str) -> float:
    a, b = normalized(left), normalized(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def validate_no_duplicates(rows: list[dict], existing: list[dict], threshold: float = .82) -> None:
    prior = [(r["id"], r["question"]) for r in existing]
    for row in rows:
        for other_id, other_text in prior:
            if similarity(row["question"], other_text) >= threshold:
                raise ValueError(f"NEAR_DUPLICATE:{row['id']}:{other_id}")
        prior.append((row["id"], row["question"]))


def question_schema(category: str) -> dict:
    return {"type": "object", "additionalProperties": False,
        "required": ["id", "category", "difficulty", "question", "hidden_rubric"],
        "properties": {"id": {"type": "string"}, "category": {"type": "string", "enum": [category]},
            "difficulty": {"type": "integer", "minimum": 3, "maximum": 5}, "question": {"type": "string"},
            "hidden_rubric": {"type": "object", "additionalProperties": False,
                "required": ["constraints", "expected_points", "critical_errors"],
                "properties": {name: {"type": "array", "items": {"type": "string"}}
                               for name in ("constraints", "expected_points", "critical_errors")}}}}


def build_request(category: str, part: int, existing: list[dict], model: str = DEFAULT_MODEL) -> dict:
    index = BASE.CATEGORIES.index(category); start = index * 10 + 1 + (part - 1) * 5
    prior = [{"id": r["id"], "question_prefix": " ".join(r["question"].split())[:160],
              "question_sha256": hashlib.sha256(r["question"].encode()).hexdigest()} for r in existing]
    prompt = f"""Sei una commissione UEFA Pro. Genera esattamente 5 domande originali
da esame Coverciano esclusivamente sulla categoria {category}. Mantieni lo stesso
livello e contratto delle domande gia congelate: scenari realistici con moduli,
fase, tempo/punteggio, vincoli, compiti e geometrie concrete. Gli ID devono essere
da coverciano_{start:03d} a coverciano_{start+4:03d}. Non duplicare o parafrasare
le domande esistenti incluse nell'input. La rubrica e nascosta al RAG."""
    body = {"base_prompt": BASE.BASE_PROMPT, "existing_questions_read_only": prior}
    schema = {"type": "object", "additionalProperties": False, "required": ["questions"],
              "properties": {"questions": {"type": "array", "minItems": 5, "maxItems": 5,
                                             "items": question_schema(category)}}}
    return {"model": model, "temperature": .5, "n": 1, "stream": False,
            "messages": [{"role": "system", "content": prompt},
                         {"role": "user", "content": json.dumps(body, ensure_ascii=False)}],
            "response_format": {"type": "json_schema", "json_schema": {
                "name": "coverciano_missing_questions", "strict": True, "schema": schema}}}


def parse_response(payload: dict, category: str, part: int, existing: list[dict]) -> list[dict]:
    rows = json.loads(payload["choices"][0]["message"]["content"])["questions"]
    start = BASE.CATEGORIES.index(category) * 10 + 1 + (part - 1) * 5
    CHUNKS.validate_part(rows, category, start, 5)
    validate_no_duplicates(rows, existing)
    return rows


def write_new(path: Path, payload: dict) -> None:
    CHUNKS.write_new(path, payload)


def generate(args) -> None:
    chunks = read_chunks(args.input_dir)
    if args.category in chunks:
        raise SystemExit("CATEGORY_ALREADY_COMPLETE")
    existing = [q for data in chunks.values() for q in data["questions"]]
    request = build_request(args.category, args.part, existing, args.model)
    if not args.execute:
        write_new(args.output, {"schema": "coverciano_groq_generation_preflight_v1", "status": "VALIDATO",
            "category": args.category, "part": args.part, "model": args.model,
            "existing_question_count": len(existing), "network_called": False,
            "payload_sha256": hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()})
        print("OFFLINE_PREFLIGHT_PASS API_REQUESTS=0"); return
    if not args.confirm_free_tier:
        raise SystemExit("FREE_TIER_CONFIRMATION_REQUIRED")
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        raise SystemExit("GROQ_API_KEY_MISSING")
    day = dt.datetime.now(dt.timezone.utc).date().isoformat()
    ledger_path = ROOT / "evaluation/.groq_coverciano_generation_ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.exists() else {}
    if not quota_allowed(ledger, day, args.estimated_tokens, LIMITS):
        raise SystemExit("LOCAL_FREE_TIER_BUDGET_EXHAUSTED")
    req = urllib.request.Request(ENDPOINT, data=json.dumps(request).encode(), method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "football-data-lab-coverciano-generator/1.0"})
    started = dt.datetime.now(dt.timezone.utc)
    try:
        with urllib.request.urlopen(req, timeout=240) as response:
            raw = json.loads(response.read()); status = response.status
        rows = parse_response(raw, args.category, args.part, existing)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:1000].replace(key, "[REDACTED]")
        raise SystemExit(f"GROQ_HTTP_{exc.code}:{detail}")
    used = int(raw.get("usage", {}).get("total_tokens", args.estimated_tokens))
    ledger[day] = {"requests": int(ledger.get(day, {}).get("requests", 0)) + 1,
                   "tokens": int(ledger.get(day, {}).get("tokens", 0)) + used}
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    write_new(args.output, {"schema": "coverciano_groq_question_part_v1", "status": "ESEGUITO",
        "provider": "groq", "model": args.model, "category": args.category, "part": args.part,
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "http_status": status,
        "elapsed_seconds": (dt.datetime.now(dt.timezone.utc) - started).total_seconds(),
        "usage": raw.get("usage", {}), "questions": rows})


def merge_category(args) -> None:
    rows = []; models = set()
    for part in (1, 2):
        path = args.input_dir / f"coverciano_{args.category}_groq_part{part}_v1.json"
        data = json.loads(path.read_text(encoding="utf-8")); rows.extend(data["questions"]); models.add(data["model"])
    start = BASE.CATEGORIES.index(args.category) * 10 + 1
    CHUNKS.validate_part(rows, args.category, start, 10)
    existing = [q for c, data in read_chunks(args.input_dir).items() if c != args.category for q in data["questions"]]
    validate_no_duplicates(rows, existing)
    write_new(args.output, {"schema": "coverciano_question_chunk_v2", "status": "ESEGUITO",
        "provider": "groq", "models": sorted(models), "category": args.category,
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "questions": rows})


def merge_manifest(args) -> None:
    chunks = read_chunks(args.input_dir)
    if len(chunks) != len(BASE.CATEGORIES):
        raise SystemExit("INCOMPLETE_CATEGORIES")
    rows = [q for category in BASE.CATEGORIES for q in chunks[category]["questions"]]
    BASE.validate(rows); validate_no_duplicates(rows, [])
    providers = {c: chunks[c].get("provider", "gemini") for c in BASE.CATEGORIES}
    write_new(args.output, {"schema": "coverciano_question_manifest_v2", "status": "ESEGUITO",
        "question_count": 100, "category_providers": providers,
        "questions_sha256": hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        "questions": rows})


def main() -> None:
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="action", required=True)
    inv = sub.add_parser("inventory"); inv.add_argument("--input-dir", type=Path, required=True)
    gen = sub.add_parser("generate"); gen.add_argument("--category", choices=BASE.CATEGORIES, required=True)
    gen.add_argument("--part", type=int, choices=(1, 2), required=True); gen.add_argument("--input-dir", type=Path, required=True)
    gen.add_argument("--output", type=Path, required=True); gen.add_argument("--model", default=DEFAULT_MODEL)
    gen.add_argument("--estimated-tokens", type=int, default=7500)
    gen.add_argument("--execute", action="store_true"); gen.add_argument("--confirm-free-tier", action="store_true")
    cat = sub.add_parser("merge-category"); cat.add_argument("--category", choices=BASE.CATEGORIES, required=True)
    cat.add_argument("--input-dir", type=Path, required=True); cat.add_argument("--output", type=Path, required=True)
    mer = sub.add_parser("merge-manifest"); mer.add_argument("--input-dir", type=Path, required=True); mer.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.action == "inventory": print(json.dumps(inventory(args.input_dir), ensure_ascii=False, indent=2))
    elif args.action == "generate": generate(args)
    elif args.action == "merge-category": merge_category(args)
    else: merge_manifest(args)


if __name__ == "__main__": main()
