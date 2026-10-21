#!/usr/bin/env python3
"""Read-only comparison of native Ollama and OpenAI-compatible JSON transports.

References: https://docs.ollama.com/api/chat
            https://docs.ollama.com/openai
No changes to models, packages, Chroma, or production.
"""
from __future__ import annotations
import argparse
import json
import time
import urllib.request
from pathlib import Path

SCHEMA = {"type": "object", "properties": {
    "label": {"type": "string", "enum": ["supported", "contradicted", "insufficient"]},
    "reason": {"type": "string"}},
    "required": ["label", "reason"], "additionalProperties": False}
PROMPT = "Fonte: se vi è spazio alle spalle della difesa si può cercare profondità. Affermazione: lo spazio alle spalle favorisce la profondità. Classifica."
def request(url, body, timeout):
    started = time.monotonic()
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
        return {"response": data, "elapsed_seconds": round(time.monotonic()-started, 2)}
    except Exception as exc:
        return {"error": type(exc).__name__ + ": " + str(exc),
                "elapsed_seconds": round(time.monotonic()-started, 2)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--url", default="http://127.0.0.1:11434")
    p.add_argument("--timeout", type=int, default=180)
    args = p.parse_args()
    body = {"model": args.model, "stream": False, "think": False,
            "format": SCHEMA, "options": {"temperature": 0, "num_predict": 256},
            "messages": [{"role": "system", "content": "Rispondi esclusivamente in JSON."},
                         {"role": "user", "content": PROMPT}]}
    raw = request(args.url.rstrip("/") + "/api/chat", body, args.timeout)
    result = {"model": args.model, "transport": "native /api/chat",
              "options": {"think": False, "num_predict": 256},
              "documentation": ["https://docs.ollama.com/api/chat", "https://docs.ollama.com/openai"],
              "elapsed_seconds": raw["elapsed_seconds"]}
    if "error" in raw:
        result["error"] = raw["error"]
    else:
        r = raw["response"]
        msg = r.get("message", {})
        result.update({"done_reason": r.get("done_reason"), "content": msg.get("content"),
                       "thinking_length": len(msg.get("thinking") or ""),
                       "eval_count": r.get("eval_count")})
        try:
            result["parsed"] = json.loads(msg.get("content") or "")
        except ValueError as exc:
            result["parse_error"] = str(exc)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
