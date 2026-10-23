# Registro autorevole esperimenti — Tactical Engine

Ultimo aggiornamento: 2026-10-23. GitHub è la fonte autorevole dello **stato**; i report runtime sulla VPS sono evidenze da collegare, non automaticamente versionate. Questo registro è obbligatorio per ogni nuova attività.

## Protocollo permanente

**Attività → script → commit → report (percorso + hash se disponibile) → risultato → decisione → stato.**

Prima di avviare qualunque test: cercare in questo registro, nel TODO, nei report e nella cronologia Git gli esperimenti equivalenti. Un rerun richiede una differenza documentata di codice, dataset, ambiente o obiettivo; non ripetere benchmark costosi per ricostruire informazioni già acquisite. Dopo ogni report: analizzarlo e aggiornare registro e TODO **nello stesso ciclo operativo**. Non segnare completato un test solo perché lo script esiste.

### Stati definitivi

- **DA FARE**: non implementato.
- **IMPLEMENTATO**: codice pubblicato, ma senza esito runtime verificato.
- **ESEGUITO**: report di esecuzione disponibile, ancora da valutare.
- **VALIDATO**: risultato esaminato rispetto a criteri dichiarati, con evidenze; limitato all'ambito del test.
- **INTEGRATO**: modifica presente nell'entry point effettivo e regressione verificata.
- **CERTIFICATO**: supera gold indipendente congelato e criteri di promozione.
- **BLOCCATO**: impedimento documentato, con prossimo passo.

Uno stato superiore **non** si deduce dal precedente. In particolare VALIDATO shadow ≠ INTEGRATO e citazioni sintatticamente valide ≠ fedeltà.

## Registro — recupero V5 per fonte/riferimento

| ID | Attività / script | Commit | Report / evidenza | Risultato e decisione | Stato |
|---|---|---|---|---|---|
| V5-SRC-01 | Audit metadata / `audit_v5_source_metadata.py` | `14c7674` | Report audit VPS riferito: 5319/5319 metadata validi | Accettato come prerequisito del filtro fonte; non certifica generazione | VALIDATO |
| V5-SRC-02 | Source retrieval / `rag_v5_source_shadow_v1.py` | `5d916af` | Diagnostica source-aware discussa; percorso/hash non consolidati | Source-filtering valutato in shadow | VALIDATO (shadow) |
| V5-SRC-03 | Source rerank / `rag_v5_source_rerank_shadow_v2.py` | `8db0760` | Report source rerank VPS; hash da acquisire | Migliora casi Foscarini, non risolve Ussia 4/A | VALIDATO (ambito mirato) |
| V5-REF-01 | Exact reference / `rag_v5_exact_reference_shadow_v1.py` | `21cdb18` | `rag_v5_exact_reference_shadow_v1.json`; hash da acquisire | Ussia 4/A recuperato, ma mMARCO lo colloca F5; non integrare ranking grezzo | VALIDATO (diagnostica) |
| V5-REF-02 | Generalizzazione / `rag_v5_reference_generalization_shadow_v1.py` | `547da5c`, fix `eaad637` | `rag_v5_reference_generalization_shadow_v1.json`; hash da acquisire | Parser e riferimenti su 4 nuovi casi, senza generazione | VALIDATO (retrieval) |
| V5-REF-03 | E2E fresh / `rag_v5_fresh_reference_e2e_shadow_v1.py` | `3d10d7f` | `rag_v5_fresh_reference_e2e_shadow_v1.json`; hash da acquisire | Quattro risposte; figura 9 F5, figura 20 con attribuzione imprecisa. Non promuovere | VALIDATO (diagnostica) |
| V5-REF-04 | Priority replay / `rag_v5_reference_priority_shadow_v1.py` | `b570abd` | `rag_v5_reference_priority_shadow_v1.json` fornito in chat 2026-10-23; SHA-256 allegato: `49c6c81d268bf05a1fc43c398daa6a266a6aea53134199186ea80d7e7ad1fb84` (file ricevuto in chat; non ancora archiviato in Git) | 4/B F1, 6/B F1+F2, fig.9 F1, fig.20 F1; stesso top8, nessuna lettura/scrittura Chroma. Risposta fig.20 cita F1, ma attribuisce esplicitamente l'incrocio ai numeri 4 e 3, mentre il testo dice solo che segue allo scambio 4/3: lieve inferenza non garantita; verificare in regressione. **Accettato solo come replay shadow e generazione mirata**, non come certificazione end-to-end | VALIDATO (shadow) |
| V5-REF-05 | Live source-aware retrieval con `--priority-exact` / `rag_v5_fresh_reference_e2e_shadow_v1.py` | `bbb9b7b` | `rag_v5_live_priority_integration_v1.json` (file chat, non Git), SHA-256 `0503e2dcc94be563a7176f0768b869360a6a2465411d4e454688f06fa21512fc` | 4/4 casi con passaggio esatto F1 (6/B anche F2), tutti i top8 invariati come insieme; Chroma 5319→5319; generazione disattivata. Accettata priorità live in shadow; non prova qualità risposta fig20 né integrazione nel candidato locked/produzione | VALIDATO |
| V5-CERT-01 | Gold indipendente V5 | `641f61e`, audit `db9abab` | `evaluation/rag_v5_independent_candidate_v2.json` | Candidato predisposto, revisione indipendente/freeze non attestati | IMPLEMENTATO |
| V5-CERT-02 | Certificazione V5 9/10 e confronto V4 | — | — | Non certificata; non ripetere holdout diagnostici | DA FARE |

