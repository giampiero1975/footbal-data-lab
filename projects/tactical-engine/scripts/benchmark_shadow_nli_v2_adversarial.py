#!/usr/bin/env python3
"""Shadow NLI V2 adversarial checks on immutable RAG V5 evidence."""
import argparse
import json
import time
from pathlib import Path
from shadow_nli_v2_inference import judge_pair

CASES = [
("q3","F1","low_block_wrong","Contro una difesa molto bassa è preferibile verticalizzare anziché sfruttare l'ampiezza.","contradicted"),
("q3","F1","low_block_right","Contro una difesa molto bassa è preferibile sfruttare l'ampiezza per arrivare al cross.","supported"),
("q3","F1","heavy_pitch","Su un campo pesante la verticalizzazione è sempre la scelta migliore.","insufficient"),
("q3","F3","offside_risk","Senza tempi di intesa corretti, verticalizzare contro una difesa in linea può causare fuorigioco.","supported"),
("q3","F3","offside_always","Verticalizzare contro una difesa in linea causa sempre fuorigioco.","insufficient"),
("q5","F1","three_systems","Nei tre sistemi descritti il centromediano metodista protegge la difesa e costruisce il gioco.","supported"),
("q5","F1","all_systems","Tutti i sistemi di gioco prevedono necessariamente un centromediano metodista.","insufficient"),
("q5","F1","counterattack","Nel secondo e terzo sistema descritti concedere campo serve a cercare il contrattacco veloce.","supported"),
("q5","F1","counterattack_wrong","Nel secondo e terzo sistema descritti concedere campo non serve a cercare il contrattacco veloce.","contradicted"),
("q2","F2","jolly_drill","Nell'esercitazione 3 contro 3 più jolly si usa il jolly per cercare gol nelle due portine.","supported"),
("q2","F2","jolly_match","In tutte le partite ufficiali è consentito un giocatore jolly neutrale aggiuntivo.","insufficient"),
]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_baseline_20261022.json"))
    p.add_argument("--output",type=Path,default=Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_adversarial_20261022.json"))
    p.add_argument("--execute",action="store_true")
    a=p.parse_args()
    if not a.execute: p.error("Specify --execute")
    if a.output.resolve()==a.source.resolve() or a.output.exists(): p.error("Output exists or overlaps input")
    if not a.source.is_file():
        p.error(f"Baseline mancante: {a.source}; nessun benchmark avviato")
    if not a.output.parent.is_dir():
        p.error(f"Directory report mancante: {a.output.parent}; non viene creata automaticamente")
    report=json.loads(a.source.read_text(encoding="utf-8"))
    questions={q["id"]:q for q in report["questions"]}
    rows=[]
    for qid,source_id,cid,claim,expected in CASES:
        evidence=next(x["text"] for x in questions[qid]["evidence"] if x["label"]==source_id)
        start=time.monotonic()
        try:
            actual=judge_pair(claim,evidence)
            row={"id":cid,"question_id":qid,"source_id":source_id,"claim":claim,"expected":expected,"actual":actual,"pass":actual==expected,"elapsed_seconds":round(time.monotonic()-start,3)}
        except Exception as e:
            row={"id":cid,"question_id":qid,"source_id":source_id,"claim":claim,"expected":expected,"actual":None,"pass":False,"error":str(e)[:300]}
        rows.append(row)
        print(f"{cid}: {row['actual']} expected={expected}",flush=True)
    result={"schema":"shadow_nli_v2_adversarial_v1","mode":"shadow_only","total":len(rows),"passed":sum(r["pass"] for r in rows),"errors":sum("error" in r for r in rows),"cases":rows,"limitations":["Curated expectations are not a population accuracy estimate","No production RAG or Chroma mutation"]}

    with a.output.open("x",encoding="utf-8") as f: json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
    print(f"ADVERSARIAL {result['passed']}/{result['total']} errors={result['errors']} REPORT {a.output}",flush=True)

if __name__=="__main__": main()
