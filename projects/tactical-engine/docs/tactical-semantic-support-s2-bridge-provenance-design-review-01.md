# RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-DESIGN-REVIEW-01

## Perimetro e riconciliazione

Revisione statica indipendente del design dell'adattatore Spatial V1 dedicato,
sulla baseline GitHub
`b2b82fd9ce90b203e1cf6d7b5ae5ecca69373c75`. HEAD locale e remoto, branch e
working tree erano conformi e non risultava una revisione equivalente già
conclusa. Sono stati confrontati TODO, registro, design, closeout forense,
report runtime, bridge V2, S2, i due contratti NLI, i due runner e i test
pertinenti. Nessun test, import applicativo, inferenza o runtime è stato eseguito.

## Evidenze del percorso attuale

- `v5_tactical_semantic_support_s2_nli_v2_bridge.py:67-86` produce sempre il
  descriptor storico V2; `:89-106` produce la rationale storica V2; `:125-130`
  accetta qualunque callable e non ne dimostra l'identità.
- Il runner Spatial importa il bridge V2 a riga 17, importa esplicitamente il
  contratto Spatial a riga 231, crea la closure Spatial a righe 247-250 e la
  passa al bridge V2 a riga 251. Il routing effettivo è Spatial, mentre la
  provenance annidata resta V2.
- Il runner storico usa lo stesso bridge a riga 220, con callable V2 creato a
  righe 216-219. Questo percorso deve restare invariato.
- S2 riduce il descriptor a `kind`, `name`, `version` e digest canonico di
  `config` (`v5_tactical_semantic_support_s2.py:30-42`), richiede esattamente
  `label` e rationale non vuota (`:166-173`), contiene le eccezioni del judge
  (`:152-176`) e imposta sempre `promotion_authorized=false` (`:45-63`).
- Il digest del record include identità del judge, righe evidence e rationale
  (`:67-74`); `verify_assessment()` ricalcola identità e record (`:191-227`).

I soli chiamanti applicativi di `build_bridge()` sono il runner V2 storico e il
runner differenziale Spatial. Gli altri riferimenti sono test. Dual output e S2
consumano judge e descriptor iniettati, ma non costruiscono il bridge.

## Valutazione dell'alternativa B

L'adattatore Spatial dedicato è la scelta con superficie e rischio minori: un
nuovo modulo e il solo collegamento del runner Spatial possono correggere la
provenance senza modificare file, API, normalizzazione, rationale o runner V2.
Non cambia routing, prompt, label, evidence o politica di non-promozione.

L'interfaccia proposta

```python
def build_bridge(nli_judge, nli_config, contract_descriptor):
    """Build an inert Spatial V1 bridge; no inference during construction."""
```

è sufficiente come boundary di dependency injection, ma non può dimostrare da
sola l'identità del callable. `callable(nli_judge)` prova soltanto
l'invocabilità; una closure può dichiarare qualsiasi nome/configurazione. Anche
`__module__`, `__qualname__`, introspezione o confronto nominale offrirebbero una
garanzia fragile e falsa per closure, wrapper e `partial`.

La rettifica minima è distinguere esplicitamente:

1. **identità dichiarata**: descriptor/config esatti e content-addressed;
2. **binding verificabile staticamente**: il runner importa esplicitamente il
   modulo Spatial e costruisce l'unica closure che invoca
   `spatial_nli.judge_pair()`;
3. **identità runtime non attestata dal bridge**: il generico oggetto Python non
   è autenticato dal solo adapter.

Il design non deve affermare che il bridge autentica il callable. Deve invece
vincolare descriptor e configurazione, rifiutare ogni incoerenza e affidare la
prova del binding ai test statici/differenziali del runner. Nessun controllo
nominale sul callable è richiesto.

## Rettifiche obbligatorie

### M1 — Identità dichiarata distinta da identità verificata

- **Classificazione:** MAGGIORE.
- **File/funzioni future:** nuovo
  `v5_tactical_semantic_support_s2_spatial_v1_bridge.py::build_bridge()` e
  `run_tactical_semantic_support_s2_spatial_relation_differential_v1.py::main()`.
