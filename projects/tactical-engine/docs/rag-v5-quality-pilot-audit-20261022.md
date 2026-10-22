# RAG V5 — Audit qualitativo del pilota a 10 domande (22 ottobre 2026)

## Evidenza
Report utente: `rag_v5_quality_holdout_pilot_results_v1.json`, 10 risposte, collezione `dribbling_tactics_v5_multisource` 5319 chunk, modello `qwen3.5:9b`, retrieval dense24 → mMARCO → collapse alias → top8. Nessuna modifica al motore.

## Triage delle risposte
| ID | Stato preliminare | Osservazione |
|---|---|---|
| 01 | revisione | Confronto pertinente; il libero è descritto come tipico di una specifica organizzazione, non di qualsiasi difesa a uomo |
| 02 | revisione | Il sostegno viene ristretto alle sovrapposizioni; verificare generalizzazioni spaziali |
| 03 | criticità | Confusione tra origine della costruzione (portiere/difensori) e costruzione lunga/corta; attributi fisici dei centrali non rispondono alla scelta |
| 04 | revisione | Movimenti coordinati pertinenti; controllo atomico delle citazioni ancora necessario |
| 05 | criticità | Mescola equilibrio preventivo durante il proprio attacco con temporeggiamento/aggressività durante la difesa |
| 06 | criticità confermata | F2 `Manuale_Diagonali_Difensive`: 'Su palla arretrata la priorità cambia verso il limite area; chi era al primo palo...' descrive una variante difensiva, non la transizione positiva dopo riconquista |
| 07 | criticità | L'affermazione che contro avversario rintanato convenga attaccare la profondità alle spalle della linea richiede prova specifica; possibile inversione della lettura del blocco basso |
| 08 | revisione | Rischi di copertura pertinenti; controllare specifiche prescrizioni sul rientro |
| 09 | criticità confermata | I passaggi top8 non autorizzano a dichiarare che tutte le fonti non documentino cambi volontari; non inferire regole FIFA/UEFA sui cambi di modulo |
| 10 | revisione | Buona distinzione delle fasi, con alcuni riferimenti di transizione negativa da ricontrollare |

## Conteggio, con interpretazione rigorosa
- 10/10 risposte generate.
- 5/10 con criticità nel triage (03, 05, 06, 07, 09), **non equivale a 5/10 qualità**.
- 2 casi (06, 09) con errori di interpretazione delle evidenze direttamente individuati.
- Score complessivo **non assegnato**: manca adjudication claim-by-claim completa.
- I controlli NLI/Judge sono misure separate, non sostituti di questo audit.

## Priorità di intervento (solo shadow, dopo conservazione baseline)
1. Verificare il nesso claim↔passaggio per fase di gioco e causalità; non basta il match semantico.
2. Distinguere condizioni della domanda da argomenti correlati; non rispondere a domanda diversa.
3. Limitare le affermazioni 'le fonti non documentano' ai soli estratti recuperati.
4. Per 07, verificare contro fonte originale il caso di blocco basso prima di definire un errore certo.
5. Terminare la revisione atomica, quindi eseguire regressione su dataset separato.

## Tracciabilità
L'audit JSON derivato è stato creato come file separato `rag_v5_quality_pilot_audit_v1.json`, con SHA256 del report originale, evidenze prioritarie e flag `atomic_claim_review_complete=false`. Conservare tutti i report. Nessuna modifica a RAG V5.
