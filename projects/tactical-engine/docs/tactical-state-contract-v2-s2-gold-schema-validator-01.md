# TSC V2 D3 — schema e validatore Gold S2 V1 offline

Attività: `RD-TSC-V2-D3-S2-GOLD-SCHEMA-VALIDATOR-01`

Data: 2026-11-05

Baseline: `13c641573cca85b1e9a0c928197a3c1558d38ca6`

Commit tecnico: `d0808dfd23802c321e490c6b6dbf32cdc6119a49`

## Attività → Script → Commit → Report → Risultato → Decisione → Stato

- Attività: implementare il contratto e il validatore deterministico Gold S2 V1.
- Script: `scripts/validate_tactical_semantic_support_gold_s2_v1.py`.
- Commit: commit tecnico sopra indicato e commit documentale separato.
- Report: questo documento.
- Risultato: schema dataset/manifest, template draft vuoti, canonicalizzazione,
  digest, riferimenti, freeze e split validation; 18/18 test mirati PASS.
- Decisione: contratto e proprietà offline coperte sono accettabili; nessun Gold
  reale è stato creato o validato semanticamente.
- Stato: schema/validator **IMPLEMENTATO**, test **ESEGUITO**, proprietà coperte
  **VALIDATO offline**; raccolta e S2 restano **BLOCCATO**.

## Riconciliazione

Branch, HEAD e working tree coincidevano con la baseline. Sono stati letti TODO,
experiment register, design Gold S2, readiness, historical recovery, design/runner
S1, contratti e test Gold E/V v1/v2. Non esisteva uno schema o validatore Gold S2
equivalente.

I nuovi file sono separati dagli artefatti E/V. Nessun file Gold E/V, D3, S1,
planner, runner, retrieval, API o pannello è stato modificato. Non sono stati
eseguiti modello, benchmark, inferenza, retrieval o runtime.

## Artefatti

- `evaluation/annotations/tactical_semantic_support_gold_s2_schema_v1.json`;
- `evaluation/annotations/tactical_semantic_support_gold_s2_template_v1.json`;
- `evaluation/annotations/tactical_semantic_support_gold_s2_freeze_manifest_schema_v1.json`;
- `evaluation/annotations/tactical_semantic_support_gold_s2_freeze_manifest_template_v1.json`;
- `scripts/validate_tactical_semantic_support_gold_s2_v1.py`;
- `tests/test_validate_tactical_semantic_support_gold_s2_v1.py`.

I template contengono zero casi, zero review e zero autorizzazioni. Non sono Gold.

## Contratto

Identificativo dataset: `tactical_semantic_support_gold_s2_v1`.

Identificativo manifest: `tactical_semantic_support_gold_s2_manifest_v1`.

Profilo canonico: `gold_s2_rfc8785_nfc_v1`. Riusa la serializzazione RFC 8785
ristretta già implementata per v2 senza modificarla; ordina soltanto le liste
set-like definite dal contratto S2. Testo di evidenza e claim usa Unicode NFC e
newline LF. Gli span sono offset Python/Unicode code point semiaperti `[start,end)`;
gli span di explanation D3 e quelli dell'evidenza sono controllati separatamente.

Etichette ammesse, mai generate dal validatore:

- `supported`;
- `contradicted`;
- `insufficient`.

Le otto categorie primarie coincidono col design. Le proprietà trasversali hanno
una allowlist separata e non possono essere usate come nuove categorie.

## Digest e autoreferenzialità

- fonte: SHA-256 dei byte UTF-8 del contenuto fornito alla validazione;
- evidenza: oggetto canonico con ID, provenance, location, testo, contesti e profilo;
- claim: testo, contesto, condizioni, quantificatori, attori, fase e riferimenti;
- subject del caso: input claim/evidence/tassonomia/split, usato da A/B/C e QA D;
- caso: record completo escluso il proprio `case_sha256`;
- dataset: documento completo escluso il proprio `dataset_sha256`.

Il formato è `sha256:<64 caratteri esadecimali minuscoli>`. Un digest sorgente senza
`source_content` è registrato come `SOURCE_HASH_UNVERIFIABLE`; è accettabile e
visibile in draft ma rende impossibile un frozen valido. Il validatore non tratta la
mera sintassi del digest come verifica.

## Controlli deterministici

- campi obbligatori, proprietà aggiuntive, tipi, enum, versioni e ID univoci;
- risoluzione provenance, evidenze, review A/B/C e QA D;
- ricomputo dei digest quando il contenuto è disponibile;
- NFC/LF e span esatti per evidence rationale, review, anchor e section D3;
- condizioni, quantificatori, attori, riferimenti e composizione multi-fonte;
- una categoria primaria e proprietà trasversali allowlisted;
- contaminazione dimostrabile fra split per source, document, cluster dichiarato e,
  se richiesto dalla policy, author group;
- stato separato `unverifiable` quando il metadata non permette una conclusione;
- frozen: provenance attiva/disponibile, hash verificabili, label/rationale,
  review A/B cieche, C quando il disaccordo è dichiarato o osservato, QA D PASS,
  autorizzazione del titolare, case/dataset digest e manifest coerenti;
- mapping D3/S1 opzionale: statement/span, claim fields, evidence refs/anchor,
  fingerprint e assessment digest, senza consumare o modificare D3/S1.

Il validatore non decide se una label umana è scientificamente corretta, non rileva
quasi duplicati semanticamente e non autorizza il freeze.

## Test mirati

Comando eseguito:

```text
python -m unittest projects/tactical-engine/tests/test_validate_tactical_semantic_support_gold_s2_v1.py -v
```

Risultato: `Ran 18 tests ... OK`.

Copertura: repository draft, bundle frozen sintetico positivo, label/categoria
sconosciute, campo mancante, tipo errato, case ID duplicato, span Unicode incoerente,
digest errato, fonte mancante, review irrisolta, contaminazione source e cluster,
frozen incompleto, autorizzazione assente, mapping D3 incoerente, source hash non
verificabile e multi-source non dichiarato.

Le fixture sono esclusivamente sintetiche. Non sono state ripetute suite Gold E/V,
D3/S1 o campagne storiche.

## Limiti

- Il JSON Schema descrive la forma; il validatore standard-library applica i
  vincoli inter-artifact e non è un motore JSON Schema general-purpose.
- La separazione semantica dei quasi duplicati non è rilevata: vengono controllati
  soltanto cluster dichiarati.
- Author-disjointness è verificabile solo con `author_group_id` completo e policy
  attiva; l'assenza resta non verificabile.
- Contenuti sorgente riservati possono essere forniti al processo di verifica senza
  pubblicarli, ma senza byte il relativo hash non è verificato e il freeze fallisce.
- Correttezza delle label, competenza dei revisori, diritti effettivi e qualità
  scientifica richiedono evidenze umane esterne al validatore.
- Un bundle frozen sintetico dimostra il contratto, non autorizza un freeze reale.

## Stati finali

- Schema, manifest, template e validatore Gold S2 V1: **IMPLEMENTATO**.
- Test differenziali mirati: **ESEGUITO**.
- Proprietà deterministiche coperte: **VALIDATO offline**.
- Inventario fonti: **DA FARE**.
- Gold S2 indipendente, raccolta, annotazione, adjudication, QA e freeze reale:
  **BLOCCATO**.
- S2 shadow, Gate, integrazione e certificazione: **BLOCCATO**.
- Readiness S2 decisione B, S1, D3 e Gold E/V: invariati.

Nessuna attività successiva è autorizzata da questo closeout.
