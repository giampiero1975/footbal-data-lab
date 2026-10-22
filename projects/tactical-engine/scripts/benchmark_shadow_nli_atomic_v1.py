#!/usr/bin/env python3
"""Atomic NLI shadow controls, read-only on RAG V5 baseline.
Docs: https://docs.ollama.com/api/chat and /capabilities/structured-outputs
"""
import argparse, json, time
from pathlib import Path
from shadow_nli_v2_inference import judge_pair

CASES=[
("q3","F1","low_block_width","Contro un avversario rintanato presso la propria area si può sfruttare l'ampiezza del campo.","supported"),
("q3","F1","low_block_cross","Contro un avversario rintanato presso la propria area si può rifinire con un cross.","supported"),
("q3","F1","low_block_reverse","Contro un avversario rintanato presso la propria area la verticalizzazione è preferibile alla manovra aggirante.","contradicted"),
("q3","F1","space_behind","Quando c'è spazio dietro la difesa avversaria si può attaccare in verticale.","supported"),
("q3","F1","vertical_always","La verticalizzazione è sempre il mezzo migliore per andare a rete.","contradicted"),
("q3","F3","offside_conditional","Contro una difesa in linea, una cattiva intesa può portare al fuorigioco verticalizzando.","supported"),
("q3","F3","offside_universal","Ogni verticalizzazione contro una difesa in linea produce fuorigioco.","insufficient"),
("q5","F1","methodist_three","Nei tre sistemi descritti il centromediano metodista protegge la difesa.","supported"),
("q5","F1","methodist_build","Nei tre sistemi descritti il centromediano metodista costruisce il gioco.","supported"),
("q5","F1","methodist_every","Tutti i sistemi di gioco del calcio richiedono un centromediano metodista.","insufficient"),
("q5","F1","counterattack_intent","Nel secondo e terzo sistema si concede campo per cercare un contrattacco veloce.","supported"),
("q5","F1","counterattack_negation","Nel secondo e terzo sistema concedere campo non è una scelta mirata al contrattacco veloce.","contradicted"),
("q2","F2","jolly_exercise","L'esercitazione 3 contro 3 più jolly prevede di sfruttare la superiorità numerica.","supported"),
("q2","F2","jolly_goals","Nell'esercitazione 3 contro 3 più jolly si cerca di segnare in due portine.","supported"),
("q2","F2","jolly_official","Il regolamento delle partite ufficiali consente sempre un jolly neutrale aggiuntivo.","insufficient"),
]

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--source",type=Path,default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_baseline_20261022.json"))
 p.add_argument("--output",type=Path,default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_atomic_v1_20261022.json"))
 p.add_argument("--execute",action="store_true")
 a=p.parse_args()
 if not a.execute:p.error("Explicit --execute required")
 if a.source.resolve()==a.output.resolve() or a.output.exists():p.error("Output already exists or overlaps source")
 baseline=json.loads(a.source.read_text(encoding="utf-8"))
 qs={q["id"]:q for q in baseline["questions"]}
 rows=[]
 for qid,source_id,cid,claim,expected in CASES:
  evidence=next(x["text"] for x in qs[qid]["evidence"] if x["label"]==source_id)
  start=time.monotonic()
  try:
   actual=judge_pair(claim,evidence)
   row={"id":cid,"question_id":qid,"source_id":source_id,"claim":claim,"expected":expected,"actual":actual,"pass":actual==expected,"elapsed_seconds":round(time.monotonic()-start,3)}
  except Exception as exc:
   row={"id":cid,"question_id":qid,"source_id":source_id,"claim":claim,"expected":expected,"actual":None,"pass":False,"error":str(exc)[:300]}
  rows.append(row)
  print(cid,row["actual"],"expected",expected,flush=True)
 report={"schema":"shadow_nli_atomic_v1","mode":"shadow_only","total":len(rows),"passed":sum(x["pass"] for x in rows),"errors":sum("error" in x for x in rows),"cases":rows,"limitations":["Curated cases; not population accuracy","RAG V5 and Chroma unchanged"]}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open("x",encoding="utf-8") as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write("\n")
 print("ATOMIC",report["passed"],"/",report["total"],"errors",report["errors"],"REPORT",a.output,flush=True)
if __name__=="__main__":main()
