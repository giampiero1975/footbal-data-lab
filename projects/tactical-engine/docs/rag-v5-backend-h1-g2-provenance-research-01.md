# H1-G2 — Ricerca documentale della provenienza della build

Data: 2026-11-11. Attività: `RD-RAG-V5-BACKEND-H1-G2-PROVENANCE-RESEARCH-01`.

## Risultato e decisione

**Decisione B — Provenienza ancora incompleta, con richiesta puntuale di documenti o attestazioni specifiche.**

Le fonti ufficiali collegano il commit Ollama al run della release e descrivono
la configurazione prevista. Il publisher identifica inoltre un archivio Linux
amd64 mediante digest. Non è stata ottenuta una prova che colleghi quel digest
al singolo `libllama-common.so.0.7.0` installato sulla VPS, né un dossier degli
input effettivi e degli header/layout C++ della sua build. H1-G2 è delimitato,
**BLOCCATO**; non è risolto. Nessuna ricostruzione presumibilmente equivalente.

Ricerca **ESEGUITO**. Attestazione ABI, implementazione harness, compatibilità
backend, accuratezza generativa, Gate, integrazione e certificazione
**BLOCCATO**; acquisizione delle prove mancanti **DA FARE**.

## Riconciliazione e tracciabilità

Branch locale e remoto: `codex/tactical-state-contract-v1`; HEAD iniziale
locale/GitHub `809be0bba0a447fa6dbb12df4ad982d43dedcf1a`, working tree pulito.
Consultati TODO e Experiment Register ufficiali, report
`rag-v5-backend-build-abi-attestation-01.md` con E1–E4, progetto documentale
`operations/backend-harness/status-correlated-01-design/` e specifica
`H1_PRETOOLCHAIN_GATES.md`. Non risultava una ricerca equivalente conclusa.
Le evidenze ABI sono riutilizzate come dati storici: nessuna nuova scansione
VPS, chiusura ELF, suite o audit delle 25 fonti del progetto ripetuti.

Flusso: **Attività → Script → Commit → Report → Risultato → Decisione → Stato**.
Script/metodo: letture locali Git/JSON e GET HTTPS pubbliche con Python stdlib,
raccolta limitata a testo/JSON, analisi statica e SHA-256; nessun eseguibile
operativo aggiunto. Le URL esatte e gli esiti delle richieste sono nel nuovo
inventario. Il commit documentale pubblica contestualmente questo report,
snapshot, inventario, TODO e registro; il suo SHA è identificabile con
`git log -1 --format=%H -- projects/tactical-engine/docs/rag-v5-backend-h1-g2-provenance-research-01.md`.
Risultato: catena interrotta fra archivio dichiarato e identità del membro
installato. Decisione B e stati sopra indicati. STOP dopo pubblicazione e
verifica GitHub.

## Bersaglio congelato e fonti

- Libreria: `libllama-common.so.0.7.0`, SHA-256
  `ef57d101f75dbfcad9f309bbc7b08e62d38120657ca146e97ffad2680a2a953d`.
- Dati storici E1–E2: 4.642.576 byte; Build ID
  `a7bb44fb1d8cae659f9e62b00c3b43690ef27614`. Non rimisurati.
- Ollama `v0.40.5`, commit
  `d919272e53593d1d55d40e1180eaa06dfbede3ac`.
- llama.cpp pubblico
  `620d2225cc436ab0b001e3200e590e3b286ef9ab`; la risoluzione b11669 e il
  percorso FetchContent/source override sono già documentati dal progetto.
  Il pin non prova che i byte pubblici siano tutti gli input effettivi.

Evidenze nuove in
[`evaluation/backend_h1_g2_provenance_01/`](../evaluation/backend_h1_g2_provenance_01/):

- [`source-inventory.json`](../evaluation/backend_h1_g2_provenance_01/source-inventory.json):
  25 richieste, URL, esiti, dimensioni e SHA-256 dei 19 corpi HTTP 200
  conservati byte-per-byte in `sources/` (746.675 byte complessivi).
