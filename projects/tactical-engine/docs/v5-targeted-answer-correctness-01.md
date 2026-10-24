# V5-TARGETED-ANSWER-CORRECTNESS-01

Data: 2026-10-24. Stato: IMPLEMENTATO.

Attività: preparare verifica di correttezza delle risposte fresh_03 e fresh_10, con differenza tecnica documentata rispetto al retrieval-only già eseguito.
Script: `scripts/v5_targeted_coverage_v1.py`, wrapper locked con `--only-ids fresh_03 fresh_10` senza `--retrieval-only`.
Commit: `e0018bf`.
Report: `docs/v5-targeted-answer-correctness-01.md`; runtime di generazione DA FARE.
Risultato: per fresh_03 il passaggio riservato dal manuale viene scelto in base alla presenza dei moduli 4-3-3, 4-4-2, 3-5-2 e 3-4-2-1, non solo al punteggio CrossEncoder; fresh_10 mantiene la riserva Ussia pagina 17. Il recupero precedente era ESEGUITO ma non verificava la correttezza delle risposte.
Decisione: eseguire una sola generazione scoped opt-in, valutare manualmente ciascun mandatory_claim e forbidden_claim del manifest locked contro le evidenze citate; non equiparare citazioni sintattiche a fedeltà fattuale. Nessuna modifica Chroma, nessuna integrazione default o certificazione. Benchmark ufficiale 5/10 invariato.
Stato: IMPLEMENTATO.
