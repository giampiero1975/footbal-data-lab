# Tactical State Contract generativo — propagazione diagnostica missing 01

Data: 2026-11-01
Baseline: `d4de177415c8633cf6b93a4034c21d4a05c90bbd`
Commit codice: `480cd9e8f73cd3f2e3fcd54235d6d5c6245935fb`
Commit test: `42a97b2dc3f64d7aff177fc1e23a2d8c7f92e812`

## Attività → Script → Commit → Report → Risultato → Decisione → Stato

Correzione minima in `generation_diagnostic()` per aggiungere i codici di `question_alignment.missing` a `reasons` mantenendo la deduplicazione finale. Un solo test differenziale aggiunto, che controlla `blocked`, `failed_scope`, `missing`, `reasons` e `promoted_answer` vuoto.

Risultato verificato: commit pubblicati su GitHub. Il 2026-11-01 è stato
eseguito esclusivamente il test differenziale mirato
`ContractGenerationTests.test_incomplete_question_alignment_reports_missing_reasons`:
1 test in 0,004 s, esito `OK`. Il caso verifica congiuntamente stato
`blocked`, `question_compatibility` in `failed_scope`, dettaglio `missing`
preservato, codice `missing_contract_field` propagato in `reasons` e
`promoted_answer` vuoto. La deduplicazione delle motivazioni resta preservata
da `list(dict.fromkeys(reasons))`.

Decisione: correzione diagnostica **VALIDATO offline** nel solo perimetro del
test differenziale. Codice **IMPLEMENTATO**, test **ESEGUITO**; percorso
generativo non **INTEGRATO** né **CERTIFICATO**. Nessuna suite o campagna
storica ripetuta; nessuna inferenza, runtime, VPS o deploy.
