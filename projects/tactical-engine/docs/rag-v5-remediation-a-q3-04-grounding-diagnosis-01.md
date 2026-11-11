# q3_04 — diagnosi documentale mirata del grounding

Data: 2026-11-11. Attività:
`RD-RAG-V5-REMEDIATION-A-Q3-04-GROUNDING-DIAGNOSIS-01`.

## Diagnosi e decisione

**Causa prossima verificabile dell'arresto:** il raw assegna a sette campi
evidence frammenti presenti soltanto nel claim. Il lato di ricerca deriva dal
contenitore; il locator cerca correttamente nell'evidence, ottiene zero
occorrenze e arresta la materializzazione. Non sono sette stringhe diverse:
sono sette campi con cinque stringhe distinte.

`claim_relation` ed `evidence_relation` sono identiche come oggetti JSON,
inclusi stati, ID, valori e frammenti, già nel content della risposta HTTP.
È una **duplicazione completa della rappresentazione del claim sul lato
evidence nell'output osservato**. Non dimostra un'operazione mentale o una
specifica direzione temporale di copia: entrambe le relation potrebbero
essere state generate sulla stessa lettura errata. L'origine testuale dei
frammenti è dimostrabile; la causa interna della generazione non lo è.

**Decisione unica: evidenze insufficienti per selezionare una correzione minima
giustificata. Nessuna patch proposta.** Il contratto e le istruzioni vietano
già l'errore osservato e il locator lo respinge. Non è documentato un difetto
deterministico da correggere né un nesso causale che giustifichi cambiare
prompt/schema. Ripetere l'istruzione, forzare valori/label, rendere diverse
le due relation per obbligo o ricollocare frammenti non è una correzione
dimostrata di questo problema. Una coincidenza lecita dei testi sui due lati
deve continuare a essere rappresentabile.

Analisi **ESEGUITO**, diagnosi **VALIDATO** nel perimetro documentale sotto
indicato. Correzione e miglioramento generativo non validati; accuratezza,
compatibilità backend completa, ABI, Gate, integrazione e certificazione
**BLOCCATO**.

## Riconciliazione, metodo e fonti

Baseline iniziale locale e GitHub
`4c4682f8c40f5850d1f5f571846bf19e20a81b53`, branch
`codex/tactical-state-contract-v1`, origin atteso, working tree pulito.
TODO e Experiment Register ufficiali letti da GitHub e confrontati coi blob;
raw letto anche via GitHub al commit congelato. Consultati il report del
tentativo e gli artefatti richiesti. Nessuna diagnosi mirata equivalente
risultava già pubblicata: il report della prova contava i sette missing,
senza matrice completa per campo e distinzione delle responsabilità.

Analisi limitata a raw, input originale, schema/payload pubblicati e lettura
statica del caller/locator; i report precedenti sono solo riferimenti storici.
Non è stata rieseguita la materializzazione, il judge o una suite. Non sono
stati usati nuovi output del modello, artifact alterati o test controfattuali.
Metodo Python inline JSON/stringhe/hash: decodifica del content, confronto
oggetti, ricerca letterale dei frammenti nei due testi, raggruppamento per
identità testuale, confronto dei blocchi FONTE/AFFERMAZIONE col rispettivo input.
Queste sono le operazioni documentali nuove richieste dal mandato, non replay
dei test del locator.

Evidenza nuova:
[`remediation-a-q3-04-grounding-diagnosis-facts-01.json`](remediation-a-q3-04-grounding-diagnosis-facts-01.json).
Include matrice completa, collegamenti a tutti gli altri campi con la stessa
stringa, posizioni, istruzione effettiva, descrizioni schema e hash dei sei
input/sorgenti letti. Sorgente generativa originale:
[`raw_response.json`](../evaluation/remediation_a_official_api_single_case_01/raw_response.json),
SHA-256 `dab16c58e6df124355630743b898926ce49d83e5336796ca3081f88155b24147`.
Payload originale:
[`request_payload.json`](../evaluation/remediation_a_official_api_single_case_01/request_payload.json),
SHA-256 `0852b5ad08557195c76a784b632d5b30e44657802b40b712b4de507629d8d16d`.

## Input e percorso fino alla localizzazione

Claim originale:

> La difesa bassa lascia molto spazio tra la linea difensiva e la porta.

Evidence originale:

> La ricerca della verticalizzazione e della profondità del gioco è, per contro, di difficile attuazione quando si affrontano squadre che difendono basse e che lasciano avanzare gli avversari togliendo però spazio tra la linea difensiva e la porta.

