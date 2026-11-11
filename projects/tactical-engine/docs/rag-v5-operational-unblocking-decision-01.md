# RAG V5 — decisione di sblocco operativo

Data: 2026-11-11. Attività documentale:
`RD-RAG-V5-OPERATIONAL-UNBLOCKING-DECISION-01`.

## Decisione unica: percorso B, API ufficiale Ollama

Raccomandato un solo esperimento successivo: una chiamata generativa controllata
a `POST /api/chat` sul caso storico `q3_04`, con schema completo e handoff della
remediation A dopo R1. Usare il caller Python già versionato e un trasporto
SSH verso il loopback del servizio. Nessun collegamento diretto del client
alla libreria C++ installata, nessun nuovo backend o staging remoto.

**Il test non è eseguito né autorizzato da questo documento.** Richiederà
autorizzazione esplicita a caricare Qwen, eseguire la conversione dello schema
nel servizio/decoder e una sola generazione. La distinzione elimina un
prerequisito del particolare harness C++, non colma o aggira un gate ABI di
quell'harness. H1–H3 e i manifest di quel progetto rimangono invariati.

L'API è un confine di servizio già utilizzato dal progetto: il client scambia
JSON e non costruisce oggetti C++ con layout supposti. Il servizio continua
a usare internamente i suoi componenti non attestati; non viene dichiarata
attestazione della build o equivalenza integrale coi sorgenti pubblici.
La fiducia operativa nel servizio installato e l'osservazione del suo output
sono esplicitamente diverse dalla prova di provenienza/ABI.

## Riconciliazione e differenza tecnica

Branch `codex/tactical-state-contract-v1`, origin
`https://github.com/giampiero1975/footbal-data-lab.git`, HEAD iniziale locale e
GitHub `cec94e57ce11903460bc9314de2c699aa83b0193`, working tree pulito.
TODO e Experiment Register consultati anche tramite raw GitHub a tale SHA e
confrontati con i blob Git. Letti report ABI `809be0b`, ricerca H1-G2 `cec94e5`,
ricognizione backend, progetto token, rivalutazione post-R1, remediation A e
risultato runtime-04. Il caller effettivo e i suoi rami sono letti staticamente.
Nessuna decisione equivalente di passaggio all'esperimento API post-R1 risulta
già conclusa nel registro.

| Evidenza riutilizzata | Cosa dimostra | Cosa non ripetere/non dedurre |
|---|---|---|
| Runtime-04: una generazione, HTTP completato, boundary semantico, modello propone supported, label osservata nulla | Il precedente percorso API ha risposto sul contratto precedente | Non dimostra compatibilità del nuovo schema o correttezza dopo remediation A |
| Remediation A `0ea62c0`, 16 controlli; R1 `5bfa489`, 5 controlli; rivalutazione `ca6bf67` | Delta implementato e controlli offline/documentali nel proprio perimetro | Nessuna suite 16/5 o revisione integrale da ripetere |
| 37 controlli deterministici, 13 controlli wrapper e gate storici | Evidenze storiche dei rispettivi perimetri | Nessun nuovo run delle suite, wrapper o gate runtime-04 |
| Ricognizione modello/backend, ABI e H1-G2 | Identità storiche e lacune precise | Nessuna nuova scansione VPS, closure ELF, audit fonti o ricerca di provenance |

**Differenza tecnica che giustifica l'unico esperimento futuro:** runtime-04
usava la baseline `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`. Ora il trasporto
ha `representation_revision=status-correlated-01`, alternative correlate
status/contenuto e istruzioni normative corrette dopo R1. Il nuovo schema
completo e il nuovo handoff non sono mai stati esercitati con Qwen nelle
evidenze riconciliate. Ripetere lo stesso caso isola il delta del contratto;
non è una ripetizione equivalente di runtime-04. Non serve cambiare modello,
Gold, parametri, locator o validatore.

## Confronto dei percorsi

Stime di pianificazione, non misure né impegni sui tempi del servizio.

