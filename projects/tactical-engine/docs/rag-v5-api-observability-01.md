# RAG V5 API observability 01

Data: 2026-10-25. Stato: IMPLEMENTATO; test VPS DA FARE.

## Attività

Aggiungere osservabilità applicativa senza eseguire nuove generazioni equivalenti. Il precedente benchmark control-plane resta autorevole per health/concorrenza; questa differenza tecnica introduce metriche persistenti e interrogabili.

## Implementazione

- endpoint autenticato `GET /v1/metrics`;
- uptime, vitalità worker, profondità/capacità coda e job correnti per stato;
- contatori cumulativi accepted/succeeded/failed/timed_out;
- fino a 200 campioni di durata con min/mediana/p95/max;
- collection, expected count e stato cache catalogo;
- persistenza atomica `evaluation/api-runs/metrics.json`, senza domande, risposte o token.

Script: `api/rag_v5_api.py`; test `tests/test_rag_v5_api.py`. Commit: DA FARE. Risultato: IMPLEMENTATO. Decisione: test offline, riavvio controllato, smoke endpoint e benchmark control-plane read-only; nessuna nuova inferenza. Stato: IMPLEMENTATO.
