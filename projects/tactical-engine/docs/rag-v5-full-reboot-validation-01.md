# Validazione reboot completo RAG V5 — 2026-10-25

Stato: **VALIDATO**.

## Attività

Verificare che il deployment applicativo locale riparta dopo un reboot completo
della VPS, senza login o avvio manuale. Questa verifica è distinta dal precedente
restart della sola unità e dal test di recovery dopo `SIGKILL`.

## Preflight

- `football-rag-api.service` attiva, abilitata e configurata `Restart=on-failure`;
- user manager con `Linger=yes`;
- `/panel` HTTP 200;
- nessuna unità utente fallita;
- timer manutenzione RAG e discovery FIGC abilitati.

## Risultato

Reboot avviato il 2026-10-25 alle 12:42 CET. Nuovo boot registrato alle
12:42:05; `football-rag-api.service` avviata automaticamente alle 12:42:14.

Controlli post-boot:

- unità API `active/running`, `Result=success`, `NRestarts=0`;
- `/healthz` `ok` e `/readyz` `ready`;
- `/panel` HTTP 200;
- collection `dribbling_tactics_v5_multisource_drive11_figc5_candidate_v1`,
  6410 chunk e 157 documenti;
- timer `football-rag-maintenance.timer` e `football-figc-discovery.timer`
  entrambi attivi con prossime scadenze pianificate;
- zero unità utente fallite;
- disco root al 32%, 40 GB disponibili.

## Decisione

Avvio automatico post-reboot **VALIDATO**. Non ripetere senza modifiche a unità,
linger, boot o configurazione del servizio. L'osservazione prolungata resta una
attività distinta; questo controllo non amplia la certificazione locked.
