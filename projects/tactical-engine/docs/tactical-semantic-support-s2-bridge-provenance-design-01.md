# RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-DESIGN-01

## Obiettivo e baseline

Progettazione esclusivamente offline della rettifica minima di provenance per il
percorso Spatial V1. Baseline GitHub:
`5d1caf239cf9ea0bbe60e2b91e5cde8c815ec6b9`. Nessun codice, test, modello,
artefatto runtime o ambiente operativo e stato modificato.

## Difetto dimostrato

`v5_tactical_semantic_support_s2_nli_v2_bridge.py` accetta un callable generico,
ma costruisce sempre provenance V2:

- `name=shadow-nli-v2-s2-bridge`;
- `nli_contract=shadow_nli_v2_inference.judge_pair(claim,evidence)`;
- rationale fissa `NLI V2 returned...` quando il callable restituisce una label.

Nel Gate Spatial il callable effettivo era
`shadow_nli_spatial_relations_v1_inference.judge_pair`; pertanto routing e label
erano corretti, mentre descriptor e rationale annidati erano fuorvianti. La
rationale fissa e generata dall'adattatore e non e reasoning del modello.

## Mappa dei chiamanti

Chiamanti applicativi effettivi di `build_bridge()`:

1. `run_tactical_semantic_support_s2_first_controlled_runtime_v1.py`: percorso
   storico NLI V2, che deve rimanere invariato.
2. `run_tactical_semantic_support_s2_spatial_relation_differential_v1.py`:
   percorso Spatial V1 che oggi riusa impropriamente il bridge nominalmente V2.

Chiamanti di verifica: test del bridge V2, runner storico e runner Spatial. Il
dual-output e l'adapter S2 ricevono un judge e un descriptor iniettati, ma non
costruiscono direttamente il bridge. Non risultano altri chiamanti applicativi.

## Mappa della provenance

| Campo | Costruttore | Persistenza |
|---|---|---|
| `judge.name`, `judge.version` | descriptor del bridge, ridotto da `_judge_identity()` | record S2 |
| `judge.config_sha256` | hash canonico di `descriptor.config` | record S2 |
| `nli_contract`, callable, labels, rationale mode, config | descriptor completo del bridge | verificabile tramite descriptor/config e relativo hash |
| contratto Spatial ID/version/instruction digest | `shadow_nli_spatial_relations_v1_inference.descriptor()` | report runtime top-level |
| `judge_rationale` | risultato del bridge | riga evidence del record S2 |
| `record_sha256` | `_finish()` in S2 | record S2, include judge identity e rationale |

S2 richiede che il judge restituisca esattamente `label` e una `rationale`
stringa non vuota. Non e quindi possibile usare `null` senza cambiare lo schema
S2, modifica fuori perimetro.

## Alternative

### A — Bridge V2 parametrizzabile

Estendere `build_bridge()` con identita callable/contratto/rationale e default
storici V2.

- Superficie: bridge V2, suoi test e runner Spatial; potenzialmente tutti i
  chiamanti condividono il codice modificato.
- Vantaggio: minore duplicazione e unico adattatore generico.
- Rischio: una regressione nei default, nella validazione o nella normalizzazione
  toccherebbe il percorso V2 gia validato; l'API diventerebbe piu generale del
  bisogno attuale.
- Digest: anche una modifica apparentemente compatibile richiederebbe dimostrare
  che descriptor e risultati V2 restano identici.
- Rollback: revert coordinato del bridge e del runner.

### B — Adattatore Spatial dedicato

Aggiungere un modulo Spatial specifico che riusa dal bridge storico soltanto la
proiezione `project_claim`, le tre label e l'errore contrattuale, mantenendo il
file V2 byte-invariato.

- Superficie: un nuovo modulo, il solo import/build del runner Spatial e test
  differenziali nuovi.
- V2: file, interfaccia, descriptor, rationale, test e runner storico invariati.
- Descriptor: identita Spatial esplicita e non configurabile arbitrariamente.
- Digest: cambiamenti confinati ai futuri record Spatial.
- Rollback: revert del nuovo modulo e del solo collegamento nel runner Spatial.
- Rischio residuo: dipendenza intenzionale dalla proiezione pubblica del bridge
  V2; va bloccata con un test di equivalenza della stringa proiettata.

## Soluzione raccomandata

**Alternativa B**, perche minimizza la superficie e rende impossibile alterare
accidentalmente il comportamento V2. Non viene proposta un'astrazione generale:
esiste un solo secondo contratto che necessita provenance distinta.

Modulo futuro proposto:

`scripts/v5_tactical_semantic_support_s2_spatial_v1_bridge.py`

Interfaccia proposta:

```python
def build_bridge(nli_judge, nli_config, contract_descriptor):
    """Build an inert Spatial V1 bridge; no inference during construction."""
```

Vincoli:

- `nli_judge` callable;
- `nli_config` dict JSON-canonicalizzabile;
- `contract_descriptor` conforme a
  `shadow_nli_spatial_relations_v1_inference.descriptor()` con ID
  `nli_spatial_relations_v1`, versione `1.0`, tre label canoniche, instruction
  SHA-256 valido e selezione esplicita;
- proiezione claim identica a `project_claim()` storico;
- risultato ammesso: sola label stringa canonica, coerente con il judge Spatial
  attuale; output malformati ed eccezioni restano fail-closed;
- nessun routing, retry, repair o fallback aggiuntivo.

