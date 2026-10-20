#!/usr/bin/env python3
"""Audit delle risposte reali del benchmark V4: metriche deterministiche e giudice locale.
Input: benchmark_citazioni_stabili_v4.json (sei risposte gia' generate).
Non legge/scrive Chroma. Non sostituisce DeepEval/Ragas.
API ufficiali: https://docs.ollama.com/api/chat
https://docs.ollama.com/capabilities/structured-outputs
"""
import argparse,json,re,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA={"type":"object","properties":{"judgments":{"type":"array","items":{
"type":"object","properties":{"id":{"type":"string"},
"coverage":{"type":"string","enum":["presente","parziale","assente","contraddetto"]},
"reason":{"type":"string"}},"required":["id","coverage","reason"],"additionalProperties":False}}},
"required":["judgments"],"additionalProperties":False}
CIT=re.compile(r"\[(?:GLEREAN-C\d{3}|\d+)\]")
def evaluate_claims(answer,claims,model,timeout):
    prompt=("Valuta la RISPOSTA rispetto ai CLAIM del Gold, senza usare conoscenze esterne. "
    "Per ogni claim: presente=interamente espresso; parziale=solo alcuni nuclei; "
    "assente=non espresso; contraddetto=la risposta inverte o nega il claim. "
    "Non considerare presente un claim solo perche' vero nella fonte. "
    "Rispondi solo in JSON.\nCLAIM:\n"+
    json.dumps([{"id":c["id"],"claim":c["claim"]} for c in claims],ensure_ascii=False)+
    "\nRISPOSTA:\n"+answer)
    payload={"model":model,"stream":False,"think":False,
       "messages":[{"role":"user","content":prompt}],"format":SCHEMA,
       "options":{"temperature":0,"num_ctx":8192,"num_predict":768}}
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat",
      data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
      headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as resp:raw=json.load(resp)
    if raw.get("done_reason")!="stop":raise RuntimeError("LLM output incomplete")
    items=json.loads(raw["message"]["content"])["judgments"]
    ids=[c["id"] for c in claims]
    if len(items)!=len(ids) or set(x["id"] for x in items)!=set(ids):
        raise ValueError("Missing or duplicated claim IDs")
    return items
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=ROOT/"benchmark_citazioni_stabili_v4.json")
    p.add_argument("--output",type=Path,default=ROOT/"audit_risposte_reali_v4_no_think_v1.json")
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--timeout",type=int,default=300)
    a=p.parse_args()
    if a.output.exists():raise FileExistsError(f"Non sovrascrivo {a.output}")
    source=json.loads(a.input.read_text(encoding="utf-8"))
    if len(source.get("runs",[]))!=6:raise ValueError("Attese sei risposte reali V4")
    report={"schema_version":1,"input":str(a.input),"model":a.model,
      "method":"fixed_context_v4_answers_with_gold_claim_coverage_and_citation_checks",
      "framework":"custom_ollama_not_deepeval",
      "limitations":["Risposte generate con contesti TOP5 fissi, non misura retrieval end-to-end",
      "Le citazioni sono controllate per ID e presenza di testo; non prova supporto semantico",
      "Copertura giudicata dal modello, da validare su etichette umane",
      "Fedelta' alle fonti NON misurata automaticamente in questa versione",
      "Gold preliminare; figure non verificate"],"runs":[]}
    start=time.monotonic()
    for run in source["runs"]:
        refs={s["ref"]:s for s in run["sources"]}
        used=CIT.findall(run["answer"])
        valid=sorted(set(used)&set(refs))
        invalid=sorted(set(used)-set(refs))
        row={"case_id":run["case_id"],"mode":run["mode"],
             "used_citations":used,"valid_citations":valid,"invalid_citations":invalid,
             "citation_id_validity":round(len([x for x in used if x in refs])/len(used),4) if used else None,
             "gold_claim_count":len(run["gold_claims"])}
        try:
            judgments=evaluate_claims(run["answer"],run["gold_claims"],a.model,a.timeout)
            row["claim_judgments"]=judgments
            counts={v:sum(j["coverage"]==v for j in judgments) for v in ("presente","parziale","assente","contraddetto")}
            row["claim_counts"]=counts
            row["claim_full_coverage"]=round(counts["presente"]/len(judgments),4)
            row["status"]="ok"
            print(f'{run["case_id"]} {run["mode"]}: claim presenti={counts["presente"]}/{len(judgments)}, citazioni invalide={len(invalid)}',flush=True)
        except Exception as exc:
            row["status"]="error";row["error"]=f"{type(exc).__name__}: {exc}"
            print(f'{run["case_id"]} {run["mode"]}: ERROR {row["error"]}',flush=True)
        report["runs"].append(row)
        a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report["elapsed_seconds"]=round(time.monotonic()-start,2)
    ok=[r for r in report["runs"] if r["status"]=="ok"]
    report["summary"]={"evaluated_answers":len(ok),"total_answers":len(report["runs"]),
      "total_claims":sum(r["gold_claim_count"] for r in ok),
      "fully_covered_claims":sum(r["claim_counts"]["presente"] for r in ok),
      "invalid_citation_ids":sum(len(r["invalid_citations"]) for r in report["runs"]),
      "technical_errors":len(report["runs"])-len(ok)}
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("REAL_ANSWERS_RESULT "+json.dumps(report["summary"],ensure_ascii=False),flush=True)
    print(f"REPORT {a.output}",flush=True)
if __name__=="__main__":main()
