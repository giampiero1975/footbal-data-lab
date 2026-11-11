# H3 — Ledger dei vincoli, congiunzioni e controlli esterni

Precisazione documentale IMPLEMENTATO, non converter/matcher implementato.
Nessuna modifica allo schema extraction, al Python o ai manifest approvati.
Non viene rieseguito il controesempio o l'audit 25/25 già concluso.

## Categorie tecniche distinte

Le categorie non sono stati del progetto e non sono una dichiarazione di
compatibilità. Scope e certezza dell'evidenza devono accompagnarle sempre.

| ID | Classificazione tecnica | Significato e prova | Conseguenza |
|---|---|---|---|
| H3-C1 | Errore di conversione o parsing | Eccezione/errore osservato nello stadio specifico, con hash input e diagnostica; distinguere converter da parser | Nessun linguaggio validamente prodotto nel relativo passo; non chiamarlo perdita silenziosa |
| H3-C2 | Vincolo schema non rappresentato | Restrizione presente nello schema ma persa nel ramo/dialetto esaminato; prova statica o sperimentale identificata, non semplice keyword assente | Coverage incompleta anche se conversione e parse fossero riusciti |
| H3-C3 | Vincolo presente, enforcement non verificato | Campo/congiunzione presente ma mancano evidenze sufficienti per quel target/dialetto/contesto | Non promuovere a supportato; non confondere con perdita già dimostrata in altro scope |
| H3-C4 | Controllo deliberatamente esterno allo schema | Invariante Python/procedurale non espresso come restrizione JSON Schema, con riferimento al predicato autorevole | Non è un errore del converter né un keyword omesso; resta fuori dalla sua prova |
| H3-C5 | Annotazione non restrittiva | Campo documentale/identificativo valutato nel suo ruolo effettivo, senza restrizione da far rispettare alla grammatica | Non contarlo come enforcement perso o come vincolo verificato |

Gli errori di processo del supervisore H2 sono una dimensione ulteriore: senza
prova di ingresso nel converter non diventano H3-C1. Nessun stderr vuoto,
exit zero o parse=true autorizza un verdetto automatico di piena compatibilità.

## Unità e campi del ledger futuro

L'unità non è il solo nome del keyword: è un vincolo o una combinazione nella
sua posizione, con direzione dei ref e ramo/dialetto/target. Per ogni voce:

- Identità dello schema originale approvato e sua provenienza; hash del file,
  non un hash assunto dalla sola dimensione.
- JSON Pointer concreto alla restrizione e lista dei pointer della congiunzione;
  traccia dei ref risolti e ruolo del nodo, con escaping ~0/~1 ove necessario.
- Ramo anyOf interessato e dialetto (GBNF o altro), flag e identità del target.
- Classificazione H3-C1–C5, campo applicabile e proprietà non dimostrata.
- Evidenza: source revision/path/righe/hash e tipo di prova (statica, da eseguire
  o osservata); non dichiarare osservato un risultato mai prodotto.
- Impatto, controllo deterministico residuo e riferimento al predicato Python;
  un controllo residuo non trasforma C2 in C4.
- Esito conversione, esito parser e classificazione coverage separati.

Per C4, quando una restrizione schema non esiste, `schema_pointer=null` è
corretto: usare un `instance_pointer` pertinente e il riferimento al predicato,
non inventare un keyword o un JSON Pointer a un campo inesistente. Per C1
senza localizzazione affidabile usare il pointer null e lo stadio documentato.
Le annotazioni non sono automaticamente restrizioni solo perché sono stringhe;
$id/$schema restano identificativi di formato, senza fetch o caricamento remoto.

L'inventario deve visitare soltanto nodi schema: properties, items, anyOf e
$defs/ref, distinguendo nomi di proprietà e valori enum/const. Deve esaminare
anche pattern con min/maxLength, anyOf con ref, required con properties e
additionalProperties, cardinalità array con items e uniqueItems. Il solo
riconoscimento dei singoli keyword non prova la loro congiunzione. Ogni ref
esterno o ciclo/ambiguità non gestibile arresta il preflight, senza riscritture.

## Controesempio statico già verificato — pattern e lunghezza

