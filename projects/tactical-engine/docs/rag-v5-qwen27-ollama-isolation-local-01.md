# Isolamento Ollama per Qwen27 mmap — implementazione locale

20 novembre 2026 · `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01` · `codex/tactical-state-contract-v1`

## Traccia

| Passaggio | Evidenza |
|---|---|
| Attività | Stesso pilot. Baseline iniziale e HEAD GitHub `d39ac92d46047544c4170d63a3b1211814fbeae2`, working tree iniziale pulito. Riconciliati TODO, Experiment Register, progetto STOP, codice e storici di Qwen27, Gemma02 e Gate02. |
| Script | `qwen27_isolation_01.py`, adattamenti a `pilot_supervision_01.py` e `paired_pilot_remote_01.py`, fixture differenziale `test_qwen27_isolation_01.py`. |
| Commit | Baseline tecnica finale `ca653e695c054619c3db7ad00dba3d3827d9c571`, pubblicata e verificata prima del report. Il commit documentale che introduce questo file completa il report, il TODO e il registro sul medesimo branch. |
| Report | Questo documento. |
| Risultato | Sintassi 4/4 e fixture differenziali 11/11 su Windows. Isolamento Linux e STOP sul carico reale ancora da verificare. |
| Decisione | Conservare il codice per una successiva verifica sintetica Linux autorizzata separatamente. |
| Stato | Isolamento **IMPLEMENTATO** localmente, verifiche locali **ESEGUITO**, verifica Linux e tentativo Qwen27 mmap **BLOCCATO**. |

Il [progetto STOP](rag-v5-qwen27-ollama-stop-design-01.md) richiede un confine di arresto esclusivo perché il daemon di produzione può condividere un runner. [Gate02](rag-v5-controller-remote-bootstrap-differential-gate-02.md) attesta custodia, READY/GO e terminazione del child sintetico. [Gemma02](rag-v5-gemma-mmap-on-02.md) ha completato sul server, con TERM locale tardivo di 944,375 s. Il [precedente Qwen](../evaluation/quality_first_qwen27_single_case_01/summary.json) ha fermato l'unico invio, senza mmap esplicito, a 3.149.516.800 byte disponibili. Nessuna evidenza equivalente sulla barriera persistente o sull'arresto di un cgroup Ollama compare nei commit e nelle fixture storiche esaminate. Il delta è stato registrato nella fixture prima dell'esecuzione.

## Codice e architettura

| File | Modifica |
|---|---|
| [`qwen27_isolation_01.py`](../operations/quality-first-pilot/qwen27_isolation_01.py) | Entrypoint Linux per un supervisore sotto PID 1. Controlla autorizzazione e identità, crea unità Ollama transitoria separata e timer, detiene il lock, gestisce le soglie e registra binding e ricevuta di arresto. |
| [`pilot_supervision_01.py`](../operations/quality-first-pilot/pilot_supervision_01.py) | Hook opzionali per deadline assoluta, notifica STOP e passaggio selettivo di descrittori. Dopo il fork, il writer può chiudere i descrittori estranei prima di confermare la custodia. L'ordine del writer, il protocollo READY/prenotazione/GO e il formato del journal sono riusati. |
| [`paired_pilot_remote_01.py`](../operations/quality-first-pilot/paired_pilot_remote_01.py) | Stesso punto d'invio HTTP e stessi controlli sullo stream. Il worker isolato verifica il marker root, namespace, genitore e lock ereditato, poi osserva il canale STOP. Il percorso legacy corrente verifica la barriera dopo aver acquisito il lock. |
| [`test_qwen27_isolation_01.py`](../operations/quality-first-pilot/test_qwen27_isolation_01.py) | Fixture mirate per le proprietà introdotte in questo commit. |

