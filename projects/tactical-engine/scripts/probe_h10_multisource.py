#!/usr/bin/env python3
"""H10 exploratory cross-document answer test. No Chroma writes, no expected claims in prompts."""
import argparse,datetime,hashlib,json,sys,time
from pathlib import Path
from compare_h09_generation_focus_ab import generate

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pilot",type=Path,default=Path(__file__).resolve().parents[1]/"evaluation/h10_multisource_football_pilot.json")
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--timeout",type=int,default=300)
    args=p.parse_args()
    if args.pilot.resolve()==args.output.resolve():p.error("Output must not overwrite pilot")
    data=json.loads(args.pilot.read_text(encoding="utf-8"))
    evidence={r["id"]:r for r in data["evidence"]}
    if len(evidence)!=len(data["evidence"]):p.error("Duplicate evidence IDs")
    rows=[]
    for case in data["cases"]:
        if not case["evidence_ids"] or any(i not in evidence for i in case["evidence_ids"]):p.error("Unknown evidence ID")
        context=[{"figure_id":i,"text":"Fonte "+evidence[i]["source_id"]+": "+evidence[i]["text"]} for i in case["evidence_ids"]]
        t=time.monotonic()
        response=generate(case["query"],context,args.ollama_url,args.model,args.timeout)
        rows.append({"case_id":case["id"],"query":case["query"],"evidence_ids":case["evidence_ids"],
                     "response":response,"generation_seconds":round(time.monotonic()-t,3)})
        print("CASE",len(rows),"/",len(data["cases"]),"done",flush=True)
    report={"experiment":"h10_cross_document_pilot","timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "pilot_sha256":hashlib.sha256(args.pilot.read_bytes()).hexdigest(),
            "model":args.model,"parameters":{"think":False,"temperature":0.1,"num_ctx":8192},
            "rows":rows,"limitations":"Manual review required; curated development cases, no holdout; ID validity is not semantic fidelity. Evidence not retrieved automatically."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("REPORT",args.output,"VALID_IDS",sum(r["response"]["citations_valid_ids"] for r in rows),"/",len(rows),flush=True)
if __name__=="__main__":main()
