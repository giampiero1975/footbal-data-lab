# Registro esperimenti DRIBBLING

Prima di un test verificare `../docs/verification.md`, `../docs/components.md` e `../docs/decisions.md`. Non confondere test **proposto** con test **eseguito**.

| ID | Ipotesi | Baseline | Variabile isolata | Gold | Risultato | Stato |
|---|---|---|---|---|---|---|
| EXP-001 | Istruzione Qwen sulla query migliora retrieval | Collection Qwen V4, stessi 86 documenti | Prefisso query | Gold semantico da validare | — | Script read-only pronto; non eseguito sulla VPS |
| EXP-002 | Metrica Chroma differente modifica il ranking | V4, metrica runtime da leggere | Spazio vettoriale, solo indice clone | Gold semantico da validare | — | Condizionato a audit |
| EXP-003 | Reranker mMARCO/BGE cambia precisione e latenza | Stessi 15 candidati Qwen e filtri | Modello reranker | Gold da validare | Benchmark storico con gold provvisori | Da validare |
| EXP-004 | Citazioni più granulari migliorano fedeltà | Qwen V4, mMARCO, prompt invariato | `citation_chunk_size` e overlap (test separati) | Claim→evidence manuale | — | Proposto |
| EXP-005 | Tokenizer Qwen migliora retrieval | V4, stessa sorgente PDF | Chunking/nuova collection | Gold da validare | — | Proposto, non sovrascrivere V4 |
| EXP-006 | Troncamento reranker degrada il ranking | Stessi candidati, stesso reranker | Lunghezza token (dopo misura) | Gold da validare | — | Proposto |
| EXP-007 | Formato strutturato aumenta verificabilità | V4 invariata | Generazione/validazione claim | Evidenza semantica | Script `test_dribbling_v5_strutturato.py` presente, esito runtime non accertato | Da valutare |

## Manifest minimo di ogni esecuzione

- Data UTC, ID esperimento, commit Git, snapshot VPS, Python/venv e versioni dipendenze.
- Digest Ollama, collection e count, metrica, sorgenti e checksum.
- Tokenizer, chunker, embedding e istruzioni query/testo, retrieval e filtri, reranker e limiti token.
- LLM, prompt, context window, temperature, thinking, sintetizzatore e citazioni.
- ID domande, gold con pagine/estratti verificati, seed dove applicabile.
- Metriche retrieval (recall@k, MRR/nDCG quando appropriati), fedeltà claim→evidence, completezza, citazioni corrette, latenza, RAM e CPU.
- Esito, decisione, eventuale regressione e rollback.

## Ordine operativo

1. Accertare entry point e collection attivi e fissare la baseline senza modificarla.
2. Validare i gold, distinguendo presenza di stringa da supporto semantico.
3. EXP-001 e audit metrica EXP-002: test di retrieval senza generazione.
4. EXP-003/006: reranker e troncamento, a candidati identici.
5. EXP-004: citazioni e generazione, senza variare retrieval.
6. EXP-005: eventuale nuovo indice solo dopo snapshot e prova di ripristino.
7. EXP-007: valutare se il formato strutturato apporta vantaggi reali.

**Divieti:** nessun `git pull` automatico sulla VPS, nessun overwrite di collection, nessuna disinstallazione di modelli o script storici. Test runtime non eseguiti durante questo audit.

## Implementazione EXP-001 disponibile

`../scripts/benchmark_qwen_query_instruction.py` confronta **sulla stessa collection V4** query normale e query formattata secondo Qwen (`Instruct: ...\\nQuery:...`), usando `OllamaEmbedding` e `collection.query` senza generazione LLM. Misura recall dei prefissi gold, primo gold, MRR diagnostico e tempi; restituisce JSON su stdout. Non modifica collection o file, non installa nulla. Gold derivati da test storici e ancora **provvisori**. Prima dell'esecuzione verificare che il runtime corrisponda all'inventario e che non ci siano attività concorrenti onerose sulla VPS CPU-only. Il benchmark non testa il reranker né la qualità finale delle risposte; se la query istruita peggiora, non attivarla automaticamente.
