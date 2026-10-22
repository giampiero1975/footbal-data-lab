# RAG V5 — Question alignment e scope, diagnostica Q4/Q5 (2026-10-22)

## Stato e provenienza

- **Stato:** revisione diagnostica provvisoria, **non gold**, non stima di accuratezza generale.
- **Fonte verificata:** JSON `rag_v5_question_alignment_diagnostic_v1.json` fornito dall'utente il 2026-10-22; valori ispezionati direttamente dal file ricevuto, **non** letti direttamente dalla VPS.
- **Baseline:** `evaluation/reports/rag_v5_shadow_baseline_20261022_v2.json` (5 domande).
- **Annotazioni:** `evaluation/annotations/rag_v5_shadow_claims_q4_q5_v2.json`; estrazione riproducibile tramite `scripts/prepare_rag_v5_shadow_q4_q5_v2.py`.
- **NLI:** `evaluation/reports/rag_v5_shadow_nli_q4_q5_results_v2.json`, `scripts/shadow_nli_v2_inference.py`; `qwen3.5:9b`, istruzione V2, JSON strutturato, `think=false`.
- **Diagnostica:** `scripts/diagnose_rag_v5_question_alignment_v1.py` -> `evaluation/reports/rag_v5_question_alignment_diagnostic_v1.json`.
- I report sono percorsi VPS; **non** presumere che i file JSON generati siano versionati in Git. Non sovrascrivere baseline e report precedenti.

## Risultati osservati

| Dimensione | Q4 | Q5 | Totale |
|---|---:|---:|---:|
| Claim selezionati | 4 | 6 | 10 |
| NLI supported (livello claim) | 4 | 6 | 10 |
| Pertinenza direct | 4 | 0 | 4 |
| Pertinenza contextual | 0 | 4 | 4 |
| Pertinenza off_target | 0 | 2 | 2 |
| Scope preserved | 2 | 3 | 5 |
| Scope needs_context | 2 | 2 | 4 |
| Scope overgeneralized | 0 | 1 | 1 |

Il test NLI precedente ha completato **13/13 coppie** senza errori, tutte etichettate `supported`. I conteggi sopra sono a livello claim, non di coppia. Il sottoinsieme Q4/Q5 è stato scelto intenzionalmente per diagnosticare criticità, non estratto casualmente.

## Evidenze puntuali e interpretazione

- **Q4 / q4_diag_02 e q4_diag_03:** direttamente pertinenti al gioco a triangoli, ma la fonte F6 parla dei vantaggi di uno specifico sistema di gioco; nella risposta il contesto del sistema non è sufficientemente esplicitato. Revisione: `needs_context`.
- **Q5 / q5_diag_01 e q5_diag_02:** F1/F2 sostengono contrattacco e densità centrale dei sistemi descritti, **non** dimostrano gli effetti di cambiare sistema *durante una partita*. Revisione: `contextual`.
- **Q5 / q5_diag_03:** la risposta dice `indipendentemente dal sistema adottato`; le fonti F1/F2 si riferiscono ai **tre sistemi analizzati**, non a tutti i sistemi. Il giudice NLI ha comunque prodotto `supported`: possibile falso positivo per generalizzazione, da sottoporre ad adjudication indipendente.
- **Q5 / q5_diag_04:** svantaggi del gioco a zona (F3), senza rapporto dimostrato con la scelta di variare il sistema in gara. Revisione: `off_target`.
- **Q5 / q5_diag_05:** criticità difensive del 3-4-1-2 (F5), pertinenti come contesto solo se si passa a quel modulo; la fonte non discute la transizione in gara. Revisione: `contextual` e `needs_context`.
- **Q5 / q5_diag_06:** apertura/chiusura delle linee di passaggio durante una singola azione (F8), fenomeno distinto dai rischi del cambio di modulo. Revisione: `off_target`.

## Decisione tecnica

1. **PASS tecnico** per esecuzione NLI 13/13, senza errori; **NO** alla conclusione che 13/13 equivalga a qualità o pertinenza perfetta.
2. **Non modificare** retrieval, prompt, Chroma, modello o baseline validata sulla base di questo solo campione.
3. Separare nella futura valutazione **faithfulness** (supporto testuale), **question alignment** (risposta alla domanda) e **scope fidelity** (condizioni, quantificatori e sistema di riferimento).
4. Prima di automatizzare il giudizio di pertinenza, costruire controlli positivi/negativi e far revisionare indipendentemente le etichette provvisorie; evitare di usare le stesse ipotesi come gold per misurare il giudice.
5. Per Q5, valutare una futura regressione che distingua esplicitamente **proprietà statiche dei moduli** da **vantaggi, rischi e condizioni del passaggio di modulo in corso di partita**.

## Limiti

- Le etichette `direct/contextual/off_target` e `preserved/needs_context/overgeneralized` sono ipotesi di revisione codificate nello script diagnostico, **non inferenze indipendenti di un secondo modello**.
- Non è stata dimostrata l'accuratezza del classificatore né misurata la qualità dell'intero RAG V5.
- I risultati riguardano solo 10 claim di Q4 e Q5; il report originale contiene cinque domande.
- Nessuna modifica alla pipeline di produzione è stata eseguita in questa fase.

## Riferimenti di implementazione

- `projects/tactical-engine/scripts/prepare_rag_v5_shadow_q4_q5_v2.py`
- `projects/tactical-engine/scripts/shadow_nli_v2_offline.py`
- `projects/tactical-engine/scripts/shadow_nli_v2_inference.py`
- `projects/tactical-engine/scripts/diagnose_rag_v5_question_alignment_v1.py`
- `projects/tactical-engine/docs/rag-v5-shadow-nli-baseline-20261022.md`
- `projects/tactical-engine/docs/nli-v2-shadow-integration.md`
