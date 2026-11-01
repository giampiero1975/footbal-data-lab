# Tactical State Contract generativo — implementazione offline 01

Data: 2026-11-01
Branch: `codex/tactical-state-contract-v1`
Baseline: `95172fb23ef758ecb711bf61880838891c53f0e1`
Commit tecnico: `acb7f7178e971173dbde1b6ff742fa5b67eebc5c`

## Attività

Implementare il percorso opt-in `--tactical-state-contract` con una sola
chiamata generativa, senza attivare `--tactical-plan`, repair generativo,
profilo pubblico, API o pannello.

La differenza tecnica rispetto alle suite concluse è il collegamento offline
fra trasporto strutturato, dominio `tactical_state_contract_v1`, quattro
controlli indipendenti e contratto fail-closed del runner.

## Script

- `scripts/v5_tactical_state_contract_v1.py`: schema di trasporto, parsing,
  normalizzazioni rappresentazionali, compatibilità domanda-piano,
  coerenza piano-prosa e diagnostica aggregata;
- `scripts/smoke_test_rag_v5_e2e.py`: ramo generativo separato
  `chat_tactical_state_once()`, con una sola invocazione del trasporto;
- `scripts/run_rag_v5_query.py`: esposizione esplicita del flag e rifiuto dei
  risultati diversi da `validated`;
- `tests/test_v5_tactical_state_generation_v1.py`: 19 test differenziali.

`DEFAULT_PROFILE_FLAGS` è invariato e non contiene né
`--tactical-state-contract` né `--tactical-plan`.

## Controlli distinti

La diagnostica conserva separatamente:

1. validità strutturale dell'applied plan;
2. copertura e compatibilità rispetto ai fatti espliciti della domanda;
3. coerenza fra applied plan e spiegazione per le relazioni strutturali
   determinabili;
4. audit tattico/documentale preesistente.

Gli stati generativi `validated`, `partial`, `blocked` e `not_evaluable` non
sono stati del progetto. La prima versione non promuove risultati `partial`.
Solo `validated` valorizza il campo legacy `answer`; negli altri casi la prosa
rimane nel raw output diagnostico e il wrapper termina `INCOMPLETE`.

## Risultato dei test

Comando differenziale:

```text
python -B -m unittest projects/tactical-engine/tests/test_v5_tactical_state_generation_v1.py
```

Risultato: 19/19 PASS.

Regressioni mirate:

```text
python -B -m unittest \
  projects/tactical-engine/tests/test_v5_tactical_state_generation_v1.py \
  projects/tactical-engine/tests/test_v5_tactical_state_contract_v1.py \
  projects/tactical-engine/tests/test_v5_tactical_query_plan_v1.py \
  projects/tactical-engine/tests/test_rag_v5_api.py
```

Risultato complessivo: 154/154 PASS.

Compilazione in memoria dei quattro file modificati: `COMPILE_OK 4`.
`git diff --check`: PASS.

Non sono state eseguite inferenze Qwen/Ollama, benchmark, SSH/VPS, modifiche
alla collection, deploy o prove sul pannello.

## Decisione e stato

- codice: **IMPLEMENTATO**;
- test differenziali e regressioni mirate: **ESEGUITO**;
- proprietà dimostrate offline (singola chiamata, fail-closed, separazione dei
  controlli e compatibilità legacy): **VALIDATO** nel solo perimetro offline;
- compatibilità effettiva `format` con Ollama/Qwen: **DA FARE**;
- qualità tattica e stabilità runtime: **DA FARE**;
- API, pannello e profilo pubblico: non modificati;
- percorso non **INTEGRATO** e non **CERTIFICATO**.

L'eventuale prova runtime richiede una nuova decisione e non è autorizzata da
questa implementazione.
