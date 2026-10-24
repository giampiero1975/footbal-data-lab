# V5-RUNTIME-FINGERPRINT-FREEZE-01

## Attività

Congelare in modo riproducibile il runtime del profilo integrato V5 senza
includere credenziali, cache o documenti privati.

## Script

`scripts/fingerprint_v5_integrated_runtime.py` registra commit/branch,
pulizia dei file tracciati, versione Python, versioni delle librerie critiche,
modelli Ollama, hash degli entry point e del manifest, configurazione e conteggi
delle due collection. Verifica gli invarianti 5319/34 e non scrive negli indici.

## Commit, report e decisione

Commit `5262067` — `feat: fingerprint integrated V5 runtime`; compilazione e
diff check superati. Dopo pubblicazione è consentita una sola
esecuzione VPS con output `evaluation/v5_integrated_runtime_fingerprint_v1.json`.

## Stato

`IMPLEMENTATO` dopo commit; non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o
`CERTIFICATO`.
