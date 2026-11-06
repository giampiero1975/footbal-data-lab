# RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-IMPLEMENTATION-REVIEW-01

## Baseline e metodo

Revisione indipendente esclusivamente statica della baseline GitHub
`33b5c7ad5a69513e7d4df7cbc26e937fccf16bdc`. Branch, HEAD locale/remoto e
working tree erano conformi; non risultava una revisione equivalente già
conclusa. Sono stati letti codice, test, diff, design, review, report di
implementazione e closeout forense. Nessun test, import applicativo, modello,
inferenza o runtime è stato eseguito.

File/funzioni revisionati integralmente:

- nuovo bridge Spatial: validatori, descriptor, normalizzazione, classe e
  `build_bridge()`;
- runner Spatial: import, closure e costruzione;
- 8 test del bridge e 6 test del runner;
- bridge/runner V2, S2 e i due contratti NLI come dipendenze.

## M1 — identità e binding

**A — dimostrato:** il descriptor dichiara
`shadow_nli_spatial_relations_v1_inference.judge_pair`, specifica
`runtime_callable_authentication=not_performed_by_bridge` e non usa
`__module__`, `__qualname__` o introspezione (`v5_*spatial_v1_bridge.py:110-131`).

**A — dimostrato dal codice:** il runner importa il nuovo bridge a riga 17,
importa il modulo Spatial a riga 231, costruisce una closure che chiama
`spatial_nli.judge_pair()` alle righe 247-250 e passa quella closure soltanto al
bridge Spatial alle righe 251-252. Non esiste fallback al judge V2.

**B — fortemente supportato come evidenza di test:** il test del runner verifica
gli import e l'assenza dei nomi V2 tramite AST, ma non ispeziona il target della
`Call` dentro la closure e non usa uno spy sul `main()`. Quindi il binding è
dimostrato dalla lettura del codice, non dal test pubblicato. Inoltre il campo
`binding_evidence` del descriptor è una dichiarazione prodotta dal bridge, non
una prova autonoma del call graph.

## M2 — schema e fail-closed

**A — dimostrato:** set esatti di chiavi per descriptor e config, valori
congelati, tipi rigorosi della config, distinzione bool/int, confronto col valore
atteso e validazione prima della costruzione (`:68-107`, `:157-162`). Dati non
serializzabili sono convertiti in `BridgeContractError`; non esistono fallback.

**A — dimostrato:** mutazioni degli input e della copia restituita dalla property
non cambiano il descriptor interno nel normale uso (`:147-149` e test 02).

**Difetti:** la validazione del descriptor canonicalizza prima di verificare i
tipi dei campi, e il dict interno resta direttamente mutabile nonostante la
docstring lo definisca immutabile. Sono dettagliati nelle criticità M1/M2 sotto.

## Boundary S2

Il bridge accetta soltanto una label stringa appartenente a `NLI_LABELS` e
restituisce esattamente `label`/`rationale` (`:134-137`). `project_claim()` è
chiamata prima del judge e l'evidence è passata come secondo argomento senza
normalizzazione (`:151-154`). Import/costruzione non chiamano il judge.

S2 richiede shape esatta, label canonica e rationale non vuota; contiene ogni
eccezione del bridge/judge come `judge_error:<tipo>`, produce `not_evaluable` e
mantiene `promotion_authorized=false`. Non risultano retry, repair o fallback.
Gli errori di costruzione avvengono prima di S2 e non producono record; gli
errori di valutazione vengono contenuti da S2. **A — dimostrato.**

## Proiezione, provenance e rationale

Il nuovo modulo importa direttamente `project_claim`, `NLI_LABELS` e
`BridgeContractError` dal bridge V2 e non duplica la proiezione. Il test 04
confronta la stringa effettivamente ricevuta dallo stub con il risultato della
funzione storica sullo stesso payload, non soltanto l'identità della funzione.
Ordine claim/evidence e metadati restano invariati. **A — dimostrato.**

