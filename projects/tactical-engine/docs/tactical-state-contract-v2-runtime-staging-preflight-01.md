# TSC V2 — staging isolato e preflight infrastrutturale 01

## Identità

- Attività: `RD-TSC-V2-RUNTIME-STAGING-PREFLIGHT-01`
- HEAD GitHub iniziale: `6b311931571cc5a1157daeb7a76e3af37822e826`
- Baseline tecnica richiesta: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`
- Alias SSH: `football-vps`
- VPS osservata: `football@football-data-lab.localdomain`

## Ricognizione read-only

Checkout operativo `/opt/football-data-lab`: presente, HEAD
`1a80fe0c6261b10f748a36c2b4fd96e8e2253971`, già sporco per artefatti non
tracciati. Non è stato modificato.

Parent staging:
`/home/football/.local/share/football-data-lab/staging`, directory regolare mode
`700`, proprietario/gruppo `football`, circa 41,6 GB disponibili.

Staging preesistente:
`/home/football/.local/share/football-data-lab/staging/tsc-v1-3fa3a18`, clone
indipendente a `3fa3a189b213884df6f08544c827fd306c5fd007`, working tree non pulito.
Non è idoneo alla baseline richiesta e non è stato modificato. È inoltre presente
il bundle storico `tsc-v1-3fa3a18.bundle`, non toccato.

Il commit `965d6b6` non è disponibile né nel checkout operativo né nello staging V1.
Il target proposto
`/home/football/.local/share/football-data-lab/staging/tsc-v2-965d6b6` era assente,
inclusi symlink dangling.

## Tentativo autorizzato di clone indipendente

È stato tentato una sola volta il clone diretto GitHub, senza `git worktree`:

`git clone --no-checkout git@github.com:giampiero1975/footbal-data-lab.git /home/football/.local/share/football-data-lab/staging/tsc-v2-965d6b6`

Esito: fallito prima del checkout con `Permission denied (publickey)`. La verifica
successiva ha confermato che il target non esiste: Git non ha lasciato un clone
parziale. Non sono stati tentati bundle, trasferimenti, copie o retry.

## Ambiente runtime osservato

- interprete richiesto presente:
  `/opt/football-data-lab/projects/tactical-engine/.venv/bin/python`;
- l'entry point è un symlink interno alla virtualenv;
- versione: Python 3.12.3;
- `/usr/bin/time`: presente;
- `/usr/bin/timeout`: presente.

La disponibilità dei moduli rispetto al nuovo staging non è attestabile in assenza
del checkout. Nessun import applicativo, modello o peso è stato caricato.

## Collection metadata-only

La verifica della collection candidata non è stata eseguita. Il fallimento del
prerequisito staging imponeva l'arresto; non è stato aperto Chroma, non sono state
eseguite query/get/retrieval e il dato storico 6410 non è stato promosso a evidenza
corrente.

## Comando Gate

La revisione statica precedente resta valida, ma `TSC_V2_GATE_ROOT` non può essere
risolto verso un checkout attestato. Nessuna rettifica ai parametri è autorizzata o
necessaria in questa attività. Il comando non è stato eseguito.

## Anomalie di ricognizione

La prima lettura si è arrestata per l'uso incompatibile di `df -P` e `--output`; è
stata ripresa una sola volta dai controlli non acquisiti con `df -B1 --output`.
L'ultima stampa del conteggio dirty ha incontrato un carattere CR nella pipeline
`wc`; HEAD e assenza del target erano già stati acquisiti e non è stato effettuato
un ulteriore tentativo. Nessuna delle due anomalie ha modificato la VPS.

## Decisione e stato

Il checkout isolato alla baseline richiesta non è stato predisposto; collection e
compatibilità completa restano non attestate. Pertanto:

- preflight infrastrutturale: **BLOCCATO**;
- Gate runtime: **BLOCCATO**;
- integrazione: **BLOCCATO**;
- certificazione: **BLOCCATO**.

Per proseguire serve una nuova autorizzazione esplicita a un metodo di trasferimento
del commit (per esempio bundle verificato), senza modificare credenziali o checkout
operativo.
