# RAG V5 runtime maintenance 01

Data: 2026-10-25. Stato: IMPLEMENTATO; collaudo VPS DA FARE.

## Perimetro

Manutenzione settimanale fail-closed del servizio applicativo. La cancellazione è limitata ai file `<job-id>.request.json` e `<job-id>.result.json` sotto `evaluation/api-runs`: età minima 30 giorni e almeno i 100 job più recenti sempre preservati. Metriche, report di benchmark, corpus, Chroma, modelli e sorgenti non corrispondono al pattern e non possono entrare nel piano.

## Controlli

- health, readiness autenticata e metriche;
- worker/coda tramite API;
- collection e conteggio atteso;
- spazio disco con soglia critica 90%;
- commit e pulizia tracked Git;
- report atomico privo di token, domande e risposte.

Lo script è dry-run per default; `--write` elimina solo se tutti i controlli sono privi di errori. Unit/timer utente: domenica 04:15 con jitter massimo 30 minuti, distinto dal monitor FIGC del sabato.

Attività: manutenzione runtime. Script: `maintain_rag_v5_runtime.py`; test `test_runtime_maintenance.py`; unit `football-rag-maintenance.user.*`. Commit: DA FARE. Risultato: IMPLEMENTATO. Decisione: suite VPS, dry-run, unica esecuzione reale e verifica timer prima dell'integrazione. Stato: IMPLEMENTATO.
