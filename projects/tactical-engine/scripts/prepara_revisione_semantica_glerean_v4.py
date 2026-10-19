#!/usr/bin/env python3
"""Prepara una matrice di revisione semantica verificabile dai gold claim.

Nessuna inferenza automatica: 'non_verificato' resta tale fino a revisione.
Non accede a Chroma, Ollama, GPU o rete.
"""
import argparse
import json
from pathlib import Path

VERDICTS={"supportato","parziale","omesso","contraddetto","non_verificato"}

def build(data):
    result={"schema_version":1,"method":"gold_claim_semantic_review",
            "warning":"La correttezza di un ID non implica supporto semantico. Le decisioni richiedono prove.",
            "cases":[]}
    for run in data["runs"]:
        refs={s["ref"]:{"chunk_index":s["chunk_index"],
                         "page_numbers":s.get("page_numbers"),"text":s["text"]}
              for s in run["sources"]}
        result["cases"].append({
            "case_id":run["case_id"],"mode":run["mode"],
            "question":run["question"],"answer":run["answer"],
            "available_sources":refs,
            "claims":[{"id":g["id"],"gold_claim":g["claim"],
                       "gold_evidence":g["evidence"],
                       "verdict":"non_verificato",
                       "answer_excerpt":"","supporting_refs":[],
                       "source_evidence_excerpt":"","review_notes":""}
                      for g in run["gold_claims"]]
        })
    return result

def validate(review):
    errors=[]
    for case in review["cases"]:
        refs=case["available_sources"]
        for claim in case["claims"]:
            label=f'{case["case_id"]}/{case["mode"]}/{claim["id"]}'
            if claim["verdict"] not in VERDICTS:
                errors.append(f"{label}: verdetto sconosciuto")
            if any(r not in refs for r in claim["supporting_refs"]):
                errors.append(f"{label}: riferimento non disponibile")
            if claim["verdict"] in {"supportato","parziale","contraddetto"}:
                if not claim["answer_excerpt"] or not claim["supporting_refs"] or not claim["source_evidence_excerpt"]:
                    errors.append(f"{label}: mancano estratto risposta, fonte o prova testuale")
                if claim["answer_excerpt"] and claim["answer_excerpt"] not in case["answer"]:
                    errors.append(f"{label}: estratto risposta non presente nella risposta")
                if claim["source_evidence_excerpt"] and not any(
                    claim["source_evidence_excerpt"] in refs[r]["text"]
                    for r in claim["supporting_refs"] if r in refs):
                    errors.append(f"{label}: prova testuale non presente nelle fonti citate")
            if claim["verdict"]=="omesso" and not claim["review_notes"]:
                errors.append(f"{label}: motivazione omissione mancante")
    return errors

def main():
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--validate",action="store_true")
    a=p.parse_args()
    data=json.loads(a.input.read_text(encoding="utf-8"))
    if a.validate:
        errors=validate(data)
        for error in errors: print("ERRORE:",error)
        print(f"Revisione: {len(data['cases'])} casi, {sum(len(c['claims']) for c in data['cases'])} claim, {len(errors)} errori di struttura")
        raise SystemExit(1 if errors else 0)
    if len(data.get("runs",[]))!=6: raise ValueError("Attese sei generazioni")
    report=build(data)
    output=a.output or a.input.with_name(a.input.stem+"_semantic_review.json")
    if output.exists(): raise FileExistsError(f"File gia presente: {output}")
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Preparata matrice: {len(report['cases'])} risposte, {sum(len(c['claims']) for c in report['cases'])} claim, tutti non_verificato")
    print(f"REPORT: {output}")

if __name__=="__main__":main()
