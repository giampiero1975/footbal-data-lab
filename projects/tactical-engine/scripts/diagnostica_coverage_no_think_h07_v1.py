#!/usr/bin/env python3
"""Test isolato H07 coverage: Ollama native API, thinking disabilitato.
Documentazione: https://docs.ollama.com/capabilities/thinking
https://docs.ollama.com/capabilities/structured-outputs
Non modifica Chroma, modelli, gold, venv o benchmark esistenti.
"""
import json, time, urllib.request
from pathlib import Path
from benchmark_holdout_glerean_v4 import TESTS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "diagnostica_coverage_no_think_h07_v1.json"
if OUT.exists():
    raise FileExistsError(f"Non sovrascrivo: {OUT}")
gold = json.loads((ROOT / "evaluation/gold_glerean_principi_v1.json").read_text(encoding="utf-8"))
claims = {c["id"]: c for case in gold["cases"] for c in case["gold_claims"]}
case = next(t for t in TESTS if t["id"] == "H07")
evidence = claims[case["claim"]]["evidence"]
prompt = ("Valuta SOLO la copertura dei nuclei semantici presenti nella FONTE. "
          "Completo se tutti i nuclei (ruoli, azioni, condizioni essenziali) "
          "sono trattati anche con parafrasi, indipendentemente dalla loro "
          "correttezza; parziale se almeno un nucleo essenziale e' assente. "
          "Non richiedere ripetizioni letterali. Rispondi esclusivamente con JSON.\n"
          f"FONTE: {evidence}\nFRASE: {case['statement']}")
schema = {"type": "object", "properties": {"value": {"type": "string", "enum": ["completo", "parziale"]}},
          "required": ["value"], "additionalProperties": False}
payload = {"model": "qwen3.5:9b", "stream": False, "think": False,
           "messages": [{"role": "user", "content": prompt}], "format": schema,
           "options": {"temperature": 0, "num_ctx": 4096, "num_predict": 256}}
report = {"schema_version": 1, "case": "H07", "purpose": "isolate_ollama_no_think_not_ragas",
          "source": "gold_glerean_principi_v1.json", "expected_coverage": case["expected_coverage"],
          "request_options": {"think": False, "temperature": 0, "num_ctx": 4096, "num_predict": 256}}
start = time.monotonic()
try:
    request = urllib.request.Request("http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=600) as response:
        raw = json.load(response)
    msg = raw.get("message", {})
    report["response"] = {"content": msg.get("content"), "thinking": msg.get("thinking"),
                          "done_reason": raw.get("done_reason"), "eval_count": raw.get("eval_count"),
                          "prompt_eval_count": raw.get("prompt_eval_count")}
    value = json.loads(msg["content"])["value"]
    report["predicted_coverage"] = value
    report["match"] = value == case["expected_coverage"]
    report["status"] = "ok"
    print(f"NO_THINK_OK value={value} expected={case['expected_coverage']}", flush=True)
except Exception as exc:
    report["status"] = "error"
    report["error"] = f"{type(exc).__name__}: {exc}"
    print(f"NO_THINK_ERROR {report['error']}", flush=True)
finally:
    report["elapsed_seconds"] = round(time.monotonic() - start, 2)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"REPORT {OUT}", flush=True)
