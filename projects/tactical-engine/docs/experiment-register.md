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
