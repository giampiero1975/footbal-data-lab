#!/usr/bin/env python3
"""Build provisional contrastive controls from existing Q4/Q5 NLI report, offline."""
import argparse
import json
from pathlib import Path
from collections import Counter

def build(report):
    c = {x["claim_id"]: x for x in report["claims"]}
    rows = []
    def add(name, cid, question, expected, reason, category, claim=None):
        x = c[cid]
        rows.append({"id": name, "source_claim_id": cid, "question": question,
                     "claim": claim or x["claim"], "evidence": x["pairs"][0]["evidence"],
                     "expected": expected, "reason": reason, "category": category})
    entail = "La fonte sostiene questa affermazione?"
    for cid in ("q4_diag_01", "q4_diag_04", "q5_diag_01", "q5_diag_04"):
        add("positive_" + cid, cid, entail, "supported",
            "Controllo positivo di supporto testuale, non di pertinenza.", "nli")
    add("negative_scope_q5", "q5_diag_03", entail, "insufficient",
        "Tre sistemi analizzati non implicano tutti i sistemi possibili.", "nli",
        "Il centromediano metodista protegge la difesa e costruisce il gioco in qualsiasi sistema di gioco.")
    question = "Quali rischi derivano dal cambiare modulo durante una partita?"
    add("negative_zone", "q5_diag_04", question, "off_target",
        "Svantaggi statici della zona, non del cambio di modulo.", "alignment")
    add("negative_pass", "q5_diag_06", question, "off_target",
        "Linee di passaggio durante un'azione, non cambio di modulo.", "alignment")
    add("context_defense3", "q5_diag_05", question, "contextual",
        "Rischi del 3-4-1-2, rilevanti se si passa a tale sistema.", "alignment")
    add("positive_triangles", "q4_diag_04",
        "Come si sviluppano combinazioni con triangoli e quarto uomo?", "direct",
        "Risponde al meccanismo richiesto.", "alignment")
    add("context_counterattack", "q5_diag_01", question, "contextual",
        "Confronto tra sistemi, non conseguenze della transizione.", "alignment")
    if len(rows) != 10 or len({r["id"] for r in rows}) != 10:
        raise ValueError("Unexpected benchmark shape")
    return {"schema": "rag_v5_alignment_controls_v1", "status": "provisional_not_gold",
            "limitations": ["Labels are manually curated, not independently adjudicated",
                            "NLI and question alignment are separate tasks",
                            "No inference and no production changes"],
            "controls": rows,
            "summary": {key: sum(r["expected"] == key for r in rows)
                        for key in ("supported", "insufficient", "direct", "contextual", "off_target")}}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    if a.input.resolve() == a.output.resolve():
        p.error("Input and output must differ")
    report = json.loads(a.input.read_text(encoding="utf-8"))
    if report.get("mode") != "shadow_nli_v2_inference":
        p.error("Expected shadow NLI V2 report")
    result = build(report)
    with a.output.open("x", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("BENCHMARK OK:", len(result["controls"]), "controls; no inference")
    print("SUMMARY:", json.dumps(result["summary"], ensure_ascii=False))
    print("REPORT:", a.output)

if __name__ == "__main__":
    main()
