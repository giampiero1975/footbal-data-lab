# RD-TSC-V2-D3-S2-Q3-04-SEMANTIC-DESIGN-01

## Baseline e riconciliazione

Progettazione esclusivamente documentale sulla baseline GitHub
`a0bd06183c26e2904c1a633d15bc79457bf4a623`. Branch e HEAD locale/remoto erano
conformi, working tree pulito e nessuna progettazione equivalente risultava già
completata. Sono stati riconciliati TODO, registro, forensi `q3_04`, Gate NLI
V2/Spatial V1, closeout della provenance, contratti e codice dei judge.

Nessun codice, contratto, fixture, Gold o artefatto è stato modificato; nessun
test, modello, Gate o runtime è stato eseguito.

## Evidenze pregresse consolidate

Caso congelato `q3_04`:

- claim: la difesa bassa lascia **molto spazio** tra linea difensiva e porta;
- fonte: la difesa bassa lascia avanzare davanti, ma **toglie spazio** tra linea
  difensiva e porta;
- Gold umano: `contradicted`;
- NLI V2: `supported`;
- Spatial V1: `supported`.

Le forensi hanno già dimostrato (**A**) identità di claim/evidence, ordine degli
argomenti, assenza di troncamento/fallback, routing Spatial, parsing e
propagazione della label. La provenance è stata corretta e chiusa offline. Il
falso positivo è localizzato nel giudizio semantico restituito (**B — fortemente
supportato**); la causa cognitiva interna del modello non è osservabile.

Non vengono riaperte ipotesi su overlap lessicale, verbo «lasciare» o mancata
osservanza dell'istruzione.

## Limite documentato di NLI V2 e Spatial V1

NLI V2 restituisce uno schema con la sola `label`. Spatial V1 aggiunge già
istruzioni esplicite per confrontare soggetto, proprietà/spazio, referente,
direzione, condizioni, fase/tempo, negazioni e quantificatori. Specifica inoltre
che `lasciare molto spazio` e `togliere spazio`, sullo stesso referente e
contesto, sono incompatibili.

Spatial V1 non rende però osservabile quel confronto: il suo schema Pydantic è
ancora soltanto `{"label": ...}` e `judge_pair()` restituisce una stringa. Il
modello può quindi produrre una label senza esporre:

- quali soggetto e referente abbia associato;
- quale proprietà/direzione abbia estratto;
- se abbia distinto spazio davanti e dietro la linea;
- come abbia trattato condizioni, fase e quantificatori;
- se la label sia coerente con la relazione da esso stesso riconosciuta.

Il parser dimostra validità sintattica della label, non il confronto semantico.
Ripetere esempi o istruzioni già presenti non aggiungerebbe una proprietà
verificabile e non costituisce una remediation tecnicamente distinta.

## Alternative valutate

### A — Rafforzare ancora il prompt Spatial V1

Scartata. Soggetto, referente, direzione, condizioni e perfino l'inversione
spaziale del caso sono già espliciti. Un altro esempio aumenterebbe esposizione
al caso noto senza rendere osservabile il processo e potrebbe indurre fitting
lessicale.

### B — Regola deterministica lessicale sul testo grezzo

Scartata come soluzione primaria. Coppie di parole o negazioni non distinguono
in modo affidabile referente, fase, soggetto e movimento davanti/dietro la
linea. Rischierebbero false contraddizioni e una regola costruita su `q3_04`.
Un controllo deterministico è ammesso soltanto sulla struttura tipizzata già
prodotta, non come classificatore semantico generale del testo.

### C — Seconda inferenza/repair

Scartata. Aumenta variabilità e costo, non fornisce indipendenza probatoria e
viola il principio di una sola valutazione senza repair.

### D — Contratto versionato con relation witness e validatore deterministico

Raccomandata. Un nuovo contratto opt-in, distinto da Spatial V1, produce in una
sola risposta sia una decomposizione relazionale ancorata sia la label proposta.
Un validatore deterministico verifica forma, ancore e coerenza interna; non
interpreta liberamente il testo e non corregge il modello mediante euristiche.

## Soluzione raccomandata

Progettare, in una futura attività separata, un contratto sperimentale
`nli_spatial_relations_v2` con un output minimo del tipo:

