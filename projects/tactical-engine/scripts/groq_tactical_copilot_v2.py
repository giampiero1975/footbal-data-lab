#!/usr/bin/env python3
"""Offline-first two-pass Groq tactical copilot contract.

Phase A deliberately contains no network execution path. It prepares and
validates the two requests while leaving the certified RAG and Gemini intact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from groq_free_reviewer_v1 import DEFAULT_MODEL, atomic_new, prepare_cases

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
    "type": "object", "additionalProperties": False, "required": ["checks", "limitations"],
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
    return parsed


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
    args = parser.parse_args()
    preflight(args.reports, args.output, args.model)
    print("OFFLINE_PREFLIGHT_PASS API_REQUESTS=0")


if __name__ == "__main__":
    main()
