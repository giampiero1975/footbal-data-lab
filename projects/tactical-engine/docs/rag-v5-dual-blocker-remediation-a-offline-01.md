# RAG V5 — remediation offline A dopo runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-REMEDIATION-A-OFFLINE-01`.
Data: 2026-11-10, Europe/Rome.

## Attività

Implementata soltanto l'alternativa A della forense runtime-04: handoff
normativo e contratto extraction correlato, senza derivazione sistemica B,
repair, normalizzazione del raw o forzatura della label.

Prima delle modifiche riconciliati TODO, Experiment Register, forense
`rag-v5-dual-blocker-runtime04-unknown-same-forensic-01.md`, originali e
controlli precedenti. HEAD iniziale locale/GitHub
`8fca97fdf596d00f14987c5527694056d382e802`, branch
`codex/tactical-state-contract-v1`, working tree pulito. Baseline applicativa
precedente `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`; nessuna divergenza
di stato o modifica applicativa intermedia non riconciliata.

I 37 controlli extraction/Spatial V2 e i 13 del wrapper erano già conclusi:
non sono stati rieseguiti. La differenza che giustifica i nuovi controlli è
il nuovo contratto status/contenuto, assente in quelle verifiche. La
giustificazione è registrata nella docstring della nuova suite prima del run.

## Script e commit

