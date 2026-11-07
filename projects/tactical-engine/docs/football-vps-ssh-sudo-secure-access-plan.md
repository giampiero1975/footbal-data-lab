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

### Verifica autorizzabile della chiave esistente — non eseguita

La verifica deve operare soltanto sui metadati e sulle funzioni native di
OpenSSH, senza stampare, copiare o esportare la chiave privata:

1. accertare che chiave, `.ssh` e configurazione siano file/directory attesi e
   non reparse point;
2. verificare proprietario, ACL esplicite ed ereditate e assenza di accessi in
   scrittura per altri utenti o gruppi non necessari;
3. ottenere la fingerprint e il tipo con strumenti OpenSSH senza riportare il
   materiale privato nel report;
4. dimostrare che il tipo sia Ed25519;
5. verificare la protezione con passphrase esclusivamente tramite caricamento
   interattivo nell'agent: nessuna passphrase in argomenti, pipe o log;
6. confrontare la fingerprint con la sola chiave pubblica autorizzata;
7. provare la compatibilità con Windows OpenSSH Agent nel reale contesto utente
   di Codex.

PASS: Ed25519, passphrase richiesta al primo caricamento, fingerprint attesa,
owner corretto, nessun reparse point, ACL minime su file e directory e agent
compatibile. FAIL: tipo diverso, chiave non cifrata, owner/ACL eccessivi,
reparse point, fingerprint inattesa o agent incompatibile. In caso di FAIL si
crea una nuova coppia dedicata con nome distinto; la corrente non viene
sovrascritta o revocata prima del secondo accesso riuscito.

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

### Metodo di autenticazione e fallback

`IdentitiesOnly yes` limita le identità pubbliche offerte dal client, ma **non
disabilita** il fallback all'autenticazione password. I controlli devono
distinguere:

- chiave caricata nell'agent;
- chiave privata disponibile sul disco e utilizzata direttamente da OpenSSH;
- autenticazione effettiva `publickey`;
- fallback `password` eventualmente ancora disponibile.

La verifica autorizzata dovrà usare diagnostica client controllata e redatta
per confermare il metodo negoziato, senza pubblicare percorsi sensibili o dati
di chiave. Un test separato con agent vuoto dovrà stabilire se OpenSSH usa la
chiave cifrata su disco e richiede la passphrase, oppure passa alla password.
Il test deve arrestarsi prima di inserire la password quando l'obiettivo è
provare il solo percorso a chiave. L'autenticazione password e una sessione di
recupero restano disponibili finché la nuova chiave non è stata verificata.

### Installazione chiave pubblica

Usare una sessione autenticata normalmente, `umask 077`, controllo duplicati e
aggiornamento atomico di `authorized_keys`. Mantenere aperta una sessione di
recupero finché un secondo collegamento non riesce. Non disabilitare ancora
l'autenticazione password.

## Soluzione sudo raccomandata

Preferire un helper `/usr/local/sbin/football-rag-journal-export`:

- `root:root`, non modificabile da `football` né tramite directory antenate;
- nessun `eval`, shell o comando scelto dall'utente;
- nessun argomento nella prima implementazione, dedicata al caso storico;
- percorsi assoluti; `SYSTEMD_PAGER=cat`, `PAGER=cat`, `--no-pager`;
- output solo su stdout, nessun file privilegiato scelto dall'utente;
- limiti temporali/dimensionali e codici d'uscita documentati;
- nessuna lettura di file arbitrari.

Regola proposta, da verificare con `visudo`:

```sudoers
Cmnd_Alias FOOTBALL_RAG_DIAG = /usr/local/sbin/football-rag-journal-export ""
football ALL=(root) NOPASSWD: FOOTBALL_RAG_DIAG
Defaults!FOOTBALL_RAG_DIAG use_pty
```

`""` vincola l'assenza di argomenti. La regola non autorizza altri comandi, il
percorso deve essere esatto e `NOPASSWD: ALL` è vietato. La forma definitiva
deve superare `visudo`; vanno inoltre inventariati gli eventuali privilegi sudo
già esistenti. La sola regola non garantisce il confinamento: esso dipende anche
dall'implementazione e dall'integrità dell'helper e delle sue dipendenze.

### Contratto di sicurezza dell'helper senza argomenti

**Perimetro fisso:** legge esclusivamente `ollama.service` e i messaggi kernel
pertinenti nella finestra `2026-11-07 12:19:00–12:25:30 Europe/Rome`. Eventuali
conversioni UTC sono interne, deterministiche e testate. Nessun'altra unità,
boot o finestra è selezionabile.

**Esecuzione:** rifiuta ogni argomento; non usa `eval`, shell arbitraria, input
utente, comandi o percorsi variabili. Usa eseguibili assoluti verificati, ambiente
minimo prefissato e `PATH` non controllabile da `football`. Non carica profili,
configurazioni o plugin modificabili dall'utente. Nessuna dipendenza eseguibile
o directory antenata può essere scrivibile da utenti non privilegiati.

**Pager e interazione:** imposta pager non interattivo e usa `--no-pager`; non
invoca editor, shell o programmi esterni selezionabili; stdin non viene letto.

**Output:** soltanto stdout/stderr; nessuna destinazione e nessuna redirezione
privilegiata sono selezionabili. L'helper applica limiti espliciti di tempo e
dimensione, restituisce codici distinti per completo, troncato, incompleto ed
errore, e non qualifica mai output troncato/incompleto come acquisizione
completa. Il report successivo deve minimizzare o redigere dati sensibili; gli
export grezzi restano protetti e fuori da Git.

