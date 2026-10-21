#!/usr/bin/env python3
"""Read-only diagnostics of Ollama's OpenAI-compatible structured response.

Official documentation: https://docs.ollama.com/openai
Tests the exact transport used by Ragas without invoking Ragas itself.
No package installation, no Chroma access, no production changes.
"""
from __future__ import annotations
import argparse
import asyncio
import json
import time
from pathlib import Path

async def run(args):
    from openai import AsyncOpenAI
    client = AsyncOpenAI(base_url=args.ollama_url.rstrip("/") + "/v1/",
                         api_key="ollama", timeout=args.timeout, max_retries=0)
    started = time.monotonic()
    report = {"model": args.model, "api": "/v1/chat/completions",
              "options": {"temperature": 0, "max_tokens": args.max_tokens},
              "source": "https://docs.ollama.com/openai"}
    try:
        result = await client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "system", "content": "Rispondi esclusivamente con un JSON contenente label e reason."},
                {"role": "user", "content": "Fonte: se vi è spazio alle spalle della difesa, è possibile cercare la profondità. Affermazione: lo spazio alle spalle favorisce la profondità. Classifica."}
            ],
            response_format={"type": "json_schema", "json_schema": {
                "name": "fidelity_judgement", "strict": True,
                "schema": {"type": "object", "properties": {
                    "label": {"type": "string", "enum": ["supported", "contradicted", "insufficient"]},
                    "reason": {"type": "string"}},
                    "required": ["label", "reason"], "additionalProperties": False}}},
            temperature=0,
            max_tokens=args.max_tokens)
        choice = result.choices[0]
        content = choice.message.content or ""
        report["finish_reason"] = choice.finish_reason
        report["content"] = content[:2000]
        report["usage"] = result.usage.model_dump() if result.usage else None
        try:
            report["parsed"] = json.loads(content)
        except json.JSONDecodeError as exc:
            report["parse_error"] = str(exc)
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)[:1500]
    report["elapsed_seconds"] = round(time.monotonic() - started, 2)
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    p.add_argument("--timeout", type=float, default=180)
    p.add_argument("--max-tokens", type=int, default=256)
    args = p.parse_args()
    report = asyncio.run(run(args))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
