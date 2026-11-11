# RAG V5 — indagine read-only di attestazione build e ABI

Attività: `RD-RAG-V5-BACKEND-BUILD-ABI-ATTESTATION-01`.
Data: 2026-11-11, Europe/Rome.

## Attività → Script → Commit → Report

**Unica decisione: B — attestazione incompleta.** Identità del file, tracce
compiler, versioni simboliche e dipendenze sono meglio documentate; manca
ancora la catena sorgenti/patch/build/header/ABI associata al binario esatto.
Non è attestata la compatibilità dei tipi C++ e non è implementato un harness.

Prima delle letture tecniche riconciliati TODO ed Experiment Register ufficiali,
ricognizione backend, progetto documentale, revisione indipendente c99a456 e
closeout H1–H3 b1ac190. HEAD iniziale locale/GitHub
`b1ac190b94d4947333c118d68004750ff38f971d`, branch
`codex/tactical-state-contract-v1`, working tree pulito. Nessuna attestazione ABI
equivalente completata nei documenti versionati: la revisione precedente
considerava esplicitamente l'ABI DA FARE.

Riusati i pin pubblici, gli hash e i simboli già pubblicati. Nessun audit 25/25,
ricognizione dei modelli o suite 37/13/16/5 ripetuti. Riancorato il solo file
bersaglio per associare le NUOVE sezioni/compiler/ABI agli stessi byte storici;
la giustificazione è registrata prima delle letture e nell'evidenza.

Script: tre connessioni SSH diagnostiche read-only via football-vps, Python
stdlib -B -I via stdin, readelf, objdump, dpkg-query e ldconfig -p. Quest'ultimo
legge la cache: non è ldd, non esegue il loader o il target. Nessun compiler,
linker, loader dinamico, converter, tokenizer o modello invocato. Nessun sudo,
permesso/configurazione modificati, lock, POST o scrittura remota impartita.
Host key rigorosa, BatchMode e UpdateHostKeys=no, identità SSH già autorizzata.

Prima raccolta interrotta dalla decodifica UTF-8 di un output binario readelf,
senza JSON persistito. Ripetuta soltanto la raccolta insufficiente con decoder
che conserva escape, hash dei byte e base64 quando necessario. È un errore del
raccoglitore, non del backend; due raccolte strutturate completate. Non costituisce
un secondo tentativo di runtime o test applicativo.

Commit: documentale con report, matrice H1, quattro evidenze, TODO e registro
pubblicati insieme; identificabile senza autoriferimento circolare con:

```text
git log -1 --format=%H -- projects/tactical-engine/docs/rag-v5-backend-build-abi-attestation-01.md
```

## Provenienza delle evidenze

Tutti i file seguenti sono in `docs/`:

| ID | File | Contenuto |
|---|---|---|
| E1 | backend-build-abi-elf-evidence-01.json | Identità target, sezioni, commenti compiler, version requirements, eccezioni/simboli, disassembly mirato, candidati dossier e ownership |
| E2 | backend-build-abi-dependency-evidence-01.json | Grafo DT_NEEDED candidato, file/hash, note ELF, cache/config, RTTI mirato, versioni runtime e limite debug |
| E3 | backend-build-abi-version-analysis-01.json | Confronto locale dei NOMI di versione richiesti dal target con le definizioni dei candidati, senza linker/loading |
| E4 | backend-build-abi-attestation-summary-01.json | Matrice H1, inventario SHA-256 E1–E3, riferimenti pubblici riusati, limiti e decisione |

Snapshot E1 `2026-11-11T13:43:05Z`, E2 `13:46:13Z` (14:43–14:46 Europe/Rome).
Ogni comando ELF in E1 conserva argv, exit, stdout/stderr e hash dei byte;
l'output non UTF-8 ha anche cattura base64. Ogni nodo E2 conserva hash, percorso
reale, metadati e hash degli output. Nessuna inferenza da output troncati:
la prima selezione simboli ha 553 match e ne conserva 180, indicandolo;
la selezione RTTI specifica successiva conserva tutti i suoi 67 match.

L0 = `/usr/local/lib/ollama/libllama-common.so.0.7.0`, 4.642.576 byte,
SHA-256 `ef57d101f75dbfcad9f309bbc7b08e62d38120657ca146e97ffad2680a2a953d`,
Build ID `a7bb44fb1d8cae659f9e62b00c3b43690ef27614`: identità coerente con lo
storico, senza dimostrare immutabilità fra tutti gli accessi al pathname.
Owner root, modo 0755, device/inode registrati sono snapshot, non custodia H1-G6.

## Matrice sorgenti → build → ABI

E1/E2/E3 identificano le proprietà tramite i relativi campi; il loro hash
integrale è nell'inventario E4. I metadati ELF L0 hanno come fonte i byte con
hash L0 sopra; i runtime hanno hash per nodo in E2, non soltanto nomi di file.

