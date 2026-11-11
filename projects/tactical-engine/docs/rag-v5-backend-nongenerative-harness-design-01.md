# RAG V5 — progettazione locale harness backend non generativo

Attività: `RD-RAG-V5-BACKEND-NONGENERATIVE-HARNESS-DESIGN-01`.
Data: 2026-11-11, Europe/Rome.

## Attività → Script → Commit → Report

Prodotto un progetto minimo documentale separato dal runtime. Interfacce
pubbliche individuate a revisione esatta; collegamento sorgenti/ABI/binario
installato ancora non dimostrato. **Implementazione eseguibile BLOCCATO**:
applicato il fallback documentale del mandato, senza dichiarazioni ABI inventate.
Nessun file C++, script di esecuzione o CMake operativo preparato.

Riconciliazione preliminare: TODO ed Experiment Register del branch ufficiale,
report e tutte le cinque evidenze della ricognizione backend letti localmente;
HEAD locale/remoto iniziale `9367aacfc83e2bb384f313e42b19c93af0462538`, branch
`codex/tactical-state-contract-v1`, working tree pulito. Confrontati i commit
`0ea62c0`, `5bfa489`, `ca6bf67`, `9367aac`: remediation A, correzione R1,
rivalutazione incrementale e ricognizione sono coerenti. Nessun harness
equivalente completato trovato nei percorsi/report versionati esaminati.

Script: sola lettura Git/JSON; HTTPS verso GitHub e raw.githubusercontent.com
per sorgenti/header pubblici, cache esclusivamente locale; SHA-256 dei file
locali e parsing JSON dei nuovi manifest. Non eseguiti moduli applicativi,
test, compiler, linker, convertitore, parser grammaticale o harness.
Zero SSH/VPS e nessuna ricognizione ripetuta. Nessun download sulla VPS.

Commit documentale che pubblica contestualmente progetto, evidenze, report,
TODO e registro; identificabile dalla storia del report:

```text
git log -1 --format=%H -- projects/tactical-engine/docs/rag-v5-backend-nongenerative-harness-design-01.md
```

## Provenienza esatta e firma

Progetto: `operations/backend-harness/status-correlated-01-design/`.

| Artefatto | Contenuto |
|---|---|
| README.md | Architettura, gate fail-closed, ABI, parsing e diagnostica |
| TOKEN_BUDGET.md | Metodo separato per rendering/tokenizer/contesto senza pesi |
| sources-lock.json | 25 sorgenti esaminati, repository, revisione completa, URL immutabile, byte e SHA-256 |
| target-contract.json | Identità bersaglio, evidenze mancanti, esecuzione false; nessun eseguibile e nessun hash schema inventato |

Impronte locali dei manifest del progetto:
`sources-lock.json` SHA-256
`614d5795a1cd2f7e5ba7138848764b3a98cc51f4bdde60b2c969589fec71ff43`;
`target-contract.json` SHA-256
`4ff99ac9c995a8bb8ad4dbc26eed5f58a34b84d89fbdec95ccf4960b40d1ae1f`.
Entrambi letti come JSON; nessuna esecuzione del progetto.

Catena pubblica risolta tramite API GitHub:

- llama.cpp `620d2225c` → `620d2225cc436ab0b001e3200e590e3b286ef9ab`;
- Ollama `v0.40.5` → `d919272e53593d1d55d40e1180eaa06dfbede3ac`;
- LLAMA_CPP_VERSION di quell'Ollama → b11669 → lo stesso commit llama.

