# RAG V5 runtime maintenance 01

Data: 2026-10-25. Stato: VALIDATO e INTEGRATO.

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

## Evidenza VPS

Suite combinata 12/12 PASS. Dry-run e prima esecuzione `--write`: health/readiness 200, worker vivo, coda 0/8, collection 6196/6196, Git tracked pulito, disco 30,77%, zero errori. Piano e rimozioni entrambi vuoti: nessun file cancellato. Unit `Result=success`, timer enabled/active; prossimo run domenica 1 novembre 2026 alle 04:31 CET.

Attività: manutenzione runtime. Script, test e unit sopra. Commit implementazione `5b877cb`. Risultato: VALIDATO. Decisione: integrare il timer settimanale; retention effettiva si attiverà soltanto quando coesistono più di 100 job e artefatti oltre 30 giorni, con tutti i check verdi. Stato: INTEGRATO.
