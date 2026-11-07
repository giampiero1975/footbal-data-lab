# FOOTBALL-DATA-LAB — Fase 1 verifica chiave SSH e OpenSSH Agent

Attività: `RD-FOOTBALL-VPS-SSH-AGENT-PHASE-01`

Data: 2026-11-07

## Baseline e perimetro

- branch: `codex/tactical-state-contract-v1`;
- HEAD iniziale locale/remoto:
  `c96f33f9a725932199cc1ff8fa97eca1cee1466b`;
- working tree iniziale pulito;
- piano, TODO ed experiment register letti e riconciliati;
- nessuna attività equivalente già conclusa;
- nessuna connessione VPS, modifica Windows, chiave, ACL, configurazione o
  servizio autorizzato è stata effettuata durante i controlli preliminari.

## Configurazione iniziale

| Elemento | Evidenza read-only | Esito |
|---|---|---|
| Client OpenSSH | `ssh`, `ssh-add`, `ssh-keygen` 9.5.4.1 in `System32\OpenSSH` | PASS |
| Contesto Codex | account Windows del titolare | PASS |
| Alias | `football@163.5.26.155:22` | PASS |
| Identità alias | `~/.ssh/codex-football-vps`, `IdentitiesOnly=yes` | PASS |
| Metodi configurati | `PubkeyAuthentication=true`, `PasswordAuthentication=yes` | informativo; `IdentitiesOnly` non disabilita il fallback password |
| Agent | servizio presente, `Stopped`, `Disabled` | prerequisito non ancora implementato |

## Verifica della chiave

I controlli hanno acquisito esclusivamente metadati filesystem e la fingerprint
della chiave **pubblica**. Il contenuto privato non è stato letto, copiato,
stampato o esportato.

| Proprietà | Risultato | Qualificazione |
|---|---|---|
| File privato presente e regolare | sì; attributo `Archive`, nessun `LinkType` | PASS |
| Proprietario file privato | account Windows del titolare | PASS |
| ACL file privato | ACL protette: titolare `Modify`, SYSTEM e Administrators `FullControl`; nessun altro principal | PASS nel perimetro osservato |
| Directory `.ssh` | directory ordinaria, owner titolare; ACL ereditate soltanto da SYSTEM, Administrators e titolare | PASS nel perimetro osservato |
| Config SSH | file ordinario, owner titolare; stessi principal ereditati | PASS nel perimetro osservato |
| Reparse point | nessuno rilevato su directory, chiave, `.pub` e config | PASS |
| Tipo | chiave pubblica 256 bit ED25519 | PASS |
| Fingerprint | fingerprint SHA-256 ottenuta dalla sola `.pub`; non riportata integralmente nel report | PASS come identità pubblica locale |
| Cifratura/passphrase privata | non verificata | **BLOCCATO** |
| Compatibilità agent | strumenti presenti, ma caricamento non eseguito | **BLOCCATO** |

## Arresto fail-closed

La verifica proposta della cifratura avrebbe richiesto a OpenSSH di aprire la
chiave privata. Il controllo di sicurezza dell'ambiente ha rifiutato questa
operazione, anche con output scartato, perché oltrepassa la sola ispezione di
metadati e chiave pubblica. Non è stato tentato alcun metodo alternativo.

Il criterio contrattuale richiede che la protezione mediante passphrase sia
realmente dimostrata prima di modificare o avviare l'agent. Poiché ciò non è
stato possibile:

- il servizio `ssh-agent` è rimasto `Stopped` e `Disabled`;
- nessuna chiave è stata caricata;
- non è stata richiesta o acquisita alcuna passphrase;
- non è stata effettuata la connessione SSH differenziale;
- nessun fallback password è stato tentato;
- nessun rollback è stato necessario.

## Risultati PASS/FAIL

| Controllo | Risultato |
|---|---|
| Esistenza, file type, owner, ACL e reparse point | PASS |
| Tipo pubblico ED25519 | PASS |
| Alias e direttive attese | PASS |
| Cifratura della chiave privata | NON DIMOSTRATA |
| Prompt interattivo protetto | NON VALUTATO |
| Agent avviato e identità caricata | NON ESEGUITO |
| Codex utilizza l'agent | NON VALUTATO |
| Autenticazione differenziale `publickey` via agent | NON ESEGUITO |
| Assenza di esposizione di credenziali | PASS nel presente lavoro |

## Ripresa interattiva e rollback

La ripresa è avvenuta in una PowerShell visibile, controllata direttamente dal
titolare. La chiave è stata aperta una prima volta tramite OpenSSH con output
pubblico scartato; il titolare ha confermato di aver interagito con il prompt.

Successivamente:

1. `ssh-agent` è stato portato da `Stopped/Disabled` a
   `Running/Automatic` tramite normale conferma amministrativa Windows;
2. l'agent iniziale era vuoto (`ssh-add -l` exit 1);
3. `ssh-add` ha caricato la chiave dedicata con exit 0;
4. l'agent conteneva una sola identità, corrispondente alla fingerprint
   pubblica attesa;
5. durante questa seconda operazione non è stata stabilita una richiesta
   protetta di passphrase; il titolare ha chiesto quale passphrase inserire.

Poiché una chiave caricata in un agent inizialmente vuoto senza una passphrase
nota o dimostrata non soddisfa il requisito di protezione, l'attività si è
arrestata prima della connessione SSH differenziale. Non viene dedotto il
metodo di autenticazione dal solo caricamento.

Rollback completato:

- rimossa esclusivamente la chiave appena caricata (`ssh-add -d`, exit 0);
- agent nuovamente vuoto (`ssh-add -l`, exit 1);
- servizio ripristinato a `Stopped/Disabled`;
- nessun'altra identità rimossa;
- nessuna connessione SSH o modifica VPS eseguita.

## Decisione

La chiave è Ed25519 e i metadati filesystem osservati risultano conformi. Il
caricamento nell'agent ha provato la compatibilità tecnica client/servizio e la
corrispondenza della fingerprint, ma non ha dimostrato la protezione mediante
passphrase. Un controllo parziale non può essere promosso a `VALIDATO`.

La Fase 1 è quindi **BLOCCATO**. Il prossimo passo non duplicativo è una nuova
identità cifrata dedicata, con nome distinto, creata e verificata in una fase
separata senza sovrascrivere o revocare la chiave corrente prima del secondo
accesso riuscito. Tale attività non è autorizzata dal presente incarico.

## Stati

- controlli metadata/ACL e tipo pubblico: **ESEGUITO**;
- proprietà osservate di file, ACL e tipo: **VALIDATO** nel solo perimetro
  metadata/public key;
- compatibilità tecnica agent/fingerprint: **ESEGUITO** nel tentativo poi
  rollbackato;
- cifratura/passphrase della chiave corrente: **BLOCCATO**;
- attivazione persistente OpenSSH Agent: **DA FARE** e **BLOCCATO**;
- autenticazione differenziale via agent: **DA FARE** e **BLOCCATO**;
- fase sudo e accesso amministrativo persistente: **BLOCCATO**.