- **Evidenza:** il bridge attuale verifica soltanto `callable()` alle righe
  125-129; la closure del runner non porta un'identità autenticabile.
- **Conseguenza:** registrare `callable_identity` come verificata dal bridge
  produrrebbe una garanzia inesistente.
- **Correzione minima:** denominare il campo come identità dichiarata del
  contratto, documentare il limite, validarlo contro costanti Spatial e provare
  il binding effettivo mediante import/call graph e test del runner. La
  costruzione deve restare inerte e senza fallback.

### M2 — Schemi esatti e validazione al momento della costruzione

- **Classificazione:** MAGGIORE.
- **File/funzione futura:** nuovo bridge Spatial, `build_bridge()`/`descriptor()`.
- **Evidenza:** il design richiede soltanto un dict JSON-canonicalizzabile e una
  conformità descrittiva; il contratto reale Spatial restituisce anche
  `base_contract`, mentre non sono definiti set esatti di chiavi o schema della
  configurazione runtime.
- **Conseguenza:** campi mancanti, inattesi o valori incoerenti potrebbero essere
  content-addressed e apparire come provenance valida.
- **Correzione minima:** definire e applicare prima di restituire il bridge:
  - `contract_descriptor` dict con chiavi esatte `contract_id`, `version`,
    `base_contract`, `labels`, `instruction_sha256`, `selection`;
  - valori esatti `nli_spatial_relations_v1`, `1.0`,
    `shadow_nli_v2_inference`, tre label canoniche nell'ordine contrattuale,
    digest congelato e `explicit_import_only`;
  - `nli_config` dict con chiavi esatte del runner (`judge`, `model`,
    `ollama_url`, `timeout_seconds_per_call`, `max_tokens`, `temperature`,
    `num_ctx`, `think`, `retry`, `repair`), tipi rigorosi e valori invarianti
    approvati; `judge` deve essere la dichiarazione Spatial esatta;
  - rifiuto di campi mancanti/inattesi, bool accettati come int, valori non
    serializzabili e incoerenze fra descriptor/config;
  - copia canonica difensiva delle strutture validate.

Gli errori di costruzione devono sollevare `BridgeContractError` prima di ogni
valutazione e non produrre record. Le eccezioni del callable durante la
valutazione restano contenute da S2 come `judge_error:<tipo>` e producono
`not_evaluable`; output malformati producono lo stesso esito tramite errore del
bridge. Errori di programmazione fuori da questi boundary restano non
recuperabili e non devono avere fallback.

## Osservazioni minori

### m1 — Nota tecnica della rationale

- **Classificazione:** MINORE.
- **Evidenza:** S2 richiede una stringa non vuota; il judge Spatial restituisce
  soltanto una label.
- **Correzione:** congelare una costante che dica esplicitamente
  `Adapter-generated technical provenance notice (not verdict rationale): ...`.
  Il testo non deve attribuire reasoning o motivazione al modello. Il
  `rationale_mode` proposto è coerente e deve restare stabile.

### m2 — Stabilità della proiezione condivisa

- **Classificazione:** MINORE.
- **Evidenza:** riusare `project_claim()` mantiene oggi la proiezione identica,
  ma crea coupling con il file V2.
- **Correzione:** importare solo `project_claim`, `NLI_LABELS` e
  `BridgeContractError`, vietare fallback/copia divergente e bloccare la
  proiezione con un test di equivalenza byte-per-byte. Qualunque futura modifica
  della proiezione V2 richiederà revisione esplicita del bridge Spatial.

Nessuna criticità BLOCCANTE è stata rilevata.

## Compatibilità S2 e V2

Il nuovo bridge può restituire esattamente `{"label": ..., "rationale": ...}`;
le tre label coincidono con `S2.LABELS`, la rationale tecnica è non vuota e S2
continua ad aggregare label, contenere eccezioni e vietare promozione. Nessuna
modifica a S2 è necessaria.

L'alternativa B lascia byte-invariati bridge, descriptor, normalizzazione,
rationale, test e runner V2. Il riuso limitato della proiezione è accettabile con
il vincolo di stabilità sopra descritto. Non emerge alcun motivo per modificare
il percorso storico.

