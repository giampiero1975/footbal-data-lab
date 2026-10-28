# Protocollo indipendente Gold E / Gold V v1

Data di preparazione: 2026-10-28  
Attività: `RD-RELATIONAL-GOLD-E-V-PREPARATION-01`  
Ambito: preparazione metodologica e infrastrutturale, senza casi annotati né benchmark.

## 1. Scopo e separazione

Il protocollo definisce due riferimenti umani distinti:

- **Gold E** misura l'estrazione dei requisiti tattici dalla sola domanda;
- **Gold V** misura il riconoscimento delle relazioni nella risposta usando i
  requisiti Gold E già corretti e congelati.

Gold E viene annotato senza mostrare al revisore `relation_requirements()`,
l'output dell'audit o una risposta Qwen. Gold V non può modificare né
reinterpretare silenziosamente Gold E dopo aver visto la risposta. Un errore
del riferimento richiede una revisione tracciata e una nuova versione.

Il regression set include casi già usati nello sviluppo. L'independent gold
set include soltanto casi selezionati prima dell'esecuzione, mai usati per
correggere l'audit e congelati prima della valutazione. Un caso indipendente
usato successivamente per lo sviluppo passa a `retired_from_independent` e non
può contribuire alle successive stime indipendenti.

Sono esclusi dall'independent gold iniziale: controesempi delle sette
remediation, test unitari del planner/audit, Drive11, Coverciano V10, risposte
corrette dall'audit e annotazioni ricavate dalle decisioni dell'audit.

## 2. Inventario riutilizzato

Il protocollo riusa senza duplicare:

- `evaluation/annotations/` per annotazioni e template;
- `eval/claim_fidelity_gold_v1.json` come precedente metodologico per etichette
  claim-evidenza, non come gold relazionale;
- `scripts/build_rag_v5_quality_adjudication_worksheet_v1.py` per il principio
  worksheet non distruttivo e revisione atomica;
- `scripts/validate_rag_v5_prospective_manifest_v1.py` per hash, controlli
  fail-closed e separazione holdout;
- `docs/rag-v5-quality-holdout-adjudication-rubric-20261022.md` per la
  distinzione fra aderenza, fedeltà, precisione tattica e validità formale
  delle citazioni;
- `evaluation/runtime_evidence_manifest_v1.json` come precedente di inventario
  con SHA-256.

Nessuno di questi artefatti rappresentava già Gold E o Gold V relazionale.

## 3. Selezione dei casi

La selezione precede qualunque esecuzione dell'audit e documenta per ogni caso:

1. origine e `source_id` stabile;
2. data di acquisizione;
3. trasformazioni del testo;
4. utilizzo precedente nello sviluppo;
5. screening di duplicati testuali e casi semanticamente equivalenti;
6. motivazione dell'inclusione;
7. conflitti d'interesse di annotatori e revisori.

Il campionamento deve essere definito prima di osservare le prestazioni e deve
coprire categorie tattiche concordate, domande esplicite e aperte, più livelli
di complessità e formulazioni realistiche. Non si bilancia il set in funzione
dei successi o fallimenti osservati del motore.

Lo screening usa prima corrispondenze esatte/hash e poi revisione umana delle
somiglianze semantiche. `possible_duplicate` non viene promosso automaticamente
a indipendente. La decisione e gli ID collegati restano nel record.

## 4. Annotazione Gold E

### 4.1 Procedura cieca

L'annotatore riceve soltanto domanda, provenienza e istruzioni. Non riceve
risposte, requisiti del motore, esiti dell'audit o risultati precedenti.
Scompone la domanda in `request_parts`, quindi identifica requisiti atomici.

Ogni valore significativo conserva uno stato di provenienza:

- `explicit`: dichiarato nel testo;
- `derived`: dedotto da una regola umana dichiarata e accompagnato da
  `rule_id`;
- `assumed`: ipotesi non confermata, mai trattata come obbligo;
- `unknown`: informazione assente.

Le dimensioni ammesse sono attore, compito, fase, trigger, spazio, finalità,
polarità e ambito di squadra. Domande aperte conservano
`open_to_multiple_solutions`; non ricevono una soluzione tattica universale.
Vincoli non determinabili e ambiguità sono espliciti, non conteggiati come
requisiti positivi per convenienza.

### 4.2 Revisione e adjudication

1. Annotazione iniziale indipendente A.
2. Revisione indipendente B, senza output del motore e senza vedere le
   decisioni di A prima di produrre la propria lettura.
3. Confronto strutturato e registrazione di ogni disaccordo.
4. Adjudication da parte di C con motivazione per elemento.
5. Approvazione finale degli ID e delle relazioni atomiche.
6. Congelamento del caso e del dataset.

Annotatore, revisore e adjudicator dichiarano competenza tattica ed eventuali
conflitti. Le qualifiche non vengono presentate come certificazione ufficiale
Coverciano in assenza di prove verificabili.

## 5. Annotazione Gold V

Gold V inizia soltanto dopo il freeze di Gold E. Ogni record riferisce la
versione e l'hash del manifest Gold E e gli ID dei requisiti congelati.

