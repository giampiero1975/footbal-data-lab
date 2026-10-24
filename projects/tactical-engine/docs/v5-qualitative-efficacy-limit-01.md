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

## Stato

`IMPLEMENTATO` dopo commit; non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o
`CERTIFICATO`.
