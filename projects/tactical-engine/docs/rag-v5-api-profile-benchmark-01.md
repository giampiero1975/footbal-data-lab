# RAG V5 API profile benchmark 01

## Attività

Misurare il profilo API 6/700 su tre domande nuove di complessità breve, media e complessa. Non è una ripetizione del benchmark locked né del singolo scenario Coverciano.

## Gate

Esecuzione sequenziale sul servizio reale. Ogni caso deve terminare con `done_reason=stop`, almeno una citazione, zero citazioni invalide e indice 6196 invariato. La valutazione qualitativa verifica inoltre che la risposta copra la richiesta senza troncamenti.

## Stato

**ESEGUITO**. Tempi breve/media/complessa: 160,18 / 194,19 / 146,13 s; 3/3 `stop`, citazioni valide e indice invariato. Il caso complesso confonde possesso/non possesso e riconquista/perdita: benchmark non VALIDATO. Correzione generica della distinzione delle fasi IMPLEMENTATA; nuova verifica consentita solo su quel caso.
