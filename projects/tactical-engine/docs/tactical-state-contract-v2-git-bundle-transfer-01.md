# TSC V2 — trasferimento Git bundle e staging isolato

## Identità

- Attività: `RD-TSC-V2-GIT-BUNDLE-TRANSFER-01`
- HEAD GitHub iniziale: `65263848e60e12569c96736129bea8881fd70ba1`
- Baseline Gate: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`
- Repository sorgente:
  `C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\codex-perf-worktree`

## Bundle locale

- Percorso:
  `C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\tsc-v2-965d6b6-965d6b60.bundle`
- Dimensione: `1926658` byte
- SHA-256: `70f7f5b4325513f78f4f42480bb7654bd4f9145398fd8b3b58b5e07b4c848e7d`
- Ref: `refs/heads/codex/tactical-state-contract-v1` a
  `65263848e60e12569c96736129bea8881fd70ba1`
- `git bundle verify`: PASS; storia completa, nessun prerequisito esterno.

La baseline tecnica è un antenato verificato del ref incluso e il bundle contiene
tutti gli oggetti necessari. Le modifiche non committate non fanno parte del bundle.

## Trasferimento e verifica VPS

- Alias: `football-vps`
- Bundle remoto:
  `/home/football/.local/share/football-data-lab/staging/tsc-v2-965d6b6-965d6b60.bundle`
- Dimensione remota: `1926658` byte
- SHA-256 remoto:
  `70f7f5b4325513f78f4f42480bb7654bd4f9145398fd8b3b58b5e07b4c848e7d`
- `git bundle verify` remoto: PASS; stessa ref e storia completa.

Il bundle è stato conservato: la presente autorizzazione non ne prevedeva la
rimozione.

## Clone indipendente

- Percorso:
  `/home/football/.local/share/football-data-lab/staging/tsc-v2-965d6b6`
- HEAD: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`
- Modalità: detached HEAD
- Working tree: pulito; hash dello status vuoto
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Git common dir: `.git`
- `objects/info/alternates`: assente
- Script V2, wrapper e runner: presenti
- `evaluation/`: directory regolare, mode `775`, proprietario/gruppo `football`,
  scrivibile e non symlink
- quattro artefatti Gate: assenti, inclusi symlink dangling.

La directory `evaluation/` era già contenuta nel checkout; il tentativo di crearla
ha restituito `File exists` dopo che clone e checkout erano già riusciti. La verifica
successiva ne ha attestato tipo, permessi e idoneità senza modificarla.

## Invarianza dei checkout preesistenti

Checkout operativo prima/dopo:

- HEAD `1a80fe0c6261b10f748a36c2b4fd96e8e2253971`
- status SHA-256
  `3877d2b2bb6f9d39300327e58e412c5178089811b9f2db77c716482f35795d06`
- common dir `.git`

Staging V1 prima/dopo:

- HEAD `3fa3a189b213884df6f08544c827fd306c5fd007`
- status SHA-256
  `dc8be9804101288dcf13ce53c8b9d7ab535ebdb5ef65dd1b75e4ed2f36c74a4d`
- common dir `.git`

Entrambi sono invariati. Nessuna pulizia o correzione è stata effettuata.

## Anomalie non sostanziali

La prima fotografia remota si è interrotta per un terminatore CR e un successivo
tentativo di quoting è fallito prima delle letture; il terzo comando read-only ha
acquisito correttamente le fotografie. Nessuna scrittura è derivata da tali errori.
Il clone diretto GitHub fallito nella precedente attività non è stato ripetuto.

## Decisione e stato

- trasferimento bundle: **VALIDATO**;
- staging isolato: **VALIDATO**;
- verifica collection: **BLOCCATO**;
- Gate runtime: **BLOCCATO**;
- integrazione: **BLOCCATO**;
- certificazione: **BLOCCATO**.

Non sono stati eseguiti Chroma, API, retrieval, test E2E, modelli o inferenze.
