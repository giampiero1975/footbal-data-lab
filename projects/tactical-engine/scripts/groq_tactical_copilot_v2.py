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

PASS1_PROMPT += """ Valuta come una commissione esigente: preserva sistema,
lato, ruolo, punteggio, minuto e vincoli della domanda. Non confondere terzino,
ala, esterno di centrocampo, mezzala e mediano. Ogni finding deve proporre una
correzione concreta, non ripetere l'errore della bozza. Per una situazione di
gara verifica sempre struttura in possesso, occupazione degli spazi, movimenti
sincroni, preventiva/transizione e uso esplicito dei cambi disponibili.
Oltre alla diagnosi scrivi replacement_answer: una nuova risposta completa da
esame, operativa e autosufficiente. Deve dire chi fa cosa, dove e quando;
rispondere a ogni vincolo numerico della domanda (cambi, slot, minuto, risultato);
definire struttura, catene/rotazioni, occupazione dell'area, preventiva e trigger.
Non limitarti a spiegare perche la bozza e sbagliata e non usare l'assenza di una
fonte come motivo per evitare una scelta logico-tattica esplicitamente qualificata.
Prima di scrivere costruisci mentalmente una mappa: NOSTRA squadra/AVVERSARIO,
lato destro/sinistro, ruolo iniziale e ruolo trasformato. Il lato destro
avversario fronteggia il nostro lato sinistro e viceversa. Non spostare dalla
zona decisiva il giocatore che sta gia vincendo il duello: usa compagni vicini,
rotazioni e corse nel mezzo spazio per rompere il raddoppio. Non inventare ruoli
assenti nel sistema dichiarato. Se sono indicati N cambi e M slot, nomina tutti
gli N cambi in ordine e raggruppali esattamente negli M slot, spiegando per
ciascuno uscita, entrata, nuova posizione e impatto strutturale."""

PASS2_PROMPT = """Sei il verificatore documentale della revisione tattica.
Ricevi osservazioni gia formulate ed estratti selezionati. Per ogni finding_id
classifica esclusivamente: SUPPORTATO, GIUDIZIO_TECNICO,
ULTERIORE_RETRIEVAL o NON_SUPPORTATO. Usa GIUDIZIO_TECNICO soltanto per una
correzione logico-tattica che nel finding dichiara needs_document_check=false;
non associarle evidence_labels.
Usa soltanto evidence_labels realmente disponibili. Non controllare la sintassi
delle citazioni della risposta: quella responsabilita appartiene al software.
Non inventare fonti, pagine, citazioni o contenuti assenti dagli estratti."""