Il descriptor distingue adapter, callable dichiarato, mancata autenticazione,
binding dichiarato, contratto, versione, instruction digest, config, label
provenance e rationale mode. `base_contract=shadow_nli_v2_inference` è un
riferimento legittimo; il judge non è identificato come bridge V2.

`TECHNICAL_NOTICE` è costante, non spiega il verdetto, dichiara esplicitamente
`not verdict rationale` e viene inserita nella riga evidence e quindi nel digest
del record. **A — dimostrato.**

## Compatibilità V2 e integrità

SHA-256 verificati staticamente:

| Artefatto | SHA-256 osservato | Esito |
|---|---|---|
| bridge V2 | `79a4cc87c0d59e087a69d295a199f7f646c4ecb42194cf45531fd96dba09f515` | conforme |
| runner V2 | `3c5818142b0a9ac1c689a1cb3c5523fae13883d95b10544963842b97134cbf91` | conforme |
| JSON Spatial storico | `a06ba357471681f2ac047af9cff8293d23e75f1c8c8e364f1b14fc4990f8c42d` | conforme |

Il diff del commit modifica soltanto nuovo bridge, due test, due righe
funzionali del runner Spatial e documentazione. Gold, fixture, contratto,
instruction digest, runner/bridge V2 e JSON storico non sono nel diff.
Il plan fingerprint storico dipende dal contract descriptor e non dal nuovo
bridge descriptor. **A — dimostrato.**

Il nuovo import condiviso carica un modulo V2 inerte che definisce funzioni e
costanti senza avviare runtime; il percorso V2 non importa il nuovo adapter.
Compatibilità V2 **A — dimostrato** nel perimetro statico.

## Revisione critica dei 14 test

| Test | Proprietà effettiva | Copertura |
|---|---|---|
| bridge 01 | costruzione inerte; nome e identità dichiarata | buona; non autentica il callable, correttamente |
| bridge 02 | mutazioni input e copia esposta | buona nel percorso pubblico; non prova `_descriptor` diretto |
| bridge 03 | chiavi config mancanti, extra, alcuni tipi/valori; descriptor missing/extra/digest | parziale: non prova tipo `labels`, non serializzabili o tutti i valori descriptor |
| bridge 04 | stringa proiettata ed evidence effettive | buona; confronto con funzione storica sul medesimo payload |
| bridge 05 | tre label e nota tecnica | buona |
| bridge 06 | quattro output malformati | rappresentativa, non esaustiva |
| bridge 07 | eccezione judge, `not_evaluable`, reason code, non-promozione | buona |
| bridge 08 | hash config e record ricalcolati con `hashlib`/JSON canonico | indipendente dalla funzione digest S2, buona |
| runner 01 | ruoli, label e identità dataset | buona |
| runner 02 | tre casi, nessun Gold nel payload, non-promozione | buona sull'orchestrazione iniettata |
| runner 03 | arresto al primo errore e `not_evaluable` | buona |
| runner 04 | digest/label alterati fail-closed | buona |
| runner 05 | import Spatial/assenza import V2 e opt-in | insufficiente per provare il target della closure |
| runner 06 | unica evidenza storica V2 attribuibile | buona, fuori dal core del nuovo bridge |

I test digest non confrontano valori prodotti esclusivamente dalla stessa
funzione: usano `hashlib` e serializzazione esplicita. I 14 test non contengono
invece asserzioni sugli SHA dei due file V2 o del JSON storico; tali invarianti
sono documentati e verificabili dal repository, ma non sono protetti dalla suite
differenziale dichiarata.

## Criticità

### M1 — tipo del descriptor non rigorosamente validato

- **Classificazione:** MAGGIORE.
- **File/funzione:** `v5_tactical_semantic_support_s2_spatial_v1_bridge.py`,
  `_validate_contract_descriptor()` righe 68-83.
- **Evidenza:** una `labels` tuple JSON-serializzabile viene trasformata in list
  da `_canonical_copy()` e può quindi uguagliare il valore atteso. La shape è
  corretta, ma il tipo originale non viene verificato; ciò contraddice M2.
