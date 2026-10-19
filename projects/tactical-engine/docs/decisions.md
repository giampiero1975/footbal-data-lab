# DRIBBLING — Registro decisioni architetturali

Aggiornamento 2026-10-19. Stato: **decisioni provvisorie**, basate su audit statico del codice GitHub e inventario VPS riportato in `environment.md`. Non attestano miglioramenti sperimentali.

| ID | Decisione | Motivazione / evidenza | Stato / trigger |
|---|---|---|---|
| D01 | Preservare V4 e le collection storiche | Script V3/V4 e benchmark non equivalenti; serve baseline riproducibile | Confermata come misura conservativa; riesaminare dopo backup e benchmark |
| D02 | Non sostituire Docling/HybridChunker | API ufficiale supportata; mismatch tokenizer V3→V4 è ipotesi, non errore provato | Esperimento E5 |
| D03 | Valutare istruzioni query Qwen | Documentazione ufficiale Qwen raccomanda istruzione task; wrapper V4 non la passa esplicitamente | Esperimento E1, senza reindicizzazione |
| D04 | Non cambiare metrica Chroma in-place | V3 imposta cosine, V4 non esplicita spazio; configurazione reale ancora ignota | Audit collection runtime E2 |
| D05 | Non sostituire mMARCO con BGE sulla sola base di benchmark storici | Gold provvisori e troncamento 512 token non ancora misurato | Esperimento E3 |
| D06 | Non cambiare `citation_chunk_size` o `response_mode` senza test | 2048/0 scelta esplicita; controlli numerici citazioni insufficienti | Esperimento E4 |
| D07 | Nessuna pulizia distruttiva di script, modelli o indici | Entry point e dipendenze runtime non censiti; rollback non validato | Dopo inventario, backup e approvazione |
| D08 | Evitare uso di API private nei nuovi componenti stabili | Diagnostiche usano metodi interni LlamaIndex, suscettibili a cambi versione | Refactor solo dopo conferma uso |
| D09 | Separare test per variabile e manifest configurazione | Script con sigla V4 impiegano talvolta collection V3 e reranker differenti | Preparare manifest di benchmark |

## Documentazione ufficiale di riferimento

- Docling: https://docling-project.github.io/docling/concepts/chunking/
- Qwen3-Embedding: https://github.com/QwenLM/Qwen3-Embedding
- LlamaIndex: https://docs.llamaindex.ai/
- Chroma: https://docs.trychroma.com/
- Sentence Transformers: https://sbert.net/docs/cross_encoder/usage/usage.html
- Ollama: https://docs.ollama.com/

## Criterio di promozione a decisione definitiva

Richiede: (1) versione e configurazione realmente in esecuzione; (2) documentazione ufficiale coerente con release; (3) benchmark su gold verificati; (4) qualità, tempi e risorse misurati; (5) rollback; (6) esito registrato. Non sostituire la V4 sulla base di questo documento.

Consultare `components.md` per la matrice tecnica, `verification.md` per le evidenze e `todo.md` per le attività aperte.
