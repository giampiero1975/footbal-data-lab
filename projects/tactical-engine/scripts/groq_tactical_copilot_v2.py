#!/usr/bin/env python3
"""Opt-in two-pass Groq tactical copilot with fail-closed final composition."""
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

from groq_free_reviewer_v1 import (DEFAULT_MODEL, ENDPOINT, atomic_new,
                                   prepare_cases, quota_allowed)

ROOT = Path(__file__).resolve().parents[1]

PASS1_PROMPT = """Sei una spalla tattica indipendente per un allenatore UEFA Pro.
Analizza soltanto domanda e risposta, senza presumere fonti. Distingui sempre:
errori certi, possibili lacune e suggerimenti opzionali. Verifica pertinenza,
correttezza di ruoli/movimenti/tempi/spazi, completezza e azioni concrete di
miglioramento. Non inventare fonti, pagine o attribuzioni. Assegna a ogni
osservazione un finding_id univoco e indica se richiede verifica documentale."""

PASS2_PROMPT = """Sei il verificatore documentale della revisione tattica.
Ricevi osservazioni gia formulate ed estratti selezionati. Per ogni finding_id
classifica esclusivamente: SUPPORTATO, ULTERIORE_RETRIEVAL o NON_SUPPORTATO.
Usa soltanto evidence_labels realmente disponibili. Non controllare la sintassi
delle citazioni della risposta: quella responsabilita appartiene al software.
Non inventare fonti, pagine, citazioni o contenuti assenti dagli estratti."""

PASS2_PROMPT += """ Dopo i controlli, riscrivi una risposta finale concreta e
completa per ogni caso. Applica soltanto finding classificati SUPPORTATO; lascia
gli altri in unresolved_findings. Ogni affermazione documentale deve citare una
evidence label disponibile nel formato [F1]. Non aggiungere bibliografie o
fonti esterne e non dichiarare verificato cio che richiede ulteriore retrieval."""

FINDING = {
    "type": "object", "additionalProperties": False,
    "required": ["finding_id", "kind", "claim", "why", "priority", "needs_document_check"],
    "properties": {
        "finding_id": {"type": "string"},
        "kind": {"type": "string", "enum": ["ERRORE_CERTO", "POSSIBILE_LACUNA", "SUGGERIMENTO_OPZIONALE"]},
        "claim": {"type": "string"}, "why": {"type": "string"},
        "priority": {"type": "integer", "minimum": 1, "maximum": 3},
        "needs_document_check": {"type": "boolean"},
    },
}

PASS1_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["reviews", "limitations"],
    "properties": {
        "reviews": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "score", "verdict", "answered_parts", "missing_parts", "digressions",
                         "confirmed_points", "findings", "improvement_plan", "retrieval_needs"],
            "properties": {
                "id": {"type": "string"}, "score": {"type": "number", "minimum": 0, "maximum": 10},
                "verdict": {"type": "string", "enum": ["PASS", "REVISIONE"]},
                "answered_parts": {"type": "array", "items": {"type": "string"}},
                "missing_parts": {"type": "array", "items": {"type": "string"}},
                "digressions": {"type": "array", "items": {"type": "string"}},
                "confirmed_points": {"type": "array", "items": {"type": "string"}},
                "findings": {"type": "array", "items": FINDING},
                "improvement_plan": {"type": "array", "items": {"type": "string"}},
                "retrieval_needs": {"type": "array", "items": {"type": "string"}},
            }}},
        "limitations": {"type": "array", "items": {"type": "string"}},
    },
}

PASS2_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["checks", "revised_answers", "limitations"],
    "properties": {
        "checks": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "finding_id", "classification", "evidence_labels", "rationale"],
            "properties": {
                "id": {"type": "string"}, "finding_id": {"type": "string"},
                "classification": {"type": "string", "enum": ["SUPPORTATO", "ULTERIORE_RETRIEVAL", "NON_SUPPORTATO"]},
                "evidence_labels": {"type": "array", "items": {"type": "string"}},
                "rationale": {"type": "string"},
            }}},
        "revised_answers": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "answer", "applied_findings", "unresolved_findings"],
            "properties": {
                "id": {"type": "string"}, "answer": {"type": "string"},
                "applied_findings": {"type": "array", "items": {"type": "string"}},
                "unresolved_findings": {"type": "array", "items": {"type": "string"}},
            }}},
        "limitations": {"type": "array", "items": {"type": "string"}},
    },
}


