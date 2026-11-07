# RD-TSC-V2-D3-S2-SPATIAL-V2-OFFLINE-IMPLEMENTATION-01

## Baseline e riconciliazione

Implementazione offline isolata sulla baseline GitHub
`4e8eabb6f3b62f1db3b2e0d620aed4663d03ddd4`, branch
`codex/tactical-state-contract-v1`. HEAD locale/remoto conformi e working tree
pulito prima delle modifiche. TODO, experiment register, specifica Spatial V2 e
remediation R1–R5 sono stati riconciliati; non esisteva un'implementazione
equivalente.

La revisione indipendente R1–R5 viene registrata **VALIDATO** esclusivamente nel
perimetro documentale dei cinque rilievi. Non valida codice, accuratezza,
generalizzazione, integrazione o runtime.

## File implementati

- `scripts/v5_tactical_semantic_support_s2_spatial_v2.py` — schema,
  vocabolario, validatore puro e derivazione label.
- `scripts/shadow_nli_spatial_relations_v2_inference.py` — judge opt-in,
  structured output, singolo trasporto e validazione post-parsing.
- `tests/test_v5_tactical_semantic_support_s2_spatial_v2.py` — test sintetici
  differenziali e mock del trasporto.

Nessun modulo esistente è stato modificato.

## Contratti e versioni

- contratto: `nli_spatial_relations_v2` `2.0.0`;
- schema: Draft 2020-12, ID
  `urn:football-data-lab:nli-spatial-relations-v2:2.0.0`;
- validatore: `nli_spatial_relations_v2_validator` `1.0.0`;
- label: `supported`, `contradicted`, `insufficient`;
- stato tecnico: `valid` oppure `not_evaluable`;
- percorso: `explicit_import_only`, una chiamata, retry/repair/fallback false;
- ogni risultato judge conserva `promotion_authorized=false`.

## Architettura isolata

Il validatore non esegue I/O e non importa client di modello. Controlla shape,
identità, NFC, offset code point, exact span, status/sentinelle, axis/value,
condizioni, fase, quantificatori, polarità, comparison e coerenza label/witness.
Non modifica l'input, non risolve coreferenze e non corregge label.

Il judge è inerte all'importazione. Solo `judge_pair()` costruisce il payload e
invoca una volta il trasporto predefinito o iniettato. Parsing/validazione
invalidi producono risultato non promotabile; eccezioni di trasporto o JSON non
attivano retry, repair o fallback. Il modulo non è collegato a runner, bridge,
S2, API o panel.

`compatible` è ammesso soltanto come comparison subject/reference. Quando
usato, il validation result imposta
`semantic_compatibility_verified=false`: la coerenza strutturale è verificata,
la coreferenza no.

## Matrice test e risultati

| Area | Copertura | Esito finale |
|---|---|---|
| Identità/schema | required, extra fields, versioni | PASS |
| Axis/value | associazioni, `stable`, asse incompatibile | PASS |
| Status/sentinelle | claim/evidence, unknown/absent/ambiguous | PASS |
| Unicode/ancore | NFC, offset, exact-span, duplicati, overlap | PASS |
| Contesto | condizioni e fase | PASS |
| Quantificatori | forza, numeric/literal | PASS |
| Polarità | negazione esplicita e incompatibilità | PASS |
| Comparison | coerenza, assi diversi, mismatch | PASS |
| Label | supported/contradicted/insufficient, mismatch fail-closed | PASS |
| `compatible` | q3_04 rappresentabile, non semanticamente verificato | PASS tecnico |
| Judge | import inerte, singola chiamata mock | PASS |
| Errori judge | witness malformato, timeout mock, JSON invalido | PASS fail-closed |

Primo run: 16 test, 6 PASS e 10 FAIL. Il difetto era nel validatore appena
implementato: `conditions.status=absent` veniva intercettato dalla regola
sentinella generica prima del confronto specifico. Corretto l'ordine; la
ricognizione diretta ha inoltre vietato `value=incompatible` quando gli assi
sono differenti e aggiunto il controllo di polarità esplicita.