Commit tecnico:
`0ea62c0ef1f0adfcd928c2893f069de060275381`.
[Diff tecnico completo](https://github.com/giampiero1975/footbal-data-lab/commit/0ea62c0ef1f0adfcd928c2893f069de060275381).

Il commit modifica soltanto:

- `scripts/shadow_nli_spatial_relations_v2_inference.py`;
- `scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py`;
- nuova suite `tests/test_v5_spatial_extraction_status_contract_v1.py`.

Report, risultati, TODO e registro pubblicati insieme con commit documentale
successivo nella stessa sessione, identificabile dalla storia di questo report.
Risultati strutturati: `docs/runtime04-remediation-a-offline-results-01.json`.
Nessuna modifica a validator finale, locator, Gold/dataset, originali,
panel, wrapper o staging; nessun runtime-05 creato.

## Delta implementato

### Handoff normativo

`extraction_handoff_instructions()` costruisce soltanto testo, senza I/O o
modelli. Le matrici asse/valori e tutte le coppie incompatibili vengono lette
dalle costanti Spatial V2 già versionate, anziché ricopiate in una seconda
tabella semantica. Il judge usa il testo solo per l'opt-in extraction.

Esplicitati:

- explicit, implicit, absent, ambiguous, unknown, con sentinelle e cardinalità;
- stati ammessi per famiglia, inclusi implicit/general, implicit/none e
  implicit/affirmed, contro unknown/unknown;
- ID concreti e sentinella, condizioni e item, contenitore distinto dall'item;
- precedenza degli stati su ID/valori, incluse le particolarità conditions;
- confronti deterministici, compatible shadow e different, quantità e literal;
- incompatibilità versionate e precedenze per la proposta di label;
- distinzione disponibilità, posizione relativa e moto/avanzamento;
- grounding separato claim/evidence e divieto di inventare certezza per
  soddisfare il formato.

Non inseriti Gold, ID q3_04 o regole lessicali del caso. Nessuna nuova chiamata,
parametro, timeout, retry, repair o fallback. Prompt normativo: 6.594 byte UTF-8;
il suo costo effettivo nel tokenizer e il budget della build reale restano
non misurati in questa fase offline.

### Schema di trasporto e controllo deterministico

Gli slot usano alternative `anyOf` complete, ciascuna con status fissato e
contenuto/frammenti correlati. Non si mescolano properties e anyOf nello stesso
nodo. Restano invariati i campi finali del contratto; ID/versione di dominio
restano 1.0.0, già definiti dalle regole finali. La revisione del trasporto è
tracciata nel descriptor opt-in come `representation_revision=status-correlated-01`.

Principali correlazioni:

| Famiglia | Vincolo nuovo sul trasporto |
|---|---|
| Entità unknown | entity:unknown, zero frammenti |
| Entità ambiguous | entity:ambiguous, 1–4 frammenti |
| Entità concrete | explicit con frammenti oppure implicit senza frammenti |
| Asse/valore | explicit concreto con frammenti, oppure sentinella coerente; niente implicit |
| Phase | implicit/general senza frammenti, unknown/unknown senza frammenti, altri stati correlati |
| Quantifier | implicit/none, literal null salvo numeric esplicito non vuoto; frammenti correlati |
| Polarity | implicit/affirmed oppure explicit/negated; unknown/unknown, ambiguous/ambiguous |
| Conditions | absent/unknown con items vuoti; explicit/ambiguous con item ancorati |

Lo shape check aggiunge `_representation_errors()` solo dopo la validità
strutturale dei campi. Controlla le stesse correlazioni finali senza localizzare
o inventare anchor. ID e cardinalità residui sono verificati deterministicamente.
Nuovo dettaglio `E_EXTRACTION_STATUS_CONTENT_INCONSISTENT` con path del campo,
entro il boundary esistente `E_EXTRACTION_SCHEMA_INVALID`.

`extraction_semantic_errors()`, materializzazione, locator side-bound,
provenance, boundary e validatore finale sono invariati. Non viene riscritto
un campo per superare il controllo; un'incoerenza di comparison su slot
correttamente rappresentati continua a produrre il boundary semantico precedente.

### Limiti espliciti del subset

La [documentazione upstream llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)
elenca limiti per i condizionali, contains e not, e per properties mescolato
con anyOf. Il [parser upstream](https://github.com/ggml-org/llama.cpp/blob/master/common/json-schema.cpp)
gestisce alternative anyOf/oneOf. La patch evita i primi costrutti e usa
alternative complete. Queste fonti descrivono upstream, non attestano la
corrispondenza con la build VPS specifica.

Restano fuori dalla grammatica: almeno un item ambiguous nel contenitore
ambiguous, unicità degli ID conditions, esclusione delle sentinelle dagli ID
concreti, alfabeti completi degli ID e restrizione absent dei target claim.
Sono tutti controllati deterministicamente. L'annotazione uniqueItems dei
frammenti, già presente, non è assunta come garanzia del decoder: il controllo
di duplicati Python resta attivo. Comparison tra lati e correttezza semantica
non sono delegati allo schema.

Non è stato installato un validatore JSON Schema o eseguito un compilatore
della grammatica della build remota. Il checker dei test interpreta soltanto
il subset esplicitamente usato; non è una certificazione Draft 2020-12 o
backend. Schema serializzato compatto: 16.869 byte UTF-8. Nessuna compatibilità
runtime dichiarata; le limitazioni non vengono compensate con repair o fallback.

## Verifiche nuove effettivamente eseguite

Comando della sola nuova suite:

```text
python -B projects/tactical-engine/tests/test_v5_spatial_extraction_status_contract_v1.py
```

Primo run di sviluppo: 13/13 PASS. La revisione locale ha rilevato duplicazioni
di inserimento nelle modifiche, eliminate prima del commit; completate anche
le istruzioni sull'identità dell'asse e sul primo carattere degli ID. Aggiornato
il replay per usare i testi originali registrati. Aggiunti controllo di unicità
delle definizioni e controllo della matrice normativa; motivata la riesecuzione
nel codice dei nuovi test. Run dopo revisione: **15/15 PASS**, 0,602 s.

Controllo aggiuntivo nuovo, da solo:

```text
python -B projects/tactical-engine/tests/test_v5_spatial_extraction_status_contract_v1.py StatusContractDeltaTests.test_new_representation_checks_match_final_slot_predicates
```

**1/1 PASS**, 0,142 s: 1.050 combinazioni limitate di stato/contenuto
confrontate con i predicati finali invariati, usando anchor letterali valide
nei soli test. La patch applicativa non crea tali anchor.
Totale finale: **16 controlli differenziali distinti coperti positivamente**.
Non è una ripetizione delle suite storiche 37/37 o wrapper 13.

Copertura:

- unknown legittimo senza contenuto concreto resta ammesso nello shape;
  target claim non determinabile resta non valutabile e non promosso;
- phase unknown legittima può restare insufficient con witness valido shadow;
- unknown con ID, valore o frammenti concreti respinto senza mutare il dato;
- unknown prevale su uguaglianza di ID/valori; comparison same incoerente
  continua a essere respinto dal precontrollo semantico;
- contenitore conditions distinto dagli item ambiguous, con controlli residui;
- correlazioni numeric/literal, implicit e sentinelle;
- singolo payload mock con regole normative, lati e parametri invariati;
- confronto frozen del payload/risultato legacy e AST delle sue funzioni;
- replay del raw runtime-04 identico agli originali, senza eseguire il locator;
- schema JSON serializzabile, riferimenti locali e alternative finite;
- AST invariato delle funzioni critiche e file finali/dataset/ops immutati;
- nessuna duplicazione delle funzioni o delle chiamate di correlazione;
- parità limitata con i predicati finali già versionati.

## Risultato del replay e invarianti

Il raw runtime-04 continua a proporre supported: non è stato corretto.
Ora viene respinto già dallo shape correlato, con
`E_EXTRACTION_SCHEMA_INVALID` e dettagli status/contenuto, senza witness,
validation o record di localizzazione, `promotion_authorized=false`.
Gli hash dei 27 originali restano identici prima/dopo. Una rejection più
precoce non è una prova di maggiore accuratezza generativa.

Il confronto frozen del percorso legacy verifica identità di payload e
risultato: nessuna modifica inevitabile al legacy da sottoporre ad eccezione.
Non modificati modello, token, contesto o trasporto. Nessuna forzatura di
comparison unknown o label contradicted, nessun risultato promosso.

## Decisione → Stato

Patch **IMPLEMENTATO** localmente; nuove verifiche **ESEGUITO** e proprietà
coperte **VALIDATO** offline. Non risultano blocchi per il perimetro locale.

**Raccomandata una revisione indipendente prima di qualsiasi nuova prova
generativa:** deve controllare la corrispondenza delle nuove correlazioni con
il dominio finale, le limitazioni del subset, l'incertezza legittima, il budget
del prompt e l'assenza di normalizzazioni/promozioni implicite. La build backend
non è stata provata, il grounding abundant/scarce resta responsabilità
generativa e una shape più stretta può indurre falsa certezza: i soli test
offline non risolvono questi punti.

STOP dopo pubblicazione. Nessun runtime-05, staging o wrapper creato,
nessun accesso o trasferimento VPS, Qwen, altro modello, merge, deploy o
modifica a indici/corpus/servizi/panel. Accuratezza delle contraddizioni,
Gate, integrazione e certificazione restano **BLOCCATO**.