- **Conseguenza:** input non conforme al tipo contrattuale può produrre
  provenance apparentemente valida.
- **Correzione minima:** verificare prima della canonicalizzazione `type(value)
  is dict`, tipi esatti di ogni campo e `type(labels) is list` con elementi
  `str`, poi confrontare ordine e valori. Aggiungere un test mirato con tuple e
  almeno un tipo non conforme per campo composito.

### M2 — descriptor interno non realmente immutabile

- **Classificazione:** MAGGIORE.
- **File/classe:** stesso modulo, `SpatialV1S2Bridge` righe 140-162.
- **Evidenza:** `@dataclass(frozen=True)` impedisce la riassegnazione
  dell'attributo, non la mutazione annidata di `bridge._descriptor`, che resta un
  dict accessibile. La property protegge soltanto la copia restituita.
- **Conseguenza:** dopo la validazione un chiamante può mutare direttamente la
  provenance interna e ottenere un descriptor alterato senza nuova validazione.
- **Correzione minima:** conservare internamente una rappresentazione canonica
  immutabile (per esempio JSON string) e ricostruire una copia nella property,
  oppure una struttura profondamente immutabile. Aggiungere il test di mutazione
  diretta/post-costruzione corrispondente.

### M3 — prova automatica del binding e degli hash incompleta

- **Classificazione:** MAGGIORE per il closeout probatorio, non per il call graph
  osservato.
- **File/test:**
  `test_run_tactical_semantic_support_s2_spatial_relation_differential_v1.py::test_05`.
- **Evidenza:** il test verifica soltanto gli import AST; non asserisce che la
  closure chiami `spatial_nli.judge_pair`. Nessun test verifica gli SHA V2/JSON
  dichiarati.
- **Conseguenza:** una futura regressione nel target della closure o negli
  artefatti storici potrebbe lasciare verdi i 14 test.
- **Correzione minima:** aggiungere una verifica AST del target esatto della
  `Call` o uno spy locale sul binding del runner, più asserzioni SHA sui tre
  artefatti congelati. Nessuna inferenza o suite storica è necessaria.

### m1 — nome `binding_evidence`

- **Classificazione:** MINORE.
- **Evidenza:** il valore è una dichiarazione del bridge, non evidenza allegata.
- **Conseguenza:** possibile sovrainterpretazione della provenance.
- **Correzione facoltativa:** rinominarlo `declared_binding_mode` oppure
  documentarlo esplicitamente come dichiarazione non autenticante. Se rinominato,
  aggiornare i digest sintetici attesi.

Nessuna criticità BLOCCANTE è stata rilevata.

## Matrice A/B/C

| Conclusione | Livello |
|---|---|
| routing effettivo del codice verso Spatial | A |
| nessun fallback/retry/repair e costruzione inerte | A |
| boundary S2 fail-closed e non-promozione | A |
| proiezione/evidence invariata | A |
| provenance/rationale Spatial content-addressed | A |
| hash V2 e JSON storico conformi | A |
| 14 test riportati come PASS nel report precedente | B, non rieseguiti per divieto |
| test sufficienti a provare binding e immutabilità completa | non dimostrato |
| autenticità runtime del callable | non attestata per design, correttamente |
| affidabilità semantica o runtime | C/fuori perimetro |

## Verdetto e stati

**IMPLEMENTAZIONE APPROVATA CON RETTIFICHE.**

L'architettura e il routing sono corretti, ma M1 e M2 violano due proprietà
fail-closed esplicitamente richieste e M3 lascia incompleta la prova automatica
del binding/immutabilità storica. Sono correzioni circoscritte, senza necessità
di riprogettare o modificare S2/V2.

Revisione statica **ESEGUITO**. Implementazione esistente **IMPLEMENTATO**, ma
closeout offline definitivo **BLOCCATO** fino alle rettifiche e alla loro
verifica mirata. Gate semantico, integrazione e certificazione restano
**BLOCCATO**.

Unico prossimo passo: decisione del titolare su una remediation offline minima
di M1-M3, senza inferenze, Gate o modifiche ai percorsi V2/S2.
