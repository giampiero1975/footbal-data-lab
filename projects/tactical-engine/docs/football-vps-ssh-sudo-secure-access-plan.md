# FOOTBALL-DATA-LAB — Piano accesso SSH persistente e sudo sicuro

Attività: `RD-FOOTBALL-VPS-SSH-SUDO-SECURE-ACCESS-PLAN-01`  
Data: 2026-11-07  
Perimetro: analisi, verifiche read-only e progettazione documentale.

## Stato attuale verificato

- alias Windows: `football-vps` → `football@163.5.26.155:22`;
- `IdentitiesOnly=yes`, identità `~/.ssh/codex-football-vps`;
- Windows OpenSSH 9.5.4.1 disponibile;
- servizio Windows `ssh-agent` fermo e disabilitato; `ssh-add -l` non può
  collegarsi all'agent;
- chiave pubblica dedicata presente; nessuna chiave privata letta o stampata;
- autenticazione non interattiva tramite alias riuscita;
- VPS: utente `football`, UID 1000, host `football-data-lab.localdomain`;
- `/usr/bin/sudo` presente, versione 1.9.15p5;
- `authorized_keys` è un file regolare con due entry non commentate; contenuto
  non acquisito;
- `sudo -n -l` richiede password o non è autorizzato;
- nessuna configurazione, chiave, servizio, gruppo o privilegio modificato.

Il precedente export dei log del 7 novembre è concluso e non va ripetuto.

## Requisiti

1. Nessuna password/passphrase in repository, `.gitignore`, skill, prompt,
   report, log, script, variabili permanenti, history o argomenti processo.
2. Chiave privata cifrata e protetta da ACL dell'account Windows.
3. Sblocco mediante prompt protetto e caching soltanto nell'agent.
4. SSH vincolato ad alias e chiave dedicata.
5. Sudo non interattivo soltanto per un helper root-owned, senza shell o
   percorsi arbitrari.
6. Revoca indipendente di chiave e privilegio sudo.

## Alternative Windows

| Alternativa | Compatibilità | Persistenza/interazione | Valutazione |
|---|---|---|---|
| Ed25519 cifrata + Windows OpenSSH Agent | nativa con `ssh.exe`; Codex può usarla nel medesimo contesto utente | passphrase al caricamento; capacità temporanea nell'agent | **raccomandata** |
| Windows Credential Manager | nessuna integrazione diretta con OpenSSH o sudo | richiede wrapper che recupera il segreto | non raccomandata |
| DPAPI/SecretManagement | cifratura disponibile, ma nessuna integrazione diretta | richiede codice che rende il segreto al processo | non conforme all'obiettivo |

Credential Manager non risolve l'autenticazione sudo e non deve essere usato
per consegnare una password a Codex.

## Architettura SSH raccomandata

Riutilizzare la chiave dedicata esistente soltanto dopo verifica autorizzata di
tipo Ed25519, cifratura e ACL. In caso contrario creare una nuova chiave senza
sovrascrivere quella corrente.

```sshconfig
Host football-vps
    HostName 163.5.26.155
    User football
    Port 22
    IdentityFile ~/.ssh/codex-football-vps
    IdentitiesOnly yes
```

L'agent conserva una capacità temporanea, non la passphrase. Dopo riavvio o
`ssh-add -D` deve essere necessario un nuovo sblocco.

## Procedura Windows proposta — non eseguita

### Preflight e backup

```powershell
ssh -V
Get-Service ssh-agent
ssh -G football-vps
Get-Acl "$HOME\.ssh\codex-football-vps"
Copy-Item "$HOME\.ssh\config" "$HOME\.ssh\config.backup-<timestamp>"
```

PASS: identità esatta, nessun reparse point e ACL ristrette. FAIL: divergenza o
ACL eccessive. Rollback: ripristinare soltanto il backup verificato.

### Nuova chiave, solo se necessaria

```powershell
ssh-keygen -t ed25519 -a 100 -f "$HOME\.ssh\codex-football-vps-next" -C "football-vps-codex"
```

La passphrase va inserita nel prompt, mai come argomento. Arresto se il target
esiste. La chiave corrente non viene rimossa prima della verifica della nuova.

### Agent

Da PowerShell elevata, previa nuova autorizzazione:

```powershell
Set-Service ssh-agent -StartupType Automatic
Start-Service ssh-agent
```

Da sessione utente:

```powershell
ssh-add "$HOME\.ssh\codex-football-vps"
ssh-add -l
ssh football-vps
```

PASS: sola fingerprint prevista e accesso senza password account. Rollback:
`ssh-add -D`, arresto agent e ripristino dello StartType precedente.

### Installazione chiave pubblica