[Pin Ollama](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/LLAMA_CPP_VERSION).
[Header converter](https://github.com/ggml-org/llama.cpp/blob/620d2225cc436ab0b001e3200e590e3b286ef9ab/common/json-schema-to-grammar.h).

La firma pubblica completa dei due overload è riportata una sola volta nel
README del progetto. I parametri sono common_json const-reference con bool
default false, oppure common_chat_schema_document const-reference; ritorno
std::string. I nomi sono coerenti coi simboli della ricognizione, ma il
mangling non dimostra identità dei layout C++, default del chiamante o tutti
i dettagli ABI/ritorno. Nessuna chiamata al binario installato è stata fatta.

common_json usa un wrapper con storage inline nel sorgente, non un alias
sostituibile con nlohmann::json. Il documento schema usa contenitori C++ e
ownership. Gli header parser sono interni e non costituiscono API C stabile.
Quindi **firma pubblica verificata, interfaccia affidabile per il binario
bersaglio non ancora dimostrata**: niente implementazione linkabile oggi.

Target preservato, riusando le evidenze senza nuove verifiche remote:
Ollama 0.40.5; commit incorporato llama 620d2225c;
`libllama-common.so.0.7.0`, SHA-256
`ef57d101f75dbfcad9f309bbc7b08e62d38120657ca146e97ffad2680a2a953d`;
modello storico qwen3.5:9b, digest
`56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`.
Il modello è solo contesto di provenienza, non un input del worker grammatica.

## Risultati nuovi dell'analisi statica

| Fonte pubblica alla revisione fissata | Osservazione | Conseguenza progettuale, non prova sul binario |
|---|---|---|
| common/json.h, json-schema.h e relativi .cpp | API JSON propria e strutture schema con layout C++ | Header e ABI esatti necessari; niente sostituzione di tipi |
| common/CMakeLists.txt | C++17, dipendenze vendor e Threads; flag opzionali | Distinguere consumo della libreria attestata da una nuova ricompilazione upstream |
| json-schema-to-grammar.cpp | Possibile ramo LLAMA_USE_LLGUIDANCE con default false; warning non esaustivi | Non forzare GBNF; identificare dialetto e arrestarsi se non approvato |
| json-schema.cpp / grammars/README.md | uniqueItems non rappresentato dal builder array esaminato e limite documentato | Ledger obbligatorio dei vincoli non rappresentati, anche con stderr vuoto |
| src/llama-grammar.h/.cpp | Parser GBNF con vocab opzionale; terminali token richiedono vocab | Parsing character-based senza modello solo dopo prova del relativo ABI |
| Ollama llama/server/CMakeLists.txt e compat | Pin preciso ma patch e source override ammessi | Catena tag/commit non è attestazione della build installata |
| Ollama llm/llama_server.go | format oggetto passa come json_schema; ramo ThinkingClose può convertirlo e incapsularlo | Tracciare il percorso effettivo, senza supporre equivalenza al solo converter |
| Stesso file, schemaGrammar | Usa POST /completion su un runner, anche se il sorgente descrive il caso senza token prodotti | Non usarlo come ingresso del progetto senza runner/modello |
| Ollama server/prompt.go | Renderer configurato precede template; conteggio/troncamento richiede tokenizzazione | Renderer qwen3.5 va attestato, non sostituito col solo template GGUF |

[Percorso pubblico Ollama](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/llm/llama_server.go).
Tutte queste sono proprietà del sorgente pubblico. La loro applicazione al
binario VPS rimane condizionata alla prova di build, flag e patch effettive.
Non riscritte o invalidate le evidenze precedenti.

## Architettura e budget previsti

Il README definisce gate separato prima del caricamento dinamico, worker
converter tipato senza GGUF, parser del dialetto attestato, ledger keyword e
finalizzazione di hash/diagnostica. Missing/mismatch/null devono bloccare prima
dell'avvio del worker. Nessun repair dello schema, overload alternativo,
ricompilazione sostitutiva o cambio flag per ottenere un esito favorevole.
Il file schema completo richiede export e hash approvati: la sola dimensione
16.869 non è identità; lo schema storico runtime-04 è precedente alla remediation.

La diagnostica distingue conversione, parse grammaticale e copertura dei
vincoli; registra eccezioni, stderr, keyword/JSON Pointer non rappresentati,
librerie effettive e hash artefatti. promotion_authorized rimane false.
Un parse riuscito non proverebbe equivalenza semantica o accuratezza generativa.

TOKEN_BUDGET.md separa vocabolario GGUF, renderer selezionato, system/user,
think=false, format, BOS/special token e politica di contesto. La via candidata
è API ufficiale vocabulary-only, previa prova del loader e delle patch che
nessun peso sia letto/mappato; nessun tokenizer alternativo implementato.
Il sorgente pubblico distingue addSpecial=false nel primo conteggio e true in
un ramo successivo di troncamento. Non si sostituisce questa politica con una
regola inventata 4096-2048. num_ctx=4096 e num_predict=2048 restano richieste
congelate; 6.967/7.311/16.869 sono byte documentali, non token misurati.

## Evidenze ancora mancanti

1. Attestazione sorgenti/patch/flag → hash della libreria installata.
2. Closure header e librerie transitive, ABI compiler/libstdc++, opzioni
   eccezioni/RTTI, modalità LLAMA_USE_LLGUIDANCE.
3. Interfaccia e simboli/layout parser compatibili, senza fallback inventati.
4. File schema completo esportato con provenienza e SHA-256 approvato.
5. Prova del percorso format/ThinkingClose/renderer e special-token effettivo.
6. Prova del vocabulary-only senza lettura/mapping pesi prima di implementare
   il conteggio; politica attiva di troncamento/contesto.
7. Implementazione futura dei gate, limiti di risorse e revisione indipendente,
   seguite dalle rispettive autorizzazioni di compilazione/esecuzione.

## Verifiche locali → Decisione → Stato

Venticinque hash di sorgenti scaricati localmente ricalcolati e coerenti col
manifest; nuovi JSON letti come dati. Nessun controllo sintattico C++ necessario:
non è prodotto codice eseguibile e non esiste una closure header attestata.
Nessuna suite 37/13/16/5, test applicativo, compilazione, link o esecuzione.
Il diff finale contiene solo il progetto documentale, questo report e gli
aggiornamenti contestuali TODO/Experiment Register.

**Idoneo a una successiva revisione indipendente come progetto documentale.**
Non è idoneità all'esecuzione e non risolve per supposizione la prova ABI:
il prerequisito è precisato, ma non può essere dichiarato interamente risolto.
Progetto **IMPLEMENTATO** documentale, analisi **ESEGUITO** e proprietà statiche
verificabili **VALIDATO** nel loro perimetro. Implementazione eseguibile,
compatibilità backend, accuratezza generativa, Gate, integrazione e
certificazione **BLOCCATO**. Nessuna modifica ai file applicativi remediation A,
VPS, trasferimento, runtime-05, staging, wrapper, Qwen, merge o deploy. STOP.
