#!/usr/bin/env python3
"""Offline diagnostic: cited support versus relevance to question and scope preservation.

Human-review seed labels are hypotheses, not validated gold. No Ollama or Chroma calls.
Inputs: shadow NLI V2 report. Output: new JSON, never overwrites input.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

# Relevance: direct / contextual / off_target.
# Scope: preserved / overgeneralized / needs_context.
# Conservative expert review hypotheses, deliberately separate from NLI labels.
REVIEW = {
    "q4_diag_01": ("direct", "preserved", "Movimenti e passaggi sincronizzati descrivono il funzionamento dei triangoli."),
    "q4_diag_02": ("direct", "needs_context", "La fonte descrive i triangoli in uno specifico sistema, non qualsiasi disposizione."),
    "q4_diag_03": ("direct", "needs_context", "La fonte attribuisce il beneficio allo specifico sistema analizzato."),
    "q4_diag_04": ("direct", "preserved", "Il quarto uomo e i triangoli successivi rispondono direttamente alla domanda."),
    "q5_diag_01": ("contextual", "preserved", "La fonte descrive due sistemi, non gli effetti del passaggio dall'uno all'altro durante la gara."),
    "q5_diag_02": ("contextual", "preserved", "Densita centrale dei sistemi descritti; non un vantaggio causato dal cambio in partita."),
    "q5_diag_03": ("contextual", "overgeneralized", "La fonte dice 'in tutti e tre i sistemi', non 'indipendentemente dal sistema adottato'."),
    "q5_diag_04": ("off_target", "preserved", "Svantaggi della zona, senza nesso con la decisione di cambiare modulo in partita."),
    "q5_diag_05": ("contextual", "needs_context", "Rischi del 3-4-1-2: applicabili se si passa a tale sistema, ma il cambio non e discusso."),
    "q5_diag_06": ("off_target", "needs_context", "Linee di passaggio variabili nell'azione, non rischi della variazione del sistema."),
}

def analyze(report):
    if report.get("mode") != "shadow_nli_v2_inference":
        raise ValueError("Expected NLI V2 inference report")
    claims = report["claims"]
    ids = [c["claim_id"] for c in claims]
    if len(ids) != len(set(ids)) or set(ids) != set(REVIEW):
        raise ValueError("Claim IDs differ from reviewed diagnostic set")
    rows = []
    for c in claims:
        relevance, scope, reason = REVIEW[c["claim_id"]]
        labels = [p["nli_label"] for p in c["pairs"]]
        if not labels or any(label is None for label in labels):
            raise ValueError("Incomplete NLI labels")
        rows.append({
            "question_id": c["question_id"], "claim_id": c["claim_id"],
            "claim": c["claim"], "nli_labels": labels,
            "nli_status": c["status"], "relevance_review": relevance,
            "scope_review": scope, "review_reason": reason,
            "review_status": "provisional_expert_hypothesis",
        })
    by_question = {}
    for qid in sorted(set(r["question_id"] for r in rows)):
        subset = [r for r in rows if r["question_id"] == qid]
        by_question[qid] = {
            "claims": len(subset),
            "relevance": dict(Counter(r["relevance_review"] for r in subset)),
            "scope": dict(Counter(r["scope_review"] for r in subset)),
            "nli_supported_claims": sum(r["nli_status"] == "supported_by_cited_evidence" for r in subset),
        }
    return {
        "schema": "rag_v5_question_alignment_scope_diagnostic_v1",
        "mode": "offline_review_only",
        "not_gold": True,
        "limitations": [
            "Provisional manually curated labels; not independently adjudicated gold",
            "Purposeful Q4/Q5 selection; cannot estimate population-level performance",
            "NLI factual support and answer relevance are different dimensions",
            "No model inference or production pipeline modifications",
        ],
        "by_question": by_question,
        "rows": rows,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input and output must differ")
    result = analyze(json.loads(args.input.read_text(encoding="utf-8")))
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print("DIAGNOSTIC OK:", len(result["rows"]), "claims")
    for qid, stats in result["by_question"].items():
        print(qid, json.dumps(stats, ensure_ascii=False))
    print("REPORT:", args.output)

if __name__ == "__main__":
    main()
