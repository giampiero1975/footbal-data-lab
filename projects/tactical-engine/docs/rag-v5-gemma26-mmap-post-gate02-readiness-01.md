# Readiness Gemma26 mmap dopo Gate02 — 01

Data: 2026-11-19. Attività invariata:
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
Baseline GitHub/locale: `12a6c113757bbe5531b28f1516fee5d1bad332e0`.
Commit delle evidenze di sola ispezione:
`b8008a2368c5f6c48f0321124dffd1dc7bfc5fc0`.

**Readiness documentale ESEGUITO / VALIDATO nel perimetro statico.**
Proposta congelata di un unico eventuale tentativo; esecuzione BLOCCATO fino
ad autorizzazione esplicita e nuovo binding/launcher esclusivo. Nessuna SSH,
POST, inferenza, caricamento, download o suite ripetuta in questa sessione.

## Riconciliazione e motivazione del nuovo eventuale tentativo

Consultati TODO, Experiment Register, report Gate02, report Gemma mmap01,
manifest, codice e ledger storici. Branch corretto, HEAD remoto/locale uguali
alla baseline e working tree iniziale pulito. Nessun tentativo Gemma mmap02
registrato; nessuna attività/campagna nuova creata.

Il Gemma mmap01 aveva una sola POST, HTTP200,707 chunk di thinking parziale e
nessun finale Ollama. Il minimo RAM osservato6156517376 byte riguarda soltanto
il tratto campionato; non dimostra sostenibilità per900s o qualità tattica.
La raccolta era terminata E_DEADLINE_AMBIGUOUS con evidenze mancanti.

Una futura prova non duplicherà lo stesso esperimento a codice invariato:
la differenza è il controller corretto, la deadline indipendente dall'I/O,
la custodia remota durevole e il recupero dopo perdita SSH. Il payload resta
identico. Gate02 ha verificato queste proprietà con un child sintetico su Linux,
non una generazione. Nessuna nuova indagine ABI, suite o gate equivalente richiesti.

Flusso: Attività → `inspect_gemma_mmap_readiness_01.py` (legge solo file
versionati, non importa il pilot) → commit evidenze sopra → questo report →
payload congelato e percorso verificato staticamente → proposta singola
subordinata ad autorizzazione → readiness documentale VALIDATO; runtime BLOCCATO.

## Percorso reale verificato e limiti

`gemma_mmap_on_01.py` storico delega a `paired_pilot_01.one_remote()`.
Quest'ultimo trasmette il core corrente e il worker congelato; bootstrap chiama
`pilot_supervision_01.remote_entry()`; `Supervisor` avvia GNU timeout900s,
kill-after15s e Python worker. Il worker controlla parent timeout e PGID prima
anche solo di READY (`paired_pilot_remote_01.py:157-167`). Non è collegato al
worker sintetico del Gate02 e non usa un percorso alternativo di generazione.

Il core corrente ha SHA-256
`bf53dd27695a0d743add0835cc7252128cfff24568b87f89d8a48e83fa20ffe3`,
identico al40590ee e a quello trasferito nel Gate02. Hash completi di controller,
core, worker, wrapper e observer in `facts.json`; inventario input in `inputs.json`.

| Requisito | Evidenza nel codice / precedente | Conclusione |
|---|---|---|
|Writer prima dei thread|Supervisor409-428 attende ack0; remote_entry696-703 crea relay/reader solo nel callback|Verificato staticamente; core VALIDATO sintetico Linux|
|READY durevole e prenotazione prima di GO|Core ack eventi, reserve_before_GO, conferma prima di outgoing GO a520-531; Gate02 seq5<6<8|Verificato; non una nuova POST|
|900s assoluti / grace15s|Core deadline monotonic, remote_entry GNU timeout900s/15s; HTTP timeout900 nel worker198|Invariati; nessun reset sui chunk|
|Riserva RAM4.000.000.000 byte|pressure_step108-129, prima della POST e nel monitor|Invariata|
|Paging persistente|64MiB/s per5s con RAM<6.000.000.000 byte; contatori globali, non attribuzione al modello|Invariato|
|Guardia prima del logging|guard_then_emit e cancel_without_logging prima dell'emissione diagnostica|Verificato staticamente|
|EOF non implica arresto Ollama|Core E_TRANSPORT_EOF; flag remote_cancellation_verified solo se esplicito; wrapper error/STOP|EOF o assenza prove non costituiscono PASS|
|Finale tardivo|Deadline ricontrollata prima di accettare il completamento|BLOCCATO anche con testo successivamente recuperato|
|Custodia locale e remota|one_remote richiede terminale locale e supervisor_terminal remoto ok con custodia verificata|Mancanze causano arresto|
|Quiete positiva|Worker richiede ps vuoto, nessun runner, servizi attivi e invarianti lock prima di finished ok|Necessaria; non provata dal Gate02 per una vera inferenza|

