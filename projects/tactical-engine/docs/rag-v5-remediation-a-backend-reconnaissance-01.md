# RAG V5 — ricognizione backend remediation A

Attività: `RD-RAG-V5-REMEDIATION-A-BACKEND-RECONNAISSANCE-01`.
Data: 2026-11-10, Europe/Rome.

## Attività → Script → Commit → Report

Ricognizione read-only della VPS, non test di compatibilità. Decisione unica
**B — occorre risolvere un prerequisito tecnico prima della verifica backend**:
identificare o predisporre un ingresso non generativo verificabile del
convertitore installato, con ABI/header corrispondenti e instradamento del
parametro format documentato. Nessun compilatore o modello eseguito.

Riconciliati TODO, Experiment Register e report remediation A offline,
revisione indipendente iniziale, closeout R1, rivalutazione post-R1 e preflight
non generativo runtime-04. Branch `codex/tactical-state-contract-v1`, HEAD
iniziale locale/GitHub `ca6bf675b53d700eafef185eba6f3bb3af2e130e`, working tree
pulito, origin `giampiero1975/footbal-data-lab`. Nessuna ricognizione equivalente
registrata: il precedente preflight rilevava versione/tags/ps, non identità del
convertitore, tokenizer, template o ingresso di compilazione senza modello.
Le vecchie evidenze sono riusate; le sole GET ripetute osservano dati volatili
richiesti dal mandato, non suite applicative.

Script: cinque sessioni SSH diagnostiche con Python stdlib
`/usr/bin/python3 -B -I -` via stdin, non installato sulla VPS; letture file,
GET note, `systemctl show`, `readelf`. Nessun import applicativo o caricamento
di librerie tramite ctypes. SSH tramite `football-vps`, BatchMode,
StrictHostKeyChecking=yes, UpdateHostKeys=no, KEX curve25519-sha256 e host key
ssh-ed25519. Profilo effettivo: football@163.5.26.155:22, identità v3 già
approvata. Il profilo sandbox iniziale non esponeva l'alias: la lettura nel
profilo Windows autorizzato lo ha confermato; nessuna configurazione SSH alterata.

Quattro sole richieste HTTP: GET `/api/version`, `/api/tags`, `/api/ps` iniziale,
GET `/api/ps` finale. Nessun POST, show via POST, generate/chat, tokenize,
warm-up, pull, wrapper o acquisizione lock. Nessun accesso a staging,
checkout operativo, Chroma, panel o artifact runtime.

Commit: esclusivamente documentale, report/evidenze/TODO/registro pubblicati
insieme; identificabile con:

```text
git log -1 --format=%H -- projects/tactical-engine/docs/rag-v5-remediation-a-backend-reconnaissance-01.md
```

Evidenze locali versionate, tutte sotto `docs/`:

- `remediation-a-backend-reconnaissance-summary-01.json`: campi selezionati
  trascritti dall'output SSH iniziale, metodo esplicitato, perimetro e decisione;
- `remediation-a-backend-installed-evidence-01.json`: stdout JSON della lettura
  di manifest, identità binari, simboli e configurazione;
- `remediation-a-backend-model-metadata-evidence-01.json`: stdout JSON di
  piccoli blob, limitazioni di accesso, simboli mirati e disponibilità strumenti;
- `remediation-a-backend-tokenizer-header-evidence-01.json`: stdout JSON dei
  soli metadati GGUF e dati ELF statici;
- `remediation-a-backend-final-observation-01.json`: stdout JSON dello snapshot
  finale, nomi candidati e dipendenze ELF.

Snapshot iniziale `16:23:50Z`, finale `16:30:01Z`; osservazioni istantanee,
non garanzia di assenza universale di attività concorrenti nell'intervallo.

## Risultato — matrice delle proprietà

