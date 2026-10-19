# Inventario statico script — primo lotto verificato

Data: 2026-10-19. **Verificato su codice GitHub; nessuna esecuzione sulla VPS.** La classificazione non dimostra l'utilizzo operativo e non autorizza cancellazioni.

| Script | Funzione dal codice | Lettura/scrittura | Dipendenze e attenzione |
|---|---|---|---|
| `ask_dribbling.py` | Interrogazione collection V1 | Query | Modello `qwen3:4b-instruct` non presente nell'ultimo inventario Ollama; possibile storico |
| `build_rag_index.py` | Indicizzazione V1 Nomic | **Scrive e cancella** record obsoleti con `collection.delete` | Non eseguire come audit; rischio di mutazione dell'indice |
| `build_rag_index_v2.py` | Costruzione collection V2 Nomic | Scrive indice | Non eseguire senza backup e manifest |
| `build_rag_index_v3.py` | Docling HybridChunker e indice V3 Nomic | Scrive indice | Baseline storica, 86 chunk dichiarati |
| `build_rag_index_v4_qwen_embedding.py` | Copia e re-embedding da V3 a V4 Qwen | Scrive indice | Non rigenerare V4 funzionante; controlla esistenza target |
| `test_dribbling_v4_top5_top10.py` | Qwen V4 + mMARCO + Qwen3.5; top5/10 | Query Chroma, **scrive report** `risposte_v4_top5_top10.txt` | L'intestazione «sola lettura» riguarda gli indici, non il filesystem |
| `test_dribbling_v5_strutturato.py` | Test claim e citazioni Qwen V4 | Query, **scrive report** | Fedeltà semantica non ancora validata |
| `test_risposte_dribbling_v4_1.py` | Test generazione V3/Nomic/BGE | Query, **scrive report** | Nome V4 non identifica collection V4 |
| `test_risposte_dribbling_v4_qwen35.py` | Test generazione V3/Nomic/BGE | Query, **scrive report** | Nome V4 non identifica collection V4 |
| `diagnosi_compact_dribbling_v4.py` | Diagnostica compact | Query e metodi privati LlamaIndex | Importa costanti da `test_dribbling_v4_top5_top10.py`; import sicuro finché main guard rimane |
| `diagnosi_repack_refine_dribbling_v4.py` | Diagnostica refine | Query e metodi privati LlamaIndex | Importa costanti dal medesimo test; non genera risposta LLM |
| `benchmark_qwen_query_instruction.py` | EXP-001 query istruita/non istruita | Query e JSON stdout | Gold provvisori; non scrive report |
| `audit_v4_runtime.py` | Ispezione V3/V4 | Query metadata e JSON stdout | `PersistentClient` può effettuare housekeeping interno |
| `audit_script_dependencies.py` | AST inventario script | Legge sorgenti e JSON stdout | Non importa né esegue script target |

## Decisioni di sicurezza

1. Non classificare uno script come totalmente read-only solo perché non muta la collection: alcuni producono report e possono sovrascrivere file.
2. Non eseguire `build_rag_index.py` per test: può rimuovere record V1 ritenuti obsoleti.
3. Non eseguire altri builder prima di aver verificato collection attive, backup, versioni e dipendenze.
4. Gli import tra diagnostiche e script di test sono dipendenze reali: non archiviare `test_dribbling_v4_top5_top10.py` senza modificare le diagnostiche.
5. La restante lista di script richiede censimento; l'inventario qui è esplicitamente parziale. Incrociare successivamente con systemd/cron/processi VPS.

## Prossimo controllo non ripetitivo

Censire i rimanenti script e riferimenti esterni; eseguire lo scanner statico senza accesso ai modelli, poi verificare entry point runtime. Documentazione ufficiale dei componenti e versioni in `components.md`; criteri di rollback in `runtime-checklist.md`.

## Secondo lotto — tutti gli altri script storici censiti dal codice GitHub

