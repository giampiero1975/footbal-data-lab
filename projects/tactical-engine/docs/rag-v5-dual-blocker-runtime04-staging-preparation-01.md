# RAG V5 Dual Blocker — staging indipendente runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-STAGING-PREPARATION-01`.
Data: 2026-11-10, Europe/Rome.

## Attività

Preparazione e verifica del solo staging Git indipendente alla baseline
applicativa congelata, autorizzata separatamente dalla preparazione wrapper.
Nessuna esecuzione o trasferimento del wrapper runtime-04.

Riconciliati prima di operare TODO ufficiale, Experiment Register, report
`rag-v5-dual-blocker-runtime04-local-preparation-01.md`, commit tecnico
`56fba214c6a2d438bf1e1c4383dc920654cfc5c7` e pubblicazione
`83abcde029a8c28432bc4a7b8b12c2a318b5dbcf`. HEAD iniziale locale e GitHub
coincidenti con quest'ultimo commit, branch
`codex/tactical-state-contract-v1`, working tree locale pulito.
Nessuna riesecuzione dei 37 test o dei 13 controlli del wrapper.

## Script

Comandi Git locali e Python stdlib inline per controllo percorsi, trasporto
binario esclusivo, hash e fotografie Git. Tre sessioni SSH: preflight read-only,
trasferimento del solo bundle, creazione/verifica staging. Nessuna installazione
di dipendenze, import applicativo, richiesta Ollama o accesso Chroma.

Comandi Git rilevanti:

```text
git bundle create <bundle-locale> refs/heads/codex/staging-runtime04-13814c2
git -C <repository-bare-vuoto> bundle verify <bundle-locale>
git clone --no-checkout --no-hardlinks --template= <bundle> <destinazione>
git -C <destinazione> checkout --detach 13814c20d80bca4d9cb4cb08a288b6e7b31dac0d
git -C <destinazione> fsck --full --strict
git -C <destinazione> bundle verify <bundle-remoto>
```

I comandi remoti Git usano anche `--no-optional-locks`,
`-c core.hooksPath=/dev/null` e `-c core.fsmonitor=false`: nessun hook o
monitor esterno eseguito. Clone da bundle locale VPS, senza rete GitHub,
senza checkout del branch documentale attuale e senza uso del checkout operativo.

## Commit → Report

Baseline applicativa congelata e verificata:
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.

Il commit di questa attività contiene soltanto report, evidenza JSON, TODO e
registro; è identificabile con la storia di questo report. È distinto dalla
baseline applicativa e dai commit del wrapper, che non vengono distribuiti.

Evidenza completa versionata:
`evaluation/runtime04_staging_preparation_evidence_01.json`.
Contiene snapshot prima/dopo, trasporto, hash, blob e risultato delle verifiche.

## Bundle e trasporto

Percorso locale del bundle effettivamente trasferito:
`C:\Users\giamp\.codex\visualizations\2026\11\10\01a1c50c-905a-7f30-a5ad-89b57aa7b71d\runtime04-staging\spatial-v2-dual-blocker-13814c2-clone.bundle`.

Percorso remoto conservato:
`/home/football/.local/share/football-data-lab/staging/spatial-v2-dual-blocker-13814c2.bundle`.

| Proprietà | Valore verificato |
|---|---|
| Dimensione locale/remota | 2.728.883 byte |
| SHA-256 locale/remoto | `05c4f8726c1a1f701ec46af63a32f066caac416d6b69f3578dc69ddf9bd0ae29` |
| Unico ref nel bundle | `refs/heads/codex/staging-runtime04-13814c2` |
| Commit del ref | baseline completa `13814c2...` |
| Storia | completa, nessun prerequisito Git esterno |
| Modo remoto bundle | `0600` |

Creato un ref temporaneo locale alla sola baseline, senza cambiare il branch
corrente; rimosso dopo la creazione del bundle. Nessun commit successivo alla
baseline incluso: il wrapper runtime-04 introdotto in `56fba21` non è stato
trasferito neppure nella storia del bundle.

Prima del trasferimento: `git bundle verify` in un repository bare vuoto e
clone locale senza checkout con presenza del commit congelato verificata.
Il trasferimento ha usato un file `.bundle.upload` creato con
`O_CREAT|O_EXCL|O_NOFOLLOW`, modo `0600`; dimensione e hash verificati prima
della pubblicazione mediante hard link senza sovrascrittura. Il solo nome
temporaneo di upload è stato poi rimosso, non sono stati rimossi altri file.

### Anomalia locale risolta prima dell'upload

Il primo bundle locale usava un ref sotto `refs/codex-staging/`: conteneva
la storia completa, ma il controllo di clone locale non selezionava quel ref
e produceva un repository vuoto. Nessuna copia era stata inviata alla VPS.

