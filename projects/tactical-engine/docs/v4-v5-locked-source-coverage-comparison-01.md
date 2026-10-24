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

## Risultato

Report SHA-256 `7e16980a7ef014b991e4c92905e85a490163bf19420368dbbb7109566fa38f56`.
V4: 0/10 casi con tutte le fonti gold; V5: 10/10. V4 non contiene Ussia,
Foscarini o i due manuali interni richiesti. Nessuna scrittura agli indici.

## Decisione

Il confronto di copertura è VALIDATO. Una generazione V4 sul manifest locked
non è eleggibile e non va eseguita: misurerebbe risposte prive delle fonti
ammissibili, non la qualità comparativa della pipeline. Il vantaggio V5 sul
perimetro locked è anzitutto di copertura corpus.

## Stato

`VALIDATO` per la copertura; non `CERTIFICATO`.
