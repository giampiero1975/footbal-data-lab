# TODO — Acquisizione automatica FIGC per DRIBBLING

Stato: **VALIDATO** monitor v1; scheduling settimanale INTEGRATO. Non modificare la collection V5 integrata prima dei test di ingestione incrementale e deduplicazione.

## Query da conservare esattamente

1. `site:figc.it/media/ "uefa pro" tattica filetype:pdf`
2. `site:figc.it/media/ tesi (tattica OR "modello di gioco" OR "sistemi di gioco" OR modulo OR moduli) filetype:pdf`

## Requisiti

- [x] Timer settimanale di discovery, sabato alle 03:15 con jitter massimo 30 minuti; controlla pagine/archivi ufficiali FIGC e allegati delle schede tesi.
- Rilevare gli URL PDF effettivi, non confondere una pagina di presentazione con il file scaricabile.
- Verificare accessibilità, risposta HTTP, MIME, firma PDF e integrità del file; registrare fallimenti e retry.
- [x] Catalogo corrente atomico per hash e storico JSONL append-only di discovery/download/errori.
- [ ] Arricchire il catalogo con autore/date estratti, revisione editoriale e riferimenti di indicizzazione.
- Classificare il contenuto effettivo (tattica, tecnica, allenamenti, non pertinente); se un PDF è misto, valutare le sezioni.
- [x] Deduplicare binariamente per SHA-256 contro corpus e download del monitor.
- [ ] Aggiungere similarità testuale per revisioni quasi duplicate.
- Ingestion Docling → chunk → embedding → ChromaDB solo dopo test reversibili, integrità e regressione RAG; preservare V5 attuale.
- [ ] Ampliare gradualmente il censimento storico; collaudo unit completato su 30 pagine (10 PDF, 2 duplicati, 8 candidati, 0 errori).

## Implementazione v1

- `scripts/figc_pdf_discovery.py`: dry-run predefinito, allowlist HTTPS FIGC, crawl limitato della categoria Tesi e delle pagine news, URL candidati espliciti, verifica MIME/firma PDF/limite dimensione/SHA-256.
- `--write` abilita download atomico in area candidata, report JSON e storico JSONL append-only; nessuna ingestion o scrittura Chroma.
- Classificazione prudente: `tattica`, `tecnica`, `allenamenti`, `review_required`; nessuna categoria incerta viene indicizzata automaticamente.
- Deduplica SHA-256 contro i corpus e contro i download del monitor; catalogo corrente scritto atomicamente.
- Unit e timer utente in `deploy/football-figc-discovery.user.*`.

## Evidenza shadow 2026-10-25

- tre URL storici verificati e riconosciuti come duplicati già presenti;
- crawl bounded: otto pagine, zero errori, un nuovo PDF ufficiale (Maresi, SHA-256 `59eca1b...52bd1`);
- revisione contenuto: scouting/psicologia/organizzazione, non pertinente al corpus tattico; escluso dall'ingestion;
- API RAG invariata sulla collection Drive11 a 6196 record; `/healthz` e `/readyz` restituiscono 200.

## Prossimo incremento autorizzato

- [x] Concludere la review dei tre documenti match/player analysis e registrare la decisione nel catalogo — **VALIDATO** (`docs/figc-match-analysis-editorial-review-01.md`).
- [ ] Escludere dall'ingestion la traduzione inglese del documento relazionale italiano.
- [ ] Creare una collection candidata isolata con i soli PDF pertinenti, quindi verificare integrità, deduplica, retrieval e regressione prima di qualsiasi promozione.

## Esempi di URL da validare nel collaudo

- https://www.figc.it/media/265344/spalla_tesi-uefa-pro.pdf
- https://www.figc.it/media/208515/maldera_tesi-uefa-pro.pdf
- https://figc.it/media/246820/contran_uefa-pro.pdf

I tre URL sono candidati citati nella conversazione, non una certificazione di scaricabilità corrente.
