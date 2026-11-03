# TSC V2 — revisione forense statica del primo Gate runtime

## Identità e perimetro

- Attività: `RD-TSC-V2-RUNTIME-GATE-FORENSIC-01`
- Gate esaminato: `RD-TSC-V2-RUNTIME-GATE-01`
- HEAD documentale iniziale: `c645c35b1bcfb3d5f886304d13f7cd66c69aedad`
- Baseline tecnica eseguita: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`
- Request ID: `tscv2gate01`
- Metodo: sola lettura di artefatti, codice alla baseline e documentazione Git; nessun test, inferenza o accesso Chroma/API.

Gli SHA-256 rilevati prima e dopo la revisione coincidono:

| Artefatto | Byte | SHA-256 |
|---|---:|---|
| JSON | 58076 | `85b578360639f8e154922d6e70cd753025874124483f9cb956e6f0da920ec22c` |
| stdout | 439 | `7d584972df4b8975b99dfc1354b7a85c920eafb32bf3d639e0cb1bb8ca4f4f97` |
| stderr/time | 1752 | `3b386ff45c874be0ecf6c35b3fe8ad8a8f571af8eba3c65f7a1d00561c2275be` |
| exit code | 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |

## Ricostruzione del percorso

| Fase | Input e trasformazione documentata | Output e controllo | Esito |
|---|---|---|---|
| Domanda/profilo | Domanda sulla copertura del lato debole alla perdita; profilo legacy | Planner deterministico V1 | acquisito |
| Planner/materializzazione | `state_contract` e requisito relazionale esplicito | Piano V2 preflight con una relazione obbligatoria attore→compito→spazio→trigger→finalità | `ready`; V1 valido e copertura V2 `passed` |
| Prompt | Piano applicato autorizzato, requisito e otto evidenze | Istruzione di riprodurre il piano e il blocco canonico | trasmesso |
| Qwen | Modello `qwen3.5:9b` | Envelope JSON con `applied_plan` ed `explanation` | una risposta client, `done_reason=stop`, raw 5015 caratteri |
| Parsing | Envelope JSON | Nessuna normalizzazione (`normalizations=[]`) | parsato |
| Validazione dominio | Piano prodotto dal modello | V1 con 26 issue bloccanti; V2 con termini operativi invalidi | fallita |
| Copertura | Requisito esplicito e relazioni prodotte | relazione invalida esclusa dall'indice di copertura | fallita |
| Piano/prosa | Piano autorizzato e explanation | confronto con blocco canonico esatto | fallito |
| Audit | Explanation ed evidenze recuperate | audit tattico-documentale V1 | `complete=false` |
| Decisione | Tutti i controlli obbligatori | `generation_diagnostic()` | `overall_status=blocked`, answer non promossa, exit 1 |

Il percorso osservato contiene una sola generazione dal punto di vista del client,
`repair_reasons=[]`, nessun rilancio e nessun repair. `done_reason=stop` attesta solo
la terminazione del trasporto, non la qualità o la validità della risposta.

## Piano autorizzato e output effettivo

Il piano preflight richiedeva la relazione
`relation:47fb039bbe2e8c34e657e800a1c7934929c941c2b4b7e38ccc1f3921c1598c3d`,
legata a `question_part:0:segment:0:relation:0`, con attore
`role:explicit:ala`, fase `state:phase:negative_transition` e termini canonici:
`copr`, `lato debole`, `alla perdita`, `per evitare`. Provenienza: `explicit`.

Il raw model output contiene una relazione con gli stessi ID, riferimento requisito,
fingerprint, attore e fase, ma sostituisce i termini normalizzati con
`copertura_lato_debole`, `lato_debole`, `perdita_palla` ed
`evitare_ripartenza`, marcandoli `derived` senza rule ID. Aggiunge inoltre elementi
non presenti nel piano autorizzato (4-3-3, giocatori, evento, assignments,
constraint e trace) e usa `id` invece del richiesto `state_id` negli stati di fase.

L'explanation effettiva è una singola riga:

`[REL 0], Ala, Copertura lato debole, Lato debole, Perdita palla, Evitare ripartenza avversaria, Fase negativa (non possesso), [F1], [F4], [F5]`

Il formato canonico atteso è invece un blocco multilinea con l'ID completo e le
etichette esatte `Attore`, `Compito`, `Spazio`, `Trigger`, `Finalità`, `Fase` ed
`Evidenze`, usando gli identificativi e i termini del piano autorizzato.

## Analisi delle motivazioni

### `invalid_operational_term_identity`

È una violazione reale. `_term_errors()`
(`scripts/v5_tactical_state_contract_v2.py:276`) ricalcola la normalizzazione del
`source_term` e richiede identità con `normalized_term`. Per tutte le quattro
dimensioni il modello ha conservato il source term ma prodotto un normalized term
diverso. Non è intervenuta alcuna normalizzazione del parser. La provenienza
`derived` senza rule ID è inoltre incompatibile, ma il controllo di identità termina
prima e tale secondo difetto non produce un codice separato.

### `explicit_operational_requirement_omitted`

Il requisito non manca letteralmente dal raw: la relazione contiene il corretto
`requirement_ref` e fingerprint. Tuttavia è strutturalmente invalida. In
`validate_operational_relations()` (`v5_tactical_state_contract_v2.py:343`), le
relazioni con errori non entrano in `by_requirement` (righe 379–388); la successiva
ricerca (righe 412–418) emette quindi anche `explicit_operational_requirement_omitted`.
La mancata copertura mediante una relazione **valida** è reale, ma la parola
“omitted” è diagnostica fuorviante: confluisce un candidato presente ma invalido con
un requisito davvero assente. Questo è un difetto deterministico dimostrato del
validatore, non la causa della corretta decisione fail-closed.

### `canonical_relation_block_mismatch`

È una violazione generativa dimostrata. `_canonical_blocks()`
(`scripts/v5_tactical_state_generation_v2.py:130`) confronta il blocco esatto.
La prima divergenza è `[REL 0]` invece dell'ID completo; seguono formato su una sola
riga, attore e fase non espressi tramite i riferimenti richiesti, termini diversi da
quelli autorizzati e lista evidenze non nel formato canonico. Il codice emette il
mismatch alla riga 177.

### `noncanonical_free_prose`

Il testo contestato è l'intera explanation sopra riportata: non viene consumata da
alcun blocco canonico e il controllo alla riga 195 la segnala. Il codice diagnostico
è coerente col contratto di formato; l'etichetta non è un giudizio stilistico. Il
testo aggiunge anche “avversaria” e “fase negativa (non possesso)” rispetto ai
termini esatti, ma non è necessario stabilire la loro correttezza tattica per
concludere la non conformità.

### `tactical_documentary_audit_failed`

L'audit (`scripts/v5_tactical_query_plan_v1.py:868`) ha ricevuto l'explanation
effettiva e le otto evidenze. Registra `complete=false`, relazione non dimostrata,
`where` mancante e dettagli mancanti: densità/prossimità, palla coperta/scoperta,
zona di campo e struttura preventiva. F1 sostiene direttamente la copertura del lato
debole dell'ala; F4 pressione/scalate/copertura; F5 copertura del cambio di gioco e
protezione della zona. Le fonti non rendono quindi l'audit privo di base, ma la
risposta non dimostra il requisito nel formato e nell'ampiezza richiesti.

L'esito negativo dell'audit è dimostrato. La ripartizione causale completa tra
insufficienza generativa e compatibilità fra il blocco canonico V2, volutamente
conciso, e i dettagli più ampi richiesti dall'audit V1 non è determinabile senza una
specifica ulteriore: esiste un rischio statico concreto di disallineamento, ma non è
stato eseguito alcun test nuovo per provarlo come causa universale.

## Matrice di attribuzione

| Violazione | Evidenza raw | Evidenza piano | Validatore | Causa attribuibile | Certezza |
|---|---|---|---|---|---|
| `invalid_operational_term_identity` | quattro normalized term divergenti | quattro termini canonici espliciti | `_term_errors()` | generazione Qwen | dimostrata |
| `explicit_operational_requirement_omitted` | relazione presente ma invalida | requisito obbligatorio presente | `validate_operational_relations()` | validatore (etichetta diagnostica); generazione per la copertura invalida | dimostrata |
| `canonical_relation_block_mismatch` | `[REL 0]` e riga non canonica | blocco esatto con ID completo | `_canonical_blocks()` | generazione Qwen | dimostrata |
| `noncanonical_free_prose` | explanation interamente non consumata | nessuna prosa extra ammessa | `_canonical_blocks()` | generazione Qwen | dimostrata |
| `tactical_documentary_audit_failed` | explanation concisa e relazione non dimostrata | evidenze F1/F4/F5 pertinenti ma non sufficienti al controllo | `audit_answer()` | generazione Qwen / audit documentale | probabile; ripartizione non determinabile |

`question_compatibility=passed` non contraddice questi risultati: il controllo V1
copre i fatti espliciti della domanda, non certifica validità strutturale o copertura
operativa V2.

## Fail-closed

Le evidenze confermano `overall_status=blocked`, exit 1, raw conservato, answer e
`promoted_answer` vuoti, diagnostica strutturata, zero retry e zero repair. I quattro
artefatti sono integri. Il blocco è coerente con `generation_diagnostic()` e con la
baseline. È **VALIDATO** il fail-closed del singolo caso, non il superamento del Gate.

## Analisi separata dell'anomalia Chroma

Il runner apre la collection mediante `chromadb.PersistentClient(path=DB)`
(`scripts/smoke_test_rag_v5_e2e.py:471`) e chiama `count()` prima e dopo. Tale client
non è aperto con una modalità filesystem dimostrabilmente read-only; inizializzazione
o housekeeping possono scrivere metadata SQLite. Durante la finestra era inoltre
attiva l'API RAG, potenziale utilizzatore concorrente della stessa collection.

`index_unchanged` è calcolato esclusivamente confrontando i count
(`smoke_test_rag_v5_e2e.py:714–717`): significa 6410→6410, non identità byte del
database. Gli hash delimitano la modifica all'intervallo fra le due acquisizioni, ma
non identificano l'autore. Dimensione invariata e sidecar assenti non risolvono
l'attribuzione. Non esiste evidenza acquisita di modifica a documenti, embedding,
collection o schema, né di corruzione o integrità completa.

Conclusione: la variazione di `chroma.sqlite3` è reale, ma causa e contenuto sono
**non determinabili**. Non è attribuibile né al Gate né al servizio concorrente con
le evidenze autorizzate.

## Limiti e remediation minima proposta

Non sono disponibili conteggi server-side indipendenti delle richieste, una traccia
SQLite delle pagine cambiate o un isolamento completo dagli altri client. Questi
limiti non invalidano la diagnosi delle violazioni contenute negli artefatti.

Prima di qualunque nuova decisione runtime è giustificata una sola remediation
deterministica delimitata: distinguere nel risultato di copertura
`present_but_invalid` da `omitted`, senza rimuovere gli errori strutturali e senza
alterare il fail-closed. Deve essere verificata offline con casi differenziali per
relazione assente, presente-invalida e presente-valida. Non è autorizzata né
implementata in questa attività.

Il possibile disallineamento fra blocco canonico V2 e audit V1 richiede una decisione
contrattuale separata prima di un nuovo Gate; le evidenze correnti non giustificano
una modifica silenziosa dell'audit o del prompt. Le violazioni generative osservate
non autorizzano automaticamente una seconda inferenza.

## Decisione e stati

- revisione forense statica: **VALIDATO**;
- unica esecuzione Gate: **ESEGUITO**;
- fail-closed del singolo caso: **VALIDATO**;
- Gate runtime TSC V2: **BLOCCATO**;
- integrazione runtime: **BLOCCATO**;
- certificazione runtime: **BLOCCATO**.

La decisione combina Caso A per le violazioni generative dimostrate, Caso B per la
diagnostica `omitted` deterministica e Caso C per l'attribuzione Chroma e per la
ripartizione completa della causa dell'audit.
