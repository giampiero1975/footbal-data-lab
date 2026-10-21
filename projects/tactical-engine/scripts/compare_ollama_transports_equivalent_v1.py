#!/usr/bin/env python3
"""Compare equivalent native and OpenAI-compatible Ollama requests, read-only.

Official docs:
  https://docs.ollama.com/api/chat
  https://docs.ollama.com/openai
  https://docs.ollama.com/capabilities/thinking

Uses the same model, messages, JSON schema, temperature, token budget and
think=false. Only the transport-specific request syntax differs.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

SCHEMA = {
    "type": "object",
    "properties": {
        "label": {"type": "string", "enum": ["supported", "contradicted", "insufficient"]},
        "reason": {"type": "string"},
    },
    "required": ["label", "reason"],
    "additionalProperties": False,
}
MESSAGES = [
    {"role": "system", "content": "Classifica l'affermazione rispetto alla fonte. Rispondi solo in JSON."},
    {"role": "user", "content": (
        "Fonte: se vi è spazio alle spalle della difesa si può cercare profondità. "
        "Affermazione: lo spazio alle spalle favorisce la profondità. Classifica."
    )},
]

def call(url, body, timeout):
    start = time.monotonic()
    try:
        request = urllib.request.Request(
            url, data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.load(response)
        return data, None, round(time.monotonic() - start, 2)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return None, f"{type(exc).__name__}: {str(exc)[:500]}", round(time.monotonic() - start, 2)

def summarize(transport, data, error, elapsed):
    result = {"transport": transport, "elapsed_seconds": elapsed}
    if error:
        result["error"] = error
        return result
    if transport == "native":
        message = data.get("message") or {}
        content = message.get("content") or ""
        result.update({
            "finish_reason": data.get("done_reason"),
            "content": content[:2000],
            "thinking_length": len(message.get("thinking") or ""),
            "thinking_excerpt": (message.get("thinking") or "")[:160],
            "completion_tokens": data.get("eval_count"),
        })
    else:
        choices = data.get("choices") or []
        choice = choices[0] if choices else {}
        message = choice.get("message") or {}
        content = message.get("content") or ""
        usage = data.get("usage") or {}
        result.update({
            "finish_reason": choice.get("finish_reason"),
            "content": content[:2000],
            "thinking_length": len(message.get("reasoning") or message.get("reasoning_content") or ""),
            "thinking_excerpt": (message.get("reasoning") or message.get("reasoning_content") or "")[:160],
            "completion_tokens": usage.get("completion_tokens"),
            "completion_tokens_details": usage.get("completion_tokens_details"),
            "message_keys": sorted(message.keys()),
        })
    try:
        result["parsed"] = json.loads(content)
    except ValueError as exc:
        result["parse_error"] = str(exc)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    base = args.ollama_url.rstrip("/")
    native = {
        "model": args.model, "messages": MESSAGES, "stream": False,
        "think": False, "format": SCHEMA,
        "options": {"temperature": 0, "num_predict": args.max_tokens},
    }
    compatible = {
        "model": args.model, "messages": MESSAGES, "stream": False,
        "think": False, "temperature": 0, "max_tokens": args.max_tokens,
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "fidelity_judgement", "strict": True, "schema": SCHEMA,
        }},
    }
    report = {
        "purpose": "Equivalent-input transport comparison; no Ragas calls",
        "model": args.model, "max_tokens": args.max_tokens, "temperature": 0,
        "think_requested": False,
        "limitations": [
            "OpenAI-compatible support for think is implementation-specific.",
            "Matching logical parameters does not guarantee identical tokenization or server behavior.",
            "One case cannot establish general reliability.",
        ],
        "results": [],
    }
    for name, endpoint, payload in (
        ("native", "/api/chat", native),
        ("openai_compatible", "/v1/chat/completions", compatible),
    ):
        data, error, elapsed = call(base + endpoint, payload, args.timeout)
        result = summarize(name, data, error, elapsed)
        report["results"].append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("REPORT", args.output, flush=True)

if __name__ == "__main__":
    main()
