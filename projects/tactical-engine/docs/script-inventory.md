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
