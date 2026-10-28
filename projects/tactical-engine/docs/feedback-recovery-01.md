# Feedback persistente — recovery 01

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit codice/test: `8102eb1`

## Attività

Correggere `RD-FEEDBACK-RECOVERY-01` senza cambiare il contratto pubblico
`/v1/feedback`, lo schema `rag_api_feedback_v1` o l'archivio esistente.

## Correzione

- `record_feedback()` tenta il recupero con `persisted_job()` quando il job non
  è più nella memoria del processo.
- Il feedback continua a essere accettato soltanto per job `succeeded`.
- `persisted_job()` associa il sidecar feedback valido alla rappresentazione
  recuperata.
- Anche la lettura di un job ancora in memoria espone il feedback già salvato.
- Il loader verifica schema, associazione esatta al `job_id` e tipo booleano.
- La scrittura resta atomica, privata e usa un solo sidecar per job; un nuovo
  voto aggiorna intenzionalmente il voto dello stesso job senza duplicarlo.

## Verifiche

Nuovi casi differenziali:

- job riuscito recuperato dopo riavvio;
- job persistito ma fallito;
- sidecar associato a un job diverso;
- aggiornamento atomico senza duplicati o file temporanei residui.

La suite API completa passa **28/28**, insieme a compilazione e diff check.

## Limiti e decisione

Questa attività rende affidabile la raccolta e la consultazione. Non trasforma
un voto utile/non utile in diagnosi tattica, correzione validata o apprendimento
automatico.

Stato: correzione **IMPLEMENTATO**, test **ESEGUITO**, recovery offline
**VALIDATO**; nessun deploy, quindi non **INTEGRATO** in produzione e non
**CERTIFICATO**.
