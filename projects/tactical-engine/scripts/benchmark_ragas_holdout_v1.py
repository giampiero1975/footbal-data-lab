#!/usr/bin/env python3
"""Esperimento Ragas isolato: holdout Glerean, nessuna lettura/scrittura Chroma.

Documentazione API:
https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/general_purpose/
https://docs.ragas.io/en/stable/getstarted/quickstart/
https://docs.ollama.com/api/openai-compatibility
"""
import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "evaluation/gold_glerean_principi_v1.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from benchmark_holdout_glerean_v4 import TESTS  # frozen baseline: do not edit labels

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="+", default=["H07", "H09", "H10", "H06"])
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--output", type=Path, default=ROOT / "benchmark_ragas_holdout_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"Non sovrascrivo un report esistente: {args.output}")
    from openai import AsyncOpenAI
    from ragas.llms import llm_factory
    from ragas.metrics import DiscreteMetric
    import ragas
    import openai
    client = AsyncOpenAI(api_key="ollama", base_url="http://127.0.0.1:11434/v1", timeout=600)
    llm = llm_factory(args.model, provider="openai", client=client)
    gold = json.loads(GOLD.read_text(encoding="utf-8"))
    claims = {c["id"]: c for case in gold["cases"] for c in case["gold_claims"]}
    tests = {t["id"]: t for t in TESTS}
    if any(i not in tests for i in args.ids):
        raise ValueError("ID non presente nel benchmark holdout")
    fidelity = DiscreteMetric(
        name="tactical_fidelity",
        allowed_values=["coerente", "contraddittorio", "evidenza_insufficiente"],
        prompt=("Confronta esclusivamente FONTE e FRASE. "
                "Se la FRASE inverte un ruolo, un'azione, una condizione o nega "
                "un principio della FONTE, rispondi contraddittorio. "
                "Se la FRASE e' supportata dalla FONTE, rispondi coerente. "
                "Se la FONTE non permette di stabilirlo, evidenza_insufficiente. "
                "Non usare conoscenze esterne.\nFONTE: {reference}\nFRASE: {response}")
    )
    coverage = DiscreteMetric(
        name="tactical_coverage",
        allowed_values=["completo", "parziale"],
        prompt=("Valuta SOLO la copertura dei nuclei semantici presenti nella FONTE. "
                "Completo se tutti i nuclei (ruoli, azioni, condizioni essenziali) "
                "sono trattati anche con parafrasi, indipendentemente dalla loro "
                "correttezza; parziale se almeno un nucleo essenziale e' assente. "
                "Non richiedere ripetizioni letterali.\nFONTE: {reference}\nFRASE: {response}")
    )
    report = {
        "schema_version": 1,
        "framework": "ragas",
        "ragas_version": getattr(ragas, "__version__", "unknown"),
        "openai_version": getattr(openai, "__version__", "unknown"),
        "model": args.model,
        "method": "ragas_discrete_metric_two_axes",
        "test_ids": args.ids,
        "results": [],
        "limitations": [
            "Metriche DiscreteMetric personalizzate, NON metriche Ragas Faithfulness standard",
            "Frasi sintetiche, non risposte RAG reali",
            "Gold etichettato preliminarmente; figure originali non verificate",
            "Un solo giudice locale; risultati non equivalgono a validazione indipendente",
        ],
    }
    for ident in args.ids:
        t = tests[ident]
        evidence = claims[t["claim"]]["evidence"]
        row = dict(t)
        start = time.monotonic()
        try:
            f = await fidelity.ascore(reference=evidence, response=t["statement"], llm=llm)
            c = await coverage.ascore(reference=evidence, response=t["statement"], llm=llm)
            row.update(
                predicted_fidelity=str(f.value),
                predicted_coverage=str(c.value),
                fidelity_match=str(f.value) == t["expected_fidelity"],
                coverage_match=str(c.value) == t["expected_coverage"],
                seconds=round(time.monotonic() - start, 1),
            )
            print(f'{ident}: fedelta={"OK" if row["fidelity_match"] else "ERRORE"} '
                  f'copertura={"OK" if row["coverage_match"] else "ERRORE"}', flush=True)
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
            print(f'{ident}: ERRORE TECNICO {row["error"]}', flush=True)
        report["results"].append(row)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    valid = [x for x in report["results"] if "fidelity_match" in x]
    print(f'REPORT {args.output}: fedelta={sum(x["fidelity_match"] for x in valid)}/{len(valid)} '
          f'copertura={sum(x["coverage_match"] for x in valid)}/{len(valid)}')

if __name__ == "__main__":
    asyncio.run(main())
