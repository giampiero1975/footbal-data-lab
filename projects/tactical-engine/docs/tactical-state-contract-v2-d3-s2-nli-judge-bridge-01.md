# TSC V2 D3 — Bridge NLI V2 verso S2 Shadow Adapter

Attivita: `RD-TSC-V2-D3-S2-NLI-JUDGE-BRIDGE-01`

Data: 2026-11-05

Baseline: `140986835e8834ca23739d14fabdbae38587a1d1`

Commit tecnico: `a07b34ff36ccf9a7cc10b10f8d18638aaf7cadc5`

## Attivita → Script → Commit → Report → Risultato → Decisione → Stato

- Attivita: collegare l'interfaccia del judge S2 al motore NLI V2 esistente.
- Script: `scripts/v5_tactical_semantic_support_s2_nli_v2_bridge.py`.
- Commit: commit tecnico sopra indicato; commit documentale separato.
- Report: questo documento.
- Risultato: bridge inerte, deterministico, mock-testato e fail-closed.
- Decisione: bridge **IMPLEMENTATO**, test **ESEGUITO**, proprieta contrattuali
  coperte **VALIDATO offline**; accuratezza e runtime **BLOCCATO**.

## 1. Implementazione

Il bridge riceve il payload gia verificato dall'adapter S2 e costruisce la claim
NLI senza eliminare:

- statement, inclusi quantificatori testuali;
- condizioni;
- polarita;
- binding di attore, compito, spazio, trigger, finalita e fase;
- identita della claim.

Il testo dell'evidenza viene passato separatamente e senza trasformazioni. Il
callable NLI resta iniettato: costruire o importare il bridge non avvia modelli,
rete o servizi. Il contratto riutilizzato e quello storico
`shadow_nli_v2_inference.judge_pair(claim, evidence)`; nessuna logica NLI e stata
copiata.

Il descriptor conserva schema/versione del bridge, contratto NLI, label ammesse,
modalita della rationale e configurazione NLI. L'adapter S2 ne registra il digest
content-addressed gia previsto.

## 2. Fail-closed e rationale

Sono accettate esclusivamente le label `supported`, `contradicted` e
`insufficient`. Payload incompatibili, label sconosciute, risultati incompleti,
rationale vuote o malformate ed eccezioni impediscono la valutazione; il boundary
S2 esistente le converte in `not_evaluable` e non autorizza promozioni.

Il judge NLI V2 storico restituisce soltanto la label. In quel caso la rationale
registrata e una traccia tecnica esplicita che dichiara l'assenza di una rationale
semantica storica; non inventa una motivazione. Se un callable compatibile fornisce
una rationale non vuota, questa viene preservata integralmente.

## 3. Invarianti

- S1 e D3 invariati e autorevoli.
- `promotion_authorized=false` preservato dall'adapter S2.
- `promoted_answer` e `overall_status` non leggono l'esito shadow.
- Nessuna label `supported` produce promozione.
- Nessun fallback positivo per errori o incompatibilita.
- Conflitti multi-evidenza restano gestiti senza maggioranza dall'adapter S2.
- Bridge non costruito/iniettato: comportamento precedente invariato.
- Nessuna dipendenza obbligatoria da un modello nel percorso D3/S1.

Non sono stati modificati S1, D3, dual-output, NLI V2, TSC V1/V2, planner,
retrieval, prompt, collection, API o pannello.

## 4. Verifiche eseguite

Suite mirata:

```text
python -m unittest \
  tests/test_v5_tactical_semantic_support_s2_nli_v2_bridge.py \
  tests/test_v5_tactical_semantic_support_s2.py \
  tests/test_v5_tactical_state_dual_output_v1.py -v
```

Risultato: **33/33 PASS** in 0,263 s:

- bridge nuovi: 8/8;
- regressioni S2: 8/8;
- regressioni dual-output: 17/17.

Dopo la rettifica finale sulla rationale, la sola suite bridge e stata rieseguita:
**8/8 PASS** in 0,006 s. Compilazione dei due file nuovi e `git diff --check`:
PASS. Tutti i judge erano mock deterministici; nessun modello e stato chiamato.

## 5. Limiti

- l'accuratezza semantica NLI non e stata misurata;
- il contratto NLI storico non produce una rationale semantica;
- condizioni e binding sono conservati nella proiezione, ma la capacita del
  modello di interpretarli non e validata;
- il Gold S2 indipendente non e disponibile;
- nessun Gate, integrazione runner/API/pannello o certificazione runtime.

## 6. Stati

- Bridge NLI V2 → S2: **IMPLEMENTATO**.
- Test differenziali e regressioni mirate: **ESEGUITO**.
- Contratto, isolamento, provenance e fail-closed: **VALIDATO offline**.
- Accuratezza semantica reale e Gold S2: **BLOCCATO**.
- Gate, integrazione e certificazione runtime: **BLOCCATO**.

Nessuna inferenza, benchmark, download modello, VPS, Chroma, retrieval, API,
pannello, deploy o merge e stato eseguito.
