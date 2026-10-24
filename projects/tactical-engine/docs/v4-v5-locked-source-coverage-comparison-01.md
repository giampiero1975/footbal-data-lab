# V4-V5-LOCKED-SOURCE-COVERAGE-COMPARISON-01

## Attività

Confrontare V4 e V5 sullo stesso manifest locked senza eseguire generazioni
prive delle fonti gold. L'inventario VPS mostra V4 con 86 chunk da due fonti
(Glerean e Giustinetti) e V5 con 5319 chunk da 141 fonti.

## Script

`scripts/compare_v4_v5_locked_source_coverage.py` verifica hash del manifest,
fonti attese per domanda e presenza nelle due collection. Non calcola embedding,
non chiama LLM e non scrive negli indici.

## Criterio

Una risposta source-grounded non è confrontabile qualitativamente se la
baseline non contiene la fonte ammessa dal gold. In quel caso il risultato
corretto è `non eleggibile`, non un punteggio generativo artificiale.

## Commit, report e decisione

Commit `12b2769` — `feat: compare locked source coverage V4 V5`.
Compilazione e diff check superati. È consentita una sola esecuzione VPS
read-only con output `evaluation/v4_v5_locked_source_coverage_v1.json`.

## Stato

`IMPLEMENTATO` dopo commit; non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o
`CERTIFICATO`.
