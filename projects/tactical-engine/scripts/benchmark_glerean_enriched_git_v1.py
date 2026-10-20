#!/usr/bin/env python3
"""Benchmark Glerean con figure: sola lettura dei contesti, sola scrittura nel report.
API Ollama: https://docs.ollama.com/api/generate
"""
import argparse,hashlib,json,re,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ROLES={"1":"portiere","2":"difensore","3":"difensore","5":"difensore","4":"centrocampista centrale","6":"centrocampista","8":"centrocampista","7":"attaccante esterno","11":"attaccante esterno","9":"attaccante centrale","10":"attaccante centrale"}
FIGURES={
"POSSESSO":[
(10,12,"I centrocampisti conquistano una seconda palla dopo respinta avversaria; il testo prescrive gestione sicura e protezione del pallone."),
(11,12,"Il n.10 spalle alla porta avversaria appoggia al n.4 che vede il gioco."),
(12,13,"Il n.4 centrocampista porta palla; gli esterni n.11 e n.7 tagliano in appoggio; n.9 si muove per primo in direzione opposta, n.10 occupa lo spazio liberato. Quattro soluzioni di passaggio per il n.4."),
(13,13,"Il n.4 protegge palla e gira indietro; n.6 e n.8 centrocampisti si allargano per correre dietro le spalle del CENTROCAMPISTA avversario, non dei difensori."),
(14,13,"I difensori n.3,5,2 arretrano rispetto al portatore per creare spazio e sostegno.")],
"UNO-CONTRO-UNO":[
(18,16,"Il n.1 portiere rilancia lungo verso attaccanti avanzati; il testo dice che uno degli attaccanti spizza la palla, ma la figura non ne identifica con certezza l'autore."),
(19,16,"Il n.8 centrocampista gestisce una seconda palla dopo respinta; gli attaccanti n.11,10,9,7 cercano spazi centrali e laterali sulla linea difensiva avversaria.")],
"VERTICALITA":[
(20,17,"Il n.4 centrocampista porta palla; i difensori n.3,5,2 arretrano per sostegno e maggiori tempi di gestione."),
(21,18,"Gli attaccanti esterni n.11,7 cercano profondita e ampiezza; i centrali n.9,10 profondita; movimenti diagonali rispetto alla palla.")]}
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
def ids(answer,allowed):
    found=[]
    for x in re.findall(r'\[([^\[\]\n]+)\]',answer):
        # il primo ID e' la fonte; numeri di pagina non sono ID
        first=x.split(',')[0].strip()
        if re.fullmatch(r'GLEREAN-C\d{3}|\d+',first):found.append(first)
    allow={x.strip('[]') for x in allowed}
    return sorted(set(found)),sorted(set(found)-allow)
def case_name(case):
    c=case.upper()
    if 'POSSESSO' in c:return 'POSSESSO'
    if 'VERTICAL' in c:return 'VERTICALITA'
    if 'UNO' in c or '1V1' in c or '1_1' in c:return 'UNO-CONTRO-UNO'
    raise ValueError('Case non riconosciuto: '+case)
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,default=ROOT/'benchmark_gemma_glerean_fixed_v2.json')
    p.add_argument('--output',type=Path,default=ROOT/'evaluation/benchmark_glerean_enriched_v1.json')
    p.add_argument('--models',nargs='+',default=['qwen3.5:9b','gemma3:12b'])
    p.add_argument('--num-ctx',type=int,default=8192)
    p.add_argument('--reserve',type=int,default=1536)
    p.add_argument('--run',action='store_true')
    a=p.parse_args()
    if a.output.exists():p.error('Non sovrascrivo output esistente')
    if a.num_ctx<=a.reserve:p.error('num_ctx deve superare reserve')
    baseline=json.loads(a.input.read_text(encoding='utf-8'))
    if len(baseline['runs'])!=6:raise ValueError('Attesi sei run congelati')
    jobs=[]
    for model in a.models:
        for r in baseline['runs']:
            name=case_name(r['case_id'])
            original='\n\n'.join('FONTE '+s['ref']+' (pagina '+str(s.get('page_numbers','?'))+'):\n'+s['text'] for s in r['sources'])
            side='MAPPA RUOLI GLEREAN 3-3-4 (solo per interpretare figure, non citare come fonte autonoma): '+', '.join('n.'+n+'='+role for n,role in ROLES.items())
            side+='\nDESCRIZIONI FIGURE DEL PDF ORIGINALE (non aggiungono nuove citazioni):\n'+'\n'.join('Fig. '+str(n)+' (pagina stampata '+str(pg)+'): '+desc for n,pg,desc in FIGURES[name])
            context=original+'\n\n'+side
            prompt=PROMPT.format(context=context,question=r['question'])
            jobs.append((model,r,prompt,hashlib.sha256(prompt.encode()).hexdigest()))
    print('PREFLIGHT:',len(jobs),'run; contesti originali immutati; figure uguali per i due modelli')
    for m,r,prompt,sha in jobs:print(m,r['case_id'],r['mode'],sha[:16],len(prompt))
    if not a.run:return
    report={'method':'glerean_figures_sidecar_v1','models':a.models,'num_ctx':a.num_ctx,'num_predict':a.reserve,'temperature':0.1,'runs':[]}
    for i,(model,r,prompt,sha) in enumerate(jobs,1):
        req=urllib.request.Request('http://127.0.0.1:11434/api/generate',data=json.dumps({'model':model,'prompt':prompt,'stream':False,'think':False,'options':{'temperature':0.1,'num_ctx':a.num_ctx,'num_predict':a.reserve}}).encode(),headers={'Content-Type':'application/json'},method='POST')
        start=time.monotonic()
        with urllib.request.urlopen(req,timeout=1200) as response:result=json.load(response)
        used,invalid=ids(result.get('response',''),[s['ref'] for s in r['sources']])
        tokens=result.get('prompt_eval_count')
        ok=tokens is not None and tokens<=a.num_ctx-a.reserve
        report['runs'].append({'model':model,'case_id':r['case_id'],'mode':r['mode'],'question':r['question'],'prompt_sha256':sha,'prompt_eval_count':tokens,'eval_count':result.get('eval_count'),'seconds_wall':round(time.monotonic()-start,2),'comparable_context':ok,'used_refs':used,'invalid_refs':invalid,'answer_raw':result.get('response',''),'gold_claims':r.get('gold_claims')})
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f"{i}/{len(jobs)} {model} {r['case_id']} {r['mode']} context_ok={ok}",flush=True)
        if not ok:raise RuntimeError('Possibile troncamento del contesto; stop')
    print('Report:',a.output)
if __name__=='__main__':main()
