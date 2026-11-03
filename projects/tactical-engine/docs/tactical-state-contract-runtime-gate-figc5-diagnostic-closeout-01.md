# Tactical State Contract runtime Gate FIGC5 — diagnostic closeout 01

Data: 2026-11-03
Esperimento: `RD-TSC-RUNTIME-GATE-FIGC5-CANDIDATE-01`
Baseline: `3fa3a189b213884df6f08544c827fd306c5fd007`

## Perimetro ed evidenze

Questa chiusura usa esclusivamente il codice della baseline, la documentazione
Git e i quattro artefatti gia prodotti dall'unica esecuzione autorizzata. Non
sono state eseguite nuove inferenze, query, prove, repair o letture runtime.

Gli artefatti erano stati verificati byte per byte prima di questa chiusura:

| Artefatto | Byte | SHA-256 |
|---|---:|---|
| `tactical_state_contract_runtime_gate_figc5_01.json` | 44185 | `a9c24186b9639d6e46c4b21795a74e5934269a8b6f0080b3c8be8a6c3bcc02b9` |
| `tactical_state_contract_runtime_gate_figc5_01.stdout.log` | 511 | `983faa69d3eb431d3bb02cdb6ec7cbb813ca7c30e19b77ba101bcd013b77aa22` |
| `tactical_state_contract_runtime_gate_figc5_01.time_stderr.log` | 1891 | `9aa6dcae25c0d2a54392301f2a8a45c9f36b64f715e90aee07b7194a066f6d10` |
| `tactical_state_contract_runtime_gate_figc5_01.exit_code.txt` | 12 | `85acfd2e79dd47df07d214334642196301332f72d792b52068cdfd8898755409` |

Il JSON registra `overall_status=blocked`, risposta non promossa, una sola
generazione e zero repair. La collection era pari a 6410 prima e dopo la
generazione e `index_unchanged=true`. Il file di exit registra codice `1`.

## Matrice contratto, piano ed esito

| Requisito/controllo | Contenuto osservato | Obbligo nella baseline | Esito e prova |
|---|---|---|---|
| Involucro generativo | `applied_plan` ed `explanation` presenti | Obbligatorio | PASS; `generation_transport_schema()`, righe 37-71 |
| Campi del dominio | schema, versione, domanda, formazioni, slot, fase e altri contenitori presenti | I contenitori sono obbligatori; il trasporto non impone che le liste operative siano non vuote | PASS strutturale; righe 39-67 e `validate_contract()`, da riga 634 |
| Formazione/slot | 4-3-3 e undici slot astratti | La formazione esplicita deve essere compatibile con la domanda | PASS `question_compatibility`; righe 177-192 |
| Attori e ruoli concreti | `actors=[]`, `role_refs=[]`, `candidate_actors=[]` | Non obbligatori se la domanda non nomina attori espliciti; non esiste cardinalita minima generale | Formalmente ammesso, tatticamente insufficiente per attribuire responsabilita |
| Eventi e vincoli | `events=[]`, `constraints=[]` | I campi sono richiesti, non contenuti non vuoti | Formalmente ammesso; nessuna relazione operativa verificabile |
| Assegnazioni e mapping | nessuna assignment e `structural_mappings=[]` | Non richiesti in modo incondizionato dalla baseline | Formalmente ammesso; piano privo di compiti, trigger, spazi e finalita collegati |
| Stato di fase | un solo stato iniziale, fase `unknown` | Una fase nota non e requisito bloccante generale | Formalmente valido, ma non dimostra transizione offensiva/difensiva |
| Coerenza domanda-piano | controllati `explicit_formations` e `explicit_actors`; nessun attore esplicito mancante | Il controllo riguarda soltanto fatti espliciti estratti dalla domanda | PASS previsto; `compare_question_and_applied_plan()`, righe 169-207 |
| Coerenza piano-prosa | `required_scope=[]`, `checked_scope=[]`, `unassessed_scope=[]`, `coverage_sufficient=false` | Lo scope nasce solo da final formation, eventi, mapping o assignment presenti | `not_assessable`; comportamento previsto dalle righe 210-267, ma rivela una lacuna di copertura rispetto alla ricchezza tattica desiderata |
| Audit tattico-documentale | `complete=false`; mancanti densita/prossimita, palla coperta/scoperta e ragione operativa | Tutti i requisiti dell'audit devono essere coperti per `complete=true` | FAIL; controllo `tactical_documentary_audit` nel JSON |

