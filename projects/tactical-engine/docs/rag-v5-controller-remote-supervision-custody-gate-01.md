# Gate remoto supervisione e custodia — 01

Data: 2026-11-19. Attività invariata:
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
Baseline: `6937df63f240a7a9a6949c29cc309bee95d5137c`.
Commit tecnico pubblicato prima di ogni accesso remoto:
`7a7bc6d34e58144ecc3e2001e1bfef084fe54f3a`.
Attempt ID esclusivo: `controller-remote-gate-20261119-01`.

**Risultato complessivo: ESEGUITO; gate BLOCCATO. Una sola invocazione remota,
zero retry, zero POST, zero caricamenti o generazioni. Nessuna correzione
successiva all'anomalia e nessuna ripetizione del gate.**

## Riconciliazione e flusso

TODO, Experiment Register, report di correzione locale, diagnosi timeout Gemma,
controller, supervisore, worker, observer e matrice delle nove fixture consultati.
HEAD locale/remoto uguali alla baseline, branch corretto e tree iniziale pulito;
nessun gate remoto equivalente pubblicato. Non rieseguite le nove fixture.

Attività → `operations/quality-first-pilot/controller_remote_gate_01.py`,
`remote_supervision_gate_01.py`, `remote_gate_synthetic_01.py` e supervisore
esistente → commit tecnico sopra → questo report → evidenze parziali e gate
BLOCCATO → fermarsi, correggere separatamente l'avvio Linux prima di un altro
tentativo → ESEGUITO, nessuna idoneità generativa o certificazione.

La nuova differenza tecnica, registrata prima dell'esecuzione in
`docs/controller-remote-gate-01/scope.md`, era Linux reale, gruppi/segnali,
clock reale, perdita SSH e custodia remota. Non altro benchmark dei modelli.

## Codice congelato e sicurezza

Il core `pilot_supervision_01.py` è byte-per-byte quello del commit `d4d2ee6`.
Nessun file applicativo o vecchio ledger è stato modificato.

| File trasferito | Byte | SHA-256 |
|---|---:|---|
|pilot_supervision_01.py|28517|0553498d3dea4ec32cff2a5f0a612f286ed26907d1cb22c66e2912d7942514a2|
|remote_supervision_gate_01.py|10285|0145b36e57933588d0579a9bab96e2926926c99163d87fd3943aaf43b74536fa|
|remote_gate_synthetic_01.py|1259|46a567d0098e95821b920985bd5a4cf0dc43179223054183793937b2062d8ee0|

Hash locali, dichiarazione installata e copie recuperate concordano. Script
controller locale e relativi hash/sintassi sono in `preparation.json`.
Il child sintetico non importa worker generativo, socket, HTTP, subprocess,
ctypes o codice RAG; un audit hook rifiuta socket/subprocess/exec/spawn/system.
Questo descrive il sorgente congelato, non una sandbox contro codice arbitrario.
Uniche richieste Ollama nei controlli: GET read-only `/api/ps`.
Nessuna POST, modello usato come simulatore o acquisizione del lock RAG.

Directory remota unica:
`/home/football/.local/share/football-data-lab/controller-remote-gate-20261119-01`.
Assente al preflight, creata con modo0700 e file esclusivi; conservata con le
prove dell'unico tentativo, non cancellata o resettata. Nessun servizio/daemon
installato. Nessuna scrittura applicativa o in staging/ledger precedenti.

Scenario predisposto: child NDJSON a4 sample/s, ignora TERM; relay opzionale
bloccato al terzo sample, taglio del solo SSH client, deadline propria e KILL.
Il timeout **sintetico** è12s, grace15s; deadline del pilot900s invariata. Il
mandato non richiedeva di aspettare900s per il child sintetico. Questa prova
non attesta una durata900s reale né la cancellazione di un'inferenza Ollama.

## Preflight osservato

SSH `football-vps` → football@163.5.26.155:22, BatchMode e verifica rigorosa
host key, nessuna accettazione automatica. ED25519 trusted:
`SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks`.

