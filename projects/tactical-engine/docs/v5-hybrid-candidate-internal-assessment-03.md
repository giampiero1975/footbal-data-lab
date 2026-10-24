# V5-HYBRID-CANDIDATE-INTERNAL-ASSESSMENT-03

Data: 2026-10-24. Stato: ESEGUITO.

## Attività

Aggiornare l'audit composito senza ripetere le nove generazioni non influenzate
dal filtro contestuale post-perdita. Si riusa l'assessment 02 e si sostituisce
soltanto `fresh_10` con la nuova evidenza differenziale VALIDATA.

## Script

Nessun nuovo script o runtime. Valutazione read-only dei report già prodotti.

## Commit

Il commit di questo report costituisce la traccia dell'audit.

## Report

- Baseline audit: `docs/v5-hybrid-candidate-internal-assessment-02.md`.
- Nuova evidenza: `evaluation/v5_post_loss_context_fresh10_v2.json`,
  SHA-256 `25c19cf4497ff4205d016a24e14a55e24c164ddaa8c988d78bed61541c92dc60`.
- Review: `docs/v5-post-loss-context-filter-02.md`.

## Risultato

`fresh_10` passa da FAIL a PASS: sono presenti i mandatory claim di Ussia e
del manuale interno, mentre rimessa laterale, fuorigioco e pressing alto
generico non sono usati come prova equivalente della riaggressione dopo
perdita. Citazioni invalide zero e indici invariati.

Esiti combinati:

- PASS: `fresh_02`, `fresh_03`, `fresh_04`, `fresh_05`, `fresh_06`, `fresh_08`, `fresh_10`.
- FAIL invariati: `fresh_01`, `fresh_07`, `fresh_09`.
- Totale interno: `7/10`.

## Decisione

La soglia `9/10` non è ancora raggiunta. Non ripetere il benchmark completo:
proseguire con differenze tecniche documentate su `fresh_07`, `fresh_01` e
`fresh_09`. Il valore ufficiale locked resta `5/10` finché la configurazione
non è integrata e sottoposta a regressione complessiva; `7/10` è un audit
interno composito.

## Stato

`ESEGUITO`. Non `VALIDATO`, `INTEGRATO` o `CERTIFICATO` come sistema completo.
