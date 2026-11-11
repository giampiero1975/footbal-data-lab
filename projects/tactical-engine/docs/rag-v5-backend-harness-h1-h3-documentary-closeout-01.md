# RAG V5 — closeout documentale precisazioni H1–H3

Attività: `RD-RAG-V5-BACKEND-HARNESS-H1-H3-DOCUMENTARY-CLOSEOUT-01`.
Data: 2026-11-11, Europe/Rome.

## Attività → Script → Commit → Report

Integrato esclusivamente il progetto documentale con i rilievi H1–H3 della
revisione indipendente `c99a456`. Prerequisiti futuri più verificabili, senza
attestarli, implementarli o autorizzarne l'esecuzione.

Prima delle modifiche: TODO e Experiment Register del branch ufficiale letti,
riconciliati report di ricognizione, progettazione e revisione indipendente,
evidenza statica e inventario delle 25 fonti già approvato. Nessun audit 25/25
ripetuto e nessuna nuova acquisizione dei sorgenti. Branch
`codex/tactical-state-contract-v1`, HEAD iniziale locale/GitHub
`c99a456ad637de6ef1d995bbe9b869a7d7378acf`, working tree pulito.
H1–H3 risultavano precisazioni DA FARE, non già integrate.

Script: sola lettura Git/JSON, scrittura dei documenti autorizzati, Python
inline per controlli documentali di presenza/struttura/riferimenti e confronto
dei due manifest congelati con i blob Git iniziali. Giustificazione registrata
nel README prima dei controlli: nuovi contenuti H1–H3 non coperti dalla verifica
precedente. Nessun file script eseguibile, compiler o harness prodotto.

Commit documentale che pubblica insieme documenti, delta, evidenze, questo
report, TODO e registro; identificabile senza autoriferimento circolare con:

```text
git log -1 --format=%H -- projects/tactical-engine/docs/rag-v5-backend-harness-h1-h3-documentary-closeout-01.md
```

## Delta documentale

Sotto `operations/backend-harness/status-correlated-01-design/`:

| Documento | Delta |
|---|---|
| README.md | Indice H1–H3 e collegamenti alle specifiche; requisiti cumulativi e nessuna deroga; esplicitata durata wall-clock; giustificazione dei nuovi controlli |
| H1_PRETOOLCHAIN_GATES.md | Nuovo: G0 e sei gate ordinati, evidenza/arresto/proprietà non dimostrata; confini pre-toolchain/link/loading e custodia |
| H2_SUPERVISOR_CONTRACT.md | Nuovo: sei categorie di policy senza soglie assegnate, contenimento del gruppo, arresto controllato/forzato e finalizzatore esterno |
| H3_CONSTRAINT_LEDGER.md | Nuovo: cinque classificazioni, congiunzioni e ref, quattro JSON Pointer concreti, scope pubblico distinto dalla VPS e controlli Python residui |

`sources-lock.json` e `target-contract.json` sono **byte-identici** al commit
iniziale, non semplicemente semanticamente equivalenti. SHA-256 conservati:

- sources-lock: `614d5795a1cd2f7e5ba7138848764b3a98cc51f4bdde60b2c969589fec71ff43`;
- target-contract: `4ff99ac9c995a8bb8ad4dbc26eed5f58a34b84d89fbdec95ccf4960b40d1ae1f`.

Non modificati TOKEN_BUDGET, schema, codice applicativo/validatore, test,
Gold/dataset, wrapper, evidenze runtime o report precedenti. Gli hash dei quattro
documenti aggiornati sono registrati nell'evidenza nuova.

## Risultato H1 — gate e proprietà non dimostrate

H1-G1 identifica compiler/linker/driver/sysroot; G2 gli input header/object e
librerie; G3 flag ABI, macro, eccezioni e RTTI; G4 percorsi/plugin/preload e
ambiente/FD; G5 closure transitiva e moduli dinamici; G6 custodia e TOCTOU.
Ogni riga definisce evidenza necessaria, arresto con reason code e limite della
prova. G0 distingue l'eventuale mandato futuro dall'approvazione del documento.

Le verifiche precedono l'invocazione della toolchain, il linking e il loading
nei rispettivi confini. Hash nel main, ricerca via PATH, DT_NEEDED considerato
esaustivo o rilettura dell'inode senza immutabilità non sono prove sufficienti.
Nessun gate è stato eseguito o implementato. Il raccordo sorgenti/build/ABI del
binario VPS resta da dimostrare separatamente.

## Risultato H2 — supervisione e finalizzazione

Definiti deadline monotono indipendente dalla CPU, budget CPU e memoria del
gruppo, limiti output, grace e risorse/durata del finalizzatore. **Tutti i valori
restano NON DEFINITO, non approvato**: prima dell'avvio servono analisi e
approvazione successive, non valori ereditati dai runtime Qwen.

