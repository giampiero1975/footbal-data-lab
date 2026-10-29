# RAG Corpus — Transizioni.Ussia Preflight Read-Only 01

Data: 2026-10-29  
Ramo: `codex/tactical-state-contract-v1`  
Baseline riconciliata: `bc752fd541dd8b178d0fa43758c33d5b392b205f`

## 1. Autorizzazione e perimetro

Il titolare ha autorizzato una sola connessione SSH alla VPS per verificare
esclusivamente i metadati filesystem di tre percorsi letterali. Erano vietati
lettura dei contenuti, enumerazione di directory, Chroma/SQLite, hash, copie,
snapshot, export, file temporanei, privilegi aggiuntivi e procedure
alternative.

La riconciliazione GitHub non ha individuato un preflight equivalente. I
preflight Ussia storici registrati riguardano fonti/Gemini, non i tre percorsi
di questa attività.

## 2. Tentativo autorizzato

È stata effettuata una sola connessione SSH non interattiva con autenticazione
batch. Il comando remoto predisposto avrebbe usato soltanto `stat`, test di
esistenza/tipo e controllo di leggibilità teorica sui tre percorsi. In caso di
link simbolico non avrebbe seguito la destinazione.

La connessione è stata rifiutata prima dell'esecuzione remota:

```text
football@163.5.26.155: Permission denied (publickey,password).
```

Non è stato eseguito alcun comando sulla VPS. In rispetto del limite di una
sola connessione non è stato effettuato un secondo tentativo né usata una
procedura alternativa.

## 3. Inventario dei percorsi

| Etichetta | Percorso autorizzato | Osservazione VPS | Classificazione |
|---|---|---|---|
| JSON | `/opt/football-data-lab/knowledge/processed/formations-and-systems/Transizioni.Ussia.json` | nessuna; autenticazione fallita | `nominal_unconfirmed` |
| Sidecar | `/opt/football-data-lab/knowledge/processed/formations-and-systems/Transizioni.Ussia.meta.json` | nessuna; autenticazione fallita | `nominal_unconfirmed` |
| Chroma root | `/opt/football-data-lab/knowledge/rag/chroma` | nessuna; autenticazione fallita | `nominal_unconfirmed` |

La classificazione deriva dall'assenza di osservazione runtime, non prova che i
percorsi siano assenti o inaccessibili con credenziali valide.

## 4. Percorsi e artefatti non verificati

Restano `unknown` nel perimetro di questo preflight:

- PDF originale;
- snapshot o backup isolato;
- staging riservato;
- log o manifest della run;
- ambiente Python storico;
- cache tokenizer e remote code.

GitHub registra storicamente un SHA-256 del PDF Ussia e precedenti attività su
fonti, ma tali attestazioni non sostituiscono la verifica dei percorsi né
autorizzano la lettura dei relativi contenuti.

## 5. Snapshot e lacune residue

La documentazione GitHub richiede uno snapshot coerente e un'evidenza
qualificata, ma non definisce un meccanismo concreto già verificato per crearlo.
Poiché la connessione non ha raggiunto la shell remota, non è stato possibile
verificare neppure l'esistenza di uno snapshot già isolato.

Restano inoltre non confermati PDF, sidecar, JSON, staging e provenienza della
stessa run. L'acquisizione non può essere richiesta come operazione eseguibile
finché autenticazione e preflight non vengono risolti mediante una nuova
autorizzazione esplicita.

## 6. Integrità del perimetro

- nessun contenuto letto o copiato;
- nessun comando eseguito sulla VPS;
- nessun accesso Chroma/SQLite;
- nessuna enumerazione, hash, snapshot, export o staging;
- nessuna modifica a corpus, indici, servizi, permessi o configurazioni;
- nessun download, test, inferenza, embedding, indicizzazione, merge o deploy.

La sola conseguenza esterna possibile è la normale registrazione del tentativo
SSH fallito nei log di autenticazione dell'host.

## 7. Decisione e stati

Decisione: preflight **BLOCCATO** per autenticazione SSH rifiutata prima di
qualsiasi osservazione. Nessun tentativo aggiuntivo senza nuova autorizzazione.

- preflight: **BLOCCATO**;
- piano pilota: **ESEGUITO**;
- acquisizione bundle: **DA FARE**;
- verificatore sintetico: **VALIDATO**;
- adapter reale: **BLOCCATO**;
- collection reale/runtime: **BLOCCATO**;
- nulla di nuovo **INTEGRATO** o **CERTIFICATO**.

