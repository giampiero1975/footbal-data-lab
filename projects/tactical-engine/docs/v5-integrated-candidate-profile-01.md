# V5-INTEGRATED-CANDIDATE-PROFILE-01

## Attività

Integrare in un solo profilo locked le correzioni validate separatamente,
eliminando dal percorso attivo le decisioni basate sugli ID del benchmark.

## Script

- `scripts/run_rag_v5_locked_candidate_v2.py`: profilo
  `--integrated-candidate`.
- `scripts/smoke_test_rag_v5_e2e.py`: routing heading compatibile con le
  coperture concettuali.
- `scripts/v5_targeted_coverage_v1.py`: confronto Ussia/manuale attivato dai
  concetti della domanda; nessun `fresh_*` nel targeting.
- `tests/test_v5_source_hybrid_rank_v4.py`.

Il profilo unifica source-aware, exercise candidate, exact priority, targeted
coverage concettuale e heading routing V4. Non modifica Chroma o corpus.

## Commit, risultato e decisione

Commit `41c86bb` — `feat: unify V5 integrated candidate profile`. Test offline
complessivi `12/12`, compilazione dei tre script superata e diff check pulito.
Dopo pubblicazione e deploy, eseguire una sola regressione completa dei dieci
casi locked con output nuovo. Non riusare il punteggio composito come sostituto
del test integrato.

## Stato

`IMPLEMENTATO` dopo commit; non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o
`CERTIFICATO`.
