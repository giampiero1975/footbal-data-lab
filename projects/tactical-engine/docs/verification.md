# Protocollo di verifica incrementale

Prima di ogni nuovo controllo: leggere todo.md, verificare l'ultima evidenza registrata e ripetere solo ciò che è cambiato.

Per ogni verifica annotare: componente, versione effettiva, configurazione, data UTC, fonte ufficiale, evidenza, risultato, evento che ne richiede la ripetizione.

Distinguere: verificato nel repository, verificato sulla VPS, raccomandazione ufficiale, ipotesi ed esperimento.

Trigger: cambio prompt -> fedeltà; cambio embedding -> retrieval e compatibilità; cambio reranker -> ranking; cambio LLM -> generazione; cambio dipendenze -> versioni e regressioni; cambio VPS -> inventario runtime.

Durante troubleshooting: un comando per volta e attendere output. Preservare baseline V4 e definire rollback prima di modificare. Non eliminare modelli, collection o dati senza inventario, verifica dipendenze, backup e approvazione.

Conservare su Git solo manifest e report sintetici non sensibili. Indici, PDF, pesi e dump grandi restano fuori Git. Riferimenti: https://git-scm.com/docs/gitignore e https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits

## Audit architetturale A01 — Docling / embedding (2026-10-19)

**Verificato nel repository GitHub, non ancora sul runtime VPS:**
- `scripts/build_rag_index_v3.py`: `HybridChunker` + `HuggingFaceTokenizer(AutoTokenizer.from_pretrained('nomic-ai/nomic-embed-text-v1.5'), max_tokens=512)`, `merge_peers=True`, `contextualize(chunk)`, embedding Nomic; collection `dribbling_tactics_v3_contextualized` con metrica cosine.
- `scripts/build_rag_index_v4_qwen_embedding.py`: legge esattamente 86 testi e metadati V3 e li ricopia in `dribbling_tactics_v4_qwen3_embedding_06b` usando `OllamaEmbedding(model_name='qwen3-embedding:0.6b')`; nessun nuovo chunking; controllo di integrità e rifiuto di sovrascrivere collection target.
- `scripts/ask_dribbling.py` punta alla vecchia V1, Nomic e `qwen3:4b-instruct`: non considerarlo entry point V4 senza prova; quel modello non figura in `ollama list` della VPS.

**Fonti ufficiali consultate:**
- Docling HybridChunker: https://docling-project.github.io/docling/_generated/examples/hybrid_chunking/ — raccomanda tokenizer coerente con embedding.
- Docling chunking concepts: https://docling-project.github.io/docling/concepts/chunking/ — `contextualize` include metadati nei testi per embedding/generazione; import da docling-core supportato.
- Qwen3-Embedding repository: https://github.com/QwenLM/Qwen3-Embedding/blob/main/README.md — istruzioni task-specific raccomandate, soprattutto lato query; il produttore riporta vantaggi medi variabili, non garantiti sul nostro corpus.
- Esempio ufficiale Qwen: https://github.com/QwenLM/Qwen3-Embedding/blob/main/examples/qwen3_embedding_transformers.py — formatta query con `Instruct: ...\\nQuery:...`, documenti senza prefisso instruction.

**Valutazione:** il riuso dei chunk Nomic con embedding Qwen è accertato nel codice, ma non prova un bug né un peggioramento. `max_tokens=512` è un parametro scelto per V3, non un limite del modello Qwen. Non è dimostrato che la V4 aggiunga istruzioni alle query: verificare lo script interrogazione V4 e comportamento della versione installata `llama-index-embeddings-ollama==0.10.0` prima di proporre modifiche. Non presumere che `ask_dribbling.py` sia il runtime.

**Decisione:** mantenere V4 immutata; proporre solo un confronto riproducibile in collection separata dopo aver ricostruito la pipeline effettiva e il gold evidence. Nessuna ottimizzazione dichiarata validata. Ripetere l'audit solo se cambiano codice, embedding, tokenizer o documenti.