def strict_request(prompt: str, body: dict, schema: dict, name: str, model: str = DEFAULT_MODEL) -> dict:
    return {"model": model, "temperature": 0, "n": 1, "stream": False,
            "messages": [{"role": "system", "content": prompt},
                         {"role": "user", "content": json.dumps(body, ensure_ascii=False)}],
            "response_format": {"type": "json_schema", "json_schema": {
                "name": name, "strict": True, "schema": schema}}}


def prepare_inputs(paths: list[Path]) -> tuple[list[dict], dict[str, str]]:
    cases, mapping = prepare_cases(paths)
    return cases, mapping


def build_pass1(cases: list[dict], model: str = DEFAULT_MODEL) -> dict:
    minimal = [{"id": c["id"], "question": c["question"], "answer": c["answer"]} for c in cases]
    return strict_request(PASS1_PROMPT, {"cases": minimal}, PASS1_SCHEMA, "groq_tactical_copilot_pass1", model)


def validate_pass1(parsed: dict, case_ids: list[str]) -> dict:
    rows = parsed.get("reviews")
    if not isinstance(rows, list) or sorted(r.get("id") for r in rows) != sorted(case_ids):
        raise ValueError("PASS1_CASE_ID_MISMATCH")
    finding_ids: set[str] = set()
    for row in rows:
        score = row.get("score")
        if not isinstance(score, (int, float)) or not 0 <= float(score) <= 10:
            raise ValueError("PASS1_SCORE")
        if (float(score) >= 8) != (row.get("verdict") == "PASS"):
            raise ValueError("PASS1_VERDICT")
        for finding in row.get("findings", []):
            fid = finding.get("finding_id")
            if not fid or fid in finding_ids:
                raise ValueError("PASS1_FINDING_ID")
            finding_ids.add(fid)
    return parsed


def build_pass2(cases: list[dict], pass1: dict, model: str = DEFAULT_MODEL) -> dict:
    by_id = {row["id"]: row for row in pass1["reviews"]}
    body = {"cases": [{"id": c["id"], "findings": by_id[c["id"]]["findings"],
                        "evidence": c["evidence"]} for c in cases]}
    return strict_request(PASS2_PROMPT, body, PASS2_SCHEMA, "groq_tactical_copilot_pass2", model)


def validate_pass2(parsed: dict, cases: list[dict], pass1: dict) -> dict:
    expected = {(row["id"], f["finding_id"]) for row in pass1["reviews"] for f in row["findings"]}
    checks = parsed.get("checks")
    if not isinstance(checks, list) or {(r.get("id"), r.get("finding_id")) for r in checks} != expected:
        raise ValueError("PASS2_FINDING_COVERAGE")
    labels = {c["id"]: {str(e.get("label", "")) for e in c["evidence"]} for c in cases}
    for row in checks:
        used = set(row.get("evidence_labels", []))
        if not used <= labels[row["id"]]:
            raise ValueError("PASS2_UNKNOWN_EVIDENCE_LABEL")
        if row.get("classification") == "SUPPORTATO" and not used:
            raise ValueError("PASS2_SUPPORTED_WITHOUT_EVIDENCE")
        if row.get("classification") != "SUPPORTATO" and used:
            raise ValueError("PASS2_UNSUPPORTED_WITH_EVIDENCE")
    revised = parsed.get("revised_answers")
    case_ids = {c["id"] for c in cases}
    if not isinstance(revised, list) or {r.get("id") for r in revised} != case_ids:
        raise ValueError("PASS2_REVISED_CASE_COVERAGE")
    supported = {(r["id"], r["finding_id"]) for r in checks if r["classification"] == "SUPPORTATO"}
    expected_by_case = {case_id: {fid for cid, fid in expected if cid == case_id} for case_id in case_ids}
    for row in revised:
        case_id = row["id"]
        answer = row.get("answer", "")
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("PASS2_EMPTY_REVISED_ANSWER")
        applied = set(row.get("applied_findings", [])); unresolved = set(row.get("unresolved_findings", []))
        if applied & unresolved or applied | unresolved != expected_by_case[case_id]:
            raise ValueError("PASS2_FINDING_PARTITION")
        if any((case_id, fid) not in supported for fid in applied):
            raise ValueError("PASS2_APPLIED_UNSUPPORTED")
        cited = set(re.findall(r"\[(F\d+)\]", answer))
        if not cited <= labels[case_id]:
            raise ValueError("PASS2_REVISED_UNKNOWN_CITATION")
    return parsed


