# FOOTBALL-DATA-LAB — accesso SSH v3 dal nuovo PC

Attività: `RD-FOOTBALL-VPS-SSH-V3-NEW-PC-ACCESS-01`.
Data: 2026-11-10, Europe/Rome.

## Attività → Script → Commit → Report

Ripristino autorizzato dell'accesso SSH Codex, senza revoca delle identità
precedenti, runtime, staging o modifiche ai servizi. TODO, Experiment Register,
report preparazione nuovo PC e rotazione v2 riconciliati prima delle operazioni.
Repository iniziale pulito, branch `codex/tactical-state-contract-v1`, HEAD
locale/GitHub `103fd8fb1de3d7712462ccb2e00e1cc63b1b4ae1`.

Script/comandi: OpenSSH nativo, inventario locale e metadati cifratura/ACL;
blocco Python stdlib eseguito personalmente dal titolare nella sessione VPS
autenticata con password; unico test Codex SSH read-only. Nessuno script
applicativo eseguito. Commit esclusivamente documentale, identificabile con
`git log -1 -- docs/football-vps-ssh-v3-new-pc-access-01.md` dalla directory
Tactical Engine. Report: questo documento; TODO e registro aggiornati insieme.

## Identità e protezione locale

- Privata: `C:\Users\giamp\.ssh\codex-football-vps-ed25519-v3`.
- Pubblica: stesso percorso con suffisso `.pub`.
- Tipo: Ed25519 256 bit; commento `football-vps-codex-v3`.
- Fingerprint pubblica:
  `SHA256:fpb/vDKCpmsoJD04J7KU3hCvlQqNL389hBp61Umj8iM`.
- Generazione interattiva richiesta con `ssh-keygen -t ed25519 -a 100`.
- Verifica successiva dei soli metadati: `cipher=none`, `kdf=none`.
  Il titolare ha scelto esplicitamente di mantenere la chiave senza passphrase
  e successivamente ha chiesto di proseguire. Il requisito iniziale di
  passphrase obbligatoria è quindi superato da tale scelta; non si dichiara
  cifratura o protezione bcrypt/100 effettiva per questa privata.
- ACL privata osservate: proprietario `LAPTOP-G59AI4M3\giamp`, ereditarietà
  disabilitata, SYSTEM/Administrators FullControl, titolare Modify/Synchronize.
  File regolare, nessun reparse point segnalato.

Nessuna chiave privata, password o passphrase è inclusa nei documenti o inviata
alla VPS. Le identità locali precedenti non sono state modificate.

## Host key e gestione degli impedimenti

Destinazione autorizzata: `football@163.5.26.155:22`.
Host key Ed25519 attendibile già presente in `known_hosts`, confermata anche
dall'output pubblico del titolare:
`SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks`.

Il primo `ssh-keyscan` non ha restituito una chiave; il controllo manuale ha
mostrato `unsupported KEX method sntrup761x25519-sha512@openssh.com`.
Successiva verifica differenziale con `ssh`, KEX supportato
`curve25519-sha256`, host key `ssh-ed25519` e tutte le autenticazioni
disabilitate: corrispondenza rigorosa con `known_hosts:15` osservata.
Il rifiuto finale di autenticazione di quel controllo era atteso, non un test v3.
Nessuna chiave sconosciuta accettata e nessun aggiornamento di `known_hosts`.

Lo script PowerShell locale predisposto per l'installazione è stato bloccato
dalla policy sugli script non firmati prima dell'esecuzione. Nessuna policy
allentata. Il titolare ha invece aperto personalmente una sessione SSH con
password, host key rigorosa e autenticazione a chiave disabilitata; ha poi
eseguito il solo blocco di append fornito in chat. Non sono stati effettuati
tentativi automatici di installazione alternativi contro la VPS.

## Autorizzazione VPS

