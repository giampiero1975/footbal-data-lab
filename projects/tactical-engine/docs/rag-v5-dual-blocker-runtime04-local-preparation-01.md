# RAG V5 Dual Blocker — preparazione locale wrapper runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-LOCAL-PREPARATION-01`.
Data: 2026-11-10, Europe/Rome.

## Attività

Preparata esclusivamente una copia locale distinta del wrapper runtime-03,
con diagnostica del nuovo boundary semantico e identità post-patch. Nessun
wrapper, generazione, preflight applicativo o staging remoto eseguito.

Prima delle scritture: TODO ufficiale, Experiment Register e report
`rag-v5-dual-blocker-runtime03-readonly-readiness-01.md` letti e riconciliati;
branch `codex/tactical-state-contract-v1`, working tree pulito, HEAD locale
e GitHub `cf6b63d21290bb77887958338e7ce8b6a2f34f79` coincidenti.
La lettura locale dei documenti corrisponde alla revisione GitHub verificata.

Baseline applicativa obbligatoria:
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.
Patch `56a7b72135595e99a98ff2fb5b1bcc3d6a0c9ebf` inclusa; nessun delta
applicativo fra baseline e HEAD documentale. Non sono emerse divergenze di
baseline, branch o sorgente originale.

## Script

Artefatti versionati in `operations/runtime-wrappers/`:

- `spatial-v2-extraction-locator-q3-04-runtime-03.original.sh`: originale;
- `spatial-v2-extraction-locator-q3-04-runtime-04.sh`: copia nuova;
- `prepare_runtime04_wrapper.py`: trasformazione locale con conteggi esatti,
  hash sorgente obbligatorio e creazione esclusiva senza sovrascritture;
- `runtime03-to-runtime04.diff`: diff completo rispetto all'originale;
- `test_runtime04_wrapper_delta.py`: controlli nuovi del delta;
- README con giustificazione registrata prima di eseguire le verifiche;
- attributi Git per conservare i byte LF dei wrapper e del diff. Le righe
  di contesto vuote del diff unificato sono dati, non whitespace del sorgente.

### Provenienza e identità

Sorgente remoto già verificato, recuperato con una sola lettura SSH senza
eseguirlo o modificarlo:
`/home/football/.local/share/football-data-lab/runtime-wrappers/spatial-v2-extraction-locator-q3-04-runtime-03-approved.sh`.

| Artefatto | Byte | SHA-256 |
|---|---:|---|
| Originale runtime-03 | 45.964 | `ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57` |
| Nuova copia runtime-04 | 47.755 | `abf6db3060b68cbc1e5d9e1c28ea13e2cb3dbce09f2ae2b5c00f8ec1e7f55f17` |
| Diff completo | 4.667 | `5ed2d8891f3524094f94dbca27e89f2d3a7715e5be7ec92320b09457c372c9bd` |

Identità dell'originale verificata al recupero, dopo la creazione della copia
e sui byte dell'index Git; nuova copia verificata anche nell'index Git.
Nessuna conversione CRLF e nessuna modifica dell'originale.

## Commit

Commit tecnico degli artefatti e dei controlli locali:
`56fba214c6a2d438bf1e1c4383dc920654cfc5c7`.

Report, TODO e registro vengono pubblicati insieme nella stessa sessione con
un commit documentale successivo. Il commit di pubblicazione del report è
rintracciabile tramite:

```text
git log -1 --format=fuller -- projects/tactical-engine/docs/rag-v5-dual-blocker-runtime04-local-preparation-01.md
```

La baseline applicativa del futuro staging resta `13814c2`, distinta dai
commit di preparazione del wrapper e di pubblicazione documentale.

## Report del delta tecnico

Il diff completo è `operations/runtime-wrappers/runtime03-to-runtime04.diff`.
La trasformazione permette soltanto:

1. HEAD atteso da `db3ad66...` alla baseline obbligatoria `13814c2...`;
2. staging futuro indipendente
   `/home/football/.local/share/football-data-lab/staging/spatial-v2-dual-blocker-13814c2`;
3. tre identificativi completi runtime-03 → runtime-04 per directory artefatti,
   stato finale e record generazione;
4. blob inference `8ac93d07341e1079ee3ca6ff98327a8391b7ab5f` ed extraction
   `1a64827b26fb30758773049eedeb342a2bb826b2`, verificati nella baseline;
5. inserimento del ramo diagnostico semantico fra schema invalido e percorso
   di localizzazione/witness, con aggiornamento del solo commento del ramo E2.

Blob del validatore, dataset e relativo hash invariati. Nessuna modifica a
schema, locator, validatore finale, codice applicativo o suite esistenti.

### Boundary semantico

Con shape valido, il verificatore chiama `extraction_semantic_errors()` prima
del ramo di localizzazione. Quando sono presenti errori richiede:

- `evaluation_status=not_evaluable` e reason code esatto
  `E_EXTRACTION_SEMANTIC_INCONSISTENT`;
