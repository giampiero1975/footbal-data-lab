# RAG V5 — revisione indipendente del progetto harness non generativo

Attività: `RD-RAG-V5-BACKEND-HARNESS-DESIGN-INDEPENDENT-REVIEW-01`.
Data: 2026-11-11, Europe/Rome.

## Attività → Script → Commit → Report

**Unica conclusione: A — progetto documentale adeguato per affrontare il
prerequisito ABI in un'attività separata.** Non è una specifica esecutiva già
approvata. I rilievi H1–H3 sotto riportati devono essere risolti prima dei passi
implementativi pertinenti; non impediscono l'indagine documentale sull'ABI.
Nessuna autorizzazione a compilare, linkare, caricare librerie o trasferire file.

HEAD iniziale locale/GitHub `5d82c54d9a1d0484cfb4d49bf1a51efcfaa2ea20`, branch
`codex/tactical-state-contract-v1`, working tree pulito. Letti TODO e registro
ufficiali del medesimo HEAD, ricognizione backend, report di progettazione,
README/TOKEN_BUDGET/sources-lock/target-contract, evidenze remediation A e
rivalutazione post-R1. Nessuna revisione equivalente completata rilevata nei
report e nello stato versionato. Il progetto è stato esaminato senza modificarlo.

Script: soli comandi Git, lettura JSON/sorgenti, HTTPS pubblico e raccolta
Python inline di hash/risoluzioni/linee di riferimento. Audit esplicitamente
richiesto della provenienza: letture indipendenti dei 25 URL con limite 2 MiB
per file e verifica degli hash dichiarati, senza assumerli corretti. Questo
non è un replay dei test applicativi o della ricognizione VPS. Fonti memorizzate
solo nella cache locale; nessun sorgente di terzi eseguito.

Evidenza nuova: `docs/backend-harness-design-independent-review-evidence-01.json`.
Commit documentale che pubblica insieme report/matrice, evidenza, TODO e registro;
identificabile senza autoriferimento circolare con:

```text
git log -1 --format=%H -- projects/tactical-engine/docs/rag-v5-backend-harness-design-independent-review-01.md
```

Zero test applicativi nuovi o ripetuti, harness, compiler, linker, loading,
SSH/VPS, modelli o inferenze. Nessuna suite 37/13/16/5 eseguita.

## Audit autonomo della provenienza

**25 riferimenti distinti su 25: URL/revisione, dimensione e SHA-256 coerenti**
con i byte ottenuti autonomamente dalle fonti primarie. Nessun errore HTTP o
mismatch. L'evidenza conserva per ogni file URL, hash atteso/osservato e byte.
Le tre risoluzioni API GitHub sono state ripetute per il mandato indipendente:

| Identità pubblica | Risoluzione osservata |
|---|---|
| llama.cpp 620d2225c | 620d2225cc436ab0b001e3200e590e3b286ef9ab |
| Ollama tag v0.40.5 | d919272e53593d1d55d40e1180eaa06dfbede3ac |
| llama.cpp tag b11669 | 620d2225cc436ab0b001e3200e590e3b286ef9ab |

LLAMA_CPP_VERSION al commit Ollama esaminato contiene b11669. Questo rende
coerente il pin pubblico col commit incorporato registrato nella ricognizione,
non prova la corrispondenza integrale sorgente/binario installato.

SHA-256 locali dei manifest del progetto coerenti col report di progettazione:
sources-lock `614d5795a1cd2f7e5ba7138848764b3a98cc51f4bdde60b2c969589fec71ff43`,
target-contract `4ff99ac9c995a8bb8ad4dbc26eed5f58a34b84d89fbdec95ccf4960b40d1ae1f`.
Il target conserva hash libllama-common
`ef57d101f75dbfcad9f309bbc7b08e62d38120657ca146e97ffad2680a2a953d`, uguale
allo snapshot storico, e commit incorporato 620d2225c. È un confronto fra
artefatti versionati, non una verifica aggiornata della VPS.

Le firme pubbliche del converter coincidono per nomi/parametri con quanto
registrato dai simboli, ma non attestano common_json, std::string, contenitori,
allineamento, calling convention, eccezioni o ABI transitiva. Patch compat,
source override, flag LLAMA_USE_LLGUIDANCE e toolchain effettiva restano non
attestati. Il progetto li considera prerequisiti e lascia
source_binary_attestation=null, execution_authorized=false, schema file/hash=null.
Questi valori non sono prove mancanti da sostituire con ipotesi.

