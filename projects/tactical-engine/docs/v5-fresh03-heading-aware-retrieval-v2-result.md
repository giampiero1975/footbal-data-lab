# V5-FRESH03-HEADING-AWARE-RETRIEVAL-01 — V2

Stato: VALIDATO per il solo retrieval mirato.

Attività: verificare i quattro moduli nel retrieval fresh_03.
Script: run_rag_v5_locked_candidate_v2.py --targeted-coverage --retrieval-only --only-ids fresh_03.
Commit: cfffe6a, 68ca18d, 95d4917, a9334bb.
Report VPS: evaluation/v5_fresh03_heading_aware_retrieval_v2.json (fornito dall'operatore).
Risultato: F1 4-3-3, F2 4-4-2, F3 3-5-2, F4 3-4-2-1; tutti pagina 4, tutti promossi; Chroma 5319 prima/dopo, index_unchanged=true; 2.26 s; nessuna generazione.
Decisione: retrieval scoped VALIDATO; non integrato né certificato. Rimane la duplicazione heading nel testo di evidenza, da correggere prima di eventuale generazione; benchmark locked 5/10 invariato.