| Proprietà | Evidenza osservata | Proprietà dimostrata | Limite residuo | Prova successiva necessaria |
|---|---|---|---|---|
| Ollama | GET version 200: 0.40.5; binario SHA-256 505c0068464497f69932d1ae5d8b6c9ad6fdcf07342c683d78dfb1ced60558e6 | Versione dichiarata dal servizio e identità file installato | Non è una versione del compilatore JSON Schema; Go VCS revision non ricavata dai metadati esaminati | Associare instradamento format alla build effettiva |
| Modello | GET tags: qwen3.5:9b, 9.0B, GGUF, Q4_K_M, runner llamacpp | Identità del record installato e manifest corrispondente | Non prova integrità di tutti i pesi né accuratezza | Riutilizzare digest immutato in una futura prova autorizzata |
| Digest | Manifest runner da 1.088 byte, hash 56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90, identico a tags | Digest è quello del manifest selezionato | Non confondere con hash del file GGUF dei pesi | Nessuna nuova hash integrale dei pesi richiesta o eseguita |
| Decoder installato | Librerie llama; dati ELF LLAMA_COMMIT=620d2225c, LLAMA_BUILD_NUMBER=1, target Linux x86_64 | Identità incorporata nella libreria installata, con hash/build ID registrati | Non prova quale ramo del convertitore sia usato da un'ipotetica richiesta nuova | Verifica del percorso format con sorgenti/ABI corrispondenti |
| Convertitore | Due simboli C++ definiti json_schema_to_grammar in libllama-common; riferimento UND dal server-impl; DT_NEEDED coerenti | Convertitore linkato disponibile nell'installazione | Nessuna compilazione del nuovo schema, ABI C++ non sostituibile con una firma supposta | Ingresso/harness non generativo verificabile della medesima build |
| Costrutti schema | Contratto versionato status-correlated-01, alternative complete anyOf e vincoli sotto elencati | Struttura statica già esaminata, invariata da R1 | Simbolo del convertitore non attesta supporto/enforcement di ogni keyword | Compilare schema completo e valutare vincoli, in attività separata |
| Tokenizer | Header GGUF: model=gpt2, pre=qwen35, 248.320 token, 247.587 merges; hash array registrati | Metadati e materiali del tokenizer installato identificati senza tensori | Non eseguito il tokenizer effettivo né verificata equivalenza di una sua eventuale reimplementazione | Conteggio con tokenizer identico, special token e percorso template verificati, senza sampling |
| Chat template | Layer Ollama di 13 byte {{ .Prompt }}; config renderer/parser qwen3.5; template Jinja GGUF di 7.756 byte | Identificati tre livelli distinti già installati | Non dimostra il testo finale applicato dal runner; i template non sono automaticamente intercambiabili | Ricostruzione del rendering effettivo della build con think=false |
| Contesto modello | tags e GGUF qwen35.context_length=262144 | Limite dichiarato dai metadati modello | Non è il contesto attivo 4096 richiesto dal progetto né garanzia di capienza | Verificare trattamento delle opzioni e politica di troncamento della build |
| Configurazione servizio | User/Group ollama, PID 812, ExecStart /usr/local/bin/ollama serve; nessuna variabile allowlist nel risultato systemd Environment | Configurazione visibile e processo server osservato | /proc/812/environ ed exe negati; ambiente effettivo completo non provato | Fonte leggibile o estratto amministrativo mirato se necessario; nessun cambio permessi |
| Parametri modello | Blob params: presence_penalty=1.5, temperature=1, top_k=20, top_p=0.95 | Default memorizzati nel modello | Payload progetto esplicita temperature=0, num_ctx=4096, num_predict=2048; fusione effettiva non provata qui | Conservare le opzioni e verificare la precedenza nella build, senza alterarle |
| Budget messaggio | Evidenze locali: handoff 6.967 byte, user storico 7.311, schema 16.869 | Dimensioni documentali, non token | GET noti non forniscono conteggio nuovo; format può essere trattato fuori dal testo | Misura separata del rendering e tokenizer, non prompt_eval_count ottenuto generando |
| Stato caricato | GET ps iniziale e finale: models=[] | Nessun modello caricato nei due snapshot | Non sorveglianza continua; non prova attività di altri client | Nessun warm-up per colmare il limite |
| Strumenti | g++/c++ risolti; go, cmake, pkg-config e CLI tokenizer/grammar esaminate non risolti; header/source non trovati nei candidati ispezionati | Prerequisito parziale di toolchain; mancano un ingresso verificato e interfacce associate nel perimetro esaminato | Non prova assenza su tutta la VPS; presenza g++ non basta | Individuare sorgenti/header o tool di sola compilazione della build corretta, previa distinta autorizzazione |

