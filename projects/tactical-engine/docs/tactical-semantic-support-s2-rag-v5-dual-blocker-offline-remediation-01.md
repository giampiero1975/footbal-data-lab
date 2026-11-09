# RAG V5 dual blocker — remediation offline

Attività: `RD-TSC-V2-D3-S2-RAG-V5-DUAL-BLOCKER-OFFLINE-REMEDIATION-01`
Baseline: `4a5ff711620970e02abbaf26c479d05cfd69260d`
Commit tecnico: `56a7b72135595e99a98ff2fb5b1bcc3d6a0c9ebf`

## Attività

È stata implementata la correzione offline dei due difetti documentati nella
revisione causale: handoff claim/evidence insufficiente e mancato controllo
semantico dell'extraction prima del locator. Nessuna inferenza o attività VPS è
stata eseguita.

## Script

- `scripts/shadow_nli_spatial_relations_v2_inference.py`: il prompt extraction
  definisce lato, subject, reference, asse, valore, condizioni, fase,
  quantificatore e polarità; trasmette matrice asse-valori e regole già presenti
  nel contratto per comparison e label.
- `scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py`: lo schema
  descrive esplicitamente i lati e gli slot; `extraction_semantic_errors()`
  verifica asse/valore e riusa `_comparison_errors()` del validatore Spatial V2
  prima della localizzazione.
- Il locator deterministico e `validate_spatial_v2()` non sono stati modificati.
  Il validatore finale resta l'autorità sul witness materializzato.

Gli errori nuovi sono specifici e fail-closed:

- `E_EXTRACTION_AXIS_VALUE_INCOMPATIBLE`;
- `E_EXTRACTION_COMPARISON_INCONSISTENT`;
- boundary `E_EXTRACTION_SEMANTIC_INCONSISTENT`.

Non vengono corretti automaticamente frammenti, valori, comparison o label e
`promotion_authorized` resta sempre `false`.

## Commit

Il commit applicativo dedicato è
`56a7b72135595e99a98ff2fb5b1bcc3d6a0c9ebf`.

## Report dei test

Comandi offline eseguiti:

```text
python -m unittest projects/tactical-engine/tests/test_v5_tactical_semantic_support_s2_spatial_v2_extraction.py
16/16 PASS

python -m unittest projects/tactical-engine/tests/test_v5_tactical_semantic_support_s2_spatial_v2.py
21/21 PASS
```

Totale mirato: **37/37 PASS**. La prima suite comprende handoff nel payload
mock, asse/valore impossibile prima del locator, quantificatori incompatibili,
replay offline della configurazione semantica documentata di runtime-03,
referenti differenti e regressioni opt-in/legacy. La seconda è la regressione
direttamente interessata delle regole versionate riusate. Nessuna campagna
storica è stata ripetuta.

## Risultato

- Side-bound e definizioni degli slot sono presenti nel payload mock con una
  sola chiamata e senza repair.
- `space_availability/between` è respinto prima del locator.
- `comparison.quantifier=same` con `many/some` è respinto.
- La configurazione semantica documentata di runtime-03 fallisce chiusa senza
  produrre witness né promozione.
- Referenti differenti conducono a `insufficient`, non a una falsa
  contraddizione.
- Lo stesso referente con valori versionati incompatibili continua a derivare
  `contradicted` nel caso positivo già esistente.
- Percorso legacy senza opt-in, singola generazione e assenza di repair/fallback
  restano invariati.

## Decisione

Patch **IMPLEMENTATO**; verifiche mirate **ESEGUITO**; proprietà deterministiche
e compatibilità direttamente osservate **VALIDATO offline**.

L'efficacia del nuovo handoff sul comportamento generativo non è dimostrata da
mock o replay. Il problema generativo delle contraddizioni non è quindi
dichiarato risolto: runtime specifico, Gate, integrazione e certificazione
restano **BLOCCATO** e richiedono decisione separata.

## Stato

- Remediation offline dual blocker: **VALIDATO** offline.
- Efficacia generativa: **BLOCCATO**.
- Runtime e Gate: **BLOCCATO**.
- Integrazione e certificazione: **BLOCCATO**.