## Obblighi di manutenzione

1. Registrare ogni nuovo report con percorso, checksum SHA-256, commit, dataset e parametri quando disponibili. Non inventare digest o versioni.
2. Chiudere le attività nel TODO **solo** se il relativo criterio è dimostrato. Conservare la cronologia qui.
3. Prima di proporre un comando VPS, verificare che non ripeta un esperimento già concluso.
4. Documentare regressioni e rollback prima di modificare un entry point funzionante; non alterare Chroma né baseline V4 senza autorizzazione.
5. Per report disponibili soltanto nella conversazione o sulla VPS, dichiarare esplicitamente la lacuna di archiviazione Git.

## Decisione integrazione controllata — 2026-10-23

- **Attività:** V5-REF-05; **script:** `rag_v5_fresh_reference_e2e_shadow_v1.py --priority-exact`; **commit:** `bbb9b7b`.
- **Report acquisito:** `rag_v5_live_priority_integration_v1.json`, SHA-256 `0503e2dcc94be563a7176f0768b869360a6a2465411d4e454688f06fa21512fc` (allegato in chat, non archiviato Git). **Risultato:** 4/B F1→F1; 6/B F1,F5→F1,F2; fig9 F5→F1; fig20 F1→F1; top8 stesso insieme di ID in 4/4; Chroma 5319→5319, `index_writes=false`, `generation_requested=false`. **Decisione:** VALIDATO limitatamente al riordino live source-aware opt-in. Conservare flag disattivato per default; candidato locked invariato. La qualità della risposta fig20 non è stata valutata da questo report. **Stato:** VALIDATO.
- **Differenza tecnica rispetto ai test già conclusi:** questo script applica la priorità *durante un retrieval live con embedding, filtro fonte e reranker*, non rigioca punteggi salvati. Il successivo test deve limitarsi a verificare questa integrazione, non ripetere la campagna di benchmark.
- **Rollback:** omettere `--priority-exact`; il comportamento precedente è conservato. Non sono previste scritture Chroma.


## V5-REF-06 — Trasferimento nel runner effettivo (2026-10-23)

- **Attività:** inserire priorità esatta nel runner richiamato dal candidato V5.
- **Script:** `scripts/smoke_test_rag_v5_e2e.py`; **commit:** `a0301b6489443ef7ac0a954af981ea09f7704676`.
- **Report:** non disponibile. **Risultato:** opzione `--priority-exact` aggiunta al runner, disattivata per default; lookup esatto limitato a domande con fonte Ussia/Foscarini esplicita; Chroma non scritto.
- **Decisione:** IMPLEMENTATO (runner e wrapper pubblicati). Il forwarding dal wrapper `run_rag_v5_locked_candidate_v2.py` è stato pubblicato nel commit `2a2ceb9409aaa2e35a1ecd7464029037277d575b`; non dichiarare INTEGRATO prima della regressione runtime. Verifica statica e regressione runtime mirata ancora mancanti. Il gold candidato resta immutato.
- **Rollback:** omettere il flag; nessuna migrazione dell'indice.

