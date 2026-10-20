#!/usr/bin/env python3
"""H10 focused multi-source prompt A/B using saved evidence; preserves prior report and V4."""
import argparse,datetime,hashlib,json,time,urllib.request
from pathlib import Path
from compare_h09_generation_focus_ab import SCHEMA

def generate(question,context,url,model,timeout):
    passages="\n\n".join("[EVIDENZA "+r["id"]+" | "+r["source"]+" | "+r["scenario"]+"] "+r["text"] for r in context)
    prompt=("Sei un analista di calcio. Spiega principi e movimenti nel loro contesto, non una scuola o un autore. "
            "Rispondi a TUTTE le parti della domanda. Distingui esplicitamente: "
            "(1) movimento specifico documentato, (2) condizioni e principi generali pertinenti "
            "ricavati da fonti diverse, (3) esempi relativi a situazioni diverse che NON vanno trasferiti. "
            "Integra informazioni complementari quando supportate; non attribuire a un autore "
            "i movimenti descritti da un altro e non trasformare principi generali in prescrizioni specifiche. "
            "Se non esistono prove sufficienti per una parte, dichiaralo. "
            "Non devi usare ogni fonte: cita solo quelle che supportano effettivamente le affermazioni. "
            "Usa come citazioni esclusivamente gli ID dopo EVIDENZA, esattamente come scritti. "
            "Rispondi in italiano nel JSON richiesto.\nDOMANDA: "+question+"\nFONTI:\n"+passages)
    payload={"model":model,"stream":False,"think":False,"format":SCHEMA,
             "options":{"temperature":0.1,"num_ctx":8192},
             "messages":[{"role":"user","content":prompt}]}
    req=urllib.request.Request(url.rstrip("/")+"/api/chat",
        data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:raw=json.load(response)
    result=json.loads(raw["message"]["content"])
    if not isinstance(result.get("answer"),str) or not isinstance(result.get("citations"),list) or not isinstance(result.get("insufficient_evidence"),bool):
        raise ValueError("Invalid structured response")
    allowed={r["id"] for r in context}
    valid=bool(result["citations"]) and all(isinstance(c,str) and c in allowed for c in result["citations"])
    return {"response":result,"citations_valid_ids":valid,
            "cited_sources":sorted({r["source"] for r in context if r["id"] in result["citations"]}),
            "ollama_metrics":{k:raw.get(k) for k in ("total_duration","prompt_eval_count","eval_count","done_reason")}}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pilot",type=Path,default=Path(__file__).resolve().parents[1]/"evaluation/h10_multisource_football_pilot.json")
    p.add_argument("--baseline",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--timeout",type=int,default=300)
    args=p.parse_args()
    if len({args.pilot.resolve(),args.baseline.resolve(),args.output.resolve()})!=3:p.error("Input and output paths must differ")
    pilot=json.loads(args.pilot.read_text(encoding="utf-8"))
    baseline=json.loads(args.baseline.read_text(encoding="utf-8"))
    if hashlib.sha256(args.pilot.read_bytes()).hexdigest()!=baseline["pilot_sha256"]:p.error("Pilot SHA does not match baseline")
    if baseline.get("model")!=args.model:p.error("Model mismatch")
    evidence={e["id"]:e for e in pilot["evidence"]}
    old={r["case_id"]:r for r in baseline["rows"]}
    rows=[]
    for case in pilot["cases"]:
        if case["id"] not in old or old[case["id"]]["evidence_ids"]!=case["evidence_ids"]:p.error("Baseline case mismatch")
        context=[{"id":i,"source":evidence[i]["source_id"],"scenario":evidence[i]["scenario"],"text":evidence[i]["text"]} for i in case["evidence_ids"]]
        t=time.monotonic()
        result=generate(case["query"],context,args.ollama_url,args.model,args.timeout)
        original=old[case["id"]]["response"]["response"]
        original_valid=bool(original["citations"]) and all(c in case["evidence_ids"] for c in original["citations"])
        rows.append({"case_id":case["id"],"query":case["query"],"evidence_ids":case["evidence_ids"],
                     "baseline":{"response":original,"citation_ids_valid":original_valid},
                     "candidate":result,"candidate_seconds":round(time.monotonic()-t,3)})
        print("CASE",len(rows),"/",len(pilot["cases"]),"done",flush=True)
    report={"experiment":"h10_multisource_prompt_ab","timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "pilot_sha256":baseline["pilot_sha256"],"baseline_sha256":hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
            "model":args.model,"parameters":{"think":False,"temperature":0.1,"num_ctx":8192},
            "rows":rows,"limitations":"Prompt and presentation labels change, same evidence/cases/model. Exploratory, manual semantic review required; no holdout."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("REPORT",args.output,"VALID_IDS",sum(r["candidate"]["citations_valid_ids"] for r in rows),"/",len(rows),flush=True)
if __name__=="__main__":main()
