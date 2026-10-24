# TODO — Acquisizione automatica FIGC per DRIBBLING

Stato: **VALIDATO** monitor v1; scheduling giornaliero IMPLEMENTATO. Non modificare la collection V5 integrata prima dei test di ingestione incrementale e deduplicazione.

## Query giornaliere da conservare esattamente

1. `site:figc.it/media/ "uefa pro" tattica filetype:pdf`
2. `site:figc.it/media/ tesi (tattica OR "modello di gioco" OR "sistemi di gioco" OR modulo OR moduli) filetype:pdf`

## Requisiti

- [x] Timer giornaliero di discovery; controlla pagine/archivi ufficiali FIGC e gli allegati delle schede tesi.
- Rilevare gli URL PDF effettivi, non confondere una pagina di presentazione con il file scaricabile.
- Verificare accessibilità, risposta HTTP, MIME, firma PDF e integrità del file; registrare fallimenti e retry.
- [x] Catalogo corrente atomico per hash e storico JSONL append-only di discovery/download/errori.
- [ ] Arricchire il catalogo con autore/date estratti, revisione editoriale e riferimenti di indicizzazione.
- Classificare il contenuto effettivo (tattica, tecnica, allenamenti, non pertinente); se un PDF è misto, valutare le sezioni.
- [x] Deduplicare binariamente per SHA-256 contro corpus e download del monitor.
- [ ] Aggiungere similarità testuale per revisioni quasi duplicate.
- Ingestion Docling → chunk → embedding → ChromaDB solo dopo test reversibili, integrità e regressione RAG; preservare V5 attuale.
- [ ] Ampliare gradualmente il censimento storico; il primo crawl bounded di otto pagine è completato.

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

## Esempi di URL da validare nel collaudo

- https://www.figc.it/media/265344/spalla_tesi-uefa-pro.pdf
- https://www.figc.it/media/208515/maldera_tesi-uefa-pro.pdf
- https://figc.it/media/246820/contran_uefa-pro.pdf

I tre URL sono candidati citati nella conversazione, non una certificazione di scaricabilità corrente.
