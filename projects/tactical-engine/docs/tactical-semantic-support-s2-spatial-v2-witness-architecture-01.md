# RD-TSC-V2-D3-S2-SPATIAL-V2-WITNESS-ARCHITECTURE-01

## Baseline e fonti

Revisione architetturale statica della separazione fra estrazione semantica e
localizzazione delle evidenze Spatial V2.

- baseline GitHub: `5cf92e3ec0a904b49ef42389789874bdfde2036c`;
- branch: `codex/tactical-state-contract-v1`;
- working tree iniziale: pulito;
- runtime storico: staging `69ec127`, 16/16 anchor invalidi;
- runtime post-remediation: staging `41d50fa`, 14/14 anchor invalidi;
- nessun test, modello, runtime, SSH o modifica agli artefatti storici.

Fonti principali: TODO, experiment register, i quattro report `q3_04` richiesti,
artefatti `case.json` e `result.json` dei due runtime, specifica Spatial V2,
judge, validatore, suite offline, S1/S2, bridge Spatial V1, dual output D3,
runner differenziale e documentazione della spalla Groq.

## Pipeline esistente

Spatial V2 è un prototipo shadow esplicito, non un componente della pipeline
pubblica. Il suo percorso effettivo è:

| Passaggio | File/funzione | Input → output | Stato e controllo |
|---|---|---|---|
| Retrieval | esterno a Spatial V2 | corpus → evidence | non eseguito dal judge; nei runtime `q3_04` claim/evidence provengono dal caso congelato |
| Preparazione | wrapper runtime esterno / fixture | caso → due stringhe originali | nessuna trasformazione nel judge |
| Prompt | `shadow_nli_spatial_relations_v2_inference.py::build_prompt()` | claim/evidence → prompt | validazione non-vuoto, concatenazione letterale |
| Generazione | `judge_pair()` / `_default_transport()` | prompt + `SPATIAL_V2_SCHEMA` → risposta Ollama | una chiamata, nessun retry/repair/fallback |
| Parsing | `judge_pair()` | `message.content` → JSON | `json.loads()`, errore fail-closed |
| Witness | output Qwen | JSON → witness V2 | oggi il modello produce semantica, span e offset insieme |
| Struttura/anchor | `validate_spatial_v2()` → `_relation_errors()` / `_anchor_errors()` | witness + testi originali → errori | source, shape, NFC, cardinalità e uguaglianza esatta della slice |
| Confronto | `_comparison_errors()` | relazioni → coerenza delle comparazioni | deterministico rispetto ai valori dichiarati |
| Label | `_derive_label()` | witness coerente → label derivata | non risolve coreference né verifica la verità semantica dei valori estratti |
| Promozione | `judge_pair()` | validazione → record shadow | `promotion_authorized=false` sempre |
| Integrazione | nessun call site applicativo Spatial V2 | — | solo test e runtime esterni; **BLOCCATO**, non INTEGRATO |

Il validatore è indipendente dal trasporto e non muta il witness. Tuttavia la
sua verifica “semantica” è limitata alla coerenza interna del vocabolario,
delle comparazioni e della label: il docstring dichiara esplicitamente che non
risolve coreference né prova la correttezza semantica.

## Inventario degli anchor storici

Classificazione: **A** frammento esatto e univoco nel testo atteso; **B** esatto
ma ripetuto nel testo atteso; **C** presente soltanto nel testo opposto;
**D** assente/alterato; **E** evidenza insufficiente. L'unicità è valutata nel
testo imposto dal lato del campo, non sull'unione dei due testi.

### Runtime `69ec127`

Tutti i 16 anchor sono **A**: gli `exact_span` sono univoci nel testo corretto,
ma ogni offset è errato. Inventario per campo:

| Lato | Campi | Classe |
|---|---|---|
| claim | subject, semantic_axis, reference, value, condition 1, condition 2, phase, polarity | A × 8 |
| evidence | subject, semantic_axis, reference, value, condition 1, condition 2, phase, polarity | A × 8 |

Non risultano B, C, D o E. Alcuni frammenti, come il referente “tra la linea
difensiva e la porta”, compaiono anche nell'altro testo, ma sono univoci nel
testo obbligatorio del rispettivo campo e quindi non sono ambigui per un
resolver side-bound.

### Runtime `41d50fa`

Tredici anchor sono **A** e uno è **C**:

| Campo | Frammento | Classe | Nota |
|---|---|---|---|
| claim subject | frase completa dell'evidence | C | `source=evidence`; assente dal claim |
| claim semantic_axis/reference/condition/phase/polarity | claim completo | A × 5 | localizzabile ma semanticamente troppo ampio per provare la specificità del campo |
| claim value | `molto` | A | offset errato |
| evidence subject/semantic_axis/reference/condition/phase/polarity | evidence completo | A × 6 | localizzabile ma semanticamente troppo ampio |
| evidence value | `spazio` | A | univoco nell'evidence, offset errato; compare anche nel claim ma il lato è noto |

