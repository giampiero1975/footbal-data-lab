# Feedback UX — conferma persistita 01

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit tecnico: `ed7a84c`

## Attività

Verificare il percorso pannello → API → persistenza → recupero del feedback e
aggiungere una conferma visiva affidabile senza cambiare contratto o logica
backend.

## Ricognizione e diagnosi

Il backend era già corretto e coperto da `RD-FEEDBACK-RECOVERY-01`:

- `State.record_feedback()` accetta soltanto job `succeeded`, scrive
  atomicamente un unico sidecar e restituisce il record realmente salvato;
- `State.feedback_for_job()` valida schema, `job_id` e tipo booleano;
- `State.persisted_job()` e `GET /v1/jobs/{job_id}` espongono il feedback
  persistito anche dopo riavvio;
- `POST /v1/feedback` restituisce HTTP 200 con il record salvato oppure un
  errore verificabile.

Il difetto era esclusivamente frontend. `sendFeedback()` attendeva il POST e
scriveva un messaggio globale, ma non rappresentava la scelta confermata, non
usava `job.feedback` alla riapertura e non impediva invii concorrenti generati
da clic ripetuti.

## Correzione

File applicativo modificato: `api/knowledge_panel.html`.

- stato iniziale privo di spunte;
- indicatore `Salvataggio feedback…` e pulsanti disabilitati durante il POST;
- conferma soltanto se la risposta server contiene lo stesso `job_id` e lo
  stesso valore richiesto;
- spunta verde, stato `aria-pressed` e messaggio `Feedback registrato.` dopo
  conferma reale;
- nessuna falsa conferma su errore; il voto precedentemente persistito, se
  presente, resta visualizzato e l'utente può riprovare;
- `renderResult()` ripristina lo stato usando esclusivamente `job.feedback`
  restituito dal backend;
- export Markdown e percorso domanda/risposta/fonti invariati.

Il contratto `/v1/feedback`, lo schema `rag_api_feedback_v1` e
`api/rag_v5_api.py` non sono stati modificati.

## Verifiche differenziali

Nuovo test: `tests/test_knowledge_panel_feedback_ui.js`.

- stato iniziale senza conferma: PASS;
- ripristino del feedback persistito: PASS;
- salvataggio confermato e protezione dal doppio clic: PASS;
- errore senza falsa conferma e conservazione del voto precedente: PASS.

Risultati:

- test UX differenziale: **4/4 PASS**;
- suite API esistente: **35/35 PASS**;
- esecuzione degli script inline nel test Node: PASS;
- `git diff --check`: PASS.

Non sono state eseguite inferenze Qwen, benchmark tattici, chiamate esterne,
merge o deploy.

## Decisione e stato

Decisione: mantenere invariato il backend e chiudere il difetto con il solo
delta frontend verificato.

Stato: correzione **IMPLEMENTATO**, test **ESEGUITO**, comportamento coperto
**VALIDATO offline**. La modifica non è **INTEGRATO** nel pannello pubblico e
non è **CERTIFICATO**, perché non è stata distribuita né collaudata in
produzione.

Per renderla visibile occorre in una fase separata pubblicare il commit sul
ramo previsto, distribuire il solo asset del pannello secondo la procedura
operativa esistente e svolgere uno smoke autenticato su un job già riuscito.
Questi passaggi non sono stati eseguiti.
