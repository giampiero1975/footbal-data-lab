#!/usr/bin/env python3
"""RD-THINK-01: compare Qwen thinking off/on with frozen input and evidence.

This diagnostic never performs retrieval and never changes production defaults.
It records the first generation and a like-for-like repair for each mode.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

import smoke_test_rag_v5_e2e as v5


RUBRIC = {
    "tactical_correctness": 35,
    "coverage": 25,
    "role_side_phase_coherence": 20,
    "documentary_support": 15,
    "constraint_compliance": 5,
}


def call(payload: dict, timeout: int) -> tuple[dict, float]:
    started = time.monotonic()
    request = Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    return result, round(time.monotonic() - started, 3)


def response_record(result: dict, elapsed: float, plan: dict) -> dict:
    message = result.get("message") or {}
    answer = v5.sanitize_tactical_output(message.get("content", ""))
    return {
        "answer": answer,
        "thinking": message.get("thinking", ""),
        "audit": v5.tactical_audit_answer(answer, plan),
        "done": result.get("done"),
        "done_reason": result.get("done_reason"),
        "prompt_eval_count": result.get("prompt_eval_count"),
        "eval_count": result.get("eval_count"),
        "total_duration_ns": result.get("total_duration"),
        "prompt_eval_duration_ns": result.get("prompt_eval_duration"),
        "eval_duration_ns": result.get("eval_duration"),
        "elapsed_seconds": elapsed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--num-predict", type=int, default=4096)
    parser.add_argument("--context-window", type=int, default=8192)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"output exists; refusing overwrite: {args.output}")

    source = json.loads(args.input.read_text(encoding="utf-8"))
    item = source["questions"][0]
    question, evidence, plan = item["question"], item["evidence"], item["tactical_plan"]
    context = "\n\n".join(
        f"[F{i}] Fonte: {row['source']} | Pagine: {row['pages']}\n{row['text']}"
        for i, row in enumerate(evidence, 1)
    )
    concise = (
        "\nRispondi direttamente, senza premessa né riepilogo della domanda, entro 350 parole. "
        "Crea una sezione numerata per ogni punto richiesto, tratta tutti i punti prima di aggiungere dettagli, "
        "usa frasi operative ed evita ripetizioni. Mantieni rigorosamente distinte le fasi richieste "
        "(possesso, non possesso, perdita e riconquista) e non sostituirle fra loro.\n"
    )
    messages = [
        {"role": "system", "content": v5.SYSTEM + v5.scoped_guidance(question)
         + v5.generation_guidance(question) + v5.generation_contract(plan) + concise},
        {"role": "user", "content": f"DOMANDA:\n{question}\n\nFONTI:\n{context}"},
    ]
    modes = {}
    for thinking in (False, True):
        payload = {
            "model": args.model,
            "stream": False,
            "think": thinking,
            "messages": messages,
            "options": {"temperature": 0, "num_ctx": args.context_window,
                        "num_predict": args.num_predict},
        }
        first_raw, first_elapsed = call(payload, args.timeout)
        first = response_record(first_raw, first_elapsed, plan)
        missing = (first["audit"]["missing_facets"] + first["audit"]["missing_operational"]
                   + first["audit"]["missing_details"] + first["audit"].get("semantic_issues", []))
        repair = None
        if missing or first["done_reason"] == "length":
            repair_payload = dict(payload)
            repair_payload["messages"] = messages + [
                {"role": "assistant", "content": first["answer"]},
                {"role": "user", "content":
                 "Riscrivi integralmente la risposta senza aggiungere nuove fonti o affermazioni non sostenute. "
                 "Correggi esclusivamente questi problemi: " + "; ".join(missing or ["risposta troncata"]) +
                 ". Copri prima tutti i requisiti obbligatori, mantieni le citazioni accanto ai principi "
                 "documentali, elimina formule astratte e resta entro il limite."},
            ]
            repair_raw, repair_elapsed = call(repair_payload, args.timeout)
            repair = response_record(repair_raw, repair_elapsed, plan)
        modes["thinking_on" if thinking else "thinking_off"] = {"first": first, "repair": repair}

    report = {
        "experiment": "RD-THINK-01",
        "status": "ESEGUITO",
        "model": args.model,
        "source_case": str(args.input),
        "question": question,
        "evidence": evidence,
        "tactical_plan": plan,
        "rubric_fixed_before_execution": RUBRIC,
        "configuration": {"temperature": 0, "context_window": args.context_window,
                          "num_predict": args.num_predict, "timeout": args.timeout,
                          "retrieval_rerun": False, "production_default_changed": False},
        "modes": modes,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({mode: {stage: None if value is None else {
        "done_reason": value["done_reason"], "elapsed_seconds": value["elapsed_seconds"],
        "eval_count": value["eval_count"], "complete": value["audit"]["complete"],
        "issues": value["audit"].get("semantic_issues", [])}
        for stage, value in data.items()} for mode, data in modes.items()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