**Temporanei:** preferibilmente nessuno. Se indispensabili, solo directory
root-owned non condivisa, `umask 077`, creazione atomica con primitive anti-
symlink, file regolari, cleanup su ogni uscita e nessun segreto persistente.

**Integrità:** helper file regolare, non symlink, `root:root`, non scrivibile da
`football`; ogni directory antenata deve essere root-owned e non scrivibile da
utenti non privilegiati. Le dipendenze e configurazioni devono rispettare gli
stessi vincoli. Prima dell'uso si verificano percorso risolto, owner, gruppo,
mode, ACL, mount e assenza di sostituibilità.

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

## Matrice dei test di accettazione — solo progettata

Nessun risultato simulato costituisce evidenza di validazione.

| ID | Requisito/scenario | Risultato atteso e PASS/FAIL | Rollback |
|---|---|---|---|
| T01 | SSH con chiave autorizzata | `publickey` dimostrato; FAIL se password o identità diversa | mantenere sessione di recupero |
| T02 | Agent privo della chiave | nessun uso silenzioso di altra identità; richiesta passphrase su disco o arresto | ricaricare chiave approvata |
| T03 | Metodo effettivo | diagnostica redatta conferma `publickey`; FAIL se ambiguo | nessuna modifica |
| T04 | Chiave non cifrata/ACL errate | riuso rifiutato e nuova coppia richiesta | non toccare chiave corrente |
| T05 | Helper senza argomenti | solo export fisso, exit completo | rimuovere regola/helper se anomalo |
| T06 | Argomenti aggiuntivi | sudo rifiuta prima dell'esecuzione | correggere regola, `visudo` |
| T07 | Altra unità | non rappresentabile/rifiutata | nessuna modifica |
| T08 | Altro intervallo | non rappresentabile/rifiutato | nessuna modifica |
| T09 | File arbitrario | nessun parametro percorso; rifiuto | nessuna modifica |
| T10 | Ambiente manipolato | ambiente fisso; output invariato o fail-closed | revocare regola |
| T11 | Pager richiesto | nessun pager/interazione | revocare regola |
| T12 | Helper/dipendenza symlink | preflight rifiuta | reinstallare atomicamente |
| T13 | Sostituzione eseguibile | scrittura negata a `football` | ripristinare artefatto verificato |
| T14 | Antenata scrivibile | preflight BLOCCATO | correggere ownership solo con autorizzazione |
| T15 | Output/redirezione arbitraria | helper non scrive; sudo non amplia privilegi della shell chiamante | nessuna modifica |
| T16 | Comando esterno arbitrario | impossibile per input/ambiente; rifiuto | revocare helper |
| T17 | Output eccessivo/incompleto | limite, exit specifico, mai promosso completo | nessuna promozione |
| T18 | Altro comando sudo | `sudo -n` rifiuta; inventario non mostra privilegi inattesi | revocare regola |
| T19 | Revoca chiave SSH | fingerprint rimossa, nuove sessioni negate, recupero preservato | reinstallare solo chiave verificata |
| T20 | Revoca sudoers | helper non eseguibile via sudo; `visudo -c` PASS | ripristinare solo file verificato |

### Controlli ACL, symlink e percorsi

Su Windows verificare owner, ACL esplicite/ereditate, altri utenti, attributi e
reparse point di chiave privata, `.ssh` e `config`. Sulla VPS verificare con
strumenti non dereferenzianti helper, ogni antenata, owner/gruppo/mode/ACL,
filesystem/mount, configurazioni e tutti gli eseguibili assoluti. PASS soltanto
se nessun componente è sostituibile o configurabile da `football`; ogni
ambiguità è FAIL e mantiene l'accesso amministrativo **BLOCCATO**.

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

Miglioramenti facoltativi, separati dalle correzioni obbligatorie: durata
limitata nell'agent con `ssh-add -t`; helper storico separato dalla futura
amministrazione ordinaria; audit periodico di `sudo -l`; verifica della reale
compatibilità Codex/agent nel contesto utente effettivo.

## Remediation revisione indipendente — C1/C5

| Correzione | Problema e modifica documentale | Evidenza futura richiesta | Stato |
|---|---|---|---|
| C1 | regola consentiva argomenti; aggiunto `""`, rimosse opzioni ridondanti e richiesto inventario sudo | `visudo`, test T06/T18 | **ESEGUITO** documentale |
| C2 | contratto helper generico; definito helper storico senza argomenti, ambiente/output/limiti/integrità | review codice e test T05–T17 | **ESEGUITO** documentale |
| C3 | proprietà chiave non dimostrate; aggiunti controlli tipo/cifratura/ACL/agent | verifica separata senza lettura della chiave | **ESEGUITO** documentale; verifica **DA FARE** |
| C4 | metodo e fallback non distinti; esplicitato che `IdentitiesOnly` non disabilita password | test T01–T03 | **ESEGUITO** documentale |
| C5 | controlli path incompleti; estesi a owner, ACL, reparse/symlink, antenate e dipendenze | test T04/T12–T14 | **ESEGUITO** documentale |

## Stato

- analisi e progettazione: **ESEGUITO**;
- accesso SSH tramite alias/chiave osservato: **VALIDATO** nel solo controllo;
- remediation documentale C1–C5: **ESEGUITO**;
- verifica cifratura/ACL chiave, agent persistente, helper e sudoers: **DA FARE**;
- accesso amministrativo persistente: **BLOCCATO** fino ad approvazione e
  applicazione controllata;
- nessun segreto memorizzato o esposto nel presente lavoro.
