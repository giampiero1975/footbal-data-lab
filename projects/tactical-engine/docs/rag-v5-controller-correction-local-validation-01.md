# Correzione controller e validazione locale — 01

Data: 2026-11-19. Attività esistente: `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
Baseline riconciliata con GitHub: `3f5b4f3da10c5275685c4bf589f1560ccb4adcae`.
Branch: `codex/tactical-state-contract-v1`. Commit tecnico:
`d4d2ee6752c74278fe718a73163ee1e4370246a9`.

## Mandato e risultato

Attività → controller/worker/observer esistenti e modulo condiviso
`operations/quality-first-pilot/pilot_supervision_01.py` → commit tecnico sopra
→ questo report → nove fixture locali PASS → correzione IMPLEMENTATO,
fixture ESEGUITO / VALIDATO esclusivamente nel perimetro simulato.
Idoneità reale VPS e nuove inferenze BLOCCATO. Nessuna nuova attività/campagna.

Prima delle modifiche sono stati riconciliati TODO, registro, diagnosi timeout,
report Gemma mmap, controller/worker/observer/wrapper e ledger precedenti.
HEAD locale/remoto uguali alla baseline, tree iniziale pulito; nessuna correzione
equivalente completata. La differenza tecnica era registrata prima delle fixture
in `controller-correction-local-01/scope.md`: separare controllo e persistenza,
aggiungere custodia indipendente e finalizzazione verificabile. Non è stato
ripetuto alcun benchmark o suite storica (32/17 e suite semantiche incluse).

## Delta tecnico rispetto al controller originale

- `paired_pilot_01.py`: sostituito il loop che serializzava lettura e fsync con
  `Supervisor`. Trasporto SSH rigoroso conservato; bootstrap via stdin per non
  superare i limiti della command line Windows. Risultato accettabile soltanto
  con terminale locale durevole e terminale del supervisore remoto verificato.
- `pilot_supervision_01.py`: processo separato per persistenza; code limitate
  (64 record, sender 2), limite journal 64 MiB / 10.000 record. Overflow o errore
  di custodia interrompono il tentativo. Il loop di sicurezza non scrive file,
  stdout o fsync mentre il child è attivo. La prenotazione deve essere fsynced
  e confermata prima di GO. Nessun retry o secondo GO.
- Il watchdog usa deadline monotonic assoluta 900s, non rinnovata dai chunk;
  ricontrolla la deadline prima di GO e prima di accettare il terminale.
  TERM e KILL dopo grace 15s sono registrati con clock, PID/PGID e return code.
  Reader, writer, join e raccolta hanno attese limitate. Le scritture esclusive
  esterne al loop usano un processo terminabile con budget 15s.
- `paired_pilot_remote_01.py`: emissione su coda non bloccante; guardia RAM/
  paging e shutdown socket precedono l'emissione diagnostica. Errori del sink
  richiedono arresto, non possono produrre successo. Il corpo `pressure_step`
  è identico per AST alla baseline; soglie 4GB, 64MiB/s per5s e condizione RAM
  associata invariate. Callsite POST, input, modello e opzioni invariati.
- Custodia remota solo predisposta: directory privata esclusiva per attempt ID
  sotto `/home/football/.local/share/football-data-lab/runtime-evidence`, raw
  stdout/stderr, journal append-only sequenziato e concatenato SHA-256,
  checkpoint, terminale. Nessun daemon/servizio. Supervisore con SIGHUP ignorato
  e deadline propria; worker ancora sotto GNU timeout900s/kill-after15s.
  Binding senza autorizzazione esplicita alla custodia remota rifiutato prima
  della connessione: nessuna scrittura remota è autorizzata dalla preparazione.
- Recupero: `remote_recovery_command()` prepara argv SSH rigoroso e stdin per
  esportazione read-only; non esegue nulla. `export_custody()` / `import_custody()`
  verificano hash, sequenze, checkpoint, raw e contenuto del terminale legato
  alla catena. Importazione locale esclusiva, nessuna riscrittura del ledger.
  Terminale assente/non integro non diventa PASS; copie parziali restano evidenze.
- `gemma_mmap_observation_01.py` e `gemma_mmap_on_01.py`: observer opzionale con
  budget monotonic condiviso e risultato separato, errori/exit strutturati;
  problemi observer non sovrascrivono lo STOP primario. Le mappe vengono
  riosservate finché accessibili; accessi negati sono registrati. Il vecchio
  journal finale non è usato come prova di osservazione continua.
- Manifest preparatorio: aggiornati esclusivamente hash del codice e relativi
  riferimenti pending; aggiunto hash del modulo condiviso. Sei payload, input,
  limiti e profili identici. Autorizzazione pending resta falsa; autorizzazioni
  storiche non modificate e non riutilizzabili sul nuovo codice.

La soluzione è condivisa dai componenti esistenti; non introduce un secondo
percorso di generazione o dipendenze applicative. Gold, RAG, corpus, panel,
configurazioni e artefatti runtime storici non modificati.

## Nove fixture: matrice di accettazione

Script: `operations/quality-first-pilot/controller_local_fixtures_01.py`.
Child sintetico: `controller_fixture_worker_01.py`. Solo processi Python locali,
stream sintetici, clock controllati e sink locali; nessun HTTP/SSH/modello.
Matrice macchina: `controller-correction-local-01/fixture-matrix.json`.

| N | Scenario autorizzato | Evidenza / criterio | Esito ultimo |
|---|---|---|---|
|1|NDJSON frammentato|Raw identico allo spool indipendente, sequenze e terminale verificati, una prenotazione durevole|PASS|
|2|Output continuo oltre deadline|Arresto E_CONTROLLER_DEADLINE nonostante traffico, nessun retry|PASS|
|3|Stdout bloccato e soglia RAM|Cancellazione E_MEMORY_RESERVE mentre il sink è ancora bloccato|PASS|
|4|Writer fermo / eccezione|Due varianti: deadline o E_CUSTODY_IO, nessun PASS senza terminale, cleanup child/writer e raw indipendente conservati|PASS run02|
|5|Terminale tardivo|Raw/terminale conservati ma deadline prevale, nessuna promozione|PASS|
|6|Consumo sospeso / EOF|Journal continua indipendente dal relay; export/import integro, una sola GO, EOF classificato trasporto; terminale alterato rifiutato|PASS run03|
|7|TERM ignorato|TERM/KILL, forced_kill, exit e cleanup registrati; cancellazione daemon non inventata|PASS|
|8|Clock civile / observer opzionale|Monotonic invariato, errore observer tipizzato, STOP primario immutato|PASS|
|9|Guardie e sink bloccato|Pagine isolate consentite; soglie memoria/paging invariate e azione prima della telemetria|PASS|

Sono conservate 12 esecuzioni di fixture per nove scenari: nessun fallimento
nascosto. La prima esecuzione della4 si è fermata perché il clock fittizio
avanzava a901 ma non attraversava il termine della grace. I soli processi
sintetici identificati (PID4044 e2096) sono stati chiusi; raw incompleto e
risultato FAIL restano in run01. Corretto il solo avanzamento della fixture
(a917), run02 PASS. Non sono stati cambiati timeout o grace del controller.
La6 è stata estesa due volte nello stesso criterio: export/import preparato,
poi legame semantico terminale/journal e rejection di copia alterata. Run01/02
restano disponibili, ultimo run03 PASS. Nessun altro scenario è stato ripetuto.

Gli hash per ogni esecuzione documentano il codice allora usato. Le modifiche
successive riguardano verifica read-only del recupero e hash del manifest,
non il loop di supervisione; la6 copre il delta e sono stati riverificati i14
terminali integri già prodotti. La copia intenzionalmente alterata e le
custodie incomplete della4 sono escluse da quel conteggio e restano pubblicate.

Verifiche statiche: sintassi dei sette file Python nuovi/modificati e del corpo
observer incorporato; identità payload/input/limiti; AST pressure_step invariato;
`git diff --check`. Evidenze in `static-delta.json`. Inventario con dimensioni e
SHA-256 di149 file in `inventory.json`, incluso il primo tentativo interrotto.

## Limiti e requisiti remoti non verificati

1. Le fixture Windows non provano killpg, GNU timeout, sopravvivenza a HUP o
   custodia su filesystem VPS. La7 inietta esplicitamente TERM ignorato; PGID
   locale è null e Windows termina il child, non attesta un process group Linux.
2. La simulazione del sink/fsync fermo non è un blocco reale del filesystem.
   I clock accelerati verificano precedenze e deadline, non900s di latenza reale,
   sospensione OS o garanzie hard real-time. Loop e cleanup hanno budget finiti;
   un kernel che non schedula il processo resta fuori da una garanzia Python.
3. Il terminale journal registra la fase pre-cleanup; il risultato del supervisore
   contiene il cleanup successivo (PID writer/exit/child_alive). Non trattare il
   solo terminale, prima della ricevuta finale, come prova di tutti i join.
   Se manca la ricevuta remota, il risultato reale rimane non verificato.
4. Un filesystem guasto non può garantire il proprio terminale. In quel caso
   la variante4 conserva raw indipendente e risultato del controller, segnala
   custodia incompleta, non inventa finalizzazione completa.
5. Nessun segnale al client dimostra l'arresto di Ollama. Il flag di cancellazione
   richiede evidenza esplicita del worker; assenza di tale evidenza resta false.
   Cancellazione HTTP, lock reale, processi/service e rilascio risorse sulla VPS
   non sono stati verificati o modificati.
6. Template, conteggi token, thinking, RAM/latency e qualità tattica dei modelli
   non acquisiscono nuove prove da queste fixture. Qwen9 rimane qualitativamente
   insufficiente secondo il giudizio del titolare già registrato.

## Decisione e risposte al mandato

1. Difetti dimostrati: correzioni IMPLEMENTATO nel codice per disaccoppiamento,
   deadline/cleanup, custodia e observer. Non è risolta retroattivamente la causa
   del gap storico2211s, che resta non determinabile.
2. Nove fixture superate: sì, ESEGUITO / VALIDATO nel solo perimetro simulato,
   con eccezioni iniziali e ripetizioni mirate documentate sopra.
3. Verifica remota ancora necessaria: semantica Linux dei processi, disconnessione
   SSH e custodia/recovery, permessi/prerequisiti effettivi e cancellazione reale
   HTTP/Ollama. Nessuna di queste proprietà è dichiarata VALIDATO.
4. Pronto localmente, non ancora attestato operativo sulla VPS. Il prossimo
   passo minimo è autorizzare separatamente una verifica remota non generativa
   della sola supervisione/custodia con child sintetico e attempt esclusivo:
   segnali Linux, deadline, disconnessione e recupero. Richiederebbe permesso
   esplicito a trasferimento/esecuzione del codice di controllo e creazione
   della custodia, senza POST, modelli, servizi o lock applicativo. Non è stata
   eseguita né autorizzata qui. Non riapre audit ABI, selezione modelli o RAG.
   Un successivo singolo test Gemma26 o Qwen27 richiederà consenso distinto,
   nuovo binding congelato e ledger nuovo; nessun reset dei tentativi storici.

Accuratezza generativa, Gate, integrazione e certificazione restano BLOCCATO.
Zero SSH, POST, caricamenti, download, modifiche VPS o nuove generazioni.
STOP dopo pubblicazione contestuale di report/TODO/registro e verifica GitHub.
Il commit documentale è il commit che introduce questo report; il suo SHA
viene restituito a pubblicazione verificata, senza riferimenti circolari.
