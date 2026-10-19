#!/usr/bin/env python3
"""Benchmark offline di un verificatore semantico post-generazione.

Input: matrice con risposte e fonti gia' disponibili sulla VPS.
Non modifica risposte, Chroma o V4. Il giudice NON vede le etichette manuali.
Confronto ex-post con 20 etichette umane gia' revisionate.
API: https://docs.ollama.com/capabilities/structured-outputs
"""
import argparse
import json
import time
import urllib.request
from pathlib import Path

MANUAL={
 "POSSESSO-002":{"numeric":["supportato","omesso","parziale"],"stable":["supportato","parziale","supportato"]},
 "UNO-CONTRO-UNO-003":{"numeric":["parziale","supportato","parziale"],"stable":["parziale","supportato","contraddetto"]},
 "VERTICALITA-004":{"numeric":["supportato"]*4,"stable":["supportato"]*4},
}
LABELS=("supportato","parziale","omesso","contraddetto")
SCHEMA={"type":"object","properties":{"judgments":{"type":"array","items":{
 "type":"object","properties":{"id":{"type":"string"},
 "verdict":{"type":"string","enum":list(LABELS)},
 "reason":{"type":"string"},"answer_quote":{"type":"string"},
 "source_ref":{"type":"string"},"source_quote":{"type":"string"}},
 "required":["id","verdict","reason","answer_quote","source_ref","source_quote"],
 "additionalProperties":False}}},"required":["judgments"],"additionalProperties":False}

def request(prompt,model,timeout):
    payload={"model":model,"stream":False,"think":False,
             "messages":[{"role":"user","content":prompt}],
             "format":SCHEMA,"options":{"temperature":0,"num_ctx":8192}}
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat",
       data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as res:
        response=json.load(res)
    return json.loads(response["message"]["content"])

def evaluate(case,model,timeout):
    claims=[{"id":c["id"],"gold_claim":c["gold_claim"]} for c in case["claims"]]
    prompt=("Sei un revisore di fedelta' documentale calcistica. Valuta OGNI claim "
     "rispetto alla RISPOSTA e alle FONTI originali. Non usare conoscenze esterne. "
     "supportato=claim completo e corretto; parziale=solo parte del claim; "
     "omesso=claim assente; contraddetto=la risposta attribuisce un ruolo, "
     "movimento o zona incompatibile con il claim e la fonte. "
     "Una citazione esistente non basta. Riporta estratti ESATTI e brevi di "
     "risposta e fonte, oppure stringhe vuote se omesso. "
     "Usa esclusivamente gli ID dei claim elencati. Rispondi nel JSON richiesto.\n"
     "CLAIM:\n"+json.dumps(claims,ensure_ascii=False)+
     "\nRISPOSTA:\n"+case["answer"]+
     "\nFONTI:\n"+json.dumps(case["available_sources"],ensure_ascii=False))
    start=time.monotonic()
    parsed=request(prompt,model,timeout)
    elapsed=round(time.monotonic()-start,1)
    byid={j["id"]:j for j in parsed.get("judgments",[])}
    if set(byid)!={c["id"] for c in case["claims"]}:
        raise ValueError("Il modello non ha restituito esattamente gli ID richiesti")
    for j in byid.values():
        if j["verdict"] not in LABELS: raise ValueError("Etichetta non valida")
        if j["answer_quote"] and j["answer_quote"] not in case["answer"]:
            raise ValueError("Citazione risposta non letterale")
        if j["source_ref"] and j["source_ref"] not in case["available_sources"]:
            raise ValueError("Fonte inesistente")
        if j["source_quote"] and not (
            j["source_ref"] and j["source_quote"] in case["available_sources"][j["source_ref"]]["text"]):
            raise ValueError("Citazione fonte non letterale")
    return byid,elapsed

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input",type=Path)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--model",default="qwen3.5:9b")
    ap.add_argument("--timeout",type=int,default=900)
    args=ap.parse_args()
    data=json.loads(args.input.read_text(encoding="utf-8"))
    if len(data["cases"])!=6: raise ValueError("Attesi sei casi")
    output=args.output or args.input.with_name("benchmark_verificatore_semantico_v4.json")
    if output.exists(): raise FileExistsError(f"Non sovrascrivo {output}")
    report={"model":args.model,"method":"post_generation_semantic_judge",
      "notes":["Nessuna correzione automatica della risposta",
               "Giudice senza accesso alle etichette manuali",
               "Una sola valutazione per caso, nessuna significativita statistica"],
      "results":[]}
    for case in data["cases"]:
        suffix=case["case_id"].replace("GLEREAN-334-","")
        ids=[c["id"] for c in case["claims"]]
        expected=dict(zip(ids,MANUAL[suffix][case["mode"]]))
        try:
            judged,seconds=evaluate(case,args.model,args.timeout)
            record={"case_id":case["case_id"],"mode":case["mode"],
               "seconds":seconds,"judgments":[{"id":i,"predicted":judged[i],
                     "manual_reference":expected[i],
                     "match":judged[i]["verdict"]==expected[i]} for i in ids]}
            print(f'{case["case_id"]} {case["mode"]}: '
                  f'{sum(x["match"] for x in record["judgments"])}/{len(ids)} accordi, {seconds}s',flush=True)
        except Exception as exc:
            record={"case_id":case["case_id"],"mode":case["mode"],
                    "error":str(exc),"judgments":[]}
            print(f'{case["case_id"]} {case["mode"]}: ERRORE {exc}',flush=True)
        report["results"].append(record)
        output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    checked=[x for r in report["results"] for x in r["judgments"]]
    print(f'COMPLETATO: {output} | accordo={sum(x["match"] for x in checked)}/{len(checked)}; Chroma invariato')

if __name__=="__main__":main()
