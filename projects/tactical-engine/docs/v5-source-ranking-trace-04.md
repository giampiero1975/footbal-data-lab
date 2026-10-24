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

Report runtime VPS:
`evaluation/v5_source_ranking_trace_fresh03_v1.json`.

SHA-256:
`c29689e627798bf88c4f4b64b7e72ba0aa5e51d52fa1ae798c76cb611b9639a9`.

## Risultato

- Test offline: `2/2` superati.
- Compilazione sintattica dei quattro script e del test: superata.
- `git diff --check`: superato.
- Esecuzione VPS retrieval-only: completata `1/1` in `6.73 s`.
- Chroma invariato: `5319 -> 5319`; `index_unchanged=true`.
- Prima fonte: `Manuale_Diagonali_Difensive`, score `-4.685579299926758`,
  formazioni `4-2-3-1`, `4-3-3`, `4-4-2`.
- Seconda fonte: `FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale`,
  score `-5.848974227905273`, formazioni `3-4-2-1`, `3-5-2`, `4-3-3`,
  `4-4-2`.
- Margine semantico della fonte selezionata sulla fonte pertinente: circa
  `1.163395`.
- Nessuna generazione eseguita; citazioni assenti come previsto.

## Decisione

La causa del fallimento V3 è dimostrata: il solo score semantico privilegia la
somiglianza lessicale con difesa/rischio, mentre non considera la copertura
dell'insieme di heading disponibile per fonte. Non ripetere questa diagnostica
e non eseguire generazione. Una V4 è giustificata soltanto se combina score
semantico e copertura richiesta dalla domanda in modo generico, senza ID locked
o lista hardcoded delle quattro formazioni. Benchmark locked invariato a `5/10`.

## Stato

`ESEGUITO`. Non `VALIDATO`, `INTEGRATO` o `CERTIFICATO`.
