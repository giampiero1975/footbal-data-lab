# Gold E / Gold V v2 — precondizioni di freeze del singolo caso

Data: 2026-10-28

Attività: `RD-RELATIONAL-GOLD-E-V2-CASE-FREEZE-01`

Commit tecnico: `454ebad`

## Evidenza precedente e delta

La revisione indipendente di HEAD `40dfd73` ha confermato il percorso completo
di freeze, individuando un solo limite residuo: il manifest congelato non
imponeva tutte le precondizioni sul singolo caso.

Il codice controllava già lo stato `frozen` di dataset e ledger. Non esistevano
controlli equivalenti per:

- `frozen_at` del manifest;
- `freeze_status` dei singoli casi;
- `independence_status` dei casi Gold E.

## Correzione

Un manifest con `manifest_status: frozen` viene ora rifiutato se `frozen_at`
è assente. Ogni record del dataset deve avere `freeze_status: frozen`. Inoltre
ogni caso Gold E deve avere `independence_status: independent_frozen`.

I nuovi errori fail-closed sono:

- `MANIFEST_FROZEN_AT_MISSING`;
- `FREEZE_CASE_STATE_INVALID:<record_id>`;
- `GOLD_E_INDEPENDENCE_STATE_INVALID:<case_id>`.

Per Gold V l'identificativo diagnostico del record è `attempt_id`; per Gold E
è `case_id`.

## Test differenziali

Tre test negativi nuovi dimostrano il rifiuto di:

1. manifest congelato senza data di freeze;
2. caso con stato `ready_for_freeze` dentro un manifest congelato;
3. caso Gold E ancora `eligible_independent` anziché `independent_frozen`.

Il test positivo del bundle completo già esistente è stato riutilizzato, senza
duplicarlo, e continua a essere accettato.

Risultati:

```text
test v2: 21/21 PASS
regressione v1: 5/5 PASS
totale: 26/26 PASS
py_compile: PASS
git diff --check: PASS
CASES 0
INFERENCE NOT_RUN
```

## Decisione e stato

Precondizioni per caso: **IMPLEMENTATO**.

Test differenziali: **ESEGUITO**.

Percorso freeze offline aggiornato: **VALIDATO**.

Gold indipendente reale e benchmark: **BLOCCATO**.

Nessun file v1, runtime, pannello, RAG, Qwen, corpus, indice, API o VPS è
stato modificato. Nessuna raccolta, annotazione reale, inferenza, benchmark,
merge o deploy.
