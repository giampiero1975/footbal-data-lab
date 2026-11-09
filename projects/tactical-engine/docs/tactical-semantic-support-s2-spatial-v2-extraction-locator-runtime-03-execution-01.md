# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03 — preflight di esecuzione

## Attività e autorizzazione

Il 2026-11-09 il titolare ha autorizzato il trasferimento sulla VPS e una sola
invocazione diagnostica del wrapper
`spatial-v2-extraction-locator-q3-04-runtime-03`, subordinata al superamento
integrale del preflight immediato.

- branch: `codex/tactical-state-contract-v1`;
- HEAD GitHub iniziale: `88243634b6e470cddd126c42c31966c1002a8f4a`;
- baseline applicativa: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- working tree iniziale: pulito e allineato al remoto;
- precedente esecuzione runtime-03: non registrata.

TODO, Experiment Register, report `runtime-01`, `runtime-02`, `runtime-03` e
`materialization-01` sono stati riconciliati prima delle operazioni. Non sono
stati ripetuti test applicativi.

## Script e trasferimento

Wrapper locale esclusivo:

`C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\spatial-v2-extraction-locator-q3-04-runtime-03-approved.sh`

- dimensione: 45.964 byte;
- SHA-256: `ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57`.

Il file è stato trasferito tramite alias `football-vps` verso un nome
temporaneo univoco e materializzato atomicamente, senza sovrascritture, nel
percorso esterno a checkout e staging:

`/home/football/.local/share/football-data-lab/runtime-wrappers/spatial-v2-extraction-locator-q3-04-runtime-03-approved.sh`

Verifica remota completata prima del preflight:

- tipo: file regolare, non symlink;
- proprietario/gruppo: `football:football`;
- modo: `0600`;
- dimensione: 45.964 byte;
- SHA-256: `ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57`.

## Preflight e arresto

La ricognizione preliminare aveva confermato:

- staging presente, non symlink e HEAD esatto `db3ad66...`;
- status Git pulito, SHA-256 della sequenza vuota
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- directory artefatti runtime-03 assente, inclusi symlink;
- destinazione wrapper inizialmente assente.

Il preflight immediatamente precedente all'esecuzione si è arrestato al primo
controllo negativo durante l'import delle dipendenze con l'interprete previsto
dal wrapper, `/usr/bin/python3`:

`ModuleNotFoundError: No module named 'pydantic'`

Reason code documentale: `E_PYTHON_DEPENDENCY_MISSING_PYDANTIC`.

Il controllo era precedente a qualsiasi invocazione del wrapper e a qualsiasi
trasporto. In applicazione della condizione fail-closed non sono stati eseguiti
retry, installazioni, adattamenti dell'ambiente o ulteriori verifiche VPS.

## Risultato

| Dimensione | Esito |
|---|---|
| Trasferimento e identità wrapper | **VALIDATO** |
| Preflight immediato | **BLOCCATO** |
| Invocazioni wrapper | 0 |
| Chiamate di trasporto | 0 |
| Generazioni Qwen | 0 |
| Exit code wrapper/runtime | non applicabile, wrapper non invocato |
| Request/response | non prodotte |
| Extraction/witness/validation | non prodotti |
| Completamento tecnico | non valutabile |
| Validità strutturale | non valutabile |
| Corrispondenza semantica | non valutabile |
| Fail-closed | rispettato nel preflight esterno |
| Promozione | non autorizzata |

## Decisione e stato

L'attività è stata arrestata prima dell'unica invocazione autorizzata. Il
wrapper remoto conforme è conservato come evidenza; non è stato eseguito.
Qualunque correzione dell'ambiente Python o successiva esecuzione richiede un
incarico esplicito distinto.

Flusso: Attività = esecuzione singola condizionata; Script = wrapper trasferito
e verificato ma non invocato; Commit = esclusivamente documentale; Report =
questo documento; Risultato = preflight bloccato per dipendenza assente;
Decisione = STOP senza retry; Stato = runtime-03 **BLOCCATO**, Gate,
integrazione e certificazione **BLOCCATO**.
