# V5-QUALITATIVE-EFFICACY-LIMIT-01

## Attività

Correggere l'unico FAIL del profilo integrato: una domanda sul limite di una
maggiore efficacia deve conservare il giudizio qualitativo della fonte e
distinguere esplicitamente l'assenza di misure comparative o percentuali.

## Script

- `scripts/smoke_test_rag_v5_e2e.py`
- `tests/test_v5_source_hybrid_rank_v4.py`

La guida si attiva sui concetti efficacia, maggiore/più efficace e limite. Non
usa ID benchmark, autore, pagina o testo della risposta attesa. Impedisce di
sostituire il limite probatorio con un limite didattico o temporale diverso.

## Commit, report e decisione

Commit `77e568c` — `fix: distinguish qualitative efficacy evidence`. Test
offline complessivi `13/13`, compilazione e diff check superati. Dopo
pubblicazione è consentita una sola generazione differenziale `fresh_01`; una
nuova regressione completa sarà consentita soltanto se il caso soddisfa tutti
i mandatory/forbidden claim.

## Risultato VPS

`evaluation/v5_qualitative_efficacy_fresh01_v1.json`, SHA-256
`42f7200c217c4cdd2c40ff55034c8fb04cbc481a8a997ad01d8d388b94bcc13e`.
Esecuzione `COMPLETE 1/1` in 139.16 s. La risposta copre le tre esercitazioni,
mantiene il giudizio qualitativo di Ussia e dichiara esplicitamente l'assenza
di misure, percentuali e confronti statistici. Nessun forbidden claim,
citazioni invalide 0, indici 5319/34 invariati.

## Decisione

`fresh_01` è VALIDATO. Non ripetere il differenziale. È autorizzata una sola
regressione completa del profilo integrato per verificare 10/10 e assenza di
regressioni.

## Stato

`VALIDATO` per `fresh_01`. Non ancora `INTEGRATO` nella regressione completa o
`CERTIFICATO`.
