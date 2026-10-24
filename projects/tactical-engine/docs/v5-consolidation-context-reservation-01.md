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

La V1 `evaluation/v5_consolidation_context_fresh09_v1.json`, SHA-256
`39a8678d9831ee350a83856480dd2bb68df85a0495ace03278a4b7267f21d410`,
è `COMPLETE 1/1` in 69.32 s e copre tutti i mandatory claim, ma include ancora
passaggi estranei sul possesso avversario consolidato e sul raddoppio
difensivo. Citazioni invalide 0 e indici 5319/34 invariati. Stato V1:
`ESEGUITO`, non `VALIDATO`; non ripetere la stessa configurazione.

Il filtro contestuale V2 è implementato nel commit `1bbfb60`: conserva i
promossi e, fra gli altri, soltanto i passaggi dello stesso manuale che citano
consolidare, riconquista o recuperatore; registra gli esclusi. Test offline
complessivi `11/11`, compilazione superata. È autorizzata una sola V2 in
`evaluation/v5_consolidation_context_fresh09_v2.json`.

La V2, SHA-256
`b73e17b767d913a6230c0d76b974ea563f03554640778068e90a3d9aa4169e55`,
è `COMPLETE 1/1` in 60.23 s, mandatory claim completi, citazioni invalide 0 e
indici 5319/34 invariati. Rimane però un falso positivo: il marker generico
`riconquista` conserva il passaggio difensivo «riconquista del territorio» e
la risposta lo trasforma in rischio accessorio. Stato V2: `ESEGUITO`, non
`VALIDATO`. La V3 restringe il marker a «dopo una riconquista», commit
`c9a41e8`; test offline 11/11 e compilazione superati. È autorizzata una sola
V3 in `evaluation/v5_consolidation_context_fresh09_v3.json`.

## Stato

V1 `ESEGUITO`; filtro V2 `IMPLEMENTATO`. Non `VALIDATO`, `INTEGRATO` o
`CERTIFICATO`.
