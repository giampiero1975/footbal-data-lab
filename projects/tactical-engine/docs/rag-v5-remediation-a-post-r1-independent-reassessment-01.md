# RAG V5 — rivalutazione indipendente incrementale dopo R1

Attività: `RD-RAG-V5-REMEDIATION-A-POST-R1-INDEPENDENT-REASSESSMENT-01`.
Data: 2026-11-10, Europe/Rome.

## Attività → Script → Commit → Report

Revisione documentale incrementale dopo R1. Non ripetuta la revisione completa
`c00af6d`, né l'inventario dello schema. **Unica decisione: A — contratto idoneo
alla successiva verifica separata del backend.** Nessuna generazione autorizzata
e nessuna compatibilità reale del backend dichiarata.

Riconciliati TODO ed Experiment Register con GitHub: branch
`codex/tactical-state-contract-v1`, origin
`https://github.com/giampiero1975/footbal-data-lab.git`, HEAD iniziale
locale/remoto `5794e2c26938aaacaac206685a886993b66cb6f1`, working tree pulito.
Nessuna rivalutazione post-R1 già registrata nei documenti del medesimo HEAD.
Letti revisione indipendente e relativi fatti, closeout R1, risultati originali
16 controlli e nuovi 5 controlli, diff remediation A `0ea62c0` e correzione
`5bfa4897e93d5d8edef0bc79371aa36b1b1409ae`. I PASS pubblicati sono evidenze
storiche, non un'assunzione di assenza di difetti e non sono stati rieseguiti.

Script: comandi locali read-only `git show`, `git diff`, lettura sorgenti e
raccolta Python inline di soli AST/literal/JSON e hash dei blob. Nessun import
applicativo, chiamata di helper di dominio, test, compilazione schema o backend.
La raccolta decodifica il Return AST dell'handoff soltanto con concatenazioni
di stringhe e json.dumps di matrici costanti: non esegue la funzione del progetto.
La prima raccolta ha incontrato un errore nel lettore AST (campo lista trattato
come metodo), corretto nel solo comando documentale; nessun file applicativo
o test è stato modificato. Raccolta finale completata.

Evidenze statiche nuove:
`docs/remediation-a-post-r1-independent-reassessment-facts-01.json`.
Commit: documentale che pubblica insieme report, fatti, TODO e registro,
identificabile senza autoriferimento circolare con:

```text
git log -1 --format=%H -- projects/tactical-engine/docs/rag-v5-remediation-a-post-r1-independent-reassessment-01.md
```

## Chiusura indipendente di R1

Il confronto dei blob a c00af6d e 5794e2c conferma che l'intero sorgente extraction
nuovo è esattamente quello precedente dopo la sola sostituzione della frase
Quantifier confrontabile, documentata dal closeout. Il resto del file è
identico, compresi schema, shape check, precontrollo, locator e materializzazione.
Validatore finale e judge sono blob identici. Il nuovo test R1 è soltanto letto.

Il testo aggiornato (extraction:358) applica stati prima dei valori e uguaglianza
dei value prima del dispatch quantifier. Il percorso reale nel validatore è:
`_expected_comparison():344` → precedenze degli stati → `cvalue == evalue:363`
→ return same → solo per value diversi dispatch a `:370`.
Con due numeric espliciti, literal 2 e 3, i value coincidono: same è ammesso
senza raggiungere il confronto dei literal del helper `:375–380`.
Questo è un percorso letto staticamente, non un nuovo test eseguito.

La frase «semantica attuale del contratto versionato, non una regola di
correttezza numerica generale» è presente. Nessun valore viene corretto per
ottenere same. `_comparison_errors()` calcola un insieme locale di confronti
ammessi, non riscrive il confronto proposto. Il finale segnala eventuale
mismatch di label; la label derivata diagnostica non è un repair del raw.
Restano nessun retry/fallback e promotion_authorized=false, senza nuove modifiche.

**R1 chiuso indipendentemente nel perimetro documentale.** Il limite numerico
è preservato e dichiarato, non risolto semanticamente.

## Ricerca incrementale: precedenze e confronti fra relazioni

Riferimenti al commit iniziale 5794e2c, sotto `projects/tactical-engine/scripts/`:
E = `v5_tactical_semantic_support_s2_spatial_v2_extraction.py`;
V = `v5_tactical_semantic_support_s2_spatial_v2.py`.
Le situazioni seguenti sono letture manuali dei rami, non fixture eseguite.

| Ambito | Istruzione e percorso effettivo | Esito della lettura incrementale |
|---|---|---|
| Unknown/ambiguous | E:356; V:344–361. Per slot ordinari ambiguous precede absent/unknown, che precedono ID/value. Unknown contro ambiguous restituisce ambiguous, non same | Coerente; l'uguaglianza delle sentinelle non supera gli stati |
| Entità e assi | E:357; V:359–372. ID uguali same; ID diversi compatible/different. Assi confrontabili uguali same, diversi different | Coerente; compatible resta dichiarazione shadow, non coreferenza indipendente |
| Valori spaziali | E:357; V:388–410. `_comparison_errors` raffina il risultato del helper solo se non unknown/ambiguous: assi diversi different; stesso asse coppia incompatibile, poi uguaglianza, poi different | Coerente col caller effettivo, non soltanto col helper |
| Quantifier non numeric | E:358; V:363–385. Valori uguali same prima del dispatch; valori diversi seguono forza evidence rispetto al claim, always/never incompatible, altri different | Coerente: many evidence contro some claim compatible; direzione inversa different; many/many same |
| Conditions | E:356; V:346–355. Status del contenitore ambiguous, poi unknown, poi liste ordinate degli ID; nessuna propagazione automatica dello status degli item | Coerente; due contenitori absent con liste vuote possono essere same, non sono soggetti alla regola absent degli altri slot |
| Polarity | E:357; V:356–369. Stati prioritari, uguaglianza same, affirmed/negated incompatible | Coerente; riduzione dello spazio non diventa automaticamente negazione grammaticale |
| Label/evidenza | E:359; V:413–435, chiamato dal finale dopo relation/comparison check | Nessuna nuova prescrizione esplicita opposta ai return; persiste la sintesi meno precisa già documentata |

