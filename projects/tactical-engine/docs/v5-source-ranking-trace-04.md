# V5-SOURCE-RANKING-TRACE-04

## Attività

Rendere ispezionabili i punteggi con cui V3 ordina i manuali candidati, senza
ripetere generazione o benchmark. Il differenziale V3 ha dimostrato una scelta
errata della fonte, ma il report non contiene punteggi, formazioni disponibili
per fonte o numerosità degli estratti usati nel profilo. L'evidenza precedente è
quindi insufficiente per progettare V4.

## Script

- `scripts/v5_source_semantic_rank_v3.py`
- `scripts/v5_heading_reservation_v2.py`
- `scripts/smoke_test_rag_v5_e2e.py`
- `scripts/run_rag_v5_locked_candidate_v2.py`
- `tests/test_v5_source_semantic_rank_v3.py`

Il nuovo flag `--source-ranking-trace` è opt-in e accettato soltanto insieme a
`--heading-routing --retrieval-only`. Il report aggiunge, per ciascuna fonte
eleggibile, `source`, `score`, `formations` e `profile_excerpt_count`. Non cambia
la selezione V3, non invoca la generazione e non scrive nella collection.

## Commit

`1355110` — `feat: trace V5 semantic source ranking`.

## Report

Questo documento registra l'implementazione. Il report runtime previsto è
`evaluation/v5_source_ranking_trace_fresh03_v1.json`.

## Risultato

- Test offline: `2/2` superati.
- Compilazione sintattica dei quattro script e del test: superata.
- `git diff --check`: superato.
- Esecuzione VPS: `DA FARE`.

## Decisione

Consentire una sola esecuzione VPS retrieval-only su `fresh_03`. Non eseguire
generazione e non aggiornare il benchmark locked. Usare i punteggi risultanti
per decidere se una V4 possiede una differenza tecnica giustificata.

## Stato

`IMPLEMENTATO`. Non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o `CERTIFICATO`.
