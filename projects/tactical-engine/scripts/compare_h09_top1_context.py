#!/usr/bin/env python3
"""H09 controlled evidence ablation: top-1 vs top-5, same questions/model; no index writes."""
import argparse,datetime,hashlib,json,time
from pathlib import Path
from compare_h09_generation_focus_ab import generate

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--baseline",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--timeout",type=int,default=300)
    args=p.parse_args()
    if args.baseline.resolve()==args.output.resolve():p.error("Cannot overwrite baseline")
    source=json.loads(args.baseline.read_text(encoding="utf-8"))
    if not source.get("rows"):p.error("Missing cases")
    rows=[]
    for row in source["rows"]:
        ctx=row["context"]
        if not ctx:p.error("Missing context")
        start=time.monotonic()
        top1=generate(row["query"],ctx[:1],args.ollama_url,args.model,args.timeout)
        rows.append({"query":row["query"],"expected_figure_id_for_retrieval_only":row.get("expected_figure_id_for_retrieval_only"),
                     "top1_context":ctx[:1],"top5_context":ctx,
                     "top1":top1,"top1_generation_seconds":round(time.monotonic()-start,3),
                     "baseline_top5_response":row["response"]})
        print("CASE",len(rows),"/",len(source["rows"]),"top1 done",flush=True)
    report={"experiment":"h09_top1_vs_top5_context_ab","timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "baseline_sha256":hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
            "evidence_sha256":source.get("evidence_sha256"),"model":args.model,
            "configuration":{"think":False,"temperature":0.1,"num_ctx":8192,
                             "top1_prompt":"condition-focused","top5_prompt":"original baseline"},
            "rows":rows,
            "official_documentation":["https://docs.ollama.com/api/chat","https://docs.ollama.com/capabilities/structured-outputs"],
            "limitations":"Exploratory: context count AND prompt differ from original baseline. Compare against focused top5 report for prompt-matched analysis. Development cases only, no holdout."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("REPORT",args.output,"CASES",len(rows),flush=True)
if __name__=="__main__":main()
