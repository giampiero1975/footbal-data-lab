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

## Risultato

Report SHA-256 `55a117b045c9420660f13f4ba192b292954587e79f202e8f300931b3f351a2eb`.
Commit runtime `37fee73b1426f39c54149a86cc5c52efc28d484c`, file tracciati puliti,
Python 3.12.3, Chroma 1.5.9, llama-index-embeddings-ollama 0.10.0,
sentence-transformers 6.1.0, torch 2.6.0+cpu, Ollama 0.40.5. Modelli:
Qwen3 Embedding ID `ac6da0dfba84`, Qwen3.5 9B ID `56671c2ab938`.
Collection e configurazioni registrate; invarianti 5319/34 superati.

## Decisione

Fingerprint VALIDATO e configurazione candidata congelata. Ogni variazione di
hash, versione, modello o collection richiede una nuova evidenza; non ripetere
questo fingerprint a runtime invariato.

## Freeze definitivo post-promozione

La promozione del wrapper ha richiesto un nuovo fingerprint. Report V2
`evaluation/v5_integrated_runtime_fingerprint_v2.json`, SHA-256
`f5718a39978495894964f79c4a9b5f4be42277affde88fe692b5382cb7c6cca9`;
commit runtime `e46746afa005412c1db60040310c0f6d84de27da`, tracked clean, invarianti e
versioni immutati. Nuovo hash wrapper:
`bafb61c30474e4946ba0a8d91b733363e3e7830fda0cb196cc37c5ed2130780e`.
Questo V2 sostituisce il V1 come freeze autorevole.

## Stato

`VALIDATO` come evidenza di freeze; acquisito dal closeout complessivo
`V5-CERTIFICATION-CLOSEOUT-01`, il cui stato è `CERTIFICATO`.
