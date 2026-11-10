# RAG V5 Dual Blocker — trasferimento e preflight non generativo runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-TRANSFER-NONGENERATIVE-PREFLIGHT-01`.
Data: 2026-11-10, Europe/Rome.

## Attività

Trasferimento controllato del solo wrapper runtime-04 e preflight diagnostico
separato. Il launcher SSH, il corpo remoto e tutti i blocchi del wrapper non
sono stati eseguiti. Nessuna autorizzazione alla generazione è stata utilizzata.

Prima di operare letti TODO, Experiment Register e report di preparazione
locale/staging, riconciliati con i commit `56fba21`, `83abcde` e `59e8917`.
HEAD iniziale locale/GitHub
`59e89172780c1312223e1271b6023d2c1d7a3f1e`, branch
`codex/tactical-state-contract-v1`, working tree pulito.
Baseline applicativa invariata:
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.

## Script → Commit → Report

Script: due sessioni SSH batch, prima per trasferimento/rilettura, seconda per
diagnostica stdlib e interrogazioni GET locali. Nessuno script installato per
il preflight e nessun processo applicativo avviato. Python diagnostico assoluto
`/usr/bin/python3 -B -I`, senza scrittura bytecode e senza import dei moduli
applicativi. Git di sola lettura con `--no-optional-locks`, hooks e fsmonitor
disabilitati per i singoli comandi.

Commit: esclusivamente report, evidenza JSON, TODO e registro pubblicati
contestualmente; identificabile dalla storia di questo report. Nessuna modifica
al commit tecnico o alla baseline applicativa. Evidenza versionata:
`evaluation/runtime04_transfer_nongenerative_preflight_evidence_01.json`.

## Trasferimento verificato

Sorgente locale:
`projects/tactical-engine/operations/runtime-wrappers/spatial-v2-extraction-locator-q3-04-runtime-04.sh`.

Destinazione VPS:
`/home/football/.local/share/football-data-lab/runtime-wrappers/spatial-v2-extraction-locator-q3-04-runtime-04.sh`.

| Proprietà | Esito osservato |
|---|---|
| Dimensione locale/remota | 47.755 byte |
| SHA-256 locale/remoto | `abf6db3060b68cbc1e5d9e1c28ea13e2cb3dbce09f2ae2b5c00f8ec1e7f55f17` |
| Confronto con commit tecnico `56fba21` | byte locali identici |
| Tipo remoto | file regolare, non symlink |
| Proprietario/gruppo | `football:football` |
| Permessi | `0600` |
| Confronto integrale | rilettura remota decodificata localmente e confrontata byte per byte, identica |
| Runtime-03 originale | byte invariati prima/dopo, SHA storico conforme |

Verificati gli antenati reali e l'assenza di destinazione e temporaneo prima
della scrittura. Temporaneo esclusivo:
`spatial-v2-extraction-locator-q3-04-runtime-04.sh.upload-59e8917` nel medesimo
parent, creato con `O_CREAT|O_EXCL|O_NOFOLLOW`, modo `0600`. Scritti i byte
originali via stdin binario senza conversioni CRLF; hash e dimensione verificati
prima della pubblicazione mediante hard link senza sovrascrittura. Rimosso
soltanto il nome temporaneo di upload; nessuna destinazione preesistente toccata.

## Preflight non generativo osservato

Snapshot diagnostico alle `2026-11-10T13:34:09.670347+00:00`
(14:34:09 Europe/Rome). Esito **VALIDATO** nel solo perimetro osservato.

### Staging ed evidenze riusate

Staging:
`/home/football/.local/share/football-data-lab/staging/spatial-v2-dual-blocker-13814c2`.

- HEAD esatto `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`, detached.
- Status vuoto anche con file untracked inclusi; SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Common directory `.git` interna, reale; nessun alternate/http-alternate,
  commondir o registrazione worktrees apparso.
- Stato Git ancora invariato alla fine della diagnostica.

I quattro blob applicativi/dataset e la validazione Git completa sono riusati
dall'evidenza `runtime04_staging_preparation_evidence_01.json`, pubblicata a
`59e8917`: baseline e stato corrente sono immutati. Non ripetuti `fsck`,
verifica bundle, hash-object dei quattro file o validazione completa staging.
Non ripetuti neppure i 37 test applicativi o i 13 controlli wrapper.

