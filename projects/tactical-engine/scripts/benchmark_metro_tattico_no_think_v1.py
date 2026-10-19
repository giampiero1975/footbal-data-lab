#!/usr/bin/env python3
"""Operational tactical judge benchmark: native Ollama JSON, thinking off.
Measures agreement with frozen human-labeled synthetic holdout; not real RAG quality.
Official: https://docs.ollama.com/capabilities/thinking
https://docs.ollama.com/capabilities/structured-outputs
"""
import argparse,json,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from benchmark_holdout_glerean_v4 import TESTS
GOLD=ROOT/"evaluation/gold_glerean_principi_v1.json"
SCHEMA={"type":"object","properties":{
 "fidelity":{"type":"string","enum":["coerente","contraddittorio","evidenza_insufficiente"]},
 "coverage":{"type":"string","enum":["completo","parziale"]}},
 "required":["fidelity","coverage"],"additionalProperties":False}
PROMPT=("Sei un verificatore di affermazioni tattiche. Confronta esclusivamente la FRASE con la FONTE. "
"Fedelta': 'coerente' se la FRASE e' supportata dalla FONTE, 'contraddittorio' se nega o "
"inverte ruoli, azioni o condizioni, 'evidenza_insufficiente' se la fonte non permette di stabilirlo. "
"Copertura: 'completo' se la FRASE tratta TUTTI i nuclei (soggetti, azioni, condizioni) "
"anche con significato invertito; 'parziale' se ne omette almeno uno. "
"Le due dimensioni sono indipendenti: una frase puo' essere contraddittoria ma completa. "
"Accetta sinonimi, non usare conoscenze esterne. Rispondi SOLO nel JSON richiesto.\n"
"FONTE:\n{source}\nFRASE:\n{statement}")
def call(model,source,statement,timeout):
    payload={"model":model,"stream":False,"think":False,
       "messages":[{"role":"user","content":PROMPT.format(source=source,statement=statement)}],
       "format":SCHEMA,"options":{"temperature":0,"num_ctx":4096,"num_predict":160}}
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat",
       data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
       headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response: raw=json.load(response)
    if raw.get("done_reason")!="stop":raise RuntimeError(f"generation not completed: {raw.get('done_reason')}")
    pred=json.loads(raw["message"]["content"])
    if pred["fidelity"] not in SCHEMA["properties"]["fidelity"]["enum"] or pred["coverage"] not in SCHEMA["properties"]["coverage"]["enum"]:
        raise ValueError("Unexpected judge labels")
    return pred,{"done_reason":raw.get("done_reason"),"eval_count":raw.get("eval_count"),
                 "prompt_eval_count":raw.get("prompt_eval_count")}
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--model",default="qwen3.5:9b")
    parser.add_argument("--timeout",type=int,default=240)
    parser.add_argument("--output",type=Path,default=ROOT/"benchmark_metro_tattico_no_think_v1.json")
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError(f"Non sovrascrivo {args.output}")
    gold=json.loads(GOLD.read_text(encoding="utf-8"))
    claims={c["id"]:c for group in gold["cases"] for c in group["gold_claims"]}
    report={"schema_version":1,"method":"native_ollama_structured_json_no_think",
            "framework":"custom_judge_not_ragas","model":args.model,
            "gold_source":"evaluation/gold_glerean_principi_v1.json",
            "cases":len(TESTS),"results":[],
            "limitations":["Misura accordo con etichette holdout preliminari, NON la qualita' delle risposte DRIBBLING",
                           "12 frasi sintetiche; non misura retrieval o qualita' delle citazioni",
                           "I gold P2 e V3 contengono ellissi, figure non verificate",
                           "Fedelta' e copertura sono metriche distinte; no score complessivo di produzione"]}
    started=time.monotonic()
    for case in TESTS:
        row={"id":case["id"],"claim":case["claim"],
             "expected_fidelity":case["expected_fidelity"],"expected_coverage":case["expected_coverage"]}
        tick=time.monotonic()
        try:
            pred,meta=call(args.model,claims[case["claim"]]["evidence"],case["statement"],args.timeout)
            row.update(predicted=pred,meta=meta,
                       fidelity_match=pred["fidelity"]==case["expected_fidelity"],
                       coverage_match=pred["coverage"]==case["expected_coverage"])
            print(f'{case["id"]}: fidelity={"OK" if row["fidelity_match"] else "FAIL"} coverage={"OK" if row["coverage_match"] else "FAIL"}',flush=True)
        except Exception as exc:
            row["error"]=f"{type(exc).__name__}: {exc}"
            print(f'{case["id"]}: TECHNICAL_ERROR {row["error"]}',flush=True)
        row["elapsed_seconds"]=round(time.monotonic()-tick,2)
        report["results"].append(row)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    valid=[r for r in report["results"] if "fidelity_match" in r]
    report["summary"]={"processed":len(valid),"total":len(TESTS),
      "fidelity_correct":sum(r["fidelity_match"] for r in valid),
      "coverage_correct":sum(r["coverage_match"] for r in valid),
      "both_correct":sum(r["fidelity_match"] and r["coverage_match"] for r in valid),
      "technical_errors":len(TESTS)-len(valid),
      "fidelity_accuracy":round(sum(r["fidelity_match"] for r in valid)/len(valid),4) if valid else None,
      "coverage_accuracy":round(sum(r["coverage_match"] for r in valid)/len(valid),4) if valid else None,
      "both_accuracy":round(sum(r["fidelity_match"] and r["coverage_match"] for r in valid)/len(valid),4) if valid else None}
    report["elapsed_seconds"]=round(time.monotonic()-started,2)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("METRO_RESULT "+json.dumps(report["summary"],ensure_ascii=False),flush=True)
    print(f"REPORT {args.output}",flush=True)
if __name__=="__main__":main()
