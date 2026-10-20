#!/usr/bin/env python3
"""Read-only assessment of already generated DRIBBLING V4 answers.

Native Ollama structured JSON: https://docs.ollama.com/capabilities/structured-outputs
Thinking: https://docs.ollama.com/capabilities/thinking
No Chroma access, no answer regeneration, no new Python dependencies.
"""
import argparse,json,re,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from benchmark_metro_tattico_no_think_v1 import call
REF=re.compile(r"\[(?:GLEREAN-C\d{3}|\d+)\]")
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--input",type=Path,default=ROOT/"confronto_risposte_v4_prompt_v2.json")
 p.add_argument("--output",type=Path,default=ROOT/"valutazione_risposte_reali_v4_v1.json")
 p.add_argument("--model",default="qwen3.5:9b")
 p.add_argument("--timeout",type=int,default=240)
 a=p.parse_args()
 if a.output.exists():raise FileExistsError("Output esistente: non sovrascrivo")
 data=json.loads(a.input.read_text(encoding="utf-8"))
 if len(data["runs"])!=6:raise ValueError("Attese 6 coppie di risposte")
 report={"schema_version":1,"method":"gold_claim_vs_existing_real_answers_native_ollama_no_think",
  "model":a.model,"input":str(a.input),"results":[],"limitations":[
  "Il judge confronta la risposta con ciascun claim gold e relativa evidenza; non valuta ogni affermazione aggiuntiva",
  "La copertura del judge misura i nuclei del singolo claim, non la completezza dell'intera domanda",
  "Le etichette sono automatiche, non verita' a terra; gold preliminare",
  "Le citazioni sono controllate sintatticamente, non per supporto semantico",
  "Nessun accesso a Chroma e nessuna rigenerazione delle risposte"] }
 for run in data["runs"]:
  allowed=set(run["allowed_refs"])
  # Le pagine tra parentesi quadre non sono ID di citazione: la verifica
  # sintattica e' solo un segnale diagnostico e va interpretata manualmente.
  for variant,key in (("baseline","baseline_answer"),("prompt_v2","answer_raw")):
   answer=run[key]
   row={"case_id":run["case_id"],"mode":run["mode"],"variant":variant,
        "claim_results":[],"answer":answer}
   ids=REF.findall(answer)
   row["unknown_bracket_tokens"]=sorted(set(ids)-allowed)
   for claim in run["gold_claims"]:
    t=time.monotonic()
    try:
     pred,meta=call(a.model,claim["evidence"],answer,a.timeout)
     row["claim_results"].append({"claim_id":claim["id"],"claim":claim["claim"],
       "fidelity":pred["fidelity"],"coverage":pred["coverage"],
       "elapsed_seconds":round(time.monotonic()-t,2),"meta":meta})
    except Exception as exc:
     row["claim_results"].append({"claim_id":claim["id"],
       "error":f"{type(exc).__name__}: {exc}"})
   report["results"].append(row)
   a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
   counts={}
   for c in row["claim_results"]:
    k=(c.get("fidelity","error"),c.get("coverage","error"))
    counts[str(k)]=counts.get(str(k),0)+1
   print(f'{row["case_id"]} {row["mode"]} {variant}: {counts}',flush=True)
 print("REPORT",a.output,flush=True)
if __name__=="__main__":main()
