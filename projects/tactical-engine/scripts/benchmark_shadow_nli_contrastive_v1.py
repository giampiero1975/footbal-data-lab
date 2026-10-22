#!/usr/bin/env python3
"""Shadow-only contrastive NLI V2 diagnostic; preserves canonical prompt and production."""
import argparse
import json
import time
from pathlib import Path
from shadow_nli_v2_inference import judge_pair

CASES = [
    # Same q3/F1 evidence; vary preference direction and logical form.
    ("q3", "F1", "low_width_preferred", "Contro una difesa molto bassa è preferibile sfruttare l'ampiezza anziché verticalizzare.", "supported", "comparison"),
    ("q3", "F1", "low_vertical_preferred", "Contro una difesa molto bassa è preferibile verticalizzare anziché sfruttare l'ampiezza.", "contradicted", "comparison"),
    ("q3", "F1", "low_width_advised", "Contro una difesa molto bassa il testo consiglia la manovra aggirante.", "supported", "paraphrase"),
    ("q3", "F1", "low_vertical_advised", "Contro una difesa molto bassa il testo consiglia la verticalizzazione invece della manovra aggirante.", "contradicted", "paraphrase"),
    ("q3", "F1", "low_width_not_preferred", "Contro una difesa molto bassa la manovra aggirante non è preferibile alla verticalizzazione.", "contradicted", "negation"),
    ("q3", "F1", "low_vertical_difficult", "Contro una difesa molto bassa la verticalizzazione è difficile da attuare.", "supported", "paraphrase"),
    # Same q5/F1 evidence; vary quantifier scope without introducing external facts.
    ("q5", "F1", "three_systems_methodist", "Nei tre sistemi descritti è previsto un centromediano metodista.", "supported", "scope"),
    ("q5", "F1", "pane_systems_methodist", "Tutti e tre i sistemi descritti dall'autore prevedono il centromediano metodista.", "supported", "scope"),
    ("q5", "F1", "all_football_systems", "Tutti i sistemi di gioco del calcio prevedono necessariamente il centromediano metodista.", "insufficient", "universal"),
    ("q5", "F1", "every_team_methodist", "Ogni squadra di calcio deve utilizzare un centromediano metodista.", "insufficient", "universal"),
    ("q5", "F1", "no_other_system", "Non esistono sistemi di gioco senza centromediano metodista.", "insufficient", "universal"),
    ("q5", "F1", "one_pane_system_no_methodist", "Uno dei tre sistemi descritti non prevede il centromediano metodista.", "contradicted", "scope"),
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_baseline_20261022.json"))
    parser.add_argument("--output", type=Path, default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_contrastive_v1_20261022.json"))
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        parser.error("Explicit --execute required")
    if args.output.resolve() == args.source.resolve() or args.output.exists():
        parser.error("Output exists or overlaps input; no overwriting allowed")
    if not args.source.is_file():
        parser.error(f"Baseline mancante: {args.source}; nessun benchmark avviato")
    if not args.output.parent.is_dir():
        parser.error(f"Directory report mancante: {args.output.parent}; non viene creata automaticamente")
    source = json.loads(args.source.read_text(encoding="utf-8"))
    questions = {q["id"]: q for q in source["questions"]}
    evidence = {}
    for qid, sid, *_ in CASES:
        evidence[(qid, sid)] = next(e["text"] for e in questions[qid]["evidence"] if e["label"] == sid)
    results = []
    for qid, sid, case_id, claim, expected, category in CASES:
        started = time.monotonic()
        try:
            actual = judge_pair(claim, evidence[(qid, sid)])
            item = {"id": case_id, "question_id": qid, "source_id": sid, "category": category, "claim": claim, "expected": expected, "actual": actual, "pass": actual == expected, "elapsed_seconds": round(time.monotonic() - started, 3)}
        except Exception as exc:
            item = {"id": case_id, "question_id": qid, "source_id": sid, "category": category, "claim": claim, "expected": expected, "actual": None, "pass": False, "error": str(exc)[:300]}
        results.append(item)
        print(case_id, item["actual"], "expected", expected, flush=True)
    report = {"schema": "shadow_nli_contrastive_v1", "mode": "shadow_only", "total": len(results), "passed": sum(r["pass"] for r in results), "errors": sum("error" in r for r in results), "cases": results, "limitations": ["Curated diagnostic; not population accuracy", "Same evidence per family; canonical NLI V2 unchanged", "RAG V5 and Chroma unchanged"]}

    with args.output.open("x", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("CONTRASTIVE", report["passed"], "/", report["total"], "errors", report["errors"], "REPORT", args.output, flush=True)

if __name__ == "__main__":
    main()
