#!/usr/bin/env python3
"""Deterministic read-only phase-shadow regression audit. Stdlib only."""
import argparse, hashlib, json, re
from pathlib import Path

def audit(report):
    assert report.get("schema") == "rag_v5_phase_passage_shadow_v1"
    assert report.get("status") == "complete"
    out = {"schema":"rag_v5_phase_passage_regression_audit_v1",
           "source_sha256":None, "policy":"read-only deterministic audit; no LLM, no Chroma",
           "questions":[]}
    for q in report["questions"]:
        allowed = {e["label"] for e in q["evidence"]}
        cited = set(re.findall(r"\\[F\\d+\\]", q["answer"]))
        invalid = sorted(cited - {"["+x+"]" for x in allowed})
        answer = q["answer"].lower()
        flags = []
        if q["id"] == "holdout_06":
            if "non è possibile" in answer and "zona" in answer:
                flags.append({"id":"limited_evidence_acknowledged","kind":"positive_signal",
                              "note":"Heuristic only: verify semantic scope manually"})
        if q["id"] == "holdout_10":
            for code, pattern, reason in [
                ("zone_high_effectiveness",r"zone alte sono generalmente più efficaci",
                 "Comparative efficacy is not established by the supplied passages"),
                ("zone_low_longer_time",r"zone basse richiedono tempi più lunghi",
                 "Low-zone duration claim is not established by the supplied passages"),
                ("training_vs_match",r"10 contro 0",
                 "Exercise progression is not direct evidence for in-match choice")]:
                if re.search(pattern,answer):
                    flags.append({"id":code,"kind":"manual_review","note":reason})
        out["questions"].append({
            "id":q["id"],"allowed_labels":sorted(allowed),
            "cited_labels":sorted(cited),"invalid_citations":invalid,
            "flags":flags,"elapsed_seconds":q.get("elapsed_seconds"),
            "semantic_pass":"not_adjudicated"})
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    if a.input.resolve()==a.output.resolve() or a.output.exists():
        p.error("Refusing overwrite")
    raw=a.input.read_bytes()
    report=json.loads(raw)
    result=audit(report)
    result["source_sha256"]=hashlib.sha256(raw).hexdigest()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("x",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
    print("REPORT",a.output,"QUESTIONS",len(result["questions"]))

if __name__=="__main__":main()