| Percorso | Prerequisiti risolvibili oggi | Tempo/complessità stimati | Rischio e valore | Scelta |
|---|---|---|---|---|
| A — Recupero ABI | Nessuna nuova prova concreta accessibile oltre il dossier H1-G2; serve documentazione del produttore | Indeterminato, dipendenza esterna | Altri indizi non colmano archivio→membro→header/layout | Non proseguire la ricerca; riaprire solo alla consegna di prove nuove specifiche |
| B — API ufficiale | Caller e servizio già usati; contratto e input locali disponibili; serve mandato generativo separato | Circa 1–2 ore di preparazione/revisione del piccolo driver e raccolta; una richiesta entro i limiti temporali già usati | Testa il servizio realmente destinato a Qwen, senza ABI client; rischio schema/budget/timeout esplicito | **Unico percorso raccomandato** |
| C — Backend isolato | Occorrerebbero build/toolchain controllate, ambiente, pesi e distinta autorizzazione | Ordine di giorni, dipende dalle risorse | Riproducibilità del nuovo backend; non trasferibili identità, ABI, compilazione, template, token o comportamento del backend VPS senza ulteriore prova | Non selezionato: non accorcia il percorso verso il servizio installato |
| D — Deterministico esistente | Già disponibile | Riutilizzo immediato | Utile per interpretare un nuovo raw; nessuna prova del decoder o accuratezza | Riutilizzato come evidenza, non nuova attività di test |

Il vecchio runtime-04 è durato circa 133 secondi: è un riferimento storico,
non una previsione sul nuovo schema/handoff. Un errore di compilazione o
budget del servizio darebbe comunque evidenza nuova direttamente utilizzabile.
Non occorre dichiarare compatibilità completa prima di poter osservare una
richiesta attraverso un'interfaccia supportata, se tale prova è autorizzata.

## Interfaccia supportata e confini della prova

