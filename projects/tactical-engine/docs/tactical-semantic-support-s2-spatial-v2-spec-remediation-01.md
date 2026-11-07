# RD-TSC-V2-D3-S2-SPATIAL-V2-SPEC-REMEDIATION-01

## Baseline verificata

Remediation esclusivamente documentale sulla baseline GitHub
`31007f2ccc5c7279d20ca0edc165237965924ad3`, branch
`codex/tactical-state-contract-v1`. HEAD locale/remoto conformi e working tree
pulito prima delle modifiche. Nessuna remediation equivalente risultava già
registrata.

Sono stati riconciliati TODO, experiment register, specifica Spatial V2, design
`q3_04` e le sole interfacce reali necessarie. Non sono stati eseguiti test,
inferenze, Gate o runtime; nessun file applicativo, Gold, fixture o artefatto è
stato modificato.

## Evidenze disponibili

- Spatial V1 richiede già il confronto relazionale, ma restituisce solo label.
- `q3_04` conserva claim/evidence integri e produce il falso `supported` sia in
  NLI V2 sia in Spatial V1.
- Routing, parsing e provenance sono già stati verificati e non vengono riaperti.
- La specifica `2.0.0` introduce witness, ancore e validazione deterministica,
  senza pretendere comprensione semantica indipendente.

## Analisi e correzioni R1–R5

| Rilievo | Esito | Correzione documentale |
|---|---|---|
| R1 — `area_extent/stable` | Parzialmente confermato | `stable` era già nell'enum generale, ma mancava un vincolo schema per asse. Aggiunti `allOf` condizionali per tutte le associazioni axis/value, incluso `area_extent = expanding|contracting|stable`. |
| R2 — insufficient/not_evaluable | Confermato | Definita precedenza totale in sei fasi più controllo label; claim indeterminata/non rappresentabile → `not_evaluable`; evidence assente/unknown/ambiguous con claim definita → `insufficient`. Eliminati gli esiti «a seconda del caso». |
| R3 — coreferenza/compatible | Confermato | Confrontate A/B; scelta A. `compatible` resta asserzione shadow del modello, strutturalmente verificabile ma semanticamente non dimostrata; nuovo flag progettuale `semantic_compatibility_verified=false`. |
| R4 — status/value/anchor | Confermato | Aggiunta matrice normativa per tutte le otto famiglie, status ammessi, sentinelle, cardinalità, ancore e codice fail-closed unico. |
| R5 — quantificatori | Confermato | Aggiunta matrice evidence→claim, relazione di forza chiusa, numeric senza ordinamento, always/never, polarità e risultato conservativo per confronti non determinabili. |

## Decisione su `compatible`

### A — compatibilità dichiarata dal modello

Verificabili: shape, ancore, status, ID, coerenza locale e assenza di sentinelle.
Non verificabile: la correttezza della coreferenza/parafrasi. Rischio: falsa
equivalenza internamente coerente. Beneficio: relazioni formulate diversamente
restano rappresentabili. Fail-closed su ogni incoerenza strutturale; nessuna
promozione e flag semantico `false`.

### B — compatibilità vietata

Verificabile: sola identità deterministica. Non verificabile e quindi esclusa:
ogni parafrasi. Riduce falsi positivi ma aumenta falsi negativi e rende
irraggiungibile la contraddizione `q3_04`, perché le due formulazioni del soggetto
non sono identiche.

### Scelta

**Alternativa A**, esclusivamente shadow. È l'unica delle due che conserva
l'obiettivo di rappresentabilità senza introdurre resolver, euristiche o seconda
inferenza. Non viene presentata come attestazione semantica indipendente.

## Matrice normativa aggiornata

| Situazione | Risultato unico | Codice/regola |
|---|---|---|
| Campo mancante, tipo/enum/extra field errato | `not_evaluable` | `E_SCHEMA_INVALID` |
| Ancora invalida o source errata | `not_evaluable` | `E_ANCHOR_INVALID` |
| Status/value/sentinella incoerenti | `not_evaluable` | `E_STATUS_VALUE_INCONSISTENT` |
| Asse e valore incompatibili | `not_evaluable` | `E_AXIS_VALUE_INCOMPATIBLE` |
| Claim obbligatoria absent/unknown/ambiguous | `not_evaluable` | target non definito |
| Evidence absent/unknown/ambiguous con claim definita | `insufficient` | insufficienza documentata |
| Relazione fuori vocabolario | `not_evaluable` | limite contrattuale |
| Subject/reference implicito senza `compatible` | `not_evaluable` | witness incoerente |
| Comparison incoerente | `not_evaluable` | `E_COMPARISON_INCONSISTENT` |
| Relazione comparabile, valore/polarità incompatibile | `contradicted` | derivazione deterministica |
| Relazione comparabile, valore compatibile e quantificatore sufficiente | `supported` | derivazione deterministica |
| Relazione valida ma differente/non conclusiva | `insufficient` | derivazione deterministica |
| Nessuna label univoca | `not_evaluable` | witness non deterministico |
| Label proposta diversa dalla derivata | `not_evaluable` | `E_LABEL_WITNESS_MISMATCH` |

