# V5-TARGETED-ANSWERS-REVIEW-01

Data: 2026-10-24. Stato: ESEGUITO.

Attività: revisione documentale delle risposte generate per fresh_03 e fresh_10, distinta dalla precedente diagnostica retrieval-only.
Script: `scripts/run_rag_v5_locked_candidate_v2.py`, `scripts/smoke_test_rag_v5_e2e.py`, helper `scripts/v5_targeted_coverage_v1.py`.
Commit codice: `0c89b47` (correzione sintassi precedente).
Report: output VPS fornito dall'operatore `evaluation/v5_targeted_answers_v1.json`; `COMPLETE 2/2`, `index_unchanged=true`.
Risultato:
- fresh_03: risposta 132.23 s, generazione 128.48 s, 467 token, 1791 token prompt; citazioni F3,F5,F7,F8 valide sintatticamente. Non soddisfa mandatory claim relativo alla descrizione esplicita di 4-3-3, 4-4-2, 3-5-2, 3-4-2-1 nel manuale; non afferma in modo netto l'assenza di prova causale del rischio del cambio di modulo. F8 manuale p5 tratta ripiegamento disordinato, non dimostra l'argomento richiesto. Decisione: NON VALIDATO (stato del test ESEGUITO).
- fresh_10: risposta 138.54 s, generazione 133.87 s, 469 token, 2243 token prompt; F5 manuale p3 e F8 Ussia p17 supportano i due mandatory claims. Digressione su evoluzione delle regole del fuorigioco F2/F3 non necessaria e temporalmente contestuale alla fonte storica; rischio di sovrageneralizzazione. La distinzione tra pressing generale e riaggressione non è esplicitata con sufficiente rigore. Decisione: revisione favorevole dei mandatory claims ma VALIDAZIONE complessiva sospesa in attesa di controllo indipendente; nessuna certificazione.
- Citazioni sintattiche valide, non prova automatica di fedeltà. Chroma 5319/34 invariati. Velocità stimata 467/128.48 = 3.63 e 469/133.87 = 3.50 token/s, includendo eventuali overhead nel tempo totale Ollama; non misurazione pura decode.
Decisione: non ripetere test equivalenti. Analizzare il contenuto del manuale sezione 9 pp4-5 per fresh_03 e delimitare rigorosamente pressing vs riaggressione in fresh_10 prima di una variante tecnica documentata. Baseline V5 locked 5/10 invariata, nessuna integrazione default.
Stato: ESEGUITO.
