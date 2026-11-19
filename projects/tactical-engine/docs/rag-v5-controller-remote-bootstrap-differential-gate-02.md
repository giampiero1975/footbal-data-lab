# Gate remoto differenziale bootstrap writer — 02

Data: 2026-11-19. Attività esistente:
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
Baseline: `e8cf22c2391e64deb9d5e228a91221f4cee64ba4`.
Commit tecnico pubblicato prima di SSH:
`ed770b7c4ec711eb38b5b4f2789aee6e8cd290cc`.
Attempt ID: `controller-remote-gate-20261119-02`.

**ESEGUITO una sola volta; VALIDATO esclusivamente nel perimetro sintetico Linux.
Una sola GO al child sintetico, zero POST, modelli caricati o inferenze.**
Il precedente attempt01 resta immutato e BLOCCATO.

## Riconciliazione e delta registrato

TODO e Experiment Register ufficiali, report gate01, report correzione bootstrap,
core, commit e manifest precedenti riconciliati. Branch corretto, HEAD locale e
GitHub uguali alla baseline, working tree iniziale pulito. Nessuna precedente
esecuzione equivalente con core corretto; nuovo ledger02 assente. Non ripetute
le nove fixture, prove semantiche, benchmark o ricognizioni.

Attività → controller_remote_gate_01.py / remote_supervision_gate_01.py /
remote_gate_synthetic_01.py e core40590ee → commit tecnico sopra → questo report
→ recupero integro con tutti i21 criteri veri → blocco bootstrap/custodia
superato nel perimetro sintetico → VALIDATO sintetico; generazione BLOCCATO.

Delta documentato prima dell'esecuzione in `docs/controller-remote-gate-02/scope.md`:
writer e journal/raw/checkpoint0 inizializzati e confermati prima di reader e
relay. Il core è **byte-identico** a40590ee; nessuna nuova patch durante il gate.
Soli ulteriori adattamenti: ID/percorso esclusivi02, diagnostica versione Python,
traccia ack prima dei thread, legame fra cut e sample già persistito e controlli
di sequenza nel recupero. Preflight considera anche altri attempt sintetici.

Evidenze di deadline, TERM/KILL e cleanup Linux del gate01 riutilizzate come
precedenti: nessuno scenario separato aggiunto per riprovarle. Nel presente
scenario rimangono gli stessi vincoli di chiusura: timeout sintetico12s,
grace15s, lateness<=0.5s, cleanup entro deadline+18s. Produzione900s e soglie
RAM/paging immutate; nessun aggiustamento per ottenere PASS.

## Preflight e identità

SSH football-vps → football@163.5.26.155:22, BatchMode, StrictHostKeyChecking=yes,
UpdateHostKeys=no, host ED25519 trusted
`SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks`.
Python Linux effettiva3.12.3, GCC13.3.0, versione completa nei raw.
Destinazione assente al preflight, poi directory privata0700 esclusiva:
`/home/football/.local/share/football-data-lab/controller-remote-gate-20261119-02`.

MemAvailable16.026.198.016 byte; disco disponibile4.770.603.008 byte.
RAG user `football-rag-api.service` e system `ollama.service` active.
GET `/api/ps` vuoto; nessun runner, test concorrente o processo sintetico
precedente. Controlli di quiete ripetuti immediatamente prima del child.
Il manifest installato conferma i byte locali; sorgenti verificati di nuovo
all'avvio e prima del recupero.

| Sorgente trasferito | Byte | SHA-256 |
|---|---:|---|
|pilot_supervision_01.py|30916|bf53dd27695a0d743add0835cc7252128cfff24568b87f89d8a48e83fa20ffe3|
|remote_supervision_gate_01.py|10844|ed594822a51221dbf024db00065681096bb7cf281eab2bc002fd80835619090f|
|remote_gate_synthetic_01.py|1259|46a567d0098e95821b920985bd5a4cf0dc43179223054183793937b2062d8ee0|

Il child congelato produce soltanto NDJSON e rifiuta socket/subprocess/exec/
spawn/system via audit hook. Nessun worker generativo trasferito/importato,
nessun lock RAG, servizio, corpus, modello o configurazione modificati.
Uniche interrogazioni Ollama: GET read-only `/api/ps`.

## Evidenze del bootstrap e timeline remota

Originali: `evaluation/controller_remote_gate_02/`.
`timeline.json` conserva selezione di record, hash, monotonic e UTC effettivi.

| Evento | Seq journal | Monotonic remoto |
|---|---:|---:|
|custody_ready, record iniziale|0|2169768.328756011|
|Ack verificato, relay ancora assente|2, timestamp nel payload|2169768.332804848|
|Reader/relay avviati dopo ack|3, timestamp nel payload|2169768.333400973|
|Lancio child|1|2169768.334247173|
|READY child registrato|5|2169768.365844127|
|Prenotazione fsynced prima di GO|6|2169768.371083921|
|Unica GO inviata al child|8|2169768.448148347|
|Terzo sample già persistito|14|2169768.951980524|
|Barriera cut emessa dal relay|riferimento al sample14|2169768.957317843|
|Trasporto EOF registrato|16|2169769.003608314|
|Ultimo sample, indice107|227|2169795.224717622|
|Terminale della custodia|230|2169795.337184543|

Le note del callback vengono accodate e riversate nel journal dopo launch:
per l'ordine reale ack→thread→child si usano i timestamp originali nei payload
più il legame SHA dell'ack0/checkpoint0, non l'ordine di append delle note.
Il writer conferma solo dopo fsync dei file e del checkpoint. Il callback
registrato contiene ack kind custody_ready, sequence0 e hash
`2470033a1191b4f625168ce172f5b92cde4daa124ffbaa72b17c916e47cb27d3`.

