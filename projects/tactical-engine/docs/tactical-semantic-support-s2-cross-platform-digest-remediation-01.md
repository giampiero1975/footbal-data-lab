# RD-TSC-V2-D3-S2-FIRST-CONTROLLED-RUNTIME-01 — Cross-platform digest remediation

## Attivita

Eliminare il blocco `source_dataset_digest_mismatch` causato esclusivamente
dalla materializzazione CRLF del working tree Windows, mantenendo byte-for-byte
il controllo SHA-256 del dataset congelato.

## Script e commit

- Dataset: `eval/claim_fidelity_gold_v1.json`.
- Fixture: `evaluation/tactical_semantic_support_s2_first_controlled_runtime_fixture_v1.json`.
- Regola Git: `.gitattributes`, limitata al solo dataset con `text eol=lf`.
- Test mirato: `tests/test_run_tactical_semantic_support_s2_first_controlled_runtime_v1.py`.
- Commit tecnico: `596bc3c6808bbd2d6d9353a0ef8eff823883a605`.

Il runner non e stato modificato: continua a confrontare i byte grezzi.

## Evidenze di integrita

Il blob Git del dataset e identico prima e dopo la correzione:

```text
baseline b1946f8 blob: 4523eb746d666fdfb161c5d38d8db31f12e99b92
commit   596bc3c blob: 4523eb746d666fdfb161c5d38d8db31f12e99b92
dimensione blob: 7612 byte
SHA-256 blob: 8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c
JSON parsato prima/dopo: uguale
```

La fixture sostituisce esclusivamente il vecchio digest Windows CRLF
`fdd6d9383493f58abd6d9a07fe0a029ecc7dc35bad106fe91ce747fb2463a605`
con il digest del blob Git autorevole `8e3933f...`. I casi `q3_05`, `q3_04` e
`q5_08`, le etichette, i claim e le evidenze restano invariati.

## Verifica Windows effettiva

Eseguito un clone temporaneo fresco del commit tecnico, configurato con
`core.autocrlf=true`, poi eliminato. Risultato del checkout:

```text
dimensione: 7612 byte
CRLF: 0
LF: 139
SHA-256: 8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c
git check-attr: text=set, eol=lf
```

Il runner ha accettato il dataset conforme nel test della fixture e continua a
rifiutare il digest alterato.

## Verifica Linux effettiva e limite

Nel clone Linux gia predisposto alla baseline precedente il dataset reale e
stato letto senza modifiche:

```text
dimensione: 7612 byte
SHA-256: 8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c
```

Il nuovo commit non e stato applicato allo staging Linux protetto, come imposto
dal perimetro. Di conseguenza la combinazione nuova fixture + dataset non e stata
rieseguita su Linux; la prova Linux riguarda i byte effettivi del dataset, mentre
la prova completa del runner e stata eseguita sul checkout Windows fresco.

## Test differenziali

Eseguita esclusivamente la suite mirata del runner: **4/4 PASS**.

- fixture content-addressed e tre label congelate: PASS;
- attraversamento mock in tre chiamate senza promozione: PASS;
- errore fail-closed, arresto senza retry: PASS;
- dataset alterato rifiutato: PASS.

Nessuna suite storica, inferenza o benchmark e stato ripetuto.

## Risultato, decisione e stato

- Regola LF e digest fixture: **IMPLEMENTATO**.
- Verifiche mirate: **ESEGUITO**.
- Identita del blob, checkout Windows e byte Linux osservati: **VALIDATO** nel
  perimetro dichiarato.
- Aggiornamento dello staging Linux e Fase B: **DA FARE** previa autorizzazione.
- Inferenze reali, accuratezza semantica, integrazione e certificazione:
  **BLOCCATO**.

Nessuna modifica e stata apportata a VPS, virtualenv, RAG, Chroma, panel, API o
servizi.
