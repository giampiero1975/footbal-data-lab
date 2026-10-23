# V5-LOCKED-CANDIDATE-FAILURE-ANALYSIS-01

Data: 2026-10-24. Stato: ESEGUITO. Diagnosi read-only dei cinque FAIL del benchmark locked V5, da evidenze esistenti. Nessuna nuova esecuzione o patch.

## Evidenze e cause
- fresh_01: estratti Ussia pertinenti presenti; risposta omette l'assenza di dati comparativi e introduce un limite non documentato. Problema di completezza/astensione della generazione.
- fresh_03: manuale Transizioni richiesto assente dalla top8; mancano 4-3-3, 4-4-2, 3-5-2, 3-4-2-1 e avvertenza contro causalità non dimostrata del cambio modulo. Problema di copertura retrieval.
- fresh_07: contaminazione della zona B di Foscarini con zona B di Indiani; percentuale 80% trasferita impropriamente. Problema di attribuzione semantica e tassonomia.
- fresh_09: evidenza pertinente parziale; mancano controllo imperfetto e compromesso tra rischio di nuova perdita e tempo concesso all'avversario; confusione fra consolidamento offensivo e ripiegamento difensivo.
- fresh_10: manca nella top8 la pagina interna 17 di Ussia necessaria per adattamento al sistema e pressione individuale/collettiva; altri estratti Ussia e manuale presenti.

## Meccanismo
Runner: scripts/smoke_test_rag_v5_e2e.py. Chroma main 5319 chunk da 141 PDF; recupero dense24, possibile espansione source-aware fino a 24 candidati per fonte esplicita, reranking mMARCO e top8 globale con deduplica. Il source-aware non garantisce quota per fonte o pagina; il validatore citazioni e solo sintattico. Il report finale non conserva tutti i candidati pre-rerank, percio non e ancora dimostrato se gli estratti mancanti erano nel pool iniziale o persi nel reranking.

## Decisione
Preservare integralmente corpus VPS e collection V5; i PDF aggiuntivi Drive sono fuori dal lavoro attuale (eventuali attivita future soltanto su nuova decisione). Evitare rerun equivalenti. Prossimo passo: verifica read-only dei candidati pre/post rerank per fresh_03 e fresh_10, previa consultazione documentazione ufficiale Chroma e Sentence Transformers. Poi verifica separazione semantica fonti fresh_07 e completezza claim fresh_01/fresh_09. Obiettivo intermedio almeno 8/10, soglia progetto 9/10 non raggiunta. Nessuna integrazione/certificazione.

Flusso: Attivita: diagnosi; Script: runner gia esistente; Commit: questo report; Report: questo documento; Risultato: cinque difetti classificati; Decisione: diagnostica mirata; Stato: ESEGUITO.
