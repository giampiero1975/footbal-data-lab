# TSC V2 Generative Handoff — implementazione offline 01

## Attività

`RD-TSC-V2-GENERATIVE-HANDOFF-IMPLEMENTATION-01`

## Script

- `scripts/v5_tactical_state_generation_v2.py`
- `scripts/smoke_test_rag_v5_e2e.py`
- `scripts/run_rag_v5_query.py`
- `tests/test_v5_tactical_state_generation_v2.py`

Il modulo generativo V2 proietta i soli requisiti `explicit_representable`, copia il
question plan V1 e materializza nel solo applied plan V2 uno stato conforme a V1 per
ogni fase canonica. L'identità è `state:phase:<canonical_phase>`: non dipende da
ordine, timestamp o testo generato e requisiti compatibili nella stessa fase
condividono lo stato. Non vengono creati eventi, movimenti, transizioni o variazioni
di cardinalità.

Il preflight fail-closed precede il trasporto. Input malformati sono `blocked`;
requisiti ambigui, inferiti, sottospecificati o non rappresentabili sono
`not_evaluable`. Il percorso opt-in `--tactical-state-contract-v2` è mutuamente
esclusivo con V1 e tactical plan, non appartiene a `DEFAULT_PROFILE_FLAGS` e può
raggiungere `_ollama_chat_once()` al massimo una volta. Non esistono retry o repair.

La diagnostica conserva separatamente validazione strutturale V1/V2, compatibilità
domanda-piano, copertura operativa V2, blocchi canonici piano-spiegazione e audit
documentale. Solo `validated` promuove `answer`; `blocked` e `not_evaluable` lasciano
la risposta vuota.

## Commit tecnico

`307064c` — `feat(tactical-engine): add TSC V2 generative handoff`

## Risultato

Comando eseguito:

`python -m unittest projects/tactical-engine/tests/test_v5_tactical_state_generation_v2.py`

Risultato: **13/13 PASS** in 0,176 s. Coperti: fase negativa esplicita, identità
stabile, deduplicazione per fase, fase ambigua senza trasporto, riferimento di fase
risolvibile, divergenza fail-closed, incompatibilità V1, immutabilità del question
plan, proiezione malformata, riuso schema V2, singola chiamata simulata/zero repair,
default legacy e separazione diagnostica V1/V2.

`git diff --check`: PASS prima del commit tecnico.

## Decisione e stato

- codice: **IMPLEMENTATO**;
- test differenziali offline: **ESEGUITO**;
- proprietà sopra elencate: **VALIDATO** offline;
- inferenza/runtime, API, pannello, retrieval e collection: non eseguiti e invariati;
- integrazione runtime: **BLOCCATO**;
- certificazione: **BLOCCATO**.

Questa validazione non dimostra qualità generativa, compatibilità Ollama/Qwen o
comportamento in produzione.
