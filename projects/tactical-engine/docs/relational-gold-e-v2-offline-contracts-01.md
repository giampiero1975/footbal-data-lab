# Gold E / Gold V v2 — patch offline isolata

Data: 2026-10-28

Attività: `RD-RELATIONAL-GOLD-E-V2-OFFLINE-CONTRACTS-01`

Ramo: `codex/tactical-state-contract-v1`

HEAD iniziale: `7c0c77988a20795e8d6cf6a8e9f947c3877d98d8`

Commit tecnico: `d26f364`

## Scopo

Implementare esclusivamente i contratti offline v2 approvati nel confronto
Codex–ChatGPT. La patch non popola dataset e non modifica motore, runtime,
retrieval, training, API, pannello, VPS o artefatti v1.

## Artefatti implementati

- Provenance Registry v2: schema e template vuoto;
- Gold E v2: schema e template vuoto;
- Gold V v2: schema e template vuoto;
- Annotation Ledger v2: schema e template vuoto;
- Freeze Manifest v2: schema e template vuoto;
- validatore offline standard-library;
- dodici test differenziali con sole fixture sintetiche.

I template contengono zero casi, zero record e zero tentativi. Non sono state
raccolte domande né prodotte annotazioni tattiche reali.

## Contratti e controlli

Il Provenance Registry usa identificativi pseudonimi, origine comune,
indipendenza, conflitti, diritti, retention, revoca e riferimenti formali alle
evidenze riservate. Un freeze richiede provenienza attiva ed evidenza
disponibile a un revisore autorizzato.

Gold E v2 conserva le strutture tattiche v1 ma sostituisce la provenienza
incorporata con `provenance_record_id` e aggiunge
`adjudication_record_id`. Il validatore risolve request part, requisiti,
registro e ledger.

Gold V v2 elimina la duplicazione di domanda e provenienza Gold E. Ogni
tentativo conserva input, configurazione e hash, e usa soltanto gli stati
`completed_evaluable`, `completed_empty`, `timeout` e `technical_error`.
Gli esiti non valutabili non possono contenere risposta o annotazioni
tattiche. Una risposta disponibile ma tatticamente errata resta valutabile.

Il ledger conserva A/B indipendenti, disaccordi e adjudication C motivata e
lega la decisione alla versione e allo SHA-256 dell'oggetto annotato.

Il manifest risolve realmente dataset e dipendenze, ricalcola hash, confronta
insieme e hash dei casi e rifiuta dipendenze circolari.

## Canonicalizzazione v2

La funzione v2 implementa il profilo RFC 8785 necessario ai contratti:

- oggetti ordinati secondo chiavi UTF-16;
- Unicode valido e serializzazione UTF-8;
- null, booleani e interi I-JSON;
- array e oggetti;
- floating-point rifiutati esplicitamente.

I contratti v2 usano interi per le durate e categorie testuali per la
confidenza, quindi non richiedono numeri floating-point. Gli array che
rappresentano insiemi vengono ordinati deterministicamente prima della
canonicalizzazione; gli array cronologici non vengono riordinati.

Questa scelta evita una nuova dipendenza. Non modifica la canonicalizzazione
v1 e non va estesa implicitamente a futuri campi numerici senza una nuova
verifica tecnica.

## Verifiche eseguite

Comandi:

```powershell
python -m py_compile `
  projects/tactical-engine/scripts/validate_relational_gold_preparation_v2.py `
  projects/tactical-engine/tests/test_validate_relational_gold_preparation_v2.py

python projects/tactical-engine/scripts/validate_relational_gold_preparation_v2.py

python -m unittest `
  projects/tactical-engine/tests/test_validate_relational_gold_preparation_v2.py `
  projects/tactical-engine/tests/test_validate_relational_gold_preparation_v1.py -v
```

Risultati:

- JSON v2: 10/10 caricati;
- compilazione Python: PASS;
- validatore: `STATUS V2_PREPARATION_VALID`, `CASES 0`, `INFERENCE NOT_RUN`;
- test v2: 12/12 PASS;
- regressione v1: 5/5 PASS;
- totale mirato: 17/17 PASS;
- `git diff --check`: PASS;
- integrazione runtime/pannello: assente e verificata staticamente.

## Immutabilità v1

Il validatore conserva e verifica gli SHA-256 iniziali di schemi, template,
manifest, validatore e test v1. Tutti i sette hash sono invariati rispetto a
HEAD `7c0c779`.

## Limiti

- Non è stato usato un motore JSON Schema esterno; i contratti sono JSON
  Schema Draft 2020-12, mentre il validatore applicativo copre i vincoli
  referenziali e le precondizioni di freeze.
- Le fixture sono sintetiche e verificano i contratti, non la qualità di un
  futuro Gold E/Gold V.
- L'attestazione di disponibilità di un'evidenza non certifica validità
  giuridica o autenticità del documento.
- Collocazione, custodia, accessi, retention e revoca operativi restano
  decisioni del titolare prima della raccolta.
- Nessun dataset indipendente esiste o viene validato da questa patch.

## Decisione e stato

Schema, template e validatore v2: **IMPLEMENTATO**.

Controlli offline: **ESEGUITO**.

Patch isolata e regressione v1: **VALIDATO** offline.

Raccolta, annotazione, adjudication e freeze: **DA FARE**.

Gold E/Gold V indipendenti e benchmark: **BLOCCATO**.

Integrazione e certificazione: non eseguite.

Non sono stati effettuati merge o deploy.
