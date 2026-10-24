# RAG-V5-HTTP-API-VALIDATION-01

Data: 2026-10-24. Stato: VALIDATO; deployment utente INTEGRATO con limite boot.

## Attività

Validare il nuovo adattatore applicativo senza ripetere il benchmark locked:
test offline, smoke HTTP locale e una domanda arbitraria nuova.

## Evidenze

- implementazione API e runner: commit `9472564`;
- unità utente: commit `60bf7b2`;
- test offline: 3/3 PASS su token, rate limit, coda e validazione input;
- `GET /healthz`: 200;
- `GET /readyz` senza token: 401;
- `GET /readyz` con token: 200;
- servizio in ascolto soltanto su `127.0.0.1:8088`;
- file token `0600`, directory risultati `0700`;
- domanda applicativa nuova completata tramite coda e worker;
- risultato SHA-256
  `9483b5b7f4b5a04b991185c76e85a8a2680f303aef979cce6008a46965ebfc31`;
- risposta 3001 caratteri, 8 evidenze, citazioni F1–F8 valide;
- collection 5319/34 e `index_unchanged=true`.

Il risultato applicativo è un test funzionale, non un nuovo benchmark di
qualità e non estende la certificazione 10/10 a domande arbitrarie.

## Deployment

`football-rag-api.service` utente è `active` e `enabled`, circa 12M a riposo.
Il token casuale resta fuori da Git. `Linger=no`: il servizio non è garantito
al boot prima di `sudo loginctl enable-linger football`, oppure installazione
dell'unità di sistema da parte di un amministratore.

## Rollback

`systemctl --user disable --now football-rag-api.service`. La pipeline CLI,
Ollama, modelli e Chroma non vengono modificati.

## Decisione

API VALIDATA e integrata come servizio locale di sessione. Non esporre la porta
direttamente su Internet. Persistenza boot e collegamento dell'applicazione
restano attività separate.
