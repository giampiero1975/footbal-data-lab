# TSC V2 D3 — Semantic Evidence Support Design

## 1. Identità e perimetro

- Attività: `RD-TSC-V2-D3-SEMANTIC-SUPPORT-DESIGN-01`
- HEAD iniziale: `d6da896f07ed20db72e91dcd2fdb3b8348a992e1`
- Implementazione D3: commit tecnico `f544589`
- Metodo: analisi statica di codice, test e report esistenti.
- Nessun test, modello, retrieval, Chroma/API o runtime eseguito.

La progettazione D3 e la relativa implementazione offline risultano già registrate.
Non esisteva una specifica equivalente del support checker.

## 2. Limite dimostrato

D3 verifica oggi che citation ID e relation/requirement ref esistano, che gli anchor
siano sottostringhe esatte delle evidenze e che i binding tattici coincidano col
piano. Non verifica che l'intera proposizione del claim sia implicata dall'anchor.

Inoltre il claim trasportato non possiede un campo atomico `statement`: contiene ID,
dimensioni, bindings, polarità, evidenze e support mode, mentre il linguaggio naturale
è soltanto nel testo più ampio della sezione. Un assessor non può quindi sapere quale
proposizione precisa debba giudicare senza una decomposizione ulteriore.

Il parametro sistemico `support_assessments` di
`v5_tactical_state_dual_output_v1.py:176–340` accetta `supported`, `unsupported` o
assenza, ma non produce tali esiti. Nei test, `supported` è una fixture sintetica che
dimostra soltanto la macchina degli stati. Il wrapper non fornisce assessment, quindi
il runtime resta correttamente `not_evaluable`.

## 3. Catena D3 e autorità

| Passaggio | Input | Output/autorità | Controllo presente | Mancanza/fail-closed |
|---|---|---|---|---|
| Question plan | domanda | planner autorevole | parsing e requisiti V1/V2 | ambiguità=`not_evaluable` |
| Applied plan | question plan | sistema autorevole | validità V1/V2, refs, fingerprint | invalidità=`blocked` |
| Explanation | prompt + piano + F | Qwen, non autorevole | schema/cardinalità/refs | malformed=`blocked` o trasporto=`not_evaluable` |
| Claims | sezione Qwen | record strutturati | ID, dimensions, bindings, polarità | manca proposizione atomica |
| Anchors | evidence refs + exact text | Qwen cita, sistema risolve | presenza byte/NFC nell'evidenza | non prova entailment |
| Semantic assessment | claim↔evidenza | oggi input esterno sintetico | stato consumato fail-closed | nessun produttore affidabile |
| Audit V1 | sola prosa + plan | sistema, lessicale | facet/details/issue note | keyword non prova verità |
| Promotion | tutti i controlli | sistema | `blocked/not_evaluable/validated` | senza supporto niente promozione |

Il modello generatore non deve mai scrivere o autocertificare l'assessment.

## 4. Inventario dei componenti disponibili

