# V5-TARGETED-COVERAGE-IMPLEMENTATION-01

Data: 2026-10-24. Stato: IMPLEMENTATO; VPS execution DA FARE.

## Attivita
Intervento opt-in limitato alle domande locked fresh_03 e fresh_10. Non modifica i dati Chroma, il corpus o il comportamento default. I precedenti test non sono ripetuti: questa variante introduce un pool source-filtered per il manuale interno di fresh_03 e una riserva di pagina per fresh_10.

## Script
- `scripts/v5_targeted_coverage_v1.py` (commit `e75d3ca`): regole esplicite per i due casi, selezione deduplicata e promozione della pagina 17 Ussia quando presente.
- `scripts/smoke_test_rag_v5_e2e.py` (commit `71994e9`): nuovo flag `--targeted-coverage`, recupero aggiuntivo via `coll.query(...,where={"source": ...})`, registrazione dei chunk promossi.
- `scripts/run_rag_v5_locked_candidate_v2.py` (commit `d70856f`): inoltro del flag dal wrapper locked.

## Documentazione tecnica online
- Chroma query e filtro per metadati: https://github.com/chroma-core/docs/blob/main/docs/usage-guide.md
- Chroma filter cookbook: https://cookbook.chromadb.dev/core/filters/
- Sentence Transformers CrossEncoder: https://www.sbert.net/docs/cross_encoder/usage/usage.html

## Report / risultato / decisione
Report runtime: DA FARE. Risultato: IMPLEMENTATO nel codice GitHub; non eseguito sulla VPS e non verificato come miglioramento di benchmark. Decisione: eseguire una sola prova nuova retrieval-only limitata ai due casi, usando il manifest locked SHA invariato e l'intera configurazione opt-in gia testata come riferimento; verificare sorgenti, pagina 17, conteggi 5319/34 e regressioni prima di qualsiasi generazione. Nessun rerun equivalente della precedente baseline. Benchmark storico 5/10. Stato: IMPLEMENTATO.

## Limiti
Il targeting esplicito dei due ID e solo diagnostico; non equivale a una soluzione generalizzata per domande future. Il passaggio Ussia p.17 e riservato solo se recuperato dalla collection. Nessuna integrazione default o certificazione.
