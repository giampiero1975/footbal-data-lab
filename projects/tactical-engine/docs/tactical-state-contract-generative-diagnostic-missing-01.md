# Tactical State Contract generativo — propagazione diagnostica missing 01

Data: 2026-11-01
Baseline: `d4de177415c8633cf6b93a4034c21d4a05c90bbd`
Commit codice: `480cd9e8f73cd3f2e3fcd54235d6d5c6245935fb`
Commit test: `42a97b2dc3f64d7aff177fc1e23a2d8c7f92e812`

## Attività → Script → Commit → Report → Risultato → Decisione → Stato

Correzione minima in `generation_diagnostic()` per aggiungere i codici di `question_alignment.missing` a `reasons` mantenendo la deduplicazione finale. Un solo test differenziale aggiunto, che controlla `blocked`, `failed_scope`, `missing`, `reasons` e `promoted_answer` vuoto.

Risultato verificato: commit pubblicati su GitHub. **Non sono stati eseguiti test** in questa sessione: il repository privato non è disponibile nell'ambiente locale e il connettore GitHub non offre esecuzione. Nessuna attestazione PASS è possibile.

Decisione: prima della convalida offline eseguire solo il test mirato, ad esempio `python -B -m unittest projects/tactical-engine/tests/test_v5_tactical_state_generation_v1.py` (suite generativa, senza ripetere campagne storiche). Stato: codice **IMPLEMENTATO**; verifica **BLOCCATO** finché non vengono acquisiti risultati eseguibili; non **INTEGRATO** né **CERTIFICATO**. Nessuna inferenza, runtime, VPS o deploy.