| Componente | File/funzione | Proprietà verificata | Limiti | Riutilizzabile in D3 |
|---|---|---|---|---|
| Resolver ID/ref D3 | `v5_tactical_state_dual_output_v1.py::documentary_diagnostic` | esistenza, tipo, cardinalità, copertura | nessuna semantica | sì, invariato |
| Anchor D3 | stessa funzione, `evidence_anchor_mismatch` | exact text presente nella F | presenza ≠ supporto | sì, precondizione |
| Bindings D3 | `relation_bindings()` e mismatch per sei dimensioni | claim strutturato coerente col piano | non collega la prosa al binding | sì, precondizione |
| Polarità D3 | `documentary_diagnostic()` | enum; negated blocca, uncertain non valuta | non analizza intera prosa | sì, precondizione |
| Audit V1 | `v5_tactical_query_plan_v1.py::audit_answer` | facet, dettagli, cue e contraddizioni note | lessicale, nessun entailment | sì, controllo separato |
| Audit relazionale | `audit_relations()` | co-occorrenza, attore-task, polarità, citation relevance | `semantic_support_verified=false`; non bloccante | sì, diagnostica/feature bounded |
| NLI diretto V2 | `benchmark_direct_three_label_nli_v2.py` | supported/contradicted/insufficient claim↔fonte | modello Qwen locale; 29/30 riportato su 30 casi/3 estratti; gold non indipendente e report originario non archiviato | candidato shadow, non gate |
| NLI/alignment shadow | `judge_rag_v5_alignment_controls_v1.py`, V2 A/B | entailment, scope, quantificatori | risultati provvisori e falsi positivi documentati | candidato per calibrazione |
| Ragas Faithfulness | adapter/diagnostici Ragas 0.4.3 | estrazione statements + verdict LLM | due chiamate LLM, errori/diagnostica storica, non indipendenza garantita | no gate diretto |
| Gemini reviewer | `review_rag_v5_gemini*.py` | review source-grounded esterna | rete/costo/privacy; non hook D3 certificato | shadow o revisione separata |
| Groq reviewer | `groq_free_reviewer_v1.py` | rubrica esterna opt-in | false contestazioni sulle citazioni nel G4; affidabilità generale non validata | non gate |
| Gold E/V | `validate_relational_gold_preparation_v2.py` | provenienza, reviewer, judgement e freeze | valida artefatti, non produce giudizi | sì, per dataset/calibrazione |
| Worksheet umano | `build_rag_v5_quality_adjudication_worksheet_v1.py` | prepara claim/evidenze | esplicitamente non assegna score | sì, S4 |
| Lint tattici | `lint_glerean_answers_v1.py` e regole audit | contraddizioni documentate specifiche | copertura stretta | sì, failure deterministiche |

Conclusione inventario: esistono materiali riutilizzabili, ma nessun produttore di
`support_assessments` è oggi VALIDATO come gate automatico D3.

## 5. Contratto formale dell'assessment

### 5.1 Delta minimo necessario al claim

Ogni claim deve aggiungere:

```json
{
  "claim_id": "claim:...",
  "statement": "proposizione atomica completa",
  "section_span": {"start": 0, "end": 42},
  "relation_refs": ["relation:..."],
  "requirement_refs": ["question_part:..."],
  "bindings": {},
  "polarity": "affirmed",
  "conditions": ["testo o ref condizione"],
  "evidence_refs": ["F1"],
  "evidence_anchors": [],
  "support_mode": "direct"
}
```

`statement` deve coincidere esattamente con lo span NFC della sezione. Gli span non
possono sovrapporsi in modo incompatibile e ogni proposizione tattica sostanziale
della sezione deve appartenere ad almeno un claim. La copertura completa della prosa
è un controllo distinto; testo descrittivo non classificato è `not_evaluable`.

### 5.2 Assessment sistemico non model-authored

```json
{
  "schema": "tactical_documentary_support_assessment_v1",
  "attempt_id": "...",
  "plan_fingerprint": "sha256:...",
  "claim_id": "claim:...",
  "statement_sha256": "sha256:...",
  "evidence": [
    {"evidence_ref": "F1", "evidence_sha256": "sha256:...",
     "verdict": "supported", "reason_codes": ["exact_atomic_statement"]}
  ],
  "aggregate_verdict": "supported",
  "assessor": {"kind": "deterministic", "name": "...", "version": "...",
               "config_sha256": "sha256:..."},
  "created_at": "..."
}
```

Il record è prodotto dopo il parsing da un componente separato. Il payload Qwen non
contiene assessment, aggregate verdict, assessor o reason code. Digest di piano,
statement ed evidenze impediscono il riuso su input diversi.

### 5.3 Stati

**`supported`** richiede:

- claim atomico, attribuibile e con condizioni/quantificatori conservati;
- bindings e polarità coerenti col piano;
- almeno una evidenza che dimostri l'intera proposizione, oppure una regola bounded
  autorizzata con tutte le premesse supportate;
- nessuna evidenza citata che dimostri una contraddizione non risolta;
- assessor e input fingerprint verificabili.

**`unsupported`** richiede una violazione positiva: evidenza incompatibile,
attore/fase/direzione/polarità errati, condizione necessaria omessa, generalizzazione
oltre lo scope, causalità invertita o regola bounded non rispettata. La semplice
assenza di prova non è `unsupported`.

