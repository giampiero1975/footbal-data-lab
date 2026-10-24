# V5-RUNTIME-SYMLINK-FIX-01

Data: 2026-10-24. Stato: IMPLEMENTATO.

Attivita: risolvere selezione erronea di /usr/bin/python3 pur avendo venv funzionante.
Script: `scripts/run_rag_v5_locked_candidate_v2.py`.
Commit: `6faa907`.
Report: log VPS ripetuto: `V5_RUNTIME /usr/bin/python3` e `ModuleNotFoundError: chromadb`; diagnostica operatore: `.venv/bin/python3` e symlink verso `/usr/bin/python3`, ma `projects/tactical-engine/.venv/bin/python -c 'import chromadb'` riuscito e caricato da site-packages del venv.
Risultato: identificato confronto scorretto basato su `Path.resolve()`, che confonde interprete venv con eseguibile sistema quando symlink puntano allo stesso binario. Fix usa `Path.absolute()` per preservare il percorso del virtualenv, necessario per `pyvenv.cfg` e i site-packages.
Decisione: nessuna installazione, riprendere soltanto la diagnostica mirata fresh_03/fresh_10 interrotta prima del retrieval. Nessun benchmark ripetuto o score aggiornato.
Stato: IMPLEMENTATO.
