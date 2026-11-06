# RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-CLOSEOUT-01

## Baseline e riconciliazione

Closeout esclusivamente documentale sulla baseline GitHub
`93b88a30ab5d42e6b9dd243764436186ccd54734`. Branch e HEAD locale/remoto erano
conformi, working tree pulito e nessun closeout equivalente risultava già
registrato. TODO, experiment register, design, implementazione, remediation e
relative revisioni indipendenti sono stati riconciliati con codice e commit.

## Autorizzazione del titolare

Il titolare approva formalmente il closeout offline della remediation della
provenance Spatial V1 sulla base del verdetto indipendente:

**REMEDIATION APPROVATA — CLOSEOUT OFFLINE AUTORIZZABILE.**

L'autorizzazione è limitata alle proprietà offline già validate. Non autorizza
inferenze, nuovi Gate, promozione del judge, integrazione, certificazione, merge
o deploy.

## Perimetro

Il closeout comprende esclusivamente:

- identità dichiarata e provenance content-addressed;
- validazione rigorosa fail-closed;
- immutabilità interna del descriptor;
- binding Spatial dimostrato staticamente;
- protezione degli SHA storici;
- compatibilità offline S2/NLI V2;
- non-promozione dei risultati shadow.

Non valuta accuratezza semantica generale o comportamento runtime futuro.

## Catena di evidenze

1. **Implementazione iniziale** — commit
   `33b5c7ad5a69513e7d4df7cbc26e937fccf16bdc`; adapter Spatial dedicato,
   provenance e test differenziali.
2. **Revisione indipendente** — commit
   `40de7501315676b7bfd0109c68fff4954ea9d599`; verdetto
   **IMPLEMENTAZIONE APPROVATA CON RETTIFICHE**, tre criticità maggiori.
3. **Remediation M1-M3** — commit
   `f953496a5e31c70665fd2f6664df3e684ae42cac`; tipi originali,
   immutabilità JSON, call graph AST e SHA byte-level; test 14/14 PASS.
4. **Revisione conclusiva** — commit
   `93b88a30ab5d42e6b9dd243764436186ccd54734`; verdetto
   **REMEDIATION APPROVATA — CLOSEOUT OFFLINE AUTORIZZABILE**, nessuna
   criticità residua M1-M3 e nessuna necessità di ulteriore review equivalente.

Report di riferimento:

- `tactical-semantic-support-s2-bridge-provenance-implementation-01.md`;
- `tactical-semantic-support-s2-bridge-provenance-implementation-review-01.md`;
- `tactical-semantic-support-s2-bridge-provenance-remediation-01.md`;
- `tactical-semantic-support-s2-bridge-provenance-remediation-review-01.md`.

## Risoluzione M1-M3

- **M1:** descriptor e campi sono controllati nei tipi originali prima della
  canonicalizzazione; tuple, sottoclassi, tipi/shape/valori errati falliscono
  chiusi.
- **M2:** la provenance interna è memorizzata come JSON canonico immutabile e la
  property restituisce copie deserializzate indipendenti.
- **M3-A:** il test AST collega import, closure `call`,
  `spatial_nli.judge_pair()` e `spatial_bridge.build_bridge(call, ...)`.
- **M3-B:** tre artefatti congelati sono protetti da SHA-256 indipendenti sui
  byte reali tramite `hashlib`.

Le proprietà sono **VALIDATO** offline. Il callable resta correttamente non
autenticato crittograficamente dal bridge; il binding è dimostrato staticamente.

## Test già eseguiti

La remediation ha registrato **14/14 PASS**, 0 FAIL, sui soli test differenziali
del bridge e runner Spatial. La revisione conclusiva ha giudicato le asserzioni
pertinenti e sufficienti. Nel presente closeout non è stato rieseguito alcun
test: la decisione si fonda sulle evidenze precedenti.

## Integrità storica consolidata

Valori provenienti dalle verifiche già concluse, non ricalcolati nel closeout:

| Artefatto | SHA-256 |
|---|---|
| Bridge NLI V2 | `79a4cc87c0d59e087a69d295a199f7f646c4ecb42194cf45531fd96dba09f515` |
| Runner NLI V2 | `3c5818142b0a9ac1c689a1cb3c5523fae13883d95b10544963842b97134cbf91` |
| JSON Spatial storico | `a06ba357471681f2ac047af9cff8293d23e75f1c8c8e364f1b14fc4990f8c42d` |

Gli artefatti non sono stati rigenerati né modificati.

## Separazione dalla qualità semantica

Il closeout della provenance non corregge né promuove il judge Spatial. Il Gate
differenziale storico resta **2/3**:

- `q3_04`: Gold `contradicted`, Spatial `supported` — falso positivo ancora
  presente;
- `q5_06`: corrispondenza confermata;
- `q5_02`: corrispondenza confermata.

La rationale resta una nota tecnica di provenance e non una motivazione
semantica del modello. Accuratezza del judge, Gate semantico, pipeline e sistema
restano fuori dal closeout.

## Decisione finale

**CLOSEOUT OFFLINE DELLA PROVENANCE SPATIAL V1 APPROVATO.**

La decisione è documentale e fondata sulle evidenze pubblicate; non sono stati
eseguiti nuovi test o controlli runtime. Non serve un'altra revisione tecnica
equivalente della provenance già validata.

## Stati ufficiali

| Componente | Stato |
|---|---|
| Implementazione adattatore Spatial V1 | **IMPLEMENTATO** |
| Test differenziali offline | **ESEGUITO** |
| Proprietà offline della provenance | **VALIDATO** |
| Remediation M1-M3 | **VALIDATO** |
| Closeout offline formale | **VALIDATO** |
| Gate semantico Spatial V1 | **BLOCCATO** |
| Integrazione nella pipeline | **BLOCCATO** |
| Certificazione del sistema | **BLOCCATO** |

## Limiti e attività separate

Restano separate e bloccate la remediation semantica del falso positivo,
qualsiasi nuovo Gate, la promozione del judge, l'integrazione e la
certificazione. Il presente closeout non autorizza alcuna di tali attività.

Unico prossimo passo: attendere un nuovo incarico esplicito del titolare su
un'attività distinta; nessuna ulteriore review equivalente della provenance.
