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

Report VPS generativo:
`evaluation/v5_source_hybrid_generation_fresh03_v1.json`.

SHA-256 generazione:
`d446a18cf18ed9b7ec4fd7b6e8f751188b82fc222adda12927982e6196bf4a6e`.

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
- Generazione differenziale completata `1/1` in `138.78 s`.
- La risposta nomina `3-4-2-1`, `3-5-2`, `4-3-3`, `4-4-2` e associa
  rispettivamente le citazioni F1–F4.
- La risposta separa le condizioni operative di ciascun modulo dalla prova
  causale e conclude che servono evidenze comparative.
- Citazioni emesse F1, F2, F3, F4, F7, F8; citazioni invalide `0`.
- Chroma invariato anche dopo la generazione: `5319 -> 5319`.

## Decisione

Retrieval e generazione V4 sono validati per `fresh_03`. Non ripetere questi
test. Prima di integrare il comportamento di default, eseguire una verifica di
regressione sulla configurazione completa tecnicamente distinta; il benchmark
ufficiale resta `5/10` fino a quella valutazione complessiva.

## Stato

`VALIDATO` per retrieval e generazione `fresh_03`. Non `INTEGRATO` o
`CERTIFICATO`.
