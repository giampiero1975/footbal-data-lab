# V5-HYBRID-CANDIDATE-INTERNAL-ASSESSMENT-02

Data: 2026-10-24. Stato: ESEGUITO.

## Attività

Aggiornare l'audit interno locked senza ripetere le nove generazioni non
influenzate dal routing heading. Si riusano gli esiti documentati in
`v5-locked-candidate-internal-assessment-01.md` e si sostituisce soltanto
`fresh_03` con la nuova evidenza V4 tecnicamente distinta.

## Script

Nessun nuovo script o runtime. Valutazione read-only dei report già prodotti.

## Commit

Il commit di questo report costituisce la traccia dell'audit.

## Report

- Baseline audit: `docs/v5-locked-candidate-internal-assessment-01.md`.
- Nuova evidenza: `evaluation/v5_source_hybrid_generation_fresh03_v1.json`,
  SHA-256 `d446a18cf18ed9b7ec4fd7b6e8f751188b82fc222adda12927982e6196bf4a6e`.

## Risultato

`fresh_03` passa da FAIL a PASS: la risposta nomina `3-4-2-1`, `3-5-2`,
`4-3-3`, `4-4-2`, cita F1–F4 e dichiara che senza evidenze comparative il
cambio modulo non dimostra un effetto causale sul rischio.

Esiti combinati:

- PASS: `fresh_02`, `fresh_03`, `fresh_04`, `fresh_05`, `fresh_06`, `fresh_08`.
- FAIL invariati: `fresh_01`, `fresh_07`, `fresh_09`, `fresh_10`.
- Totale interno: `6/10`.

## Decisione

La soglia `9/10` non è raggiunta. Non ripetere il benchmark completo: nove casi
non hanno ricevuto una differenza tecnica. Proseguire con diagnosi e correzioni
distinte sui quattro FAIL residui, iniziando dalle evidenze già disponibili per
`fresh_10`, quindi `fresh_07`, `fresh_01` e `fresh_09`. Il valore ufficiale
locked resta `5/10` finché la configurazione non è integrata e sottoposta a una
valutazione complessiva; `6/10` è audit interno composito.

## Stato

`ESEGUITO`. Non `VALIDATO`, `INTEGRATO` o `CERTIFICATO` come sistema completo.
