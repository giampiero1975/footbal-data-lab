# Knowledge Panel feedback ed export 01

Data: 2026-10-25. Stato: **IMPLEMENTATO**.

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

Eseguire deploy VPS, smoke autenticato del feedback su un job controllato e
verifica HTTP del pannello. Non eseguire inferenze o benchmark. Stato corrente:
**IMPLEMENTATO**, non ancora INTEGRATO.