- **Sblocco 2026-10-23:** wrapper `scripts/run_rag_v5_locked_candidate_v2.py` aggiornato nel commit `2a2ceb9409aaa2e35a1ecd7464029037277d575b`: il flag opt-in è inoltrato al runner; senza flag comportamento precedente. **Stato:** IMPLEMENTATO. Verifica statica e regressione runtime ancora DA FARE; non ripetere benchmark shadow.

### V5-REF-06 preflight mirato

Commit `a8cfef6`: gestione distanze assenti per chunk lessicali e opzioni `--retrieval-only`, `--probe-question` nel runner effettivo. Nessun report runtime disponibile. Stato: IMPLEMENTATO. Prova successiva: una domanda diagnostica, niente gold e niente generazione; verificare F1, indice immutato e assenza errori.

### V5-REF-06 — Esito probe runner effettivo (2026-10-23)

- Attività: regressione mirata del percorso opt-in nel runner effettivo, distinta dai test shadow già conclusi.
- Script: `scripts/smoke_test_rag_v5_e2e.py`, commit `a8cfef6a84d259a78606524f24a61659ca00cfb1`.
- Report: `rag_v5_effective_priority_probe_v1.json`, ricevuto in chat; SHA-256 `e52c802051873703c197e8b28123a580a3b56a2268a2309b11e4d5f764f6bbda`.
- Risultato: Foscarini figura 20 promossa a F1, un candidato esatto, 8 evidenze; Chroma 5319 prima e dopo; retrieval-only, nessuna risposta generata, nessun errore nel report.
- Decisione: VALIDATO per la sola probe del retrieval nel runner effettivo. Il forwarding wrapper è verificato staticamente, non esercitato in questa probe. Nessuna certificazione E2E o qualità della risposta; mantenere opt-in default off.
- Stato: VALIDATO (probe retrieval); integrazione end-to-end del candidato locked ancora DA FARE.

### V5-REF-07 — Verifica risposta nel runner effettivo (2026-10-23)

Attività: verificare la generazione di una sola risposta per Foscarini figura 20 nel runner effettivo con priorità opt-in, dopo probe retrieval VALIDATA V5-REF-06. Script: `scripts/smoke_test_rag_v5_e2e.py`, commit `00c3a7766f1703cc08a415737ad6a06345ddc92e`; la domanda singola è ora ammessa anche con generazione. Report atteso: `rag_v5_effective_priority_answer_fig20_v1.json`. Risultato e decisione in attesa del report VPS. Stato: IMPLEMENTATO. Differenza dal precedente shadow: percorso generativo effettivo dopo dense24, mMARCO, collapse alias e promozione exact; non è benchmark gold.

### V5-REF-07 follow-up

Il report di risposta figura 20 evidenzia attribuzione non supportata del ruolo del giocatore 7. Esito ESEGUITO, accuratezza non VALIDATA. Correzione mirata del prompt nel commit `f22ade7`: vincoli sui ruoli e sui soggetti, senza modificare retrieval. Stato IMPLEMENTATO; attesa verifica differenziale.

### V5-REF-07 verifica differenziale — esito

Script `scripts/smoke_test_rag_v5_e2e.py`, prompt commit `f22ade7`; report `rag_v5_effective_priority_answer_fig20_promptfix_v1.json`, SHA-256 `d2d071ca77ec43b9132fff19a553f191d0e19f17129466f1a715eafb1e81f05a`. Risultato: Foscarini F1, scambio 4/3, incrocio mediani, movimenti 7 e 6 corretti; il 7 non viene piu definito mediano. Citazioni F1/F2/F4 esistenti; F2 e F4 sono digressioni non richieste. Chroma 5319 prima e dopo; 101,8 s. Decisione: VALIDATO per la correzione puntuale dell'attribuzione dei ruoli, non CERTIFICATO come qualita generale o integrazione locked. Nessun nuovo test equivalente.

### V5-CERT-02 — Gate revisione indipendente

Attivita: protocollo per revisione e freeze del candidato v2. Artefatto: `docs/rag-v5-independent-review-gate-v1.md`, commit `0c79578`. Nessuna esecuzione o report. Risultato: checklist pronta; candidato invariato. Decisione: richiedere revisore indipendente e fingerprint runtime prima del freeze. Stato protocollo: IMPLEMENTATO; certificazione: BLOCCATO.
