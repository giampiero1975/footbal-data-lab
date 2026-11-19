# Correzione ordine di bootstrap writer Linux — 01

Data: 2026-11-19. Attività esistente:
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
Baseline riconciliata GitHub/locale: `e6f1fbfe7e2f089645d7254d9300dc4a7ebd4bc2`.
Commit tecnico: `40590ee72e40af49d0277f5fb1f861ef5295bc1c`.

**Correzione IMPLEMENTATO. Verifica locale mirata ESEGUITO / VALIDATO su Windows.
Linux nativo non verificato; gate remoto e inferenze restano BLOCCATO.**

## Riconciliazione e differenza tecnica

Consultati TODO e registro ufficiali, report del gate remoto, manifest, ricevuta
supervisore e originali dell'attempt `controller-remote-gate-20261119-01`.
Branch corretto, HEAD locale/GitHub uguali alla baseline, tree iniziale pulito.
Il core dei commit d4d2ee6 e7a7bc6d è identico; il gate7a7bc6d avviava il reader
stdin prima del writer, come l'entry point reale del pilot. Nessuna correzione
equivalente già completata. Nessuno degli originali del gate è stato modificato.

Attività → `writer_bootstrap_order_check_01.py` e modifica dei soli bootstrap
→ commit tecnico sopra → questo report → un controllo differenziale locale
con rami direttamente dipendenti → pronto a futura verifica sintetica separata
→ IMPLEMENTATO; verifica locale VALIDATO, remota BLOCCATO.

Differenza registrata prima del controllo in `writer-bootstrap-order-local-01/scope.md`:
conferma durevole iniziale, ordine writer→reader/relay→child→READY→prenotazione→GO,
rifiuto del fork con altri thread Python, helper finale indipendente dal fork.
Non rieseguite nove fixture, benchmark o prove generative.

## Patch limitata al bootstrap

### Supervisore condiviso e barriera durevole

`pilot_supervision_01.py`, `Supervisor.run()`:

1. Su contesto fork, prima di creare directory/processi, richiede main thread
   unico (`E_CUSTODY_FORK_THREADS` altrimenti).
2. Avvia writer prima di creare qualsiasi reader/relay del supervisore.
3. Invia record0 `custody_ready` e attende ack con sequenza/tipo/hash. Il writer
   esistente crea journal/raw, fsync dei file e checkpoint0 prima dell'ack.
4. Soltanto dopo ack0 richiama `on_custody_ready`, che può avviare i thread di
   controllo, e lancia il child. Il suo READY viene inoltrato soltanto dopo
   persistenza, come prima. Prenotazione fsynced prima di GO invariata.
5. Ack assente, errato, writer morto o errore I/O impediscono callback, child e
   GO, con errore bootstrap esplicito e cleanup limitato. Attesa di inizializzazione
   entro min(grace, timeout), inclusa nella deadline esistente, senza rinnovo.

`remote_entry()` reale del pilot e `remote_supervision_gate_01.py:run()`:
relay e reader stdin vengono entrambi creati nel callback successivo all'ack,
non prima di `Supervisor.run()`. Nessun percorso di generazione alternativo.

### Scritture esclusive successive ai thread

Anche `durable_file()` usava fork su Linux, compresa la ricevuta finale dopo
l'avvio del reader. Solo spostare il primo writer avrebbe lasciato questo rischio.
Ora usa spawn su entrambe le piattaforme: interprete separato, target built-in
`exec` con codice fisso di scrittura/fsync e dati passati come oggetti, nessuna
shell. Il target non richiede l'importazione del modulo iniettato via stdin.
Nessuna nuova libreria, servizio o processo persistente; timeout/join/TERM/KILL
dell'helper invariati. Il controllo mirato esercita lo stesso target spawn
mentre il reader locale è attivo. L'esecuzione spawn sulla Python Linux VPS
rimane non verificata in questa sessione.

### Invarianti verificate staticamente

Il confronto AST con la baseline conferma identici loop di controllo e blocco
finally/cleanup, `_journal_writer`, `recover()` e `guard_then_emit()`. Invariati
900s, grace15s, segnali, guardie RAM/paging, limiti delle code e custodia.
Payload, input e limiti del manifest del pilot identici; aggiornati soltanto
hash del core e riferimenti nei manifest pending. Autorizzazione pending falsa;
nessun aggiornamento delle autorizzazioni storiche. Sintassi dei tre file toccati
controllata e `git diff --check` superato. Evidenza: `static-delta.json`.

## Una verifica differenziale, con le sole dipendenze necessarie