Non risultano B, D o E. Tutti i 14 offset sono invalidi. La remediation ha
corretto entrambi i quantificatori (`implicit/none/null/[]`), ma non gli anchor.
La polarità resta `explicit/affirmed` su entrambi i lati, combinazione vietata
indipendentemente dalla localizzazione. Inoltre il witness assegna
`space_availability=abundant` all'evidence contenente “togliendo però spazio”:
la presenza letterale di “spazio” non prova la correttezza del valore semantico.

## Problemi residui distinti

1. **Localizzazione:** 30/30 offset storici sono errati; 29 frammenti sono
   comunque univocamente localizzabili nel lato atteso.
2. **Sorgente:** un anchor post-remediation usa il lato opposto.
3. **Specificità:** molti nuovi span sono intere frasi e non dimostrano che il
   frammento supporti precisamente subject/axis/reference/phase/polarity.
4. **Status/value:** la polarità `explicit/affirmed` resta invalida; questo
   errore non può essere risolto da un localizzatore.
5. **Semantica:** un locator può trovare “spazio”, ma non stabilisce che
   “togliendo spazio” significhi `abundant`; non deve mascherare tale errore.
6. **Confronto:** il secondo witness dichiara subject `different` e label
   `supported`; se la struttura fosse materializzata, il validatore dovrebbe
   comunque verificare confronto e label.

## Componenti disponibili e riutilizzabili

- `validate_spatial_v2()` e `_anchor_errors()` sono l'autorità finale già
  VALIDATA offline per shape, source, slice, NFC e fail-closed; non vanno
  indeboliti né duplicati.
- `v5_tactical_state_dual_output_v1.py` conserva per D3
  `evidence_anchors={evidence_ref, exact_text}` e verifica appartenenza testuale
  senza chiedere offset al modello. È un precedente architetturale utile, non
  un resolver Spatial V2 pronto all'uso.
- S1 e i validator Gold verificano span già materializzati e digest, ma non
  localizzano frammenti ambigui per la produzione.
- Gli helper `anchor()` basati su `text.index()` esistono soltanto nei test
  Spatial V2: non sono componenti applicativi e non gestiscono ambiguità.
- Il bridge S2 disponibile è `SpatialV1S2Bridge`; valida provenienza e adatta
  label Spatial V1. Non integra Spatial V2 e non calcola offset.
- L'adapter S2 è shadow-only, content-addressed e impone sempre
  `promotion_authorized=false`; può ispirare la provenienza del nuovo stadio,
  ma non va usato come autorità di localizzazione.

Non esiste quindi un resolver applicativo equivalente già implementato.

## Stato della “spalla”

La spalla tattica Groq esiste in `groq_tactical_copilot_v2.py`, usa per default
`openai/gpt-oss-120b` e svolge due passaggi: revisione tattica e verifica
documentale/composizione. È opt-in dietro configurazione API; lo stato corrente
documentato la mantiene disattivata e il copilot live non eredita lo stato
INTEGRATO del pannello. Non è collegata a Spatial V2, non implementa il
contratto witness, non autentica span e non calcola offset.

Il judge NLI S2 iniettato è anch'esso shadow e non autorizza promozione. Può
fornire un secondo parere semantico, ma non è certificato come gate e non è
indipendente se usa lo stesso modello Qwen. Nessuna delle due “spalle” è una
soluzione alla localizzazione; introdurla nel percorso aumenterebbe costo e
complessità senza risolvere deterministicamente gli offset.

## Confronto delle alternative

| Opzione | Affidabilità attesa | Rischi/costo | Contratto e fail-closed | Valutazione |
|---|---|---|---|---|
| A — witness completo da Qwen | due runtime mostrano 0/30 offset validi | prompt lungo, latenza ~4 min, errori source/status ancora presenti | contratto invariato e fail-closed già corretto | ulteriori sole modifiche al prompt non sono giustificate come priorità |
| B — estrazione + locator deterministico | alta per span letterali univoci; nessuna pretesa semantica | nuovo piccolo contratto e stadio; rischio di mascherare estrazioni troppo larghe | witness V2 e validatore finale invariati; zero match/match multipli bloccano | **raccomandata** |
| C — riuso componenti | pattern D3/S1 e validatore riutilizzabili | nessun resolver completo esistente | evita duplicare validazione | integra B, non è alternativa autonoma |
| D — revisore AI | potenziale controllo semantico aggiuntivo non calibrato | seconda chiamata, rete/costo/latency, errori propri | solo shadow; non deve materializzare offset | non prioritario per questo difetto |

Non sono attribuiti miglioramenti prestazionali: nessuna opzione è stata
misurata in questa revisione.

## Raccomandazione prioritaria

