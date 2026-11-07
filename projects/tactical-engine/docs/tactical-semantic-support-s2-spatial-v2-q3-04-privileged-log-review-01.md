# RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-PRIVILEGED-LOG-REVIEW-01

## Baseline e riconciliazione

Tentativo autorizzato di lettura privilegiata read-only dei log storici del
singolo run Spatial V2 `q3_04`.

- HEAD documentale iniziale:
  `1e47f3aa8334eca4b90a0a2d30ccdc48600045e8`;
- baseline runtime congelata:
  `009f76e71c0351da9d2b797ad3c9ff1928671a4e`;
- nessuna revisione privilegiata equivalente già registrata;
- staging e artefatti originali non modificati.

TODO, experiment register e report forense precedente sono stati riconciliati.
Non sono state eseguite inferenze, query generative, modifiche o test.

## Modalità di accesso e fuso orario

Accesso SSH tramite alias `football-vps`, utente ordinario `football`.
Il server ha riportato:

- `Timezone=Europe/Rome`;
- offset corrente `+01:00`;
- `LocalRTC=no`;
- `NTPSynchronized=yes`.

La finestra interrogata è stata quindi mantenuta esattamente in ora locale CET:
`2026-11-07 12:19:00`–`12:25:30`.

## Disponibilità dei log

La query ordinaria di `ollama.service` ha restituito zero righe perché l'utente
non può vedere i messaggi degli altri utenti del journal.

È stato quindi tentato direttamente il solo comando privilegiato read-only
autorizzato, mediante `sudo -n journalctl`. Esito:

- exit code `1`;
- messaggio: `sudo: a password is required`;
- nessuna entry privilegiata acquisita.

Anche `sudo -n journalctl --list-boots` richiede password. Non è stato richiesto
o inserito alcun segreto e non sono state tentate escalation alternative.

La configurazione systemd leggibile ordinariamente conferma:

- `ExecStart=/usr/local/bin/ollama serve`;
- `User=ollama`, `Group=ollama`;
- `StandardOutput=journal`;
- `StandardError=inherit`;
- nessuna `LogsDirectory` dichiarata.

Non esiste quindi, nelle evidenze autorizzate, un file log alternativo indicato
dalla unità. La query kernel ordinaria nella stessa finestra non ha restituito
eventi pertinenti; quella privilegiata non è stata eseguibile senza password.

## Timeline ed eventi significativi

Nessun nuovo evento server o kernel è stato acquisito. Resta valida la timeline
client già verificata:

| Timestamp CET | Componente | Evento | Correlazione |
|---|---|---|---|
| 12:20:38 | wrapper client | richiesta unica avviata | alta, artefatti content-addressed |
| durante il run | `/api/ps` | modello osservato caricato | temporale, senza request ID |
| 12:23:38 | wrapper client | timeout e envelope `not_evaluable` | alta |
| 12:24:25 | artefatti | inventario SHA-256 finale | alta |

Non è possibile aggiungere timestamp di ricezione server, caricamento,
generazione, token, completamento o cancellazione.

## Matrice causale aggiornata

L'assenza di nuove evidenze impedisce modifiche sostanziali alla matrice:

| Possibile causa | Qualificazione | Evidenza/limite |
|---|---|---|
| Timeout client | **Dimostrata** | artefatti e codice già verificati |
| Caricamento iniziale modello | **Compatibile** | modello assente prima e presente durante; log inaccessibili |
| Lentezza della generazione | **Compatibile** | nessuna risposta entro 180 s; metriche assenti |
| Complessità structured output | **Compatibile** | dimensioni note, causalità non provata |
| Saturazione risorse | **Non supportata** | log kernel privilegiati e telemetria durante il run assenti |
| Concorrenza | **Non supportata** | nessun concorrente nello snapshot, nessuna correlazione journal |
| Errore o blocco server | **Non supportata** | journal Ollama non acquisibile |
| Completamento server dopo timeout | **Non supportata** | nessuna entry server accessibile |
| Malfunzionamento fail-closed wrapper | **Esclusa** nel percorso osservato | envelope coerente e non-promozione |

## Decisione e limiti

Alla domanda «perché non abbiamo ricevuto una risposta entro 180 secondi?» la
sola risposta dimostrata resta: il client non ha ricevuto una risposta completa
entro il timeout contrattuale. Non è possibile attribuire il ritardo a
caricamento, generazione, risorse o errore server perché i log completi non sono
accessibili con privilegi non interattivi già disponibili.

L'attività è **BLOCCATO** per indisponibilità di `sudo -n` sui comandi journal.
Il fail-closed già osservato resta **VALIDATO**; la semantica non è valutabile.

Unico prossimo passo raccomandato, non eseguito: il titolare può fornire
direttamente un export read-only, limitato e redatto dei log
`ollama.service`/kernel della finestra autorizzata, generato da un amministratore
senza cambiare gruppi, sudoers o configurazioni. Non richiede una nuova
inferenza.

| Componente | Stato |
|---|---|
| Revisione privilegiata log | **BLOCCATO** |
| Fail-closed del singolo tentativo | **VALIDATO** |
| Diagnosi semantica `q3_04` | **BLOCCATO** |
| Accuratezza, Gate, integrazione, certificazione | **BLOCCATO** |