Script: `operations/quality-first-pilot/writer_bootstrap_order_check_01.py`.
Nessuna SSH, rete, POST, modello o codice applicativo. Child Python sintetico.

| Criterio | Evidenza | Esito |
|---|---|---|
|Writer prima del reader|Callback controlla journal/checkpoint0 e hash ack prima di creare reader e child|PASS|
|Lettura concorrente successiva|Reader su pipe locale avviato solo dopo ack0; attende autorizzazione|PASS|
|READY e GO durevoli|READY presente nel journal prima del relay; un reserve_before_GO precedente all'unica GO_sent|PASS|
|Journal/checkpoint/terminale|Catena, raw e terminale verificati tramite recover()|PASS|
|Custodia non pronta|Writer fallisce al record0: errore E_CUSTODY_BOOTSTRAP_IO, callback mai eseguito, nessun child/GO|PASS|
|Thread già attivo|Guardia Python rifiuta il fork; il ramo Linux di Supervisor non è eseguito su Windows|PASS guardia, Linux non verificato|
|Scrittura dopo reader attivo|Ricevuta tramite spawn, contenuto verificato|PASS|
|Terminazione|Child e writer reaped, reader/emitter chiusi e active_children vuoto|PASS|

Due esecuzioni dello stesso controllo, non due suite: la prima è conservata in
`run-before-shared-spawn`; dopo avere condiviso il target spawn sulle piattaforme
è stata ripetuta solo la verifica interessata, estesa alla ricevuta con reader
attivo. Ultimo risultato in `run-01/result.json`: PASS, platform win32,
Linux_native_tested=false. Entrambi i risultati precedenti sono conservati.
Un controllo statico AST iniziale selezionava il loop di raccolta terminale
anziché quello di controllo: corretta la selezione nell'analisi, senza cambiare
il controller o rieseguire altre fixture.

WSL non ha distribuzioni installate, Docker CLI non disponibile; non sono stati
installati Linux, toolchain o dipendenze. `linux-availability.json` conserva
l'output reale WSL. Nessuna equivalenza Windows/Linux dichiarata.
Inventario con SHA-256 e dimensioni di29 file in
`docs/writer-bootstrap-order-local-01/inventory.json`.

## Thread preesistenti e limiti espliciti

Nel bootstrap controllato non rimane il fork del writer dopo reader/relay:
il writer nasce sul main thread unico, i feeder delle sue code nascono dopo il
fork e ogni scrittura successiva usa spawn. Con altri thread Python già attivi
il supervisore Linux rifiuta l'avvio prima del fork, invece di tentare un ordine
non sicuro. Questo è un comportamento fail-closed, non supporto del fork da un
host multithread. L'observer locale su Windows usa spawn e non cambia percorso.

`threading.enumerate()` non può attestare l'assenza di thread nativi invisibili
alla Python o impedire thread creati da codice esterno non controllato fra check
e fork. Non promettiamo sicurezza universale in un interprete embedded.
Gli entry point interessati sono processi Python controllati, senza tale codice;
quel contesto non è autorizzato/supportato da questa patch. Se servisse davvero
un host multithread arbitrario, andrebbe progettato separatamente un writer
avviato tramite exec/spawn indipendente; nessun cambiamento architetturale di
quel tipo è stato applicato qui al journal writer.

La causa effettiva del vecchio blocco non è retroattivamente dimostrata:
è eliminato il rischio statico identificato, non ricostruito lo stack perduto.

## Decisione finale

1. Ordine corretto: writer inizializzato e fsynced → ack0 → thread reader/relay
   → child/READY durevole → prenotazione durevole → GO.
2. Percorsi modificati: supervisore condiviso, entry reale `remote_entry`,
   bootstrap gate sintetico e helper di persistenza finale; manifest solo hash.
3. Verifica locale mirata superata su Windows, con rami negativi e dipendenze
   dirette; nessuna prova Linux reale disponibile e nessuna suite storica ripetuta.
4. Nessun fork noto dopo thread nei percorsi controllati; thread preesistenti
   rilevati comportano rifiuto. Limite dell'host embedded esplicito sopra.
5. Codice predisposto per futura verifica remota sintetica separatamente
   autorizzata; Linux/SSH, custodia reale e cancellazione Ollama non VALIDATO.
   Occorrerà un nuovo attempt ID autorizzato, senza reset o riutilizzo del ledger
   fallito. Non è stato predisposto o avviato un altro gate in questa sessione.

Report/TODO/registro pubblicati contestualmente; commit documentale restituito
con verifica GitHub e working tree pulito. Accuratezza generativa, Gate RAG V5,
integrazione e certificazione restano BLOCCATO. **STOP, zero SSH/inferenze.**