### Percorsi, strumenti e dipendenze

- Parent `runtime-artifacts`, `runtime-locks` e `runtime-wrappers`: directory
  reali, UID 1000 (`football`), modo `0700`, scrivibili/attraversabili.
- Directory `runtime-artifacts/spatial-v2-extraction-locator-q3-04-runtime-04`
  assente anche come symlink, all'inizio e alla fine; mai creata.
- Disponibili Git, Bash, curl, timeout, flock, ps, stat, sha256sum, awk, find,
  sort, xargs, sed, date, id, chmod, mkdir, mv, rm e cat; solo risoluzione dei
  percorsi per gli strumenti, nessuna loro azione di modifica nel preflight.
- `/usr/bin/python3`: Python 3.12.3, interprete diagnostico esatto;
  `/usr/bin/time` eseguibile. Spazio libero osservato: 41.404.141.568 byte.
- Sorgenti dei tre moduli locali richiesti presenti. Import analizzati
  staticamente: solo tali moduli e stdlib `hashlib`, `json`, `unicodedata`,
  `urllib.error`, `urllib.request`. Verificati import delle sole dipendenze
  stdlib; nessun import o chiamata applicativa e nessuna installazione.
  Non richiesti `pydantic` o `requests`.

### Lock e concorrenza — osservazione senza acquisizione

Lock condiviso:
`/home/football/.local/share/football-data-lab/runtime-locks/spatial-v2-extraction-locator.lock`.

File regolare non symlink, proprietario corrente, modo `0600`, zero byte,
accessibile in lettura/scrittura; device `64769`, inode `842518`.
Letto `/proc/locks` e confrontati device/inode: nessuna entry corrispondente.
Il file non è stato aperto per scrittura, acquisito, ricreato o modificato.

Esaminati 186 cmdline di processi visibili, zero letture negate o processi
scomparsi durante la lettura; nessuna corrispondenza con i runner diagnostici
pertinenti o i runner Ollama ricercati. Questa è un'osservazione dei processi
visibili e del namespace procfs corrente, non una prova universale di assenza
di attività né una prenotazione del lock. Non garantisce lo stato futuro o
l'acquisibilità esclusiva al momento di una futura esecuzione.

### Diagnostica Ollama

Effettuate esclusivamente:

```text
GET http://127.0.0.1:11434/api/tags
GET http://127.0.0.1:11434/api/ps
GET http://127.0.0.1:11434/api/version
```

Ollama `0.40.5`. Un solo record corrispondente a `qwen3.5:9b`, 9.0B Q4_K_M,
digest esatto
`56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`.
`/api/ps` restituisce `models=[]`: nessun modello caricato nello snapshot.
Nessun endpoint generativo, POST, warm-up, caricamento o pull del modello.

## Anomalie e limiti

Nessuna anomalia bloccante osservata. I controlli di dipendenze attestano
presenza dei sorgenti e disponibilità della stdlib; l'import effettivo dei
moduli applicativi non è stato eseguito per mantenere il limite richiesto.
Lock e concorrenza sono osservazioni istantanee e non sono risorse riservate.
La preparazione non attesta tempi reali, validità di un futuro output Qwen o
accuratezza delle contraddizioni.

## Risultato → Decisione → Stato

Trasferimento **ESEGUITO** e identità integrale **VALIDATO**. Preflight
**ESEGUITO**, **VALIDATO** esclusivamente nel perimetro non generativo
osservato. Evidenze di perimetro: zero esecuzioni wrapper, zero richieste
generative inviate, tre sole GET diagnostiche, lock non acquisito, nessun
modulo applicativo importato e directory artefatti runtime-04 ancora assente.

Decisione: STOP dopo pubblicazione del report e aggiornamento contestuale
TODO/registro. Nessun retry/repair/fallback, modifica al checkout operativo,
staging storici, Chroma, indici, corpus, servizi o panel; nessun merge, deploy
o promozione. Il runtime-04 resta **BLOCCATO** fino a distinta autorizzazione
all'esecuzione; accuratezza delle contraddizioni, Gate, integrazione e
certificazione restano **BLOCCATO**.
