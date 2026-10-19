#!/usr/bin/env python3
"""Riproduzione diagnostica Ragas DiscreteMetric H07, senza modificare il benchmark.

Documentazione:
https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/general_purpose/
https://docs.ollama.com/api/openai-compatibility

Output separato, traceback integrale, eccezioni concatenate e traceback per fase.
Non accede a Chroma; non modifica gold, modelli o benchmark.
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

def describe_exception(exc):
    result = {"type": type(exc).__module__ + "." + type(exc).__qualname__,
              "message": str(exc),
              "repr": repr(exc),
              "args": [repr(a) for a in exc.args],
              "traceback": "".join(traceback.format_exception(exc))}
    for field in ("response", "last_completion", "completion", "raw_output"):
        try:
            value = getattr(exc, field, None)
            if value is not None:
                result[field] = str(value)[:20000]
        except Exception:
            pass
    return result

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="H07")
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "diagnostica_ragas_discrete_h07_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"Non sovrascrivo il report esistente: {args.output}")

    from openai import AsyncOpenAI
    from ragas.llms import llm_factory
    from ragas.metrics import DiscreteMetric
    import ragas
    import openai

    gold = json.loads((ROOT / "evaluation/gold_glerean_principi_v1.json").read_text(encoding="utf-8"))
    claims = {c["id"]: c for case in gold["cases"] for c in case["gold_claims"]}
    case = next((t for t in TESTS if t["id"] == args.id), None)
    if case is None:
        raise ValueError(f"ID non presente: {args.id}")
    evidence = claims[case["claim"]]["evidence"]
    client = AsyncOpenAI(api_key="ollama", base_url="http://127.0.0.1:11434/v1", timeout=600)
    llm = llm_factory(args.model, provider="openai", client=client)

    fidelity = DiscreteMetric(
        name="tactical_fidelity",
        allowed_values=["coerente", "contraddittorio", "evidenza_insufficiente"],
        prompt=("Confronta esclusivamente FONTE e FRASE. "
                "Se la FRASE inverte un ruolo, un'azione, una condizione o nega "
                "un principio della FONTE, rispondi contraddittorio. "
                "Se la FRASE e' supportata dalla FONTE, rispondi coerente. "
                "Se la FONTE non permette di stabilirlo, evidenza_insufficiente. "
                "Non usare conoscenze esterne.\nFONTE: {reference}\nFRASE: {response}"))
    report = {
        "schema_version": 1,
        "purpose": "ragas_discrete_metric_error_trace_not_a_benchmark",
        "ragas_version": getattr(ragas, "__version__", "unknown"),
        "openai_version": getattr(openai, "__version__", "unknown"),
        "model": args.model,
        "case": args.id,
        "claim": case["claim"],
        "phase": "fidelity_only",
        "results": [],
        "limitations": ["Una sola chiamata Ragas; errore eventualmente intermittente",
                        "Non misura coverage né modifica benchmark originali"]
    }
    started = time.monotonic()
    try:
        score = await fidelity.ascore(reference=evidence, response=case["statement"], llm=llm)
        report["results"].append({"status": "success", "value": str(score.value),
                                  "expected": case["expected_fidelity"]})
        print(f"RAGAS_FIDELITY_OK value={score.value}", flush=True)
    except Exception as exc:
        detail = describe_exception(exc)
        report["results"].append({"status": "error", "exception": detail})
        print(f"RAGAS_FIDELITY_ERROR {detail['type']}: {detail['repr']}", flush=True)
        print(detail["traceback"], flush=True)
    finally:
        report["elapsed_seconds"] = round(time.monotonic() - started, 2)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
        print(f"REPORT {args.output}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
