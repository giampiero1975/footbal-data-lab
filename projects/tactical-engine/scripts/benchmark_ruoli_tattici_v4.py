#!/usr/bin/env python3
"""Test avversariale isolato di attribuzione tattica, senza accesso a Chroma.

Fonte: GLEREAN-C018, principio 4 (ricerca dell'uno contro uno).
L'LLM giudice riceve il fatto di riferimento e UNA variante per volta.
API ufficiale: https://docs.ollama.com/capabilities/structured-outputs
"""
import argparse
import json
import time
import urllib.request
from pathlib import Path

SOURCE = ("Gestione della palla da parte dei difensori e centrocampisti "
          "con gli attaccanti che si mettono nella condizione di ricevere "
          "palla negli spazi laterali e centrali e in linea con i difensori avversari.")
CASES = [
    {"id":"T01","dimension":"controllo","expected":"coerente",
     "statement":"Difensori e centrocampisti gestiscono la palla mentre gli attaccanti si preparano a riceverla negli spazi laterali e centrali sulla linea dei difensori avversari."},
    {"id":"T02","dimension":"reparto","expected":"contraddizione",
     "statement":"Gli attaccanti gestiscono la palla mentre difensori e centrocampisti si preparano a riceverla negli spazi laterali e centrali sulla linea dei difensori avversari."},
    {"id":"T03","dimension":"reparto","expected":"contraddizione",
     "statement":"Attaccanti, difensori e centrocampisti si posizionano tutti per ricevere palla negli spazi laterali e centrali, allineati ai difensori avversari."},
    {"id":"T04","dimension":"reparto","expected":"contraddizione",
     "statement":"I difensori si posizionano sulla linea dei difensori avversari per ricevere palla, mentre gli attaccanti la gestiscono."},
    {"id":"T05","dimension":"movimento","expected":"contraddizione",
     "statement":"Gli attaccanti devono rimanere fermi e non cercare gli spazi laterali e centrali per ricevere palla."},
    {"id":"T06","dimension":"spazio","expected":"contraddizione",
     "statement":"Gli attaccanti si preparano a ricevere esclusivamente nella propria area di rigore e mai negli spazi laterali e centrali."},
    {"id":"T07","dimension":"controllo","expected":"coerente",
     "statement":"I giocatori di difesa e centrocampo possono amministrare il possesso, consentendo agli attaccanti di rendersi disponibili tra le linee laterali e centrali, in corrispondenza della linea difensiva avversaria."},
    {"id":"T08","dimension":"omissione","expected":"non_determinabile",
     "statement":"Gli attaccanti cercano spazi per ricevere palla."},
    {"id":"T09","dimension":"controllo","expected":"coerente",
     "statement":"La gestione del pallone compete a difensori e centrocampisti; gli attaccanti cercano posizioni utili alla ricezione vicino alla linea avversaria."},
    {"id":"T10","dimension":"reparto","expected":"contraddizione",
     "statement":"La ricezione sulla linea difensiva avversaria è un compito esclusivo dei centrocampisti, non degli attaccanti."},
]
LABELS=["coerente","contraddizione","non_determinabile"]
SCHEMA={"type":"object","properties":{"verdict":{"type":"string","enum":LABELS},
 "dimension":{"type":"string"},"reason":{"type":"string"}},
 "required":["verdict","dimension","reason"],"additionalProperties":False}

def ask(model, statement, timeout):
    prompt=("Sei un verificatore di fedelta' tattica. Confronta UNA affermazione con "
       "il brano fonte. Valuta reparto/soggetto, azione, spazio e condizioni. "
       "coerente=compatibile con la fonte, anche se parafrasata; "
       "contraddizione=altera o nega un ruolo, un movimento o una zona attribuiti "
       "esplicitamente dalla fonte; non_determinabile=affermazione troppo generica "
       "per stabilire tutti i dettagli, ma senza contraddizione esplicita. "
       "Non considerare coerente una frase solo per parole in comune. "
       "Restituisci un solo JSON.\nFONTE:\n"+SOURCE+
       "\nAFFERMAZIONE:\n"+statement)
    payload={"model":model,"stream":False,"think":False,
             "messages":[{"role":"user","content":prompt}],
             "format":SCHEMA,"options":{"temperature":0,"num_ctx":4096}}
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat",
      data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    start=time.monotonic()
    with urllib.request.urlopen(req,timeout=timeout) as response:
        result=json.load(response)
    parsed=json.loads(result["message"]["content"])
    if parsed["verdict"] not in LABELS: raise ValueError("Verdetto non valido")
    return parsed,round(time.monotonic()-start,1)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--model",default="qwen3.5:9b")
    parser.add_argument("--timeout",type=int,default=900)
    parser.add_argument("--output",type=Path,
        default=Path("projects/tactical-engine/benchmark_ruoli_tattici_v4.json"))
    args=parser.parse_args()
    if args.output.exists(): raise FileExistsError(f"Non sovrascrivo: {args.output}")
    report={"schema_version":1,"source_ref":"GLEREAN-C018","source_text":SOURCE,
            "model":args.model,"method":"adversarial_single_statement_v1",
            "limitations":["Dieci casi sintetici su una sola fonte",
                           "Il giudice vede la fonte; questo non misura il recupero RAG",
                           "La classificazione attesa e' definita prima del test"],
            "results":[]}
    for item in CASES:
        entry=dict(item)
        try:
            entry["predicted"],entry["seconds"]=ask(args.model,item["statement"],args.timeout)
            entry["match"]=entry["predicted"]["verdict"]==item["expected"]
            print(f'{item["id"]}: {entry["predicted"]["verdict"]} '
                  f'(atteso {item["expected"]}) '
                  f'{"OK" if entry["match"] else "ERRORE"}',flush=True)
        except Exception as exc:
            entry["error"]=str(exc)
            print(f'{item["id"]}: ERRORE TECNICO {exc}',flush=True)
        report["results"].append(entry)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    completed=[x for x in report["results"] if "match" in x]
    print(f'REPORT: {args.output} | accordo='
          f'{sum(x["match"] for x in completed)}/{len(completed)}',flush=True)

if __name__=="__main__":main()
