# RAG V5 Dual Blocker — verifica read-only runtime-03

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME03-READONLY-READINESS-01`.
Data: 2026-11-10, Europe/Rome.

## Attività → Script → Commit → Report

Ripresa della sola verifica read-only degli artefatti già presenti sulla VPS,
dopo il ripristino SSH v3. Il backup cifrato resta separato e **DA FARE**;
non è un prerequisito bloccante per questa ricognizione.

TODO, Experiment Register e piano nuovo PC riconciliati con GitHub e codice.
Baseline documentale iniziale locale/remoto:
`b180f97233496602168bea975f1a55e25940afcf`, branch
`codex/tactical-state-contract-v1`, working tree locale pulito.
Baseline applicativa prevista per la futura prova invariata:
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`, comprendente `56a7b72`.

Script: tre connessioni SSH batch con identità v3 e controllo host rigoroso;
Python stdlib inline per lettura, hash e selezione di righe; Git
`--no-optional-locks` per sola lettura dello stato. Nessun file di script
trasferito o scritto sulla VPS; nessun modulo applicativo importato.
Commit: esclusivamente documentale, identificabile dalla storia di questo
report, aggiornato insieme a TODO e registro.

Questa verifica accerta disponibilità e identità attuali degli artefatti dopo
il cambio PC e legge il wrapper prima del riuso post-patch. Non ripete un test
generativo, una suite offline o l'analisi forense del contenuto Qwen. I 37/37
risultati già registrati non sono stati rieseguiti.

## Wrapper storico verificato

Percorso:
`/home/football/.local/share/football-data-lab/runtime-wrappers/spatial-v2-extraction-locator-q3-04-runtime-03-approved.sh`.

| Proprietà | Osservato |
|---|---|
| Tipo | file regolare, non symlink |
| Proprietario/gruppo | `football:football` |
| Modo | `0600` |
| Dimensione | 45.964 byte |
| SHA-256 | `ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57` |

Identità coincidente con i report storici. Letti i parametri e i rami di
classificazione pertinenti senza eseguire il wrapper o i suoi blocchi Python.

Parametri effettivi confermati da sorgente, `config.json` e
`request_payload.json` storici:

- modello `qwen3.5:9b`, digest atteso nel wrapper
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
- `temperature=0`, `num_ctx=4096`, `num_predict=2048`;
- `think=false`, `stream=false`, schema extraction come oggetto nel payload;
- timeout HTTP effettivo 360 s tramite opt-in; il valore base passato al judge
  resta 180 s e viene sostituito dall'opt-in;
- supervisore `timeout --signal=TERM --kill-after=15s 450s`;
- una sola chiamata di trasporto, nessun retry/repair/fallback;
- `promotion_authorized=false` e lock comune
  `/home/football/.local/share/football-data-lab/runtime-locks/spatial-v2-extraction-locator.lock`.

Il digest modello è qui un'identità storica/attesa: non è stata effettuata
una nuova chiamata Ollama per attestarne lo stato corrente.

Il file inizia con `ssh football-vps 'bash -s' <<'BASH'`: contiene anche il
launcher SSH. Nel futuro adattamento va conservata e revisionata la distinzione
fra launcher e corpo remoto; non è stato invocato come script Bash sulla VPS.

## Artefatti storici e inventari

Directory reale presente:
`/home/football/.local/share/football-data-lab/runtime-artifacts/spatial-v2-extraction-locator-q3-04-runtime-03`.

Verificati tutti gli hash dichiarati nei tre inventari, limitando la lettura
a file regolari diretti della directory, senza seguire symlink o percorsi
esterni. Non è stato eseguito il finalizzatore.

| Inventario | Entry verificate | SHA-256 inventario |
|---|---:|---|
| `hashes.sha256` | 23 | `110a288d9cf9ee9e6133121c481cb6baee1031c65d10f9911034546c27cd2dfd` |
| `attempt_state.sha256` | 1 | `209127f7068636c5e47f271ac7710ef23cc495e961cff9bfdd6318e864706832` |
| `hashes.sha256.digest` | 1 | `0317eaac9ecf7e56444eb3267ea4c4c4c2528ecdef6d4e31d2d2be1087437996` |

Stato storico riconfermato, senza nuova valutazione del raw:
`finalization_complete=true`, `completed_fail_closed`, una generazione completa,
una chiamata, 142,340508 s, processo generativo exit 0 e wrapper exit 80;
`E_EXTRACTION_LOCALIZATION_NOT_UNIQUE`, `not_evaluable`, label osservata e
semantic match nulli. Gold `contradicted`. `witness.json`, `validation.json`
e `finalization_errors.log` assenti, coerentemente con quel percorso.

