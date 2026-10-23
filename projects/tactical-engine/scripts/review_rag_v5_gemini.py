#!/usr/bin/env python3
"""Read-only, blind, source-grounded Gemini review of a V5 benchmark item."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import random
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evaluation/rag_v5_independent_candidate_v2.json"
EXPECTED = "f0d36bc5b35ddcfd42bfef234db2380db6a684a9b81fb9cd19ab75bea81755c0"
ALLOWED = {"gemini-3-flash-preview": (5, 20), "gemini-3.1-flash-lite-preview": (15, 500)}
PROMPT = """Sei un revisore esterno del benchmark tattico calcistico. NON rispondere alla domanda.
Valuta esclusivamente se domanda, mandatory_claims e forbidden_claims siano
sostenuti dai brani originali allegati. Non assumere corrette le note del creatore.
Ogni rilievo deve citare source_file_id, pagina e citazione testuale breve presente
negli estratti. Se evidenza insufficiente: NEEDS_SOURCE, non PASS.
Non inventare pagine o passaggi. Distingui fatto e inferenza, non fare tuning.
Restituisci SOLO JSON: {{"id":"...","decision":"PASS|REVISIONE|NEEDS_SOURCE",
"checks":[{{"claim_type":"mandatory|forbidden|question","claim":"...",
"supported":true,"evidence":[{{"source_file_id":"...","page":"...",
"quote":"..."}}],"reason":"..."}}],"issues":[],"limitations":[]}}.
"""
def atomic_write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit("REFUSING_OVERWRITE: " + str(path))
    tmp = path.with_name(path.name + ".tmp." + str(os.getpid()))
    try:
        tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.rename(path)
    finally:
        if tmp.exists():
            tmp.unlink()

def validate_bundle(bundle, row):
    if bundle.get("question_id") != row["id"]:
        raise SystemExit("SOURCE_BUNDLE_QUESTION_MISMATCH")
    required = row["source_file_id"]
    required = set(required if isinstance(required, list) else [required])
    docs = bundle.get("documents", [])
    if not isinstance(docs, list) or not docs:
        raise SystemExit("SOURCE_BUNDLE_EMPTY")
    got = set()
    for doc in docs:
        if not isinstance(doc, dict) or not all(doc.get(k) for k in ("source_file_id", "source_title", "page", "text", "origin_url")):
            raise SystemExit("SOURCE_BUNDLE_MISSING_PROVENANCE")
        if not isinstance(doc["text"], str) or len(doc["text"].strip()) < 40:
            raise SystemExit("SOURCE_BUNDLE_TEXT_TOO_SHORT")
        got.add(doc["source_file_id"])
    if not required.issubset(got):
        raise SystemExit("SOURCE_BUNDLE_MISSING_REQUIRED_FILES: " + str(sorted(required-got)))
    return docs

def validate_review(result, row, docs):
    if not isinstance(result, dict) or result.get("id") != row["id"]:
        raise ValueError("wrong review id")
    if result.get("decision") not in ("PASS", "REVISIONE", "NEEDS_SOURCE"):
        raise ValueError("invalid decision")
    checks = result.get("checks")
    if not isinstance(checks, list):
        raise ValueError("missing checks")
    for check in checks:
        if not isinstance(check, dict) or not isinstance(check.get("supported"), bool):
            raise ValueError("invalid check")
        for ev in check.get("evidence", []):
            matches = [d for d in docs if str(d["source_file_id"]) == str(ev.get("source_file_id")) and str(d["page"]) == str(ev.get("page"))]
            quote = ev.get("quote", "")
            if not isinstance(quote, str) or not quote.strip() or not any(quote.strip() in d["text"] for d in matches):
                raise ValueError("UNVERIFIABLE_QUOTE: page=" + str(ev.get("page")) + " claim=" + str(check.get("claim", ""))[:100] + " quote=" + str(quote)[:120])
    claims = row["mandatory_claims"] + row["forbidden_claims"]
    covered = {c.get("claim") for c in checks}
    if not all(c in covered for c in claims):
        raise ValueError("INCOMPLETE_CLAIM_COVERAGE")
    if result["decision"] == "PASS" and (any(c.get("supported") is not True for c in checks) or not all(c.get("evidence") for c in checks)):
        raise ValueError("UNSUPPORTED_PASS")
    return result

def load_local_env(path):
    """Load only GEMINI_API_KEY from a local untracked env file."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if not line.startswith("GEMINI_API_KEY="):
            continue
        value = line.split("=", 1)[1].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if value:
            os.environ.setdefault("GEMINI_API_KEY", value)
        return

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question-id", default="fresh_01")
    ap.add_argument("--source-bundle", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--model", choices=sorted(ALLOWED), default="gemini-3-flash-preview")
    ap.add_argument("--max-daily-requests", type=int, default=1)
    ap.add_argument("--confirm-free-tier", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.question_id != "fresh_01":
        raise SystemExit("INITIAL_GATE_ONLY_FRESH_01")
    data = MANIFEST.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED:
        raise SystemExit("MANIFEST_SHA256_MISMATCH: " + digest)
    manifest = json.loads(data)
    row = next((r for r in manifest["questions"] if r["id"] == args.question_id), None)
    if row is None:
        raise SystemExit("UNKNOWN_QUESTION")
    raw_bundle = args.source_bundle.read_bytes()
    bundle = json.loads(raw_bundle)
    docs = validate_bundle(bundle, row)
    if args.output.exists():
        raise SystemExit("REFUSING_OVERWRITE")
    if args.max_daily_requests < 1:
        raise SystemExit("INVALID_DAILY_LIMIT")
    rpm, rpd = ALLOWED[args.model]
    if args.max_daily_requests > rpd:
        raise SystemExit("DAILY_LIMIT_EXCEEDS_MODEL_FREE_TIER")
    request_data = {"system_instruction": {"parts": [{"text": PROMPT}]},
      "contents": [{"role": "user", "parts": [{"text": json.dumps({
        "question": {k: row[k] for k in ("id", "question", "mandatory_claims", "forbidden_claims", "abstention", "source_file_id", "source_page")},
        "original_sources": docs
      }, ensure_ascii=False)}]}],
      "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}}
    meta = {"question_id": args.question_id, "model": args.model, "manifest_sha256": digest,
      "source_bundle_sha256": hashlib.sha256(raw_bundle).hexdigest(),
      "source_ids": sorted({d["source_file_id"] for d in docs}),
      "blind": True, "ollama_outputs_sent": False}
    if args.dry_run:
        print(json.dumps({"preflight": "PASS", **meta}, ensure_ascii=False, indent=2))
        return
    if not args.confirm_free_tier:
        raise SystemExit("FREE_TIER_CONFIRMATION_REQUIRED")
    load_local_env(ROOT / ".env")
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        raise SystemExit("GEMINI_API_KEY_MISSING")
    # Local persistent budget; refuse on errors rather than retrying blindly.
    ledger = ROOT / "evaluation/.gemini_review_request_ledger.json"
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    used = {}
    if ledger.exists():
        used = json.loads(ledger.read_text(encoding="utf-8"))
    count = int(used.get(today, 0))
    if count >= args.max_daily_requests:
        raise SystemExit("LOCAL_DAILY_BUDGET_EXHAUSTED")
    used[today] = count + 1
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(json.dumps(used, indent=2), encoding="utf-8")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + args.model + ":generateContent"
    req = urllib.request.Request(endpoint, data=json.dumps(request_data).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read())
        txt = "".join(p.get("text", "") for p in payload["candidates"][0]["content"]["parts"])
        parsed = json.loads(txt)
        meta["raw_review"] = parsed
        meta["raw_response_sha256"] = hashlib.sha256(txt.encode("utf-8")).hexdigest()
        meta["usage_metadata"] = payload.get("usageMetadata", {})
        review = validate_review(parsed, row, docs)
        meta.update({"status": "ESEGUITO", "review": review})
    except (urllib.error.HTTPError, urllib.error.URLError, KeyError, ValueError, json.JSONDecodeError) as exc:
        # No automatic retry: prevent extra billed/limited requests and preserve diagnostic.
        meta.update({"status": "BLOCCATO", "error_type": type(exc).__name__,
                     "http_status": getattr(exc, "code", None),
                     "reason": str(exc)[:250].replace(key, "[REDACTED]")})
    atomic_write(args.output, meta)
    print("REPORT", args.output, "STATUS", meta["status"])
    if meta["status"] != "ESEGUITO":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