## Identità e correlazioni dei file

Store: `/usr/share/ollama/.ollama/models`.
Il manifest legacy del tag ha hash `85879493124988ce76ff36a6ac583504cc8d893727db6a0c4f9992a079e6ca49`;
il manifest-list v2 hash `fdf5fd4cd409881fac86077d7be23e1cb1a4d1c0083108ff81ad557b3dfd7b01`
seleziona runner llamacpp, digest `56671c2a...`. La diversa identità del
contenitore legacy non è una divergenza del modello selezionato.
Il manifest selezionato indica il GGUF
`sha256:02d45dc1cf451ba2475ac33b301c2dd8f985abe4c182ce04a1f2f5bf0260278d`,
5.629.109.120 byte; non è stato letto o hashato integralmente.

`libllama-common.so.0.7.0` SHA-256
`ef57d101f75dbfcad9f309bbc7b08e62d38120657ca146e97ffad2680a2a953d`,
Build ID `a7bb44fb1d8cae659f9e62b00c3b43690ef27614`.
`libllama-server-impl.so` SHA-256
`2d8d42a9328139d4847452d67aeb894a315bebe242a6c67507334ec96396d86d`.
LLAMA_COMMIT è un'identità incorporata breve, non una certificazione di
corrispondenza integrale al sorgente upstream. SONAME 0.7.0, build number 1,
commit llama e versione Ollama sono dati distinti. Con ps vuoto non è osservabile
un decoder caricato dal runner; il commit identifica la libreria installata,
non una chiamata effettiva del servizio. Il divieto di leggere /proc/812/exe
impedisce inoltre di confrontare l'inode eseguito con il file su disco. Le licenze XGRAMMAR presenti
non dimostrano che XGrammar gestisca questo modello o schema.

I simboli Ollama leggibili includono llamaServerRunner.schemaGrammar,
ApplyChatTemplate, Tokenize e thinkingGrammar. Sono indizi statici di componenti,
non tracce di esecuzione: non dimostrano come format o think=false interagiscano
con prompt e grammatica. Non si assume né inserimento integrale dello schema
nel contesto né costo nullo dello schema. Non sono stati interrogati endpoint
nuovi per dedurre queste proprietà.

## Tokenizer, template e budget senza caricamento

Il JSON metadata separato del GGUF è negato a football (PermissionError), come
alcuni file procfs del servizio. Nessun sudo, cambio ACL o lettura privilegiata.
Il contenitore GGUF è invece leggibile: esaminato il solo header fino a offset
10.942.739, con limite rigido 32 MiB e nessuna lettura di tensor info/data.
Letture totali dei metadati, inclusa rilettura per hash array: 14.909.929 byte.
Questo è parsing documentale, non llama_model_load, mmap dei pesi o caricamento
tramite Ollama.

Token EOS 248046, padding 248044, add_bos_token=false. Le impronte negli
artefatti riguardano gli array GGUF codificati, non un tokenizer.json alternativo.
Il template GGUF, conservato integralmente nell'evidenza, ha SHA-256
`a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715`.
Contiene regole per system/user, tool e enable_thinking. Non è stato renderizzato:
la presenza di un ramo non prova che la build lo selezioni o con quali kwargs.

Nei tre GET autorizzati non si è osservato un servizio di conteggio token o
compilazione. Non è stata tentata una richiesta vuota, num_predict=0 o altra
variante di generate/chat: potrebbe caricare il modello o avviare lavoro
applicativo e non rispetterebbe il mandato. Neppure prompt_eval_count del vecchio
runtime-04 (592) misura il nuovo handoff. Nessun rapporto byte/token applicato.

