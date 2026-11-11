# status-correlated-01 — progetto harness non generativo

Attività `RD-RAG-V5-BACKEND-NONGENERATIVE-HARNESS-DESIGN-01`, 2026-11-11.
Progetto **IMPLEMENTATO** come documentazione; implementazione eseguibile
**BLOCCATO**. Nessun C++, launcher o CMake eseguibile è fornito.
Questo progetto è separato dal runtime applicativo e non autorizza esecuzione.

## Interfacce verificate e confine della prova

Sorgente pubblico llama.cpp:
`620d2225cc436ab0b001e3200e590e3b286ef9ab`.
In `common/json-schema-to-grammar.h` sono dichiarate:

```cpp
std::string json_schema_to_grammar(const common_json & schema, bool force_gbnf = false);
std::string json_schema_to_grammar(const common_chat_schema_document & schema);
```

[Header originale a revisione esatta](https://github.com/ggml-org/llama.cpp/blob/620d2225cc436ab0b001e3200e590e3b286ef9ab/common/json-schema-to-grammar.h).
Le fonti e gli hash locali dei byte esaminati sono in `sources-lock.json`.
`common_json` NON è un alias intercambiabile con nlohmann::json: ha API propria
con parse, costruttori/distruttore e storage inline alignas(8) di 32 byte nel
sorgente pubblico. Questa dimensione non è provata per la libreria installata.
`common_chat_schema_document` contiene unique_ptr e map; nessun layout è da
ricostruire a mano. Entrambi richiedono i loro header originali.

Il simbolo installato registrato per il primo overload ha il parametro bool e
il tag ABI cxx11; quello del secondo nomina common_chat_schema_document.
La corrispondenza dei nomi non dimostra layout, ritorno completo, flag di build
o identità sorgente/binario. Il valore default del bool è una proprietà
compilata nel chiamante, non una prova contenuta nel nome del simbolo.

Ollama pubblico v0.40.5 risolve a
`d919272e53593d1d55d40e1180eaa06dfbede3ac`;
`LLAMA_CPP_VERSION` fissa b11669, tag che risolve al commit llama sopra.
Tuttavia `llama/server/CMakeLists.txt` ammette override OLLAMA_LLAMA_CPP_SOURCE
e patch compat; il commit incorporato non certifica la build VPS.
La patch pubblica esaminata tocca loader modello e clip, non basta a escludere
altre modifiche locali o flag differenti sul convertitore.

**Firma pubblica verificata; firma/ABI utilizzabile con affidabilità sul binario
bersaglio non dimostrata.** Applicato il fallback del mandato: solo progetto
documentale. Né ctypes, cast ABI, header sintetici, dlsym con firme inventate,
né una ricompilazione upstream sostitutiva possono colmare la prova mancante.

## Componenti previsti, non implementati

| Componente | Responsabilità | Limite |
|---|---|---|
| Preflight supervisor | Verificare autorizzazione separata, input, manifest firmato/revisionato e librerie come file; inventario e hash | Non carica librerie, non avvia servizi o runtime |
| Converter worker | Parsing common_json e chiamata tipata al primo overload, solo dopo i gate | Nessun GGUF, modello, tokenizer, contesto o sampler |
| Grammar parser | Parsing sintattico della grammatica prodotta con interfaccia ufficiale attestata | Nessun vocabolario per il solo GBNF character-based |
| Constraint ledger | Inventario semantico dei keyword per JSON Pointer, avvisi e vincoli residui | Non riscrive schema o grammatica e non presume enforcement |
| Evidence finalizer | Diagnostica strutturata, hash/inventario anche in caso di errore | Nessuna promozione di risultati o diagnosi generativa |

È progettato un processo di gate separato perché il loader dinamico può caricare
le dipendenze prima del main di un worker già linkato. Il gate deve completarsi
prima del suo avvio; non basta un controllo hash nel main.
Un ambiente di esecuzione futuro deve essere isolato dalla rete e dai servizi,
con directory librerie immutable/revisionate, LD_PRELOAD/LD_LIBRARY_PATH non
incontrollati e assenza di TOCTOU fra hash e loading. Si devono fissare prima
dell'esecuzione limiti revisionati di CPU/RSS e output, senza importare i timeout
del runtime Qwen. Nessun ambiente del genere è creato in questa attività.

## Ordine fail-closed previsto

1. Richiedere autorizzazione distinta all'esecuzione. `target-contract.json`
   oggi impone execution_authorized=false; null/missing non significa approvato.
2. Verificare hash atteso di libllama-common.so.0.7.0, build ID, architettura,
   dipendenze transitive e prova sorgenti/patch/flag associata a quei byte.
   Occorrono C++17, ABI libstdc++ coerente, eccezioni/RTTI, flag del parser e
   LLAMA_USE_LLGUIDANCE. Il tag cxx11 suggerisce solo una parte del vincolo.
3. Verificare un file schema completo approvato: SHA-256, byte UTF-8,
   provenienza dal sorgente remediation A, $id e contract_id/version.
   La revisione status-correlated-01 è metadato di trasporto esterno, NON un
   campo root da inserire automaticamente nello schema. Il dominio resta 1.0.0.
4. Vietare file troncati, duplicate key ambigue, ref esterni o input divergenti.
   Nessuna normalizzazione o export automatico da moduli applicativi nel worker.
   La dimensione storica 16.869 byte non sostituisce l'hash approvato. In questa
   attività non è prodotto un export schema: file/hash approvati restano null.
   Il vecchio request_payload runtime-04 contiene lo schema PRE-remediation e
   non può essere usato come surrogato del nuovo contratto.
5. Costruire l'inventario dei keyword in posizioni schema effettive: properties,
   items, anyOf, $defs, ecc.; non classificare i nomi delle proprietà o gli
   oggetti dentro enum/const come nuovi keyword JSON Schema.
6. Solo con gate soddisfatti, usare common_json::parse e la dichiarazione del
   convertitore dall'header attestato; non sostituire il tipo con nlohmann o
   selezionare un overload diverso per evitare errori.
7. Conservare ritorno del convertitore, stderr ed eccezioni separatamente.
   Nel sorgente pubblico, il bool default false può restituire un documento
   %llguidance se la libreria è compilata LLAMA_USE_LLGUIDANCE. Non passare true
   per ottenere GBNF come ripiego: cambierebbe il ramo rispetto al target.
8. Identificare il dialetto prima del parser. Se %llguidance è fuori dal percorso
   approvato, arresto con diagnostica; non darlo al parser GBNF. Per GBNF puro,
   il parser ufficiale llama_grammar_parser::parse è documentato in
   src/llama-grammar.h/.cpp. È interfaccia interna: richiede prova separata di
   header, simboli e layout; il parser non è certificato dalla firma converter.
   Con vocab=nullptr vanno esclusi terminali che richiedono token di vocabolario.
   Controllare parse=true, regole non vuote e presenza root, senza sampler.
9. Finalizzare hash dello schema originale, librerie realmente risolte, worker,
   header/source lock, grammatica, diagnostica e inventario. Errori parziali
   conservano quanto disponibile; niente secondo tentativo o fallback.

## Diagnostica prevista

Ogni esito deve distinguere stadio preflight, JSON parse, conversione, dialetto,
grammar parse e coverage dei vincoli. `reason_codes` devono distinguere almeno
identità mancante/diversa, ABI non attestata, hash schema mancante, keyword non
rappresentato, converter error, dialect fuori ambito e parser error.
Il risultato deve includere hash e dimensioni, eccezioni e warning osservati,
vincoli non rappresentati e vincoli non verificati per JSON Pointer.
`promotion_authorized` rimane sempre false; compiler_returned e parser_ok sono
evidenze tecniche, non accuratezza generativa o compatibilità completa.

Il converter pubblico stampa alcuni warning, ma non garantisce diagnostica
esaustiva. In particolare l'array builder pubblico non rappresenta uniqueItems;
la documentazione ne dichiara il limite. Il ledger deve segnalarlo anche con
stderr vuoto. Non rimuovere uniqueItems per ottenere una compilazione riuscita:
il controllo deterministico esistente resta necessario. Annotation quali
description/$schema/$id vanno distinte dai vincoli; gli altri keyword non
riconosciuti restano non verificati, non vengono promossi a supportati.
Una conversione e un parse riusciti non provano equivalenza semantica schema/GBNF.

## Dipendenze e linking

Un worker che consuma la libreria attestata usa gli header originali e l'intera
closure delle dipendenze dinamiche con hash/provenienza verificati, senza
ri-compilare il convertitore. Almeno libllama, ggml, libstdc++/ABI e loader
Linux x86_64 vanno riconciliati. Non linkare contro la prima libreria dal PATH.
La ricostruzione upstream completa richiederebbe inoltre vendor nlohmann,
sheredom, cpp-httplib, Threads e opzioni CMake; LLAMA_LLGUIDANCE può introdurre
una dipendenza esterna. Sarebbe un artefatto diverso, non una prova del binario
VPS. Nessun FetchContent, build, link o installazione viene eseguito qui.

## Evidenze mancanti e decisione

Mancano: attestazione del build installato; closure header e dipendenze;
flag/compiler/libstdc++ ABI; modalità llguidance/GBNF; ABI/parser export;
file/hash schema completo approvato; percorso format e rendering effettivo;
implementazione e revisione indipendente dei gate/limiti del futuro worker.
Il metodo token separato è in `TOKEN_BUDGET.md`.

Progetto idoneo a revisione indipendente come progetto documentale.
Implementazione e successiva compilazione/esecuzione **BLOCCATO** finché tali
evidenze non sono risolte. Non è stata dimostrata compatibilità del backend.
