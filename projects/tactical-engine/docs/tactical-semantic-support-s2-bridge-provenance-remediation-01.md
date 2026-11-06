# RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-REMEDIATION-01

## Baseline e perimetro

Remediation offline minima M1-M3 sulla baseline GitHub
`40de7501315676b7bfd0109c68fff4954ea9d599`. Branch e remoto erano conformi,
working tree pulito e le rettifiche non erano già presenti.

File tecnici modificati esclusivamente:

- `scripts/v5_tactical_semantic_support_s2_spatial_v1_bridge.py`;
- `tests/test_v5_tactical_semantic_support_s2_spatial_v1_bridge.py`;
- `tests/test_run_tactical_semantic_support_s2_spatial_relation_differential_v1.py`.

Runner Spatial, bridge/runner V2, S1/S2, contratti, fixture, Gold e artefatti
runtime non sono stati modificati.

## M1 — tipi originali

`_validate_contract_descriptor()` verifica prima di qualsiasi
canonicalizzazione:

- `type(value) is dict` e sei chiavi esatte;
- tipo `str` esatto per i cinque campi scalari;
- `type(labels) is list` ed elementi `str` esatti;
- ordine/valori delle tre label, identità, versione, base contract, selection e
  instruction digest congelati.

Tuple, sottoclassi di dict, elemento label non stringa, booleano al posto di una
stringa, campo mancante/inatteso e oggetto non serializzabile sono rifiutati con
`BridgeContractError` prima della costruzione. Anche `nli_config` richiede ora
un dict esatto oltre ai tipi/valori già congelati.

## M2 — immutabilità interna

Dopo la validazione, il descriptor completo viene canonicalizzato una volta e
memorizzato esclusivamente come stringa JSON `_descriptor_json`. Nessun dict o
lista del descriptor rimane nello stato interno. `judge_descriptor` deserializza
ogni volta una nuova copia.

I test mutano input e copia restituita, tentano la mutazione indicizzata della
stringa interna, controllano l'assenza di dict/list in `vars(adapter)` e
confrontano descriptor e identità/digest prima e dopo. La struttura pubblica e i
valori del descriptor sono invariati rispetto alla versione precedente.

## M3 — binding e artefatti congelati

Il test AST collega esplicitamente:

1. import del modulo Spatial e del bridge Spatial;
2. funzione locale `call` nel `main()`;
3. `Return(Call(spatial_nli.judge_pair(...)))`;
4. assegnazione `bridge = spatial_bridge.build_bridge(call, ...)`.

Non si limita quindi alla presenza/assenza dei nomi. Il runner non è stato
modificato.

Tre asserzioni indipendenti usano `hashlib.sha256(path.read_bytes())`:

| Artefatto | SHA-256 verificato |
|---|---|
| bridge NLI V2 | `79a4cc87c0d59e087a69d295a199f7f646c4ecb42194cf45531fd96dba09f515` |
| runner NLI V2 | `3c5818142b0a9ac1c689a1cb3c5523fae13883d95b10544963842b97134cbf91` |
| JSON Spatial storico | `a06ba357471681f2ac047af9cff8293d23e75f1c8c8e364f1b14fc4990f8c42d` |

## Test

Comando differenziale eseguito:

```text
python -m unittest projects/tactical-engine/tests/test_v5_tactical_semantic_support_s2_spatial_v1_bridge.py projects/tactical-engine/tests/test_run_tactical_semantic_support_s2_spatial_relation_differential_v1.py
```

Risultato: **14/14 PASS**, 0 FAIL, in 0,035 secondi.

| Area | Evidenza | Esito |
|---|---|---|
| M1 shape/tipi/valori originali | matrice parametrica inclusi tuple/subclass/nonserializzabile | PASS |
| M2 mutazioni input/copia/interno | descriptor e digest invariati | PASS |
| M3 call graph | AST closure -> Spatial judge -> Spatial bridge | PASS |
| M3 artefatti | SHA sui byte con `hashlib` | PASS |
| regressioni bridge | proiezione, label, rationale, fail-closed, digest | PASS |
| regressioni runner | 6 casi di test direttamente interessati | PASS |

Nessuna suite storica completa, Gold, inferenza, Ollama o Gate è stato eseguito.

## Descriptor e invarianti

La struttura pubblica resta:

```json
{
  "kind": "injected",
  "name": "shadow-nli-spatial-v1-s2-bridge",
  "version": "1.0",
  "config": {
    "bridge_schema": "tactical_semantic_support_s2_spatial_v1_bridge_v1",
    "declared_callable_identity": "shadow_nli_spatial_relations_v1_inference.judge_pair",
    "runtime_callable_authentication": "not_performed_by_bridge",
    "binding_evidence": "explicit_spatial_runner_import_and_closure",
    "label_provenance": "canonical_spatial_v1_judge_output",
    "rationale_mode": "adapter_generated_technical_notice_not_verdict_rationale"
  }
}
```

Il descriptor completo conserva contratto, label e configurazione identici.
Rationale tecnica, label, proiezione, evidence, routing, prompt, modello,
parametri e non-promozione sono invariati. Il runner Spatial ha SHA-256 corrente
`02a5a41e433d9010cb70ac08a0cb870f67ae39382e74676fe376f52fbea4024e` e
non compare nel diff.

## Rischi residui

Il callable runtime resta deliberatamente non autenticato dal bridge: il
binding è provato staticamente dal runner/test, non crittograficamente. Come per
ogni oggetto Python, primitive di introspezione estrema come
`object.__setattr__` possono aggirare convenzioni del linguaggio; non esistono
però riferimenti mutabili al descriptor nel normale contratto pubblico. Nessun
rischio residuo impedisce la validazione offline delle rettifiche.

## Decisione e stati

- Rettifiche M1-M3: **IMPLEMENTATO**.
- Test differenziali: **ESEGUITO**, 14/14 PASS.
- Tipi fail-closed, immutabilità, binding e SHA congelati: **VALIDATO** offline.
- Closeout offline definitivo: **DA FARE** mediante revisione indipendente.
- Gate semantico, integrazione e certificazione: **BLOCCATO**.

Unico prossimo passo: revisione indipendente conclusiva della remediation
pubblicata; nessun nuovo Gate o runtime senza decisione separata del titolare.