```json
{
  "contract_id": "nli_spatial_relations_v2",
  "label": "contradicted",
  "claim_relation": {
    "subject": {"status": "explicit", "exact_span": "difesa bassa"},
    "property_axis": "spatial_quantity",
    "reference": {"status": "explicit", "exact_span": "tra la linea difensiva e la porta"},
    "value_direction": "abundant",
    "conditions": [],
    "phase": "not_explicit",
    "quantifier": "none",
    "polarity": "affirmed"
  },
  "evidence_relation": {
    "subject": {"status": "explicit", "exact_span": "squadre che difendono basse"},
    "property_axis": "spatial_quantity",
    "reference": {"status": "explicit", "exact_span": "tra la linea difensiva e la porta"},
    "value_direction": "reduced",
    "conditions": [],
    "phase": "not_explicit",
    "quantifier": "none",
    "polarity": "affirmed"
  },
  "comparison": {
    "subject": "compatible",
    "property_axis": "same",
    "reference": "same",
    "conditions": "compatible",
    "phase": "compatible",
    "value_relation": "incompatible"
  }
}
```

L'esempio illustra il contratto, non è un output osservato né una regola
hard-coded. I valori e le cardinalità definitivi richiederebbero specifica
separata prima dell'implementazione.

### Regole minime

1. Una sola generazione; nessun retry, repair o fallback a V1/V2.
2. Shape esatta, campi tipizzati, enum versionati e proprietà aggiuntive vietate.
3. Ogni componente `explicit` deve avere un'ancora testuale esatta presente nel
   rispettivo claim/evidence; offset opzionali, se introdotti, devono risolvere
   esattamente la stessa stringa.
4. Valori `ambiguous`, `absent` o `unknown` sono rappresentati esplicitamente e
   non possono essere promossi a corrispondenze.
5. Il validatore ricalcola la label consentita dalla struttura:
   - `supported` soltanto con soggetto/referente/contesto comparabili e valore
     compatibile;
   - `contradicted` soltanto con soggetto, asse, referente e contesto comparabili
     e valori incompatibili sullo stesso asse;
   - `insufficient` quando la fonte non determina la relazione;
   - `not_evaluable` al boundary S2 per shape, ancore, enum o coerenza non
     verificabili.
6. Se la label proposta non coincide con quella derivabile dal witness, il
   risultato è fail-closed `not_evaluable`; nessuna sostituzione silenziosa.
7. La struttura resta shadow e `promotion_authorized=false`.

Il validatore prova coerenza del witness e delle ancore, non la correttezza
semantica dell'asse/valore scelto dal modello. Tale limite deve restare
esplicito: un modello può ancora assegnare una categoria errata, ma l'errore
diventa osservabile e falsificabile invece di essere nascosto nella sola label.

## Differenza tecnica rispetto a NLI V2 e Spatial V1

1. **Cambiamento reale:** da una label opaca a label più relation witness
   strutturato e ancorato, con derivazione/controllo deterministico della
   coerenza.
2. **Nuova osservabilità:** soggetto, asse, referente, valore/direzione,
   condizioni, fase, quantificatore e confronto diventano persistibili e
   revisionabili.
3. **Assenza nei contratti precedenti:** V2 e Spatial V1 espongono soltanto la
   label; Spatial V1 richiede mentalmente il confronto ma non lo rende parte
   dello schema.
4. **Errore intercettabile:** una label `supported` accompagnata da stesso
   referente/contesto e valori strutturati incompatibili viene rifiutata dal
   validatore.
5. **Falsi positivi possibili:** equivalenze errate di soggetto/referente,
   categorie di valore troppo grossolane, fasi diverse considerate compatibili
   o quantificatori persi. Per questo unknown/ambiguous falliscono chiusi.
6. **Falsificabilità:** futuri output possono mostrare se il modello estrae
   ancora male soggetto, referente o valore; casi indipendenti possono misurare
   false contraddizioni e regressioni `insufficient`/`supported`.
7. **Non equivalenza al Gate V1:** non viene ripetuto lo stesso prompt/schema;
   cambia il contratto osservabile e viene aggiunta una proprietà deterministica
   verificabile offline prima di qualsiasi Gate.

Questa è una differenza tecnica documentabile. Non dimostra ancora che V2
correggerà `q3_04` o generalizzerà.

## Protezione dalle false contraddizioni

Il validatore non può dichiarare `contradicted` quando uno dei seguenti è
`different`, `unknown` o `ambiguous`: soggetto, property axis, referente,
condizioni/tempo o fase applicabile. Movimento consentito davanti alla linea e
spazio dietro la linea devono avere referenti distinti; la condivisione della
parola “spazio” non basta. Quantificatori, negazioni e causalità restano campi
separati e non possono essere inferiti per default.

