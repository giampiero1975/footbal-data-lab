# RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-REMEDIATION-REVIEW-01

## Baseline e perimetro

Revisione indipendente conclusiva, esclusivamente statica, della remediation
M1-M3 sulla baseline GitHub
`f953496a5e31c70665fd2f6664df3e684ae42cac`. Branch, HEAD locale/remoto e
working tree erano conformi; nessuna revisione equivalente risultava già
conclusa.

Diff revisionato:
`40de7501315676b7bfd0109c68fff4954ea9d599..f953496a5e31c70665fd2f6664df3e684ae42cac`.
Sono stati esaminati integralmente bridge Spatial, due test modificati,
dipendenze e documentazione. Nessun test, import applicativo, inferenza o
runtime è stato eseguito.

## M1 — tipi originali

`_validate_contract_descriptor()` esegue nell'ordine:

1. `type(value) is dict` e confronto dell'insieme esatto delle sei chiavi;
2. `type(...) is str` per i cinque campi scalari;
3. `type(labels) is list` e `type(label) is str` per ogni elemento;
4. confronto dell'intero valore con identità, versione, base contract, ordine
   delle label, instruction digest e selection congelati;
5. costruzione di una nuova struttura senza alias alla lista originale.

La canonicalizzazione avviene soltanto dopo questa validazione, nel
`build_bridge()`. Tuple, sottoclassi di dict, elementi non stringa, booleani,
campi mancanti/inattesi e oggetti non serializzabili non possono essere
normalizzati in valori validi. Tutte le violazioni percorrono
`BridgeContractError` prima della valutazione. **A — dimostrato.**

## M2 — immutabilità

Dopo la validazione, il descriptor completo viene serializzato una volta con
JSON canonico e lo stato interno conserva soltanto `_descriptor_json: str`.
La property `judge_descriptor` esegue `json.loads()` e restituisce ogni volta
una struttura nuova. Input, copia esposta e stato interno non condividono
dict/list.

La dataclass frozen impedisce la riassegnazione ordinaria; la stringa impedisce
mutazioni annidate. Il test muta input e copia pubblica, tenta la mutazione
indicizzata della stringa, verifica che `vars(adapter)` non contenga dict/list e
confronta descriptor e identità/digest. La struttura pubblica del descriptor e
la sua serializzazione canonica restano equivalenti alla versione precedente.
**A — dimostrato nel normale contratto applicativo Python.**

Non sono richieste garanzie contro `object.__setattr__` o manipolazioni
deliberate fuori contratto.

## M3-A — binding Spatial

Il test AST non si limita ai nomi. Identifica il `main()`, trova la closure
`call`, verifica il nodo `Return(Call(...))`, il target attributo
`spatial_nli.judge_pair`, quindi trova l'assegnazione `bridge` e verifica
`spatial_bridge.build_bridge` con la stessa variabile `call` come primo
argomento. Controlla inoltre import Spatial e assenza degli import V2 nel
runner.

Il call graph coincide col codice del runner, che non è stato modificato dalla
remediation. Il bridge dichiara correttamente che non autentica il callable.
**A — dimostrato staticamente.**

## M3-B — artefatti congelati

Il test usa costanti indipendenti, path corretti, `Path.read_bytes()` e
`hashlib.sha256`, senza funzioni digest applicative e senza rigenerare file:

| Artefatto | SHA-256 osservato/atteso | Esito |
|---|---|---|
| bridge NLI V2 | `79a4cc87c0d59e087a69d295a199f7f646c4ecb42194cf45531fd96dba09f515` | conforme |
| runner NLI V2 | `3c5818142b0a9ac1c689a1cb3c5523fae13883d95b10544963842b97134cbf91` | conforme |
| JSON Spatial storico | `a06ba357471681f2ac047af9cff8293d23e75f1c8c8e364f1b14fc4990f8c42d` | conforme |

I medesimi valori sono stati verificati staticamente sui file correnti durante
la review. **A — dimostrato.**

## Qualità dei test

Gli 8 test del bridge e i 6 test del runner coprono il delta senza chiamate
runtime:

- casi negativi M1 pertinenti e non tautologici;
- mutazioni successive M2 su input, copia e rappresentazione interna;
- call graph AST M3 collegato alla closure effettiva;
- hash byte-level indipendenti;
- regressioni di proiezione, evidence, tre label, rationale, errori,
  `not_evaluable`, non-promozione e digest.

I digest sintetici sono ricalcolati con `hashlib` e JSON canonico esplicito, non
soltanto richiamando la funzione sotto test. Il report precedente registra
**14/14 PASS**; tale esecuzione è **B — fortemente supportata** dalle evidenze
pubblicate e non è stata ripetuta per espresso divieto. La pertinenza e
sufficienza delle asserzioni è **A — dimostrato** dalla lettura statica.

## Compatibilità e invarianti

Il diff tecnico modifica soltanto il bridge Spatial e i due test. Restano fuori
dal diff runner Spatial, bridge/runner V2, S2, contratto Spatial, fixture, Gold,
JSON storico e ogni percorso runtime. Label, rationale tecnica, proiezione,
claim/evidence, routing, plan fingerprint e `promotion_authorized=false` sono
invariati.

La rappresentazione interna stringa non cambia il descriptor pubblico:
`json.loads()` ricostruisce gli stessi tipi/valori e S2 continua a calcolare il
digest sul JSON canonico della stessa `config`. **A — dimostrato.**

## Matrice A/B/C

| Conclusione | Livello |
|---|---|
| M1 impedisce normalizzazione di tipi originali errati | A |
| M2 elimina alias mutabili ordinari del descriptor | A |
| M3-A collega import, closure, judge e bridge Spatial | A |
| M3-B protegge i tre SHA sui byte reali | A |
| descriptor pubblico e digest semanticamente invariati | A |
| runner/contratti/artefatti storici invariati | A |
| risultato storico 14/14 PASS | B, evidenza registrata non rieseguita |
| autenticità crittografica del callable | fuori contratto, non dichiarata |
| qualità semantica del judge | C/fuori perimetro |

## Criticità e verdetto

Non sono emerse criticità BLOCCANTI, MAGGIORI o MINORI nel perimetro M1-M3.
Non è necessaria alcuna ulteriore correzione tecnica per la provenance offline.

**REMEDIATION APPROVATA — CLOSEOUT OFFLINE AUTORIZZABILE.**

M1, M2 e M3 sono risolte e le evidenze sono sufficienti. Non serve una nuova
revisione tecnica equivalente. La decisione formale di registrare il closeout
resta al titolare e non autorizza Gate, inferenze, integrazione o certificazione.

Stati:

- revisione indipendente: **ESEGUITO**;
- remediation M1-M3: **IMPLEMENTATO**;
- proprietà offline della remediation: **VALIDATO**;
- closeout offline formale: **DA FARE** fino alla decisione del titolare;
- Gate semantico, integrazione e certificazione: **BLOCCATO**.

Unico prossimo passo: presa d'atto/decisione formale del titolare sul closeout
offline; nessuna nuova revisione tecnica equivalente.
