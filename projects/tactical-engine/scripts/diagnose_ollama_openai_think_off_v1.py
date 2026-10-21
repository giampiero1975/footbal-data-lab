#!/usr/bin/env python3
"""Probe Ollama OpenAI-compatible think=false with a bounded JSON response.

Official reference: https://docs.ollama.com/openai
This is a transport diagnostic, not a Ragas benchmark. No production writes.
"""
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
    result = {"model": args.model, "endpoint": "/v1/chat/completions",
              "request": {"think": False, "max_tokens": args.max_tokens,
                          "temperature": 0}}
    try:
        response = await client.chat.completions.create(
            model=args.model,
            messages=[{"role": "system", "content": "Classifica l'affermazione rispetto alla fonte. Rispondi solo in JSON."},
                      {"role": "user", "content": "Fonte: con spazio alle spalle della difesa si può ricercare profondità. Affermazione: lo spazio alle spalle favorisce la profondità."}],
            response_format={"type": "json_schema", "json_schema": {
                "name": "judgement", "strict": True,
                "schema": {"type": "object",
                           "properties": {"label": {"type": "string", "enum": ["supported", "contradicted", "insufficient"]},
                                          "reason": {"type": "string"}},
                           "required": ["label", "reason"], "additionalProperties": False}}},
            extra_body={"think": False},
            temperature=0, max_tokens=args.max_tokens)
        choice = response.choices[0]
        result["finish_reason"] = choice.finish_reason
        result["content"] = choice.message.content
        result["usage"] = response.usage.model_dump() if response.usage else None
        try:
            result["parsed"] = json.loads(choice.message.content or "")
        except ValueError as exc:
            result["parse_error"] = str(exc)
    except Exception as exc:
        result["error"] = type(exc).__name__ + ": " + str(exc)[:1000]
    result["elapsed_seconds"] = round(time.monotonic() - started, 2)
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    p.add_argument("--max-tokens", type=int, default=256)
    p.add_argument("--timeout", type=float, default=120)
    args = p.parse_args()
    report = asyncio.run(run(args))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