La specifica contiene la matrice completa status/value/anchor per entity, axis,
reference, value, conditions, phase, quantifier e polarity. Ogni combinazione
non elencata fallisce chiusa.

## Coerenza schema, vocabolario e algoritmo

- Tutti i valori del vocabolario sono presenti nello schema.
- Ogni asse accetta soltanto i propri valori tramite condizioni `allOf`.
- `stable` è rappresentabile per `distance_change` e `area_extent`, senza
  diventare valido su altri assi.
- Sentinelle e status sono legati dalla matrice normativa.
- Le ancore restano exact-span, NFC e source-specific.
- La precedenza separa invalidità tecnica da insufficienza documentata.
- `not_evaluable` rimane uno stato del boundary, non una quarta label.
- Quantificatori diversi non diventano automaticamente contraddittori.
- Il validatore non corregge label, non riscrive witness e non chiama modelli.

Non sono state rilevate contraddizioni nuove causate dalla remediation.

## Verifica concettuale `q3_04`

La rappresentabilità è preservata sulla carta:

1. subject claim/evidence differenti ma dichiarati `compatible`, con ancore
   esatte e compatibilità semanticamente non verificata;
2. reference «tra la linea difensiva e la porta» con identità locale e
   comparison `same`;
3. asse `space_availability` in entrambe le relazioni;
4. claim `abundant`, evidence `scarce`;
5. coppia incompatibile nel vocabolario;
6. label deterministica `contradicted`; un `supported` fallisce chiuso.

Questo prova soltanto che il contratto può rappresentare il caso. Non prova che
il modello produca il witness corretto o che il falso positivo sia risolto.

## Limiti residui

- `compatible` è prodotto dallo stesso modello e non è verificato semanticamente.
- Le ancore provano presenza testuale, non interpretazione.
- Il vocabolario può non rappresentare relazioni future.
- Il witness può essere semanticamente errato ma internamente coerente.
- Accuratezza, generalizzazione e impatto su `q3_04` richiedono attività future
  separatamente autorizzate.

## Matrice probatoria A/B/C

| Conclusione | Livello |
|---|---|
| R1 reale: mancava binding schema axis/value | A — dimostrato |
| Precedenza R2 ora completa e non sovrapposta | A come proprietà documentale |
| Matrice R4 e quantificatori R5 sono deterministici | A come proprietà documentale |
| Alternativa B impedirebbe la rappresentabilità della parafrasi q3_04 | A rispetto alle regole proposte |
| `compatible` dichiarato corrisponde a coreferenza reale | C — ipotesi del modello |
| q3_04 è rappresentabile dal contratto corretto | A |
| Spatial V2 correggerà q3_04 | C |
| Spatial V2 migliorerà accuratezza generale | C |

## Decisione finale

I cinque rilievi sono chiusi a livello di specifica documentale. L'architettura
resta invariata: contratto opt-in, una generazione, nessun retry/repair/fallback,
validatore deterministico e percorso shadow non promotabile.

La specifica corretta è **ESEGUITO**, non **VALIDATO**: richiede ancora revisione
indipendente. Nessuna implementazione è autorizzata da questa remediation.

## Stati ufficiali

| Attività/componente | Stato |
|---|---|
| Progettazione semantica `q3_04` | **ESEGUITO** |
| Specifica Spatial V2 | **ESEGUITO** |
| Remediation documentale R1–R5 | **ESEGUITO** dopo pubblicazione |
| Validazione indipendente della specifica corretta | **DA FARE** |
| Implementazione Spatial V2 | **DA FARE** |
| Efficacia semantica | **BLOCCATO** |
| Gate runtime | **BLOCCATO** |
| Integrazione | **BLOCCATO** |
| Certificazione | **BLOCCATO** |
| Provenance Spatial V1 | **VALIDATO** |

Unico prossimo passo: revisione indipendente della specifica corretta e nuova
decisione esplicita del titolare. Nessuna implementazione o inferenza.