`one_remote()` non tratta un EOF o una terminazione SSH come prova di
cancellazione del daemon. Su errore/abort il worker emette
remote_cancellation_verified=false; il caller arresta il flusso, senza retry.
Tuttavia il percorso d'errore non fornisce automaticamente una fotografia
post-STOP completa di Ollama. È un limite già aperto, non una cancellazione
VALIDATO: il protocollo sotto richiede raccolta read-only esplicita e mantiene
BLOCCATO il risultato se la prova manca. Non modificato codice in questa sessione.

Il launcher storico non è riutilizzabile: vecchi hash autorizzativi, binding
privo dell'autorizzazione alla nuova custodia e ledger01 già esistente provocano
arresto sicuro. Non vanno aggiornati o resettati per simulare una nuova
esecuzione. Serve un nuovo wrapper singolo e binding congelato, con consenso
esplicito: non il comando execute del pilot completo a sei slot.

Nel perimetro esaminato non è stato individuato un nuovo difetto concreto
che richieda una patch automatica. Non sono dichiarate INTEGRATO o CERTIFICATO
la catena generativa o la cancellazione reale di Ollama.

## Payload congelato, identico allo storico

File preparatorio: `docs/gemma26-mmap-post-gate02-readiness-01/payload.frozen.json`.
6211 byte, SHA-256:
`7bc057b52a120ebbc5415ebd22da236f66fd1240421f4b114fcde629a6de97ce`.
Identico all'oggetto payload in `evaluation/gemma_mmap_on_01/call-01/request.json`
e al caso Gemma V10-02 del manifest aggiungendo la sola opzione mmap già storica.
Domanda/fonti/system message invariati; nessuna risposta storica, Gold o repair
aggiunti. Il file preparatorio non è un ledger esecutivo o un'autorizzazione.

| Parametro | Valore congelato |
|---|---|
|Caso / ordinal|V10-02 /1|
|Modello|gemma4:26b, Gemma4 26B-A4B, Q4_K_M|
|Digest storico atteso|001e5dafc3c77684c2307ebc6ab8e336e10c9b18eca52acf547d72fc83c3ca8c|
|use_mmap|true|
|num_ctx / num_predict|8192 /4096|
|Thinking|true|
|Seed|42|
|Sampling|temperature1.0, top_p0.95, top_k64|
|stream / keep_alive|true /0|
|Retry / repair / fallback|0 /0 /0|
|Timeout assoluto / grace|900s /15s|
|Riserva RAM|4.000.000.000 byte|
|Paging|64MiB/s per5s con available<6.000.000.000 byte|
|promotion_authorized|false|

Draft non è impostato nel payload. Lo storico documenta il default runner
`draft-mtp` con3, parallel1 e batch/ubatch1024. La proposta non aggiunge né
modifica opzioni draft e non assume che il default attuale sia già attestato.
Versione/configurazione osservabili dovranno concordare con lo storico prima
dell'eventuale invio; se non verificabili, registrarne il limite e fermarsi,
non forzare opzioni nuove. I6211 byte non sono convertiti in token.

## Prerequisiti all'unica eventuale POST

Ordine obbligatorio, senza operazioni eseguite qui:

1. Autorizzazione esplicita a un solo caso Gemma mmap, nessun altro slot.
   Proposta ID `gemma-mmap-on-02`, ledger `evaluation/gemma_mmap_on_02`,
   custodia `gemma-mmap-on-02-call-01` sotto runtime-evidence. Solo nomi proposti:
   non create directory locali/remoti di esecuzione; assenza da verificare
   atomicamente nel nuovo launcher. Mai riutilizzare01 o altri attempt.
2. Congelare/pubblicare launcher singolo, commit/blob/hash, binding e consenso
   nuovi; stessi controller/core/worker ispezionati, payload hash sopra,
   autorizzazione esplicita alla custodia remota esclusiva e ledger persistente.
3. Preflight volatile minimo con SSH rigoroso: host key nota ED25519,
   versione Ollama storica0.40.5, tag/digest/Q4_K_M/template e profili coerenti;
   servizi RAG/Ollama active, ps vuoto, nessun runner/test concorrente,
   memoria>=4GB e disco sufficiente. Non usare lo snapshot Gate02 come stato attuale.
