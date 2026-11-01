# Tactical State Contract generativo — correzioni offline 01

Data: 2026-11-01
Baseline revisionata: `5992c5818fecef174fde4bd21fc839f14323e0cd`
Commit tecnico: `21bfd36`

## Attività

Recepire esclusivamente i quattro rilievi della revisione indipendente sulla
copertura piano-prosa, sulla promozione fail-closed e sui tipi annidati, senza
modificare trasporto a chiamata singola, percorso legacy, retrieval, API o
pannello.

## Correzioni

1. `compare_plan_and_explanation()` espone ora `required_scope`,
   `checked_scope`, `unassessed_scope` e `coverage_sufficient`. Scope critico
   vuoto o relazioni non verificabili deterministicamente restituiscono
   `not_assessable`, non un passaggio positivo.
2. `generation_diagnostic()` assegna `validated` soltanto quando tutte le
   verifiche obbligatorie sono valutabili e superate. Fallimenti dimostrati
   restano `blocked`; insufficienza di copertura resta `not_evaluable`.
3. `validate_generation_shape()` controlla separatamente contenitori, elementi
   annidati, stati e riferimenti tipizzati. Gli errori di forma sono conservati
   con codici specifici e non raggiungono la promozione di `answer`.
4. Lo schema di trasporto resta distinto da `validate_contract()`: il primo
   controlla forma e parsing, il secondo applica le regole del dominio
   `tactical_state_contract_v1`.

Non sono state aggiunte regex tattiche ad hoc. Le sostituzioni, le espulsioni,
le rotazioni, i mapping e le assegnazioni che non possono essere dimostrati
integralmente dal controllo conservativo rimangono esplicitamente non
valutabili.

## Test

Cinque test differenziali nuovi coprono:

- scope critico vuoto;
- sostituzione citata ma direzione/effetto non verificabili;
- audit documentale non valutabile;
- contenitore annidato di stato invalido;
- riferimento tipizzato malformato.

Suite generativa: 24/24 PASS.

Regressione mirata complessiva, comprendente contratto, planner/audit e API:
159/159 PASS.

Compilazione in memoria dei due file modificati: 2/2 PASS.
`git diff --check`: PASS.

## Risultato, decisione e stato

- correzioni: **IMPLEMENTATO**;
- test: **ESEGUITO**;
- comportamento fail-closed coperto: **VALIDATO** offline;
- singola chiamata, assenza di repair e default legacy: invariati;
- runtime Ollama/Qwen e qualità generativa: **DA FARE**;
- API, pannello, corpus, indici e deploy: invariati;
- non **INTEGRATO** e non **CERTIFICATO**.

Nessuna inferenza, attività SSH/VPS o esecuzione runtime è stata effettuata.
