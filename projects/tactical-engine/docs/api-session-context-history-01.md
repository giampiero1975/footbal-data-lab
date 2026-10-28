# Sessioni e cronologia API — supporto isolato 01

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit codice/test: `863a943`

## Attività

Implementare un unico supporto backend per `RD-SESSION-01` e per la futura
cronologia persistente del pannello, riutilizzando i sidecar dei job. Nessuna
modifica a `knowledge_panel.html`, nessun deploy.

## Contratto retrocompatibile

La richiesta legacy `{"question":"..."}` mantiene sia validazione sia file
persistito originali. L'estensione opzionale accetta:

- `session_id` e `case_id` con identificatori limitati;
- `confirmed_context`, elenco di fatti esplicitamente confermati dall'utente;
- `prior_job_ids`, soli riferimenti a job riusciti.

La domanda originale viene sempre conservata. `effective_question` viene
costruita soltanto dallo scenario confermato e dalla domanda originale. Le
risposte generate nei job precedenti non vengono mai concatenate né promosse a
fatti. Job falliti, incompleti o segnaposto non possono essere riferimenti.

`GET /v1/sessions/{session_id}` ricostruisce lo storico dai file request/job/
result/feedback già esistenti, senza creare un archivio concorrente. La
ricostruzione sopravvive al riavvio e conserva stato, tempi, risultato,
evidenze e metadati disponibili nei job.

## Verifiche

Nuovi casi:

- payload e file legacy invariati;
- domanda contestualizzata composta soltanto da fatti confermati;
- rifiuto di job precedente fallito o segnaposto;
- ricostruzione della sessione dopo riavvio.

Suite API: **32/32 PASS**. Compilazione e diff check: **PASS**.

## Decisione e limiti

Il backend è pronto per una futura UI, ma il pannello operativo non invia
ancora i nuovi campi e non offre ancora ripresa/export cumulativo. Non è stato
effettuato alcun deploy.

Stato: supporto API **IMPLEMENTATO**, test **ESEGUITO**, retrocompatibilità e
recovery offline **VALIDATO**; integrazione nel pannello **DA FARE**, non
**INTEGRATO** in produzione e non **CERTIFICATO**.
