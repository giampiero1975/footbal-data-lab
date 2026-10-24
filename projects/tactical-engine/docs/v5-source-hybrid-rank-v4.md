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

Questo documento registra l'implementazione. Il primo report VPS autorizzato è
`evaluation/v5_source_hybrid_rank_fresh03_v1.json`, esclusivamente retrieval-only.

## Risultato

- Test offline V3/V4: `5/5` superati.
- Compilazione sintattica: superata.
- `git diff --check`: superato.
- Esecuzione VPS: `DA FARE`.

## Decisione

Consentire una sola verifica VPS con `--heading-routing --source-ranking-trace
--retrieval-only --only-ids fresh_03`. Generazione consentita soltanto se la
fonte selezionata e gli heading recuperati risultano corretti e Chroma resta
invariato.

## Stato

`IMPLEMENTATO`. Non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o `CERTIFICATO`.