Il revisore riceve domanda, risposta, requisiti Gold E congelati ed eventuali
evidenze. Per ogni requisito assegna uno fra:

- `satisfied`;
- `not_demonstrated`;
- `contradicted`;
- `ambiguous`;
- `not_applicable`.

Annota separatamente associazione attore-compito, fase-trigger, spazio,
finalità, polarità e ambito propria/avversaria. Lo span della risposta e la
motivazione rendono la decisione auditabile.

Restano distinti quattro giudizi:

1. **completezza** della risposta;
2. **coerenza relazionale** (obiettivo principale di Gold V);
3. **correttezza tattica** secondo il revisore competente;
4. **supporto documentale** reale delle affermazioni.

Una relazione coerente non è automaticamente corretta tatticamente. Un ID
fonte valido non dimostra pertinenza o supporto semantico. Dove il controllo
non è affidabile si usa `not_verifiable`, non un passaggio positivo.

La revisione umana segue lo stesso ciclo A/B/C di Gold E. Una controversia su
Gold E sospende il caso Gold V: non autorizza la modifica locale del requisito.

## 6. Freeze e versionamento

Il manifest deriva da
`evaluation/annotations/relational_gold_freeze_manifest_template_v1.json`.
In stato `frozen` deve contenere:

- tipo e versione semantica del dataset;
- percorso e SHA-256 del dataset canonico;
- conteggio, ID e SHA-256 per caso;
- data UTC di congelamento;
- ID di annotatori, revisori e adjudicator;
- stato dell'adjudication;
- inventario delle fonti ed esclusioni;
- separazione esplicita fra regression e independent set;
- eventuale manifest genitore o sostituito.

Canonicalizzazione: JSON UTF-8, chiavi degli oggetti ordinate, separatori
compatti e nessuna newline terminale nel byte stream sottoposto a hash. Gli
array mantengono l'ordine dichiarato. Prima del freeze i casi sono ordinati per
`case_id`; liste che rappresentano insiemi sono ordinate lessicograficamente.

Il file congelato è immutabile. Correzioni successive producono una nuova
versione e un nuovo manifest, conservando hash e percorso della versione
precedente. Un manifest `draft` non costituisce freeze.

## 7. Metriche future

Le metriche non vengono calcolate in questa attività.

### 7.1 Gold E

Il confronto avviene fra atomi umani e atomi estratti, con matching per
`request_part` e dimensioni. Ogni abbinamento contestato è revisionato, non
risolto usando l'output del sistema.

- precisione, recall e F1 micro e macro;
- precisione/recall/F1 per categoria e dimensione;
- errori di atomizzazione: split, merge, omissione, duplicazione;
- errori attore-compito, fase, trigger e requisito aperto;
- copertura delle ambiguità e dei non determinabili, riportata separatamente.

I casi `ambiguous` e `non_determinable` non diventano veri positivi. Si
riportano due denominatori: casi determinabili e totale dei casi, con tasso di
astensione/ambiguità.

### 7.2 Gold V

Per i requisiti determinabili si costruisce la matrice TP/FP/TN/FN rispetto
alla decisione umana. Si riportano precisione, recall e F1 micro/macro, per
categoria e complessivi. Separatamente:

- tasso di ambiguità e astensione;
- errori di polarità;
- errori di ambito proprio/avversario;
- errori attore-compito, fase-trigger, spazio, finalità e attribuzione
  dell'obiettivo.

`not_applicable`, `ambiguous` e `not_verifiable` sono esclusi dal denominatore
binario principale ma sempre conteggiati e pubblicati. Nessun caso
indeterminabile riceve automaticamente un esito positivo.

### 7.3 Accordo umano

Prima dell'adjudication si pubblicano accordo percentuale e, quando il volume
lo consente, Cohen's kappa per etichette nominali. Disaccordi e tasso di
adjudication restano visibili; il solo consenso finale non misura
l'affidabilità iniziale.

## 8. Controlli statici e stati

`scripts/validate_relational_gold_preparation_v1.py` controlla esclusivamente
schemi, template vuoti e manifest draft. Non valida semanticamente annotazioni
e non trasforma i template in gold.

La preparazione può essere dichiarata `VALIDATO` offline soltanto dopo i
controlli statici e la revisione degli artefatti. Restano distinti:

- protocollo/schemi/template: preparazione metodologica;
- raccolta casi: `DA FARE`;
- annotazione e doppia revisione: `DA FARE`;
- adjudication e freeze: `DA FARE`;
- benchmark indipendente: `BLOCCATO` fino al freeze;
- audit relazionale: non `INTEGRATO` e non `CERTIFICATO`.

## 9. CancellI per la fase successiva

La fase di popolamento richiede una decisione separata su fonti, numerosità,
stratificazione, competenze dei revisori e gestione dei conflitti. Prima di
qualsiasi audit devono esistere manifest Gold E congelato e, per Gold V,
riferimento verificabile a quel manifest. Nessun feedback del gold modifica
automaticamente corpus, regole o pipeline.
