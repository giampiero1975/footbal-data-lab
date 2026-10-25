# RAG V5 API observability 01

Data: 2026-10-25. Stato: VALIDATO e INTEGRATO nel pannello.

## Attività

Aggiungere osservabilità applicativa senza eseguire nuove generazioni equivalenti. Il precedente benchmark control-plane resta autorevole per health/concorrenza; questa differenza tecnica introduce metriche persistenti e interrogabili.

## Implementazione

- endpoint autenticato `GET /v1/metrics`;
- uptime, vitalità worker, profondità/capacità coda e job correnti per stato;
- contatori cumulativi accepted/succeeded/failed/timed_out;
- fino a 200 campioni di durata con min/mediana/p95/max;
- collection, expected count e stato cache catalogo;
- persistenza atomica `evaluation/api-runs/metrics.json`, senza domande, risposte o token.
- registro diagnostico append-only `events.jsonl`, limitato a transizioni del
  servizio/job, durata e motivo normalizzato; nessun contenuto di domanda,
  risposta, stderr o credenziale;
- endpoint autenticato `GET /v1/events` e vista nel pannello per gli ultimi
  eventi;
- distinzione `job_lost_after_restart` per un job presente su disco ma non più
  nella memoria del servizio dopo un riavvio.

## Evidenza VPS

- test offline 10/10;
- `/v1/metrics` 200, worker vivo, coda 0/8 e collection/count corretti;
- `metrics.json` creato atomicamente all'avvio con permessi `0600`;
- 500/500 richieste HTTP 200 a concorrenza 25, worker vivo 500/500;
- latenza metriche: min 0,61 ms, mediana 4,19 ms, media 62,83 ms, p95 411,96 ms, max 1680,21 ms;
- nessuna inferenza o scrittura Chroma durante il benchmark.

Il pannello espone ora la vista Qualità operativa: worker, coda, job completati/errori e distribuzione delle durate. Script: API, pannello e test. Commit iniziali `fbf4162`, `424a4b2`. Decisione: metriche VALIDATE e pannello INTEGRATO; raccogliere campioni reali nel tempo, mantenendo il worker seriale finché non esiste un benchmark di risorse per inferenze parallele. Stato: INTEGRATO.
