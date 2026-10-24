# RAG-V5-HTTP-API-CONTRACT-01

Data: 2026-10-24. Stato: VALIDATO.

## Perimetro

Esporre domande applicative tramite lo stesso percorso V5 integrato senza
modificare il wrapper locked certificato. L'API è una candidata applicativa:
il 10/10 locked non certifica automaticamente domande arbitrarie o il servizio.

## Contratto

- `GET /healthz`: processo vivo, senza autenticazione e senza chiamate modello;
- `GET /readyz`: autenticato, verifica runner/interprete e Ollama;
- `POST /v1/query`: Bearer token, body esatto `{"question":"..."}`, risposta
  `202` con ID job;
- `GET /v1/jobs/{id}`: stato autenticato e risultato quando completato.

Vincoli: domanda 10–2000 caratteri, body massimo 16 KiB, coda predefinita 8,
un solo worker, 10 richieste/minuto per IP e timeout runner 900 secondi. Il
token deve avere almeno 32 caratteri. Log HTTP senza domanda né token.

## Sicurezza e deployment

Bind predefinito `127.0.0.1:8088`; nessuna esposizione Internet diretta.
Configurazione segreta in `/etc/football-data-lab/rag-api.env`, fuori da Git.
Unit file candidata `deploy/football-rag-api.service` con utente non root,
filesystem protetto e unica directory scrivibile `evaluation/api-runs`.
È disponibile anche `deploy/football-rag-api.user.service` per deployment senza
privilegi. Sulla VPS il linger dell'utente `football` è stato abilitato e
verificato (`Linger=yes`) il 2026-10-24.

## Rollback

Fermare/disabilitare l'unità API. La pipeline CLI certificata e Ollama restano
indipendenti. Nessuna modifica a Chroma o ai modelli.

## Stato

VALIDATO con test offline, smoke HTTP e una domanda applicativa nuova. Evidenze
in `docs/rag-v5-http-api-validation-01.md`.