Progettare e, solo dopo autorizzazione, implementare **un contratto di
estrazione Spatial V2 distinto e opt-in**, seguito da un localizzatore puro e
dal validatore V2 esistente.

### Contratto progettuale minimo

Il modello non produce `start`, `end` o `source`. Il lato è determinato dalla
posizione strutturale (`claim_relation` oppure `evidence_relation`). Per ogni
slot conserva:

- gli stessi campi semantici V2 (`status`, entity/value/ID, literal dove
  previsto);
- `selected_fragments`: lista ordinata di stringhe non vuote, copiate
  letteralmente dal solo testo del lato;
- comparison e label proposte, con lo stesso vocabolario V2;
- identità/versione del contratto di estrazione.

Invarianti:

1. nessun offset o source generato dal modello;
2. nessuna normalizzazione, fuzzy matching, casefold o correzione;
3. il locator usa esclusivamente il testo originale e ricerca ogni frammento
   con confronto letterale;
4. esattamente una occorrenza produce `{source,start,end,exact_span}`;
5. zero o più occorrenze producono `not_evaluable`, non una scelta euristica;
6. il lato del contenitore è vincolante: nessun passaggio automatico al testo
   opposto;
7. ordine, duplicati e cardinalità restano verificabili;
8. ogni materializzazione registra path del campo, digest del testo,
   frammento, numero di occorrenze e offset prodotto;
9. il locator non modifica status, value, entity ID, comparison o label;
10. il witness materializzato passa integralmente al `validate_spatial_v2()`
    invariato; soltanto quel risultato può qualificare la struttura.

Questo non è post-processing degli offset di Qwen: gli offset non fanno parte
dell'output del modello. È una trasformazione esplicita e tracciata fra due
contratti distinti. Span troppo ampi possono essere localizzati, ma non diventano
per questo semanticamente specifici; status/value, confronto, label e audit
semantico restano controlli separati.

## Rischi e invarianti

- Un frammento letterale univoco può essere semanticamente irrilevante o troppo
  ampio: la localizzazione non equivale a supporto.
- Frammenti brevi possono essere duplicati; il sistema deve bloccare anziché
  scegliere la prima occorrenza.
- Il nuovo contratto aumenta le superfici di shape/provenienza; serve versione
  esplicita e nessuna conversione implicita da witness storici.
- Il modello può continuare a sbagliare status/value o confronto; il locator
  deve conservarli e il validatore deve respingerli.
- Spatial V2 resta shadow, senza promozione, finché efficacia semantica e
  integrazione non sono validate separatamente.

Restano obbligatori: nessuna evidenza inventata, nessun repair silenzioso,
provenienza content-addressed, validatore indipendente invariato, artefatti
storici immutabili e fail-closed a ogni incertezza.

## Piano minimo di verifica offline

Solo casi differenziali nuovi, tutti senza modello reale:

1. frammento univoco claim/evidence → offset esatti e witness accettato dal
   validatore esistente;
2. frammento assente → `not_evaluable`, nessun witness promosso;
3. frammento ripetuto → `not_evaluable`, nessuna prima-occurrence implicita;
4. frammento presente soltanto nel lato opposto → `not_evaluable`;
5. frammento univoco ma status/value invalido → materializzazione tracciata e
   rifiuto invariato del validatore;
6. frammento univoco ma comparison/label incoerenti → rifiuto invariato;
7. span Unicode/punteggiatura → identità code-point e slice esatta;
8. adapter disattivato → percorso Spatial V2 corrente invariato;
9. provenienza/digest alterati → fail-closed;
10. verifica statica che locator e parser non chiamino modelli, retry o repair.

Questi casi non ripetono i test esistenti: verificano la nuova frontiera fra
contratto di estrazione e witness finale, non le regole interne già validate.

## Decisione e stati

La risposta alla domanda architetturale è **sì, con condizioni strette**:
Qwen può selezionare frammenti e proporre la semantica; un componente
deterministico può localizzare soltanto frammenti letterali univoci. Tale
separazione risolve il difetto meccanico degli offset senza dichiarare corretta
la semantica e senza indebolire il validatore.

Flusso: Attività = revisione architetturale; Script = nessuno eseguito; Commit =
documentale; Report = questo documento; Risultato = architettura e alternativa
minima determinate; Decisione = sottoporre il contratto di estrazione/locator a
successiva autorizzazione implementativa.

| Componente | Stato |
|---|---|
| Revisione architetturale | **ESEGUITO** |
| Evidenza del difetto di localizzazione e assenza di resolver equivalente | **VALIDATO** |
| Raccomandazione contratto di estrazione + locator | **VALIDATO** progettualmente |
| Implementazione e test differenziali | **DA FARE** previa autorizzazione |
| Spatial V2 pubblico, Gate, integrazione e certificazione | **BLOCCATO** |

Nessuna implementazione o nuova inferenza è autorizzata da questa decisione.
