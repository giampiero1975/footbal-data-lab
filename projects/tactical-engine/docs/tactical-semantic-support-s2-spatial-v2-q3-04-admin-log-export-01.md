# RD-TSC-V2-D3-S2-Q3-04-ADMIN-LOG-EXPORT-01

## Baseline e riconciliazione

Tentativo di individuare un accesso amministrativo già configurato e autorizzato
per esportare read-only i log storici del run Spatial V2 `q3_04`.

- HEAD documentale iniziale:
  `49dac1fd9d3625665b16d63669e5229f0893c18d`;
- baseline runtime congelata:
  `009f76e71c0351da9d2b797ad3c9ff1928671a4e`;
- nessun export amministrativo equivalente già registrato.

TODO, experiment register e review privilegiata precedente sono stati
riconciliati. Non sono state ripetute query `sudo -n`, inferenze o letture
journal già concluse.

## Verifica dell'accesso disponibile

È stata risolta localmente, senza connessione, la sola configurazione dell'alias
SSH autorizzato `football-vps`:

- host `163.5.26.155`;
- porta 22;
- utente `football`;
- `IdentitiesOnly=yes`;
- identity file già approvato `codex-football-vps`.

La configurazione non espone un'identità amministrativa. La precedente attività
ha già verificato che l'utente `football` non dispone di `sudo -n journalctl`:
exit code 1 e password richiesta. L'incarico corrente vieta di ripetere quel
tentativo, cercare credenziali, modificare configurazioni o usare escalation
alternative.

Non esiste quindi un accesso amministrativo non interattivo già disponibile e
autorizzato nel contesto Codex. L'attività si è arrestata prima di qualsiasi
connessione amministrativa o interrogazione dei log.

## Export ed evidenze

- export Ollama: non prodotto;
- export kernel: non prodotto;
- directory di evidenza: non creata;
- SHA-256 export: non disponibili;
- eventi server nuovi: nessuno acquisito;
- staging, artefatti originali e VPS: invariati.

Non vengono dichiarati log recuperati o timeline server inesistenti. Resta
valida soltanto la timeline client già documentata e la causa dimostrata del
timeout lato client; caricamento, generazione, risorse ed errore server restano
non separabili con le evidenze disponibili.

## Decisione e stati

Attività **BLOCCATO**: manca un'identità amministrativa già configurata e
autorizzata, mentre l'unico alias disponibile usa l'account non privilegiato.

Unico prossimo passo raccomandato, non eseguito: un amministratore autorizzato
può produrre e consegnare al titolare due export redatti, limitati alla finestra
`2026-11-07 12:19:00–12:25:30 CET`, con comandi e SHA-256. Codex potrà poi
analizzarli offline senza credenziali amministrative e senza nuova inferenza.

| Componente | Stato |
|---|---|
| Recupero amministrativo log | **BLOCCATO** |
| Fail-closed del singolo tentativo | **VALIDATO** |
| Diagnosi semantica `q3_04` | **BLOCCATO** |
| Accuratezza, Gate, integrazione, certificazione | **BLOCCATO** |

