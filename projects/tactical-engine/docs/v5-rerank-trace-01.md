# V5-RERANK-TRACE-01

Data: 2026-10-24. Stato: ESEGUITO.

Attivita: diagnosi retrieval e reranking per fresh_03 e fresh_10.
Script: scripts/diagnose_v5_rerank_failures_v1.py (commit c4ee2b5).
Commit: presente report.
Report: `evaluation/runtime-archive/diagnostica_v5_rerank_failures_v1.json`, eseguito sulla VPS e fornito dall'operatore.
Risultato: collection principale 5319 record e candidata 34 prima e dopo; index_unchanged=true.

fresh_03: 24 candidati del recupero globale. Il documento FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale e assente gia dal pool dense24: il reranker non puo promuoverlo. Nessun problema di indicizzazione dimostrato.

fresh_10: 72 candidati nel pool diagnostico. Ussia pagina 17 arriva nella selezione filtrata per fonte, ma si classifica al rango 9 del reranker, appena fuori dalla top8; l'ulteriore candidato relativo alla pagina 17 arriva al rango 16. Il manuale interno Transizioni pagina 3 si classifica al rango 5.

Decisione: mantenere invariati corpus e Chroma, non ripetere il benchmark equivalente, progettare differenze tecniche motivate nella selezione delle fonti e delle pagine. I PDF aggiuntivi Drive restano fuori dal lavoro corrente. La diagnostica non equivale a certificazione e non dimostra ancora miglioramenti di score. Benchmark locked resta 5/10.
Stato: ESEGUITO.
