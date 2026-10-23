# V5-USSIA-4A-CHUNK-CODE-01 — audit statico

Stato: ESEGUITO. Nessun test VPS e nessuna modifica a Chroma.

## Evidenze
- Script GitHub: `scripts/build_rag_index_v5_multisource.py`.
- `HybridChunker(tokenizer=HuggingFaceTokenizer(... max_tokens=512), merge_peers=True)`.
- `contextualized = chunker.contextualize(chunk).strip()`; `headings` da `chunk.meta.headings`; `page_numbers` da `chunk.meta.doc_items[*].prov[*].page_no`.
- ID `sha256(f'{relative}:{index}:{contextualized}')`: cambiare il testo cambia gli ID.
- Report VPS preesistente `evaluation/ussia_4a_chunk_mapping_v1.json`: elemento Docling `#/texts/151` = `Esercitazione 4/A` a pagina 14; `#/texts/154` = svolgimento; chunk 10 include svolgimento, heading solo `SVOLGIMENTO:`, pagine `[12,13,14]`; chunk 45 è indice pagina 48.

## Risultato e decisione
Il codice non integra un recupero dell'intestazione superiore quando `chunk.meta.headings` la omette. L'associazione errata è osservata nei dati; la responsabilità precisa di Docling/struttura JSON non è dimostrata senza un'ispezione isolata del comportamento. Non ripetere il mapping o il retrieval già eseguiti. Progettare una correzione opt-in o una versione separata dei chunk con confini e intestazioni coerenti; prima di scrivere un indice richiedere piano di migrazione, rollback e confronto distinto. Non usare `--write` sul V5 attuale.