**`not_evaluable`** copre evidenza insufficiente/ambigua, claim non atomico,
combinazione multi-fonte non attribuibile, contesto mancante, disagreement non
risolto, assessor indisponibile o classe non coperta.

Aggregazione conservativa per claim atomici: `unsupported` se esiste una
contraddizione probante; altrimenti `supported` solo se almeno una singola evidenza
supporta l'intera proposizione e le altre non la contraddicono; altrimenti
`not_evaluable`. Claim che richiedono fonti congiunte devono essere separati oppure
usare una regola compositiva registrata; non si concatenano automaticamente le F.

## 6. Alternative

| Alternativa | Copertura/affidabilità | Costo/complessità | Falsi positivi e fail-closed | Compatibilità D3 |
|---|---|---|---|---|
| S1 deterministica limitata | alta affidabilità su citazioni letterali atomiche, ID/binding/polarità e regole note; copertura bassa | bassa | rischio basso se whitelist chiusa; resto `not_evaluable` | immediata e modulare |
| S2 revisore indipendente | copertura potenzialmente alta | latenza/token/rete e calibrazione; Qwen uguale al generatore non è indipendente | errori NLI/reviewer già osservati; serve gold e soglie | solo shadow finché non VALIDATO |
| S3 ibrida | S1 decide classi strette, reviewer separato tenta le altre, disagreement/insufficienza chiudono | media-alta | miglior equilibrio se il reviewer non ha autorità esclusiva | raccomandata |
| S4 umana | massima adattabilità, idonea a gold/certificazione | lenta e non automatica | richiede doppia revisione/adjudication e provenienza | essenziale per calibrazione e casi indecidibili |

### Decisione

Raccomandata **S3 incrementale**, iniziando da **S1 soltanto**. Il primo incremento
non introduce alcuna chiamata modello:

1. claim atomico con statement/span;
2. checker deterministico per exact atomic quotation, binding, polarità, condizioni e
   contraddizioni whitelist già documentate;
3. tutto il resto `not_evaluable`;
4. assessment content-addressed separato.

S2 resta shadow fino a un benchmark claim-level congelato, indipendente e
source-disjoint che includa supporto parziale, negazioni, causalità, quantificatori,
scope, condizioni e multi-fonte. Un reviewer non deve essere lo stesso modello e la
stessa configurazione del generatore; indipendenza di processo e versione deve essere
registrata. Nessuna soglia è proposta senza dati nuovi.

S4 produce/adjudica il gold e rimane obbligatoria per certificazione o disagreement
non risolti. L'eventuale reviewer non sostituisce S4.

## 7. Direct, bounded inference e uncertainty

### Direct

S1 può dichiarare `supported` soltanto quando lo `statement` atomico è, dopo NFC e
normalizzazione newline, identico a un anchor continuo dell'evidenza, senza parole,
negazioni, quantificatori o condizioni aggiunti. La citazione può essere resa nella
prosa, ma la proposizione valutata resta l'estratto esatto. Parafrasi, riassunti e
traduzioni non rientrano in questa classe.

### Bounded inference

Richiede una rule registry versionata. Ogni regola dichiara:

- ID/versione e dominio;
- tipi e numero delle premesse;
- trasformazione esatta;
- condizioni e casi vietati;
- output consentito;
- test positivi, negativi e boundary;
- provenance e approvazione.

Tutte le premesse devono essere `supported`; la conclusione deve essere prodotta
dalla regola, non da Qwen. Non esistono oggi regole approvate per D3: ogni
`bounded_inference` resta `not_evaluable`.

### Uncertainty

Registra il limite ma non soddisfa un requisito, non copre una relazione normativa e
non contribuisce alla promozione. Non diventa `supported` per prudenza stilistica.

## 8. Protezioni contro falsi positivi

- atomizzazione obbligatoria: nessun verdict unico per claim compositi;
- statement/span immutabili e digestati;
- evidence per claim, senza concatenazione indiscriminata;
- confronto esatto di attore, fase, polarità, condizioni e quantificatori;
- `insufficient` mappato a `not_evaluable`, mai a contraddizione;
- generalizzazioni (“sempre”, “ogni”, “garantisce”) richiedono lo stesso scope nella
  fonte;