Il blocco FONTE del messaggio user coincide esattamente con evidence;
AFFERMAZIONE coincide con claim: nessuno scambio o sostituzione dei testi
nel payload pubblicato. Il caller `build_extraction_prompt()` a righe 59–64
concatena evidence e claim nello stesso ordine. `judge_pair()` passa claim
ed evidence separatamente al materializzatore. Il raw contiene già le
relation duplicate: il difetto osservabile precede il locator.

Nel modulo `v5_tactical_semantic_support_s2_spatial_v2_extraction.py`, alla
baseline congelata:

- righe 344 e 353: grounding separato e nessun trasferimento fra lati/regioni;
- righe 162–168: descrizioni schema che vincolano claim ad AFFERMAZIONE ed
  evidence a FONTE, presenti anche nello schema effettivo del payload;
- `_occurrences()`, righe 428–435: ricerca `str.find`, case-sensitive,
  tutte le occorrenze anche sovrapposte, senza normalizzazione/fuzzy matching;
- `_localize_fragments()`, righe 438–465: accetta solo una occorrenza;
  zero produce missing, più di una ambiguous;
- `materialize_extraction()`, righe 559–572: claim_relation/claim_text ed
  evidence_relation/evidence_text passati correttamente; arresto se uno dei
  lati fallisce, witness e validation null.

`E_EXTRACTION_LOCALIZATION_NOT_UNIQUE` è il reason code aggregato anche per
zero occorrenze. In questo raw non sono fallimenti da frammento ripetuto
nella sorgente: sono assenze nel lato assegnato.

## Matrice dei sette campi

Ogni riga indica il suffisso del campo sotto `evidence_relation`; ogni percorso
termina in `selected_fragments[0]`. Le posizioni sono intervalli Unicode
code-point `[start,end)` nel claim. Tutti i frammenti hanno **lato assegnato
evidence**, **una occorrenza nel claim** e **zero nell'evidence**.

| Campo evidence | Testo esatto prodotto | Claim: posizione | Evidence | Altre corrispondenze nel raw | Origine osservabile |
|---|---|---|---|---|---|
| subject | `La difesa bassa` | [0,15) | Assente | Identico a claim_relation.subject | Stringa letterale del claim assegnata alla FONTE |
| semantic_axis | `lascia molto spazio` | [16,35) | Assente | Identico a claim.semantic_axis/phase/polarity e evidence.phase/polarity | Stesso frammento del claim ripetuto in più slot |
| value | `molto spazio` | [23,35) | Assente | Identico a claim_relation.value; sottostringa di altri frammenti | Stringa letterale del claim, non della FONTE |
| conditions.items[0] | `molto spazio tra la linea difensiva e la porta` | [23,69) | Assente | Identico a claim_relation.conditions.items[0]; contiene value e quantifier | Frammento esteso del claim assegnato alla FONTE |
| phase | `lascia molto spazio` | [16,35) | Assente | Stesso gruppo semantic_axis/phase/polarity dei due lati | Duplicazione del gruppo testuale del claim |
| quantifier | `molto` | [23,28) | Assente | Identico a claim_relation.quantifier; sottostringa di value/conditions | Quantificatore testuale del claim assegnato alla FONTE |
| polarity | `lascia molto spazio` | [16,35) | Assente | Stesso gruppo semantic_axis/phase/polarity dei due lati | Duplicazione del gruppo testuale del claim |

`claim.` nelle celle compatte significa `claim_relation.`. La matrice JSON
espande i path di tutte le corrispondenze per identità, senza abbreviarle.
Il riuso dello stesso frammento fra slot non è di per sé vietato: l'errore
verificabile qui è l'assenza dal lato evidence, non la condivisione fra slot.

Controllo negativo interpretativo, senza eseguire test: il referente
`tra la linea difensiva e la porta` è presente in entrambi i testi e in
entrambi i campi reference. La relazione duplicata comprende quindi anche
un frammento comune lecito; una regola che vietasse ogni uguaglianza fra
claim ed evidence eliminerebbe anche questa rappresentazione valida.

## Copia, parafrasi e responsabilità

**Copia nell'output:** la duplicazione integrale dei due oggetti, oltre alla
provenienza letterale dei cinque testi dal claim, è osservabile. Non è
dimostrato che il modello abbia prima costruito claim e poi eseguito una
copia, né che abbia ignorato una particolare parte del prompt.

**Parafrasi:** `La difesa bassa` potrebbe isolatamente essere una riformulazione
di `squadre che difendono basse`; il raw non ne rivela il processo di origine.
Resta comunque una stringa non letterale rispetto all'evidence, identica al
claim, e quindi non ammessa per il grounding explicit della FONTE. Non si
può spiegare l'intero fallimento come semplice parafrasi fedele: `molto spazio`
e `lascia molto spazio` non rappresentano letteralmente `togliendo però spazio`,
e il raw assegna abundant a entrambi i lati. Sono errori osservati di
rappresentazione/grounding, non una diagnosi cognitiva del modello.