## Provenance Spatial corretta

Il futuro descriptor deve distinguere:

- adapter: `shadow-nli-spatial-v1-s2-bridge`;
- contratto dichiarato: `nli_spatial_relations_v1` 1.0;
- callable dichiarato: `shadow_nli_spatial_relations_v1_inference.judge_pair`;
- instruction digest congelato;
- configurazione runtime canonica;
- provenienza label: output canonico del contratto Spatial;
- rationale mode: nota tecnica generata dall'adapter, non reasoning.

Il nome `shadow-nli-v2-s2-bridge` e il valore
`shadow_nli_v2_inference.judge_pair(claim,evidence)` non devono comparire come
identità del judge Spatial. Il legittimo `base_contract` V2 e gli import tecnici
condivisi non sono identità del judge e possono rimanere.

## Verifica dei digest

La matrice del design è corretta:

- il plan fingerprint del runner Spatial usa activity ID, fixture digest, case
  IDs e contract descriptor (`run_*spatial*:114-119`), non il bridge descriptor;
- fixture, Gold, contratto, instruction digest e plan fingerprint restano
  invariati;
- bridge, runner, descriptor, record e artefatti V2 storici restano invariati;
- il JSON Spatial storico resta immutato a SHA-256
  `a06ba357471681f2ac047af9cff8293d23e75f1c8c8e364f1b14fc4990f8c42d`;
- nei soli record Spatial futuri cambiano legittimamente identità/config digest
  del judge, nota tecnica, `record_sha256` e digest del nuovo report.

S2 calcola `config_sha256` sul JSON canonico del descriptor config e
`record_sha256` sull'intero record con il proprio campo digest posto a `null`;
pertanto le variazioni indicate sono effettivamente content-addressed.

## Piano differenziale rettificato

Il piano futuro deve comprendere, senza rieseguire campagne storiche:

1. blob/hash del bridge V2 e runner V2 invariati;
2. import e costruzione Spatial inerti, con spy che prova zero chiamate;
3. descriptor Spatial esatto e copia difensiva;
4. matrice di descriptor/config mancanti, inattesi, mal tipizzati e incoerenti,
   tutti rifiutati alla costruzione;
5. prova esplicita che l'identità callable è dichiarata e che il runner collega
   soltanto `spatial_nli.judge_pair`, senza pretendere introspezione autenticante;
6. proiezione claim/evidence byte-identica;
7. tre label canoniche propagate senza rimappatura;
8. output malformati e label sconosciute fail-closed;
9. eccezioni del judge convertite da S2 in `not_evaluable` con reason code;
10. nota tecnica stabile, non semantica e senza stringa storica V2;
11. `judge.config_sha256` e `record_sha256` verificati indipendentemente;
12. `promotion_authorized=false`, S1 e output autorevoli invariati;
13. nuovo adapter selezionato soltanto dal runner Spatial;
14. fixture, Gold, contratto, instruction digest, plan fingerprint e JSON
    storico invariati;
15. controllo che mutare descriptor dopo la costruzione non alteri la provenance
    interna;
16. distinzione testata fra errore di costruzione e errore di valutazione.

I punti 4, 5, 15 e 16 precisano verifiche non sufficientemente esplicite nel
design originale.

## Verdetto e stati

**DESIGN APPROVATO CON RETTIFICHE.**

L'alternativa B è valida e non presenta blocchi architetturali, ma le due
rettifiche maggiori sono obbligatorie prima dell'implementazione: nessuna falsa
attestazione dell'identità del callable e schemi/validazione di costruzione
esatti e fail-closed. Le due osservazioni minori sono criteri di accettazione
raccomandati e non richiedono una nuova architettura.

Revisione **ESEGUITO**; design **VALIDATO** soltanto con le rettifiche sopra;
implementazione **DA FARE**. Gate semantico, integrazione e certificazione
restano **BLOCCATO**.

Unico prossimo passo: decisione del titolare sull'implementazione offline
dell'alternativa B incorporando M1 e M2, senza nuovi cicli di design equivalenti.