- causa/effetto e direzione comparativa devono essere espliciti;
- una fonte pertinente ma non probante non è supporto;
- condizioni omesse impediscono `supported`;
- disagreement fra checker/reviewer o fra reviewer produce `not_evaluable` e record
  di adjudication richiesto;
- claim plausibile tatticamente ma non documentato resta `not_evaluable` o
  `unsupported` solo con controevidenza positiva;
- audit V1 positivo e NLI positivo restano controlli necessari/ausiliari, non prova
  singola sufficiente.

## 9. Impatto minimo futuro

| Componente | Delta futuro | Invarianti |
|---|---|---|
| D3 transport schema | aggiungere statement, span, conditions, requirement refs per claim | piano/model authority invariata |
| nuovo support module | produrre assessment S1 content-addressed | nessun modello/retrieval |
| diagnostic D3 | consumare record verificato, non dict libero | stessa precedenza blocked/not_evaluable |
| audit adapter | nessuna modifica | audit V1 invariato |
| runner | chiamare S1 solo nel flag D3 | legacy/V1/V2 invariati |
| report | conservare input hash, verdict e assessor | raw e assessment separati |
| S2 futuro | adapter shadow separato | nessuna promozione fino a VALIDATO |
| API/pannello | nessun delta prima fase | fuori perimetro |

Il parametro libero `support_assessments={claim_id: status}` deve essere sostituito in
produzione da record validati contro schema, digest e assessor allowlist. Può restare
solo come fixture interna ai test esistenti durante una migrazione esplicita.

## 10. Piano differenziale futuro (non eseguito)

Nuovi casi giustificati dal delta:

1. statement atomico identico all'anchor → S1 supported;
2. aggiunta di quantificatore, condizione, soggetto o causalità → not_evaluable;
3. negazione/direzione opposta esplicita → unsupported;
4. fonte pertinente ma parziale → not_evaluable;
5. span errato, overlap incompatibile o prosa sostanziale senza claim → blocked o
   not_evaluable secondo evidenza positiva;
6. digest di piano/statement/evidenza alterato → blocked;
7. claim multi-fonte composito → not_evaluable;
8. regola bounded assente, sconosciuta o con premessa non supportata → not_evaluable;
9. rule registry positiva/negativa/boundary quando esisterà una regola approvata;
10. verdict S2 supported/contradicted/insufficient e disagreement S1/S2, solo shadow;
11. assessor coincidente col generatore o config non allowlisted → not_evaluable;
12. assessment model-authored nel transport → schema failure;
13. regressione D3: anchor solo non promuove e V1/V2/default restano invariati.

Non vanno ripetuti i 17 casi D3 o le campagne NLI storiche salvo regressioni
direttamente interessate dal futuro delta.

## 11. Rischi residui e decisioni da approvare

Rischi residui:

- S1 ha copertura intenzionalmente bassa;
- l'atomizzazione automatica può introdurre o nascondere proposizioni;
- S2 può condividere bias/dati col generatore anche usando un processo diverso;
- NLI locale e reviewer esterni non sono certificati come gate;
- contenuto distribuito su più fonti richiede una semantica compositiva non definita;
- revisione umana richiede governance, versionamento e gestione dei disaccordi.

Decisioni richieste prima dell'implementazione:

1. approvare S3 incrementale con prima fase S1-only;
2. approvare l'estensione claim con statement/span/conditions;
3. approvare la regola exact-atomic come unica classe automaticamente supported
   nella prima fase;
4. approvare schema content-addressed e allowlist degli assessor;
5. decidere protocollo Gold S4 e indipendenza minima per un futuro S2;
6. mantenere bounded inference non valutabile finché non esiste una rule approvata;
7. mantenere API/pannello e runtime fuori dalla prima implementazione.

## 12. Stati ufficiali

- semantic support design: **VALIDATO**;
- support checker S1/S3: **DA FARE** previa approvazione;
- D3 deterministico offline: **VALIDATO**;
- D3 semantic support automatico: **BLOCCATO**;
- Gate runtime D3: **BLOCCATO**;
- integrazione runtime: **BLOCCATO**;
- certificazione: **BLOCCATO**.

La specifica non autorizza implementazione, reviewer AI o nuovo Gate.
