#!/usr/bin/env python3
"""Seconda prova isolata: verifica copertura risposta PRIMA delle fonti.

Il giudice riceve solo claim e risposta; le fonti non sono disponibili in
questa fase, per evitare la confusione tra verita' nel documento e presenza
nella risposta. Nessuna modifica a V4/Chroma. Risultati e output originali
restano intatti.
Documentazione API: https://docs.ollama.com/api/chat
"""
import argparse,json,time,urllib.request
from pathlib import Path
LABELS=("presente","parziale","assente","incompatibile")
SCHEMA={"type":"object","properties":{"judgments":{"type":"array","items":{
"type":"object","properties":{"id":{"type":"string"},
"verdict":{"type":"string","enum":list(LABELS)},
"reason":{"type":"string"}},"required":["id","verdict","reason"],
"additionalProperties":False}}},"required":["judgments"],"additionalProperties":False}
MANUAL={
"POSSESSO-002":{"numeric":["presente","assente","parziale"],"stable":["presente","parziale","presente"]},
"UNO-CONTRO-UNO-003":{"numeric":["parziale","presente","parziale"],"stable":["parziale","presente","incompatibile"]},
"VERTICALITA-004":{"numeric":["presente"]*4,"stable":["presente"]*4}}
def judge(case,model,timeout):
    claims=[{"id":c["id"],"claim":c["gold_claim"]} for c in case["claims"]]
    prompt=("Confronta SOLO i claim con la RISPOSTA, non con fonti o conoscenze esterne. "
      "Per ciascun claim: presente=contenuto interamente nella risposta; "
      "parziale=solo alcuni elementi; assente=non compare; "
      "incompatibile=la risposta dice qualcosa in contrasto con il claim "
      "(es. attribuisce a un altro reparto il movimento). "
      "Non dedurre che un claim sia presente solo perche' sarebbe vero. "
      "Motiva con parole tue, senza citazioni letterali. "
      "Restituisci tutti gli ID, una volta ciascuno.\nCLAIM:\n"+
      json.dumps(claims,ensure_ascii=False)+"\nRISPOSTA:\n"+case["answer"])
    payload={"model":model,"stream":False,"think":False,
      "messages":[{"role":"user","content":prompt}],"format":SCHEMA,
      "options":{"temperature":0,"num_ctx":8192}}
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat",
      data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    start=time.monotonic()
    with urllib.request.urlopen(req,timeout=timeout) as resp:
        raw=json.load(resp)
    parsed=json.loads(raw["message"]["content"])
    items=parsed["judgments"]
    expected_ids=[c["id"] for c in case["claims"]]
    if len(items)!=len(expected_ids) or set(j["id"] for j in items)!=set(expected_ids):
        raise ValueError("ID incompleti o duplicati")
    return {j["id"]:j for j in items},round(time.monotonic()-start,1)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input",type=Path)
    ap.add_argument("--model",default="qwen3.5:9b")
    ap.add_argument("--output",type=Path)
    ap.add_argument("--timeout",type=int,default=900)
    args=ap.parse_args()
    data=json.loads(args.input.read_text(encoding="utf-8"))
    if len(data["cases"])!=6: raise ValueError("Attese sei risposte")
    out=args.output or args.input.with_name("benchmark_verificatore_semantico_v4_bis.json")
    if out.exists(): raise FileExistsError(f"Non sovrascrivo {out}")
    report={"method":"answer_only_coverage_v2","model":args.model,
      "limitations":["Il giudice non controlla la veridicita' nelle fonti",
                     "Le etichette manuali sono riferimento di confronto, non verita' automatica",
                     "Una prova non stima la robustezza"],"results":[]}
    for case in data["cases"]:
        suffix=case["case_id"].removeprefix("GLEREAN-334-")
        ids=[c["id"] for c in case["claims"]]
        reference=dict(zip(ids,MANUAL[suffix][case["mode"]]))
        try:
            results,seconds=judge(case,args.model,args.timeout)
            items=[{"id":i,"predicted":results[i],
                    "manual_reference":reference[i],
                    "match":results[i]["verdict"]==reference[i]} for i in ids]
            record={"case_id":case["case_id"],"mode":case["mode"],
                    "seconds":seconds,"judgments":items}
            print(f'{case["case_id"]} {case["mode"]}: '
                  f'{sum(x["match"] for x in items)}/{len(items)} accordi; {seconds}s',flush=True)
        except Exception as exc:
            record={"case_id":case["case_id"],"mode":case["mode"],
                    "error":str(exc),"judgments":[]}
            print(f'{case["case_id"]} {case["mode"]}: ERRORE {exc}',flush=True)
        report["results"].append(record)
        out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    items=[j for r in report["results"] for j in r["judgments"]]
    print(f'REPORT: {out} | accordo={sum(j["match"] for j in items)}/{len(items)}',flush=True)
if __name__=="__main__":main()
