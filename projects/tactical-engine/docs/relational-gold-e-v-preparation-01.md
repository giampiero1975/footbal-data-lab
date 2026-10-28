# Preparazione indipendente Gold E / Gold V

Data: 2026-10-28  
Attività: `RD-RELATIONAL-GOLD-E-V-PREPARATION-01`  
Ramo: `codex/tactical-state-contract-v1`  
HEAD iniziale: `7ff85157704cf5c3c04768c14573b001f297ae4b`  
Commit tecnico: `6f4579fdeca7c522f127a31bb4cc9bcbf7933750`

## 1. Perimetro rispettato

È stata eseguita soltanto la preparazione metodologica e infrastrutturale dei
due gold relazionali. Non sono stati generati o annotati casi, non è stato
eseguito alcun benchmark e non sono stati chiamati modelli. Non sono cambiati
`relation_requirements()`, `audit_relations()`, quality gate, runner, API,
pannello, profilo locked, corpus o indici. Nessun merge, deploy o intervento
VPS.

I template contengono zero casi. Lo script di controllo rifiuta un template
popolato e continua a dichiarare il benchmark indipendente `BLOCKED`.

## 2. Inventario precedente

La ricognizione ha individuato materiali riutilizzabili ma nessun equivalente
completo di Gold E / Gold V:

- `eval/claim_fidelity_gold_v1.json`: gold claim-evidenza, non relazionale;
- `evaluation/annotations/rag_v5_shadow_claims_q4_q5_v2.json`: annotazioni
  storiche, non indipendenti per questo obiettivo;
- `scripts/build_rag_v5_quality_adjudication_worksheet_v1.py`: precedente per
  worksheet non distruttivo e review atomica;
- `scripts/validate_rag_v5_prospective_manifest_v1.py`: precedente per
  controlli fail-closed e hash;
- `evaluation/runtime_evidence_manifest_v1.json`: precedente di manifest
  SHA-256;
- rubriche NLI/holdout in `docs/`: separano validità formale, supporto
  documentale e qualità;
- report quarta-settima revisione: definiscono Gold E/Gold V, ma dichiarano
  correttamente assente un insieme indipendente congelato.

Drive11, Coverciano V10, test e controesempi delle sette remediation restano
esclusi dall'independent gold.

## 3. Artefatti creati

### Protocollo

- `docs/relational-gold-e-v-protocol-v1.md`

Integra selezione, provenienza, cecità Gold E, dipendenza congelata Gold V,
doppia revisione, adjudication, freeze, separazione regression/independent e
metriche future.

### Schemi e template

- `evaluation/annotations/relational_gold_e_schema_v1.json`
  (`relational_gold_e_v1`);
- `evaluation/annotations/relational_gold_v_schema_v1.json`
  (`relational_gold_v_v1`);
- `evaluation/annotations/relational_gold_e_template_v1.json`;
- `evaluation/annotations/relational_gold_v_template_v1.json`;
- `evaluation/annotations/relational_gold_freeze_manifest_template_v1.json`
  (`relational_gold_freeze_manifest_v1`).

Gold E conserva sottodomande, requisiti, dimensioni, ambiguità e provenienza
`explicit/derived/assumed/unknown`; `derived` richiede `rule_id`. Gold V
riferisce un manifest Gold E congelato, conserva provenienza della risposta e
distingue relazione, completezza, correttezza tattica e supporto documentale.

Hash SHA-256 di preparazione (non hash di freeze):

| File | SHA-256 |
|---|---|
| `relational_gold_e_schema_v1.json` | `79e6f4fc63936409a2cd1fc2d210dc80f2f97e4f7980cbc97f15a44872b03bf7` |
| `relational_gold_v_schema_v1.json` | `d29495df218610dab66b4f55c7d240916226ef0cb407b0751b0edf55e89d9d96` |
| `relational_gold_e_template_v1.json` | `2b9ea4be5f7ef6ffafda6b87fb402f3ff9c76832e91ad78da2de2fe0d63af247` |
| `relational_gold_v_template_v1.json` | `a9850a6695ef0d589930d72fa6d55b1a36133de7c0ecf28fbbc84aa55d80d680` |
| `relational_gold_freeze_manifest_template_v1.json` | `9669f11970aa64f29337cabc6587b1cf6d7181c21cb773a57a9d241989597c7e` |