Nuova consultazione strettamente mirata, giustificata dal confronto B richiesto:
[documentazione structured outputs](https://docs.ollama.com/capabilities/structured-outputs)
e [riferimento API chat](https://docs.ollama.com/api/chat), osservati il
2026-11-11. Documentano schema JSON nel campo `format` di `POST /api/chat`,
messaggi, opzioni e contatori della risposta. Sono documentazione corrente,
non un'attestazione della build VPS 0.40.5 o del supporto di ogni keyword.
Non ne viene seguito il suggerimento opzionale di duplicare lo schema nel
prompt: il payload del caller rimane invariato.

Nel codice congelato a `cec94e5`,
`scripts/shadow_nli_spatial_relations_v2_inference.py`:

- `_default_transport()` righe 67–75 usa già `POST /api/chat`;
- `judge_pair()` righe 110–121 costruisce schema completo, system/user,
  `think=false`, `stream=false`, opzioni e una sola chiamata al trasporto;
- il ramo extraction passa il raw a `materialize_extraction()`; i risultati
  non valutabili restano fail-closed e senza promozione.

| Livello | Classificazione corretta |
|---|---|
| GET version/tags/ps | Diagnostica non generativa; non compila lo schema e non prova compatibilità |
| Compilazione senza modello tramite API ufficiale | Nessun ingresso compiler-only supportato è dimostrato dalle fonti disponibili; non viene proposto un nuovo giro di ricerca |
| Decoder con `format` | Conversione/uso interno della grammatica e selezione vincolata dei token; una risposta non prova enforcement universale di tutte le keyword |
| `/api/chat` sul caso proposto | Esperimento generativo: può caricare modello/pesi ed eseguire inferenza, oltre al decoder |

Non usare richieste vuote, `num_predict=0`, `-1`, warm-up o endpoint interni
`/completion` come surrogati di una prova non generativa. Non sono scorciatoie
attestate e non sono incluse nel metodo. Un HTTP 200 o un JSON valido non
bastano per dichiarare schema completo o accuratezza validati.

## Una sola attività successiva

**ID:** `RD-RAG-V5-REMEDIATION-A-OFFICIAL-API-SINGLE-CASE-01`.
**Stato: DA FARE**, esecuzione non autorizzata. Non è runtime-05, non esegue
wrapper storici e non richiede staging. La preparazione del driver e la sua
eventuale singola esecuzione appartengono a questa stessa attività futura;
non si propone un'altra indagine o catena di revisioni documentali.

### Script/metodo previsto

Piccolo driver Python locale dedicato, da predisporre e controllare staticamente
nell'attività autorizzata. Riusa `judge_pair(extraction_locator=True,
q3_04_timeout_360=True, max_tokens=2048)` dal codice locale congelato, con
adattatore di trasporto SSH auditabile verso `football-vps` e
`http://127.0.0.1:11434/api/chat`. L'adattatore trasmette il payload originale
via stdin e raccoglie localmente la risposta integrale prima di consegnarla
al caller; non modifica il contenuto restituito dal modello. Anche corpi di
errore HTTP e stderr vanno conservati prima della classificazione del caller.
Solo il trasporto HTTP gira sulla VPS; post-processing deterministico locale
tramite le funzioni già versionate, senza rieseguire suite.

Una sola richiesta POST, zero retry/repair/fallback; `temperature=0`,
`num_ctx=4096`, `num_predict=2048`, `think=false`, `stream=false`, timeout HTTP
360 s. Supervisione 450 s e kill-after 15 s, senza cambiare automaticamente
i limiti in caso di errore. Il supervisore deve vincolare il processo remoto,
non soltanto chiudere il client SSH; nessuna seconda chiamata per accertare
un esito ambiguo. Nessun download/installazione o caricamento C++ dal client.

Concorrenza: stesso lock condiviso storico
`/home/football/.local/share/football-data-lab/runtime-locks/spatial-v2-extraction-locator.lock`;
sola acquisizione esclusiva non bloccante del file esistente, durata dell'unica
operazione. Nessuna creazione directory/file lock, chmod o variazione di
servizi; se il lock manca, è occupato o non è utilizzabile, arresto.
L'uso del lock e l'esecuzione del trasporto remoto richiedono autorizzazione
esplicita insieme alla generazione. Artefatti e ledger del tentativo solo
locali, distinti e senza sovrascritture; nessuna scrittura allo staging VPS.

### Prerequisiti

1. Mandato distinto che autorizzi preparazione del driver, connessione SSH,
   diagnostica volatile minima, uso del lock esistente, conversione interna
   dello schema, caricamento Qwen e **una sola richiesta generativa**; raccolta
   locale e pubblicazione di report/evidenze/TODO/registro. Senza tale mandato
   nessuna di queste operazioni è autorizzata dal presente report.
2. Congelare driver e blob locali al commit prima della chiamata. Codice
   applicativo preso da `cec94e57ce11903460bc9314de2c699aa83b0193`, non dalla
   vecchia baseline 13814c2. Il successivo commit del driver non deve cambiare
   codice applicativo. Schema e handoff sono costruiti dal caller, non ricopiati
   o semplificati manualmente; conservare payload serializzato e hash.
3. Riutilizzare claim/evidence di
   `evaluation/runtime04_execution_01/artifacts/input.json`; Gold contradicted
   soltanto per il confronto successivo, mai nei messaggi inviati al modello.
4. Modello `qwen3.5:9b`, digest del manifest
   `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`.
   Prima della chiamata solo identità volatili GET version/tags/ps e stato
   concorrenza/lock necessari al nuovo tentativo: non ripetizione dei gate
   runtime-04 o della ricognizione. Versione diversa, digest diverso, tentativo
   locale già registrato o stato ambiguo implicano STOP senza correzione.
5. Autenticazione SSH e host key già autorizzate; verifica rigorosa della host
   key. Nessuna installazione di dipendenze o modifica del servizio.

### Evidenze attese e criteri

Conservare commit/blob/hash di caller, extraction, validatore e driver;
input, schema e payload integrali con hash; ledger locale scritto **prima**
dell'invio; contatore delle invocazioni POST, UTC/durate, exit SSH/supervisore,
HTTP status/errori, risposta grezza integrale, `done`, `done_reason`,
`prompt_eval_count`, `eval_count`, tempi quando forniti; estrazione, errori
shape/semantici, boundary, witness/validation/provenance quando raggiunti,
label proposta e osservata distinte, confronto col Gold, manifest finale.
Non chiamare `eval_count` numero di generazioni: è un conteggio di token
riportato dal servizio. Una chiamata inviata non prova da sola una generazione
completata. Se il trasporto si interrompe, registrare ciò che è noto e ignoto.

PASS/FAIL sono criteri dell'esperimento, non nuovi stati del progetto.

| Livello | PASS | FAIL | BLOCCATO |
|---|---|---|---|
| Tecnico API sul singolo payload | Una richiesta tracciata, risposta completa con stop, contenuto JSON conforme ai controlli strutturali del contratto invariato, nessun errore tecnico osservato | Rifiuto schema/HTTP, errore tecnico, timeout, length/incomplete, JSON o struttura invalidi; classificare precisamente, senza attribuire ogni errore al compilatore | Prerequisito/autorizzazione/identità/lock/ledger insufficiente prima dell'invio: nessuna richiesta |
| Ipotesi semantica q3_04 | Witness valido, validazione finale valida, label osservata contradicted e confronto Gold positivo | Label valida supported/insufficient oppure not_evaluable con reason/boundary; non trasformare il fail-closed corretto in successo generativo | Nessun risultato interpretabile per impedimento tecnico; accuratezza non dimostrata |
| Custodia/finalizzazione | Raw conservato, conteggi giustificati, manifest/hash completi e report verificabile | Evidenze alterate/mancanti o finalizzazione incompleta, da documentare senza ripetere la generazione | Impossibile ricostruire esito: nessuna conclusione favorevole e nessun nuovo invio |

Un arresto semantico può coesistere con un PASS tecnico API. Il PASS tecnico
vale solo per l'esercizio osservato del payload: non prova assenza di keyword
ignorate, corretto enforcement universale o compilazione isolata. Il confronto
semantico resta separato. `promotion_authorized=false` in ogni esito.

### Budget e condizioni di arresto

Riutilizzare 6.967 byte handoff, 7.311 user storico e 16.869 schema come dati
documentali, senza convertirli in token o sommarli come contesto effettivo.
Il budget esatto senza modello resta non verificato. Questa proposta accetta
esplicitamente di raccogliere contatori **durante una prova generativa**:
`prompt_eval_count` è il conteggio riportato per la richiesta processata, non
prova del prompt prima del troncamento, degli ID token o della conservazione
integrale del contesto. Un test positivo non colma queste lacune. Nessun
aumento automatico di contesto, riduzione schema o seconda richiesta.

STOP prima dell'invio a qualunque prerequisito fallito. Dopo invio o stato
ambiguo del tentativo, nessun retry, anche dopo timeout o disconnessione.
Una finalizzazione interrotta consente solo raccolta delle evidenze già
disponibili, senza nuova generazione. Dopo raccolta/report aggiornare TODO e
registro, pubblicare, verificare e fermarsi. Nessun altro caso o benchmark.

Restano non dimostrati: ABI/provenienza libreria, compatibilità completa di
tutti i costrutti, conteggio token pre-troncamento, assenza di context shift,
accuratezza generale delle contraddizioni, robustezza, integrazione e
certificazione. Un witness valido contradicted avvicinerebbe il Gate perché
fornirebbe la prima evidenza positiva su q3_04 col contratto aggiornato;
un errore delimiterebbe direttamente il blocco sul percorso reale. Nessuno
dei due esiti equivale al superamento del Gate RAG V5.

## Tracciamento e stato della presente sessione

Attività → letture Git/file e consultazione mirata delle due pagine API
ufficiali, senza script operativo → commit documentale → presente report →
selezione B e specifica dell'unica attività futura → decisione motivata →
analisi **ESEGUITO**, prossima attività **DA FARE**, esecuzione non autorizzata.
Il commit di pubblicazione è identificabile nella storia di questo file;
report, TODO ed Experiment Register sono pubblicati contestualmente.

Verifiche della sessione limitate a identità Git, custodia degli input citati,
perimetro del diff, riferimenti documentali e pubblicazione GitHub. Nessun
import applicativo, test, POST, accesso VPS, compilazione, linking, loading,
tokenizzazione o modello eseguito. Nessun codice/script operativo aggiunto.
Le indagini A si fermano finché non arrivano prove nuove concrete; il progetto
C++ rimane **BLOCCATO** senza diventare prerequisito per B. I risultati storici
rimangono validi nei rispettivi perimetri e non sono riscritti.
ABI, compatibilità backend completa, accuratezza generativa, Gate, integrazione
e certificazione **BLOCCATO**. Nessun runtime-05, staging, wrapper, merge o
deploy. STOP dopo pubblicazione documentale e verifica del working tree.
