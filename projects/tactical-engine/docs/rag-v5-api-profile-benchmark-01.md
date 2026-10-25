# RAG V5 API profile benchmark 01

## Attività

Misurare il profilo API 6/700 su tre domande nuove di complessità breve, media e complessa. Non è una ripetizione del benchmark locked né del singolo scenario Coverciano.

## Gate

Esecuzione sequenziale sul servizio reale. Ogni caso deve terminare con `done_reason=stop`, almeno una citazione, zero citazioni invalide e indice 6196 invariato. La valutazione qualitativa verifica inoltre che la risposta copra la richiesta senza troncamenti.

## Stato

**ESEGUITO**. Tempi breve/media/complessa: 160,18 / 194,19 / 146,13 s; 3/3 `stop`, citazioni valide e indice invariato. Il caso complesso confonde possesso/non possesso e riconquista/perdita: benchmark non VALIDATO. Correzione generica della distinzione delle fasi IMPLEMENTATA; nuova verifica consentita solo su quel caso.

Retest mirato: 143,29 s, `stop`, zero citazioni invalide e 6196 invariato. La distinzione migliora, ma resta una frase ambigua fra superamento del pressing e reazione alla perdita. Il caso complesso rimane **ESEGUITO**, non VALIDATO; i casi breve e medio sono VALIDATI tecnicamente e qualitativamente.

Correzione V2 **IMPLEMENTATO**: per domande con perdita, la seconda fase ammette soltanto azioni della squadra che ha appena perso palla ed esclude esplicitamente uscita dal pressing, conduzione e passaggi della squadra in possesso. Un ultimo test differenziale è autorizzato.

Correzione conclusiva: controllo automatico rileva le due famiglie cross-phase, tenta una rigenerazione e, se il modello le ripete, rimuove soltanto i claim completi ancorati alle rispettive citazioni. Evidenza finale `evaluation/runtime-archive/rag_v5_complex_phase_prune_v2.json`: 132,7 s, `stop`, due sezioni coerenti, zero citazioni invalide e 6196 invariato. Caso complesso **VALIDATO**; benchmark applicativo 3/3 VALIDATO.
