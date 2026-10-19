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

## Audit architetturale A02 — retrieval, reranker e naming V4 (2026-10-19)

**Verificato nel codice GitHub:**
- `scripts/test_risposte_dribbling_v4_qwen35.py` e `test_risposte_dribbling_v4_1.py` usano collection **V3** `dribbling_tactics_v3_contextualized`, embedding Nomic e reranker `BAAI/bge-reranker-v2-m3`, non la collection Qwen V4. Generazione Qwen3.5 9B, thinking false, temperatura 0.1, contesto 8192; default retrieval 15 candidati, top reranker 5, citation chunks 2048, overlap 0, response_mode compact.
- `scripts/diagnosi_compact_dribbling_v4.py` usa invece collection V4 Qwen, embedding Qwen e reranker `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` top 5/10; filtra metadata `source`; usa API interne `_create_citation_nodes`, `_response_synthesizer`, `_make_compact_text_chunks` per diagnostica: fragili rispetto a upgrade, **non** sostituire senza valutare dipendenze.
- `scripts/confronta_reranker_bge_mmarco.py` confronta BGE/mMARCO con gli stessi candidati Qwen top 15, `CrossEncoder(..., device='cpu', max_length=512)`; gold provvisori, Q8 senza gold. Metriche limitate al benchmark; non provano qualità finale delle risposte.
- `scripts/ask_dribbling.py` è un vecchio entry point V1 con Nomic e `qwen3:4b-instruct` non presente nell'ultimo inventario Ollama. Uso runtime da accertare.

**Rischio architetturale verificato:** la sigla “V4” compare in script che interrogano indici e reranker differenti; benchmark e risultati non sono confrontabili senza registrare esplicitamente configurazione/collection. **Nessuna prova che il sistema operativo usi uno specifico script**.

**Raccomandazioni per test successivi:** identificare entry point reale; rendere manifesto di configurazione esplicito; controllare coerenza embedding scrittura/query, filtri autore, reranker e citations; confrontare test con gold semantici corretti. Nessuna modifica runtime, nessuna cancellazione.

**Documentazione ufficiale da consultare/riconfermare per le versioni installate prima di ogni cambio:** https://docs.llamaindex.ai/ ; https://docs.trychroma.com/ ; https://sbert.net/docs/cross_encoder/usage/usage.html ; https://docs.ollama.com/ . Questo audit A02 è **verifica del codice**, non certificazione di ottimizzazione secondo le fonti ufficiali.

## Audit architetturale A03 — citazioni, gold e API ufficiali (2026-10-19)

**Codice verificato:** `test_dribbling_v4_top5_top10.py` usa Qwen embedding V4, filtro autore Glerean, 15 candidati, mMARCO top 5/10, Qwen3.5 9B e `CitationQueryEngine`; controlla solo riferimenti numerici fuori intervallo e annota che lo split dei citation nodes può rendere inaffidabile il confronto dei node ID con i GOLD. `test_dribbling_v5_strutturato.py` genera claim/estratti JSON e verifica la presenza letterale dell'estratto, marcando esplicitamente `ESTRATTO_PRESENTE_SEMANTICA_NON_VERIFICATA`. `test_prompt_fedelta_dribbling_v4_corretto.py` usa una regex per individuare una frase errata specifica: controllo di regressione ristretto, non metrica generale di fedeltà. `diagnosi_q8_retrieval.py` controlla tre gold Q8 per ID nei primi 30 dense e reranking top 15, ma non costituisce validazione semantica completa.

**Documentazione ufficiale effettivamente consultata il 2026-10-19:**
- Docling: https://docling-project.github.io/docling/concepts/chunking/ — `HybridChunker` parte dalla gerarchia documentale, usa tokenizer scelto dall'utente, split/merge, `contextualize` arricchisce il testo.
- Docling: https://docling-project.github.io/docling/_generated/examples/hybrid_chunking/ — in retrieval il tokenizer chunker dovrebbe essere coerente con quello del modello embedding; `merge_peers=True` è default documentato.

**Conclusioni supportate:** (a) uso di `HybridChunker` e `contextualize` coerente con API documentata; (b) V4 riusa chunk prodotti con tokenizer Nomic, per cui l'allineamento Qwen non è dimostrato; (c) i controlli citazione/range e substring non dimostrano che le affermazioni siano semanticamente sostenute. Nessun parametro alternativo è ancora validato sperimentalmente.