Il piano e quindi **formalmente valido ma tatticamente insufficiente** per la
domanda. Attori, ruoli, assignments, constraints e relazioni operative non
erano obbligatori in modo incondizionato dal contratto della baseline; non
vengono resi retroattivamente obbligatori da questo report. La lacuna e che i
controlli domanda-piano e piano-prosa possono non ottenere uno scope tattico
utile quando il piano omette proprio le relazioni che dovrebbero essere
valutate.

`question_compatibility` ha restituito PASS perche verifica campi minimi e fatti
espliciti: formazione, numero effettivo di giocatori se esplicito, attori ed
eventi espliciti. Non valuta la completezza tattica generica della risposta.
`plan_prose_alignment` ha restituito `not_assessable` perche nessuno dei suoi
generatori di scope era presente: `final_formation`, sostituzioni/espulsioni/
rotazioni, mapping strutturali o assignments di fase. Le righe 256-262
richiedono inoltre `bool(required)` per una copertura sufficiente.

## Matrice claim, fonte e supporto

La colonna "claim" identifica il passaggio semantico conservato
nell'`explanation`; non introduce una citazione letterale non disponibile nel
checkout Git. F2, F3 e F8 sono gli identificativi delle evidenze conservate nel
JSON del Gate.

| Claim dell'explanation | Evidenza pertinente | Classificazione | Motivazione |
|---|---|---|---|
| Il 4-3-3 produce triangoli, ampiezza offensiva e spazi ai lati della punta | F8 | Supportata direttamente | F8 documenta triangoli del 4-3-3, ampiezza in attacco e spazi accanto alla punta |
| I tre centrocampisti e le ali sono gli specifici autori di tale struttura | F8 | Inferenza tattica ragionevole, non esplicitamente documentata | La struttura e documentata, l'attribuzione operativa completa non lo e |
| L'ala debole copre e si ristabilisce un 3+1 | F2 | Supportata direttamente | F2 documenta copertura dell'ala sul lato debole e ricomposizione 3+1 |
| La stessa disposizione costituisce gia la struttura preventiva nel momento della perdita | F2 | Inferenza tattica ragionevole, non esplicitamente documentata | Il frammento descrive la copertura ma non la lega in modo inequivoco al preciso istante della perdita |
| I tre centrocampisti distribuiscono la copertura; almeno un'ala collabora; squadra compatta ed equilibrata ritarda l'avversario | F3 | Supportata direttamente | Tutti questi elementi sono espressi nel frammento pertinente |
| Pressing immediato in transizione | F3 | Non supportata dalle evidenze disponibili | F3 condiziona il pressing a prerequisiti tattici; non documenta un contropressing sempre immediato |
| Punta e ala opposta sono appoggi immediati per la ripartenza propria | F2 | Non determinabile | F2 parla di "ripartenza" ma il frammento isolato non rende univoco quale squadra riparta; non e lecito trasformarlo in contraddizione certa |
| Punta e ala opposta sostengono pressing o copertura laterale | F2/F3 | Non supportata dalle evidenze disponibili | Le fonti disponibili non attribuiscono loro entrambe queste responsabilita operative |
| Densita e prossimita come criterio operativo | Nessuna fra le otto evidenze | Non supportata dalle evidenze disponibili | L'audit registra `density_or_proximity` mancante |
| Palla coperta/scoperta come trigger operativo | Nessuna fra le otto evidenze | Non supportata dalle evidenze disponibili | L'audit registra `covered_or_uncovered_ball` mancante |
| Responsabilita complete attore-compito-spazio-trigger-finalita | F2/F3/F8 solo parziali | Non supportata come relazione completa | L'audit registra relazione non dimostrata, requisito sottospecificato e pertinenza di attore/obiettivo non dimostrata |

