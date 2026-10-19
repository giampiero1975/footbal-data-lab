#!/usr/bin/env python3
"""Isola la metrica coverage Ragas DiscreteMetric su H07, con traceback completo.

Documentazione: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/general_purpose/
Non legge/scrive Chroma, non modifica gold o benchmark precedenti.
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="H07")
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--output", type=Path, default=ROOT / "diagnostica_ragas_coverage_h07_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"Non sovrascrivo: {args.output}")

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
    coverage = DiscreteMetric(
        name="tactical_coverage",
        allowed_values=["completo", "parziale"],
        prompt=("Valuta SOLO la copertura dei nuclei semantici presenti nella FONTE. "
                "Completo se tutti i nuclei (ruoli, azioni, condizioni essenziali) "
                "sono trattati anche con parafrasi, indipendentemente dalla loro "
                "correttezza; parziale se almeno un nucleo essenziale e' assente. "
                "Non richiedere ripetizioni letterali.\nFONTE: {reference}\nFRASE: {response}"))
    report = {
        "schema_version": 1, "purpose": "ragas_coverage_diagnostic_not_benchmark",
        "ragas_version": getattr(ragas, "__version__", "unknown"),
        "openai_version": getattr(openai, "__version__", "unknown"),
        "model": args.model, "case": args.id, "claim": case["claim"],
        "phase": "coverage_only", "results": [],
        "limitations": ["Una sola chiamata Ragas, possibile variabilita' stocastica",
                        "Gold preliminare; non misura fedelta'"]
    }
    start = time.monotonic()
    try:
        score = await coverage.ascore(reference=evidence, response=case["statement"], llm=llm)
        report["results"].append({"status": "success", "value": str(score.value),
                                  "expected": case["expected_coverage"],
                                  "match": str(score.value) == case["expected_coverage"]})
        print(f"RAGAS_COVERAGE_OK value={score.value} expected={case['expected_coverage']}", flush=True)
    except Exception as exc:
        details = {
            "type": type(exc).__module__ + "." + type(exc).__qualname__,
            "repr": repr(exc), "message": str(exc),
            "args": [repr(x) for x in exc.args],
            "traceback": "".join(traceback.format_exception(exc))
        }
        report["results"].append({"status": "error", "exception": details})
        print(f"RAGAS_COVERAGE_ERROR {details['repr']}\n{details['traceback']}", flush=True)
    finally:
        report["elapsed_seconds"] = round(time.monotonic() - start, 2)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"REPORT {args.output}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