**Prossime verifiche mirate:** versione installata LlamaIndex 0.14.25 e comportamento effettivo CitationQueryEngine; istruzioni Qwen query vs document; filtro autore per domande multi-autore; gold Q8 manuale; misurazione latenza e risorse sotto carico. Evitare di ripetere inventario hardware.

## Audit A04 — API ufficiali Qwen/LlamaIndex/Chroma (2026-10-19)

**Fonti ufficiali verificate online:**
- Qwen3-Embedding README https://github.com/QwenLM/Qwen3-Embedding/blob/main/README.md e esempio https://github.com/QwenLM/Qwen3-Embedding/blob/main/examples/qwen3_embedding_transformers.py: per retrieval raccomandate istruzioni lato query; formato dell'esempio `Instruct: {task_description}\\nQuery:{query}`; documenti senza prefisso di query. Miglioramento medio riportato dal produttore non è garanzia su DRIBBLING.
- LlamaIndex OllamaEmbedding https://developers.llamaindex.ai/python/framework-api-reference/embeddings/ollama/ : `query_instruction` e `text_instruction` opzionali; `_format_query` prepende la prima alla query, se fornita; senza istruzione invia query non prefissata. **Attenzione:** la pagina corrente non garantisce identità esatta con plugin VPS 0.10.0; verificare codice/tag di tale release prima di implementare.
- LlamaIndex CitationQueryEngine https://developers.llamaindex.ai/python/framework-api-reference/query_engine/citation/ : default `citation_chunk_size=512`, `citation_chunk_overlap=20`; usa `SentenceSplitter`, genera nuovi citation nodes, quindi l'ID originale può cambiare. `response_mode='compact'` è modalità supportata. **Attenzione:** documentazione corrente; confrontare con core VPS 0.14.25 prima di modifica.
- Chroma Python https://docs.trychroma.com/reference/python : `PersistentClient` è descritto per uso locale e test; per produzione preferisce istanza server-backed. Per questo progetto CPU/VPS single-node non è ancora dimostrata la necessità di migrare: valutare rischi concorrenza, deploy e backup prima.

**Gap accertato nel codice degli script V4 esaminati:** `OllamaEmbedding(model_name='qwen3-embedding:0.6b', ...)` non passa `query_instruction`; secondo implementazione ufficiale LlamaIndex corrente, la query non riceve istruzione tramite tale wrapper. **Non ancora verificato** se Ollama applica template o preprocessing lato modello: evitare conclusione assoluta sull'input interno del modello.

**Test reversibili proposti (non eseguiti):** A/B retrieval read-only sulla collection V4 con query senza istruzione vs istruzione Qwen formattata; stesso gold semantico, stesso filtro autore, top-k e reranker. Separatamente A/B `citation_chunk_size=2048/512` e overlap `0/20`, mantenendo retrieval e prompt invariati e verificando claim→passaggio, copertura, latenza. Non mescolare variabili in un unico esperimento. Nessuna modifica della baseline.

## Audit A05 — consolidamento dei rischi e dipendenze (2026-10-19)

**Evidenza GitHub:** `diagnosi_repack_refine_dribbling_v4.py` usa metodi e attributi privati LlamaIndex (`_create_citation_nodes`, `_response_synthesizer`, `_make_compact_text_chunks`, `_prompt_helper`), e `test_retrieval_ibrido.py` contiene una deduplicazione manuale basata su inclusione di testo e soglia fissa di 100 caratteri. Sono script diagnostici/sperimentali, non componenti runtime confermati. Non sostituire né rimuovere prima di sapere se sono invocati.

**Coerenza repository:** `projects/tactical-engine/README.md` rimanda a `docs/decisions.md`, ma al controllo tramite GitHub tale percorso restituisce 404: riferimento documentale da correggere o file da creare, non problema runtime dimostrato.

**Vincoli di sicurezza dell'audit:** non lanciare script che scrivono report su VPS, non aggiornare pacchetti, non ricreare indici, non effettuare `git pull` finché non sono noti deploy, baseline e backup. Rimanenti verifiche runtime richiedono accesso VPS o output mirati, non possono essere dedotte dal repository.
