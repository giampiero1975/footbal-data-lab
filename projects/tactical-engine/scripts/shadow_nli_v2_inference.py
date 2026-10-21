#!/usr/bin/env python3
"""Opt-in NLI V2 shadow inference over a prepared offline report.

Never changes the source report, answer, retrieval or Chroma. Output is exclusive.
Uses the exact V2 prompt and the V1 Ollama payload/schema contract.
Docs: https://docs.ollama.com/api/chat
      https://docs.ollama.com/capabilities/structured-outputs
"""
from __future__ import annotations
import argparse
import copy
import json
import time
import urllib.request
from pathlib import Path

from benchmark_direct_three_label_nli_v2 import benchmark
from shadow_nli_v2_offline import LABELS, apply_verdicts

SCHEMA = benchmark.Verdict.model_json_schema()


def judge_pair(claim, evidence, *, model="qwen3.5:9b",
               ollama_url="http://127.0.0.1:11434", timeout=180, max_tokens=1024):
    prompt = benchmark.INSTRUCTION + "\n\nFONTE:\n" + evidence + "\n\nAFFERMAZIONE:\n" + claim
    payload = {
        "model": model, "stream": False, "think": False, "format": SCHEMA,
        "options": {"temperature": 0, "num_predict": max_tokens, "num_ctx": 4096},
        "messages": [
            {"role": "system", "content": "Rispondi esclusivamente con JSON conforme allo schema richiesto. Non aggiungere testo esterno."},
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        ollama_url.rstrip("/") + "/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    message = result.get("message") or {}
    content = message.get("content") or ""
    if result.get("done_reason") != "stop" or not content:
        raise RuntimeError("Ollama output incomplete")
    label = benchmark.Verdict.model_validate_json(content).label
    return label


def evaluate(prepared, judge, *, max_pairs=0):
    """Pure orchestration; injected judge permits tests without model calls."""
    if prepared.get("schema") != "dribbling_nli_shadow_offline_v1":
        raise ValueError("Unexpected input schema")
    if max_pairs < 0:
        raise ValueError("max_pairs must be >= 0")
    verdicts, errors = [], []
    for item in prepared["claims"]:
        if item["status"] not in {"pending_nli", "invalid_citation"}:
            continue
        for pair in item["pairs"]:
            if max_pairs and len(verdicts) + len(errors) >= max_pairs:
                break
            key = {"question_id": item["question_id"], "claim_id": item["claim_id"],
                   "source_id": pair["source_id"],
                   "source_text_hash": pair["source_text_hash"]}
            started = time.monotonic()
            try:
                label = judge(pair["claim"], pair["evidence"])
                if label not in LABELS:
                    raise ValueError("Invalid NLI label")
                verdicts.append({**key, "nli_label": label,
                                 "elapsed_seconds": round(time.monotonic() - started, 3)})
            except Exception as exc:
                errors.append({**key, "error": type(exc).__name__ + ": " + str(exc)[:300]})
        if max_pairs and len(verdicts) + len(errors) >= max_pairs:
            break
    result = apply_verdicts(prepared, {"verdicts": verdicts})
    result["mode"] = "shadow_nli_v2_inference"
    result["inference"] = {"attempted": len(verdicts) + len(errors),
                           "completed": len(verdicts), "errors": errors,
                           "model_contract": "qwen3.5:9b / V2 instruction / structured JSON / think false"}
    result["limitations"] = [
        "Claims are manually annotated; automatic claim extraction not validated",
        "Only cited individual excerpts are judged; no global factuality guarantee",
        "No modification to source answer or production pipeline",
    ]
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prepared", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument("--max-tokens", type=int, default=1024)
    p.add_argument("--max-pairs", type=int, default=0)
    p.add_argument("--execute", action="store_true",
                   help="Explicit opt-in required to contact Ollama")
    args = p.parse_args()
    if not args.execute:
        p.error("Inference disabled by default: specify --execute explicitly")
    if args.output.resolve() == args.prepared.resolve():
        p.error("Output must not overwrite prepared input")
    if args.timeout < 1 or args.max_tokens < 1 or args.max_pairs < 0:
        p.error("Invalid limits")
    prepared = json.loads(args.prepared.read_text(encoding="utf-8"))
    def call(claim, evidence):
        return judge_pair(claim, evidence, model=args.model,
                          ollama_url=args.ollama_url, timeout=args.timeout,
                          max_tokens=args.max_tokens)
    result = evaluate(prepared, call, max_pairs=args.max_pairs)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print("NLI SHADOW:", result["inference"]["completed"], "completed;",
          len(result["inference"]["errors"]), "errors; report:", args.output)


if __name__ == "__main__":
    main()
