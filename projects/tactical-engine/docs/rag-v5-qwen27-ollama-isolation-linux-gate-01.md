# Gate Linux differenziale isolamento Ollama — preflight 01

20 novembre 2026 · `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01` · `codex/tactical-state-contract-v1`

**BLOCCATO al preflight.** Sulla VPS sono presenti systemd 255, cgroup v2 e `cgroup.kill`. L'account `football-qwen27` e la directory `/var/lib/football-qwen27-isolation` richiesti dall'implementazione sono assenti. Il Gate sintetico si è fermato prima di creare unità, processi bersaglio, sentinella o marker. **Qwen27 mmap resta BLOCCATO.**

## Traccia

| Passaggio | Evidenza |
|---|---|
| Attività | Stesso pilot. Branch, HEAD locale, GitHub e working tree iniziale verificati alla baseline documentale `0259ce998acf8a78c97655085fef30aee1835b07`. |
| Script | [`qwen27_isolation_linux_preflight_01.py`](../operations/quality-first-pilot/qwen27_isolation_linux_preflight_01.py), sola lettura con loader stdin. |
| Commit | `1f7a72afdbd45b240e883ae2f8f38fee7ae50157`, pubblicato e verificato su GitHub prima dell'unico SSH. Codice operativo da `ca653e695c054619c3db7ad00dba3d3827d9c571`. |
| Report | Questo documento. TODO e registro aggiornati nella stessa pubblicazione documentale. |
| Risultato | SSH read-only con exit 0. Capacità Linux di base presenti e prerequisiti applicativi mancanti. |
| Decisione | Arresto prima dell'esecuzione sintetica secondo il criterio di ammissione. I prerequisiti richiedono una predisposizione esplicitamente autorizzata. |
| Stato | Preflight **ESEGUITO**. Gate sintetico e Qwen27 mmap **BLOCCATO**. |

## Riconciliazione statica e differenza

Verificati TODO, Experiment Register, [implementazione locale](rag-v5-qwen27-ollama-isolation-local-01.md), [progetto STOP](rag-v5-qwen27-ollama-stop-design-01.md), [Gate02](rag-v5-controller-remote-bootstrap-differential-gate-02.md), driver e cronologia Git. Tra `ca653e6` e `0259ce9` differiscono solamente i documenti di chiusura. Non risultano esecuzioni equivalenti. Gate02 riguarda il child sintetico, il processo di custodia e la caduta del trasporto. Le 11 fixture Windows coprono contratti locali. Il Gate qui esaminato richiede invece systemd di sistema e cgroup v2 reali, namespace privato con bersaglio e sentinella distinti, STOP selettivo e persistenza del marker alla perdita del supervisore. Le prove precedenti non sono state rilanciate.

Verificati staticamente `PrivateNetwork` del supervisore, `NetworkNamespacePath` del bersaglio, unità dedicate `system.slice`, `Restart=no`, `BindsTo`, `KillMode=control-group`, timer monotonic a `T0+900 s` e `T0+915 s`, binding di boot, invocazione e inode, TERM circoscritto e KILL sul descrittore `cgroup.kill`. Il codice richiede EUID 0 nel supervisore, `pwd.getpwnam('football-qwen27')` per l'UID isolato e uno store root-owned già esistente. `open.json` deve essere durabile prima del carico e la quiete attestata prima della sua rimozione. Sono rimaste le soglie operative 900 s e 15 s. Nessuna durata sintetica è stata applicata, perché il preflight non ha ammesso l'esecuzione. Una futura finestra ridotta dovrà applicarsi esclusivamente al fixture autorizzato e conservare la relazione deadline a `T0+D`, escalation al più a `T0+D+G` per deadline `D` e grace `G`.

### Identità del codice

