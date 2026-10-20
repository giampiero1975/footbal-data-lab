#!/usr/bin/env python3
"""H09 isolated answer-generation probe; NO V4 writes; manual semantic audit required."""
import argparse, datetime, hashlib, json, subprocess, time, urllib.request
from pathlib import Path
from compare_h09_dense_bm25 import embed, cosine
from evaluate_h09_lexical import CASES

RERANKER = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
SCHEMA = {"type":"object","properties":{
 "answer":{"type":"string"},"citations":{"type":"array","items":{"type":"string"}},
 "insufficient_evidence":{"type":"boolean"}},"required":["answer","citations","insufficient_evidence"]}
DOCS = ["https://docs.ollama.com/api/chat",
        "https://docs.ollama.com/capabilities/structured-outputs",
        "https://docs.ollama.com/api/embed",
        "https://sbert.net/docs/package_reference/cross_encoder/model.html"]

def chat(url, model, question, selected, timeout):
    passages = "\n\n".join("[FIGURA "+r["figure_id"]+"] "+r["text"] for r in selected)
    prompt = ("Rispondi in italiano esclusivamente usando i brani forniti. "
              "Distingui ruoli, fase di gioco, condizioni e movimenti senza inventare. "
              "Se le prove sono insufficienti, dichiaralo e non colmare lacune. "
              "Il campo citations deve contenere soltanto ID figura presenti nei brani "
              "e realmente pertinenti. Rispondi con JSON conforme allo schema.\n"
              "DOMANDA: "+question+"\nEVIDENZE:\n"+passages)
    payload = {"model":model,"stream":False,"think":False,"format":SCHEMA,
               "options":{"temperature":0.1,"num_ctx":8192},
               "messages":[{"role":"user","content":prompt}]}
    req = urllib.request.Request(url.rstrip("/")+"/api/chat",
          data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
          headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        raw = json.load(response)
    result = json.loads(raw["message"]["content"])
    if not isinstance(result,dict) or not isinstance(result.get("answer"),str) or not isinstance(result.get("citations"),list) or not isinstance(result.get("insufficient_evidence"),bool):
        raise ValueError("Unexpected response JSON shape")
    allowed = {r["figure_id"] for r in selected}
    valid = all(isinstance(c,str) and c in allowed for c in result["citations"])
    return {"response":result,"citations_valid_ids":valid,
            "ollama_metrics":{k:raw.get(k) for k in ("total_duration","load_duration","prompt_eval_count","eval_count","done_reason")}}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence",type=Path,required=True)
    p.add_argument("--cases",type=Path)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--top-n",type=int,default=15)
    p.add_argument("--top-k",type=int,default=5)
    p.add_argument("--timeout",type=int,default=300)
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    args=p.parse_args()
    if min(args.top_n,args.top_k,args.timeout)<1:p.error("top-n, top-k, timeout must be positive")
    if args.output.resolve()==args.evidence.resolve():p.error("output cannot overwrite evidence")
    records=json.loads(args.evidence.read_text(encoding="utf-8"))["records"]
    cases=json.loads(args.cases.read_text(encoding="utf-8")) if args.cases else CASES
    if not records or not cases:p.error("evidence and cases must be nonempty")
    from sentence_transformers import CrossEncoder
    reranker=CrossEncoder(RERANKER,device="cpu",max_length=512)
    started=time.monotonic()
    vectors=embed([r["text"] for r in records],args.ollama_url,"qwen3-embedding:0.6b",4,120)
    qvectors=embed([c["query"] for c in cases],args.ollama_url,"qwen3-embedding:0.6b",4,120)
    rows=[]
    for case,qvec in zip(cases,qvectors):
        dense=sorted(zip([cosine(qvec,v) for v in vectors],records),
                     key=lambda x:(-x[0],str(x[1].get("id",""))))[:args.top_n]
        scores=reranker.predict([(case["query"],r["text"]) for _,r in dense],
                                batch_size=1,show_progress_bar=False)
        ordered=sorted(zip(scores,dense),key=lambda x:(-float(x[0]),str(x[1][1].get("id",""))))
        selected=[x[1][1] for x in ordered[:args.top_k]]
        t0=time.monotonic()
        answer=chat(args.ollama_url,"qwen3.5:9b",case["query"],selected,args.timeout)
        rows.append({"query":case["query"],"expected_figure_id_for_retrieval_only":case.get("expected_figure_id"),
                     "context":[{"figure_id":r["figure_id"],"text":r["text"]} for r in selected],
                     "generation_seconds":round(time.monotonic()-t0,3),**answer})
        print("CASE",len(rows),"/",len(cases),"generated",flush=True)
    try:
        commit=subprocess.run(["git","rev-parse","HEAD"],check=True,capture_output=True,text=True,timeout=5).stdout.strip()
    except (OSError,subprocess.SubprocessError):commit=None
    report={"experiment":"h09_grounded_generation_dev","timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "git_commit":commit,"evidence_sha256":hashlib.sha256(args.evidence.read_bytes()).hexdigest(),
            "cases_sha256":hashlib.sha256(args.cases.read_bytes()).hexdigest() if args.cases else None,
            "models":{"embedding":"qwen3-embedding:0.6b","reranker":RERANKER,"generation":"qwen3.5:9b"},
            "config":{"top_n":args.top_n,"top_k":args.top_k,"reranker_max_length":512,"think":False,"temperature":0.1,"num_ctx":8192},
            "official_documentation":DOCS,"elapsed_seconds":round(time.monotonic()-started,3),
            "rows":rows,"limitations":"Development cases, figure paragraphs only. Citation-ID validation is NOT semantic fidelity; manual claim-by-claim audit and holdout required."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("REPORT",args.output,"CASES",len(rows),"VALID_IDS",sum(r["citations_valid_ids"] for r in rows),flush=True)

if __name__=="__main__":main()