- [`evidence-summary.json`](../evaluation/backend_h1_g2_provenance_01/evidence-summary.json):
  selezione esplicita di release, asset, run, job e candidato BuildKit.
- Snapshot delle risposte API preservati: metadati osservati il 2026-11-11,
  non garanzia di immutabilità futura. I sorgenti raw sono fissati al commit
  completo; l'inventario distingue le due classi di URL. Gli errori HTTP sono
  registrati separatamente, senza attribuire loro hash di corpi non acquisiti.

## Processo pubblico di build e distribuzione

### Sorgenti, patch e configurazione prevista

Il [workflow release fissato](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/.github/workflows/release.yaml)
si attiva sui tag `v*`. Le azioni comprendono riferimenti a major tag,
es. `actions/checkout@v4`: il file non è un inventario degli esatti commit
delle azioni effettivamente risolti. I passi Docker Linux dipendenze,
immagine e archivio hanno `provenance: false` e `sbom: false`
(righe 543–544, 637–638, 657–658). Questo prova la configurazione prevista
dei passi esaminati, non l'assenza globale di attestazioni presso il produttore.
Sono previsti cache di registry e build args; il repository non sostituisce
il record di materiali/cache effettivamente usati.

Il [Dockerfile fissato](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/Dockerfile)
prevede per amd64 `rocm/dev-almalinux-8:${ROCMVERSION}-complete`, ROCm 7.2.1,
pacchetti `gcc-toolset-13-gcc`, `gcc-toolset-13-gcc-c++` e binutils, PATH del
toolset, CMake 3.31.2 e Ninja 1.12.1. I tag immagine e i pacchetti non sono
un'attestazione dei digest/versioni realmente impiegati. Il percorso CPU usa
il preset `cpu` e installazione `--strip` (righe 91–93). Il preset eredita
Release, shared libraries, backend DL, native/OpenMP disattivati e aggiunge
CPU all variants; sono valori previsti, non un CMakeCache della build VPS.
Le opzioni Go `-w -s` del workflow non attestano da sole i flag ABI C++.

Nel tree pubblico completo acquisito, `llama/compat/` contiene la patch
[`001-llama-cpp-hooks.patch`](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/llama/compat/001-llama-cpp-hooks.patch),
che interviene su `src/llama-model-loader.cpp` e `tools/mtmd/clip.cpp`.
Il [driver delle patch](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/cmake/apply-git-patches.cmake)
ordina i nomi e usa git apply, riconoscendo anche patch già applicate.
Il progetto precedente documenta `OLLAMA_LLAMA_CPP_SOURCE` e il bypass
compat: non è stata ottenuta prova dei valori effettivi in quel run.
Patch pubblica e pin non attestano l'assenza di override/materiali ulteriori.

### CI pertinente e limiti di accesso

L'API dei run per il commit esatto registra:

