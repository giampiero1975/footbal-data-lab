#!/usr/bin/env python3
"""Offline H10 report audit; source-ID membership and explicit development-claim coverage."""
import argparse,json
from pathlib import Path

def audit(pilot,report):
    evidence={e["id"]:e for e in pilot["evidence"]}
    cases={c["id"]:c for c in pilot["cases"]}
    results=[]
    for row in report["rows"]:
        case=cases[row["case_id"]]
        answer=row["response"]["response"]
        citations=answer["citations"]
        allowed=set(case["evidence_ids"])
        valid=bool(citations) and all(isinstance(c,str) and c in allowed for c in citations)
        results.append({"case_id":row["case_id"],"citations":citations,"citation_ids_valid":valid,
                        "citation_sources":[evidence[c]["source_id"] for c in citations if c in evidence],
                        "distinct_cited_sources":len({evidence[c]["source_id"] for c in citations if c in evidence}),
                        "required_claims_for_manual_review":case["required_claims"],
                        "forbidden_for_manual_review":case["forbidden"],
                        "answer":answer["answer"]})
    return results

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pilot",type=Path,default=Path(__file__).resolve().parents[1]/"evaluation/h10_multisource_football_pilot.json")
    p.add_argument("--report",type=Path,required=True)
    args=p.parse_args()
    result=audit(json.loads(args.pilot.read_text(encoding="utf-8")),json.loads(args.report.read_text(encoding="utf-8")))
    print(json.dumps({"valid_ids":sum(r["citation_ids_valid"] for r in result),"cases":len(result),"rows":result},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
