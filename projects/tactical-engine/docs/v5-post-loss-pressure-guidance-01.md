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

Report runtime:
`evaluation/v5_post_loss_pressure_fresh10_v1.json`.

SHA-256:
`d1cdad96dcdb7f5cd37fbd69e04f04f47807f2a4c6449a3c2898688d8bf321aa`.

## Risultato

- Test offline complessivi: `7/7` superati.
- Compilazione sintattica: superata.
- Esecuzione VPS completata `1/1` in `150.02 s`.
- Mandatory claim presenti: Ussia sistema + pressione individuale/collettiva
  (F2); manuale interno vicinanza, orientamento, uscita prevedibile e copertura
  preventiva (F7).
- La conclusione distingue pressing generale e riaggressione post-perdita.
- La risposta include però ancora la rimessa laterale F8 fra le condizioni
  favorevoli post-perdita: forbidden claim non risolto completamente.
- Citazioni invalide `0`; Chroma `5319 -> 5319`.

## Decisione

Non validare e non ripetere lo stesso test. La prossima variante è consentita
solo con una differenza tecnica più forte: omettere dalla risposta post-perdita
le evidenze di pressing generale, fuorigioco e rimesse laterali, anziché
limitarne verbalmente l'equivalenza.

## Stato

`ESEGUITO`. Non `VALIDATO`, `INTEGRATO` o `CERTIFICATO`.