Run finale: **16/16 PASS**, 0 FAIL, 0 errori.

## Comandi eseguiti

```text
python -m unittest tests.test_v5_tactical_semantic_support_s2_spatial_v2 -v
```

Il comando è stato eseguito due volte sulla sola suite nuova: primo run
diagnostico fallito come sopra; secondo run finale PASS. Non sono state eseguite
suite storiche, campagne Gold, Gate o inferenze.

Controlli statici:

```text
git diff --check
git diff --quiet HEAD -- <moduli legacy interessati>
```

## Differenze rispetto alla specifica

Nessuna differenza semantica deliberata. Lo schema è esposto come dizionario
Draft 2020-12 senza dipendenza `jsonschema`; il validatore manuale applica le
regole incrociate normative. Il judge restituisce un envelope sperimentale
locale con witness e validation result, ma non viene adattato alla shape S2:
la decisione sul futuro record/bridge resta fuori perimetro.

## Assenza di inferenze reali

- i test usano esclusivamente `transport` iniettato;
- nessun test invoca `_default_transport`;
- nessuna chiamata Ollama/Qwen, VPS, API o rete;
- import del judge verificato inerte;
- conteggio mock verificato esattamente pari a uno;
- retry, repair e fallback dichiarati e testati `false`.

## Compatibilità legacy

Il diff non modifica NLI V2, Spatial V1, bridge Spatial V1, S1, adapter/boundary
S2, retrieval, fixture, Gold, pipeline, API, RAG, Chroma o panel. Un controllo
Git mirato sui quattro moduli legacy direttamente interessati ha restituito
`LEGACY_FILES_UNCHANGED=PASS`. Nessuna selezione automatica del nuovo judge.

## Limiti residui

- `compatible` resta un'asserzione dello stesso modello, non una coreferenza
  verificata.
- Lo schema/validatore provano struttura e coerenza interna, non accuratezza.
- `q3_04` è soltanto rappresentabile; non è stato inferito né corretto.
- L'envelope judge non è integrato nel record S2.
- Nessuna generalizzazione, qualità runtime o affidabilità del modello è
  dimostrata.

## Matrice probatoria A/B/C

| Conclusione | Livello |
|---|---|
| Moduli nuovi isolati e legacy invariato | A — dimostrato dal diff |
| 16 test finali PASS | A |
| Import inerte e singola chiamata mock | A |
| Derivazione/fail-closed conformi nei casi testati | A |
| `compatible` è coreferenza semanticamente corretta | C — ipotesi modello |
| Spatial V2 corregge `q3_04` | non dimostrato |
| Spatial V2 generalizza | non dimostrato |

## Decisione

**PASS tecnico offline** nel perimetro deterministico testato. Implementazione
nuova **IMPLEMENTATO**; test differenziali **ESEGUITO** e proprietà coperte
**VALIDATO** offline. Questo non costituisce integrazione, certificazione o
validazione semantica.

## Stati ufficiali

| Componente | Stato |
|---|---|
| Progettazione `q3_04` | **ESEGUITO** |
| Specifica e remediation R1–R5 | **ESEGUITO** |
| Revisione documentale mirata R1–R5 | **VALIDATO** |
| Implementazione Spatial V2 offline | **IMPLEMENTATO** |
| Test deterministici nuovi | **ESEGUITO** |
| Proprietà offline coperte | **VALIDATO** |
| Efficacia semantica | **BLOCCATO** |
| Gate runtime | **BLOCCATO** |
| Integrazione | **BLOCCATO** |
| Certificazione | **BLOCCATO** |
| Provenance Spatial V1 | **VALIDATO** |

Unico prossimo passo: revisione indipendente di codice, test e report. Nessuna
integrazione o inferenza è autorizzata.