| Proprietà | Evidenza concreta, fonte e hash | Proprietà dimostrata | Informazione mancante | Impatto sulla futura implementazione |
|---|---|---|---|---|
| Origine sorgenti compilati | Pin pubblici riusati in E4; otto candidati di dossier mirati assenti in E1; dpkg-query non trova owner per L0 | Riferimenti pubblici noti e assenza di quei soli dossier nei percorsi ispezionati | Associazione attendibile fra sorgenti effettivi e hash L0 | Non assumere che gli header upstream siano l'SDK del binario |
| Patch/source override | CMake Ollama pubblico già fissato a d919272e53593d1d55d40e1180eaa06dfbede3ac ammette override/compat; riferimenti/hash riusati in E4 | Possibilità nel candidato pubblico, non uso effettivo | Patch set e override della build L0 | Nessuna equivalenza integrale da commit incorporato |
| Configurazione CMake/build | E1 sections: niente .GCC.command.line; CMakeCache/compile_commands/build.ninja e altri candidati assenti | Questi metadati non sono disponibili nelle posizioni mirate | Cache, build logs, opzioni per TU e configurazione effettiva | Macro/default non vanno inventati |
| Compiler/linker usati | E1 compiler_comment, fonte L0: GCC GNU 13.3.1 20240611 Red Hat 13.3.1-2 | Traccia di toolchain nei componenti ELF | Tutta la toolchain, linker/versione, sysroot, comandi e mapping oggetti | Commento GCC non equivale a dossier compiler/linker completo |
| libstdc++ runtime | E2: `/usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33`, SHA-256 1fd75fe70354a416d75aef22bcae68c47bd25d20e2d0568c30b1a9838cf62f11; pacchetto 14.2.0-4ubuntu2~24.04.1 | Candidato installato e versioni esportate osservati | Risoluzione effettiva del loader e ABI del futuro worker | Non confondere runtime Ubuntu con compiler Red Hat della build |
| ABI C++ / macro CXX11 | Tag B5cxx11 e riferimenti std::__cxx11 in E1 L0 | Superficie di interfacce con ABI string cxx11 | Valore globale/per-TU di _GLIBCXX_USE_CXX11_ABI, opzioni debug/packing e tutti i layout | Il tag non attesta common_json o l'intero progetto |
| Eccezioni/RTTI | L0 .eh_frame, .gcc_except_table, __cxa_throw, __gxx_personality_v0, _Unwind_Resume; 67 simboli specifici RTTI/vtable in E2 | Presenza di infrastruttura EH e RTTI per tipi osservati | Flag uniformi, layout e confine eccezioni della futura build | Non dedurre -fexceptions/-frtti per tutte le unità o compatibilità globale |
| LLAMA_USE_LLGUIDANCE | E1 disassembly overload bool: builder from_json seguito dall'overload document; E2 nessun simbolo nominale llguidance | Percorso normale osservato compatibile col ramo GBNF pubblico, senza selezione iniziale sul bool | Flag CMake/macro attestato e identità sorgente/binario; assenza nomi non prova assenza di ogni implementazione | Non forzare un flag per aggirare il dubbio; non dichiarare attestata la macro globale |
| Closure ELF | E2: dieci dipendenze candidate con hash oltre a L0, nessuna dipendenza DT_NEEDED senza candidato nella ricerca | Grafo statico candidato diretto, ricorsivamente identificato entro i limiti | Loader effettivo, hwcaps/preload, moduli dlopen/plugin e futuro worker | Closure completa di codice caricabile non dimostrata |
| Tipi common_json/document | Nomi/metodi/vtable in E1/E2; niente .debug_info e file debug da Build ID assente nel candidato derivato | Simboli e assenza di quelle fonti di layout, non dimensioni dei tipi | Dati tipi/debug o SDK/header/build attestati per L0, size/align/ownership/calling convention | Nessuna prova utilizzabile per dichiarazioni ABI o cast manuali |

## Interpretazione delle nuove tracce

La sezione .comment riporta GCC Red Hat 13.3.1-2, ma il compiler effettivo di
ogni oggetto e il linker non sono identificati da quel commento. La presenza
del pacchetto binutils 2.42 sulla VPS non prova che sia stato usato per creare
L0. La nota .gnu.build.attributes contiene soltanto la nota OPEN/versione
osservata, non un set completo di flag o una build attestation.

Le versioni richieste da L0 includono GLIBCXX_3.4.22 e CXXABI_1.3.11. Il
confronto E3 trova nei candidati tutti i nomi richiesti dai sei provider di
versione di L0. È disponibilità NOMINALE di namespace/versioni, non verifica
di ogni binding simbolico o dell'ABI dei tipi. GCC Red Hat nella build e
libstdc++ Ubuntu nel runtime non costituiscono da soli una divergenza accertata.

