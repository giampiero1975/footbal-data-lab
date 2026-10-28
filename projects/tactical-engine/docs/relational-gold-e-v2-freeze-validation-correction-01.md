# Gold E / Gold V v2 — correzione differenziale del freeze

Data: 2026-10-28

Attività: `RD-RELATIONAL-GOLD-E-V2-FREEZE-VALIDATION-01`

Ramo: `codex/tactical-state-contract-v1`

Commit tecnico: `596c4ba`

## Origine

La revisione indipendente del commit `dabfff6` ha classificato la patch
**APPROVABILE CON CORREZIONI**. I contratti erano isolati e gli hash v1
invariati, ma il CLI eseguiva soltanto la preparazione dei template e non
orchestrava tutte le funzioni referenziali durante un freeze reale.

## Confronto dei cinque rilievi

1. **Percorso completo di freeze: confermato.** Le funzioni referenziali
   esistevano, ma `main()` non le collegava. È stato aggiunto
   `--freeze-manifest` e un validatore ricorsivo dei file effettivi.
2. **Identità Gold V nel manifest: confermato.** Il confronto usava
   `case_id`; ora Gold E usa `case_id` e Gold V usa `attempt_id`, consentendo
   più tentativi dello stesso caso.
3. **Hash dei contenuti: parzialmente già coperto.** Dataset, dipendenze,
   casi e oggetto del ledger erano già ricalcolati. La correzione aggiunge
   ricalcolo di answer, input e configurazione sui file effettivi.
4. **Coerenza del manifest Gold E: confermato.** Ora hash e versione devono
   coincidere fra dipendenza del manifest Gold V, `gold_e_reference`, ogni
   `input_reference` e manifest Gold E risolto.
5. **Precondizioni congiunte: confermato.** Il nuovo percorso valida
   ricorsivamente manifest Gold E, registry, ledger A/B/C, dataset Gold E/V,
   stati congelati, tentativi, dipendenze, hash e assenza di cicli.

## Delta implementato

- `input_reference` richiede il percorso del payload effettivo;
- `generation_configuration` richiede il percorso della configurazione;
- manifest v2 ammette esattamente `case_id` oppure `attempt_id` per record;
- ordinamento normativo dei record Gold V basato su `attempt_id`;
- `answer_sha256` ricalcolato sulla risposta disponibile;
- CLI offline `--freeze-manifest` fail-closed;
- validazione ricorsiva del manifest Gold E referenziato;
- risoluzione e hash reali di input e configurazione;
- controllo congiunto degli stati `frozen` e dei ledger.

## Test differenziali nuovi

I test 13–18 verificano:

- bundle Gold E/Gold V completo valido;
- due tentativi dello stesso `case_id` distinti per `attempt_id`;
- alterazione di input, configurazione e answer;
- divergenza fra hash Gold E dichiarati e manifest effettivo;
- dipendenza ledger non congelata;
- esecuzione effettiva del CLI completo.

## Risultati

```text
STATUS V2_PREPARATION_VALID
CASES 0
INFERENCE NOT_RUN
INDEPENDENT_GOLD BLOCKED

test v2: 18/18 PASS
regressione v1: 5/5 PASS
totale: 23/23 PASS
py_compile: PASS
git diff --check: PASS
```

Fixture esclusivamente sintetiche; nessun dato Gold reale, inferenza o
benchmark.

## Decisione e stato

Correzione del percorso di freeze: **IMPLEMENTATO**.

Test differenziali: **ESEGUITO**.

Percorso offline completo e regressione v1: **VALIDATO**.

Gold indipendente, raccolta, annotazione e freeze reali: **BLOCCATO** o
**DA FARE** secondo il piano esistente.

La patch non è **INTEGRATO** o **CERTIFICATO** e non modifica runtime,
pannello, RAG, Qwen, corpus, indici, API o VPS. Nessun merge o deploy.
