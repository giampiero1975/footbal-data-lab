# V5-TARGETED-COVERAGE-RETRIEVAL-01

Data: 2026-10-24. Stato: ESEGUITO.

## Attività → Script → Commit
Verifica VPS retrieval-only, manifest locked SHA256 `c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71`, due domande fresh_03/fresh_10.
Script: `scripts/run_rag_v5_locked_candidate_v2.py`, `scripts/smoke_test_rag_v5_e2e.py`, `scripts/v5_targeted_coverage_v1.py`.
Commit codice: `e75d3ca`, `71994e9`, `b4d1ebf`, runtime fix `6faa907`.

## Report → Risultato
Evidenza VPS fornita dall'operatore: `evaluation/v5_targeted_coverage_retrieval_v1.json`; console `COMPLETE 2/2; V5 unchanged=True`, `V5 COMPLETE: 2/2; retrieval_only=True; no certification`.
- fresh_03: manuale `FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale` recuperato e promosso in F8, pagina 5, testo sul ripiegamento disordinato. Copertura nominale della fonte raggiunta, ma il passaggio non dimostra adeguata copertura dei moduli e dell'inferenza causale richiesta: non validare il caso come risolto.
- fresh_10: manuale interno pagina 3 F5, Ussia pagine 5-6 F7 e pagina 17 F8 (figura 6/A), promozione p17 documentata. Evidenze comparate disponibili; qualità della risposta non ancora verificata.
- Chroma principale 5319 prima/dopo, candidata 34 prima/dopo; `index_unchanged=true`.
- `citations=[]`, `answer=""` coerenti con `retrieval_only=true`; nessuna generazione, nessuna verifica di fedeltà.
- Durata riportata: fresh_03 3.8 s; fresh_10 4.12 s.

## Decisione → Stato
Stato ESEGUITO della sola diagnostica retrieval. Conservare baseline locked 5/10. Non integrare nella pipeline default, non certificare. Prima di una generazione mirata, migliorare pertinenza del chunk fresh_03 con recupero e ranking motivati; per fresh_10 passare a controllo di generazione solo con differenza tecnica esplicita, mantenendo fonti e pagine. Nessun nuovo corpus o indicizzazione.
