# Pannello — recupero job e cronologia dopo riavvio

## Incidente

Durante il job `259b7f4bdb2649a3a2958763a743f678` il servizio e stato riavviato
per distribuire una correzione. Il job era gia terminato e i file RAG erano sul
disco, ma stato e cronologia del pannello vivevano soltanto in memoria. Il
browser e rimasto visivamente sulla fase Copilot e, dopo refresh, la cronologia
e risultata vuota.

## Correzione

- ricostruzione autenticata dei job completati da request/result e report
  copilot privati presenti in `evaluation/api-runs`;
- `GET /v1/jobs/<id>` recupera un risultato completato anche dopo restart;
- `GET /v1/jobs/recent?limit=20` espone soltanto all'utente autenticato le
  analisi recenti necessarie a ricostruire la cronologia;
- il pannello carica la cronologia persistente alla connessione;
- un vero job perso chiude lo stato grafico come `Interrotto` invece di lasciare
  una fase apparentemente attiva.

I file restano privati sulla VPS, le risposte non entrano nei log tecnici e gli
header HTTP restano `no-store`. Nessun nuovo RAG o chiamata esterna.

## Verifica

Suite API/copilot 30/30, compilazione Python e sintassi JavaScript PASS. Stato:
**VALIDATO offline**; deploy e verifica di recupero del job reale DA FARE.

