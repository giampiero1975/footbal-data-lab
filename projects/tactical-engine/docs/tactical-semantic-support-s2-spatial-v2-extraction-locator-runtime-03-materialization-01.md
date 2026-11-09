# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03 — materializzazione conforme

## Attività

Il 2026-11-09 è stata autorizzata esclusivamente una nuova materializzazione
byte-preserving del wrapper `runtime-03`, senza esecuzione diagnostica,
trasporto o inferenza.

- branch: `codex/tactical-state-contract-v1`;
- HEAD GitHub iniziale: `94cf530af87cdf540f2e59e5b69f4958a8d63d2f`;
- baseline applicativa: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- working tree iniziale: pulito;
- runtime-03 conforme già registrato: assente.

TODO, Experiment Register e i report `runtime-01`, `runtime-02` e `runtime-03`
sono stati riconciliati prima della scrittura. Non sono stati ripetuti test
applicativi o controlli ambientali.

## Script e trasformazione

Sorgente esclusivo:

`C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\spatial-v2-extraction-locator-q3-04-runtime-02.sh`

- dimensione: 45.964 byte;
- SHA-256: `5bcc18266daadb984f5dc8b6256f2bb1a8d095eecab8a03948bef14c8fbcfcaf`;
- occorrenze complete `runtime-02`: 3;
- occorrenze complete `runtime-03`: 0.

La trasformazione ha operato direttamente sui byte originali, sostituendo le
tre sequenze ASCII complete
`spatial-v2-extraction-locator-q3-04-runtime-02` con
`spatial-v2-extraction-locator-q3-04-runtime-03`, agli offset 472, 5175 e
16840. La lunghezza delle sequenze è identica; non sono stati modificati altri
byte.

Artefatto conforme prodotto con nome distinto:

`C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\spatial-v2-extraction-locator-q3-04-runtime-03-approved.sh`

- dimensione: 45.964 byte;
- SHA-256: `ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57`;
- occorrenze complete `runtime-03`: 3;
- occorrenze complete `runtime-02`: 0;
- confronto con la trasformazione binaria autorizzata: identico byte per byte;
- delta di lunghezza rispetto al sorgente: 0;
- ultimo byte sorgente/risultato: `0A`, senza LF aggiuntivo.

## Evidenza precedente conservata

Il file divergente documentato dal tentativo precedente è rimasto presente,
non sovrascritto e non cancellato:

`C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\spatial-v2-extraction-locator-q3-04-runtime-03.sh`

- dimensione: 45.965 byte;
- SHA-256: `ddd74491691beca61a6670622453e31b7ee910544f13aa1a886dd3004c923930`.

## Risultato, decisione e stato

- wrapper Bash eseguiti: 0;
- chiamate di trasporto: 0;
- generazioni Qwen: 0;
- trasferimenti VPS: 0;
- modifiche a staging, checkout operativo, collection, servizi o
  configurazioni: 0;
- wrapper aggiunti al repository: 0.

La materializzazione conforme è **ESEGUITO** e la sua identità byte-per-byte è
**VALIDATO**. Il wrapper è soltanto disponibile localmente fuori dal
repository. Runtime-03 resta **BLOCCATO** e non eseguito; Gate, integrazione e
certificazione restano **BLOCCATO**. La disponibilità dell'artefatto non
costituisce autorizzazione runtime.

Flusso: Attività = materializzazione controllata; Script = wrapper conforme
non eseguito; Commit = esclusivamente documentale; Report = questo documento;
Risultato = identità attesa verificata; Decisione = nessun trasferimento o
runtime; Stato = materializzazione **VALIDATO**, runtime **BLOCCATO**.