Nel disassembly mirato l'overload common_json/bool chiama
common_chat_schema_from_json e poi l'overload common_chat_schema_document.
Il parametro bool non governa una selezione iniziale visibile prima del builder;
non è una chiamata eseguita e non ricostruisce tutti i flag della build.
L'assenza di simboli llguidance nominali è corroborante, non una prova globale
negativa. I tipi non polimorfici non richiedono necessariamente RTTI: non si
deduce layout dall'assenza di un nome o dalla sola presenza di una vtable.

Sono stati cercati otto nomi precisi di dossier nella directory nota e un solo
file debug derivato dal Build ID. La loro assenza non è una scansione globale
o una dichiarazione che documenti non esistano altrove. Nessun log personale,
cronologia shell, directory modello o peso GGUF è stato letto. Il source pin
pubblico 620d2225cc436ab0b001e3200e590e3b286ef9ab resta distinto da L0.

## Closure: metodo e limite

E2 segue soltanto gli archi DT_NEEDED, con massimo 24 file e limite 64 MiB per
file; dieci candidati distinti osservati, nessun limite raggiunto. Il target
principale era già vincolato dall'evidenza E1: non rifatto un inventario Ollama.
RUNPATH=$ORIGIN e cache x86-64 determinano candidati statici, non una promessa
sulla scelta del loader. Registrati i soli dati della cache/configurazioni
pertinenti; l'output globale ldconfig -p è hashato, ma conservati solo i candidati
consultati per dipendenza. Configurazioni ld.so sono lette, non aggiornate.

Il percorso `/etc/ld.so.preload` non risulta presente nello snapshot, ma l'ambiente LD_*
registrato è quello del processo diagnostico SSH, NON quello del servizio o
del futuro worker. Il limite di accesso al procfs del servizio era già noto
dalla ricognizione: non è stato aggirato né ritentato con privilegi. Non sono
provati header/search path/plugin della build, FD o isolamento del futuro gate.

## Matrice H1 — sola futura soddisfacibilità

Gli esiti descrittivi seguenti NON sono stati del progetto e NON indicano gate
eseguiti. Nessun gate ha evidenza sufficiente completa; nessuna divergenza
integrale di identità è stata accertata.

| Gate | Esito descrittivo | Evidenza disponibile | Residuo prima della futura implementazione |
|---|---|---|---|
| H1-G1 — toolchain | Evidenza parziale | ELF x86-64, commento GCC, runtime e reader installati | Compiler/linker/assembler/sysroot e mapping build esatti |
| H1-G2 — origine input | Evidenza mancante | Pin pubblico e assenza dei dossier mirati, ownership dpkg non trovata | Provenienza effettiva sorgenti/patch/header/object associata all'hash L0 |
| H1-G3 — flag ABI | Evidenza parziale | Interfacce cxx11, EH/RTTI e percorso overload | Flag/macro, dialetto e layout attestati |
| H1-G4 — search/ambiente | Evidenza parziale | RUNPATH, cache/config e ambiente della sola diagnostica | Search path, plugin, response file, ambiente/FD della build e del worker |
| H1-G5 — closure | Evidenza parziale | Grafo diretto con dieci candidati e namespace richiesti disponibili | Risoluzione effettiva, moduli dinamici e closure del futuro worker |
| H1-G6 — custodia | Evidenza parziale | Hash, UID/mode e device/inode fotografati | Antenati/strategie di immutabilità e vincolo dei byte fino all'uso |

## Prerequisiti specifici → Decisione → Stato

Occorrono in un'attività distinta: dossier attendibile del produttore o altra
prova revisionata che associ L0 a sorgenti/patch/build commands/flag/toolchain;
header/SDK o dati debug di tipi vincolati allo stesso artefatto/Build ID;
closure ABI e ricerca/librerie del futuro worker; scelta documentata del
meccanismo di custodia/isolamento. I file eventualmente forniti devono avere
origine e hash verificabili: un checkout dello stesso commit non basta.
Nessuna richiesta implicita di rifare la build o di provare sizeof tramite
compilazione; nessuna operazione del genere è autorizzata o eseguita qui.

**Decisione B — attestazione incompleta:** i prerequisiti sono specifici e
la raccolta identifica un percorso di approfondimento; non si conclude C per
assenza di qualunque bersaglio affidabile. Non si conclude A perché la sola
coerenza di file/commit/versioni non dimostra le interfacce C++ richieste.

Indagine **ESEGUITO**. Attestazione ABI **BLOCCATO**, prerequisiti **DA FARE**;
ABI non VALIDATO. Implementazione harness, compatibilità backend, accuratezza
generativa, Gate, integrazione e certificazione **BLOCCATO**. Nessuna modifica
al progetto documentale, ai manifest approvati, al codice o ai servizi.
Report, matrice, evidenze, TODO e Experiment Register pubblicati nello stesso
ciclo. STOP dopo pubblicazione e verifica GitHub, senza implementazione,
compilazione, linking/loading, VPS ulteriore, modelli, runtime/staging/wrapper,
merge o deploy.