def call_groq(request: dict, key: str, timeout: int = 180) -> tuple[dict, float]:
    req = urllib.request.Request(ENDPOINT, data=json.dumps(request).encode(), method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "football-data-lab-groq-copilot/2.0"})
    started = dt.datetime.now(dt.timezone.utc)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = json.loads(response.read())
    return payload, (dt.datetime.now(dt.timezone.utc) - started).total_seconds()


def parsed_content(payload: dict) -> dict:
    return json.loads(payload["choices"][0]["message"]["content"])


def execute(paths: list[Path], output: Path, model: str, estimated_tokens: int) -> None:
    cases, mapping = prepare_inputs(paths)
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        raise SystemExit("GROQ_API_KEY_MISSING")
    day = dt.datetime.now(dt.timezone.utc).date().isoformat()
    ledger_path = ROOT / "evaluation/.groq_free_ledger.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    if not quota_allowed(ledger, day, estimated_tokens):
        raise SystemExit("LOCAL_DAILY_BUDGET_EXHAUSTED")
    req1 = build_pass1(cases, model); payload1, elapsed1 = call_groq(req1, key)
    pass1 = validate_pass1(parsed_content(payload1), list(mapping))
    req2 = build_pass2(cases, pass1, model); payload2, elapsed2 = call_groq(req2, key)
    pass2 = validate_pass2(parsed_content(payload2), cases, pass1)
    usage1 = payload1.get("usage", {}); usage2 = payload2.get("usage", {})
    used = int(usage1.get("total_tokens", 0)) + int(usage2.get("total_tokens", 0))
    ledger[day] = {"requests": int(ledger.get(day, {}).get("requests", 0)) + 2,
                   "tokens": int(ledger.get(day, {}).get("tokens", 0)) + used}
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    atomic_new(output, {"schema": "groq_tactical_copilot_runtime_v2", "status": "ESEGUITO",
        "provider": "groq", "model": model, "runtime_case_map": mapping,
        "network_called": True, "rag_executed": False, "index_writes": False,
        "elapsed_seconds": round(elapsed1 + elapsed2, 3),
        "passes": [{"elapsed_seconds": elapsed1, "usage": usage1},
                   {"elapsed_seconds": elapsed2, "usage": usage2}],
        "pass1": pass1, "pass2": pass2})


def preflight(paths: list[Path], output: Path, model: str) -> None:
    cases, mapping = prepare_inputs(paths)
    request1 = build_pass1(cases, model)
    synthetic_pass1 = {"reviews": [{"id": c["id"], "score": 0, "verdict": "REVISIONE",
        "answered_parts": [], "missing_parts": [], "digressions": [], "confirmed_points": [],
        "findings": [], "improvement_plan": [], "retrieval_needs": []} for c in cases], "limitations": []}
    validate_pass1(synthetic_pass1, list(mapping))
    request2 = build_pass2(cases, synthetic_pass1, model)
    atomic_new(output, {"schema": "groq_tactical_copilot_preflight_v2", "status": "VALIDATO",
        "model": model, "case_count": len(cases), "runtime_case_map": mapping,
        "pass1_payload_sha256": hashlib.sha256(json.dumps(request1, sort_keys=True).encode()).hexdigest(),
        "pass2_payload_sha256": hashlib.sha256(json.dumps(request2, sort_keys=True).encode()).hexdigest(),
        "network_called": False, "rag_executed": False, "index_writes": False,
        "result": "OFFLINE_PREFLIGHT_PASS"})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-free-tier", action="store_true")
    parser.add_argument("--estimated-tokens", type=int, default=7500)
    args = parser.parse_args()
    if not args.execute:
        preflight(args.reports, args.output, args.model)
        print("OFFLINE_PREFLIGHT_PASS API_REQUESTS=0")
        return
    if not args.confirm_free_tier:
        raise SystemExit("FREE_TIER_CONFIRMATION_REQUIRED")
    execute(args.reports, args.output, args.model, args.estimated_tokens)
    print("COPILOT_COMPLETE")


if __name__ == "__main__":
    main()
