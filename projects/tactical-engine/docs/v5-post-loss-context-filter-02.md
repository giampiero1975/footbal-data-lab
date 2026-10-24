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

Output VPS: `evaluation/v5_post_loss_context_fresh10_v2.json`.
SHA-256: `25c19cf4497ff4205d016a24e14a55e24c164ddaa8c988d78bed61541c92dc60`.

## Risultato

- Test offline complessivi: `8/8` superati.
- Compilazione sintattica: superata.
- Esecuzione VPS: `COMPLETE 1/1` in 93.89 s.
- Evidenze finali: Ussia F1-F2 e manuale interno F3; cinque evidenze di
  pressing generale escluse e registrate in `post_loss_excluded_ids`.
- Mandatory claim Ussia: presenti adattamento al sistema e rapporto fra
  pressione individuale/collettiva.
- Mandatory claim manuale: presenti prossimità, orientamento avversario,
  prevedibilità dell'uscita e copertura preventiva.
- Forbidden claim: assente; rimessa laterale, fuorigioco e pressing alto
  generico non compaiono come condizioni post-perdita.
- Citazioni invalide: 0. Chroma baseline 5319 -> 5319; candidate 34 -> 34.

## Decisione

La differenza tecnica risolve il difetto osservato nella V1. `fresh_10` è
validato nel perimetro della configurazione opt-in testata. Non ripetere la
generazione; il risultato non implica integrazione di default o certificazione
del sistema.

## Stato

`VALIDATO`. Non `INTEGRATO` o `CERTIFICATO`.
