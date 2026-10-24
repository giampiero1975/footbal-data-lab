# V5-HYBRID-CANDIDATE-INTERNAL-ASSESSMENT-04

Data: 2026-10-24. Stato: ESEGUITO.

## Attività

Aggiornare l'audit composito senza ripetere i nove casi non influenzati dal
filtro di fonte nominata e dalla guida laterali/zona B. Si riusa l'assessment
03 e si sostituisce soltanto `fresh_07` con la V2 VALIDATA.

## Script

Nessun nuovo runtime. Valutazione read-only dei report già prodotti.

## Report

- Baseline: `docs/v5-hybrid-candidate-internal-assessment-03.md`.
- Evidenza: `evaluation/v5_named_source_context_fresh07_v2.json`, SHA-256
  `9da89f8287a02504445501800fbf73df6c752603f30b9a043216ae51ee40b371`.
- Review: `docs/v5-named-source-context-filter-01.md`.

## Risultato

- PASS: `fresh_02`, `fresh_03`, `fresh_04`, `fresh_05`, `fresh_06`,
  `fresh_07`, `fresh_08`, `fresh_10`.
- FAIL invariati: `fresh_01`, `fresh_09`.
- Totale interno: `8/10`.

## Decisione

La soglia `9/10` non è ancora raggiunta. Proseguire su `fresh_09` usando le
evidenze esistenti e una differenza tecnica documentata; non ripetere gli otto
casi PASS. Il valore ufficiale locked resta 5/10 fino a integrazione e
regressione complessiva.

## Stato

`ESEGUITO`. Non `VALIDATO`, `INTEGRATO` o `CERTIFICATO` come sistema completo.
