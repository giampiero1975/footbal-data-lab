#!/usr/bin/env python3
"""Reversible H09 generation A/B using exactly the saved baseline contexts; V4 untouched."""
import argparse, datetime, hashlib, json, re, time, urllib.request
from pathlib import Path

DOCS=["https://docs.ollama.com/api/chat","https://docs.ollama.com/capabilities/structured-outputs"]
SCHEMA={"type":"object","properties":{"answer":{"type":"string"},"citations":{"type":"array","items":{"type":"string"}},"insufficient_evidence":{"type":"boolean"}},"required":["answer","citations","insufficient_evidence"]}
def normalize_id(value):
    if not isinstance(value,str):return None
    match=re.fullmatch(r"\s*(?:(?:FIGURA|FIG\.)\s*)?(\d+(?:/[a-z])?)\s*",value,re.I)
    return match.group(1).lower() if match else None

def validate_citations(citations, context):
    allowed={normalize_id(r["figure_id"]) for r in context}
    normalized=[normalize_id(c) for c in citations]
    return bool(normalized) and all(c is not None and c in allowed for c in normalized),normalized

def generate(question,context,url,model,timeout):
    passages="\n\n".join("[FIGURA "+r["figure_id"]+"] "+r["text"] for r in context)
    prompt=("Sei un analista tattico che risponde soltanto sulla base dei brani riportati. "
            "Prima identifica la condizione esatta della domanda (zona del campo, fase di gioco, possessore e reparti coinvolti). "
            "Usa SOLO i brani che descrivono la medesima condizione: non aggiungere movimenti da altri scenari "
            "anche se tatticamente plausibili o presenti in altre figure. "
            "Riporta tutte le informazioni pertinenti della fonte principale, inclusi appoggi e ruoli; "
            "non generalizzare regole valide solo in altri scenari. "
            "Se la condizione richiesta non è documentata, dichiara insufficienza di evidenze. "
            "In citations inserisci soltanto gli identificativi esatti (esempio: 15/a, non FIGURA 15/a) "
            "dei brani effettivamente usati. Non citare brani esclusi. Rispondi nel formato JSON richiesto.\n"
            "DOMANDA: "+question+"\nBRANI:\n"+passages)
    payload={"model":model,"stream":False,"think":False,"format":SCHEMA,
             "options":{"temperature":0.1,"num_ctx":8192},
             "messages":[{"role":"user","content":prompt}]}
    req=urllib.request.Request(url.rstrip("/")+"/api/chat",
          data=json.dumps(payload,ensure_ascii=False).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:raw=json.load(response)
    result=json.loads(raw["message"]["content"])
    if not isinstance(result.get("answer"),str) or not isinstance(result.get("citations"),list) or not isinstance(result.get("insufficient_evidence"),bool):
        raise ValueError("Invalid structured response")
    valid,normalized=validate_citations(result["citations"],context)
    return {"response":result,"citation_ids_normalized":normalized,"citations_valid_ids":valid,
            "ollama_metrics":{k:raw.get(k) for k in ("total_duration","prompt_eval_count","eval_count","done_reason")}}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--baseline",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--timeout",type=int,default=300)
    args=p.parse_args()
    if args.output.resolve()==args.baseline.resolve():p.error("Do not overwrite baseline")
    source=json.loads(args.baseline.read_text(encoding="utf-8"))
    rows=[]
    for row in source["rows"]:
        t0=time.monotonic()
        result=generate(row["query"],row["context"],args.ollama_url,args.model,args.timeout)
        baseline_valid,baseline_ids=validate_citations(row["response"]["citations"],row["context"])
        rows.append({"query":row["query"],"context":row["context"],
                     "baseline":{"response":row["response"],"citations_valid_after_normalization":baseline_valid,
                                 "citation_ids_normalized":baseline_ids},
                     "candidate":result,"candidate_generation_seconds":round(time.monotonic()-t0,3)})
        print("CASE",len(rows),"/",len(source["rows"]),"done",flush=True)
    report={"experiment":"h09_condition_focused_prompt_ab","timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "baseline_sha256":hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
            "baseline_git_commit":source.get("git_commit"),"evidence_sha256":source.get("evidence_sha256"),
            "model":args.model,"config":{"think":False,"temperature":0.1,"num_ctx":8192,"identical_contexts":True},
            "official_documentation":DOCS,"rows":rows,
            "limitations":"Development only, no holdout. Valid citation identifiers do not prove claims are supported; manual tactical audit required."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("REPORT",args.output,"VALID_IDS",sum(r["candidate"]["citations_valid_ids"] for r in rows),"/",len(rows),flush=True)
if __name__=="__main__":main()