PASS2_PROMPT += """ Dopo i controlli, usa replacement_answer come ossatura e
riscrivi una risposta finale concreta e completa per ogni caso: non produrre una
diagnosi della bozza. La risposta deve avere sezioni operative su obiettivo e
struttura, compiti e movimenti coordinati, utilizzo di tutti i cambi/slot o altri
vincoli espliciti, occupazione dell'area, preventiva/transizione e trigger
decisionali. Applica soltanto finding classificati SUPPORTATO o
GIUDIZIO_TECNICO; lascia gli altri in unresolved_findings. Preserva le parti
corrette della bozza, ma sostituisci integralmente quelle errate. Non presentare
i GIUDIZIO_TECNICO come fatti documentali. Ogni affermazione documentale deve citare una
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
                         "confirmed_points", "findings", "improvement_plan", "replacement_answer",
                         "retrieval_needs"],
            "properties": {
                "id": {"type": "string"}, "score": {"type": "number", "minimum": 0, "maximum": 10},
                "verdict": {"type": "string", "enum": ["PASS", "REVISIONE"]},
                "answered_parts": {"type": "array", "items": {"type": "string"}},
                "missing_parts": {"type": "array", "items": {"type": "string"}},
                "digressions": {"type": "array", "items": {"type": "string"}},
                "confirmed_points": {"type": "array", "items": {"type": "string"}},
                "findings": {"type": "array", "items": FINDING},
                "improvement_plan": {"type": "array", "items": {"type": "string"}},
                "replacement_answer": {"type": "string"},
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
                "classification": {"type": "string", "enum": ["SUPPORTATO", "GIUDIZIO_TECNICO", "ULTERIORE_RETRIEVAL", "NON_SUPPORTATO"]},
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
    # Keep the request aligned with Groq's documented strict-output example.
    # A small positive temperature also avoids the provider's compatibility
    # conversion from 0 to 1e-8, documented as a possible source of issues.
    return {"model": model, "temperature": 0.1,
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


def normalize_pass1(parsed: dict, case_ids: list[str]) -> tuple[dict, list[str]]:
    """Normalize only identifiers and score-derived verdicts, never tactical text."""
    normalized = json.loads(json.dumps(parsed))
    rows = normalized.get("reviews")
    if not isinstance(rows, list) or len(rows) != len(case_ids):
        raise ValueError("PASS1_CASE_COUNT_MISMATCH")
    notes: list[str] = []
    returned_ids = [row.get("id") if isinstance(row, dict) else None for row in rows]
    if sorted(returned_ids, key=str) != sorted(case_ids):
        for row, case_id in zip(rows, case_ids):
            if not isinstance(row, dict):
                raise ValueError("PASS1_REVIEW_TYPE")
            row["id"] = case_id
        notes.append("CASE_IDS_POSITIONALLY_NORMALIZED")
    used: set[str] = set()
    for row in rows:
        score = row.get("score")
        if not isinstance(score, (int, float)) or not 0 <= float(score) <= 10:
            raise ValueError("PASS1_SCORE")
        expected_verdict = "PASS" if float(score) >= 8 else "REVISIONE"
        if row.get("verdict") != expected_verdict:
            row["verdict"] = expected_verdict
            notes.append(f"{row['id']}:VERDICT_DERIVED_FROM_SCORE")
        findings = row.get("findings")
        if not isinstance(findings, list):
            raise ValueError("PASS1_FINDINGS_TYPE")
        for index, finding in enumerate(findings, 1):
            if not isinstance(finding, dict):
                raise ValueError("PASS1_FINDING_TYPE")
            fid = finding.get("finding_id")
            if not isinstance(fid, str) or not fid.strip() or fid in used:
                fid = f"{row['id']}_f{index:02d}"
                while fid in used:
                    index += 1; fid = f"{row['id']}_f{index:02d}"
                finding["finding_id"] = fid
                notes.append(f"{row['id']}:FINDING_ID_NORMALIZED")
            used.add(fid)
    return normalized, notes


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
        replacement = row.get("replacement_answer")
        if not isinstance(replacement, str) or len(replacement.strip()) < 400:
            raise ValueError("PASS1_REPLACEMENT_ANSWER")
        for finding in row.get("findings", []):
            fid = finding.get("finding_id")
            if not fid or fid in finding_ids:
                raise ValueError("PASS1_FINDING_ID")
            finding_ids.add(fid)
    return parsed


def build_pass2(cases: list[dict], pass1: dict, model: str = DEFAULT_MODEL) -> dict:
    by_id = {row["id"]: row for row in pass1["reviews"]}
    body = {"cases": [{"id": c["id"], "question": c["question"],
                        "original_answer": c["answer"],
                        "replacement_answer": by_id[c["id"]]["replacement_answer"],
                        "improvement_plan": by_id[c["id"]]["improvement_plan"],
                        "findings": by_id[c["id"]]["findings"],
                        "evidence": c["evidence"]} for c in cases]}
    # Schema names are immutable provider-side contract identifiers.  The v1
    # name was used by an experimental dynamic schema, so the restored static
    # contract receives a fresh versioned name.
    return strict_request(PASS2_PROMPT, body, PASS2_SCHEMA,
                          "groq_tactical_copilot_pass2_static_v2", model)


def normalize_pass2(parsed: dict, cases: list[dict], pass1: dict) -> tuple[dict, list[str]]:
    """Fail closed on omitted checks and mechanical finding partitions."""
    normalized = json.loads(json.dumps(parsed))
    expected_order = [(row["id"], f["finding_id"])
                      for row in pass1["reviews"] for f in row["findings"]]
    expected = set(expected_order)
    checks = normalized.get("checks")
    if not isinstance(checks, list):
        raise ValueError("PASS2_CHECKS_TYPE")
    notes: list[str] = []
    raw_keys = [(row.get("id"), row.get("finding_id"))
                for row in checks if isinstance(row, dict)]
    if len(raw_keys) != len(checks):
        raise ValueError("PASS2_CHECK_TYPE")
    if len(checks) == len(expected_order) and set(raw_keys) != expected:
        for row, (case_id, finding_id) in zip(checks, expected_order):
            row["id"] = case_id
            row["finding_id"] = finding_id
        notes.append("CHECK_IDS_POSITIONALLY_NORMALIZED")

    observed: set[tuple[str, str]] = set()
    for row in checks:
        if not isinstance(row, dict):
            raise ValueError("PASS2_CHECK_TYPE")
        key = (row.get("id"), row.get("finding_id"))
        if key not in expected or key in observed:
            raise ValueError("PASS2_UNKNOWN_OR_DUPLICATE_FINDING")
        observed.add(key)
    for case_id, finding_id in sorted(expected - observed):
        checks.append({"id": case_id, "finding_id": finding_id,
            "classification": "ULTERIORE_RETRIEVAL", "evidence_labels": [],
            "rationale": "Verifica non restituita dal copilot; mantenuta fuori dalla risposta finale."})
        notes.append(f"{case_id}:{finding_id}:MISSING_CHECK_FAIL_CLOSED")

    labels = {c["id"]: {str(e.get("label", "")) for e in c["evidence"]} for c in cases}
    for row in checks:
        classification = row.get("classification")
        used = set(row.get("evidence_labels", []))
        valid = used & labels[row["id"]]
        if classification != "SUPPORTATO" and used:
            row["evidence_labels"] = []
            notes.append(f"{row['id']}:{row['finding_id']}:UNSUPPORTED_LABELS_REMOVED")
        elif classification == "SUPPORTATO" and valid != used:
            row["evidence_labels"] = sorted(valid)
            notes.append(f"{row['id']}:{row['finding_id']}:UNKNOWN_LABELS_REMOVED")
            if not valid:
                row["classification"] = "ULTERIORE_RETRIEVAL"
                notes.append(f"{row['id']}:{row['finding_id']}:SUPPORT_DOWNGRADED_FAIL_CLOSED")

    revised = normalized.get("revised_answers")
    if not isinstance(revised, list):
        raise ValueError("PASS2_REVISED_TYPE")
    by_case = {row.get("id"): row for row in revised if isinstance(row, dict)}
    if len(by_case) != len(revised):
        raise ValueError("PASS2_REVISED_DUPLICATE_ID")
    needs_check = {(row["id"], finding["finding_id"]): finding.get("needs_document_check", True)
                   for row in pass1["reviews"] for finding in row["findings"]}
    for row in checks:
        key = (row["id"], row["finding_id"])
        if row.get("classification") == "GIUDIZIO_TECNICO" and needs_check.get(key, True):
            row["classification"] = "ULTERIORE_RETRIEVAL"
            row["evidence_labels"] = []
            notes.append(f"{row['id']}:{row['finding_id']}:EXPERT_JUDGMENT_DOWNGRADED")
    supported = {(r["id"], r["finding_id"]) for r in checks
                 if r.get("classification") in {"SUPPORTATO", "GIUDIZIO_TECNICO"}}
    for case in cases:
        case_id = case["id"]
        row = by_case.get(case_id)
        if row is None:
            raise ValueError("PASS2_REVISED_CASE_COVERAGE")
        expected_ids = {fid for cid, fid in expected if cid == case_id}
        applied = set(row.get("applied_findings", []))
        unresolved = set(row.get("unresolved_findings", []))
        unknown = (applied | unresolved) - expected_ids
        if unknown:
            applied &= expected_ids
            unresolved &= expected_ids
            notes.append(f"{case_id}:UNKNOWN_PARTITION_IDS_REMOVED")
        unsafe = {fid for fid in applied if (case_id, fid) not in supported}
        missing = expected_ids - applied - unresolved
        if unsafe or missing:
            row["applied_findings"] = sorted(applied - unsafe)
            row["unresolved_findings"] = sorted(unresolved | unsafe | missing)
            notes.append(f"{case_id}:FINDING_PARTITION_FAIL_CLOSED")
    return normalized, notes


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
    needs_check = {(row["id"], finding["finding_id"]): finding.get("needs_document_check", True)
                   for row in pass1["reviews"] for finding in row["findings"]}
    for row in checks:
        key = (row["id"], row["finding_id"])
        if row["classification"] == "GIUDIZIO_TECNICO" and needs_check.get(key, True):
            raise ValueError("PASS2_INVALID_EXPERT_JUDGMENT")
    supported = {(r["id"], r["finding_id"]) for r in checks
                 if r["classification"] in {"SUPPORTATO", "GIUDIZIO_TECNICO"}}
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


def _redacted_http_400_category(exc: urllib.error.HTTPError) -> str:
    """Classify a provider error without retaining its message or payload."""
    try:
        raw = exc.read(65536)
        payload = json.loads(raw.decode("utf-8", errors="replace"))
        error = payload.get("error", {}) if isinstance(payload, dict) else {}
        message = str(error.get("message", "")).lower()
        param = str(error.get("param", "")).lower()
    except (AttributeError, OSError, UnicodeError, json.JSONDecodeError):
        return "UNCLASSIFIED"
    text = f"{param} {message}"
    if any(word in text for word in ("response_format", "json_schema", "schema")):
        return "SCHEMA"
    if "temperature" in text:
        return "TEMPERATURE"
    if "model" in text:
        return "MODEL"
    if any(word in text for word in ("token", "context", "too large")):
        return "SIZE"
    if any(word in text for word in ("generated json", "does not match")):
        return "OUTPUT_MISMATCH"
    return "INVALID_REQUEST"


def redacted_failure_reason(exc: Exception) -> str:
    """Return a diagnostic code without response bodies, prompts or secrets."""
    if isinstance(exc, urllib.error.HTTPError):
        if exc.code == 400:
            return f"GROQ_HTTP_400_{_redacted_http_400_category(exc)}"
        return f"GROQ_HTTP_{exc.code}"
    if isinstance(exc, urllib.error.URLError):
        return "GROQ_NETWORK_ERROR"
    if isinstance(exc, TimeoutError):
        return "GROQ_TIMEOUT"
    if isinstance(exc, ValueError) and re.fullmatch(r"PASS[12]_[A-Z0-9_]+", str(exc)):
        return f"GROQ_{exc}"
    if isinstance(exc, (json.JSONDecodeError, KeyError, TypeError, ValueError)):
        return "GROQ_INVALID_STRUCTURED_RESPONSE"
    return "GROQ_UNEXPECTED_ERROR"


def write_failure(output: Path, model: str, reason: str) -> None:
    atomic_new(output, {"schema": "groq_tactical_copilot_runtime_v2",
        "status": "BLOCCATO", "provider": "groq", "model": model,
        "reason": reason, "network_called": True, "rag_executed": False,
        "index_writes": False, "contains_prompt_or_evidence": False})


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
    pass1, normalizations = normalize_pass1(parsed_content(payload1), list(mapping))
    pass1 = validate_pass1(pass1, list(mapping))
    req2 = build_pass2(cases, pass1, model); payload2, elapsed2 = call_groq(req2, key)
    pass2, pass2_normalizations = normalize_pass2(parsed_content(payload2), cases, pass1)
    pass2 = validate_pass2(pass2, cases, pass1)
    usage1 = payload1.get("usage", {}); usage2 = payload2.get("usage", {})
    used = int(usage1.get("total_tokens", 0)) + int(usage2.get("total_tokens", 0))
    ledger[day] = {"requests": int(ledger.get(day, {}).get("requests", 0)) + 2,
                   "tokens": int(ledger.get(day, {}).get("tokens", 0)) + used}
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    atomic_new(output, {"schema": "groq_tactical_copilot_runtime_v2", "status": "ESEGUITO",
        "provider": "groq", "model": model, "runtime_case_map": mapping,
        "network_called": True, "rag_executed": False, "index_writes": False,
        "elapsed_seconds": round(elapsed1 + elapsed2, 3),
        "mechanical_normalizations": normalizations + pass2_normalizations,
        "passes": [{"elapsed_seconds": elapsed1, "usage": usage1},
                   {"elapsed_seconds": elapsed2, "usage": usage2}],
        "pass1": pass1, "pass2": pass2})


def preflight(paths: list[Path], output: Path, model: str) -> None:
    cases, mapping = prepare_inputs(paths)
    request1 = build_pass1(cases, model)
    synthetic_pass1 = {"reviews": [{"id": c["id"], "score": 0, "verdict": "REVISIONE",
        "answered_parts": [], "missing_parts": [], "digressions": [], "confirmed_points": [],
        "findings": [], "improvement_plan": [],
        "replacement_answer": "Preflight placeholder operativo. " * 20,
        "retrieval_needs": []} for c in cases], "limitations": []}
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
    try:
        execute(args.reports, args.output, args.model, args.estimated_tokens)
    except Exception as exc:
        reason = redacted_failure_reason(exc)
        write_failure(args.output, args.model, reason)
        raise SystemExit(reason) from None
    print("COPILOT_COMPLETE")


if __name__ == "__main__":
    main()
