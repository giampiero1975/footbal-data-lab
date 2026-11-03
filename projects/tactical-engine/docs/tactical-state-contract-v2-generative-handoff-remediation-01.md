# TSC V2 Generative Handoff — remediation fail-closed 01

## Attività

`RD-TSC-V2-GENERATIVE-HANDOFF-REMEDIATION-01`

## Difetti confermati

1. `done_reason="length"` era conservato ma non impediva `validated`.
2. `complete=True` poteva promuovere un audit con stato o dettagli negativi.
3. `_canonical_blocks()` dereferenziava direttamente campi annidati malformati.

## Script e commit

- `scripts/v5_tactical_state_generation_v2.py`
- `tests/test_v5_tactical_state_generation_v2.py`
- commit tecnico: `8a16a73`

La remediation classifica il troncamento accertato come `not_evaluable`, salvo una
violazione dimostrata già `blocked`; l'assenza di `done_reason` non è considerata
troncamento. L'audit è positivo soltanto se `complete=True`, non presenta dettagli
negativi e non espone uno stato sconosciuto/negativo. Audit incompleto senza
violazione è `not_evaluable`; stato o dettagli negativi sono `blocked`.

Il controllo canonico valida localmente soltanto la forma dei campi che deve
confrontare. Container, relazioni, riferimenti e termini malformati producono
diagnostica strutturata senza ricostruzione o modifica del piano; il validatore V2
resta l'autorità sul dominio.

## Test eseguiti

Nuovi test differenziali, eseguiti singolarmente:

- troncamento `length`: PASS;
- audit negativo con `complete=True`: PASS;
- relazione annidata malformata: PASS.

Risultato: **3/3 PASS** in 0,015 s.

È stata inoltre rieseguita una sola regressione positiva direttamente interessata
per dimostrare che il percorso a singola chiamata non è reso sempre bloccante:
`test_v2_path_calls_transport_once_and_never_repairs`, **1/1 PASS** in 0,097 s.

La precedente campagna 13/13 e le suite V1/V2 non sono state ripetute.
`git diff --check`: PASS.

## Decisione e stato

- remediation: **IMPLEMENTATO**;
- test differenziali: **ESEGUITO**;
- proprietà fail-closed corrette: **VALIDATO** offline;
- runtime e integrazione: **BLOCCATO**;
- certificazione: **BLOCCATO**.

Nessuna inferenza, query Chroma/API, modifica a retrieval, runner, dominio, audit,
API o pannello è stata eseguita.
