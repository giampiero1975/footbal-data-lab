# V5-POST-LOSS-PRESSURE-GUIDANCE-01

## Attività

Correggere il forbidden claim residuo di `fresh_10`: la risposta targeted
contiene i mandatory claim, ma usa pressing alto, rimesse laterali e fuorigioco
come se fossero prova equivalente della riaggressione immediata dopo perdita.

## Script

- `scripts/smoke_test_rag_v5_e2e.py`
- `tests/test_v5_source_hybrid_rank_v4.py`

La guida si attiva genericamente quando la domanda contiene perdita e
pressione/riaggressione. Richiede di separare riaggressione post-perdita e
pressing generale, usare solo estratti esplicitamente collegati alla perdita e
non trattare fuorigioco o rimesse laterali come prova equivalente. Nessun ID
benchmark o nome fonte è codificato.

## Commit

`8b62956` — `fix: separate post-loss pressure guidance`.

## Report

Report runtime previsto:
`evaluation/v5_post_loss_pressure_fresh10_v1.json`.

## Risultato

- Test offline complessivi: `7/7` superati.
- Compilazione sintattica: superata.
- Esecuzione VPS: `DA FARE`.

## Decisione

Consentire una sola generazione `fresh_10` con la copertura targeted già
verificata e la nuova guida. Valutare mandatory e forbidden claim senza
equiparare citazioni valide a fedeltà.

## Stato

`IMPLEMENTATO`. Non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o `CERTIFICATO`.
