#!/usr/bin/env python3
"""Read-only controlled A/B for V5: same retrieved evidence, two prompts.

No automatic faithfulness claims. Stores complete answers/evidence for review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.request import Request,urlopen
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

COLLECTION="dribbling_tactics_v5_multisource"
DB="/opt/football-data-lab/knowledge/rag/chroma"
ALIASES={"Allegati_222010155625":"LA TECNICA APPLICATA COME PRESUPPOSTO DEL GIOCO COLLETTIVO",
         "Allegati_45201211489":"Conseiderazione sul sistema di gioco 4-3-2-1",
         "Allegati_71201095736":"IL CONCETTO DI MARCAMENTO NELLA DIFESA AD UOMO E A ZONA",
         "Categoria_Tattiche del calcio - Wikipedia(1)":"Categoria_Tattiche del calcio - Wikipedia"}
QUESTIONS=[
 ("q1","Come affrontare con il 4-4-2 una squadra schierata con il 3-4-1-2?"),
 ("q2","Come creare superiorità numerica in fase di possesso palla?"),
 ("q3","Quali principi favoriscono la verticalizzazione nella fase offensiva?"),
 ("q4","Come sfruttare i triangoli per sviluppare il gioco di squadra?"),
 ("q5","Quali vantaggi e rischi comporta variare il sistema di gioco durante una partita?")]
BASELINE=("Sei DRIBBLING, assistente di analisi tattica calcistica. "
 "Rispondi esclusivamente in base agli estratti numerati forniti. "
 "Non inventare fatti, autori, pagine o citazioni. "
 "Ogni affermazione tattica sostanziale deve avere una citazione nel formato [F1], [F2], ecc. "
 "Se le fonti non consentono una risposta affidabile, esplicita il limite. "
 "Rispondi in italiano in modo chiaro e sintetico.")
STRICT=("Sei DRIBBLING, analista tattico del calcio. Usa ESCLUSIVAMENTE le evidenze fornite. "
 "Rispondi alla domanda specifica, non a una domanda correlata. "
 "Distingui rigorosamente: (a) principi generali; (b) esempi di uno specifico sistema di gioco; "
 "(c) esercitazioni; (d) conseguenze di una VARIAZIONE del sistema durante la gara. "
 "Non trasformare un esempio di un sistema in una regola generale né una esercitazione in una tattica di partita. "
 "Se la domanda riguarda il CAMBIO di modulo, non sostituirla con i pro e contro di moduli isolati: "
 "dichiara esplicitamente quali conseguenze del cambio sono documentate e quali no. "
 "Se le fonti descrivono condizioni opposte, preserva il contrasto: ad esempio non confondere "
 "la profondità contro difese alte con l'ampiezza contro difese basse. "
 "Prima di rispondere verifica internamente che ogni affermazione sia sostenuta dagli estratti e "
 "non contraddica altre evidenze; non mostrare il ragionamento interno. "
 "Cita ogni affermazione tattica rilevante con [F1], [F2], ecc., usando solo ID esistenti. "
 "Se le evidenze non rispondono alla domanda, ammetti il limite invece di colmarlo con conoscenze esterne. "
 "Struttura: risposta diretta; condizioni e limiti; eventuali esempi chiaramente etichettati. "
 "Rispondi in italiano, conciso e preciso.")
def norm(s):
 return re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",s.casefold())).strip()
def chat(model,system,question,evidence,timeout):
 context="\n\n".join(f"[F{i}] Fonte: {r['source']} | Pagine: {r['pages']}\n{r['text']}"
                      for i,r in enumerate(evidence,1))
 payload={"model":model,"stream":False,"think":False,
          "messages":[{"role":"system","content":system},
                      {"role":"user","content":f"DOMANDA:\n{question}\n\nFONTI:\n{context}"}],
          "options":{"temperature":0,"num_ctx":8192}}
 req=Request("http://127.0.0.1:11434/api/chat",data=json.dumps(payload,ensure_ascii=False).encode(),
             headers={"Content-Type":"application/json"},method="POST")
 with urlopen(req,timeout=timeout) as res: obj=json.load(res)
 answer=(obj.get("message") or {}).get("content","")
 if not answer.strip():raise RuntimeError("Empty answer from Ollama")
 return answer,{"total_duration_ns":obj.get("total_duration"),
                "eval_count":obj.get("eval_count"),"prompt_eval_count":obj.get("prompt_eval_count")}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--output",type=Path,required=True)
 p.add_argument("--model",default="qwen3.5:9b")
 p.add_argument("--timeout",type=int,default=900)
 args=p.parse_args()
 coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
 count=coll.count()
 if count!=5319:raise RuntimeError(f"Unexpected V5 size: {count}")
 embed=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
 rerank=CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",device="cpu",max_length=512)
 report={"collection":COLLECTION,"model":args.model,"count_before":count,
         "prompts":{"baseline":BASELINE,"strict":STRICT},
         "method":"same 24 dense candidates, mMARCO ranking and 8 deduplicated evidences per question",
         "questions":[],"caveat":"Citation syntax is not factual verification; human review needed."}
 def save():
  report["count_after"]=coll.count()
  report["index_unchanged"]=(report["count_after"]==count)
  args.output.parent.mkdir(parents=True,exist_ok=True)
  args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 try:
  for qid,question in QUESTIONS:
   print("START",qid,flush=True)
   got=coll.query(query_embeddings=[embed.get_query_embedding(question)],n_results=24,
                  include=["documents","metadatas","distances"])
   rows=[]
   for cid,doc,meta,dist in zip(got["ids"][0],got["documents"][0],
                                 got["metadatas"][0],got["distances"][0]):
    raw=meta.get("raw_text") or doc
    rows.append({"id":cid,"source":meta["source"],"source_relative":meta.get("source_relative"),
                 "pages":meta.get("page_numbers"),"text":doc,"distance":round(float(dist),5),
                 "fingerprint":hashlib.sha256(norm(raw).encode()).hexdigest()})
   scores=rerank.predict([(question,r["text"]) for r in rows],batch_size=1,show_progress_bar=False)
   evidence=[];seen=set()
   for ix in sorted(range(len(rows)),key=lambda i:float(scores[i]),reverse=True):
    row=rows[ix]
    key=(ALIASES.get(row["source"],row["source"]),row["fingerprint"])
    if key in seen:continue
    seen.add(key)
    evidence.append({k:v for k,v in row.items() if k!="fingerprint"})
    if len(evidence)==8:break
   entry={"id":qid,"question":question,"evidence":evidence,"variants":{}}
   report["questions"].append(entry)
   save()
   for variant,system in (("baseline",BASELINE),("strict",STRICT)):
    t=time.monotonic()
    answer,stats=chat(args.model,system,question,evidence,args.timeout)
    cited=sorted(set(re.findall(r"\[F(\d+)\]",answer)),key=int)
    entry["variants"][variant]={"answer":answer,"citation_ids":cited,
      "invalid_citation_ids":[x for x in cited if not 1<=int(x)<=len(evidence)],
      "elapsed_seconds":round(time.monotonic()-t,2),"generation":stats}
    save()
    print("DONE",qid,variant,"seconds",entry["variants"][variant]["elapsed_seconds"],flush=True)
 except (Exception,KeyboardInterrupt) as exc:
  report["error"]=f"{type(exc).__name__}: {exc}"
  save()
  print("ERROR",report["error"],flush=True)
  raise
 save()
 print("PASS: A/B completed; V5 unchanged =",report["index_unchanged"],flush=True)
if __name__=="__main__":main()