Usare una sessione autenticata normalmente, `umask 077`, controllo duplicati e
aggiornamento atomico di `authorized_keys`. Mantenere aperta una sessione di
recupero finché un secondo collegamento non riesce. Non disabilitare ancora
l'autenticazione password.

## Soluzione sudo raccomandata

Preferire un helper `/usr/local/sbin/football-rag-journal-export`:

- `root:root`, non modificabile da `football` né tramite directory antenate;
- nessun `eval`, shell o comando scelto dall'utente;
- allowlist di unità e intervalli, oppure nessun argomento per un caso fisso;
- percorsi assoluti; `SYSTEMD_PAGER=cat`, `PAGER=cat`, `--no-pager`;
- output solo su stdout, nessun file privilegiato scelto dall'utente;
- limiti temporali/dimensionali e codici d'uscita documentati;
- nessuna lettura di file arbitrari.

Regola proposta, da verificare con `visudo`:

```sudoers
Cmnd_Alias FOOTBALL_RAG_DIAG = /usr/local/sbin/football-rag-journal-export
football ALL=(root) NOPASSWD: FOOTBALL_RAG_DIAG
Defaults!FOOTBALL_RAG_DIAG !set_home, !authenticate, use_pty
```

Se l'helper accetta argomenti, le sole forme ammesse devono essere finite e
validate. Mai `NOPASSWD: ALL`.

### Perché non autorizzare direttamente `journalctl`

Wildcard, argomenti aggiuntivi, selezione di unità/intervalli e pager possono
ampliare i log leggibili. Una regola diretta è accettabile solo se il match
esatto degli argomenti e tutti i test negativi sono dimostrati; l'helper resta
più verificabile e revocabile.

## Piano di applicazione futuro

| Fase | Privilegio/modifica | PASS/FAIL e rollback |
|---|---|---|
| 1. Preflight/backup | lettura; backup ACL/sudoers root-only | PASS identità e hash; rollback dei soli backup verificati |
| 2. Chiave | utente; nuovi file dedicati | PASS cifratura/ACL; rimuovere solo i nuovi file se non installati |
| 3. Chiave pubblica | utente VPS; `authorized_keys` atomico | PASS secondo login; ripristino backup con sessione aperta |
| 4. Agent | amministratore Windows per servizio | PASS fingerprint attesa; `ssh-add -D` e StartType precedente |
| 5. Helper | root; nuovo eseguibile | PASS ownership, path e review; rimuovere solo helper identificato |
| 6. Sudoers | root; file dedicato `0440` | `visudo -cf` PASS; rimuovere solo la regola e rivalidare |
| 7. Test | comando positivo e negativi | extra args/unità/path/shell devono fallire |
| 8. Minimo privilegio | `sudo -n -l` | deve mostrare soltanto l'helper |

Non usare `sshpass`, `sudo -S`, script expect, password in `cmdkey`, `.env`,
clipboard automatizzate o file temporanei non protetti.

## Test di accettazione

- alias risolve esattamente host, utente, porta, chiave e `IdentitiesOnly`;
- agent espone soltanto la fingerprint dedicata;
- nessuna password account è richiesta dopo lo sblocco dell'agent;
- dopo revoca dall'agent l'accesso non usa silenziosamente altre identità;
- il solo helper sudo approvato riesce;
- argomenti extra, altre unità, altri intervalli, file e comandi falliscono;
- nessun segreto compare in process list, history, log, report o Git.

## Revoca, rotazione e rollback

- revoca SSH: rimuovere atomicamente la sola chiave pubblica identificata;
- rotazione: verificare la nuova chiave prima di revocare la precedente;
- agent: `ssh-add -d <key>` o `ssh-add -D` e chiusura sessioni;
- password account: ruotarla in terminale protetto perché precedentemente
  esposta, senza inserirla in Codex o report;
- sudo: rimuovere il solo file in `/etc/sudoers.d`, validare `visudo -c`, poi
  rimuovere l'helper;
- errore: usare sessione di recupero o console provider, senza allentare sshd o
  sudo globalmente.

## Decisioni ancora richieste

1. Abilitazione e StartType dell'agent Windows.
2. Riutilizzo o rotazione della chiave dopo verifica di tipo/cifratura/ACL.
3. Installazione/revoca della sola chiave pubblica.
4. Codice e percorso definitivi dell'helper root-owned.
5. Regola sudoers esatta e relativi test/rollback.
6. Rotazione sicura della password precedentemente esposta.

## Stato

- analisi e progettazione: **ESEGUITO**;
- accesso SSH tramite alias/chiave osservato: **VALIDATO** nel solo controllo;
- agent persistente, helper e sudoers: **DA FARE**;
- accesso amministrativo persistente: **BLOCCATO** fino ad approvazione e
  applicazione controllata;
- nessun segreto memorizzato o esposto nel presente lavoro.
