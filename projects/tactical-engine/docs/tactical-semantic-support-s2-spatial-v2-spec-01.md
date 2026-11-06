# RD-TSC-V2-D3-S2-SPATIAL-V2-SPEC-01

## Baseline e riconciliazione

Specifica esclusivamente documentale sulla baseline GitHub
`16c6daf1762b6e328546726a45d91d11f91d2b37`, branch
`codex/tactical-state-contract-v1`. Prima della redazione, HEAD locale e remoto
erano conformi e il working tree era pulito. Sono stati riconciliati TODO,
experiment register, design semantico `q3_04`, forensi `q3_04` e differenziale,
closeout della provenance, judge NLI V2/Spatial V1, bridge e boundary S2.

Non è stato eseguito alcuno script di test, modello, Gate o runtime. Nessun
codice, contratto eseguibile, fixture, dataset, Gold o artefatto storico è stato
modificato.

## Scopo e confini

La specifica definisce il contratto sperimentale opt-in
`nli_spatial_relations_v2`, versione `2.0.0`. Spatial V2 produce, in una sola
generazione, una label e un relation witness strutturato per claim ed evidenza.
Un validatore puro verifica shape, vocabolario, ancore e coerenza fra witness,
comparison e label.

Invarianti:

- una generazione, zero retry, zero repair e zero fallback;
- selezione esplicita; NLI V2 e Spatial V1 invariati;
- nessuna chiamata del validatore a modelli o servizi;
- nessuna riscrittura di witness o label;
- errore o incertezza tecnica: fail-closed `not_evaluable` al boundary S2;
- risultato shadow, `promotion_authorized=false`;
- legacy, S1, adapter S2, retrieval, Gold, API, RAG, Chroma e panel invariati.

La specifica rende il confronto osservabile e falsificabile. Non dimostra che
il modello estragga correttamente la semantica, né che corregga `q3_04`.

## Schema formale

