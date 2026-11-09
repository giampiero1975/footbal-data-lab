# RD-TSC-V2-D3-S2-RAG-V5-DUAL-BLOCKER-CAUSAL-REVIEW-01

## Attività e perimetro

Revisione causale statica dei due blocchi osservati nel runtime-03 Extraction
Locator sul caso `q3_04`:

1. frammento assegnato al lato claim ma appartenente all'evidence;
2. label proposta `supported` rispetto al Gold `contradicted`.

- data: 2026-11-09;
- branch: `codex/tactical-state-contract-v1`;
- HEAD GitHub iniziale: `2f24765b5661b8fcb6aca1ec1e6fd56caaa11dd1`;
- baseline applicativa degli artefatti: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- runtime analizzato:
  `spatial-v2-extraction-locator-q3-04-runtime-03`.

Sono stati riconciliati TODO, Experiment Register, codice, specifiche e report
forensi precedenti. Gli artefatti originali VPS sono stati letti in sola
lettura e confrontati con i digest già verificati. Nessuna inferenza, test,
modifica applicativa o operazione sul panel è stata eseguita.

## Evidenze autorevoli

| Artefatto | SHA-256 |
|---|---|
| `input.json` | `6927b40d3a9973fa4697df47d652eab80fc1a5ff5c92b09571c27f9234a875e5` |
| `prompt.txt` | `1def1a03c3c399658a89e8b7c7d4cdfb8a0bfb1ce43acc41c187a08349bec87f` |
| `raw_response.json` | `f1a28ba8f5910ba665de25c036734a7c98cbd757c971b3e5270905688a1e9034` |
| `extraction.json` | `caeb9d256461ebc75e3aaf9b61f9cddbd6aa00a3e464405e9ab80fce6ee32c10` |
| `result.json` | `7b1cfcb923b9008d9781e1a5b1a9ef5b9c4ce320472d69f0f98a89c4192d43fe` |

Claim:

> La difesa bassa lascia molto spazio tra la linea difensiva e la porta.

Evidence:

> La ricerca della verticalizzazione e della profondità del gioco è, per
> contro, di difficile attuazione quando si affrontano squadre che difendono
> basse e che lasciano avanzare gli avversari togliendo però spazio tra la
> linea difensiva e la porta.

Gold congelato: `contradicted`.

## 1. Blocco di localizzazione

### Fatti verificati

Il prompt runtime impone esplicitamente:

- `claim_relation` può selezionare frammenti soltanto dall'AFFERMAZIONE;
- `evidence_relation` può selezionare frammenti soltanto dalla FONTE;
- nessun passaggio automatico a un lato diverso;
- nessuna normalizzazione, correzione o parafrasi.

Il JSON grezzo di Qwen viola direttamente tale istruzione. Nel campo
`claim_relation.reference.selected_fragments[0]` inserisce:

> squadre che difendono basse e che lasciano avanzare gli avversari togliendo
> però spazio tra la linea difensiva e la porta

La stringa ha zero occorrenze nel claim ed è invece un frammento letterale
dell'evidence. Il valore errato è già presente in `raw_response.json`; non è
introdotto dal parser, dal locator o dal wrapper.

`_localize_fragments()` in
`scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py` cerca ogni
frammento esclusivamente nel testo imposto dal contenitore. Zero occorrenze
producono `missing`, non una ricerca sul lato opposto. `materialize_extraction()`
restituisce quindi `not_evaluable` e
`E_EXTRACTION_LOCALIZATION_NOT_UNIQUE`. Il comportamento applicativo è coerente
con il contratto e il fail-closed è corretto.

### Causa accertata e limite causale

**Causa diretta accertata:** output del modello non conforme al vincolo
side-bound. Non emerge un difetto applicativo del locator.

**Difetto contrattuale concorrente:** l'handoff definisce il vincolo globale di
lato, ma non definisce nel prompt la semantica operativa dei singoli slot. Lo
schema usa lo stesso `ENTITY_EXTRACTION_SCHEMA` generico per `subject` e
`reference` e non contiene descrizioni side-specific o della nozione di
referente. Questo rende il campo `reference` sottospecificato per il modello,
pur senza rendere ambigua la regola claim/evidence.

Non è determinabile quale meccanismo interno abbia indotto Qwen a copiare la
frase dal lato opposto: non esiste rationale. Non è quindi dimostrato che la
sottospecificazione del campo sia l'unica causa cognitiva.

### Lavori già conclusi da non ripetere

- test di frammento mancante;
- test di frammento ripetuto;
- test di frammento presente soltanto sul lato opposto;
- divieto di first-match, fuzzy matching e correzione automatica;
- provenienza, digest, Unicode e locator side-bound;
- runtime-03 e verifica del fail-closed.

### Correzione minima proposta

Intervenire soltanto sull'handoff di estrazione, senza cambiare il locator:

1. aggiungere definizioni normative e concise di `subject`, `reference`,
   `semantic_axis`, `value`, `conditions`, `phase`, `quantifier` e `polarity`;
2. rendere distinti nello schema/prompt i contenitori claim ed evidence con
   descrizioni side-specific, mantenendo identica la struttura finale;
3. definire `reference` come referente spaziale/oggetto della relazione nel
   testo dello stesso lato, non come proposizione corrispondente del lato
   opposto;
4. preservare il locator invariato: zero o più occorrenze restano
   `not_evaluable`; nessun trasferimento automatico fra lati.

Questa modifica riduce la sottospecificazione ma non garantisce da sola che il
modello obbedisca. L'efficacia richiederà evidenza distinta.

## 2. Blocco di riconoscimento della contraddizione

### Gold e significato delle proposizioni

Claim ed evidence condividono soggetto tattico e referente spaziale. La
relazione è opposta:

- claim: la difesa bassa **lascia molto spazio** tra linea e porta;
- evidence: le squadre basse **tolgono spazio** tra linea e porta.

Il fatto che gli avversari possano avanzare non riguarda lo stesso spazio
dietro la linea: la fonte distingue l'avanzamento concesso davanti dalla
riduzione dello spazio tra linea difensiva e porta. Non è assenza di conferma o
informazione insufficiente; la label Gold `contradicted` resta coerente.

### Fatti verificati nell'output runtime-03

Qwen propone `supported` e costruisce una rappresentazione semanticamente
inadeguata:

- assegna a entrambi `semantic_axis=space_availability`;
- assegna a entrambi `value=between`, valore appartenente all'asse
  `relative_position`, non a `space_availability`;
- non rappresenta la coppia direzionale `abundant`/`scarce`;
- produce quantificatori claim `many` ed evidence `some`, ma dichiara
  `comparison.quantifier=same`;
- usa entity ID distinti `s1/s2` e `r1/r2`, ma dichiara subject e reference
  `same`;
- usa condition ID distinti `c1/c2`, ma dichiara conditions `same`;
- propone label `supported` sulla base di questi confronti incoerenti.

La schema validation di estrazione accetta attualmente `value` dall'unione di
tutti i valori di tutti gli assi. Non verifica nella fase extraction la coppia
asse/valore né la coerenza dei confronti. Il validatore finale Spatial V2
contiene invece già i controlli deterministici:

- `E_AXIS_VALUE_INCOMPATIBLE` per `space_availability/between`;
- `E_COMPARISON_INCONSISTENT` per confronti incompatibili con ID, condizioni e
  quantificatori.

Tali controlli non sono stati raggiunti perché il locator ha bloccato prima la
materializzazione del witness.

### Indipendenza dal blocco di localizzazione

Il falso positivo semantico è indipendente dal singolo frammento mal assegnato:

- `q3_04` aveva già prodotto `supported` nel primo runtime S2 e in Spatial V1,
  prima dell'Extraction Locator;
- il runtime-03 contiene più incoerenze semantiche oltre al frammento
  side-bound;
- correggere soltanto la provenienza del frammento non renderebbe valido il
  witness: asse/valore e comparison resterebbero incoerenti.

La causa diretta osservabile è quindi un errore di estrazione/giudizio
semantico del modello. La causa cognitiva interna — per esempio prevalenza
dell'overlap lessicale — resta un'ipotesi non dimostrabile.

### Difetto dell'handoff concorrente

`EXTRACTION_INSTRUCTION` richiede genericamente di conservare la semantica
Spatial V2, ma non trasmette il vocabolario asse→valori, le coppie incompatibili
o le regole di derivazione della label. Lo schema espone enum globali e consente
la combinazione non rappresentabile `space_availability/between`. Questo è un
difetto concreto dell'handoff e della validazione extraction, distinto
dall'errore cognitivo non osservabile del modello.

### Correzione minima proposta

1. Trasmettere nel prompt extraction le regole normative già esistenti, senza
   nuovi concetti: valori ammessi per ogni asse, confrontabilità di
   soggetto/referente/contesto, incompatibilità di valori sullo stesso asse e
   separazione fra referente spaziale e quantità disponibile.
2. Aggiungere alla validazione extraction un precontrollo deterministico di
   asse/valore e comparison, riusando la semantica del validatore Spatial V2
   anziché duplicarla o correggere la label.
3. Fallire chiuso con codici specifici prima della localizzazione quando
   l'extraction è semanticamente non rappresentabile; non derivare o sostituire
   automaticamente una label corretta.
4. Mantenere il validatore Spatial V2 come autorità finale sul witness
   materializzato e `promotion_authorized=false`.

Il precontrollo rende il difetto osservabile prima, ma non migliora da solo
l'accuratezza del modello. La correzione dell'handoff deve essere validata
separatamente sul comportamento generativo.

## Piano tecnico e verifiche differenziali

### Patch A — handoff e shape extraction

File interessati:

- `scripts/shadow_nli_spatial_relations_v2_inference.py`:
  `EXTRACTION_INSTRUCTION`, `build_extraction_prompt()`;