Fonte approvata dalla revisione indipendente c99a456:
llama.cpp `620d2225cc436ab0b001e3200e590e3b286ef9ab`,
`common/json-schema-to-grammar.cpp`,
`common_chat_schema_converter::visit`, case KIND_STRING, righe 933–948.
Il ramo pattern ritorna a 935–936, prima del ramo min/maxLength a 945–948.
Hash e URL della fonte restano quelli del sources-lock.json congelato e
[la prova statica precedente](../../../docs/backend-harness-design-independent-review-evidence-01.json).
Non vengono acquisiti nuovamente i 25 sorgenti.

Lo schema concreto combina pattern `^entity:.+$`, minLength=8, maxLength=71.
`entity:` seguito da 65 caratteri `a` ha 72 caratteri: soddisfa il pattern ma
supera maxLength=71. minLength=8 è implicato dal pattern per questo caso, mentre
il limite massimo non lo è. Nessuna stringa di prova viene inviata al backend.

| Voce | JSON Pointer concreto al limite | Ramo/dialetto | Classificazione e impatto |
|---|---|---|---|
| H3-E1 | /$defs/relation/properties/subject/anyOf/0/properties/entity_id/maxLength | subject explicit, ramo GBNF pubblico | H3-C2 nello scope sorgente: lunghezza massima non congiunta al pattern |
| H3-E2 | /$defs/relation/properties/subject/anyOf/1/properties/entity_id/maxLength | subject implicit, ramo GBNF pubblico | H3-C2 nello scope sorgente: medesima perdita di enforcement |
| H3-E3 | /$defs/relation/properties/reference/anyOf/0/properties/entity_id/maxLength | reference explicit, ramo GBNF pubblico | H3-C2 nello scope sorgente: medesima perdita di enforcement |
| H3-E4 | /$defs/relation/properties/reference/anyOf/1/properties/entity_id/maxLength | reference implicit, ramo GBNF pubblico | H3-C2 nello scope sorgente: medesima perdita di enforcement |

Per ciascuna voce, i pointer della congiunzione sono i fratelli pattern,
minLength e maxLength sotto lo stesso entity_id; i ref d'uso claim/evidence
rimandano al nodo condiviso $defs/relation. I pointer in tabella sono pointer
al documento schema, non wildcard o esempi con parentesi da interpretare.

L'osservazione riguarda il ramo GBNF dei sorgenti pubblici esaminati, NON una
prova sulla VPS. Il dialetto/flag e la corrispondenza binaria non sono attestati:
per lo scope libreria installata, la corrispondente conclusione di enforcement
rimane H3-C3. Non trasferire una prova da uno scope all'altro come osservazione.

Controllo residuo invariato: `_representation_errors` richiama
`spatial_v2._valid_entity_id`, che mantiene il limite 71 anche nel validatore
finale. L'evidenza è nei sorgenti Python già versionati. Non correggere ID,
comparison o label, non allungare il limite e non eliminare maxLength dallo
schema per far riuscire il converter. Una rejection Python non rende completa
la grammatica e non prova un miglioramento generativo.

## Altri esempi di classificazione, non nuovi test

| Oggetto | Pointer/posizione | Categoria e scope | Responsabilità residua |
|---|---|---|---|
| uniqueItems dei frammenti | /$defs/relation/properties/subject/anyOf/0/properties/selected_fragments/uniqueItems | H3-C2 nel builder GBNF pubblico già esaminato; enforcement VPS H3-C3 | `_fragments_valid` verifica duplicati; vincolo presente nello schema, non C4 |
| Coerenza dei comparison fra lati | schema_pointer=null; instance_pointer=/comparison | H3-C4, deliberatamente esterno come regola fra campi | `extraction_semantic_errors` e `_comparison_errors` restano autorevoli |
| Grounding letterale e label | schema_pointer=null; instance_pointer=/claim_relation e /label | H3-C4 per le relazioni semantiche non espresse dal solo schema | Locator side-bound e validatore finale; non è enforcement provato dal converter |
| Descrizione subject | /$defs/relation/properties/subject/description | H3-C5, annotazione | Nessuna restrizione semantica dichiarata persa |
| Eccezione del converter | pointer dello schema solo se provato, altrimenti null | H3-C1 soltanto se osservata nel converter; qui nessuna esecuzione | Diagnostica e H2, nessuna attribuzione inventata |

Un eventuale ritorno del converter e il parsing della grammatica sono passi
tecnici diversi dall'enforcement del decoder, dal percorso format/ThinkingClose
e dai predicati Python. Il ledger deve conservarne i confini e non trasformare
le restrizioni deliberatamente esterne in prove di compatibilità completa.
`promotion_authorized=false`; nessuna nuova autorizzazione all'esecuzione.