Schema normativo: JSON Schema Draft 2020-12. Un'implementazione futura dovrà
usare semanticamente questo schema senza ampliamenti permissivi.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:football-data-lab:nli-spatial-relations-v2:2.0.0",
  "title": "NLI Spatial Relations V2 Witness",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "contract_id", "contract_version", "label",
    "claim_relation", "evidence_relation", "comparison"
  ],
  "properties": {
    "contract_id": {"const": "nli_spatial_relations_v2"},
    "contract_version": {"const": "2.0.0"},
    "label": {
      "type": "string",
      "enum": ["supported", "contradicted", "insufficient"]
    },
    "claim_relation": {"$ref": "#/$defs/claimRelation"},
    "evidence_relation": {"$ref": "#/$defs/evidenceRelation"},
    "comparison": {"$ref": "#/$defs/comparison"}
  },
  "$defs": {
    "anchor": {
      "type": "object",
      "additionalProperties": false,
      "required": ["source", "start", "end", "exact_span"],
      "properties": {
        "source": {"type": "string", "enum": ["claim", "evidence"]},
        "start": {"type": "integer", "minimum": 0},
        "end": {"type": "integer", "minimum": 1},
        "exact_span": {"type": "string", "minLength": 1}
      }
    },
    "status": {
      "type": "string",
      "enum": ["explicit", "implicit", "absent", "ambiguous", "unknown"]
    },
    "entity": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "entity_id", "anchors"],
      "properties": {
        "status": {"$ref": "#/$defs/status"},
        "entity_id": {
          "type": "string",
          "pattern": "^entity:[a-z0-9][a-z0-9._-]{0,63}$"
        },
        "anchors": {
          "type": "array", "items": {"$ref": "#/$defs/anchor"},
          "minItems": 0, "maxItems": 4
        }
      },
      "allOf": [
        {
          "if": {"properties": {"status": {"const": "explicit"}}},
          "then": {"properties": {"anchors": {"minItems": 1}}}
        },
        {
          "if": {"properties": {"status": {"enum": ["absent", "unknown"]}}},
          "then": {"properties": {"anchors": {"maxItems": 0}}}
        }
      ]
    },
    "axis": {
      "type": "string",
      "enum": [
        "space_availability", "distance_change", "movement_direction",
        "area_extent", "relative_position"
      ]
    },
    "axisSlot": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "value", "anchors"],
      "properties": {
        "status": {"$ref": "#/$defs/status"},
        "value": {
          "oneOf": [
            {"$ref": "#/$defs/axis"},
            {"type": "string", "enum": ["absent", "ambiguous", "unknown"]}
          ]
        },
        "anchors": {
          "type": "array", "items": {"$ref": "#/$defs/anchor"},
          "minItems": 0, "maxItems": 4
        }
      }
    },
    "valueSlot": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "value", "anchors"],
      "properties": {
        "status": {"$ref": "#/$defs/status"},
        "value": {
          "type": "string",
          "enum": [
            "abundant", "scarce", "neutral",
            "increasing", "decreasing", "stable",
            "advancing", "retreating", "stationary",
            "expanding", "contracting",
            "ahead_of", "behind", "between", "inside", "outside", "adjacent",
            "absent", "ambiguous", "unknown"
          ]
        },
        "anchors": {
          "type": "array", "items": {"$ref": "#/$defs/anchor"},
          "minItems": 0, "maxItems": 4
        }
      }
    },
    "condition": {
      "type": "object",
      "additionalProperties": false,
      "required": ["condition_id", "status", "anchors"],
      "properties": {
        "condition_id": {
          "type": "string",
          "pattern": "^condition:[a-z0-9][a-z0-9._-]{0,63}$"
        },
        "status": {"type": "string", "enum": ["explicit", "ambiguous"]},
        "anchors": {
          "type": "array", "items": {"$ref": "#/$defs/anchor"},
          "minItems": 1, "maxItems": 4
        }
      }
    },
    "conditions": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "items"],
      "properties": {
        "status": {"$ref": "#/$defs/status"},
        "items": {
          "type": "array", "items": {"$ref": "#/$defs/condition"},
          "minItems": 0, "maxItems": 8
        }
      }
    },
    "phase": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "value", "anchors"],
      "properties": {
        "status": {"$ref": "#/$defs/status"},
        "value": {
          "type": "string",
          "enum": [
            "attack", "offensive_transition", "defense", "defensive_transition",
            "set_piece", "general", "absent", "ambiguous", "unknown"
          ]
        },
        "anchors": {
          "type": "array", "items": {"$ref": "#/$defs/anchor"},
          "minItems": 0, "maxItems": 4
        }
      }
    },
    "quantifier": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "value", "literal", "anchors"],
      "properties": {
        "status": {"$ref": "#/$defs/status"},
        "value": {
          "type": "string",
          "enum": [
            "none", "existential", "some", "many", "most", "all",
            "always", "never", "numeric", "absent", "ambiguous", "unknown"
          ]
        },
        "literal": {"type": ["string", "null"], "maxLength": 64},
        "anchors": {
          "type": "array", "items": {"$ref": "#/$defs/anchor"},
          "minItems": 0, "maxItems": 2
        }
      }
    },
    "polarity": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "value", "anchors"],
      "properties": {
        "status": {"$ref": "#/$defs/status"},
        "value": {
          "type": "string",
          "enum": ["affirmed", "negated", "ambiguous", "unknown"]
        },
        "anchors": {
          "type": "array", "items": {"$ref": "#/$defs/anchor"},
          "minItems": 0, "maxItems": 2
        }
      }
    },
    "relationCore": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "subject", "semantic_axis", "reference", "value", "conditions",
        "phase", "quantifier", "polarity"
      ],
      "properties": {
        "subject": {"$ref": "#/$defs/entity"},
        "semantic_axis": {"$ref": "#/$defs/axisSlot"},
        "reference": {"$ref": "#/$defs/entity"},
        "value": {"$ref": "#/$defs/valueSlot"},
        "conditions": {"$ref": "#/$defs/conditions"},
        "phase": {"$ref": "#/$defs/phase"},
        "quantifier": {"$ref": "#/$defs/quantifier"},
        "polarity": {"$ref": "#/$defs/polarity"}
      }
    },
    "claimRelation": {
      "allOf": [
        {"$ref": "#/$defs/relationCore"},
        {
          "properties": {
            "subject": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "claim"}}}}}},
            "semantic_axis": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "claim"}}}}}},
            "reference": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "claim"}}}}}},
            "value": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "claim"}}}}}},
            "phase": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "claim"}}}}}},
            "quantifier": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "claim"}}}}}},
            "polarity": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "claim"}}}}}}
          }
        }
      ]
    },
    "evidenceRelation": {
      "allOf": [
        {"$ref": "#/$defs/relationCore"},
        {
          "properties": {
            "subject": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "evidence"}}}}}},
            "semantic_axis": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "evidence"}}}}}},
            "reference": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "evidence"}}}}}},
            "value": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "evidence"}}}}}},
            "phase": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "evidence"}}}}}},
            "quantifier": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "evidence"}}}}}},
            "polarity": {"properties": {"anchors": {"items": {"properties": {"source": {"const": "evidence"}}}}}}
          }
        }
      ]
    },
    "comparisonValue": {
      "type": "string",
      "enum": ["same", "compatible", "different", "incompatible", "unknown", "ambiguous"]
    },
    "comparison": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "subject", "semantic_axis", "reference", "conditions", "phase",
        "value", "quantifier", "polarity"
      ],
      "properties": {
        "subject": {"$ref": "#/$defs/comparisonValue"},
        "semantic_axis": {"$ref": "#/$defs/comparisonValue"},
        "reference": {"$ref": "#/$defs/comparisonValue"},
        "conditions": {"$ref": "#/$defs/comparisonValue"},
        "phase": {"$ref": "#/$defs/comparisonValue"},
        "value": {"$ref": "#/$defs/comparisonValue"},
        "quantifier": {"$ref": "#/$defs/comparisonValue"},
        "polarity": {"$ref": "#/$defs/comparisonValue"}
      }
    }
  }
}
```

### Vincoli incrociati oltre JSON Schema

Il validatore deve applicare anche regole non esprimibili convenientemente nel
solo schema:

1. `explicit` richiede almeno un'ancora; `absent` e `unknown` richiedono zero
   ancore e rispettivamente valore `absent`/`unknown` dove previsto.
2. `ambiguous` richiede valore `ambiguous`; può avere ancore solo se l'ambiguità
   è esplicitamente localizzabile.
3. `implicit` è ammesso solo per subject/reference recuperabili per coreferenza,
   phase `general`, quantifier `none` e polarity `affirmed`; non è prova
   testuale autonoma e rende `supported`/`contradicted` impossibili se riguarda
   subject o reference.
4. `semantic_axis` e `value` devono appartenere alla stessa famiglia del
   vocabolario sotto definito.
5. ID uguali dichiarano identità locale; ID diversi non provano diversità
   semantica. Il comparison resta un'asserzione del modello, controllabile solo
   per non contraddizione con ID, enum e status.
6. `conditions.status=absent` richiede `items=[]`; `explicit` richiede almeno un
   item; ID duplicati sono invalidi.
7. `quantifier.value=numeric` richiede `literal` non vuoto e ancora esplicita;
   ogni altro valore richiede `literal=null`.
8. `polarity=negated` richiede ancora esplicita; `affirmed` può avere zero
   ancore perché indica assenza di negazione grammaticale osservata.
9. Ogni array di ancore è ordinato per `(start,end,exact_span)` e non contiene
   duplicati. L'ordine è normativo per la serializzazione canonica.
10. Tutte le ancore, incluse quelle delle condizioni, devono avere `source`
    uguale alla relazione che le contiene: `claim` in `claim_relation` ed
    `evidence` in `evidence_relation`.

## Regole di ancoraggio

- `start` ed `end` sono offset zero-based in Unicode code point, intervallo
  semiaperto `[start,end)`, sul testo originale esatto fornito al judge.
- Claim, evidence ed `exact_span` devono essere NFC. Il validatore rifiuta input
  non NFC; non li normalizza silenziosamente.
- Deve valere `source_text[start:end] == exact_span`, con confronto case-sensitive
  e sensibile a spazi, accenti e punteggiatura.
- Uno span ripetuto è ammesso solo indicando l'occorrenza corretta mediante
  offset. Lo stesso span può ancorare più componenti se realmente pertinente.
- Span sovrapposti sono ammessi; non aumentano il peso probatorio.
- Span inesistente, fuori limite, vuoto o associato alla sorgente errata rende
  il witness strutturalmente invalido: `not_evaluable`.
- Parafrasi e referenti impliciti non possono essere presentati come
  `exact_span`. Possono essere marcati `implicit`, con i limiti fail-closed
  sopra descritti; il validatore non risolve coreferenze.
- L'ancora prova presenza testuale, non correttezza di entity ID, asse o valore.

La serializzazione canonica per digest futuri è UTF-8, NFC, JSON con chiavi
ordinate, separatori `(',', ':')`, `ensure_ascii=false`, newline escluso. Questa
regola non cambia i digest storici e sarà applicabile solo ai nuovi record V2.

## Vocabolario relazionale versionato

Vocabolario `spatial_relation_vocab_v2`, versione `1.0.0`:

| Asse | Valori ammessi | Compatibili | Incompatibili | Ordinamento |
|---|---|---|---|---|
| `space_availability` | `abundant`, `scarce`, `neutral` | identici; `neutral` solo con `neutral` | `abundant` ↔ `scarce` | `scarce < neutral < abundant` |
| `distance_change` | `increasing`, `decreasing`, `stable` | identici | increasing ↔ decreasing; ciascuno ↔ stable | nessun ordine quantitativo |
| `movement_direction` | `advancing`, `retreating`, `stationary` | identici | advancing ↔ retreating; movimento ↔ stationary | nessuno |
| `area_extent` | `expanding`, `contracting`, `stable` | identici | expanding ↔ contracting; ciascuno ↔ stable | nessuno |
| `relative_position` | `ahead_of`, `behind`, `between`, `inside`, `outside`, `adjacent` | identici | ahead_of ↔ behind; inside ↔ outside | nessuno; le altre coppie sono `different` |

`unknown`, `ambiguous` e `absent` sono sentinelle, non valori semantici. Assi
diversi sono `different` e non confrontabili, mai automaticamente
`incompatible`. Non sono ammesse nuove categorie runtime: un concetto non
rappresentabile diventa `unknown` e conduce a insufficienza o non valutabilità
secondo la causa.

Quantificatori:

- `none`: nessun quantificatore esplicito;
- `existential`, `some`, `many`, `most`, `all`: forza crescente ma senza
  conversione numerica;
- `always` e `never`: quantificatori temporali assoluti;
- `numeric`: valore letterale conservato, senza parsing semantico automatico.

Compatibilità deterministica dei quantificatori è limitata all'identità. Valori
diversi sono `different`; `all` rispetto a `some`, o `always` rispetto a una
descrizione occasionale, non diventa contraddizione senza una proposizione
esplicitamente incompatibile. `never` è trattato insieme alla polarità: la sola
assenza di un evento non prova `never`.

Polarità: identica è `same`; `affirmed`/`negated` è `incompatible` soltanto se
soggetto, asse, referente, condizioni, fase e valore sono comparabili. In caso
contrario il confronto non può produrre `contradicted`.

## Semantica di comparabilità

Il comparison è prodotto dal modello ma verificato per coerenza locale:

- `same`: valori/ID canonici identici e status determinati;
- `compatible`: valori non identici ma compatibilità ammessa esplicitamente dal
  vocabolario o identità locale dichiarata con formulazioni diverse;
- `different`: entrambi determinati, ma non uguali e non incompatibili;
- `incompatible`: coppia esplicitamente incompatibile nel vocabolario, oppure
  polarità opposta su relazione altrimenti comparabile;
- `unknown`: almeno un componente ha status/value `unknown` o `absent` e non è
  possibile concludere;
- `ambiguous`: almeno un componente è `ambiguous`.

Regole per dimensione:

1. **Subject/reference.** Stesso `entity_id` consente `same`; ID diversi non
   consentono al validatore di dedurre equivalenza. `compatible` resta
   un'asserzione osservabile del modello e non una proprietà dimostrata.
   `different` è ammesso con ID distinti e status espliciti. `incompatible` non
   è ammesso per entity: entità diverse sono `different`.
2. **Axis/value.** Sono verificabili rispetto agli enum e alla matrice del
   vocabolario. Assi diversi rendono il valore non confrontabile.
3. **Conditions.** Set di `condition_id` identici: `same`; insiemi distinti:
   `different`, salvo `ambiguous`/`unknown`. `compatible` non è derivabile
   deterministicamente nella versione 2.0.0 e quindi non è ammesso qui.
4. **Phase.** Valori identici: `same`; `general` rispetto a fase specifica:
   `unknown`, non `compatible`; fasi specifiche diverse: `different`.
5. **Quantifier.** Identico: `same`; diverso determinato: `different`;
   `incompatible` solo per `always`/`never` sulla stessa proposizione e con
   polarità coerentemente rappresentata.
6. **Polarity.** Identica: `same`; affirmed/negated: `incompatible` quando le
   altre dimensioni obbligatorie sono comparabili.

Una relazione è comparabile ai fini di `supported` o `contradicted` solo se:

- subject e reference sono `same` o `compatible`;
- semantic axis è `same`;
- conditions e phase sono `same` oppure entrambi esplicitamente `absent`;
- nessuna dimensione obbligatoria è `unknown` o `ambiguous`;
- quantifier non introduce una generalizzazione non documentata.

Il validatore può verificare che la dichiarazione sia coerente con ID/status ed
enum; non può dimostrare che due espressioni diverse rappresentino davvero lo
stesso soggetto o referente. Tale interpretazione resta del modello.

## Derivazione deterministica della label

Il validatore calcola `derived_label` senza modificare `label`:

1. Se schema, tipo, enum, ancora, cross-rule o comparison sono invalidi:
   `technical_status=not_evaluable`; nessuna label semantica derivata.
2. Se subject/reference/axis sono `unknown`, `ambiguous`, `absent` oppure non
   comparabili perché impliciti: `derived_label=insufficient` solo quando il
   witness è strutturalmente valido e dichiara onestamente la mancanza nella
   fonte; altrimenti `not_evaluable`.
3. Se la fonte non contiene valore determinato per una relazione richiesta dal
   claim: `insufficient`.
4. Se relazione comparabile e value/polarity sono `same` o compatibili, e il
   quantificatore della claim non è più forte di quello attestato:
   `supported`.
5. Se relazione comparabile e value oppure polarity sono `incompatible` secondo
   il vocabolario: `contradicted`.
6. Se dimensioni determinate sono `different` ma non incompatibili:
   `insufficient`.
7. Se `label != derived_label`: errore `E_LABEL_WITNESS_MISMATCH`, risultato
   `not_evaluable`. La label non viene corretta.

`not_evaluable` è uno stato tecnico del validatore/boundary, non una quarta
label del judge. `insufficient` è una label semantica valida prodotta da un
witness ben formato che mostra insufficienza dell'evidenza.

## Matrice decisionale

| Caso strutturato | Esito | Regola | Motivazione/fail-closed |
|---|---|---|---|
| subject same, reference same, axis same, value same, contesto same | `supported` | D4 | relazione attestata |
| subject compatible dichiarato, resto same, value compatibile | `supported` | D4 | compatibilità osservabile ma semanticamente model-dependent |
| subject different | `insufficient` | D6 | fonte parla di altro attore |
| subject unknown/ambiguous | `insufficient` o `not_evaluable` | D2 | insufficient solo con mancanza valida nella fonte |
| reference different | `insufficient` | D6 | parole comuni non rendono uguale lo spazio |
| reference unknown/ambiguous | `insufficient` o `not_evaluable` | D2 | nessuna falsa equivalenza |
| axis same, abundant/scarce, tutto il resto comparabile | `contradicted` | D5 | coppia incompatibile versionata |
| axis diversi | `insufficient` | D6 | non confrontabili, non contraddittori |
| advancing/retreating, resto comparabile | `contradicted` | D5 | direzioni inverse sullo stesso asse |
| phase specifiche differenti | `insufficient` | D6 | fatti in fasi diverse |
| phase general vs specifica | `insufficient` | D2/D6 | general non prova equivalenza |
| conditions set uguali | continua | comparabilità | condizioni confrontabili |
| conditions set differenti | `insufficient` | D6 | contesti differenti |
| evidenza senza valore | `insufficient` | D3 | fonte non determina la relazione |
| value ambiguous | `insufficient` | D2 | witness valido ma semantica non conclusiva |
| axis unknown/non rappresentabile | `insufficient` | D2 | nessuna categoria inventata |
| polarity affirmed/negated, resto comparabile | `contradicted` | D5 | negazione esplicita |
| quantifier claim più forte, fonte più debole | `insufficient` | D4/D6 | non falsa automaticamente |
| always/never sulla stessa proposizione | `contradicted` solo se esplicito | D5 | incompatibilità assoluta ancorata |
| relation non rappresentabile dichiarata unknown | `insufficient` | D2 | contratto valido, evidenza non determinabile |
| comparison contraddice ID/status/vocab | `not_evaluable` | D1 | `E_COMPARISON_INCONSISTENT` |
| label non coincide con derivazione | `not_evaluable` | D7 | `E_LABEL_WITNESS_MISMATCH` |
| ancora inesistente/fuori limite/source errata | `not_evaluable` | D1 | `E_ANCHOR_INVALID` |
| campo extra/tipo/enum errato | `not_evaluable` | D1 | invalidità strutturale |
| output troncato/non JSON/eccezione | `not_evaluable` | boundary | zero retry/repair/fallback |

Per `q3_04`, un witness che dichiari stesso soggetto, stesso referente,
`space_availability`, claim `abundant` ed evidence `scarce` consentirebbe solo
`contradicted`. Questa è una dimostrazione della regola, non un output osservato.

## Contratto del validatore

Interfaccia progettuale pura:

```text
validate_spatial_v2(witness, claim_text, evidence_text) -> validation_result
```

Output esatto proposto:

```json
{
  "validator_id": "nli_spatial_relations_v2_validator",
  "validator_version": "1.0.0",
  "technical_status": "valid",
  "derived_label": "contradicted",
  "model_label": "contradicted",
  "comparison_verified": true,
  "error_codes": []
}
```

`technical_status` è `valid` o `not_evaluable`; `derived_label` è una delle tre
label oppure `null`. Ordine dei controlli, con arresto della derivazione ma
raccolta deterministica degli errori della stessa fase:

1. tipo radice e JSON Schema;
2. identità/versione e proprietà aggiuntive;
3. NFC e validità delle sorgenti;
4. offset, exact spans, ordinamento e duplicati;
5. cross-rule status/value/anchor;
6. compatibilità axis/value e ID/cardinalità;
7. coerenza del comparison;
8. derivazione della label;
9. confronto label/witness.

Codici minimi:

| Codice | Significato |
|---|---|
| `E_SCHEMA_INVALID` | shape, required, tipo o extra field errato |
| `E_IDENTITY_INVALID` | contract ID/version non conformi |
| `E_TEXT_NOT_NFC` | sorgente o span non NFC |
| `E_ANCHOR_INVALID` | offset/span/source non corrispondente |
| `E_ANCHOR_ORDER_OR_DUPLICATE` | ordine o unicità non conforme |
| `E_STATUS_VALUE_INCONSISTENT` | status, sentinel e anchors incoerenti |
| `E_AXIS_VALUE_INCOMPATIBLE` | valore non appartenente all'asse |
| `E_DUPLICATE_LOCAL_ID` | condition ID duplicato nello stesso ambito |
| `E_COMPARISON_INCONSISTENT` | confronto incompatibile con witness/vocab |
| `E_RELATION_NOT_COMPARABLE` | comparabilità richiesta ma non dimostrata |
| `E_LABEL_WITNESS_MISMATCH` | label modello diversa da derived label |
| `E_VALIDATOR_EXCEPTION` | eccezione contenuta al boundary |

Campi sconosciuti, dati parziali e qualunque eccezione sono `not_evaluable`.
Il validatore non chiama il modello, non normalizza l'input, non riscrive il
witness, non cambia label e non effettua fallback.

Proprietà dimostrabili: conformità strutturale, presenza esatta degli span,
appartenenza a enum, coerenza interna, applicazione della matrice e identità
content-addressed. Non dimostrabili: correttezza dell'entità estratta,
coreferenza, sinonimia, scelta dell'asse/valore e verità della label rispetto al
linguaggio naturale.

## Integrazione futura e isolamento

Percorso minimo, solo progettuale:

1. nuovo modulo judge V2 opt-in, inerte su import, selezionato esplicitamente da
   un futuro runner dedicato;
2. schema structured-output uguale a quello normativo e singola chiamata;
3. validatore puro immediatamente dopo il parsing;
4. bridge Spatial V2 dedicato, senza modificare bridge Spatial V1/NLI V2;
5. bridge restituisce al boundary S2 label e rationale tecnica, più witness e
   validation result in una nuova estensione versionata del record; non altera
   le chiavi storiche senza un contratto S2 separatamente approvato;
6. boundary S2 converte ogni `not_evaluable`/eccezione in record shadow non
   promotabile; non cambia S1, `overall_status` o `promoted_answer`;
7. provenance include contract/schema/vocab/validator version, instruction
   digest, model config e digest canonico del witness;
8. persistenza soltanto in nuovi artefatti esclusivi; nessuna sovrascrittura di
   JSON storici.

Interfacce reali considerate: oggi Spatial V1 usa `judge_pair(claim,evidence) ->
label`, un bridge dedicato trasforma la label in `{label,rationale}`, e S2 accetta
esattamente quel risultato. Spatial V2 richiederà quindi un bridge/record
versionato o un'estensione esplicitamente approvata: inserire silenziosamente il
witness nel formato S2 corrente violerebbe la shape esatta. Questa è una
decisione implementativa ancora necessaria, non un permesso a cambiare S2.

Nuovi digest futuri: schema, vocabolario, instruction, validator source,
configurazione judge, witness canonico e record. Essi attestano identità e
integrità, non correttezza semantica.

## Compatibilità

- Spatial V2 è opt-in e non sostituisce NLI V2 o Spatial V1.
- Nessun fallback automatico fra contratti.
- Il bridge Spatial V1 validato, S1 e adapter S2 restano byte-invariati finché
  una futura patch non sia separatamente autorizzata.
- Fixture, Gold, dataset, report e artefatti storici non vengono migrati.
- Retrieval, collection, API, RAG, Chroma e panel non selezionano V2.
- `promotion_authorized=false` resta obbligatorio.
- Isolamento futuro verificabile tramite import esplicito, call graph, conteggio
  di una chiamata mock, assenza di retry/repair/fallback, SHA dei moduli storici
  e regressione adapter-disabilitato.

## Piano futuro di verifica — non eseguito

### A. Offline deterministico

- schema completo, campi extra, tipi JSON e non-hashable;
- NFC, offset code point, span ripetuti/sovrapposti e source errata;
- ogni status/sentinel e cross-rule;
- tutte le famiglie axis/value e coppie incompatibili;
- subject/reference/phase/conditions/quantifier/polarity comparabili e non;
- derivazione supported/contradicted/insufficient;
- mismatch label/witness e comparison incoerente fail-closed;
- output malformato/eccezione `not_evaluable`;
- una chiamata mock, zero retry/repair/fallback;
- invarianti S1/S2/legacy e digest storici.

### B. Verifica semantica futura

- `q3_04`: regressione nota, atteso `contradicted`;
- `q5_06`: inverso distinto ma correlato, atteso `contradicted`;
- `q5_02`: guardia `insufficient`;
- `q3_05`: controllo `supported`;
- `q5_08`: guardia quantificatore `insufficient`;
- `low_block_wrong`: solo controllo storico documentato, non nuovo Gold.

Questi casi non bastano a provare generalizzazione e non vengono rieseguiti in
questa attività.

### C. Generalizzazione

Una futura decisione umana dovrà autorizzare casi indipendenti con:

- stesso lessico e referente diverso;
- stessa relazione in fase diversa;
- parafrasi con soggetto coreferente;
- movimento davanti alla linea rispetto a spazio dietro la linea;
- negazione, quantificatore e condizione temporale variati;
- relazioni non rappresentabili e ambigue.

Non sono fissate soglie numeriche: richiedono un Gold indipendente e una decisione
separata. Il solo successo di `q3_04` o 3/3 non autorizza promozione.

## Rischi e limiti

- Il witness proviene dallo stesso modello: può essere sbagliato ma coerente.
- Entity ID e `compatible` per parafrasi/coreferenza non sono verificabili dal
  validatore senza introdurre un secondo sistema semantico.
- Vocabolario stretto può aumentare `insufficient`/`not_evaluable`; ampliarlo
  senza evidenze può creare false equivalenze.
- Le ancore provano presenza, non interpretazione.
- Lo schema più ampio può aumentare output incompleti o malformati.
- Structured output e validazione interna non costituiscono revisione
  indipendente né misura di accuratezza.

## Matrice probatoria A/B/C

| Conclusione | Livello |
|---|---|
| Input, routing, parsing e provenance storici corretti | A — dimostrato |
| Spatial V1 espone solo la label pur chiedendo confronto relazionale | A |
| q3_04 resta falso positivo in NLI V2 e Spatial V1 | A |
| Errore localizzato nel verdetto semantico restituito | B — fortemente supportato |
| Witness/ancore rendono il confronto osservabile e internamente verificabile | A come proprietà del contratto |
| Entity equivalence dichiarata dal witness è semanticamente corretta | C — ipotesi del modello |
| Spatial V2 correggerà q3_04 | C |
| Spatial V2 migliorerà accuratezza generale | C |
| Causa cognitiva interna del falso positivo | non determinabile |

## Decisioni progettuali aperte

Non bloccano la completezza della specifica del judge/validatore, ma richiedono
decisione prima dell'implementazione integrata:

1. approvare un record/bridge S2 V2 separato per conservare witness e validation
   result senza alterare la shape S2 corrente;
2. decidere se `compatible` per subject/reference debba essere conservato come
   asserzione non verificata o vietato nella prima implementazione più stretta;
3. approvare l'insieme di casi indipendenti e il relativo Gold prima di qualsiasi
   affermazione di generalizzazione.

Non viene inventato un resolver di coreferenza né un classificatore lessicale.

## Decisione tecnica e stati

La specifica è completa per una futura implementazione offline isolata del
judge e validatore. La scelta raccomandata è procedere soltanto dopo revisione
indipendente della specifica e decisione sulle interfacce S2 versionate.

| Attività/componente | Stato |
|---|---|
| Progettazione semantica `q3_04` | **ESEGUITO** |
| Specifica tecnica offline Spatial V2 | **ESEGUITO** dopo pubblicazione |
| Implementazione Spatial V2 | **DA FARE** |
| Efficacia semantica | **BLOCCATO** |
| Gate runtime | **BLOCCATO** |
| Integrazione | **BLOCCATO** |
| Certificazione | **BLOCCATO** |
| Closeout provenance Spatial V1 | **VALIDATO** |

Unico prossimo passo: revisione indipendente della presente specifica e decisione
esplicita del titolare; nessuna implementazione o inferenza è autorizzata.
