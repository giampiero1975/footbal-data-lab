# RAG V5 — Registro qualità consolidato (22 ottobre 2026)

## Obiettivo
**9/10 di qualità nelle risposte tattiche**, da dimostrare su un insieme indipendente di domande e criteri espliciti. Non è un risultato già raggiunto.

## Versioni: non confondere
- **RAG V5** = motore in validazione, invariato.
- **Shadow NLI V2/V3** = varianti del controllo fedeltà fonte-affermazione.
- **Judge alignment V1/V2** = varianti del controllo risposta-domanda.
- Numeri dei giudici non sono versioni del RAG.

## Evidenze recuperate dal repository
| Test | Esito osservato | Interpretazione |
|---|---|---|
| Retrieval baseline iniziale | MRR ~0,697 (risultato storico) | Non misura qualità completa delle risposte |
| Generazione focus iniziale | ~7/10 qualitativo (risultato storico) | Non certifica qualità RAG V5 |
| Multi-source iniziale | 0/2 (risultato storico) | Criticità originaria, non prova dello stato attuale |
| Shadow NLI baseline | 20/20 coppie supported; 15/15 claim supported | Sono predizioni del giudice, non 100% correttezza: revisione manuale ha individuato possibili falsi positivi |
| NLI adversarial V2 | 9/11, zero errori | Controlli curati, non gold indipendente |
| NLI experimental V3 | 7/11 | Peggioramento sullo stesso insieme: respinto |
| NLI atomic V1 | 13/15 | Campione differente; non confrontare come trend |
| NLI contrastive V1 | 4/12 | Debolezza su comparativi e quantificatori |
| Alignment judge V1 | 6/10 accordi provvisori | Misura giudice, non qualità RAG |
| Alignment judge V2 | 6/10 accordi provvisori | Un verdetto cambiato, nessun miglioramento netto |

## Errori concreti da non perdere
1. Domanda su cambio modulo durante una partita: risposta con proprietà statiche dei moduli, pur con fonti citate.
2. Universalizzazione: fonte dice 'in tutti e tre i sistemi', risposta o giudice interpreta 'in qualsiasi sistema'.
3. Contro blocco basso: rischio di invertire raccomandazione ampiezza vs verticalizzazione.
4. Affermazioni composite supportate solo parzialmente da singoli estratti.
5. Confusione tra movimento delle linee di passaggio e cambio del modulo.

## Gate verso 9/10
Valutare separatamente retrieval, fedeltà fattuale, pertinenza alla domanda, completezza e coerenza tattica. Prima stabilire rubric con giudizio umano indipendente e holdout multisorgente, poi testare RAG V5 congelato. Non trasformare il 6/10 dei giudici in un punteggio del motore.

## Conservazione e reversibilità
Non cancellare JSON o baseline. Non modificare Chroma, retrieval, prompt di produzione, modelli o NLI canonico senza regressioni controllate. Script shadow restano separati.

## Provenienza
Documentazione GitHub consultata:
- docs/rag-v5-shadow-nli-baseline-20261022.md
- docs/rag-v5-shadow-nli-adversarial-20261022.md
- docs/rag-v5-shadow-nli-v3-comparison-20261022.md
- docs/rag-v5-shadow-nli-atomic-v1-results-20261022.md
- docs/rag-v5-shadow-nli-contrastive-v1-results-20261022.md
- docs/rag-v5-alignment-judge-shadow-results-20261022.md
- docs/rag-v5-status-and-judge-v1-v2-20261022.md

I dati sono tratti dai report storici documentati e da quelli forniti dall'utente; la VPS non è stata interrogata direttamente. Per le prossime verifiche tecniche consultare documentazione ufficiale delle configurazioni effettivamente coinvolte.
