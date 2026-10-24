# V5-POST-LOSS-CONTEXT-FILTER-02

## Attività

Rimuovere dal contesto generativo post-perdita le evidenze di pressing generale
che la sola guida testuale non è riuscita a escludere in modo affidabile.

## Script

- `scripts/smoke_test_rag_v5_e2e.py`
- `tests/test_v5_source_hybrid_rank_v4.py`

Il filtro si attiva genericamente per domande con perdita e
pressione/riaggressione. Conserva le evidenze targeted promosse e gli estratti
che citano esplicitamente perdita, palla persa, riaggressione o copertura
preventiva. Registra gli ID esclusi nel report. Nessun ID benchmark o nome
fonte è codificato.

## Commit

`ecad16b` — `fix: filter post-loss generation context`.

## Report

Output VPS previsto: `evaluation/v5_post_loss_context_fresh10_v2.json`.

## Risultato

- Test offline complessivi: `8/8` superati.
- Compilazione sintattica: superata.
- Esecuzione VPS: `DA FARE`.

## Decisione

Consentire una sola generazione fresh_10 con la configurazione targeted già
verificata. Validare soltanto se mandatory claim presenti, forbidden claim
assente, citazioni valide e indice invariato.

## Stato

`IMPLEMENTATO`. Non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o `CERTIFICATO`.
