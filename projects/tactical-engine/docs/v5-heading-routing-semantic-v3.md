V5-HEADING-ROUTING-INTEGRATION-03 — Semantic source ranking

Attività: correggere scelta della fonte emersa dal differenziale v2 (manuale non pertinente malgrado heading riservati).

Script: scripts/v5_source_semantic_rank_v3.py, scripts/v5_heading_reservation_v2.py, scripts/smoke_test_rag_v5_e2e.py.
Commit: cb8cdb1, af903d1, df514a3, 4c8bb24, 362e6cd.

Risultato: IMPLEMENTATO, non ESEGUITO sulla VPS. Ranking con cross-encoder già in uso applicato ai profili dei manuali (titolo e estratti indicizzati); riserva heading invariata. Opt-in --heading-routing, nessun ID benchmark né hardcoding delle quattro formazioni. Non è garantito che il manuale vincente sia quello pertinente: occorre evidenza differenziale.

Decisione: consentito un nuovo test di retrieval/generazione v3 per differenza tecnica documentata rispetto a v2. Verificare fonte in top8, heading, risposta e citazioni, Chroma 5319 invariato, e non attribuire effetti causali non dimostrati. Benchmark locked 5/10 invariato. Stato: IMPLEMENTATO, non VALIDATO, INTEGRATO o CERTIFICATO.
