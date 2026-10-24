# TODO — Acquisizione automatica FIGC per DRIBBLING

Stato: **IMPLEMENTATO** monitor v1; collaudo shadow VPS DA FARE. Non modificare la collection V5 integrata prima dei test di ingestione incrementale e deduplicazione.

## Query giornaliere da conservare esattamente

1. `site:figc.it/media/ "uefa pro" tattica filetype:pdf`
2. `site:figc.it/media/ tesi (tattica OR "modello di gioco" OR "sistemi di gioco" OR modulo OR moduli) filetype:pdf`

## Requisiti

- Cron giornaliero di discovery; controllare anche pagine/archivi ufficiali FIGC e gli allegati delle schede tesi, perché i motori di ricerca non garantiscono copertura completa.
- Rilevare gli URL PDF effettivi, non confondere una pagina di presentazione con il file scaricabile.
- Verificare accessibilità, risposta HTTP, MIME, firma PDF e integrità del file; registrare fallimenti e retry.
- Registro persistente di documenti noti, URL, autore, titolo, date, hash SHA-256, pertinenza, categoria, stato e riferimenti di indicizzazione.
- Storico append-only di discovery, download, errori, classificazione, scarti e ingestion.
- Classificare il contenuto effettivo (tattica, tecnica, allenamenti, non pertinente); se un PDF è misto, valutare le sezioni.
- Deduplicare per contenuto e somiglianza, non solo URL/nome. Evitare download e reindicizzazione superflui.
- Ingestion Docling → chunk → embedding → ChromaDB solo dopo test reversibili, integrità e regressione RAG; preservare V5 attuale.
- Censimento iniziale dell'archivio storico FIGC e successivo monitoraggio incrementale.

## Implementazione v1

- `scripts/figc_pdf_discovery.py`: dry-run predefinito, allowlist HTTPS FIGC, crawl limitato della categoria Tesi e delle pagine news, URL candidati espliciti, verifica MIME/firma PDF/limite dimensione/SHA-256.
- `--write` abilita download atomico in area candidata, report JSON e storico JSONL append-only; nessuna ingestion o scrittura Chroma.
- Classificazione prudente: `tattica`, `tecnica`, `allenamenti`, `review_required`; nessuna categoria incerta viene indicizzata automaticamente.
- Deduplica binaria segnalata per SHA-256; similarità testuale e scheduling giornaliero restano DA FARE dopo il collaudo shadow.

## Esempi di URL da validare nel collaudo

- https://www.figc.it/media/265344/spalla_tesi-uefa-pro.pdf
- https://www.figc.it/media/208515/maldera_tesi-uefa-pro.pdf
- https://figc.it/media/246820/contran_uefa-pro.pdf

I tre URL sono candidati citati nella conversazione, non una certificazione di scaricabilità corrente.