Il blocco di append ha verificato utente `football`, `.ssh` directory reale
mode `0700`, `authorized_keys` file regolare mode `0600`, proprietario corrente;
ha aperto il file con `O_APPEND|O_NOFOLLOW`, acquisito lock esclusivo e impedito
duplicati. Nessuna sostituzione del file. Verifica finale dei byte precedenti
come prefisso invariato del file risultante.

Esito fornito dal titolare:

```json
{
  "v3_occurrences": 1,
  "previous_bytes_preserved": true,
  "previous_sha256": "45df62899fb12a59a8ecebbb3170f4e2ad7c9c2e4b718d98b80317ca32202a56",
  "after_sha256": "07c6bb9c1259c24dce3ed6b7db25d3e9eace1e14fbe2fd1912cefbfaa509a78a"
}
```

La conservazione dei byte precedenti è evidenza dell'installazione manuale;
il test Codex successivo ha verificato direttamente hash finale e conteggio.
Nessuna revoca o alterazione delle vecchie entry, modifica di `sshd_config`,
riavvio o modifica di codice/servizi.

## Alias Windows

Creato esclusivamente il nuovo `C:\Users\giamp\.ssh\config` con modalità
CreateNew dopo verifica della sua assenza. Configurazione:

```sshconfig
Host football-vps
    HostName 163.5.26.155
    User football
    Port 22
    IdentityFile ~/.ssh/codex-football-vps-ed25519-v3
    IdentitiesOnly yes
    StrictHostKeyChecking yes
    UpdateHostKeys no
    HostKeyAlgorithms ssh-ed25519
    KexAlgorithms curve25519-sha256
```

`ssh -G football-vps` ha confermato selezione di identità, destinazione e
controlli host. Non sono state sovrascritte configurazioni esistenti.

## Unico test v3 read-only

Una sola connessione Codex con `BatchMode=yes`, `ConnectionAttempts=1`,
`IdentityAgent=none`, `PreferredAuthentications=publickey`, password e
keyboard-interactive disabilitate. Nessun retry. Comandi remoti limitati a
utente, SHA-256 di `authorized_keys` e conteggio della pubblica v3.

Evidenze osservate direttamente:

- exit SSH `0`;
- host Ed25519 corrispondente alla fingerprint attesa;
- chiave offerta e accettata: v3, fingerprint pubblica sopra indicata;
- `Authenticated ... using "publickey"`;
- utente remoto `football`;
- SHA-256 remoto `07c6bb9c1259c24dce3ed6b7db25d3e9eace1e14fbe2fd1912cefbfaa509a78a`;
- singola occorrenza della pubblica v3: `1`.

Evidenza locale priva di segreti, fuori dal repository:
`C:\Users\giamp\.codex\visualizations\2026\11\10\01a1c50c-905a-7f30-a5ad-89b57aa7b71d\ssh-v3-single-verification.json`.

## Backup — istruzioni, non eseguito

Conservare una copia della privata v3 su un volume o archivio cifrato separato
dal PC, insieme a `.pub`, blocco alias e host key verificata. Poiché la privata
attuale è senza passphrase, la cifratura del supporto/archivio è necessaria per
ottenere una copia cifrata. Conservare il segreto di sblocco separatamente.
Verificare l'identità della copia sul supporto protetto, senza esporla o provarla
contro la VPS. Non inserire la privata in Git, report o chat. Nessuna copia
privata o archivio di backup è stato creato da Codex. Backup **DA FARE**.

## Risultato → Decisione → Stato

Autorizzazione pubblica e configurazione alias **ESEGUITO**. Accesso SSH v3
**VALIDATO** dal singolo test autorizzato. Vecchie chiavi preservate; nessuna
ulteriore connessione necessaria per questo closeout. Decisione: STOP operativo
dopo la verifica, con sola registrazione documentale dell'esito.

Nessun test RAG, inferenza Qwen, staging, wrapper remoto, panel, merge o deploy.
Ripristinare SSH non autorizza tali attività: problema generativo RAG V5,
contraddizioni, Gate, integrazione e certificazione restano **BLOCCATO**.