## 8. Secondo tentativo autorizzato e diagnosi differenziale

Il titolare ha successivamente confermato di avere aperto manualmente una
sessione `ssh football@163.5.26.155` e di essersi autenticato con password.
Questa evidenza dimostra l'utilizzabilità del metodo interattivo dal suo
terminale, ma non autorizza né prova l'accesso dal processo isolato Codex.

Con una nuova autorizzazione limitata a una sola connessione, Codex ha tentato
di aprire una sessione SSH interattiva con pseudo-terminale. Il client è
terminato prima di mostrare la richiesta della password:

```text
ssh: connect to host 163.5.26.155 port 22: Permission denied
```

Il messaggio differisce dal precedente rifiuto di autenticazione
`football@... Permission denied (publickey,password)`: in questo secondo caso
non risulta avviato lo scambio di autenticazione e il titolare non ha avuto la
possibilità di inserire la password. Non è quindi corretto attribuire il
fallimento a password, account o configurazione SSH della VPS. L'evidenza
circoscrive il blocco al percorso di rete/processo del contesto Codex usato per
il tentativo.

In rispetto del limite autorizzato non è stato effettuato alcun retry. Nessun
comando remoto è stato eseguito e le classificazioni dei tre percorsi restano
`nominal_unconfirmed`.

Decisione aggiornata: preflight ancora **BLOCCATO**, ora per impossibilità del
processo Codex di aprire la connessione interattiva autorizzata, non per
indisponibilità dimostrata dell'autenticazione a password. Un passo successivo
richiede una procedura distinta: esecuzione manuale, da parte del titolare, di
un comando metadata-only previamente revisionato oppure disponibilità di un
terminale Codex con accesso di rete SSH effettivo. Nessuna delle due procedure
è autorizzata implicitamente da questo report.

## 9. Esecuzione manuale metadata-only autorizzata

Il titolare ha autorizzato ed eseguito una sola volta il comando metadata-only
revisionato, dopo autenticazione SSH manuale come utente `football`. Il comando
ha usato esclusivamente test shell e `stat` sui tre percorsi letterali, senza
lettura di contenuti, enumerazione di directory, hash, copie, snapshot, export,
Chroma, SQLite, Python, privilegi aggiuntivi o modifiche remote.

Output restituito integralmente e verificato:

| Etichetta | Stato | Tipo | Dimensione | Mtime | Proprietario:gruppo | Permessi |
|---|---|---|---:|---|---|---|
| JSON | `confirmed` | regular file | 501909 | `2026-10-21 03:16:21.319698605 +0200` | `football:football` | `-rw-------` (`600`) |
| SIDECAR | `confirmed` | regular file | 500 | `2026-10-21 03:16:24.888796756 +0200` | `football:football` | `-rw-------` (`600`) |
| CHROMA_ROOT | `confirmed` | directory | 4096 | `2026-10-29 09:01:05.208828426 +0100` | `football:football` | `drwxrwxr-x` (`775`) |

Nessun percorso è stato riportato come link simbolico e non sono stati
restituiti errori di accesso ai metadati. `confirmed` prova esclusivamente
l'osservazione del percorso e dei metadati sopra riportati: non prova integrità,
provenienza storica, appartenenza alla stessa run, completezza documentale,
consistenza della collection o disponibilità di uno snapshot probatorio.

## 10. Recupero accesso tecnico Codex

Separatamente dal preflight, è stata creata una chiave Ed25519 locale dedicata
e la sola chiave pubblica è stata aggiunta dal titolare all'account `football`
con opzione OpenSSH `restrict`. Un unico test autorizzato, con password e
fallback interattivi disabilitati, ha restituito:

```text
SSH_KEY_ACCESS_OK
```

La chiave privata non è nel repository. Il test dimostra soltanto
l'autenticazione tramite la chiave dedicata; non amplia il perimetro delle
future operazioni, che restano soggette ad autorizzazione.

## 11. Decisione conclusiva

Il preflight metadata-only è **ESEGUITO**: i tre percorsi nominali sono ora
`confirmed`. L'acquisizione del bundle resta **DA FARE** e non è autorizzata da
questa evidenza. Restano **BLOCCATO** lo snapshot probatorio, l'adapter reale e
la verifica della collection runtime. Nulla è **INTEGRATO** o **CERTIFICATO**.
