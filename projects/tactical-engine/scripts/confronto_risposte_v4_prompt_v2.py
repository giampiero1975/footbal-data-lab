#!/usr/bin/env python3
"""Esperimento reversibile di miglioramento risposte V4 su contesti TOP5 gia salvati.

Nessuna scrittura su Chroma; baseline originale intatta. L'output espone
sia il testo grezzo sia il testo con marcatura degli ID non validi.
Un ID valido NON prova supporto semantico.
API Ollama: https://docs.ollama.com/api/generate
"""
import argparse,json,re,time
from pathlib import Path
from llama_index.llms.ollama import Ollama
ROOT=Path(__file__).resolve().parents[1]
CIT=re.compile(r"\[(?:GLEREAN-C\d{3}|\d+)\]")
PROMPT="""Sei DRIBBLING, analista tattico del calcio. Rispondi in italiano solo in base alle FONTI qui sotto.
La risposta deve essere completa ma solo su principi documentati. Non aggiungere tattiche generiche.
REGOLE:
- Prima identifica tutti i principi pertinenti alla domanda presenti nelle fonti; copri ciascuno distintamente.
- Distingui compiti dei difensori, centrocampisti, attaccanti centrali e laterali; non scambiare i ruoli.
- Se la fonte distingue zone di campo, esplicita le condizioni: non confondere zona difensiva nostra e avversaria.
- Se una fonte descrive una regola generale e un'eccezione contestuale, spiega entrambe.
- Non attribuire alle figure contenuti non verificati. Non parlare di Gustinetti salvo richiesta.
- Cita soltanto gli ID tra PARENTESI QUADRE presenti nell'elenco FONTI. Non usare [11], [12], [8] se non compaiono esattamente nell'elenco.
- Una citazione va accanto all'affermazione specifica sostenuta. Non inventare fonti o pagine.
- Se un elemento non e' documentato, dichiaralo.
FONTI:
{context}

DOMANDA: {question}

RISPOSTA:"""
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--input",type=Path,default=ROOT/"benchmark_citazioni_stabili_v4.json")
 p.add_argument("--output",type=Path,default=ROOT/"confronto_risposte_v4_prompt_v2.json")
 p.add_argument("--model",default="qwen3.5:9b")
 a=p.parse_args()
 if a.output.exists():raise FileExistsError(f"Non sovrascrivo {a.output}")
 data=json.loads(a.input.read_text(encoding="utf-8"))
 if len(data.get("runs",[]))!=6:raise ValueError("Attese 6 risposte baseline")
 llm=Ollama(model=a.model,base_url="http://127.0.0.1:11434",
            request_timeout=900.0,temperature=0.1,context_window=8192,thinking=False)
 report={"schema_version":1,"method":"same_fixed_top5_context_prompt_v2",
         "baseline":str(a.input),"model":a.model,
         "limitations":["Non modifica motore produzione o Chroma V4",
         "Validazione sintattica ID, non verifica supporto semantico",
         "Contesti fissi TOP5: non misura retrieval end-to-end"],"runs":[]}
 for run in data["runs"]:
  refs=[s["ref"] for s in run["sources"]]
  context="\n\n".join(f'FONTE {s["ref"]} (pagina {s.get("page_numbers","?")}):\n{s["text"]}' for s in run["sources"])
  start=time.monotonic()
  answer=str(llm.complete(PROMPT.format(context=context,question=run["question"])))
  cited=CIT.findall(answer)
  invalid=sorted(set(cited)-set(refs))
  # Non cancellare silenziosamente: evidenzia gli ID non ammessi e conserva il grezzo.
  marked=CIT.sub(lambda m:m.group(0) if m.group(0) in refs else
                 f'[CITAZIONE_NON_VALIDA:{m.group(0)[1:-1]}]',answer)
  result={"case_id":run["case_id"],"mode":run["mode"],
    "question":run["question"],"allowed_refs":refs,
    "baseline_answer":run["answer"],"baseline_invalid_refs":run.get("invalid_refs",[]),
    "answer_raw":answer,"answer_marked":marked,"used_refs":cited,
    "invalid_refs":invalid,"valid_citation_ids":not invalid,
    "seconds":round(time.monotonic()-start,2),"gold_claims":run["gold_claims"],
    "sources":run["sources"]}
  report["runs"].append(result)
  a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(f'{run["case_id"]} {run["mode"]}: invalid={invalid} | {result["seconds"]}s',flush=True)
 print("REPORT",a.output,flush=True)
if __name__=="__main__":main()