## Snapshot dei percorsi

- Checkout operativo `/opt/football-data-lab` a
  `1a80fe0c6261b10f748a36c2b4fd96e8e2253971`, common dir `.git`.
  Nessuna modifica tracked segnalata; presenti 17 percorsi non tracciati di
  evaluation/ledger/indici, lasciati intatti. Il checkout operativo non viene
  qualificato come completamente pulito.
- Staging storico `spatial-v2-extraction-locator-db3ad66`: directory reale,
  HEAD `db3ad66f6254f43bcc625b605b68f2f181c1af69`, status vuoto, common dir
  `.git`. Non aggiornato né riutilizzato per il post-patch.
- Target proposto `staging/spatial-v2-dual-blocker-13814c2`: assente anche
  come symlink.
- Target proposto `runtime-artifacts/spatial-v2-extraction-locator-q3-04-runtime-04`:
  assente anche come symlink.

L'assenza riguarda questi percorsi letterali, non costituisce un inventario
universale di tutti gli esperimenti possibili. La ricognizione non è un
preflight runtime completo: non controlla concorrenza live, lock acquisibile,
versione corrente Ollama, disponibilità modello o dipendenze applicative.

## Adattamento necessario del verificatore

**Rilievo statico nuovo**, non un difetto riaperto del locator o del motore:
il verificatore incorporato nel wrapper runtime-03 non gestisce il nuovo
boundary post-patch `E_EXTRACTION_SEMANTIC_INCONSISTENT`.

Catena verificata nel sorgente originale:

1. Righe 1132–1140: calcola soltanto `extraction_shape_errors()` per scegliere
   fra schema invalido e extraction strutturalmente valida.
2. Righe 1195–1220: una extraction con shape valido entra nel ramo E2;
   `verify_materialization()` post-patch ricostruirebbe correttamente anche
   il nuovo boundary semantico.
3. Righe 1226–1234: qualunque `localization.status=not_evaluable` richiede però
   esattamente `E_EXTRACTION_LOCALIZATION_NOT_UNIQUE`. Il boundary semantico
   è quindi respinto dalla verifica del contenuto.
4. Righe 1382–1386: una simile verifica fallita conduce a
   `E_CONTENT_VERIFICATION`, `attempt_status=incomplete`, exit 100.

Questa è una deduzione statica condizionale, non un nuovo risultato runtime.
Il risultato applicativo resterebbe fail-closed e conservato, ma il wrapper
non descriverebbe correttamente l'esito: non basta sostituire SHA, baseline
e attempt ID per poterlo riusare dopo la patch.

Nella futura copia locale, prima del ramo di localizzazione, occorre distinguere
shape valido con errori semantici da localizzazione fallita: verificare il
boundary specifico e i `details` contro `extraction_semantic_errors()`,
assenza di witness/validation, provenance diagnostica senza record di
localizzazione, label osservata/semantic match nulli e non promozione.
Non riclassificare tale fallimento come successo semantico. Il ramo positivo,
il locator e il validatore finale restano invariati.

Questo delta del solo verificatore wrapper, oltre a identità/percorsi e
telemetria, dovrà essere revisionato e verificato offline nel suo perimetro
nuovo prima di autorizzare una generazione. Non richiede ripetere le suite
37/37 già concluse né modificare il motore semantico. Nessun adattamento o
nuovo test è stato eseguito in questa ricognizione.

## Risultato → Decisione → Stato

Verifica read-only **ESEGUITO**; identità wrapper e integrità degli artefatti
storici **VALIDATO** nel perimetro osservato. Parametri effettivi disponibili
per riuso; backup cifrato **DA FARE**, separato. Nessun blocco SSH residuo.

Prossimo passo proposto: preparare localmente la copia runtime-04 adattando
anche il verificatore, con diff e inventario propri, senza eseguirla né
trasferirla. Stato di tale preparazione **DA FARE**, da autorizzare come
passaggio distinto. Staging indipendente a `13814c2` **DA FARE**; creazione
e trasferimenti non autorizzati da questa ricognizione.

Nessuna esecuzione wrapper, Qwen, test applicativo, download di corpus,
Chroma, modifica VPS, staging, panel, servizio, merge o deploy. La lettura
SSH del sorgente e degli artefatti non costituisce trasferimento/installazione
di un wrapper o preparazione dello staging. Contraddizioni e accuratezza
generativa, runtime post-patch, Gate, integrazione e certificazione
restano **BLOCCATO**.
