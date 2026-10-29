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
