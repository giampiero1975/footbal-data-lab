# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-01

## Baseline e perimetro

- baseline GitHub: `ad8344c2d9ef568ab0c0d6fadd80cb10605a2f32`;
- branch: `codex/tactical-state-contract-v1`;
- report architetturale:
  `tactical-semantic-support-s2-spatial-v2-witness-architecture-01.md`;
- perimetro: implementazione e verifica offline opt-in, shadow-only;
- nessuna inferenza, rete, VPS, Gate, benchmark o deploy.

File applicativi:

- nuovo `scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py`;
- integrazione opt-in in
  `scripts/shadow_nli_spatial_relations_v2_inference.py`;
- nuova suite
  `tests/test_v5_tactical_semantic_support_s2_spatial_v2_extraction.py`.

Il validatore `v5_tactical_semantic_support_s2_spatial_v2.py` è invariato;
SHA-256 prima e dopo:
`06e071b50c69683c8ed69257a238c6fe53b00cc60ad589ec61ab1100b59a3b46`.

## Contratto di estrazione

Identità:

- `contract_id=nli_spatial_relations_v2_extraction`;
- `contract_version=1.0.0`;
- locator `nli_spatial_relations_v2_literal_locator/1.0.0`.

`EXTRACTION_SCHEMA` è distinto da `SPATIAL_V2_SCHEMA`. Conserva label,
comparison e le strutture semantiche di subject, axis, reference, value,
conditions, phase, quantifier e polarity. Al posto degli anchor usa soltanto
`selected_fragments`, lista di stringhe letterali non vuote.

Lo schema non contiene campi `source`, `start`, `end`, `anchors` o
`exact_span`. Il lato deriva esclusivamente dal contenitore:
`claim_relation` usa il claim; `evidence_relation` usa l'evidence. Nessuna
conversione implicita da witness V2 o artefatti storici è prevista.

## Localizzatore deterministico

`materialize_extraction()` esegue soltanto operazioni pure:

1. valida shape, identità, tipi, vocabolari e frammenti;
2. cerca tutte le occorrenze letterali nel solo lato assegnato;
3. accetta esclusivamente `occurrence_count == 1`;
4. usa indici Python Unicode code-point e intervallo `[start,end)`;
5. ricontrolla `source_text[start:end] == selected_fragment`;
6. materializza gli anchor del contratto V2 senza modificare la semantica;
7. invoca integralmente `validate_spatial_v2()` invariato.

Non usa casefold, NFC automatico, fuzzy matching, correzioni, prima occorrenza,
ricerca sul lato opposto, retry, repair o fallback. Zero corrispondenze e
corrispondenze multiple producono `not_evaluable`, `witness=null` e diagnostica
separata. Un witness materializzato ma semanticamente/strutturalmente invalido
resta `not_evaluable` con gli errori del validatore.

## Provenienza

Ogni record conserva:

- field ID completo;
- lato obbligatorio;
- SHA-256 del testo sorgente;
- frammento selezionato;
- numero di occorrenze;
- start/end oppure `null`;
- risultato `localized`, `missing`, `ambiguous` o `slice_mismatch`.

Il contenitore conserva identità/versione di contratto e locator, digest
dell'estrazione, digest di claim/evidence, stato e `record_sha256` canonico.
`verify_materialization()` ricalcola l'intero risultato puro: qualunque modifica
a digest, record, witness o diagnostica produce
`E_EXTRACTION_PROVENANCE_MISMATCH`. La provenienza resta separata dal witness
finale.

## Integrazione opt-in

`judge_pair()` accetta il nuovo keyword booleano `extraction_locator`, default
`False`.

- `False`: usa senza variazioni `INSTRUCTION`, `SPATIAL_V2_SCHEMA`, parsing,
  validazione e forma del risultato legacy.
- `True`: usa `EXTRACTION_INSTRUCTION`, `EXTRACTION_SCHEMA`, una sola chiamata
  di trasporto e quindi il localizzatore puro.

Modello, temperatura 0, contesto 4096, `num_predict`, timeout 180/360,
`stream=false` e `think=false` restano invariati. Il descrittore opt-in dichiara
single generation e retry/repair/fallback falsi. Ogni risultato mantiene
`promotion_authorized=false`. Non esistono call site pubblici modificati né
attivazioni in API, pannello, retrieval o Gate.

## Test differenziali

Eseguita esclusivamente la nuova suite:

```text
python -m unittest tests.test_v5_tactical_semantic_support_s2_spatial_v2_extraction -v
```

Risultato: **12/12 PASS**. Copertura:

1. match univoci con offset e validazione finale;
2. frammento assente;
3. frammento ripetuto senza first-match;
4. frammento presente soltanto nel lato opposto;
5. `explicit/affirmed` non corretto dal locator;
6. comparison/label incoerenti non corretti;
7. Unicode e punteggiatura con slice letterale;
8. percorso legacy e schema storico invariati;
9. provenienza alterata;
10. assenza di campi di localizzazione nello schema modello;
11. opt-in mock con una chiamata e zero retry/repair/fallback;
12. parsing, shape e risposta malformati fail-closed.

Regressione direttamente interessata:

```text
python -m unittest tests.test_v5_tactical_semantic_support_s2_spatial_v2 -v
```

Risultato: **21/21 PASS**. Non sono state ripetute campagne storiche, runtime
`q3_04` o suite non interessate.

## Invarianti e limiti

Confermati:

- contratto e validatore Spatial V2 invariati;
- default legacy invariato;
- nessuna modifica a modello, timeout, token, retry/repair/fallback;
- nessuna modifica a Tactical State Contract, retrieval, collection, API,
  pannello o produzione;
- nessuna dipendenza esterna aggiunta;
- import e localizzatore privi di I/O o chiamate modello.

Il locator prova soltanto presenza e unicità letterale. Non prova pertinenza,
specificità o verità semantica; uno span troppo ampio può essere localizzato ma
restare semanticamente insufficiente. L'efficacia su output Qwen reale non è
stata verificata. Runtime, Gate, integrazione pubblica e certificazione restano
bloccati e richiedono decisioni separate.

## Decisione e stati

Flusso: Attività = extraction/locator; Script = nuovo modulo, judge opt-in e
suite differenziale; Commit = changeset tecnico-documentale; Report = questo
documento; Risultato = 12/12 nuovi + 21/21 regressioni PASS; Decisione = chiudere
l'implementazione offline senza runtime o integrazione.

| Componente | Stato |
|---|---|
| Contratto di estrazione e locator | **IMPLEMENTATO** |
| Test differenziali e regressioni mirate | **ESEGUITO** |
| Proprietà offline e fail-closed interessati | **VALIDATO** |
| Efficacia Qwen reale | **BLOCCATO** |
| Runtime/Gate Spatial V2 | **BLOCCATO** |
| Integrazione pubblica e certificazione | **BLOCCATO** |

Nessuna ulteriore attività è autorizzata da questo closeout.
