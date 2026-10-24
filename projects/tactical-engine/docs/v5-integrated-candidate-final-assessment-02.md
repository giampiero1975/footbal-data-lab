# V5-INTEGRATED-CANDIDATE-FINAL-ASSESSMENT-02

Data: 2026-10-24. Stato: VALIDATO.

## Attività → Script → Commit

Regressione finale del profilo `--integrated-candidate` dopo la correzione
generica del limite probatorio (`77e568c`). Runner
`run_rag_v5_locked_candidate_v2.py`; manifest locked SHA-256
`c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71`.

## Report → Risultato

`evaluation/rag_v5_integrated_candidate_full_v2.json`, SHA-256
`f2d54944085b1586067679ac76fb6e2696e5ab24d36d40e84cd3ffb2d4f76a55`.
Esecuzione unica `COMPLETE 10/10`, 824.35 s; citazioni invalide 0; baseline
5319 -> 5319 e candidate 34 -> 34.

Confronto read-only con V1:

- `fresh_01` è l'unica risposta cambiata, a evidenze identiche; ora copre le
  tre zone, conserva il giudizio qualitativo di Ussia e dichiara l'assenza di
  misure, percentuali e confronti statistici.
- `fresh_02`–`fresh_10` hanno risposta ed evidenze identiche alla V1 già
  adjudicata PASS.

Adjudication ufficiale: **10/10 PASS**.

## Decisione → Stato

Il candidato locked è `INTEGRATO` e il risultato 10/10 è `VALIDATO`. Non
ripetere questa regressione. Non dichiarare ancora `CERTIFICATO`: restano il
confronto controllato con V4, il fingerprint/freeze runtime completo e una
decisione esplicita sulla promozione del profilo nella pipeline ordinaria.