- MemAvailable16.024.403.968 byte, disco disponibile4.770.787.328 byte.
- `football-rag-api.service` user e `ollama.service` system: active.
- GET `/api/ps`: models vuoto; nessun runner, test concorrente o processo
  sintetico precedente rilevato. Destinazione assente.
- Verifica ripetuta immediatamente prima del child: servizi attivi e quiete.

Preflight VALIDATO nel perimetro osservato. Il ledger persistente locale è
stato creato prima dell'invocazione; nessun reset o ripresa consentiti.

## Sequenza effettiva e anomalia

Fonti originali in `evaluation/controller_remote_gate_01/`: invocazioni/exit,
raw stdout/stderr SSH, STOP originale, raccolta read-only e assessment.

| Evento remoto | Monotonic secondi | Evidenza |
|---|---:|---|
|Preflight iniziale|2168139.287901|preflight.json|
|Installazione sorgenti|2168140.067304|code-manifest.json|
|Sessione riservata|2168140.877541|session-started.json|
|Inizio supervisore|2168140.887438|supervisor-result.json|
|Deadline prevista|2168152.887438|supervisor-result.json|
|TERM gruppo child|2168152.888959|actions, delivery POSIX_process_group|
|KILL gruppo child|2168167.889206|actions, forced_kill=true|
|Cleanup registrato|2168169.099355|cleanup child/writer|
|Snapshot finale read-only|2168218.632373|anomaly-readonly.stdout.raw|

Ogni record originale conserva anche `utc_ns`; non sono state sottratte
origini monotonic fra PC e VPS. Localmente il client SSH è partito a21666.343
ed è stato terminato a21691.390: circa25.047s. Il coordinatore ha registrato
`E_NO_CUT_BARRIER`, non ha ricevuto READY durevole e **non ha inviato GO**.
Raw stdout e stderr SSH sono vuoti. Nessuna barriera `transport_cut_ready`:
il taglio controllato al terzo sample non è stato raggiunto. Il client è stato
terminato dal cleanup locale dopo il limite, non dalla barriera prevista;
`ssh-exit.json` conserva `intentionally_cut=false` e returncode locale1.

Il risultato remoto recuperato contiene:

- Supervisore PID/PGID243143; child PID/PGID243149; writer PID243148.
- `reason=E_CONTROLLER_DEADLINE`, `GO_sent=false`, `forced_kill=true`.
- Child returncode **-9** (SIGKILL); writer **-15** (terminato nel cleanup).
- Ritardo TERM rispetto deadline:0.001521s; TERM→KILL15.000247s.
- Cleanup a16.211916s dopo deadline, durata supervisore28.211916s.
- `custody_terminal_verified=false`, `writer_error=null`, terminal_event null.
- `relay_deliberately_blocked=false`: il ramo di backpressure previsto non
  è stato raggiunto e non può essere dichiarato verificato.

Il codice di uscita del parent remoto non è stato acquisito dopo la perdita
del client: non dedurlo dal return previsto nel sorgente. Il returncode del
client SSH non dimostra arresto di daemon o correttezza del protocollo.

La directory `custody` esiste ma è **vuota**: nessun journal, raw, checkpoint
oppure terminale. Non c'è una catena da verificare. È stato possibile recuperare
in sola lettura sei file (sorgenti, manifest, prenotazione e ricevuta del
supervisore), verificarne gli hash e conservare tutto in `recovered-partial`.
Questo è recupero parziale, non recupero completo della custodia.

## Analisi delimitata, senza nuovo esperimento

Fatti dimostrati: writer avviato e poi terminato senza creare journal; nessun
ack durevole per READY/GO; deadline e arresto del child continuano a funzionare;
nessun flusso sintetico persistito. Non è un fallimento Gemma/Qwen/Ollama.

Rischio statico specifico riscontrato:

1. `remote_supervision_gate_01.py:217,227-228` avvia il thread che esegue
   `sys.stdin.buffer.readline()` prima di `supervisor.run()`.
