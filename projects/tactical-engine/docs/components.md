# Registro componenti e abbinamenti — audit documentale

Aggiornamento: 2026-10-19. Fonti: inventario VPS in `docs/environment.md`, script GitHub e documentazione ufficiale. **Non è un certificato di compatibilità end-to-end né una modifica runtime.**

| Componente | Versione rilevata | Configurazione osservata nel codice | Evidenza ufficiale | Decisione provvisoria |
|---|---|---|---|---|
| Docling | 2.140.0; docling-core 2.101.1 | `HybridChunker`, `contextualize`, tokenizer Nomic max 512 | [Docling chunking](https://docling-project.github.io/docling/concepts/chunking/) | Mantenere; test tokenizer Qwen in nuova collection |
| Embedding Qwen | Ollama qwen3-embedding:0.6b Q8_0, 1024D; wrapper 0.10.0 | 86 testi V3 ricodificati, query senza `query_instruction` esplicita | [Qwen3-Embedding](https://github.com/QwenLM/Qwen3-Embedding/blob/main/README.md) | Test read-only istruzione query; verificare wrapper della versione |
| Nomic | Ollama nomic-embed-text:latest, 768D | Collection V3 e vecchi test | [Nomic model](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) | Conservare per riproducibilità |
| Chroma | 1.5.9; plugin LlamaIndex 0.6.0 | PersistentClient; V3 cosine; V4 creata senza spazio esplicito | [Chroma distance](https://docs.trychroma.com/docs/collections/configure) | Verificare metrica V4 runtime; non migrare senza necessità |
| LlamaIndex | core 0.14.25; Ollama LLM 0.11.0 | VectorStoreIndex, filtri source, CitationQueryEngine | [Citation engine](https://docs.llamaindex.ai/en/v0.10.17/api_reference/query/query_engines/citation_query_engine.html) (versione storica, NON prova v0.14.25) | Test citazioni 2048/0 vs 512/20; verificare API esatta |
| Reranker | sentence-transformers 6.1.0; plugin 0.6.0 | mMARCO o BGE, CPU, max_length 512 nei benchmark | [CrossEncoder](https://www.sbert.net/docs/cross_encoder/usage/usage.html), [max_length](https://sbert.net/docs/package_reference/cross_encoder/model.html) | Test truncation e gold validati, non scegliere per score grezzo |
| LLM | Ollama server 0.40.5; qwen3.5:9b Q4_K_M | thinking false, context_window 8192, temperatura 0.1 in test V4 | [Ollama docs](https://docs.ollama.com/) | Mantenere fino a benchmark latenza/fedeltà sotto carico |
| Valutazione | pytest 9.1.1 | Gold parzialmente provvisori; regex e citazioni nel range | [CrossEncoderRerankingEvaluator](https://sbert.net/docs/package_reference/cross_encoder/evaluation.html) | Prima validare gold e supporto semantico |

## Rilievi tecnici da non confondere con errori provati

1. **Metrica Chroma V4**: `build_rag_index_v3.py` dichiara `hnsw:space=cosine`; `build_rag_index_v4_qwen_embedding.py` crea collection senza specificare `hnsw:space`. Possibile metrica differente. Non basta leggere lo script per sapere il valore effettivo della collection già presente: controllare configurazione runtime una sola volta.
2. **Troncamento reranker**: `CrossEncoder(max_length=512)` limita la coppia query+documento; non garantisce lettura integrale di tutti i chunk contextualized. La documentazione ufficiale dice che input lunghi vengono troncati. Verificare distribuzione lunghezze prima di modificare.
3. **Identità V4**: script chiamati V4 interrogano talvolta V3/Nomic/BGE e talvolta V4/Qwen/mMARCO. Usare manifest univoco, non nome file, per comparazioni.
4. **CitationQueryEngine**: lo split in source nodes e il `compact` rendono insufficienti check numerici. Gold di evidenza e fedeltà semantica sono prioritari.
5. **Istruzioni query Qwen**: non presenti esplicitamente nel codice V4 ispezionato; verificare il wrapper esatto e il preprocessing Ollama, poi A/B read-only.
6. **Componenti storici**: nessuna rimozione finché entry point e dipendenze non sono censiti.

## Sequenza sperimentale, una variabile alla volta

- **E0 — Baseline**: identificare entry point runtime, collection, modello, prompt, digest e gold; snapshot/backup verificato prima di qualunque scrittura.
- **E1 — Query Qwen**: confrontare query attuale vs istruzione Qwen con identici embedding corpus, filtri, top-k e reranker; misurare recall@k e MRR su gold validati.
- **E2 — Metrica Chroma**: leggere configurazione reale e misurare impatto solo se difforme; eventuale indice alternativo isolato, mai modifica in-place.
- **E3 — Reranker**: misurare troncamento e confrontare mMARCO/BGE con identici candidati; registrare tempi CPU, copertura, nDCG/MRR.
- **E4 — Citazioni**: confronto 2048/0 vs 512/20 a retrieval invariato; giudicare fedeltà claim→passaggio, completezza, tempi.
- **E5 — Chunker**: nuovo indice con tokenizer Qwen e chunking documentato, confrontando qualità e memoria; mai sovrascrivere V4.
- **E6 — Consolidamento**: solo dopo benchmark riproducibili, configurazione dichiarativa e pulizia componenti inutilizzati con rollback.

**Stato:** audit statico avviato, nessun benchmark eseguito, nessuna configurazione dichiarata ottimizzata o pronta alla sostituzione. Nessuna modifica alla VPS.

## Riscontri sperimentali e runtime — 2026-10-19

- **Chroma verificato sulla VPS:** V3 `dribbling_tactics_v3_contextualized` = 86 chunk, 768 dimensioni, spazio HNSW cosine; V4 `dribbling_tactics_v4_qwen3_embedding_06b` = 86 chunk, 1024 dimensioni, spazio HNSW L2. Entrambe contengono 49 record `334_principi_Glerean` e 37 `il_3412_Giustinetti`, con ID unici. L'audit V4 su tutti gli 86 vettori ha trovato norme vicine a 1 (deviazione massima circa 5e-7) e nessun valore non finito. La differenza L2/cosine **non giustifica da sola** la ricostruzione della collection: per vettori unitari i ranking esatti sono equivalenti, pur potendo differire le approssimazioni HNSW.
- **EXP-001 eseguito:** benchmark A/B read-only su nove query, otto con gold ID **provvisori**, top-15, filtro sorgente. Recall@15 = 1,0 per baseline e instruction; MRR del primo gold baseline = 0,6354167, instruction = 0,46875; tempo medio embedding baseline = 0,09533 s, instruction = 0,17956 s. Baseline migliore in quattro domande, parità in quattro, instruction mai migliore. **Decisione provvisoria: mantenere query baseline senza istruzione aggiunta.** Non prova la fedeltà delle risposte né la qualità con reranker e gold validati.
- **Servizio/modelli:** Ollama attivo e tre modelli installati; nessun servizio DRIBBLING dedicato individuato dai controlli nominali. La pipeline end-to-end V4 con reranker e generazione non è ancora stata validata.

**Aggiornamento rispetto allo stato iniziale:** audit metrica e benchmark query ora eseguiti; le sezioni precedenti restano traccia delle ipotesi e del piano prima delle misurazioni. Non confondere i risultati sperimentali con una configurazione di produzione approvata.