### Controlli

- `scripts/validate_relational_gold_preparation_v1.py`;
- `tests/test_validate_relational_gold_preparation_v1.py`.

Il validatore usa soltanto la libreria standard, non introduce dipendenze e
non pretende di validare semanticamente annotazioni umane.

## 4. Evidenze dei controlli statici

Comando di validazione: **PASS**

```text
STATUS PREPARATION_VALID
CASES 0
INDEPENDENT_BENCHMARK BLOCKED
```

Test unitari: **5/5 PASS**. Coprono artefatti repository validi e vuoti,
rifiuto di template Gold E popolato, rifiuto di Gold V che dichiara un Gold E
inesistente come congelato, rifiuto di freeze dichiarato nel manifest draft e
presenza dei campi minimi/separazione dei quattro giudizi.

Compilazione Python: **PASS**. `git diff --check`: **PASS**.

Il runtime Python di Windows Store non era eseguibile; i controlli sono stati
ripetuti con il runtime Python configurato dal workspace Codex. Questo non ha
richiesto modifiche agli artefatti o dipendenze aggiuntive.

## 5. Garanzie d'indipendenza

- selezione dei casi prima dell'esecuzione dell'audit;
- provenienza e uso nello sviluppo obbligatori;
- screening duplicati e casi semanticamente equivalenti;
- Gold E annotato senza risposta né output del motore;
- Gold V vincolato a hash/versione Gold E congelata;
- annotatore e revisore indipendenti, disaccordi conservati e adjudication
  motivata;
- perdita dello status indipendente se il caso viene usato per sviluppo;
- nessuna promozione automatica di `ambiguous`, `unknown` o
  `non_determinable`;
- nessun feedback modifica automaticamente corpus o regole.

## 6. Freeze e revisione umana

Il protocollo prescrive annotazione A, revisione cieca B, confronto,
adjudication C, approvazione e freeze. Competenza e conflitti sono documentati.
Il manifest frozen contiene hash dataset e per-caso, identità dei revisori,
fonti, esclusioni e separazione development/independent. Una correzione genera
una nuova versione senza sovrascrivere quella congelata.

## 7. Metriche predisposte

Gold E: precisione, recall e F1 micro/macro e per categoria/dimensione; errori
di atomizzazione, associazione attore-compito, fase-trigger e requisiti aperti.

Gold V: TP/FP/TN/FN, precisione, recall, F1, ambiguità, polarità, ambito
proprio/avversario, attore-compito, fase-trigger, spazio, finalità e obiettivo.

Ambigui, non determinabili, non applicabili e non verificabili sono pubblicati
separatamente con denominatori espliciti e non diventano automaticamente
positivi. Sono previste anche misure di accordo umano pre-adjudication.

## 8. Attività ancora necessarie

Richiedono una decisione successiva separata:

1. fonti, numerosità e stratificazione dei nuovi casi;
2. scelta e documentazione delle competenze dei revisori;
3. raccolta e screening dei candidati;
4. annotazione Gold E, doppia review, adjudication e freeze;
5. acquisizione delle risposte senza contaminare Gold E;
6. annotazione Gold V, doppia review, adjudication e freeze;
7. sola dopo entrambi i freeze, esecuzione del benchmark indipendente.

## 9. Risultato, decisione e stato

Risultato: processo documentato, verificabile e pronto a ricevere annotazioni
indipendenti; nessun dataset fittizio prodotto.

Decisione: chiudere `RD-RELATIONAL-GOLD-E-V-PREPARATION-01` come preparazione
metodologica **VALIDATO offline**. Mantenere raccolta/annotazione/freeze **DA
FARE** e `RD-RELATIONAL-GOLD-E-V-01` **BLOCCATO** fino all'esistenza di Gold E
e Gold V indipendenti e congelati. I gold non sono **VALIDATO**, **INTEGRATO**
o **CERTIFICATO**; l'audit resta offline e non bloccante.
