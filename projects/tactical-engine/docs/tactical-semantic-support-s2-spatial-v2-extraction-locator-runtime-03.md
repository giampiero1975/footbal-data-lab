# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03

## Attività e autorizzazione

Tentativo autorizzato per la materializzazione controllata e una sola
esecuzione diagnostica di
`spatial-v2-extraction-locator-q3-04-runtime-03`.

- data: 2026-11-09;
- branch: `codex/tactical-state-contract-v1`;
- HEAD GitHub iniziale: `1774a4adf387980283ac784828dc680b7138cce4`;
- baseline applicativa: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- wrapper sorgente SHA-256:
  `5bcc18266daadb984f5dc8b6256f2bb1a8d095eecab8a03948bef14c8fbcfcaf`;
- wrapper atteso `runtime-03`: 45964 byte, SHA-256
  `ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57`.

TODO, Experiment Register e report precedenti sono stati riconciliati prima
delle scritture. `runtime-03` non risultava eseguito o registrato e il working
tree documentale era pulito.

## Preflight read-only

Il preflight remoto precedente alla materializzazione ha restituito PASS:

- staging presente, non symlink, detached a `db3ad66...`;
- index e working tree puliti, status SHA-256 vuoto
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- common directory interna e alternates assenti;
- quattro blob Git conformi;
- dataset SHA-256
  `8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c`;
- dipendenze richieste disponibili;
- directory artefatti `runtime-03` assente, inclusi symlink;
- lock regolare vuoto e non symlink;
- modello `qwen3.5:9b` con digest
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
- endpoint non generativi disponibili, zero modelli caricati e zero processi
  concorrenti pertinenti osservati;
- spazio disponibile circa 40,5 GB.

Non è stata inviata alcuna richiesta generativa.

## Materializzazione e arresto

Il file locale è stato derivato dal wrapper `runtime-02` sostituendo i tre
riferimenti completi con `runtime-03`. La verifica obbligatoria dell'identità ha
però rilevato:

| Proprietà | Atteso | Osservato |
|---|---:|---:|
| dimensione | 45964 byte | 45965 byte |
| SHA-256 | `ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57` | `ddd74491691beca61a6670622453e31b7ee910544f13aa1a886dd3004c923930` |
| riferimenti `runtime-02` | 0 | 0 |
| riferimenti `runtime-03` | 3 | 3 |

Confronto byte-per-byte: i primi 45964 byte coincidono con la trasformazione
autorizzata; il file osservato contiene un byte LF aggiuntivo (`0A`) in coda.

In applicazione della condizione fail-closed, il file non è stato corretto,
trasferito o eseguito. È stato conservato come evidenza locale in:

`C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\spatial-v2-extraction-locator-q3-04-runtime-03.sh`

## Risultato e classificazione

- esecuzioni effettive del wrapper: `0`;
- chiamate di trasporto: `0`;
- generazioni Qwen: `0`;
- exit code runtime: non applicabile;
- reason code documentale: `E_WRAPPER_IDENTITY_MISMATCH`;
- request/response/extraction/witness/validation: non prodotti;
- esito tecnico e semantico: non valutabile;
- promozione: non autorizzata;
- staging: invariato rispetto al preflight read-only.

| Componente | Stato |
|---|---|
| Preflight read-only | **ESEGUITO** |
| Prerequisiti ambientali osservati | **VALIDATO** nel solo snapshot |
| Materializzazione wrapper runtime-03 | **BLOCCATO** |
| Runtime runtime-03 | **BLOCCATO** e non eseguito |
| Gate, integrazione e certificazione | **BLOCCATO** |

## Decisione

Arresto prima dell'esecuzione, senza retry o correzioni automatiche. Qualunque
nuova materializzazione o tentativo richiede una decisione esplicita distinta.

Flusso: Attività = runtime-03 autorizzato condizionatamente; Script = wrapper
non conforme all'identità attesa e non eseguito; Commit = documentale; Report =
questo documento; Risultato = arresto pre-esecuzione; Decisione = nessun retry;
Stato = **BLOCCATO**.
