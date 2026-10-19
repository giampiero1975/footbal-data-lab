#!/usr/bin/env python3
"""Diagnostica read-only per IncompleteOutputException Ragas 0.4.3.

Isola il trasporto Ollama OpenAI-compatible da Ragas. Non legge Chroma,
non modifica il benchmark originale e non sovrascrive report esistenti.
Fonti: https://docs.ollama.com/api/openai-compatibility
       https://docs.ollama.com/capabilities/structured-outputs
"""
import argparse
import asyncio
import json
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from benchmark_holdout_glerean_v4 import TESTS

async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--id", default="H07")
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--output", type=Path, default=ROOT / "diagnostica_ragas_h07_v1.json")
    args = p.parse_args()
    if args.output.exists():
        raise FileExistsError(f"Report gia' presente: {args.output}")
    from openai import AsyncOpenAI
    import openai
    import ragas
    gold = json.loads((ROOT / "evaluation/gold_glerean_principi_v1.json").read_text(encoding="utf-8"))
    claims = {c["id"]: c for case in gold["cases"] for c in case["gold_claims"]}
    t = next((x for x in TESTS if x["id"] == args.id), None)
    if t is None:
        raise ValueError("ID non presente nel benchmark")
    source = claims[t["claim"]]["evidence"]
    prompt = ("Confronta il principio tattico e la frase. Restituisci solo JSON "
              "con una proprieta' fidelity uguale a coerente, contraddittorio "
              "o evidenza_insufficiente. Non usare conoscenze esterne.\n"
              f"FONTE:\n{source}\nFRASE:\n{t['statement']}")
    report = {
        "schema_version": 1,
        "purpose": "transport_and_structured_output_diagnostic_not_benchmark",
        "ragas_version": getattr(ragas, "__version__", "unknown"),
        "openai_version": getattr(openai, "__version__", "unknown"),
        "model": args.model, "test_id": args.id,
        "source_claim": t["claim"], "checks": [],
    }
    client = AsyncOpenAI(api_key="ollama", base_url="http://127.0.0.1:11434/v1", timeout=600)
    schema = {"type": "json_schema", "json_schema": {
        "name": "tactical_fidelity_probe", "strict": True,
        "schema": {"type": "object", "properties": {
            "fidelity": {"type": "string", "enum": [
                "coerente", "contraddittorio", "evidenza_insufficiente"]}},
            "required": ["fidelity"], "additionalProperties": False}}}
    for mode in ("plain", "json_schema"):
        row = {"mode": mode}
        start = time.monotonic()
        try:
            kw = {"model": args.model,
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0}
            if mode == "json_schema":
                kw["response_format"] = schema
            response = await client.chat.completions.create(**kw)
            choice = response.choices[0]
            raw = choice.message.content
            row.update(finish_reason=choice.finish_reason,
                       raw_content=raw,
                       parsed_json=None,
                       usage=response.usage.model_dump() if response.usage else None)
            try:
                row["parsed_json"] = json.loads(raw) if raw else None
            except (ValueError, TypeError) as exc:
                row["json_error"] = str(exc)
        except Exception as exc:
            row.update(error_type=type(exc).__name__, error=str(exc),
                       traceback=traceback.format_exc(limit=8))
        row["seconds"] = round(time.monotonic() - start, 2)
        report["checks"].append(row)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{mode}: finish={row.get('finish_reason')} "
              f"error={row.get('error_type')} "
              f"json={row.get('parsed_json') is not None}", flush=True)
    print(f"REPORT: {args.output}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