| Responsabilità | Evidenza | Conclusione e limite |
|---|---|---|
| Generazione | Oggetti uguali e sette frammenti fuori lato già nel content HTTP | Errore di output accertato; meccanismo interno non dimostrato |
| Contratto | Separazione side-bound esplicita; frammenti stringa e vincoli strutturali; verifica sui testi nel locator | Il formato statico non certifica l'appartenenza al testo runtime; limite dichiarato, non nuova contraddizione del contratto |
| Istruzioni | Il messaggio effettivo vieta parafrasi e trasferimenti; schema descrive i lati | Regola presente, quindi non provata una sua omissione; salienza, comprensione e contesto effettivo non isolati |
| Payload/handoff | FONTE ed AFFERMAZIONE fedeli; relazione duplicata già nel raw | Nessuno scambio osservato nell'input o introdotto dal locator; i byte del payload non provano il rendering interno del servizio |
| Locator | Cerca solo nel testo assegnato, rifiuta 0 match; i sette sono assenti | Fail-closed coerente; non è un difetto da correggere cercando nel claim o con fuzzy match |
| Validatore finale | Arresto prima del witness | Non raggiunto: nessun errore o successo attribuibile |

Non disponibili trace del decoder, log del rendering/troncamento, probabilità
dei token o confronto controfattuale controllato. Non si attribuisce il
risultato a ordine FONTE/claim, lunghezza del prompt, schema, bias degli enum,
temperature, capacità linguistica o limiti di contesto senza tali prove.
Gli errori ulteriori di interpretazione dei valori non vengono corretti
automaticamente nell'ambito di questa diagnosi di frammenti.

## Confronto con le precedenti analisi

Il report `tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-03-run-01.md`
documentava un frammento evidence assegnato al lato claim e lì assente:
errore inverso rispetto ai sette di questa nuova risposta. Quel risultato
storico già motivava il divieto di ricollocazione automatica; non viene
rieseguito o ripresentato come scoperta nuova.

Implementazione/revisione locator `tactical-semantic-support-s2-spatial-v2-extraction-locator-01.md`
e `tactical-semantic-support-s2-spatial-v2-extraction-locator-review-01.md`
descrivono la medesima regola letterale side-bound, coerente con il codice
letto oggi. La forense runtime-04
`rag-v5-dual-blocker-runtime04-unknown-same-forensic-01.md` riguardava invece
unknown/same e si arrestava prima del locator. Il nuovo raw non riproduce
quel boundary; raggiungere ora il locator non prova un miglioramento
generativo. Nessuna suite o analisi storica completa ripetuta.

## Verifica futura e arresto

La **verifica della diagnosi è interamente offline**: raw e due testi bastano
per controllare uguaglianza degli oggetti, appartenenza dei frammenti e regola
di selezione del lato. La nuova differenza documentale è la matrice per campo,
con corrispondenze e responsabilità, rispetto al precedente inventario dei
soli missing. Non occorre un'altra generazione per confermare questa causa
prossima, né ripetere adesso questi confronti già pubblicati.

Una futura prova che sostenga di **migliorare la generazione** richiederebbe
invece output nuovo del modello: un replay offline non dimostrerebbe tale
efficacia. Prima servirebbero una correzione specifica e motivata, un delta
tecnico identificabile nel futuro payload/codice e relativa autorizzazione.
Qui quel delta non è selezionabile con evidenza sufficiente: quindi **nessuna
nuova generazione è attualmente giustificata dalla presente diagnosi**.
Non viene proposta una campagna, un'altra indagine ABI o una modifica di
validatori/Gold per accettare il raw.

## Tracciamento e stato

Attività → analisi documentale Python inline JSON/stringhe/hash e lettura
statica, senza script operativo aggiunto → commit documentale → questo
report e fatti nuovi → duplicazione fuori lato accertata, causa interna non
isolata → nessuna correzione minima giustificabile → analisi **ESEGUITO**,
diagnosi **VALIDATO** soltanto nel perimetro documentale.

Report, evidenza, TODO ed Experiment Register pubblicati nello stesso commit;
il commit è identificabile nella storia di questo file e verificato su GitHub.
Working tree finale controllato. Input e risultati originali, codice, prompt,
schema, dataset e validatori invariati. Nessun import applicativo, test,
SSH, Qwen, inferenza, compilazione, merge o deploy. Accuratezza generativa,
compatibilità backend completa, ABI, Gate, integrazione e certificazione
**BLOCCATO**. STOP dopo la pubblicazione della diagnosi.