Una futura misura attendibile deve usare vocabolario/merges/pre-tokenizer
esatti, special token e rendering effettivo della build con gli stessi
system/user, think=false e trattamento format; deve produrre il conteggio senza
sampling o pesi caricati. Se non esiste un tale ingresso, prima va progettato
e revisionato un tool separato di sola metadata/tokenizzazione. Non basta
usare un tokenizer genericamente chiamato GPT-2 o il template layer da solo.
Le impostazioni attive di contesto e l'eventuale eliminazione di messaggi vanno
verificate sul codice corrispondente, non dedotte da 262144 o dalle dimensioni.

## Schema e prerequisito della prova successiva

Costrutti del contratto `status-correlated-01`: type, enum, const, properties,
required, additionalProperties, anyOf completo, $defs/$ref locali, min/maxItems,
min/maxLength, pattern, uniqueItems; metadati description, $schema e $id.
Non introdotti if/then/else, contains, not, allOf o dependentSchemas. Comparison
tra lati, ID, condizioni residue, grounding e coerenza label restano controlli
deterministici del progetto: non diventano garanzie della grammatica.

La versione applicazione e i simboli esportati provano una **compatibilità
potenziale da investigare**, non il supporto effettivo di anyOf annidati, refs,
pattern, array vuoti o uniqueItems nello schema completo. Non è stato invocato
il convertitore, il parser grammaticale o un backend validatore. Nessuna
modifica al contratto per adattarlo alla build.

Mancano un ingresso non generativo verificato e header/ABI affidabili per i
tipi C++ common_json/common_chat_schema_document esportati. Il solo simbolo
non permette una chiamata sicura con ctypes o una dichiarazione C++ inventata.
Nei percorsi convenzionali esaminati e nel tree `/usr/local/lib/ollama` non sono
stati localizzati i relativi sorgenti/header o un CLI dedicato; questa è una
ricerca delimitata, non una dichiarazione su file mai ispezionati.

**Prerequisito da risolvere separatamente:** individuare o procurare, con
autorizzazione distinta, sorgenti/interfacce compatibili con commit incorporato
e hash installati, oppure un ingresso già disponibile dimostrabilmente privo
di caricamento/sampling. Solo dopo definire un comando riproducibile di
compilazione dello schema completo con diagnostica di vincoli ignorati e prova
della corrispondenza al percorso format. Nessun download, harness, compilazione
o nuova installazione effettuati ora.

L'eventuale prova futura avrebbe una differenza tecnica rispetto ai test
Python già conclusi: bersaglio il convertitore reale della build identificata,
non lo shape checker locale. Non sono proposti retry generativi o una nuova
campagna di casi. Le suite 37/13/16/5 non sono state eseguite.

## Impedimento automatico e alternativa sicura

Un comando iniziale di lettura blob è stato respinto dall'auto-review prima di
partire: `read_bytes()` senza limiti poteva caricare un file grande in memoria.
La lettura successiva, approvata, ha imposto media type allowlist escludendo
model/projector, stat-before-read, massimo 64 KiB per i piccoli blob e 8 MiB per
il JSON metadata. L'header GGUF successivo ha un limite indipendente 32 MiB e
arresto prima dei tensori. Nessuna operazione rimane bloccata da quel rifiuto;
il prerequisito B riguarda invece le interfacce non generative non verificate.

## Decisione → Stato

**Unica decisione: B — risolvere il prerequisito tecnico dell'ingresso di prova
non generativo prima della verifica backend.** Le identità e i metadati sono
abbastanza precisi per delimitare il bersaglio; manca ancora un comando
attendibile che eserciti quel compilatore senza runner/modello e senza ABI
supposte. Non è una dichiarazione di incompatibilità dello schema o della build.

Ricognizione **ESEGUITO**, evidenze dichiarate **VALIDATO** nel solo perimetro
osservato. Verifica backend **BLOCCATO** dal prerequisito; soluzione del
prerequisito **DA FARE**. Backend non **VALIDATO**, modello non caricato,
conteggio token e compilazione schema non effettuati. Accuratezza generativa,
Gate, integrazione e certificazione restano **BLOCCATO**.

Pubblicati insieme report, cinque evidenze diagnostiche, TODO e Experiment
Register. Nessuna modifica applicativa o remota; nessun wrapper/runtime-05,
trasferimento di artefatti, staging, lock, merge, deploy o promozione. STOP.