| Run | Evento/branch | Esito osservato | Uso probatorio |
|---|---|---|---|
| [38782957421](https://github.com/ollama/ollama/actions/runs/38782957421) | push / v0.40.5, attempt 1 | success, 2026-10-15 18:07:07–18:50:40 UTC | Run finale pertinente, head SHA esatto |
| [38766961352](https://github.com/ollama/ollama/actions/runs/38766961352) | push / v0.40.5-rc2 | success | RC2 distinto, non prova della release finale |
| [38792847862](https://github.com/ollama/ollama/actions/runs/38792847862) | release / v0.40.5, workflow latest | success | Aggiornamento successivo, non confuso con build finale |

Nel run finale risultano success i job `116587680764` (linux-depends amd64
llama-server-cpu), `116600156173` (archive Linux amd64) e `116605208443`
(release). Tempi della pubblicazione dell'asset coerenti con il job release
non sono una prova crittografica della composizione interna del payload.

La lista API contiene 33 artefatti, inclusi record `.dockerbuild` piccoli.
Il record `11995174889`, `ollama~ollama~N2Q1CH.dockerbuild`, 43.846 byte,
digest dichiarato
`5c672dcc7ab0adbd34d1060a4d03a887f1e845f502d8d0d83f813feaf969a130`,
è solo un candidato per sovrapposizione temporale al job CPU; non ne è
dimostrata l'associazione al job. La richiesta ZIP pubblica restituisce 401.
Le richieste ai log dei due job CPU/archive restituiscono 403. Nessun contenuto
di tali record/log ottenuto, nessun aggiramento dell'autenticazione.
Visibilità dei metadati non equivale ad accesso ai materiali di build.

### Archivio distribuito e checksum

La [release API](https://api.github.com/repos/ollama/ollama/releases/tags/v0.40.5)
osservata ha ID `413093320`, `immutable=false`, `target_commitish=main` e
17 asset elencati. La data pubblicata è 2026-10-14, mentre il run finale e
gli upload pertinenti sono del 15: il solo tag/data della pagina non
identifica una build. Il workflow prevede upload `--clobber` (righe 843/859).
Si conservano quindi ID, digest e snapshot, senza assumere release immutabile.

| Asset | Dimensione | SHA-256 dichiarato |
|---|---:|---|
| [644827088 — ollama-linux-amd64.tar.zst](https://api.github.com/repos/ollama/ollama/releases/assets/644827088) | 1.438.684.604 byte | `dc5eabc292f9949546c90a97c820f924b035e05243b0de13c7f366182562169c` |
| [644830363 — sha256sum.txt](https://api.github.com/repos/ollama/ollama/releases/assets/644830363) | 1.472 byte | `d617f91f1dee86904a2a7776c7b896321a10009a52bba95b09278b3614ef9425` |

Scaricato soltanto il piccolo testo checksum, il cui SHA-256 locale coincide
con il digest API dell'asset. La riga dell'archivio concorda con il digest
API `dc5e…`; **l'archivio non è stato scaricato o verificato localmente**.
Il testo enumera pacchetti/installatori/script, non l'hash della libreria.

Il workflow seleziona `lib/ollama/*.so*` per l'archivio principale
(riga 680), genera liste di percorsi `.tar.in`, controlla la presenza di
payload e produce checksum dei file distribuiti (riga 789). Queste liste
non costituiscono un manifest degli hash dei membri. L'instradamento di
`lib/ollama/include*` nell'archivio MLX (riga 685) non dimostra disponibilità
degli header C++ common/json associati al Build ID bersaglio. Nessun altro
archivio è stato acquisito o proposto come sostituto.

Le richieste pubbliche all'API attestazioni per il digest della libreria e
per quello dell'archivio hanno restituito 404. Nell'elenco asset osservato non
sono presenti asset esplicitamente identificati come SBOM/provenance o SDK/debug
del target. **Non sono state ottenute attestazioni**: 404 e inventario asset
non dimostrano che il produttore non ne possieda o non ne pubblichi altrove.

## Matrice della catena di provenienza

| Livello | Evidenza osservata | Proprietà dimostrata nel perimetro | Limite residuo / H1-G2 |
|---|---|---|---|
| Sorgenti | SHA Ollama completo, pin llama storico, tree/patch pubblici con hash | Ricetta e sorgenti pubblici identificabili | Non attestati tutti gli input realmente usati, override o object precompilati |
| Configurazione di build | Workflow, Dockerfile, preset, driver patch fissati; run finale head SHA concorde | Configurazione prevista e run registrato con esito success | Mancano materiali effettivi, digest container, package lock, CMakeCache, compile/link commands e valori override |
| Binario distribuito | Asset ID/dimensione/digest, checksum testuale verificato | Identità dichiarata dal publisher per l'archivio nello snapshot | Nessuna verifica locale dei byte archivio o attestazione ottenuta che lo leghi a tutti gli input |
| Corrispondenza VPS byte-per-byte | Hash e Build ID storici E1–E2, senza nuove letture VPS | Identità storica del target congelato | Nessun manifest attendibile archivio→membro→hash `ef57…`; catena interrotta qui |
| Header e layout C++ | Firme/header pubblici già nel progetto; ricetta strip | Disponibilità del contratto pubblico candidato | Nessun SDK/debug/header closure attestato per Build ID esatto; layout/ABI non provati anche ipotizzando match del membro |

## Richiesta documentale puntuale e criterio di arresto

Per completare il dossier servono prove del produttore/custode, senza
effettuare nuove compilazioni o assumere una build upstream equivalente:

1. **Legame archivio/membro installato:** manifest per-file autenticato o
   attestazione di estrazione attendibile riferita all'asset `644827088` e
   digest completo `dc5e…`, che identifichi il percorso membro
   `lib/ollama/libllama-common.so.0.7.0`, SHA-256 completo `ef57…`, dimensione
   e Build ID storico. Se il percorso effettivo è diverso, deve essere
   dichiarato nel manifest: il percorso atteso dalla ricetta non è una prova.
2. **Provenance della build effettiva:** attestazione che leghi quel prodotto
   al run `38782957421`/attempt 1 e ai job/materiali realmente utilizzati,
   commit completi, patch con digest, eventuali override e input precompilati;
   digest container/sysroot/package/toolchain e opzioni compile/link/macros,
   include closure e CMakeCache. Un'eventuale SLSA/SBOM va valutata per il
   contenuto effettivo: il nome del formato non garantisce i campi necessari.
3. **Header e tipi del prodotto:** SDK/header manifest e debug symbols o
   attestazione attendibile di layout per Build ID
   `a7bb44fb1d8cae659f9e62b00c3b43690ef27614`, con identità di ogni input
   pertinente. Header upstream e simboli esportati non sostituiscono la prova.
4. **Supporto CI consultabile:** esportazione dei piccoli record BuildKit/log
   pertinenti con associazione certa ai job e digest; gli endpoint pubblici
   interrogati non ne consentono l'acquisizione. Tali record sarebbero supporto
   al dossier, non automaticamente una prova del layout o del membro VPS.

È una richiesta documentata, non un messaggio inviato a terzi. Non richiede
in questa sessione grandi download o accesso autenticato aggiuntivo.
L'interruzione pubblica è identificata: digest del pacchetto dichiarato,
ma nessuna associazione attendibile ottenuta al membro `ef57…` e ai suoi
input/header reali. Ulteriori somiglianze di compiler, commit, simboli o
versioni non colmerebbero questa lacuna; la ricerca si arresta qui.
La disponibilità potenziale di record CI giustifica **B**, senza dichiarare
definitivamente impossibile ottenere documentazione dal produttore (decisione C).

## Verifiche documentali e conservazione

Eseguiti soltanto controlli locali dei nuovi materiali: tutti i 19 snapshot
HTTP 200 corrispondono a dimensioni/SHA-256 inventariati; checksum testuale
coerente con metadati asset; distinzione run finale/RC2 e confini probatori
documentati. Questi sono controlli di custodia della nuova raccolta, non
ripetizioni di attestazione ABI o test backend. Prima della pubblicazione si
verificano inoltre riferimenti locali, JSON, diff e perimetro dei file.
Gli snapshot upstream conservano anche gli spazi finali originali segnalati
da diff --check; non vengono normalizzati per preservarne gli hash. Il
controllo whitespace dei documenti redatti esclude soltanto `sources/`.
Nessun miglioramento di accuratezza o compatibilità dichiarato.

Nessun accesso VPS, download di archivi binari, compiler, linking, loading,
converter, tokenizer o modelli. Nessun harness implementato, file applicativo,
schema, progetto harness, manifest congelato o risultato storico modificato.
Nessun runtime-05, staging, wrapper, inferenza, merge o deploy. STOP.
