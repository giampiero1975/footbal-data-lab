#!/usr/bin/env python3
"""Holdout Glerean: fonti diverse, relazioni attese esplicite, due assi.

Nessun accesso a Chroma. Il set holdout non riutilizza i dieci testi T01-T10.
Fonti tratte dal gold_glerean_principi_v1.json nel repository.
Documentazione: https://docs.ollama.com/capabilities/structured-outputs
"""
import argparse,json,time,urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOLD=ROOT/"evaluation/gold_glerean_principi_v1.json"
# Etichette fissate prima del test. Completezza valuta gli slot essenziali
# del singolo principio, NON la somiglianza letterale.
TESTS=[
{"id":"H01","claim":"V1","expected_fidelity":"coerente","expected_coverage":"completo",
 "statement":"Per centrocampisti e attaccanti la verticalità è in avanti; per i difensori può essere all'indietro."},
{"id":"H02","claim":"V1","expected_fidelity":"contraddittorio","expected_coverage":"completo",
 "statement":"Per i difensori la verticalità è in avanti; per centrocampisti e attaccanti è all'indietro."},
{"id":"H03","claim":"V1","expected_fidelity":"coerente","expected_coverage":"parziale",
 "statement":"Anche il movimento all'indietro può essere verticale."},
{"id":"H04","claim":"V3","expected_fidelity":"coerente","expected_coverage":"completo",
 "statement":"I centrocampisti aspettano che il compagno abbia il possesso sicuro prima di arretrare in appoggio e possono inserirsi brevemente in verticale al centro."},
{"id":"H05","claim":"V3","expected_fidelity":"contraddittorio","expected_coverage":"parziale",
 "statement":"I centrocampisti arretrano in appoggio prima che il compagno abbia messo al sicuro il pallone."},
{"id":"H06","claim":"V4","expected_fidelity":"coerente","expected_coverage":"completo",
 "statement":"Gli esterni d'attacco cercano ampiezza e profondità, gli attaccanti centrali profondità; le corse sono diagonali rispetto alla palla."},
{"id":"H07","claim":"V4","expected_fidelity":"contraddittorio","expected_coverage":"completo",
 "statement":"Gli attaccanti centrali cercano ampiezza e profondità, quelli laterali soltanto profondità; le corse sono diagonali alla palla."},
{"id":"H08","claim":"V4","expected_fidelity":"coerente","expected_coverage":"parziale",
 "statement":"Gli attaccanti laterali cercano anche ampiezza."},
{"id":"H09","claim":"P1","expected_fidelity":"coerente","expected_coverage":"completo",
 "statement":"Il portatore deve preferire il controllo sicuro alla giocata veloce ma rischiosa, anche schermando il pallone con il corpo."},
{"id":"H10","claim":"P1","expected_fidelity":"contraddittorio","expected_coverage":"parziale",
 "statement":"Chi conquista palla deve sempre privilegiare il passaggio immediato e rischioso invece di proteggerla."},
{"id":"H11","claim":"P2","expected_fidelity":"coerente","expected_coverage":"completo",
 "statement":"La gestione può coinvolgere i compagni, ma un attaccante in zona offensiva può anche tentare una giocata rapida rischiosa."},
{"id":"H12","claim":"P2","expected_fidelity":"contraddittorio","expected_coverage":"completo",
 "statement":"La gestione non deve mai coinvolgere i compagni e un attaccante in zona offensiva non può rischiare una giocata rapida."},
]
SCHEMA={"type":"object","properties":{
"source_roles":{"type":"array","items":{"type":"object","properties":{
"subject":{"type":"string"},"action":{"type":"string"},"condition":{"type":"string"}},
"required":["subject","action","condition"],"additionalProperties":False}},
"statement_roles":{"type":"array","items":{"type":"object","properties":{
"subject":{"type":"string"},"action":{"type":"string"},"condition":{"type":"string"}},
"required":["subject","action","condition"],"additionalProperties":False}},
"fidelity":{"type":"string","enum":["coerente","contraddittorio","evidenza_insufficiente"]},
"coverage":{"type":"string","enum":["completo","parziale"]},
"reason":{"type":"string"}},
"required":["source_roles","statement_roles","fidelity","coverage","reason"],
"additionalProperties":False}

