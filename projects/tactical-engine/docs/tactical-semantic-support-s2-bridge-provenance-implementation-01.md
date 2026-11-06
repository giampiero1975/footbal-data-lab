# RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-IMPLEMENTATION-01

## Attività e baseline

Implementazione esclusivamente offline dell'adattatore S2 dedicato a Spatial V1
sulla baseline GitHub
`0de21a2fa1b3a8cb1b62df384421fae8aa286969`. Branch e remoto erano conformi,
working tree pulito e nessuna implementazione equivalente presente.

File applicativi:

- creato `scripts/v5_tactical_semantic_support_s2_spatial_v1_bridge.py`;
- modificato soltanto import e costruzione del bridge in
  `scripts/run_tactical_semantic_support_s2_spatial_relation_differential_v1.py`;
- creato il test differenziale del bridge e aggiornato il test del runner
  Spatial;
- nessun altro file applicativo modificato.

## Implementazione M1

Il descriptor identifica l'adattatore
`shadow-nli-spatial-v1-s2-bridge`, il callable **dichiarato**
`shadow_nli_spatial_relations_v1_inference.judge_pair`, il contratto e la
configurazione content-addressed. Registra esplicitamente
`runtime_callable_authentication=not_performed_by_bridge` e il binding
`explicit_spatial_runner_import_and_closure`: il bridge non presenta
`callable()`, introspezione o nomi Python come autenticazione.

Il runner importa esclusivamente il nuovo bridge per S2 e continua a importare
esplicitamente il judge Spatial, costruendo la stessa closure sulle stesse
opzioni. Nessun import o percorso al judge NLI V2 è stato introdotto. Import e
costruzione del bridge sono inerti.

## Implementazione M2

La costruzione accetta soltanto:

- contract descriptor con le sei chiavi esatte e valori congelati Spatial V1,
  incluso instruction digest
  `sha256:861dbec3daac9ac34169356ad51a453f6267175afaa5d296f84c92586d2f3a00`;
- runtime config con le dieci chiavi esatte, tipi rigorosi (bool non accettati
  come int) e valori congelati del runner autorizzato.

Chiavi mancanti/inattese, tipi errati, valori incoerenti, digest diverso e dati
non serializzabili sollevano `BridgeContractError` durante la costruzione. Le
strutture sono canonicalizzate e copiate; la proprietà del descriptor restituisce
una copia difensiva. Non esistono fallback, retry o repair.

Il bridge riusa esclusivamente `project_claim`, `NLI_LABELS` e
`BridgeContractError` dal bridge storico. Evidence e ordine degli argomenti sono
invariati. Accetta soltanto una delle tre label stringa e restituisce la label
senza rimappatura con la nota tecnica stabile:

```text
Adapter-generated technical provenance notice (not verdict rationale): the injected Spatial V1 judge returned only a label; no semantic rationale was provided by the model.
```

## Test differenziali

Comando eseguito:

```text
python -m unittest projects/tactical-engine/tests/test_v5_tactical_semantic_support_s2_spatial_v1_bridge.py projects/tactical-engine/tests/test_run_tactical_semantic_support_s2_spatial_relation_differential_v1.py
```

Risultato: **14/14 PASS** in 0,033 secondi.

| Gruppo | Casi | Esito |
|---|---:|---|
| Nuovo bridge: costruzione inerte e descriptor Spatial | 1 | PASS |
| Copie difensive | 1 | PASS |
| Config/descriptor mancanti, inattesi, tipi e valori errati | 1 parametrico | PASS |
| Proiezione claim ed evidence identiche | 1 | PASS |
| Tre label e nota tecnica | 1 parametrico | PASS |
| Output malformati fail-closed | 1 parametrico | PASS |
| Eccezioni contenute da S2 e non-promozione | 1 | PASS |
| Digest config e record ricalcolati indipendentemente | 1 | PASS |
| Runner: fixture, binding, arresto, integrità e invarianti | 6 | PASS |

I test usano soltanto stub/mock locali. Nessuna inferenza, chiamata Ollama,
modello, Gate o runtime è stato eseguito. Non sono state ripetute suite storiche.

## Immutabilità e digest

| Artefatto | SHA-256 prima | SHA-256 dopo | Esito |
|---|---|---|---|
| bridge NLI V2 | `79a4cc87c0d59e087a69d295a199f7f646c4ecb42194cf45531fd96dba09f515` | uguale | invariato |
| runner V2 storico | `3c5818142b0a9ac1c689a1cb3c5523fae13883d95b10544963842b97134cbf91` | uguale | invariato |
| JSON Spatial storico | `a06ba357471681f2ac047af9cff8293d23e75f1c8c8e364f1b14fc4990f8c42d` | uguale | invariato |

Fixture Spatial (`45c26718...`), Gold, contratto Spatial e artefatti runtime non
sono stati modificati. Il runner continua a calcolare il plan fingerprint dal
contract descriptor, non dal descriptor del bridge. I test ricalcolano
indipendentemente `judge.config_sha256` e `record_sha256` dei soli record
sintetici nuovi.

## Descriptor sintetico

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

Il descriptor completo include anche contratto, label e configurazione runtime
canonici. Nessuna identità V2 è registrata come judge Spatial; il riferimento
`base_contract=shadow_nli_v2_inference` resta legittimo e distinto.

## Rischi e limiti residui

Il bridge non autentica il callable runtime: il binding è dimostrato dal codice
esplicito del runner e dai test, come richiesto da M1. Il riuso di
`project_claim()` crea un coupling intenzionale col bridge storico, bloccato dal
test di equivalenza; una sua futura modifica richiederà revisione. La presente
validazione prova orchestrazione, provenance, fail-closed e digest, non
affidabilità semantica del modello.

## Decisione e stato

- Codice adapter Spatial: **IMPLEMENTATO**.
- Test differenziali: **ESEGUITO**, 14/14 PASS.
- M1, M2, provenance, fail-closed, digest e non-promozione: **VALIDATO** offline.
- Gate semantico, integrazione e certificazione: **BLOCCATO**.

Nessuna inferenza, Gate, modifica operativa, deploy o merge. Unico prossimo
passo: revisione indipendente del codice, test e presente report; nessun nuovo
Gate senza decisione separata del titolare.