4. Lock condiviso già esistente: identità/permessi/symlink corretti e acquisizione
   esclusiva non bloccante da parte del solo worker autorizzato. Nessuna creazione
   o modifica del lock, nessuna attesa o installazione per aggirare un prerequisito.
5. Writer confermato, journal/raw/checkpoint0, READY con payload/model binding,
   prenotazioni durevoli locali/remota, quindi una sola GO e una sola POST loopback.
   Qualsiasi barriera mancante impedisce invio. Se inviata o stato ambiguo,
   il tentativo è consumato anche con timeout o dati incompleti.

## Protocollo di raccolta e classificazione

| Livello | Evidenza da conservare | Quando è insufficiente |
|---|---|---|
|HTTP e stream|post_started, contatore1, status/header e raw NDJSON sequenziato|HTTP200 o thinking parziale da soli non bastano|
|Finale Ollama|done=true, done_reason=stop, contenuto finale non vuoto, metadata/counts|EOF senza done, errori, limite token o finale tardivo: BLOCCATO|
|Supervisore e custodia|Termine entro deadline, exit, manifest/hash/raw/checkpoint/terminale e ricevuta cleanup|SSH exit da solo o terminale mancante: BLOCCATO|
|Quiete e cancellazione|Socket/shutdown/abort registrati; fotografia read-only ps, runner/processi, servizi e memoria post-STOP|Shutdown socket o quiete osservata non provano automaticamente causalità della cancellazione|
|RAM e paging|Campioni monotonic, riserva rispettata e nessun abort/paging persistente|Qualsiasi soglia violata: arresto/BLOCCATO anche con risposta valida|

**PASS tecnico proposto** solo se tutte le evidenze necessarie sono presenti:
una POST, risposta completa entro900s, nessun abort, raw/custodia integri,
quiete finale comprovata e servizi preservati. Conservare anche la politica
deterministica già esistente: eval_count in1..4096, prompt_eval_count in1..4096
entro il contesto8192; nessuna variazione del tetto per recuperare un risultato.
PASS è criterio di accettazione, lo stato ufficiale sarebbe VALIDATO nel solo
perimetro tecnico del caso. Non dimostra il punteggio tattico28/30 o il Gate RAG.

**BLOCCATO/arresto** per prerequisiti mancanti, barriera non confermata, timeout,
HTTP rejection, EOF, risposta parziale, finale oltre deadline, custodia incompleta,
violazione RAM/paging o quiete non attestata. Conservare tutti i raw e l'errore
originale; nessun retry, repair, rigenerazione o chiamata ad altro modello.
Dopo STOP è necessaria una raccolta diagnostica read-only separata dall'invio
(GET ps, processi e servizi, senza POST o cambiamenti). Se non ottenibile,
cancellazione/quiete non verificate e risultato BLOCCATO. Se la sola quiete è
osservata ma manca prova dell'effettiva cancellazione, riportare i due fatti
separatamente senza promuovere il tentativo interrotto.

In assenza di quiete, nessun nuovo invio, unload forzato, kill indiscriminato,
restart o modifica di configurazione è implicitamente autorizzato. Il protocollo
non promette che uccidere il client/worker termini il daemon o l'inferenza.

## Rischi residui e decisione

Non verificabili qui: comportamento HTTP/cancellazione reale Ollama, completamento
Gemma entro budget, RAM/paging lungo l'intera generazione, applicazione effettiva
mmap/thinking/draft, contatori token e possibile troncamento, qualità tattica.
Il file del modello non equivale al working set RAM. Gate02 non risolve questi
punti e non va ripetuto per dimostrarli. Limiti del tokenizer/backend restano
espliciti senza riaprire ABI o proporre nuove infrastrutture.

Proposta: **un unico eventuale Gemma26 mmap / V10-02**, stesso payload e vincoli,
con controller corretto; autorizzazione distinta ancora necessaria. Preparazione
documentale conclusa, codice esecutivo storico non riabilitato e nuova prova
non autorizzata (`authorization=false`, `launchable_now=false` nei facts).
Nessuna nuova generazione Qwen/Gemma o campagna predisposta automaticamente.

Report/TODO/Experiment Register contestuali, evidenze congelate in b8008a2;
commit documentale e pubblicazione verificati alla consegna. Accuratezza,
Gate RAG V5, integrazione/certificazione e cancellazione reale restano BLOCCATO.
**STOP dopo il report. Zero SSH, POST, inferenze o cambiamenti VPS/RAG.**