Registrata la differenza tecnica, è stato creato un bundle distinto con ref
`refs/heads/...`, senza cambiare la baseline; verifica in repository vuoto e
clone locale hanno superato il controllo. Gli artefatti locali iniziali sono
stati conservati e non trasferiti. Nessun retry di runtime o test applicativo.

## Destinazione e isolamento

Staging creato esclusivamente in:
`/home/football/.local/share/football-data-lab/staging/spatial-v2-dual-blocker-13814c2`.

| Controllo | Evidenza |
|---|---|
| Parent | directory reale `football`, modo `0700`, accessibile in scrittura |
| Destinazione/bundle/upload prima delle scritture | assenti, inclusi symlink dangling |
| Destinazione creata | directory reale modo `0700`, creazione esclusiva |
| HEAD | `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`, detached |
| Working tree | pulito, anche con `--untracked-files=all` |
| SHA-256 status vuoto | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `.git` e common directory | directory reale interna allo staging |
| Git alternates/http-alternates | assenti |
| `.git/commondir`, `.git/worktrees` | assenti |
| Shallow repository | false |
| Symlink e hardlink nei file `.git` | assenti; file con link count 1 |
| `GIT_ALTERNATE_OBJECT_DIRECTORIES` | non impostato |
| Origin | percorso del solo bundle remoto sopra indicato |
| `git fsck --full --strict` | exit 0 |
| `git bundle verify` remoto | exit 0, storia completa |

Nessun symlink negli antenati critici, in `.git` o nei percorsi dei quattro
file richiesti. I quattro file sono regolari, modo `0600`; blob HEAD,
`hash-object --no-filters` e SHA-256 dei byte di checkout corrispondono.

| Componente in `projects/tactical-engine/` | Blob Git | SHA-256 checkout |
|---|---|---|
| `scripts/shadow_nli_spatial_relations_v2_inference.py` | `8ac93d07341e1079ee3ca6ff98327a8391b7ab5f` | `b6f30e76a2ccf98a4c027beff7fd2e36128da42797d2fcbbe144dc3e6089a9c6` |
| `scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py` | `1a64827b26fb30758773049eedeb342a2bb826b2` | `a1592fa491fe20590e2e85e35b5c4397365c8bdc9dbc898bc9d9e0c2d8b73aef` |
| `scripts/v5_tactical_semantic_support_s2_spatial_v2.py` | `0a8b92acbda67afeaee4bc057f89729e11e20ab5` | `06e071b50c69683c8ed69257a238c6fe53b00cc60ad589ec61ab1100b59a3b46` |
| `eval/claim_fidelity_gold_v1.json` | `4523eb746d666fdfb161c5d38d8db31f12e99b92` | `8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c` |

I quattro blob coincidono con quelli richiesti dal wrapper runtime-04 locale.
Non è stata eseguita alcuna funzione di quei moduli.

## Preservazione dei checkout precedenti

Confrontati prima/dopo HEAD, detached/branch, hash e numero righe di status,
common directory del checkout operativo e di tutti gli otto staging storici
Git reali trovati direttamente nel parent staging. Tutti i nove snapshot
coincidono esattamente; dettaglio nell'evidenza JSON.

- Operativo `/opt/football-data-lab`: `1a80fe0...`, 17 righe untracked
  preesistenti preservate, status SHA-256
  `3877d2b2bb6f9d39300327e58e412c5178089811b9f2db77c716482f35795d06`.
- Storici: `s2-first-controlled-b1946f8`,
  `s2-spatial-differential-0d40719`,
  `spatial-v2-extraction-locator-db3ad66`, `spatial-v2-q3-04-009f76e`,
  `spatial-v2-q3-04-360-69ec127`, `spatial-v2-q3-04-prompt-runtime-41d50fa`,
  `tsc-v1-3fa3a18`, `tsc-v2-965d6b6`.

Gli snapshot Git attestano tali proprietà, non l'identità universale di ogni
file runtime non tracciato. Nessuna operazione di scrittura è stata indirizzata
ai checkout precedenti o agli artefatti runtime, modelli, servizi e indici.
La directory artefatti runtime-04 è ancora assente. Il nuovo staging non
contiene `operations/runtime-wrappers`, introdotta solo dopo la sua baseline.

## Risultato → Decisione → Stato

Bundle autosufficiente e identità trasporto **VALIDATO**. Clone staging
**IMPLEMENTATO**, controlli Git/blob/isolamento **ESEGUITO**, staging isolato
**VALIDATO** nel perimetro sopra descritto. Nessun blocco residuo per questa
sola preparazione; backup della chiave separato.

Decisione: STOP operativo dopo la verifica dello staging e sola pubblicazione
del closeout. Nessun trasferimento o esecuzione wrapper runtime-04, nessun
Qwen, codice applicativo, corpus, dipendenza, Chroma, panel, servizio, merge
o deploy. Trasferimento del wrapper e preflight runtime richiedono una
successiva autorizzazione. Runtime post-patch, accuratezza delle contraddizioni,
Gate, integrazione e certificazione restano **BLOCCATO**.
