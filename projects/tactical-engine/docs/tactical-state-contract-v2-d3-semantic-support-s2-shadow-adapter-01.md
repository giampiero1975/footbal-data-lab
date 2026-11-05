# TSC V2 D3 — S2 Shadow Adapter offline

Attivita: `RD-TSC-V2-D3-SEMANTIC-SUPPORT-S2-SHADOW-ADAPTER-01`

Data: 2026-11-05

Baseline: `ef1c0f96c4796e5b566daa25cb95b43781de838a`

Commit tecnico: `8aa248957a9c6500861a049c6621ea71aa02bc61`

## Attivita → Script → Commit → Report → Risultato → Decisione → Stato

- Attivita: collegare in shadow claim D3 ed evidenze a un judge semantico
  iniettato, senza cambiare l'autorita S1.
- Script: `scripts/v5_tactical_semantic_support_s2.py`; hook opt-in in
  `scripts/v5_tactical_state_dual_output_v1.py`.
- Commit: commit tecnico sopra indicato; commit documentale separato.
- Report: questo documento.
- Risultato: adapter content-addressed fail-closed, otto test mock nuovi e 29
  regressioni S1/dual direttamente interessate, tutti PASS.
- Decisione: infrastruttura shadow **IMPLEMENTATO** e invarianti testati
  **VALIDATO offline**; affidabilita semantica, Gate, integrazione e certificazione
  **BLOCCATO**.

## 1. Architettura implementata

Il nuovo adapter riceve esclusivamente:

- attempt ID e fingerprint del piano autorizzato;
- claim D3 gia strutturato;
- mappa delle evidenze dichiarate;
- assessment S1 prodotto e verificabile;
- binding autorevoli derivati dalle operational relations;
- funzione judge iniettata e descrittore di configurazione.

Non contiene client Ollama/Qwen, URL, retry o fallback. Il judge deve essere
fornito dal chiamante e restituire esattamente `label` e `rationale`.

Il record `tactical_documentary_semantic_support_shadow_v1` conserva:

- identita del tentativo, piano e claim;
- digest del testo del claim e dell'assessment S1;
- digest delle evidenze;
- fingerprint della configurazione del judge;
- label/rationale per evidenza;
- stato di valutabilita, aggregato e reason codes;
- digest content-addressed del record;
- `mode=shadow_only` e `promotion_authorized=false` invariabili.

## 2. Validazione e aggregazione conservativa

Prima del judge sono verificati assessment S1, fingerprint, claim, evidence refs,
digest e binding attore/compito/spazio/trigger/finalita/fase. Un errore impedisce
la chiamata e produce `not_evaluable`.

Output malformato o eccezione del judge non esce dal boundary e produce
`not_evaluable`. L'aggregazione non usa maggioranza:

- tutte `supported` → `supported` shadow;
- tutte `contradicted` → `contradicted` shadow;
- presenza simultanea di `supported` e `contradicted` → `conflicting`;
- ogni altra combinazione completa → `insufficient`;
- errore o risultato incompleto → `not_evaluable`.

Queste etichette sono diagnostiche e non certificano correttezza semantica.

## 3. Integrazione opt-in e invarianti

`documentary_diagnostic()` accetta due nuovi keyword argument opzionali:

- `semantic_support_s2_judge`;
- `semantic_support_s2_judge_descriptor`.

Se il judge e assente, non viene aggiunta alcuna chiave e l'output legacy resta
invariato. Se presente, i record compaiono esclusivamente in
`controls.semantic_support_s2_shadow`.

Il calcolo di `failures`, `unassessed`, `overall_status`, `promoted_answer` e degli
assessment S1 non legge mai il risultato S2. Anche `supported` shadow non promuove
una parafrasi; una contraddizione shadow non viene trasformata in decisione
autorevole. Tale separazione e intenzionale finche S2 non dispone di Gold e Gate.

## 4. File modificati

- nuovo `scripts/v5_tactical_semantic_support_s2.py`;
- modifica opt-in `scripts/v5_tactical_state_dual_output_v1.py`;
- nuovo `tests/test_v5_tactical_semantic_support_s2.py`.

TSC V1/V2, planner, retrieval, prompt, runner generativo, Candidate Registry,
Gold S2, API e panel sono invariati.

## 5. Test eseguiti

Comando con Python 3.13 locale:

```text
python.exe -m unittest \
  tests/test_v5_tactical_semantic_support_s2.py \
  tests/test_v5_tactical_semantic_support_s1.py \
  tests/test_v5_tactical_state_dual_output_v1.py -v
```

Risultato: **37/37 PASS** in 0,314 s:

- S2 nuovi: 8/8;
- S1 direttamente interessati: 12/12;
- dual-output direttamente interessati: 17/17.

Dopo l'aggiunta della verifica esplicita del digest record, la sola suite S2 e
stata rieseguita: **8/8 PASS** in 0,038 s. Compilazione statica dei tre file: PASS.
`git diff --check`: PASS.

I test nuovi coprono parafrasi shadow, contraddizione, condizione/quantificatore
omessi, mismatch attore/fase, fingerprint/digest/record alterati, output
malformato, eccezione del judge, evidenze conflittuali e adapter disattivato.
Usano esclusivamente mock; non misurano accuratezza NLI.

## 6. Prove degli invarianti

- parafrasi `supported` shadow: S1 resta `not_evaluable`, risposta non promossa;
- contraddizione shadow: risultato autorevole invariato;
- conflitto multi-evidenza: `conflicting`, nessuna maggioranza;
- binding incoerente: judge non chiamato;
- digest/fingerprint alterato: `not_evaluable`;
- record alterato: digest mismatch;
- judge malformato o in errore: `not_evaluable`;
- adapter disabilitato: risultato legacy identico e nessuna chiave S2.

## 7. Limiti residui

- nessun judge reale e stato collegato o eseguito;
- accuratezza su parafrasi, negazioni, condizioni, ruoli e fasi non e validata;
- NLI V2 storico condivide Qwen e presenta errori documentati su scope e
  quantificatori;
- nessun Gold S2 indipendente e congelato;
- nessuna policy di promozione e autorizzata;
- nessuna integrazione runner/API/panel o runtime.

## 8. Stati ufficiali

- S2 Shadow Adapter: **IMPLEMENTATO**.
- Test mock e regressioni interessate: **ESEGUITO**.
- Orchestrazione, provenance, content addressing, isolamento e fail-closed:
  **VALIDATO offline**.
- Affidabilita semantica S2 e Gold indipendente: **BLOCCATO**.
- Gate, integrazione e certificazione runtime: **BLOCCATO**.

Nessuna inferenza, benchmark, VPS, Chroma, collection, deploy, merge o modifica
al panel e stata eseguita.

## 9. Prossimo intervento possibile, non eseguito

Con autorizzazione separata, adattare il judge NLI V2 gia esistente all'interfaccia
iniettata, mantenendolo offline/shadow e verificandone solo il contratto con mock.
Qualunque inferenza reale o Gate richiede una decisione ulteriore e non puo
promuovere risultati prima di Gold e criteri approvati.