Il client ha ricevuto READY con hash del child atteso, persistito la propria
prenotazione e inviato una sola autorizzazione. Il supervisore remoto ha inviato
la sola GO effettiva al child dopo il proprio reserve_before_GO durevole.
`transport-cut.json` collega barriera al sample indice2 e al suo timestamp;
il sample corrispondente è nel journal alla sequenza14, già acked prima del relay.
Il client ha terminato esclusivamente il proprio processo SSH PID19764;
`ssh-exit.json` conserva intentionally_cut=true, returncode locale1.
Questo codice di uscita è l'interruzione voluta, non un errore del modello.

Dopo EOF16 il journal continua fino al sample107 e al terminale230;108 sample
con indici0–107 senza buchi,231 record con sequenze0–230 e catena integra.
Il relay è rimasto deliberatamente bloccato; il controllo e la custodia hanno
continuato indipendentemente da quel thread e dal canale SSH chiuso.
Non sono sottratti clock monotonic o wall-clock di macchine diverse.

## Chiusura e recupero read-only

Supervisore PID/PGID243555; writer243558; child PID/PGID243563.
TERM alla deadline+0.000899s, KILL15.002306s dopo TERM; child returncode-9.
Writer exit0, cleanup a15.023954s dopo deadline, nessun child/writer vivo.
Questi valori sono controlli di consistenza nel singolo scenario, non nuove
prove autonome di caratteristiche già documentate dal gate01.

Il child sintetico ignora TERM per esercitare la chiusura prevista: il risultato
del supervisore riporta coerentemente `reason=E_CONTROLLER_DEADLINE`, `ok=false`
e terminal_event null. **Questo non è un output modello riuscito**. Il successo
del gate riguarda la gestione attesa di tale arresto e la custodia completa:
`terminal.json` è presente, hash/catena verificati e
`custody_terminal_verified=true`. Terminale di custodia e finale del child
sono distinti. `promotion_authorized=false`, cancellazione Ollama false.

Una sola connessione successiva di recupero, senza rilancio o GO. Export remoto
verifica sorgenti e custodia; import locale esclusivo riverifica sequenze,
checkpoint, terminale, hash e concatenazione dei raw. Ricevuta post-cleanup
`remote-supervisor-result.json` presente e integra; è stata prodotta usando
spawn anche su Linux dopo l'avvio dei thread, senza riprodurre il vecchio fork.

| Artefatto | SHA-256 verificato |
|---|---|
|journal.ndjson|a0d6e1e4bb57a1f3f4a0ecb6ebdc0112f35d33651249e00484b19f360e777a66|
|stdout.raw|d4569be83315b336fb4a92dd605be473bb32304f53499df90b5f4515813522b7|
|stderr.raw, vuoto|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855|
|Catena finale|7be97a2f82f777b8ac5654230078299049021317592a60d28a515afbbebe43b7|

Inventario con dimensioni/SHA-256 di40 file in `inventory.json`. Raw e messaggi
originali sono conservati; nessuna riscrittura per cambiare l'esito. Quattro
connessioni SSH (preflight, trasferimento, unico run, recupero), una sola
esecuzione sintetica e nessun retry. Nessuna anomalia osservata.

## Matrice finale e decisione

| Requisito rimasto aperto | Esito osservato | Stato |
|---|---|---|
|Writer Linux inizializzato prima dei reader|Record0/checkpoint0/ack, callback successivo|VALIDATO sintetico|
|READY e prenotazione prima di GO|Sequenze5<6<8, una sola GO|VALIDATO sintetico|
|Barriera durevole e cut SSH raggiunto|Sample14 correlato e intentionally_cut=true|VALIDATO sintetico|
|Custodia dopo disconnessione e relay bloccato|EOF16, sample fino227, terminale230|VALIDATO sintetico|
|Recupero completo con hash/checkpoint/terminale|Export/import verificati,231 record,108 sample|VALIDATO sintetico|
|Terminazione, cleanup e quiete|Child/writer reaped, nessun processo sintetico residuo|VALIDATO sintetico|
|Servizi preservati|RAG/Ollama active, ps vuoto, nessun runner/concorrenza|VALIDATO osservato|
|Cancellazione effettiva inferenza Ollama|Nessuna inferenza autorizzata/eseguita|BLOCCATO, fuori prova|
|Qualità tattica, accuratezza, Gate RAG V5|Nessuna nuova evidenza generativa|BLOCCATO|

Snapshot finale: MemAvailable16.042.024.960 byte, servizi active, nessun modello
residente, runner o processo dell'attempt. Directory02 conservata come evidenza;
nessun reset/cancellazione/riutilizzo dell'attempt01. Storici e RAG immutati.

Il blocco specifico di bootstrap/custodia è superato nel perimetro sintetico:
non serve ripetere un gate equivalente per le stesse proprietà. Non è provata
la causa esatta del vecchio blocco né l'integrazione generativa completa del
pilot. Il core reale è identico a quello sottoposto alla prova sintetica, ma
nessuna inferenza o capacità di cancellazione del daemon è certificata.
Eventuale singola generazione Gemma26 o Qwen27 richiede autorizzazione distinta;
non viene preparata o avviata automaticamente. Nessuna nuova campagna proposta.

Report, TODO e Experiment Register pubblicati nella stessa sessione, con
verifica GitHub e working tree finale pulito. Il commit documentale è quello
che introduce questo report, restituito dopo la verifica. **STOP.**
