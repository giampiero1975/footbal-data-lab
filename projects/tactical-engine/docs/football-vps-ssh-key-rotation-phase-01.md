# FOOTBALL-DATA-LAB — Rotazione controllata chiave SSH v2

Attività: `RD-FOOTBALL-VPS-SSH-KEY-ROTATION-PHASE-01`

Data: 2026-11-07

## Baseline e perimetro

- branch: `codex/tactical-state-contract-v1`;
- HEAD iniziale locale/remoto:
  `c6bd962667a70fd56ce1fdcf83e383ceb77251a7`;
- working tree iniziale pulito;
- nuova coppia già creata dal titolare:
  `~/.ssh/codex-football-vps-ed25519-v2`;
- nessuna nuova chiave generata da Codex;
- nessuna modifica a sudoers, sshd, servizi VPS o privilegi.

## Verifica nuova identità

| Controllo | Evidenza | Esito |
|---|---|---|
| File privato/pubblico | file regolari, nessun reparse point | PASS |
| Proprietario | account Windows del titolare | PASS |
| ACL privata | protetta; titolare, SYSTEM e Administrators | PASS |
| Tipo | Ed25519 256 bit dalla sola chiave pubblica | PASS |
| Fingerprint | corrisponde al valore autorizzato; riportata redatta | PASS |
| Passphrase | richiesta e inserita dal titolare in PowerShell visibile tramite prompt nativo OpenSSH | PASS |
| Contenuto privato | non letto, stampato, copiato o esportato | PASS |

## Windows OpenSSH Agent

Stato iniziale: `Stopped/Disabled`, nessuna identità. Dopo conferma UAC:

- servizio impostato `Running/Automatic`;
- caricata esclusivamente la chiave v2 tramite prompt protetto;
- agent finale con una sola identità;
- fingerprint caricata corrispondente a quella pubblica attesa;
- nessuna passphrase acquisita da Codex o registrata.

## Installazione della chiave pubblica VPS

Il collegamento preesistente è stato usato senza modificare inizialmente l'alias.
Preflight remoto:

- utente `football`;
- `~/.ssh/authorized_keys` file regolare, `football:football`, modalità `600`;
- percorsi temporaneo e backup assenti, inclusi symlink dangling.

È stata trasferita esclusivamente la chiave `.pub`. La fingerprint remota è
stata confrontata con quella autorizzata. Tutte le entry precedenti sono state
preservate e la nuova chiave è stata aggiunta atomicamente.

- backup protetto:
  `/home/football/.ssh/authorized_keys.backup-rd-ssh-key-rotation-20261107`;
- backup regolare, `football:football`, modalità `600`, 225 byte;
- `authorized_keys` finale regolare, modalità `600`;
- file pubblico temporaneo rimosso;
- nessuna chiave privata trasferita.

## Verifica differenziale

Una sola connessione differenziale è stata eseguita selezionando esplicitamente
la nuova identità, senza usare l'alias aggiornato e con:

- `IdentitiesOnly=yes`;
- `BatchMode=yes`;
- `PasswordAuthentication=no`;
- `KbdInteractiveAuthentication=no`;
- `PreferredAuthentications=publickey`.

Sono stati conservati soltanto indicatori redatti:

- exit code `0`;
- agent osservato con una sola chiave;
- fingerprint v2 offerta dall'agent;
- chiave accettata dal server;
- autenticazione effettiva `publickey`;
- nessun prompt password o fallback osservato;
- nessun comando amministrativo remoto.

## Alias e conservazione accesso precedente

Prima della modifica è stato creato e verificato il backup locale:

`~/.ssh/config.backup-rd-ssh-key-rotation-20261107`

È stata modificata esclusivamente la direttiva `IdentityFile` del blocco
`football-vps` in:

`~/.ssh/codex-football-vps-ed25519-v2`

`ssh -G` conferma host, utente, porta e `IdentitiesOnly=yes` invariati. Non è
stata ripetuta una seconda connessione, perché il test differenziale precedente
era conclusivo.

La vecchia chiave privata locale è preservata. La precedente chiave pubblica
rimane autorizzata sulla VPS come recupero; nessuna entry è stata revocata.

## Rollback disponibile

Non è stato necessario applicarlo. Gli elementi disponibili sono:

- backup locale della configurazione SSH;
- backup remoto protetto di `authorized_keys`;
- vecchia chiave privata locale invariata;
- precedente chiave pubblica ancora autorizzata;
- rimozione selettiva della sola identità v2 dall'agent, se futura decisione.

## Decisione e stati

La nuova identità cifrata, l'agent e l'autenticazione `publickey` senza fallback
sono dimostrati nel perimetro autorizzato.

- nuova chiave v2 e ACL: **VALIDATO**;
- caricamento protetto e Windows OpenSSH Agent: **VALIDATO**;
- installazione chiave pubblica: **ESEGUITO**;
- autenticazione differenziale via agent: **VALIDATO**;
- alias `football-vps` aggiornato: **ESEGUITO**;
- vecchio accesso di recupero: preservato;
- rotazione SSH Fase 1: **VALIDATO**;
- revoca vecchia chiave: **DA FARE** solo con autorizzazione separata;
- helper, sudoers e accesso amministrativo persistente: **BLOCCATO**.