- `details` identici a quelli calcolati dal precontrollo versionato;
- witness e validation nulli e relativi file assenti;
- provenance diagnostica coerente con i testi originali, stato non valutabile
  e `records=[]`, senza localizzazione inventata;
- ricostruzione completa tramite `verify_materialization()` coincidente con
  result/provenance, inclusi digest e dettagli;
- label osservata e semantic match nulli, invarianti di non promozione.

Classificazione nuova: `fail_closed_extraction_semantic`, exit 80 e successivo
stato finale `completed_fail_closed` con reason code preservato. È un arresto
diagnosticato correttamente, non un successo generativo o semantico.

Restano distinti `fail_closed_extraction_schema`, `fail_closed_localization`
e il percorso con witness/validazione. Un witness valido in discordanza con
Gold mantiene exit 81, senza correzione della label. Nessun repair, fallback,
spostamento di frammenti o sostituzione del contenuto generato.

### Invarianti preservate

Modello `qwen3.5:9b` e digest atteso storico, `num_predict=2048`, contesto
4.096, temperatura 0, think false, HTTP 360 s, timeout esterno 450 s e
kill-after 15 s; lock condiviso storico. Una sola generazione e chiamata di
trasporto, nessun retry/repair/fallback, `promotion_authorized=false`.

Launcher SSH e corpo remoto restano separati dal delimitatore `BASH`.
Finalizzatore, inventari, supervisione e verifica finale dello staging sono
identici salvo l'attempt ID esplicitamente aggiornato. Non sono stati
eseguiti per verificarli: il confronto statico copre la loro invarianza.

## Verifiche locali effettivamente eseguite

Comando della nuova suite, non delle precedenti 37 verifiche:

```text
python -B projects/tactical-engine/operations/runtime-wrappers/test_runtime04_wrapper_delta.py
```

Prima esecuzione: 13 controlli, 12 PASS e un confronto statico respinto perché
il test non normalizzava l'attempt ID autorizzato nel finalizzatore. Corretto
solo quel confronto, senza alterare il wrapper. Motivazione della riesecuzione
registrata nel README prima di rilanciare il solo controllo fallito:

```text
python -B projects/tactical-engine/operations/runtime-wrappers/test_runtime04_wrapper_delta.py Runtime04WrapperDeltaTests.test_generation_lock_timeouts_and_finalization_unchanged
```

Esito differenziale: 1/1 PASS. Insieme finale dei 13 controlli distinti coperto
con esito positivo; gli altri dodici non sono stati ripetuti.

Evidenze dei controlli:

- `bash --noprofile --norc -n` locale su launcher e, separatamente, corpo
  remoto: entrambi PASS, senza esecuzione shell del contenuto;
- cinque blocchi Python incorporati compilati senza esecuzione; solo il
  blocco generazione cambia attempt ID e il verificatore cambia diagnostica;
- originale, trasformazione completa, diff e identità dei blob controllati;
- solo il verificatore estratto eseguito su file JSON sintetici in directory
  temporanee locali, con creazione socket e processi esterni vietata;
- quattro percorsi distinti verificati, nuovo errore comparison incluso;
- reason code errato, details mancanti/alterati, provenance/record alterati,
  witness/validation indebiti e promozioni respinti;
- originale respinge il nuovo boundary mentre la copia lo descrive
  fail-closed; mismatch Gold conserva label osservata e non promuove;
- nessun delta in `scripts/` e `tests/` rispetto alla baseline; `git diff
  --cached --check` PASS e hash dei wrapper presenti nell'index conformi.

Le fixture riusano soltanto costanti e helper dei test già versionati,
estratti staticamente: nessuna suite storica importata o eseguita e nessun
raw runtime-03 ricostruito presentato come originale. Non sono stati eseguiti
launcher, corpo Bash, blocco generativo, finalizzatore o wrapper completo.

## Risultato → Decisione → Stato

Nuovo wrapper **IMPLEMENTATO**; controlli locali nuovi **ESEGUITO**;
preparazione locale **VALIDATO** esclusivamente per il delta osservato.
Originale preservato byte-per-byte e diff completo disponibile.

Limiti: nessun preflight dell'ambiente VPS per questa copia, nessuna verifica
generativa, nessuna dimostrazione di accuratezza o generalizzazione. Gli
inventari futuri non sono stati prodotti sulla VPS; è preservata staticamente
la logica di finalizzazione già presente nel sorgente originale.

Decisione: STOP dopo pubblicazione e verifica documentale. Nessun upload,
creazione staging, trasferimento del nuovo wrapper o inferenza autorizzati.
L'unico recupero remoto è stato la lettura dell'originale espressamente
richiesta. Staging e futuro preflight **DA FARE** con autorizzazione distinta;
runtime post-patch, accuratezza delle contraddizioni, Gate, integrazione e
certificazione restano **BLOCCATO**. Nessun merge, deploy, panel, Chroma,
indice, servizio o checkout operativo modificato.
