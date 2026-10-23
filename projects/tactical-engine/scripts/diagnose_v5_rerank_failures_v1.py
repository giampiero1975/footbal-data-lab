#!/usr/bin/env python3
"""Read-only V5 diagnostic for fresh_03 and fresh_10; no generation."""
import argparse, hashlib, json, re
from pathlib import Path
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

DB="/opt/football-data-lab/knowledge/rag/chroma"
MAIN="dribbling_tactics_v5_multisource"
EXTRA="dribbling_tactics_v5_exercise_candidate_v1"
QUESTIONS={
 "fresh_03":"Perché la descrizione di un assetto difensivo nel manuale interno non basta a dimostrare che cambiare modulo durante una gara aumenti o riduca il rischio?",
 "fresh_10":"Confrontando Ussia e il manuale interno FOOTBALL-DATA-LAB, quali condizioni favoriscono la pressione dopo la perdita e perché l'esercitazione di Ussia non dimostra una regola universale?",
}
ALIASES={
 "Allegati_222010155625":"LA TECNICA APPLICATA COME PRESUPPOSTO DEL GIOCO COLLETTIVO",
 "Allegati_45201211489":"Conseiderazione sul sistema di gioco 4-3-2-1",
 "Allegati_71201095736":"IL CONCETTO DI MARCAMENTO NELLA DIFESA AD UOMO E A ZONA",
 "Categoria_Tattiche del calcio - Wikipedia(1)":"Categoria_Tattiche del calcio - Wikipedia",
}
def norm(s):
 return re.sub(r"\\s+"," ",re.sub(r"[^\\w\\s]"," ",s.casefold())).strip()
def rows_for(coll,embedding,stage,n=24,where=None):
 got=coll.query(query_embeddings=[embedding],n_results=n,where=where,include=["documents","metadatas","distances"])
 out=[]
 for i,(cid,doc,meta,dist) in enumerate(zip(got["ids"][0],got["documents"][0],got["metadatas"][0],got["distances"][0]),1):
  out.append({"id":cid,"stage":stage,"dense_rank":i,"source":meta.get("source"),"pages":meta.get("page_numbers"),"distance":float(dist),"text":doc,"fingerprint":hashlib.sha256(norm(meta.get("raw_text") or doc).encode()).hexdigest()})
 return out
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--output",type=Path,default=Path("projects/tactical-engine/diagnostica_v5_rerank_failures_v1.json"))
 args=ap.parse_args()
 client=chromadb.PersistentClient(path=DB)
 main=client.get_collection(MAIN)
 extra=client.get_collection(EXTRA)
 before=(main.count(),extra.count())
 if before!=(5319,34):raise RuntimeError(f"Unexpected counts: {before}")
 embed=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
 rerank=CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",device="cpu",max_length=512)
 report={"schema":"v5_rerank_diagnostic_v1","read_only":True,"count_before":before,"questions":[]}
 for qid,q in QUESTIONS.items():
  vector=embed.get_query_embedding(q)
  rows=rows_for(main,vector,"global_dense24")
  if qid=="fresh_10":
   rows+=rows_for(main,vector,"source_aware_ussia24",where={"source":"Transizioni.Ussia"})
   rows+=rows_for(extra,vector,"exercise_candidate24",n=24)
  seen_ids=set();unique=[]
  for row in rows:
   if row["id"] not in seen_ids:unique.append(row);seen_ids.add(row["id"])
  scores=rerank.predict([(q,r["text"]) for r in unique],batch_size=1,show_progress_bar=False)
  seen=set();rank=0
  for i in sorted(range(len(unique)),key=lambda j:float(scores[j]),reverse=True):
   r=unique[i];r["score"]=float(scores[i])
   key=(ALIASES.get(r["source"],r["source"]),r["fingerprint"])
   if key in seen:r["rerank_rank"]=None;r["duplicate"]=True;continue
   seen.add(key);rank+=1;r["rerank_rank"]=rank;r["duplicate"]=False
  report["questions"].append({"id":qid,"question":q,"candidate_count":len(unique),"candidates":unique})
  print(f"{qid}: candidates={len(unique)}; top8:",[(r["source"],r["pages"]) for r in sorted(unique,key=lambda x:x["rerank_rank"] or 999)[:8]],flush=True)
 report["count_after"]=(main.count(),extra.count())
 report["index_unchanged"]=report["count_before"]==report["count_after"]
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print("REPORT:",args.output,"unchanged:",report["index_unchanged"],flush=True)
if __name__=="__main__":main()
