# Knowledge Panel API v1

Data: 2026-10-25. Stato: API read-only VALIDATA; pannello INTEGRATO localmente.

## Attività e differenza tecnica

Primo consumer applicativo read-only dell'API RAG, derivato dalla specifica `TODO_KNOWLEDGE_BASE_PANEL.md`. Non ripete il test generativo: legge la collection operativa senza embedding, LLM o scritture e rende ispezionabili inventario, copertura e provenienza.

## Audit reale iniziale

Collection `dribbling_tactics_v5_multisource_drive11_candidate_v1`: 6196 chunk, 152 fonti, `hnsw:space=cosine`, pipeline `v5_multisource`, embedding `qwen3-embedding:0.6b`. I dieci campi metadata osservati sono presenti su tutti i record; quattro `raw_text` sono vuoti, ma nessun documento indicizzato è vuoto.

## Contratto implementato

- `GET /v1/knowledge/stats`: conteggi e configurazione effettiva della collection;
- `GET /v1/knowledge/documents?offset=0&limit=25`: inventario paginato per fonte;
- `GET /v1/knowledge/search?q=pressing&limit=20`: ricerca lessicale read-only con chunk, fonte e pagina;
- tutti gli endpoint richiedono lo stesso Bearer token dell'API;
- catalogo derivato in memoria al primo accesso; nessuna scrittura Chroma.

Script: `api/knowledge_catalog.py`, `api/rag_v5_api.py`. Test: `tests/test_knowledge_catalog.py`, `tests/test_rag_v5_api.py`. Commit: DA FARE. Risultato: IMPLEMENTATO. Decisione: eseguire test offline e smoke HTTP VPS; integrare una UI soltanto dopo corrispondenza esatta 6196/152 e provenienza verificata. Stato: IMPLEMENTATO.

## Evidenza API VPS

Suite 7/7 PASS. Smoke autenticato: stats 200 con 6196/152; documenti 200 e paginazione corretta; ricerca `pressing` 200 con fonte e pagina; health/readiness 200. Primo caricamento del catalogo 1355,90 ms, chiamate successive 1,72–38,42 ms. Collection invariata.

## Consumer web

`GET /panel` serve un'interfaccia locale statica con inventario, ricerca e submit/polling delle domande RAG. Il token viene inserito dall'utente, mantenuto soltanto in memoria JavaScript e non incorporato o salvato. CSP, `nosniff`, no-referrer e no-store sono impostati dalla risposta HTTP. Il bind rimane localhost: l'accesso remoto richiede tunnel SSH e non espone 8088 su Internet.

Script: `api/knowledge_panel.html`, `api/rag_v5_api.py`. Risultato: 8/8 test, `/panel` HTTP 200, CSP presente, nessun segreto incorporato, inventario completo su più pagine e mapping reale `questions[0].answer`. Decisione: consumer locale INTEGRATO; conservare bind localhost e usare tunnel SSH. La vista Qualità e l'integrazione degli stati FIGC restano incrementi separati. Stato: INTEGRATO.
