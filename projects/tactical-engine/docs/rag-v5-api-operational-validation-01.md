# RAG-V5-API-OPERATIONAL-VALIDATION-01

Data: 2026-10-24. Stato: VALIDATO per carico controllo e recovery.

## Attività

Verificare carico concorrente senza generazioni duplicate, recupero del servizio
e disponibilità di un client applicativo riusabile.

## Evidenze

- commit client/probe/template: `d9eafc1`;
- 500 richieste `healthz`, concorrenza 25: 500/500 HTTP 200;
- latenza ms: min 0.43, mediana 3.36, media 76.16, massimo 1711.98;
- readiness autenticata: HTTP 200, 3.89 ms;
- job RAG avviati dal test: 0;
- report VPS SHA-256
  `51e491ab7b5336ce44604a433d215b4dbab3fc8e0eddad5231393766d5064ff9`;
- kill controllato del processo principale: systemd lo ha riavviato con nuovo
  PID, health ripristinato e `NRestarts=1`;
- memoria dopo recovery: circa 11M.

## Integrazione applicativa

`api/rag_v5_client.py` implementa submit, polling e deadline tramite sola
libreria standard. L'adattatore è pronto; nel repository non è presente il
codice dell'applicazione consumer da collegare.

## HTTPS

`deploy/nginx-football-rag-api.conf.example` definisce TLS, redirect HTTP,
body limit, timeout e rate limit, mantenendo upstream su localhost. La VPS non
ha Nginx/Caddy/Apache installati e non dispone di un dominio pubblico nel
repository o nel DNS verificato. Installazione e certificato restano sospesi
fino alla scelta del nome DNS; non esporre direttamente la porta 8088.

## Decisione

Carico del control plane e recovery VALIDATI. Non eseguire più inferenze per
simulare concorrenza: CPU e worker sono intenzionalmente serializzati. Collegare
il client al consumer reale quando disponibile. Pubblicare HTTPS soltanto dopo
DNS e certificato validi.