**Benchmark retrieval e confronto (non scrivono collection):** `benchmark_llamaindex_mmr.py` (V4 Qwen, mMARCO), `benchmark_postrerank_diversity.py` (V4 Qwen, mMARCO, NumPy), `confronta_indici_dribbling.py` (V1/V2), `confronta_reranker_bge_mmarco.py` (V4 Qwen, BGE/mMARCO), `confronta_reranker_bge_qwen.py` (V4 Qwen, BGE e altro modello), `confronta_retrieval_v2_v3.py` (V2/V3 Nomic), `confronta_retriever.py` (V1 Nomic), `diagnosi_q8_ampiezza.py`, `diagnosi_q8_retrieval.py` (V4 Qwen/mMARCO), `diagnosi_retrieval_dribbling.py` (V3/V4, Nomic/Qwen/BGE), `test_reranker.py` e `valida_bge.py` (V1), `test_retrieval_ibrido.py` (V1+V2). **La classificazione è statica:** query e caricamento modelli possono consumare risorse, e Chroma PersistentClient può effettuare housekeeping interno.

**Benchmark che scrivono report su disco:** `confronta_embedding_v3_v4.py` (V3/V4, Nomic/Qwen, BGE), `test_prompt_fedelta_dribbling_v4.py`, `test_prompt_fedelta_dribbling_v4_corretto.py`, `test_prompt_fedelta_dribbling_v5.py`, `test_risposte_dribbling_v3.py` (V3/Nomic/BGE, `qwen3:4b-instruct` assente nell'ultimo inventario), `verifica_fedelta_dribbling_v4.py` (LLM Qwen3.5 e report). Non considerarli read-only del filesystem.

**Ingestion e immagini, scrivono file:** `ingest_pdfs.py` converte PDF in JSON/Markdown e immagini, crea directory e artefatti; `extract_figures.py` estrae figure da PDF e crea directory/file. Sono strumenti di trasformazione del corpus, non test innocui.

**Altri test di generazione/diagnostica:** `prova_risposta_dribbling.py` usa V1/Nomic/BGE e `qwen3:4b-instruct`; `test_ragionamento_applicato_v4.py`, `test_ragionamento_thinking_v4.py`, `test_ragionamento_thinking_16k_v4.py`, `test_ragionamento_thinking_16k_timeout_v4.py` importano direttamente `test_prompt_fedelta_dribbling_v4_corretto` e ne modificano configurazioni a runtime per esperimenti. **Dipendenza diretta verificata**: non archiviare lo script base finché tali esperimenti devono essere riproducibili.

**Nota sul metodo:** le scritture elencate sono dedotte dalle chiamate visibili e non costituiscono audit dinamico di tutte le librerie. L'inventario riguarda tutti i nomi di script presenti nell'elenco GitHub del 2026-10-19, ma non i chiamanti esterni, cron, systemd, processi, documenti o file non Python. La pulizia fisica resta sospesa.

## Classificazione preliminare per gruppi

| Gruppo | Script | Stato |
|---|---|---|
| Costruttori indici | `build_rag_index*.py` | **Scrivono indici**; mantenere, non eseguire come audit |
| Ingestion | `ingest_pdfs.py`, `extract_figures.py` | **Scrivono artefatti**; mantenere |
| Legacy V1/V2 | `ask_dribbling.py`, `prova_risposta_dribbling.py`, `confronta_indici_dribbling.py`, `confronta_retriever.py`, `test_reranker.py`, `valida_bge.py`, `test_retrieval_ibrido.py` | Candidati ad archivio **solo dopo** verifica entry point e dipendenze |
| V3 / confronti | `test_risposte_dribbling_v3.py`, `confronta_retrieval_v2_v3.py`, `confronta_embedding_v3_v4.py`, `diagnosi_retrieval_dribbling.py` | Conservare per regressioni |
| V4/V5 esperimenti | benchmark, diagnostiche, test fedeltà/ragionamento, confronto reranker | Conservare come esperimenti; consolidamento successivo |
| Nuovi audit | `audit_script_dependencies.py`, `audit_v4_runtime.py`, `benchmark_qwen_query_instruction.py` | Creati in GitHub, non validati sulla VPS |

**Risultato:** inventario nominale statico di tutti gli script Python nel percorso GitHub completato; **nessuno è dichiarato inutilizzato o eliminabile**.
