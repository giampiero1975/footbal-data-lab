# Monitor PDF FIGC v1

Stato: VALIDATO; monitoraggio giornaliero INTEGRATO, ingestion automatica esclusa.

## Scopo

Individuare e verificare PDF tattici pubblicati sui domini ufficiali FIGC senza alterare automaticamente il corpus RAG. Le due query storiche restano registrate esattamente, ma il monitor affianca un crawl bounded della categoria Tesi e delle pagine news perché l'indice dei motori di ricerca può essere incompleto.

## Sicurezza e dati

- solo HTTPS e host `figc.it`/`www.figc.it`, più l'endpoint allegati ufficiale collegato dalle pagine FIGC `api.figc.atexcloud.io`, inclusi redirect;
- timeout, massimo pagine e massimo byte configurabili;
- verifica firma `%PDF-`, MIME osservato, SHA-256 e dimensione;
- dry-run predefinito; `--write` usa file temporaneo e rename atomico;
- storico JSONL append-only, catalogo corrente atomico e report JSON separato;
- nessuna chiamata Docling, embedding o Chroma.

La classificazione lessicale è un triage, non una validazione: gli incerti restano `review_required`. La similarità testuale resta DA FARE e l'ingestion richiede sempre revisione e regressione separata.

## Collaudo shadow e decisione

I tre URL storici Spalla/Maldera/Contran sono accessibili e sono stati riconosciuti tramite SHA-256 come documenti già presenti: nessuna copia o reindicizzazione. Il crawl bounded della categoria Tesi e di sette schede ufficiali ha prodotto zero errori e un solo documento nuovo, `Lo scout dedicato_Tesi Maresi.pdf`, SHA-256 `59eca1b8642b2dec921284b643e4636c29d596e907cc1947eddd2a3c17752bd1`.

La revisione delle prime quindici pagine e dell'indice mostra un contenuto centrato su scouting, psicologia professionale e organizzazione dello staff. I riferimenti tattici sono accessori: pertinenza `non pertinente`, decisione `escluso`, nessuna esecuzione Docling/chunk/embedding/Chroma.

La normalizzazione del nome e la deduplica interna sono state validate nell'ambiente VPS: una sola copia fisica, rerun `duplicate_existing`, test 5/5. Il timer utente esegue giornalmente un crawl massimo di 30 pagine con ritardo casuale fino a 30 minuti; il job rimane fail-closed e non può modificare gli indici.

Flusso: Attività = discovery FIGC; Script = `figc_pdf_discovery.py`; Commit = `be0c7f2`, `fa893b9`, `266d8a8`, `5f38313`, `9232e25`; Report = questo documento e JSON runtime; Risultato = shadow superato; Decisione = integrare solo discovery/download candidato, mantenere review e ingestion separate; Stato = VALIDATO per discovery, INTEGRATO per scheduling, non CERTIFICATO per il censimento storico completo.
