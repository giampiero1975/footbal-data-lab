# V5-SOURCE-HYBRID-RANK-V4

## Attività

Correggere la selezione V3 dimostrata da `V5-SOURCE-RANKING-TRACE-04` senza
hardcoding di benchmark, fonti o moduli. V3 sceglie il massimo score semantico
anche quando una fonte semanticamente vicina offre una copertura di heading più
completa.

## Script

- `scripts/v5_source_hybrid_rank_v4.py`
- `scripts/v5_source_semantic_rank_v3.py`
- `scripts/v5_heading_reservation_v2.py`
- `scripts/smoke_test_rag_v5_e2e.py`
- `tests/test_v5_source_hybrid_rank_v4.py`

V4 usa il miglior punteggio semantico come gate. Considera competitive soltanto
le fonti entro `1.5` punti dal leader; fra queste privilegia il numero di
formazioni disponibili e usa score e nome come tie-break deterministici. Fonti
oltre il margine non possono vincere per sola copertura.

## Commit

`30b04d4` — `feat: rank V5 sources by relevance and coverage`.

## Report

Report VPS retrieval-only:
`evaluation/v5_source_hybrid_rank_fresh03_v1.json`.

SHA-256:
`51f01a0280434501b6eb2f1d6fedc6adcd92198f88a7c6c26c19c7c145367ab2`.

## Risultato

- Test offline V3/V4: `5/5` superati.
- Compilazione sintattica: superata.
- `git diff --check`: superato.
- Esecuzione VPS retrieval-only: completata `1/1` in `7.21 s`.
- Chroma invariato: `5319 -> 5319`.
- Fonte selezionata:
  `FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale`.
- Heading riservati: `3-4-2-1`, `3-5-2`, `4-3-3`, `4-4-2`.
- Le sole fonti competitive entro il margine sono il leader semantico con tre
  heading e la fonte selezionata con quattro heading.
- Nessuna generazione eseguita.

## Decisione

Il retrieval V4 è validato per `fresh_03`. La differenza tecnica rispetto a V3
è verificata e consente una sola generazione differenziale con
`--heading-routing`, senza targeted coverage. Non modificare Chroma o benchmark
prima della valutazione claim-level della risposta.

## Stato

`VALIDATO` limitatamente al retrieval. Non `INTEGRATO` o `CERTIFICATO`.