Un'incompatibilità è ammessa soltanto fra valori versionati dello stesso asse e
con comparabilità positiva delle altre dimensioni. Il set di assi/valori deve
essere piccolo, documentato e non costruito sul solo lessico `q3_04`; valori non
rappresentabili diventano `unknown`, non nuove regole implicite.

## Piano futuro di validazione — non eseguito

### Offline deterministico

- schema esatto, enum, ancore e offset;
- label/witness coerenti e incoerenti;
- stesso/differente soggetto, referente, fase e condizioni;
- valori compatible/incompatible/unknown sullo stesso asse;
- quantificatori, negazioni e causalità non persi;
- output malformati/eccezioni `not_evaluable`;
- una sola chiamata, zero retry/repair/fallback;
- V1/V2, S2, bridge, Gold, fixture e artefatti storici byte-invariati;
- non-promozione invariata.

### Controlli semantici futuri

Regressioni già disponibili, senza attribuire indipendenza inesistente:

- `q3_04`: deve diventare `contradicted`, ma non basta da solo;
- `q5_06`: controllo inverso correlato, `contradicted`;
- `q5_02`: guardia `insufficient`;
- `q3_05`: controllo `supported` su condizione offside;
- `q5_08`: guardia quantificatore `insufficient`;
- `low_block_wrong`: storico pertinente, da usare soltanto secondo le evidenze
  documentate e non come Gold nuovo.

Prima di un Gate servirebbe una decisione separata su controlli nuovi e
non-equivalenti: stessi termini con referente diverso, stessa relazione in fase
diversa, movimento davanti contro spazio dietro, condizione temporale diversa e
parafrasi compatibile. In questa attività non vengono selezionati, annotati o
aggiunti casi Gold.

### Successo e arresto

Un futuro Gate potrebbe essere richiesto soltanto dopo test offline completi e
review indipendente. Successo minimo: witness validi, coerenza deterministica,
nessuna regressione sui controlli disponibili, `q3_04` corretto e almeno
controlli indipendenti autorizzati su referenti/fasi differenti. Il solo 3/3
rispetto allo storico 2/3 non dimostra generalizzazione.

Arresto fail-closed per schema/ancore/enum incoerenti, componente obbligatoria
ambigua, regressione `supported`/`insufficient`, seconda chiamata, retry, repair
o modifica di artefatti congelati. Nessun risultato `not_evaluable` è PASS.

## Rischi e limiti probatori

- Il witness è prodotto dallo stesso modello: migliora osservabilità e coerenza,
  non costituisce una seconda attestazione indipendente.
- Un vocabolario troppo stretto aumenta `not_evaluable`; troppo largo aumenta
  falsa equivalenza.
- Exact spans provano l'ancoraggio testuale, non la correttezza della categoria
  semantica assegnata.
- `q3_04` e `q5_06` sono esposti/correlati e non provano generalizzazione.
- Senza nuovi controlli indipendenti l'efficacia generale resta non determinata.

## Matrice A/B/C

| Conclusione | Livello |
|---|---|
| input/routing/parsing/provenance storici corretti | A |
| Spatial V1 richiede già confronto relazionale nel prompt | A |
| Spatial V1 espone soltanto la label | A |
| falso positivo localizzato nel giudizio restituito | B |
| relation witness rende confronto osservabile e label internamente verificabile | A come proprietà progettuale |
| relation witness correggerà `q3_04` | C |
| nuova versione ridurrà falsi positivi in generale | C |
| causa cognitiva interna del falso positivo | non determinabile |

## Decisione e stati

**PROCEDERE CON SPECIFICA OFFLINE VERSIONATA**, non con implementazione o Gate.

La soluzione raccomandata è l'alternativa D: contratto opt-in
`nli_spatial_relations_v2`, relation witness ancorato e validatore deterministico
di coerenza. La progettazione è **ESEGUITO**; specifica e implementazione sono
**DA FARE** previa autorizzazione distinta. Efficacia semantica, nuovo Gate,
integrazione e certificazione restano **BLOCCATO**. Il closeout della provenance
Spatial V1 resta **VALIDATO**.

Unico prossimo passo: decisione del titolare sull'autorizzazione di una specifica
tecnica offline completa del contratto V2 e del validatore, senza implementazione
né inferenze.