def judge(model,source,statement,timeout):
    prompt=("Valuta una frase rispetto a UN SOLO principio tattico. "
    "Prima estrai coppie soggetto-azione-condizione da ciascun testo, "
    "senza attribuire a un soggetto le azioni di un altro. "
    "Fedelta': coerente se compatibile, contraddittorio se nega/inverte "
    "soggetto-azione-condizione, evidenza_insufficiente solo se non decidibile. "
    "Copertura: completo se TUTTI i nuclei informativi del principio sono "
    "rappresentati anche con sinonimi, parziale se manca un nucleo; "
    "una frase puo' essere contraddittoria e completa se tratta tutti i "
    "nuclei ma li inverte. Non penalizzare le parafrasi. "
    "Non aggiungere conoscenze esterne. Rispondi nel JSON richiesto.\n"
    "PRINCIPIO:\n"+source+"\nFRASE:\n"+statement)
    payload={"model":model,"stream":False,"think":False,
             "messages":[{"role":"user","content":prompt}],
             "format":SCHEMA,"options":{"temperature":0,"num_ctx":4096}}
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    started=time.monotonic()
    with urllib.request.urlopen(req,timeout=timeout) as resp: result=json.load(resp)
    pred=json.loads(result["message"]["content"])
    if pred["fidelity"] not in ("coerente","contraddittorio","evidenza_insufficiente"):
        raise ValueError("Etichetta fedelta non valida")
    if pred["coverage"] not in ("completo","parziale"):
        raise ValueError("Etichetta copertura non valida")
    return pred,round(time.monotonic()-started,1)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--model",default="qwen3.5:9b")
    p.add_argument("--timeout",type=int,default=900)
    p.add_argument("--output",type=Path,default=Path(
        "projects/tactical-engine/benchmark_holdout_glerean_v4.json"))
    a=p.parse_args()
    if a.output.exists():raise FileExistsError(f"Non sovrascrivo: {a.output}")
    gold=json.loads(GOLD.read_text(encoding="utf-8"))
    claims={c["id"]:c for case in gold["cases"] for c in case["gold_claims"]}
    report={"schema_version":1,"model":a.model,
      "method":"holdout_two_axes_with_relation_extraction",
      "source_file":str(GOLD),"results":[],
      "limitations":["12 frasi sintetiche, non risposte RAG reali",
        "Etichette preliminari soggette a revisione umana",
        "Estrazioni intermedie non ancora valutate automaticamente",
        "Fonti di evidenza da gold Glerean; figure non verificate"]}
    for t in TESTS:
        entry=dict(t)
        try:
            evidence=claims[t["claim"]]["evidence"]
            pred,secs=judge(a.model,evidence,t["statement"],a.timeout)
            entry.update(predicted=pred,seconds=secs,
              fidelity_match=pred["fidelity"]==t["expected_fidelity"],
              coverage_match=pred["coverage"]==t["expected_coverage"])
            print(f'{t["id"]} {t["claim"]}: fedelta '
                  f'{"OK" if entry["fidelity_match"] else "ERRORE"}, '
                  f'copertura {"OK" if entry["coverage_match"] else "ERRORE"}',flush=True)
        except Exception as exc:
            entry["error"]=str(exc)
            print(f'{t["id"]}: ERRORE TECNICO {exc}',flush=True)
        report["results"].append(entry)
        a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    done=[r for r in report["results"] if "fidelity_match" in r]
    print(f'REPORT: {a.output} | fedelta='
          f'{sum(x["fidelity_match"] for x in done)}/{len(done)} '
          f'copertura={sum(x["coverage_match"] for x in done)}/{len(done)}',flush=True)

if __name__=="__main__":main()