Nessun claim esaminato puo essere classificato con certezza come "in
contraddizione con la fonte". Il caso degli appoggi alla ripartenza resta
ambiguo e quindi non determinabile, non un errore certo del modello.

## Copertura documentale

Nelle otto evidenze recuperate sono presenti e solo parzialmente sfruttati i
contenuti utili di F2, F3 e F8: ampiezza/triangoli, copertura sul lato debole,
3+1, collaborazione di almeno un'ala, compattezza, equilibrio, ritardo e
pressing condizionato. Le evidenze F1, F5 e F7 risultano meno pertinenti perche
riguardano formazioni o prospettive differenti.

Nelle otto evidenze non risultano documentati: contropressing immediato,
densita/prossimita, palla coperta/scoperta, protezione completa di centro e
profondita, criteri completi pressare-versus-ripiegare e una relazione completa
attore-compito-spazio-trigger-finalita. Questo e un giudizio sul solo set F1-F8:
la presenza o assenza nell'intero corpus **non e determinabile** senza un nuovo
retrieval, che non e autorizzato.

## Diagnosi causale

### Causa tecnica diretta

`plan_prose_alignment.status=not_assessable` e
`tactical_documentary_audit.complete=false` sono composti da
`generation_diagnostic()` in `overall_status=blocked` (righe 270-352). Il
wrapper rifiuta quindi il report come query completata e restituisce exit `1`.
La prosa non viene promossa (`promoted_answer=""`). Questo comportamento
fail-closed e osservato e **VALIDATO** per il singolo caso.

### Difetti sostanziali concorrenti

1. **Insufficienza del modello:** il piano applicato contiene formazione e slot
   ma non relazioni operative; la spiegazione e piu ricca del piano e include
   ampliamenti non dimostrati dalle fonti disponibili.
2. **Insufficienza documentale del set recuperato:** F1-F8 non coprono tutti i
   dettagli richiesti dall'audit; non e dimostrata un'insufficienza dell'intero
   corpus.
3. **Limite del validatore:** la validita strutturale ammette contenitori
   operativi vuoti; la compatibilita con la domanda non misura completezza
   tattica generica; l'allineamento piano-prosa deriva lo scope dal piano e
   diventa non valutabile quando il piano e tatticamente vuoto. L'audit e
   euristico e non equivale a una verifica semantica generale claim-per-fonte.

## Punti non determinabili

- presenza dei dettagli mancanti nell'intero corpus;
- interpretazione univoca del soggetto della "ripartenza" in F2 senza contesto
  ulteriore;
- equivalenza semantica generale fra explanation e fonti oltre i controlli
  deterministici disponibili;
- comportamento del modello in altri casi o dopo eventuali modifiche, non
  essendo autorizzati rerun o repair.

## Tracciamento e decisione

**Attivita**: chiusura diagnostica offline del Gate FIGC5.
**Script**: nessuno eseguito; solo lettura di codice, documentazione ed evidenze
gia acquisite.
**Commit**: commit documentale di questa sessione.
**Report**: questo documento.
**Risultato**: causa diretta e cause concorrenti separate con limiti di
valutabilita espliciti.
**Decisione**: nessuna correzione implementativa proposta; attendere una nuova
decisione del titolare.
**Stato**: chiusura diagnostica offline **ESEGUITO**; fail-closed del singolo
caso **VALIDATO**; Gate runtime FIGC5 **BLOCCATO**; integrazione runtime TSC
**BLOCCATO**; certificazione runtime non conseguita.

## Verdetto

Il Gate non e stato superato correttamente. Il blocco non deriva da un errore
di trasporto o da troncamento: deriva dalla combinazione verificata di piano
formalmente valido ma tatticamente vuoto, controllo piano-prosa non valutabile
e audit documentale incompleto. Le evidenze recuperate sostengono parte della
spiegazione, ma non tutte le relazioni operative dichiarate. Il fail-closed e
corretto per questo caso; il Gate complessivo resta **BLOCCATO** e non dimostra
integrazione o certificazione runtime.
