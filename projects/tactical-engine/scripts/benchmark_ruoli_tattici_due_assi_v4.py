#!/usr/bin/env python3
"""Test offline a due assi: relazioni reparto-azione e completezza.

Usa il corpus sintetico del benchmark precedente; conserva i report storici.
Non accede a Chroma, non modifica risposte e non applica correzioni.
API: https://docs.ollama.com/capabilities/structured-outputs
"""
import argparse,json,time,urllib.request
from pathlib import Path

SOURCE=("Gestione della palla da parte dei difensori e centrocampisti con gli "
"attaccanti che si mettono nella condizione di ricevere palla negli spazi "
"laterali e centrali e in linea con i difensori avversari.")
CASES=[
("T01","coerente","completo","Difensori e centrocampisti gestiscono la palla mentre gli attaccanti si preparano a riceverla negli spazi laterali e centrali sulla linea dei difensori avversari."),
("T02","contraddittorio","completo","Gli attaccanti gestiscono la palla mentre difensori e centrocampisti si preparano a riceverla negli spazi laterali e centrali sulla linea dei difensori avversari."),
("T03","contraddittorio","parziale","Attaccanti, difensori e centrocampisti si posizionano tutti per ricevere palla negli spazi laterali e centrali, allineati ai difensori avversari."),
("T04","contraddittorio","parziale","I difensori si posizionano sulla linea dei difensori avversari per ricevere palla, mentre gli attaccanti la gestiscono."),
("T05","contraddittorio","parziale","Gli attaccanti devono rimanere fermi e non cercare gli spazi laterali e centrali per ricevere palla."),
("T06","contraddittorio","parziale","Gli attaccanti si preparano a ricevere esclusivamente nella propria area di rigore e mai negli spazi laterali e centrali."),
("T07","coerente","completo","I giocatori di difesa e centrocampo possono amministrare il possesso, consentendo agli attaccanti di rendersi disponibili tra le linee laterali e centrali, in corrispondenza della linea difensiva avversaria."),
("T08","coerente","parziale","Gli attaccanti cercano spazi per ricevere palla."),
("T09","coerente","parziale","La gestione del pallone compete a difensori e centrocampisti; gli attaccanti cercano posizioni utili alla ricezione vicino alla linea avversaria."),
("T10","contraddittorio","parziale","La ricezione sulla linea difensiva avversaria è un compito esclusivo dei centrocampisti, non degli attaccanti."),
]
REL={"type":"object","properties":{"reparto":{"type":"string"},
"azione":{"type":"string"},"spazio":{"type":"string"}},"required":["reparto","azione","spazio"],
"additionalProperties":False}
SCHEMA={"type":"object","properties":{
"source_relations":{"type":"array","items":REL},
"statement_relations":{"type":"array","items":REL},
"fidelity":{"type":"string","enum":["coerente","contraddittorio","evidenza_insufficiente"]},
"completeness":{"type":"string","enum":["completo","parziale"]},
"reason":{"type":"string"}},
"required":["source_relations","statement_relations","fidelity","completeness","reason"],
"additionalProperties":False}

def ask(model,statement,timeout):
    prompt=("Sei un revisore tattico. PRIMA estrai separatamente le relazioni "
    "reparto-azione-spazio dalla FONTE e dalla AFFERMAZIONE. Ogni reparto va "
    "associato solo alle azioni attribuitegli dalla frase: non propagare "
    "l'azione di un reparto agli altri solo perche' tutti sono nominati. "
    "POI confronta le relazioni. fidelity=contraddittorio se la frase assegna "
    "a un reparto l'azione che la fonte attribuisce a un altro, la nega o "
    "inverte i compiti; coerente se compatibile; evidenza_insufficiente se "
    "non decidibile. completeness=parziale se manca almeno un dettaglio "
    "della fonte, anche se fidelity e' coerente. Un'affermazione breve "
    "puo' essere coerente E parziale. Restituisci JSON.\nFONTE:\n"+
    SOURCE+"\nAFFERMAZIONE:\n"+statement)
    payload={"model":model,"stream":False,"think":False,
             "messages":[{"role":"user","content":prompt}],
             "format":SCHEMA,"options":{"temperature":0,"num_ctx":4096}}
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat",
      data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    start=time.monotonic()
    with urllib.request.urlopen(req,timeout=timeout) as response:
        raw=json.load(response)
    result=json.loads(raw["message"]["content"])
    if result["fidelity"] not in ("coerente","contraddittorio","evidenza_insufficiente"):
        raise ValueError("fidelity non valida")
    if result["completeness"] not in ("completo","parziale"):
        raise ValueError("completeness non valida")
    return result,round(time.monotonic()-start,1)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--model",default="qwen3.5:9b")
    parser.add_argument("--timeout",type=int,default=900)
    parser.add_argument("--output",type=Path,default=Path(
      "projects/tactical-engine/benchmark_ruoli_tattici_due_assi_v4.json"))
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError(f"Report gia' presente: {args.output}")
    report={"schema_version":1,"method":"role_action_then_two_axis_judgment",
            "model":args.model,"source_ref":"GLEREAN-C018","source_text":SOURCE,
            "notes":["Etichette definite prima dell'esecuzione",
            "Le etichette di completezza sono esplorative e richiedono revisione umana",
            "Dieci casi sintetici, una sola fonte; nessuna misura globale del RAG"],
            "results":[]}
    for id_,fidelity,completeness,statement in CASES:
        entry={"id":id_,"statement":statement,"expected_fidelity":fidelity,
               "expected_completeness":completeness}
        try:
            pred,seconds=ask(args.model,statement,args.timeout)
            entry.update(predicted=pred,seconds=seconds,
              fidelity_match=pred["fidelity"]==fidelity,
              completeness_match=pred["completeness"]==completeness)
            print(f'{id_}: fedelta={pred["fidelity"]} '
                  f'({fidelity}) {"OK" if entry["fidelity_match"] else "ERRORE"}; '
                  f'completezza={pred["completeness"]} ({completeness}) '
                  f'{"OK" if entry["completeness_match"] else "ERRORE"}',flush=True)
        except Exception as exc:
            entry["error"]=str(exc)
            print(f'{id_}: ERRORE TECNICO {exc}',flush=True)
        report["results"].append(entry)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",
                               encoding="utf-8")
    completed=[x for x in report["results"] if "fidelity_match" in x]
    print(f'REPORT: {args.output} | fedelta='
          f'{sum(x["fidelity_match"] for x in completed)}/{len(completed)} '
          f'completezza={sum(x["completeness_match"] for x in completed)}/{len(completed)}',
          flush=True)
if __name__=="__main__":main()
