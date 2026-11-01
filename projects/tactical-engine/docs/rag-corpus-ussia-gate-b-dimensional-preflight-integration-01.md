# RAG Corpus — USSIA Gate B dimensional preflight integration 01

Data: 2026-10-30
Branch: `codex/tactical-state-contract-v1`
Baseline: `23508fc3a7bb4f0b33ab95687ae5d55b6c6be6ab`
Commit tecnico: `7e9dae3211c3a65113524cef3ca980e77eae5c77`

## Attività e obiettivo

Consolidare localmente nel repository lo script metadata-only USSIA Gate B
approvato mediante revisione statica indipendente, senza eseguirlo e senza
autorizzare preflight, cold copy o attività runtime.

## Artefatto sorgente

- nome: `USSIA_GATE_B_DIMENSIONAL_PREFLIGHT_DERIVED_05.txt`;
- righe: 1.486;
- dimensione: 36.372 byte;
- SHA-256: `2644d06899c74d1eae49c1de6bdbdde82e88382844993200bdee98edf3f800dd`;
- newline terminale: presente;
- prima riga: `#!/usr/bin/env bash`;
- ultima riga logica: `finish_result 0 'COMPLETE_CAPACITY_PASS'`.

La revisione statica indipendente di Derived 05 è **VALIDATO** esclusivamente
nel perimetro statico. Non costituisce validazione dinamica o runtime.

## Integrazione

Percorso definitivo:

`projects/tactical-engine/scripts/ussia_gate_b_dimensional_preflight_v1.sh`

Il file è stato copiato byte-per-byte, mantenendo LF e newline terminale. La
modalità Git è `100755`. Lo SHA-256 del file integrato è:

`2644d06899c74d1eae49c1de6bdbdde82e88382844993200bdee98edf3f800dd`

ed è identico all'artefatto approvato. Il commit tecnico contiene soltanto il
nuovo script.

## Controlli svolti

- branch e HEAD iniziali riconciliati con la baseline;
- fetch del solo branch GitHub pertinente;
- remoto e locale sulla stessa baseline, divergenza `0/0`;
- working tree iniziale pulito;
- destinazione precedentemente assente;
- assenza di uno script Bash equivalente nel repository;
- identità sorgente/destinazione verificata per hash, byte e righe;
- diff statico circoscritto e `git diff --check` superato;
- modalità Git eseguibile verificata.

Non sono stati eseguiti lo script, `bash -n`, ShellCheck, fixture, test,
SSH/VPS, Chroma/SQLite, snapshot, arresti di servizi o cold copy.

## Risultato e decisione

Lo script è **IMPLEMENTATO** localmente al commit tecnico
`7e9dae3211c3a65113524cef3ca980e77eae5c77`.

I commit locali non costituiscono ancora tracciamento GitHub remoto e non
saranno pubblicati senza autorizzazione separata.

## Addendum post-pubblicazione

Il consolidamento locale documentato sopra è stato successivamente pubblicato
sul branch GitHub `codex/tactical-state-contract-v1`.

HEAD remoto verificato:

`032bd5594b7939bb23c36eb05d436adbc317632a`

Catena pubblicata:

`23508fc3a7bb4f0b33ab95687ae5d55b6c6be6ab`

→ `7e9dae3211c3a65113524cef3ca980e77eae5c77`

→ `032bd5594b7939bb23c36eb05d436adbc317632a`

Pubblicazione GitHub: **ESEGUITO**.

Questa pubblicazione non modifica gli altri stati: revisione statica
**VALIDATO** esclusivamente nel perimetro statico; script **IMPLEMENTATO**;
preflight dimensionale e misurazione RSS **DA FARE**; cold copy, adapter reale
e certificazione runtime **BLOCCATO**. Non **VALIDATO runtime**, **INTEGRATO**
o **CERTIFICATO**.

## Limiti residui

- preflight dimensionale non eseguito;
- misurazione RSS ancora **DA FARE** e priva di soglia numerica arbitraria;
- quote non promosse a `VERIFIED`;
- nessuna consistenza temporale della collection dimostrata;
- limite di un milione di identità non equivalente a garanzia RAM;
- nessuna validazione runtime, integrazione nella pipeline o certificazione;
- cold copy non autorizzata.

## Stati ufficiali

| Attività | Stato |
|---|---|
| Diagnostica SSH Gate B | **ESEGUITO** |
| Closeout documentale Gate B | **ESEGUITO** |
| Revisione statica Derived 05 | **VALIDATO** limitatamente al controllo statico |
| Script consolidato | **IMPLEMENTATO** localmente |
| Preflight dimensionale | **DA FARE** |
| Misurazione RSS | **DA FARE** |
| Cold copy | **BLOCCATO** |
| Adapter reale | **BLOCCATO** |
| Certificazione runtime | **BLOCCATO** |

Non sono assegnati gli stati **VALIDATO runtime**, **INTEGRATO** o
**CERTIFICATO**.

## Decisione contrattuale sulle attestazioni (2026-11-01)

Il titolare ha approvato espressamente, nel solo perimetro documentale,
l'alternativa B. Il risultato del futuro preflight deve essere descritto
mediante quattro attestazioni indipendenti:

1. `dimensional_collection_status`: `complete`, `incomplete` oppure
   `indeterminate`. `complete` richiede evidenze positive, integre,
   attribuibili e verificabili per tutte le misure obbligatorie; non può essere
   dedotto dal solo exit code `2`.
2. `structural_assessment`: separa `completeness`
   (`complete|incomplete|indeterminate`) e `outcome`
   (`favorable|unfavorable|not_assessable`). Una valutazione completa e
   sfavorevole non autorizza alcuna promozione della capacità.
3. `quota_verification_status`: distingue verifica effettiva, mancata verifica
   e non applicabilità. La verifica deve coprire tutti i domini applicabili;
   `not_applicable` richiede evidenza positiva. Derived 05 non attribuisce
   autonomamente `VERIFIED`.
4. `capacity_readiness_status`: `verified_favorable`,
   `verified_unfavorable`, `incomplete` oppure `indeterminate`.
   `verified_favorable` richiede tutte le dipendenze obbligatorie complete,
   favorevoli e verificabili.

`verified_unfavorable` può essere attribuito in presenza di una condizione
bloccante positivamente dimostrata, completa, attribuibile e conclusiva, anche
quando altre dipendenze rimangono incomplete, purché tali dipendenze non
possano invalidare il blocco né modificarne la conclusione. L'esito non
implica la verifica completa delle altre attestazioni.

Timeout, output parziale, interruzione, misure non affidabili o attribuzione
incerta non possono essere trasformati in esiti negativi verificati. L'exit
code `2` è ammesso per una raccolta informativa non promuovibile, ma non prova
da solo completezza, integrità o attribuzione. L'alternativa A resta quindi
solo informativa; l'alternativa C resta necessaria per una futura verifica
effettiva delle quote.

Nessuna attestazione, singola o combinata, autorizza la cold copy. La decisione
è esclusivamente documentale e non autorizza preflight, wrapper, SSH/VPS,
controlli privilegiati, misurazioni RSS, snapshot, cold copy o deploy.

Formalizzazione documentale del contratto B: **ESEGUITO** con il commit che
include questa sezione. Preflight dimensionale e misurazione RSS restano
**DA FARE**; cold copy, adapter reale e certificazione runtime restano
**BLOCCATO**.