Passaggio particolarmente rilevante per evitare un secondo errore caller/helper:
con value stable su distance_change e area_extent, il helper isolato vede valori
uguali e propone same; `_comparison_errors` rileva assi diversi e ammette invece
different. L'handoff dice esplicitamente assi differenti=different. Sullo stesso
asse space_availability, abundant/scarce è invece incompatible, dopo gli stati.
Non è un nuovo rilievo: è una verifica statica del percorso composto effettivo.

### Label: precedenze reali e limite della formulazione

Il percorso `validate_spatial_v2` esegue relation check, comparison check e poi
`_derive_label`. Ordine effettivo:

1. Claim core absent/unknown/ambiguous: nessuna label derivabile,
   E_RELATION_NOT_COMPARABLE.
2. Evidence core absent/unknown/ambiguous: insufficient.
3. Comparison subject/axis/reference/conditions/phase different/unknown/ambiguous:
   insufficient, prima di eventuale incompatibilità value/polarity.
4. Value o polarity incompatible: contradicted, prima dell'insufficienza quantifier.
5. Quantifier different/unknown/ambiguous: insufficient.
6. Value same/compatible, polarity same e quantifier same/compatible: supported.
7. Ogni residuo: insufficient.

Esempi di lettura: fase unknown con valori incompatibili resta insufficient;
condizioni allineate e valore incompatible con quantifier different resta
contradicted; always/never nel solo quantifier produce comparison incompatible,
ma non attiva il ramo contradicted riservato a value/polarity e ricade in
insufficient se non sussiste altra incompatibilità. Il prompt non prescrive
contradicted per l'incompatibilità del solo quantifier.

La frase «non dimostra supporto» non specifica letteralmente insufficient in
tutti i casi, e «quantifier non confrontabile» è una sintesi, non un elenco
esaustivo dei rami. È il limite **Non bloccante** già registrato in c00af6d,
non una nuova contraddizione normativa accertata. Non prescrive di emettere
supported o contradicted quando il finale impone insufficient. La clausola
«su relazioni confrontabili» e l'obbligo di rispettare tutte le precedenze
vanno letti insieme alle restrizioni precedenti, non come loro sostituzione.
Non si dichiara per questo il testo una specifica esaustiva del derivatore.

Nessun nuovo rilievo bloccante: non esiste quindi un nuovo controesempio
accertato handoff/codice da correggere automaticamente. Restano limiti del
contratto: identità/compatible e conditions basate su ID, grounding non prova
equivalenza semantica, numeric con literal diversi può essere same. Sono
comportamenti versionati, non un miglioramento generativo. Nessun locator o
validatore finale modificato; nessun errore attribuito a componenti non eseguiti.

## Budget documentale: solo delta R1

| Componente | Conferma incrementale |
|---|---|
| Handoff UTF-8 | **6.967 byte**, ricostruzione statica dai literal e dalle matrici costanti |
| User, stessa coppia storica | **7.311 byte**, stessa concatenazione FONTE/evidence/AFFERMAZIONE/claim |
| Delta R1 | **+373 byte**, sola frase sostituita |
| Schema | Invariato; **16.869 byte** dalla misura pubblicata precedente, senza ricostruire o ricompilare lo schema |

Nessuna conversione byte/token. Costo nel tokenizer reale, politica di contesto,
eventuale troncamento ed effettiva compilazione/enforcement della grammatica
restano non verificati. Il limite statico non viene interpretato come fallimento
o successo del backend. Nessun accesso a VPS, Ollama o modelli.

## Risultato → Decisione → Stato

**Unica decisione: A — Contratto idoneo alla successiva verifica separata del
backend.** R1 è chiuso sul delta effettivo; la ricerca incrementale dei percorsi
tra due relazioni non ha individuato altre contraddizioni normative bloccanti.
Il limite sulla sintesi delle label non ostacola la verifica di compatibilità
del decoder, ma non costituisce prova della qualità delle future risposte.

La decisione è di idoneità al passo separato, non di compatibilità già provata
e non autorizza una generazione. Nessuna verifica backend svolta nella sessione.
Il prossimo passo proposto richiede una distinta attività nel proprio perimetro;
non è stato eseguito automaticamente.

Rivalutazione **ESEGUITO** e **VALIDATO** come analisi documentale incrementale;
patch **IMPLEMENTATO**, evidenze offline precedenti conservate. Verifica backend
**DA FARE**, compatibilità reale non dimostrata. Accuratezza generativa delle
contraddizioni, Gate, integrazione e certificazione **BLOCCATO**.

Pubblicati contestualmente report, nuovi fatti statici, TODO ed Experiment
Register. Nessun report precedente riscritto o invalidato. Zero codice/test
modificati, test applicativi eseguiti, VPS, inferenze, runtime-05, staging,
wrapper, merge o deploy. STOP dopo pubblicazione.