Il runner Spatial cambierebbe soltanto import del bridge e chiamata
`build_bridge(call, runtime_config, contract_descriptor)`. Judge, prompt,
parametri e ordine claim/evidence resterebbero invariati.

## Descriptor illustrativi

Gli esempi seguenti sono design, non risultati runtime.

### V2 storico invariato

```json
{
  "kind": "injected",
  "name": "shadow-nli-v2-s2-bridge",
  "version": "1.0",
  "config": {
    "bridge_schema": "tactical_semantic_support_s2_nli_v2_bridge_v1",
    "nli_contract": "shadow_nli_v2_inference.judge_pair(claim,evidence)",
    "labels": ["contradicted", "insufficient", "supported"],
    "rationale_mode": "bridge_trace_only_no_semantic_rationale",
    "nli_config": {"...": "configurazione storica invariata"}
  }
}
```

### Spatial V1 proposto

```json
{
  "kind": "injected",
  "name": "shadow-nli-spatial-v1-s2-bridge",
  "version": "1.0",
  "config": {
    "bridge_schema": "tactical_semantic_support_s2_spatial_v1_bridge_v1",
    "callable_identity": "shadow_nli_spatial_relations_v1_inference.judge_pair(claim,evidence)",
    "contract": {
      "contract_id": "nli_spatial_relations_v1",
      "version": "1.0",
      "instruction_sha256": "sha256:861dbec3daac9ac34169356ad51a453f6267175afaa5d296f84c92586d2f3a00",
      "selection": "explicit_import_only"
    },
    "labels": ["contradicted", "insufficient", "supported"],
    "rationale_mode": "adapter_generated_absence_notice_no_model_rationale",
    "nli_config": {"...": "configurazione Spatial congelata"}
  }
}
```

## Rationale

Poiche S2 richiede una stringa non vuota, una label Spatial priva di rationale
deve produrre esclusivamente un avviso neutro, per esempio:

```text
Adapter-generated provenance notice: the injected Spatial V1 judge returned
only a label; no semantic rationale was provided by the model.
```

Il testo deve essere costante, identificato nel descriptor come generato
dall'adattatore e non deve contenere spiegazioni del verdetto. Non va modificato
lo schema S2 e non vanno inventati reasoning o cause.

## Impatto sui digest

Devono restare invariati:

- contratto Spatial V1 e instruction digest;
- fixture e Gold;
- plan fingerprint, poiche la formula usa fixture, casi e contract descriptor,
  non il bridge descriptor;
- bridge, descriptor, record e artefatti V2 storici;
- JSON Gate 2/3, 13.138 byte, SHA-256
  `a06ba357471681f2ac047af9cff8293d23e75f1c8c8e364f1b14fc4990f8c42d`.

Cambierebbero legittimamente soltanto in nuovi record Spatial:

- `judge.name`, `judge.version` e `judge.config_sha256`;
- `judge_rationale` come avviso di assenza;
- conseguente `record_sha256` e SHA-256 dell'eventuale nuovo report.

Nessun artefatto storico deve essere riscritto o ricalcolato.

## Piano minimo di verifica offline futura

1. Hash/blob del bridge V2 e descriptor V2 invariati.
2. Nuovo modulo inerte all'import e costruzione senza chiamate.
3. Descriptor Spatial con callable, contratto, versione, instruction digest,
   label e rationale mode esatti.
4. Proiezione claim/evidence byte-identica al bridge storico.
5. Le tre label passano senza rimappatura; output non canonici ed eccezioni
   restano fail-closed.
6. Avviso rationale non attribuisce reasoning al modello; la vecchia stringa V2
   non compare nel percorso Spatial.
7. S2 conserva `promotion_authorized=false`; errori diventano `not_evaluable`.
8. `judge.config_sha256` e `record_sha256` ricalcolati coerentemente sui nuovi
   metadati.
9. Runner Spatial seleziona solo il nuovo adattatore; runner V2 invariato.
10. Digest del JSON storico 2/3, fixture, Gold, contratto e plan fingerprint
    invariati.

Solo test differenziali nuovi e regressioni direttamente interessate; nessuna
inferenza, Gate o suite storica completa.

## Criteri di accettazione

- Nessuna modifica al bridge o runner V2.
- Provenance Spatial non contiene identificativi V2.
- Callable e contract descriptor validati fail-closed prima della valutazione.
- Label, prompt, evidence, parametri e verdetti non cambiano.
- Rationale chiaramente adapter-generated e semanticamente vuota.
- Nuovi digest verificabili; digest storici invariati.
- S1/S2, routing operativo e non-promozione invariati.

## Rischi e rollback

Rischi minori: duplicazione limitata della normalizzazione, coupling alla
proiezione storica e possibile divergenza futura tra i due adattatori. Mitigazioni:
riuso diretto di `project_claim`, test di equivalenza, costanti versionate e
nessun fallback.

Rollback: revert del nuovo modulo, dei test e del solo import/build del runner
Spatial. Il percorso V2 non richiede rollback. Nessun dato o artefatto runtime va
modificato.

## Decisione e stato

**DESIGN APPROVABILE.**

Non risultano problemi bloccanti o maggiori. Rischi residui minori sono coperti
dal piano differenziale. Progettazione **ESEGUITO**; implementazione **DA FARE**
previa autorizzazione separata. Gate semantico, integrazione e certificazione
restano **BLOCCATO**.

Unico prossimo passo: revisione indipendente del presente design e successiva
decisione del titolare sull'implementazione offline dell'alternativa B.
