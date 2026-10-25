# Knowledge Panel feedback ed export 01

Data: 2026-10-25. Stato: **VALIDATO e INTEGRATO**.

## Attività e differenza tecnica

Completare il consumer locale senza ripetere benchmark generativi: le funzioni
di cronologia e provenienza erano già presenti; l'incremento aggiunge fonti
espandibili, esportazione Markdown locale e feedback utile/non utile persistente.

## Sicurezza e dati

`POST /v1/feedback` richiede lo stesso Bearer token, è soggetto al rate limit e
accetta soltanto un job ID valido già concluso con successo e un booleano
`helpful`. Il file persistito contiene esclusivamente schema, job ID, giudizio e
timestamp: nessuna domanda, risposta o evidenza. Un nuovo giudizio sul medesimo
job sostituisce atomicamente il precedente.

L'esportazione è prodotta dal browser in Markdown e non invia dati a servizi
esterni. Il token resta soltanto in memoria come prima.

## Evidenza offline

- compilazione Python superata;
- suite API/catalogo 14/14;
- sintassi JavaScript verificata con Node;
- `git diff --check` superato.

## Decisione

Deploy VPS completato nel commit `e9dda93`. Suite VPS 14/14, compilazione
superata e servizio `active/running`. Smoke HTTP non generativo:

- readiness `ready`;
- collection invariata a 6410 chunk/157 documenti;
- pannello contiene feedback ed export;
- endpoint autenticato risponde correttamente `404 not_found` per un job
  inesistente senza creare file;
- percorso positivo e assenza di contenuti nel file verificati dal test unitario.

Decisione: pannello **VALIDATO e INTEGRATO**. Non è stata eseguita alcuna
inferenza o ripetizione di benchmark. Il feedback reale inizierà a essere
raccolto soltanto quando l'utente valuterà risposte concluse dal pannello.

## Osservabilità feedback

Incremento distinto **VALIDATO e INTEGRATO**: `/v1/metrics` aggrega il numero di file di
feedback validi in totale, utili e non utili; il pannello mostra il rapporto
senza leggere o esporre domande e risposte. La scansione ignora file corrotti e
un nuovo voto sullo stesso job sostituisce il precedente, evitando doppi
conteggi. Test locale e VPS 14/14, compilazione e sintassi JavaScript superati.
Smoke reale: servizio attivo, worker vivo, coda zero, collection attesa 6410 e
feedback iniziale `0/0/0`; vista `Feedback utili` servita dal pannello. Nessuna
inferenza eseguita.
