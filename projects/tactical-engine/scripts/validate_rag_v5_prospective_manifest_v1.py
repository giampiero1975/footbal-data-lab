#!/usr/bin/env python3
"""Validate prospective RAG holdout candidate; never touches Chroma or Ollama."""
import argparse, hashlib, json
from pathlib import Path

REQUIRED_CATEGORIES={"transizione_positiva","transizione_negativa","confine_fasi","zona_recupero","blocco_basso","cambio_modulo","multisorgente","esercitazione_vs_gara","quantificatori","astensione"}

def validate(doc):
    errors=[]
    questions=doc.get("questions",[])
    if len(questions)!=10:errors.append("expected exactly 10 questions")
    ids=[q.get("id") for q in questions]
    if len(ids)!=len(set(ids)):errors.append("duplicate question IDs")
    categories={q.get("category") for q in questions}
    if categories!=REQUIRED_CATEGORIES:errors.append("unexpected or missing categories")
    if not doc.get("policy",{}).get("no_tuning_on_holdout"):errors.append("no_tuning_on_holdout must be true")
    for q in questions:
        id=q.get("id","<missing>")
        if not q.get("question"):errors.append(f"{id}: missing question")
        if not q.get("source_refs"):errors.append(f"{id}: missing source refs")
        if not q.get("verified_pages"):errors.append(f"{id}: missing verified pages")
        if not q.get("mandatory_claims"):errors.append(f"{id}: missing mandatory claims")
        if not q.get("forbidden_claims"):errors.append(f"{id}: missing forbidden claims")
        if not q.get("reviewer"):errors.append(f"{id}: missing independent reviewer")
        if any(not r.get("drive_file_id") or not r.get("page_label") for r in q.get("source_refs",[])):errors.append(f"{id}: source missing Drive ID or page label")
        if any("pending" in str(p).lower() or "verificare" in str(p).lower() or "confermare" in str(p).lower() for p in q.get("verified_pages",[])):errors.append(f"{id}: unverified page locator")
        if q.get("gold_status")!="verified":errors.append(f"{id}: gold not verified")
    return errors

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True,type=Path)
    args=p.parse_args()
    raw=args.manifest.read_bytes()
    data=json.loads(raw)
    errors=validate(data)
    print("SHA256",hashlib.sha256(raw).hexdigest())
    print("STATUS","BLOCKED" if errors else "READY_FOR_FREEZE")
    for e in errors:print("BLOCKER",e)
    raise SystemExit(1 if errors else 0)

if __name__=="__main__":main()
