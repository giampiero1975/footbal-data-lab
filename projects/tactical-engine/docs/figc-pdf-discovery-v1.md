# Monitor PDF FIGC v1

Stato: IMPLEMENTATO; collaudo shadow DA FARE.

## Scopo

Individuare e verificare PDF tattici pubblicati sui domini ufficiali FIGC senza alterare automaticamente il corpus RAG. Le due query storiche restano registrate esattamente, ma il monitor affianca un crawl bounded della categoria Tesi e delle pagine news perché l'indice dei motori di ricerca può essere incompleto.

## Sicurezza e dati

- solo HTTPS e host `figc.it`/`www.figc.it`, inclusi redirect;
- timeout, massimo pagine e massimo byte configurabili;
- verifica firma `%PDF-`, MIME osservato, SHA-256 e dimensione;
- dry-run predefinito; `--write` usa file temporaneo e rename atomico;
- storico JSONL append-only e report JSON separato;
- nessuna chiamata Docling, embedding o Chroma.

La classificazione lessicale è un triage, non una validazione: gli incerti restano `review_required`. La similarità testuale, il cron giornaliero e l'ingestion candidata dipendono dal collaudo shadow.

Flusso: Attività = discovery FIGC; Script = `figc_pdf_discovery.py`; Commit = DA FARE; Report = questo documento; Risultato = IMPLEMENTATO; Decisione = shadow bounded; Stato = IMPLEMENTATO.