1. **Istanza e rete.** L'entrypoint richiede un supervisore di sistema separato, con `PrivateNetwork=yes`, senza restart e con il solo loopback nel namespace. Il worker esistente gira come `football` nel medesimo namespace del supervisore. L'unità Ollama transitoria entra in quel namespace, usa `127.0.0.1:11434` e ha un proprio cgroup sotto `system.slice`. `BindsTo=` lega il suo ciclo di vita al supervisore. L'istanza usa l'UID dedicato `football-qwen27`, distinto da produzione e worker, senza capability e con protezione del cgroup. Modello e binario provengono dall'installazione esistente. Manifest, digest, dimensioni e leggibilità dei blob sono verificati senza leggere i pesi per intero. Lo store è montato in sola lettura e lo scratch è privato. L'API di produzione sta nel namespace host. [systemd: namespace](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#NetworkNamespacePath=) · [systemd: arresto](https://www.freedesktop.org/software/systemd/man/latest/systemd.kill.html).
2. **Ammissione e custodia.** La futura esecuzione richiede un file root-owned con consenso a una POST e all'escalation, un attempt ID nuovo e il payload Qwen V10-02 con il solo delta `use_mmap=true`, verificato sull'hash canonico `331530c85dac2e0030e5c8d3489cee9c4ea0ee5e53486667e95b00096304451e`. Il supervisore prende il lock del pilot una volta e pubblica `open.json` prima dell'unità di carico. Il record include boot ID, hash dei sorgenti, identità del supervisore, namespace, digest, riserva temporale e inode del lock. `binding.json` aggiunge invocazione systemd, cgroup e inode del bersaglio, identità del suo processo principale e hash binario. Il worker eredita il lock senza una seconda `flock`. Il writer esclude i descrittori del lock e del canale STOP. Il core manda l'unica GO dopo READY, prenotazione durevole e primo campione valido.
3. **Controllo indipendente.** La deadline monotonic parte prima dell'unità di carico e non riparte alla GO. Il watchdog riusa `pressure_step`. Soglie invariate: `MemAvailable < 4.000.000.000` byte oppure almeno 5 s consecutivi con swap cumulativo a `≥ 67.108.864` byte/s e `MemAvailable < 6.000.000.000` byte. Campionamento previsto a 1 s durante il carico, inclusa la chiusura. Il monitor chiude il canale del worker per attivare lo `shutdown` cooperativo del socket. TERM passa solo all'invocazione verificata e non blocca il thread di escalation. KILL si appoggia al file `cgroup.kill` ancorato al cgroup originale. Il limite è `min(trigger, T0 + 900 s) + 15 s`. Due timer monotonic di PID 1 a `T0 + 900 s` e `T0 + 915 s` costituiscono il percorso di riserva. Prima di agire verificano marker, boot, invocazione e inode. [systemd: timer monotonic](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html#OnActiveSec=) · [Linux: cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html).
4. **Ricevuta e interdizione.** Si registrano trigger, invio azioni, campioni, appartenenza dei processi, prova del cgroup, memoria e stato delle unità di produzione. Per la prova del cgroup si richiedono lo stato inattivo del manager e `populated=0` con lista vuota, oppure rimozione corroborata dal manager per l'unità riservata e il percorso originale. Si verificano inoltre boot, lock invariato, cleanup del worker e del writer, terminale della custodia, riserva RAM e servizi. La ricevuta è sincronizzata prima della rimozione del marker. Se manca la quiete, il marker resta anche dopo crash o reboot. La directory per attempt resta esclusiva e impedisce il riutilizzo dello stesso ID. Lo STOP operativo non imposta `remote_cancellation_verified=true`. Il percorso Qwen isolato non presume la causalità della cancellazione HTTP.

### Scelte rispetto al progetto

- Il punto d'ingresso isolato è un supervisore distaccato avviato dal manager di sistema con autorizzazione già congelata. La precedente sessione SSH interattiva resta nel percorso storico. L'unico worker generativo viene riusato e la decisione di sicurezza a 900 s appartiene alla VPS. Il controllo non pubblica una route HTTP o un secondo driver di generazione.
- Il namespace nasce sul supervisore e viene condiviso col servizio Ollama, mantenendo distinti i cgroup. L'UID dedicato e il file root-owned sono prerequisiti d'installazione verificabili. Il codice non crea account, ACL, permessi generici, grant `sudo` o configurazioni persistenti della VPS.
- I due timer verificano l'identità anche sul percorso di riserva. Il monitor selettivo e i timer hanno azioni distinte dalle prove di estinzione. Un ritardo dello scheduler, un file del kernel non leggibile o una ricevuta incompleta non vengono classificati come prova puntuale.
- L'isolamento controlla l'ingresso corrente del pilot. I byte storici, report, launcher e manifest restano archiviati. Gli hash congelati dei precedenti core/worker continuano a identificare le revisioni storiche e non autorizzano una nuova esecuzione con le versioni modificate. Lo stato persistente ha un'ammissione nuova, senza recupero automatico di un marker ambiguo.

## Evidenze locali e limiti

Comando differenziale eseguito su Windows con Python 3.9:

```text
python -B -m unittest discover -s projects/tactical-engine/operations/quality-first-pilot -p test_qwen27_isolation_01.py -v
Ran 11 tests in 0.177s
OK
```

Le fixture coprono marker lasciato aperto su esito ambiguo, riapertura dopo ricevuta quieta, ID consumato, marker incongruente, hash e consenso, limite grace, `cgroup.events` ambiguo, descrittore STOP del writer, guardia RAM prima della raccolta, escalation indipendente dalla richiesta TERM e rifiuto di invocazione systemd cambiata. Il controllo statico degli argv e dell'AST rileva una sola POST nel worker condiviso. Compilazione in memoria dei quattro file e `git diff --check` riusciti. Il file manifest Qwen archiviato ha SHA-256 uguale al digest atteso. Nessuna suite o Gate02 ripetuti.

`sys.platform` ha restituito `win32`. `wsl --list --quiet` non ha elencato distribuzioni. Nelle fixture sono simulati systemd, il bersaglio cgroup e la sincronizzazione della directory. Restano da verificare su Linux il passaggio effettivo degli FD al processo, il namespace privato col proprio loopback, i permessi dello store, l'accesso ai bus systemd, `cgroup.events` e la rimozione effettiva dell'unità, BindsTo dopo crash e la puntualità di timer e segnali. Il completamento della finestra di STOP e il rilascio della RAM con Ollama reale non sono stati misurati.

### Condizioni per la verifica sintetica Linux

Prima di qualsiasi attivazione serve autorizzazione separata e un perimetro sintetico senza modelli. Verificare versione di systemd, namespace, cgroup v2 con `cgroup.kill`, account distinti, invocazione sistema e permessi minimi per il solo bersaglio. Predisporre per quella verifica un carico sintetico dentro un'unità transitoria con i medesimi confini e una sentinella fuori bersaglio. Usare un nuovo ledger sintetico. Dimostrare mancata raggiungibilità dell'endpoint dal namespace host, arresto durante due fasi sintetiche, TERM/KILL nel budget e cgroup vuoto, sentinella viva, conservazione del marker dopo crash/SSH EOF e impossibilità di riusare l'ID. Registrare i tempi effettivi di azione e uscita. Le evidenze Gate02 già valide coprono i meccanismi di custodia e vanno riutilizzate. La futura prova Qwen27 richiede poi un consenso distinto, il binding reale verificato e tutte le condizioni già documentate di singolo invio e nessun retry.

**STOP dopo la pubblicazione del report.** Nessuna attivazione systemd, SSH sulla VPS, modifica di daemon o VPS, caricamento, download di pesi, POST Ollama o inferenza. Nessuna modifica a RAG V5, pannello, corpus, retrieval, modelli, prompt, soglie o artefatti storici.