| File | SHA-256 |
|---|---|
| `qwen27_isolation_linux_preflight_01.py` | `48751814730a6d3737efb94f751885b395bed075fe8709615e5c596f44779370` |
| `qwen27_isolation_01.py` | `360dbe51c69f9bf3a6a3579fa611153d5c2ee166a43e120e84c9584e32204461` |
| `pilot_supervision_01.py` | `523e2c597b93886d0265a85d89b5245a1b17504f48e08dfe46b51cdf07a7576f` |
| `paired_pilot_remote_01.py` | `1f045315aae4c5a20df865b933d14a5e38eeb9df15af50a2e81d278ce2c4f130` |

Il commit tecnico contiene soltanto il nuovo script read-only, compilato in memoria prima del suo impiego. Il loader SSH ha hashato i byte effettivamente ricevuti, coincidenti con il file versionato. SSH `football-vps` con host key ED25519 storica, `BatchMode=yes`, `StrictHostKeyChecking=yes`, `UpdateHostKeys=no`. Raw stdout, stderr, invocazione, exit e inventario SHA-256 in [evidenze del preflight](qwen27-isolation-linux-gate-01/inventory.json). Nessun file caricato o scritto come artefatto sulla VPS.

## Risultato Linux e soglia di ammissione

| Requisito | Osservazione |
|---|---|
| Linux e systemd | Kernel `6.8.0-147-generic`, PID 1 `systemd`, systemd `255 (255.4-1ubuntu8.18)`, Python `3.12.3`. L'help locale espone le opzioni richieste per unità e timer. |
| Cgroup v2 e `cgroup.kill` | Filesystem `cgroup2fs`, controller memoria disponibile. `cgroup.kill` esiste nei cgroup ispezionati ed è root-owned `0200`. La sessione `football` non ha accesso diretto in scrittura. File osservati tramite stat, senza apertura in scrittura. |
| Namespace | Il namespace della sessione è visibile, `nsenter` è presente e `max_net_namespaces=63630`. La lettura del namespace di PID 1 da UID 1000 restituisce `EACCES`. La creazione e il confinamento di un namespace privato richiedono ancora una prova sintetica autorizzata. |
| Identità e policy | `football` UID 1000 e `ollama` UID 999 esistono. `football-qwen27` risulta assente. `sudo -n -l` ha elencato `/usr/bin/systemd-run` e `/usr/bin/python3` attraverso due interrogazioni di policy. Nessun comando è stato elevato. `pkcheck` ha rifiutato la query con dettagli da un chiamante privo dell'identità richiesta, quindi quel risultato non determina la regola effettiva per l'unità. |
| Lock, stato, marker | Il lock esistente è un file regolare di `football`, inode `842518`, modo `0600`. La directory radice prevista è assente, come il relativo `open.json`. Una prova con UID sostitutivo o directory alternativa lascerebbe aperti i prerequisiti dell'ammissione implementata. |
| Unità e risorse sintetiche | Tutte le sette unità candidate erano `LoadState=not-found`. Attempt ID previsto `qwen27-isolation-linux-gate-20261120-01`, senza riserva remota. Nessuna unità, cgroup, namespace, sentinella o marker sintetici creati dal Gate. Nessun residuo del Gate da rimuovere. |
| RAG e Ollama di produzione | Entrambi `active/running` all'inizio e alla fine del preflight. Per entrambi coincidono MainPID, InvocationID, cgroup e ActiveEnterTimestampMonotonic. Nessun restart richiesto. |

Restano senza misura il cgroup del bersaglio, il namespace privato effettivo, la selettività dello STOP, i tempi TERM/KILL e quiete, lo stato della sentinella e la persistenza del marker dopo interruzione. Il codice operativo e le evidenze storiche sono rimasti intatti. Serve una decisione separata sulla predisposizione dell'account dedicato e dello store di stato con ownership e permessi minimi, oltre alla verifica dei permessi effettivi per l'unità transitoria. Nessun account, ACL, grant o directory sono stati creati o modificati.

**STOP al preflight.** Un SSH read-only. Zero avvii sintetici, chiamate HTTP Ollama, caricamenti, inferenze, modifiche persistenti o pressione RAM/paging indotta. Nessun tentativo autorizzato per Qwen27 mmap.