Il supervisore deve controllare tutti i discendenti e rimanere con il
finalizzatore fuori dal gruppo da terminare; contenimento e identificazione
stabile sono prerequisiti. La sequenza prevede stop controllato, eventuale
terminazione forzata, prova di cessazione e finalizzazione esterna anche senza
JSON del worker. Nessun riavvio/retry automatico.

Dodici categorie distinguono eccezione, loader, crash, OOM, wall timeout,
CPU/memoria/output, protocollo worker, segnale senza causa dimostrata,
contenimento e finalizzazione; il pre-avvio ha il proprio arresto.
SIGKILL/exit 137 non bastano per diagnosticare OOM. Trigger multipli e cause
incerte sono conservati, non convertiti in incompatibilità dello schema.

Inventari e SHA-256 riguardano i byte realmente persistiti; catture troncate e
perdite non quantificabili sono dichiarate. Il marcatore finale richiede prova
di terminazione e inventario coerente. La finalizzazione incompleta non è
completamento tecnico e non promuove il backend. Tutto resta una specifica.

## Risultato H3 — ledger dei vincoli composti

H3-C1 errore converter/parser; C2 restrizione schema non rappresentata; C3
presenza senza enforcement verificato; C4 controllo deliberatamente esterno;
C5 annotazione non restrittiva. Le categorie sono tecniche, non stati di progetto.
Il ledger considera congiunzioni, scope/ramo/dialetto, origine dei ref e JSON
Pointer concreti; non classifica i nomi delle proprietà come keyword schema.

Documentato senza riesecuzione il controesempio già approvato: `entity:` più
65 `a` è lungo 72, soddisfa `^entity:.+$` e viola maxLength=71. Quattro voci
individuano il limite per subject/reference e rami explicit/implicit.
La prova statica precedente riguarda il GBNF pubblico
`620d2225cc436ab0b001e3200e590e3b286ef9ab`, non la VPS. Nel primo scope è C2;
nel target installato non attestato l'enforcement resta C3.

Ogni voce registra evidenza, impatto e residuo `_valid_entity_id` richiamato
anche da `_representation_errors`. Né maxLength né il predicato Python sono
modificati. uniqueItems perso dalla grammatica non diventa C4 perché esiste
una rejection Python. Comparison, grounding e derivazione label restano invece
controlli deliberatamente esterni come relazioni semantiche. Se una restrizione
non esiste nello schema, schema_pointer=null evita pointer inventati.

## Nuovi controlli documentali eseguiti

Evidenza: `docs/backend-harness-h1-h3-documentary-checks-01.json`.
**17/17 controlli documentali nuovi coperti**, zero fallimenti:

| Gruppo | Controlli | Evidenza documentale coperta |
|---|---|---|
| H1 | D01–D04 | Sei gate, tre confini, origini/flag/ambiente/closure, custodia e arresti |
| H2 | D05–D09 | Policy senza soglie, clock monotono, gruppo, dodici categorie e finalizzazione senza JSON |
| H3 | D10–D13 | Cinque categorie, quattro pointer, combinazione/source scope/VPS e distinzione esterno/annotazione/perdita |
| Riferimenti/perimetro | D14–D17 | Link locali, manifest byte-identici, autorizzazione false e attestazione null, percorsi applicativi/storici invariati |

Sono controlli di presenza, struttura, riferimenti e preservazione, accompagnati
da ispezione manuale delle specifiche. Non sono test di un supervisore, prove
di enforcement, attestazione ABI o compilazione di uno schema. Nessun audit
25/25, suite 37/13/16/5, modello o verifica remota ripetuti.

## Decisione → Stato

**Progetto idoneo a una successiva attività separata di attestazione ABI**:
H1–H3 hanno ora requisiti documentali verificabili, arresti e limiti espliciti,
senza inferire identità del binario o sostituire dati mancanti con valori.
Non si avvia tale attività e non si autorizza implementazione, toolchain,
linking o loading. La chiusura è delle precisazioni documentali, non delle
prove operative richieste dalle specifiche.

Precisazioni **IMPLEMENTATO** documentale; controlli **ESEGUITO**, proprietà
documentali coperte **VALIDATO**. Attestazione ABI **DA FARE**. Implementazione
eseguibile, compatibilità backend, accuratezza generativa, Gate, integrazione
e certificazione **BLOCCATO**.

Report, delta, evidenza dei controlli, documenti, TODO e Experiment Register
pubblicati nello stesso ciclo. Nessun C++, CMake, script eseguibile, harness,
VPS, compilazione/link/loading, inferenza, runtime-05, staging, wrapper, merge
o deploy. STOP dopo pubblicazione e verifica GitHub/repository.