2. `pilot_supervision_01.py` sceglie fork su Linux e avvia il writer a300-302.
3. La Python installata3.12.3, letta senza compilare o avviare un altro child,
   chiama `multiprocessing.util._close_stdin()` nel bootstrap **prima** del
   target writer; `_close_stdin()` esegue `sys.stdin.close()`.
4. È quindi presente il rischio di ereditare nel fork il lock dello stdin
   buffered detenuto dall'altro thread. L'entry point preparato del pilot ha
   lo stesso ordine a642,657-658: non è una proprietà provata dalle fixture
   Windows che usano spawn e non esercitano quel reader remoto.

Questa spiegazione è coerente con writer bloccato prima di creare file e
assenza di eccezioni, ma **non è dimostrato lo stack effettivo del writer**:
era già terminato al recupero. Non attribuiamo con certezza il punto di blocco,
né un guasto di disco/fsync, rete o scheduling senza prova. Sorgenti stdlib e
inventario directory sono in `startup-static-readonly.stdout.raw`.

Delta minimo da sottoporre ad autorizzazione separata: eliminare l'ordine
fork-dopo-reader-buffered, avviando il processo di custodia prima di qualunque
thread di controllo che usa stdin, e preservare la prenotazione prima di GO.
Non basta allungare timeout o riavviare servizi. Nessuna correzione applicata
in questa sessione; nessuna nuova prova o indagine ABI proposta.

## Matrice comparativa e decisione

| Proprietà | Evidenza locale precedente | Evidenza Linux di questa sessione | Stato nel perimetro |
|---|---|---|---|
|Deadline monotonic|Clock simulato|12s reali, TERM circa1.5ms dopo deadline|VALIDATO sintetico|
|TERM/KILL e grace|TERM ignorato iniettato|Process group reale, grace15.000247s, child -9|VALIDATO sintetico|
|Cleanup|Child/writer simulati reaped|Child/writer non vivi e quiete finale|VALIDATO sintetico|
|Fsync-before-GO|Prenotazione simulata|GO non inviato in assenza di custodia|BLOCCATO percorso positivo; fail-closed osservato|
|Journal e checkpoint|Catena simulata verificata|Directory vuota|BLOCCATO|
|Indipendenza da relay bloccato|Sink simulato|Barriera non raggiunta|BLOCCATO|
|Perdita SSH e journal continuo|Consumo locale sospeso simulato|Nessun journal; taglio previsto non raggiunto|BLOCCATO|
|Recupero completo|Export/import simulato|Solo sorgenti/manifest/ricevuta recuperati|BLOCCATO|
|Cancellazione inferenza Ollama|Non verificata|Nessuna inferenza permessa o eseguita|BLOCCATO|

Le nove fixture storiche rimangono valide nel proprio perimetro; non erano
una certificazione dell'avvio Linux e non vengono riscritte retroattivamente.
Il gate complessivo resta **BLOCCATO**: i PASS parziali di supervisione non
compensano la mancanza di custodia. Nessuna nuova generazione preparata.

## Stato finale e conservazione

Snapshot finale: RAG e Ollama active, `/api/ps` vuoto, nessun runner, test
concorrente o processo dell'attempt residuo. MemAvailable16.038.567.936 byte.
Non sono state necessarie ulteriori terminazioni remote dopo il cleanup
registrato; nessun killall/pkill, riavvio, acquisizione lock o modifica servizi.
Cinque connessioni SSH: preflight, trasferimento, unico run, recupero parziale
read-only, lettura statica mirata post-anomalia. Le ultime due non avviano il
worker e non ripetono il test. La raccolta è limitata all'attempt e al bootstrap
stdlib pertinente. Originali di questa sessione e storici conservati.

Inventario SHA-256 e dimensioni di33 file in
`evaluation/controller_remote_gate_01/inventory.json`; matrice macchina e
calcoli in `assessment.json`. STOP originale lasciato invariato.
Report, TODO e Experiment Register pubblicati contestualmente; verifica GitHub
e tree finale richiesta prima della consegna. Il commit documentale è quello
che introduce questo report, restituito dopo la verifica di pubblicazione.

**STOP. Nessuna inferenza, altro tentativo, patch automatica, merge o deploy.**
