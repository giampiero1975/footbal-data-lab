# RAG V5 — Piano source-aware retrieval shadow (2026-10-23)

## Evidenza
La revisione diagnostica candidate v2 registra errori di attribuzione tra autori (Foscarini/Indiani), recupero di esercitazioni omonime e selezione di indici invece di passaggi pertinenti. Il candidato v2 è già stato utilizzato: non va riutilizzato come holdout indipendente dopo tuning.

## Codice verificato
Lo script `scripts/smoke_test_rag_v5_e2e.py` interroga Chroma con `query_embeddings`, `n_results=24` e metadati/documenti/distanze, applica CrossEncoder mMARCO e seleziona fino a otto evidenze dopo deduplica. Non applica un filtro sull'autore. I campi osservati nel codice sono `source`, `source_relative`, `page_numbers` e `raw_text`. I valori effettivi e i tipi presenti nella collection devono ancora essere censiti.

## Sequenza proposta
1. Censire in sola lettura i valori distinti e le frequenze di `source`, la struttura di `page_numbers` e alcuni esempi di `source_relative` sulla collection V5.
2. Mappare gli autori e i documenti ai valori metadata realmente presenti, senza matching ambiguo o inventato.
3. Preparare uno script shadow separato che confronti retrieval globale e retrieval vincolato per sorgente, senza modificare collection o pipeline attuale.
4. Preservare ranking mMARCO, deduplica e provenienza; registrare esplicitamente i casi senza evidenza della sorgente richiesta.
5. Valutare su casi di sviluppo e regressione, non ottimizzare sul candidato v2. Misurare recall della fonte, correttezza dell'attribuzione, latenza e astensioni.
6. Soltanto dopo la validazione, proporre un eventuale nuovo holdout indipendente congelato prima dell'esecuzione.

## Fonti ufficiali da applicare
- Chroma query/get: https://docs.trychroma.com/docs/querying-collections/query-and-get
- Chroma metadata filtering: https://docs.trychroma.com/docs/querying-collections/metadata-filtering
- Sentence Transformers CrossEncoder: https://www.sbert.net/docs/cross_encoder/usage/usage.html
- Ollama Chat API: https://docs.ollama.com/api/chat

## Sicurezza e stato
Nessuna modifica a V4, V5, indici, manifest o report precedenti. Prima di usare `where` bisogna verificare che il campo e il valore di filtro esistano davvero nella collection.

**VERIFICATO:** struttura dello script GitHub e analisi diagnostica precedente. **DOCUMENTATO:** inventario dipendenze in `docs/environment.md`. **DA VERIFICARE:** metadata effettivi sulla VPS, prestazioni e regressioni del retrieval shadow. La progettazione non equivale a validazione runtime.
