# V5-RUNTIME-IMPORT-FAILURE-01

Data: 2026-10-24. Stato: IMPLEMENTATO (fix), runtime DA FARE.

Attivita: diagnosi del blocco della prova retrieval-only fresh_03/fresh_10.
Script: `scripts/run_rag_v5_locked_candidate_v2.py`.
Commit: `779f4c3`.
Report: output console operatore: manifest LOCK_OK SHA c160a8a2..., `V5_RUNTIME /usr/bin/python3`, poi `ModuleNotFoundError: No module named 'chromadb'` durante import del runner.
Risultato: nessun retrieval o rerank eseguito; nessun JSON prodotto da questa esecuzione; non vi e evidenza di modifica Chroma.
Causa documentata: il controllo precedente `importlib.util.find_spec` verificava solo presenza di specifiche di moduli, non la reale importabilita delle dipendenze necessarie. L'interprete selezionato `/usr/bin/python3` non ha importato `chromadb`.
Decisione: controllo con import reali `chromadb`, `OllamaEmbedding`, `CrossEncoder` in ogni interprete candidato; mantenere il selettore degli ambienti virtuali esistenti senza installazioni. Riprovare una sola volta la diagnostica con differenza tecnica documentata. Nessun test duplicato completato. Benchmark storico 5/10 invariato.
Stato: IMPLEMENTATO.