- `scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py`:
  schema/descrizioni claim-evidence ed `extraction_shape_errors()`;
- test Extraction Locator già esistenti, senza creare una pipeline nuova.

Delta minimo:

- definizioni side-bound e dei campi;
- vocabolario asse→valori e regole di comparison già versionati;
- precontrollo fail-closed delle combinazioni semanticamente impossibili.

Non cambiano: contratto witness Spatial V2, locator, matching letterale,
retrieval, modello, trasporto, retry/repair, panel o promozione.

### Verifiche da riutilizzare

Non vanno duplicate le verifiche già esistenti per missing, repeated,
opposite-side, Unicode, provenance alterata, status/value invalido,
comparison/label incoerenti, singola chiamata e percorso legacy disattivato.

### Nuove verifiche indispensabili

| Caso nuovo | Proprietà nuova | Esito richiesto |
|---|---|---|
| Handoff contiene definizione side-specific di `reference` | nuovo contenuto normativo trasmesso | payload mock contiene regole esatte, una chiamata, zero repair |
| Extraction `space_availability/between` | nuovo precontrollo asse/valore | fail-closed specifico prima del locator |
| Comparison `same` con quantificatori `many/some` | nuovo precontrollo comparison | fail-closed specifico, nessuna label corretta automaticamente |
| Replay offline dell'extraction runtime-03 | attribuzione causale senza modello | rileva sia lato mancante sia incoerenze semantiche, preservando artefatto |
| Controllo sintetico con termini simili ma referente diverso | protezione da falsa contraddizione | non promuove `contradicted` |
| Controllo sintetico stesso referente con valori versionati incompatibili | regola generale, non lessicale | witness coerente deriva `contradicted` |

Il replay è differenziale perché esercita il nuovo precontrollo, non ripete il
runtime. I due controlli sintetici sono necessari per evitare una correzione
costruita soltanto su `q3_04`.

### Evidenza futura di efficacia

Dopo implementazione offline, test mirati e revisione indipendente, un nuovo
runtime potrebbe essere richiesto separatamente. Il solo `q3_04` corretto non
proverebbe generalizzazione: servono almeno le guardie già disponibili
`q5_06` (`contradicted`), `q5_02`/`q5_08` (`insufficient`) e `q3_05`
(`supported`), più i nuovi controlli autorizzati su referente/fase differente.

## Ordine raccomandato

Le correzioni sono sviluppabili indipendentemente ma condividono lo stesso
handoff. Ordine consigliato:

1. precontrollo deterministico dell'extraction e diagnostica specifica;
2. chiarimento side-bound e semantico del prompt/schema;
3. test offline differenziali e regressioni direttamente interessate;
4. revisione indipendente;
5. soltanto dopo, richiesta separata per evidenza runtime.

Il precontrollo viene prima perché impedisce che un futuro frammento corretto
nasconda incoerenze semantiche già osservabili. Non costituisce però una
correzione dell'accuratezza.

## Matrice finale

| Problema | Causa | Evidenza | Correzione proposta | Criterio di validazione | Stato |
|---|---|---|---|---|---|
| Localizzazione | Qwen viola il vincolo side-bound; semantica di `reference` sottospecificata nell'handoff | raw response contiene frase evidence in `claim_relation.reference`; locator registra 0 occorrenze | definizioni side-specific e del referente; locator invariato e nessun auto-spostamento | output conforme localizza tutti i frammenti; wrong-side continua fail-closed; controlli sintetici non duplicativi | **BLOCCATO** |
| Contraddizioni | estrazione/giudizio semantico errato; handoff non espone integralmente asse→valori e derivazione | `supported`, `space_availability/between`, comparison `same` incoerenti; falso storico precedente al locator | regole normative nel prompt e precontrollo deterministicamente riusato dal validatore V2 | combinazioni impossibili respinte; valori incompatibili sullo stesso asse producono witness coerente `contradicted`; guardie supported/insufficient senza regressioni | **BLOCCATO** |

## Decisione e stato

**PROCEDERE** con una singola patch offline circoscritta all'handoff extraction
e al suo precontrollo deterministico, mantenendo i due esiti diagnostici
separati. La raccomandazione non autorizza implementazione o runtime.

- revisione causale: **ESEGUITO**;
- cause dirette e indipendenza dei blocchi: **VALIDATO** nel perimetro degli
  artefatti disponibili;
- causa cognitiva interna del modello: non determinabile;
- patch e test differenziali: **DA FARE** previa autorizzazione;
- runtime, Gate, integrazione, panel e certificazione: **BLOCCATO**.

Flusso: Attività = revisione causale; Script = nessuno eseguito; Commit =
esclusivamente documentale; Report = questo documento; Risultato = due cause e
delta minimo separati; Decisione = proporre patch offline; Stato = analisi
**VALIDATO**, implementazione e runtime **BLOCCATO**.