[Header pubblico fissato](https://github.com/ggml-org/llama.cpp/blob/620d2225cc436ab0b001e3200e590e3b286ef9ab/common/json-schema-to-grammar.h).
[Pin pubblico Ollama](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/LLAMA_CPP_VERSION).

## Matrice indipendente

Severità e classi dei rilievi non sono stati del progetto. Tutti i giudizi sono
sul disegno documentale; nessun gate o isolamento è stato provato in esecuzione.
P indica `operations/backend-harness/status-correlated-01-design/`.

| Proprietà | Evidenza concreta | Rischio residuo | Severità | Decisione |
|---|---|---|---|---|
| Provenienza | 25/25 fonti e risoluzioni nell'evidenza nuova | SHA di un sorgente pubblico non identifica una build privata | Bassa | Adeguata per l'indagine ABI |
| Firma e tipi C++ | P/README:12–42; header pubblici JSON e converter | Layout/header installati e ABI non provati | Alta, prerequisito dichiarato | Mantenere implementazione BLOCCATO |
| Gate prima del loading | P/README:56–63 e step 1–2; target execution=false | Hash nel main sarebbe tardivo; nessun gate reale implementato | Media — H1 | Necessario ma non sufficiente; precisazioni prima di build/loading |
| Linking e closure | P/README:124–133; target richiede header e dependency closure | Include/object search, compiler driver, plugin/LTO, loader e moduli risolti possono introdurre input non attestati | Media — H1 | Gate anche prima della toolchain/link, non solo prima del worker |
| Isolamento | P/README:56–63; invarianti network=false, Ollama_service=false | Declarazione non è enforcement OS; ambiente e FD ereditati non verificati | Media, prerequisito dichiarato | Definire ambiente minimo/isolamento prima di qualsiasi worker |
| Eccezioni e fallimenti | P/README:90–111, finalizer; converter pubblico check_errors | Eccezioni C++ non coprono segnali, OOM, crash, deadlock o loader failure | Media — H2 | Supervisore deve finalizzare anche senza output JSON del worker |
| CPU, memoria e durata | P/README:62 prevede CPU/RSS/output; target richiede resource limits | Nessun valore approvato; wall-clock e gestione processi figli non espliciti | Media — H2 | Obbligatori prima di esecuzione, senza ereditare i timeout Qwen |
| Hash e diagnostica | P/README:102–122; target future_diagnostics_required | Inventario teorico e stderr incompleto non dimostrano coverage | Media — H3 | Conservare evidenze parziali e distinguere esiti/coverage |
| Assenza GGUF e sampling | Worker converter escluso da GGUF; invarianti e progetto senza eseguibili | Non dimostrato dinamicamente; futuro worker va vincolato e revisionato | Bassa per il disegno attuale | Separazione corretta, nessuna autorizzazione esecutiva |
| Missing/mismatch | P/target-contract gate_policy e nove attestazioni pendenti | Gate non implementato; non basta cambiare un booleano nel JSON | Bassa per l'attività ABI | Default-deny documentale adeguato |
| Conversione diretta/dialetto | P/README:90–102; converter pubblico ramo LLAMA_USE_LLGUIDANCE | Default false può non produrre GBNF; flag installato sconosciuto | Alta, dichiarata | Nessuna forzatura o fallback; blocco sul dialetto non attestato |
| format/ThinkingClose | Ollama pubblico llm/llama_server.go:1472,1701–1727; P/TOKEN_BUDGET | Direct converter non copre wrapper grammaticale, routing o servizio | Alta, dichiarata | Fuori dalla prova diretta; attività separata necessaria |
| Parser e enforcement | P/README:96–122; parser interno pubblico | Parse sintattico non equivale a correttezza del linguaggio/schema | Media | Tenere distinti converter, parser e vincoli |
| Ledger di vincoli composti | Converter pubblico:933–948; schema Python entity_id:95–99 | Pattern può mascherare maxLength senza errore | Media — H3 | Estendere l'analisi per combinazioni; nessuna modifica dello schema |
| Tokenizer/renderer | P/TOKEN_BUDGET:9–58 e sorgenti pubblici | Loader vocab-only, renderer effettivo, special token e patch non provati | Alta, dichiarata | Metodo candidato valido; conteggio ancora BLOCCATO |
| Contesto/output | P/TOKEN_BUDGET:61–82 | Politica attiva, ContextShift e output intero non attestati | Media, dichiarata | Non stimare token e non assumere 4096-2048 come politica |

## H1 — gate d'identità necessario, non ancora sufficiente

La distinzione fra gate esterno e worker evita correttamente il controllo solo
nel main, quando DT_NEEDED, init e loader possono avere già agito. Non dimostra
però che la futura build usi i medesimi header/oggetti/dipendenze verificati.
Prima di compilazione o linking servono toolchain/sysroot, include e library
search path, eventuali plugin, opzioni ABI e provenienza degli object attestati;
prima del loading occorre verificare la closure effettiva e l'immutabilità dei
file verificati. I moduli caricabili a runtime non sono tutti necessariamente
elencati in DT_NEEDED. Vanno esclusi input di ambiente/FD non controllati e race
fra verifica e uso. Il progetto già richiede assenza di TOCTOU, ma non ne fornisce
ancora un meccanismo implementato.

Questo è un requisito prima di realizzare il gate, non un motivo per impedire
l'acquisizione delle prove ABI. Né nomi simboli né una build upstream sostitutiva
sono una soluzione all'attestazione mancante.

## H2 — limiti di durata e fallimenti del processo

CPU/RSS/output sono previsti, ma nessun limite numerico è approvato e non è
esplicito un deadline wall-clock indipendente dalla CPU. Una chiamata bloccata
può non consumare CPU: serve un controllo di durata del supervisore, con
terminazione dell'intero gruppo di processi, gestione del cleanup e inventario
parziale. Segnale, OOM, timeout, errore del loader ed eccezione di conversione
non devono diventare indistintamente «schema incompatibile».

Tali limiti, enforcement e reason code vanno stabiliti prima di qualsiasi
esecuzione. Non vengono proposti valori o importati i timeout del runtime.
L'assenza è accettabile per una base di indagine ABI che oggi non esegue nulla,
non per un'autorizzazione a implementare/eseguire.

## H3 — coverage: perdita silenziosa, errore e semantica esterna

Rilievo statico nuovo, non fixture eseguita: nel converter pubblico fissato,
`common_chat_schema_converter::visit`, case KIND_STRING a riga 933,
il ramo pattern a 935–936 restituisce prima di quello min/maxLength a 945–948.
Il builder conserva entrambi, ma il ramo GBNF del converter non li congiunge.
Lo schema attuale della remediation A usa per entity_id concreto pattern
`^entity:.+$`, minLength 8 e maxLength 71.

Controesempio ragionato: `entity:` seguito da 65 lettere minuscole a è lungo
72 caratteri e soddisfa il pattern, ma viola maxLength. Nel ramo pattern
pubblico riuscito il limite 71 non viene aggiunto. Non è un errore di
conversione e non si può dedurre un warning dal solo ritorno anticipato.
L'effetto sulla libreria VPS non è verificato: il sorgente è pubblico e la
modalità effettiva GBNF/llguidance non è attestata. Il controllo deterministico
`_valid_entity_id` Python conserva il limite 71; non va cambiato lo schema.

Posizioni interessate: `#/$defs/relation/properties/{subject,reference}/anyOf/{0,1}/properties/entity_id/maxLength`.
Le parentesi indicano le quattro posizioni concrete, non un JSON Pointer
letterale da inviare al backend. minLength=8 è già implicato dal pattern in
questo caso; maxLength non lo è. Non è affermato che ogni uso di pattern sia
incompatibile o che una compilazione sia stata eseguita.

[Converter pubblico, revisione esatta](https://github.com/ggml-org/llama.cpp/blob/620d2225cc436ab0b001e3200e590e3b286ef9ab/common/json-schema-to-grammar.cpp#L933).

Il ledger deve distinguere categorie tecniche separate:

- errore di conversione/parsing: nessun linguaggio validamente prodotto;
- perdita di enforcement di un vincolo presente nello schema, es. uniqueItems
  e la congiunzione pattern/maxLength nel ramo pubblico esaminato;
- vincolo presente ma ancora non verificato, senza promozione a supportato;
- controllo deliberatamente esterno allo schema, es. comparison fra lati,
  grounding, precedenze e label nel Python;
- annotation, che non è una restrizione da dichiarare persa.

P/target-contract prevede unsupported_keywords_by_json_pointer e
unverified_constraints; P/README descrive vincoli residui e distingue annotation.
È una buona base, ma prima dell'implementazione le categorie e le combinazioni
di keyword devono essere esplicite nei risultati. Un elenco di keyword
singolarmente riconosciuti non prova che le loro congiunzioni siano applicate.

## Copertura dello schema: cosa si potrà dimostrare

| Famiglia | Lettura statica indipendente | Limite della futura prova diretta |
|---|---|---|
| anyOf annidati | Builder pubblico costruisce alternative; progetto evita properties fratello di anyOf | Occorre comunque schema completo e percorso effettivo; nome keyword non prova composizione corretta |
| $defs/$ref | Resolver pubblico limita i ref al documento; gate vieta fetch esterno | Conversione riuscita non dimostra ogni linguaggio riferito; file/export ancora null |
| const/enum | Rami dedicati nel builder pubblico | Nessun enforcement reale testato; non sostituisce la semantica fra relazioni |
| pattern e lunghezza | Rami distinti, con precedenza pattern nel converter | H3: congiunzione non garantita anche quando ogni keyword è riconosciuto |
| Array/cardinalità | Builder pubblico conserva min/maxItems, converter usa ripetizioni | Nessuna compilazione o accettazione/rejection di esempi eseguita |
| uniqueItems | Non rappresentato dal builder array pubblico, limite già dichiarato | Deve emergere come perdita di enforcement, non semplice controllo esterno |
| required/additionalProperties | Builder pubblico costruisce proprietà obbligatorie e policy extra | Non basta parse=true per affermare equivalenza completa |
| Vincoli Python residui | Contratto finale invariato e separato dal converter | Non sono proprietà dimostrate da grammatica o tokenizer |

## format, parsing e token: confini confermati

La conversione diretta potrebbe dimostrare soltanto che un input fissato produce
un artefatto con una data libreria/ABI; il parser potrebbe dimostrarne la
validità sintattica nel dialetto attestato. Nessuno dei due proverebbe da solo
il percorso Ollama format, la gestione ThinkingClose, il decoder enforcement,
il prompt effettivo, la qualità del modello o l'accuratezza delle contraddizioni.
Il sorgente Ollama pubblico può trasformare json_schema in grammatica avvolta;
il suo schemaGrammar usa POST /completion su un runner. Il progetto lo esclude
correttamente: nessuna scorciatoia n_predict=0 è autorizzata.

TOKEN_BUDGET distingue hash vocabolario/merges dal semplice nome GPT-2, renderer
qwen3.5 da template GGUF/layer Go, think=false, flag add_special/parse_special e
due punti del conteggio nel percorso pubblico. Vocabulary-only è una via
candidata, non una prova zero-pesi: loader, compat patch e inizializzazione
richiedono ancora evidenze. Il progetto non implementa un tokenizer alternativo.

Rendering, sequenza token, politica di troncamento, input prima/dopo il taglio,
num_ctx=4096 e num_predict=2048 sono grandezze distinte. La prova non generativa
futura può misurarle soltanto dopo il collegamento affidabile al codice effettivo
e al vocabolario; non garantisce 2048 token di output perché il conteggio
input sia inferiore a 4096. Nessuna conversione byte/token o conteggio prodotto.
Le dimensioni storiche 6.967/7.311/16.869 byte restano evidenze documentali.

## Risultato → Decisione → Stato

**Unica conclusione A:** la base documentale è affidabile per affrontare
separatamente il prerequisito ABI, perché provenienza e limiti sono tracciati,
le assunzioni non provate bloccano già il progetto eseguibile e conversione,
parsing, enforcement e token sono distinti. H1–H3 sono precisazioni obbligatorie
prima dei successivi passi implementativi, non autorizzazioni né correzioni
applicate in questa revisione.

Revisione **ESEGUITO** e **VALIDATO** come analisi indipendente documentale.
Progetto resta **IMPLEMENTATO** documentale; implementazione, compatibilità
backend, accuratezza generativa, Gate, integrazione e certificazione **BLOCCATO**.
Attestazione ABI e precisazioni progettuali **DA FARE** in attività separate.
Report, matrice, evidenza statica, TODO e registro pubblicati nello stesso ciclo.
Nessun progetto/report precedente modificato, test ripetuto, eseguibile creato,
compilazione, linking, loading, VPS, modello, runtime-05, staging/wrapper,
merge o deploy. STOP dopo pubblicazione.
