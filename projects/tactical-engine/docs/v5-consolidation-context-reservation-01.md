# V5-CONSOLIDATION-CONTEXT-RESERVATION-01

## Attività

Recuperare e riservare le condizioni e il trade-off espliciti del manuale per
domande sul consolidamento dopo riconquista, evitando la commistione con
ripiegamento e pressing difensivo osservata in `fresh_09`.

## Evidenza diagnostica

Ispezione read-only dei 62 chunk del manuale, collection invariata a 5319:

- `Quando è opportuno`, pagina 3, ID `98bd91e...`: inferiorità locale, palla
  non controllata, assenza di riceventi profondi, avversario organizzato.
- `Pro e contro`, pagina 3, ID `a1fb9f4...`: riduzione delle perdite immediate
  e tempo concesso all'avversario per ricompattarsi.

Nessun embedding, reranking o LLM eseguito nella diagnostica.

## Script

- `scripts/v5_targeted_coverage_v1.py`
- `scripts/smoke_test_rag_v5_e2e.py`
- `tests/test_v5_source_hybrid_rank_v4.py`

La riserva si attiva sui concetti consolidamento, riconquista e accelerazione;
usa fonte e headings, non ID benchmark o ID chunk.

## Commit, risultato e decisione

Commit `7004986` — `fix: reserve consolidation decision evidence`. Test offline
complessivi `10/10` e compilazione superati. È consentita una sola generazione
`fresh_09`, con mandatory/forbidden claim, citazioni e indici come gate.

## Stato

`IMPLEMENTATO` dopo commit; non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o
`CERTIFICATO`.
