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

## Regressione completa e adjudication

Report VPS `evaluation/rag_v5_integrated_candidate_full_v1.json`, SHA-256
`20ec77d22cb5bb4548d6589a41aecd01e529ee53fd45fb199631d766c471c86d`.
Esecuzione `COMPLETE 10/10`, 814.98 s complessivi; citazioni invalide 0 in
tutti i casi, baseline 5319 -> 5319 e candidate 34 -> 34.

Adjudication claim-by-claim sul manifest locked:

- PASS: `fresh_02`, `fresh_03`, `fresh_04`, `fresh_05`, `fresh_06`,
  `fresh_07`, `fresh_08`, `fresh_09`, `fresh_10`.
- FAIL: `fresh_01`. La risposta descrive correttamente alta/centrale/bassa e
  conserva l'affermazione qualitativa di Ussia, ma non esplicita che mancano
  misure comparative o percentuali; propone invece come limite la progressione
  didattica e il tempo di allenamento.
- Risultato ufficiale del profilo locked integrato: `9/10`.

## Decisione

Il profilo è `INTEGRATO` nel wrapper locked e `VALIDATO` sull'intero manifest.
Non ripetere la regressione. Non è `CERTIFICATO` come sistema generale e non è
un confronto V4; `fresh_01` resta il solo FAIL documentato.

## Stato

`INTEGRATO` e `VALIDATO` nel perimetro locked. Non `CERTIFICATO`.
