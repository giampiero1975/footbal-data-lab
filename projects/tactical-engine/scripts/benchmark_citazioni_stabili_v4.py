#!/usr/bin/env python3
"""Test isolato: citazioni numeriche vs ID stabili sullo stesso contesto.

Usa la selezione TOP5 tecnico gia verificata; nessuna scrittura su Chroma.
La generazione diretta e' diversa da CitationQueryEngine: confronto interno
a parita' di contesto e parametri, NON confronto diretto con benchmark precedenti.
"""
import argparse
import json
import re
import time
from pathlib import Path
import chromadb
from llama_index.llms.ollama import Ollama
from test_dribbling_v4_top5_top10 import DB,COLLECTION,SOURCE

ROOT=Path("/opt/football-data-lab/projects/tactical-engine")
CASES=[
 ("GLEREAN-334-POSSESSO-002",[6,13,14,17,16]),
 ("GLEREAN-334-UNO-CONTRO-UNO-003",[18,12,14,24,20]),
 ("GLEREAN-334-VERTICALITA-004",[19,20,8,21,17]),
]
PROMPT=(
 "Sei DRIBBLING, analista tattico. Rispondi in italiano SOLO con le fonti elencate. "
 "Non usare conoscenze esterne. Ogni affermazione tattica specifica deve avere "
 "una citazione esatta della fonte che la documenta. Non citare fonti per sola "
 "somiglianza tematica. Non confondere la NOSTRA zona difensiva con la zona "
 "difensiva AVVERSARIA. Non attribuire informazioni alle figure: non sono state "
 "analizzate visivamente. Non aggiungere commenti su Gustinetti se non richiesti. "
 "Se una informazione manca, dichiaralo. "
 "Formato citazione obbligatorio: {citation_format}. "
 "Cita soltanto identificatori elencati nelle fonti.\n\n"
 "FONTI:\n{context}\n\nDOMANDA: {question}\n\nRISPOSTA:"
)

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--output",default=str(ROOT/"benchmark_citazioni_stabili_v4.json"))
 args=ap.parse_args()
 out=Path(args.output)
 if out.exists(): raise FileExistsError(f"Non sovrascrivo un report precedente: {out}")
 gold=json.loads((ROOT/"evaluation/gold_glerean_principi_v1.json").read_text(encoding="utf-8"))
 questions={c["case_id"]:c for c in gold["cases"]}
 coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
 if coll.count()!=86: raise RuntimeError("Collection V4 inattesa")
 rows=coll.get(where={"source":SOURCE},include=["documents","metadatas"])
 chunks={int(m["chunk_index"]):(d,m) for d,m in zip(rows["documents"],rows["metadatas"])}
 llm=Ollama(model="qwen3.5:9b",base_url="http://127.0.0.1:11434",
            request_timeout=900.0,temperature=0.1,context_window=8192,thinking=False)
 report={"method":"direct_llm_complete_fixed_context","model":"qwen3.5:9b",
         "notes":["Confronto controllato del formato citazioni, non CitationQueryEngine",
                  "Verifica automatica soltanto validita ID, non supporto semantico",
                  "I gold claim non sono forniti al modello"],"runs":[]}
 for case_id,indices in CASES:
  question=questions[case_id]["question"]
  for mode in ("numeric","stable"):
   refs=[f"[{j}]" if mode=="numeric" else f"[GLEREAN-C{idx:03d}]" for j,idx in enumerate(indices,1)]
   context="\n\n".join(f"FONTE {ref} (pagina {chunks[idx][1].get('page_numbers','?')}):\n{chunks[idx][0]}"
                        for ref,idx in zip(refs,indices))
   prompt=PROMPT.format(citation_format=("numeri come [1]" if mode=="numeric" else
                        "ID come [GLEREAN-C013]"),context=context,question=question)
   start=time.monotonic()
   answer=str(llm.complete(prompt))
   seconds=round(time.monotonic()-start,1)
   used=re.findall(r"\[(?:GLEREAN-C\d{3}|\d+)\]",answer)
   invalid=sorted(set(used)-set(refs))
   entry={"case_id":case_id,"mode":mode,"question":question,"chunk_indices":indices,
          "seconds":seconds,"answer":answer,"used_refs":used,"invalid_refs":invalid,
          "gold_claims":questions[case_id]["gold_claims"],
          "sources":[{"ref":ref,"chunk_index":idx,"page_numbers":chunks[idx][1].get("page_numbers"),
                      "text":chunks[idx][0]} for ref,idx in zip(refs,indices)]}
   report["runs"].append(entry)
   out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
   print(f"{case_id} {mode}: {seconds}s | citazioni={len(used)} | ID_non_validi={invalid}",flush=True)
 print(f"COMPLETATO: {out} | {len(report['runs'])} generazioni; Chroma invariato",flush=True)

if __name__=="__main__":
 main()
