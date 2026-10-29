# RAG Corpus — Ussia Gate A Read-Only 01

Data: 2026-10-29  
Ramo: `codex/tactical-state-contract-v1`  
Baseline: `3bbb3c6723b653b991ebdfe1e9bd641bb44b73c7`

## 1. Perimetro

Una sola connessione SSH autorizzata ha eseguito la ricognizione Gate A con
controlli preventivamente delimitati. Sono stati letti esclusivamente
metadati filesystem, mount/dispositivi, disponibilità di comandi, stati/nome
di unità e timer, processi pertinenti, file descriptor visibili e presenza di
cron pertinenti. Non sono stati aperti Chroma o SQLite, letti contenuti del
corpus, enumerati record, creati file/directory/snapshot, calcolati hash,
effettuati export o modificati servizi/configurazioni.

Due tentativi di composizione locale dello script erano terminati prima di
invocare `ssh`; non costituiscono connessioni né retry remoti. La ricognizione
remota è stata eseguita una sola volta e si è conclusa con exit code 0.

## 2. Filesystem e capacità di snapshot

- root Chroma confermata in
  `/opt/football-data-lab/knowledge/rag/chroma`, `football:football`, mode
  `775`;
- filesystem: `ext4`, mount `/`, sorgente `/dev/vda1`, opzioni `rw`;
- dispositivo: partizione diretta `vda1`, non volume LVM e non filesystem
  Btrfs/ZFS;
- spazio osservato: 61.285.326.848 byte totali, 41.794.781.184 disponibili,
  32% usato;
- comandi `lvs`, `vgs`, `pvs`, `lvcreate`, `btrfs` e `rsync` presenti; `zfs`
  assente.

La presenza dei comandi non dimostra capacità di snapshot: il backing store
osservato è una partizione ext4 diretta. Non risulta quindi un meccanismo
locale atomico LVM/Btrfs/ZFS applicabile al percorso. Un eventuale snapshot
del provider/hypervisor non è documentato né verificato da Gate A.

La dimensione ricorsiva della directory Chroma non è stata acquisita, perché
avrebbe richiesto enumerazione. Lo spazio libero non dimostra quindi ancora la
sufficienza dello staging.

## 3. Utilizzatori potenziali e stato osservato

Unità utente pertinenti:

- `football-rag-api.service`: `active/running`;
- `football-rag-maintenance.service`: `inactive/dead`;
- `football-figc-discovery.service`: `inactive/dead`;
- `football-rag-maintenance.timer`: `active/waiting`;
- `football-figc-discovery.timer`: `active/waiting`.

Unità di sistema pertinente osservata: `ollama.service`, `active/running`.
Ollama è un utilizzatore potenziale della pipeline, ma questa ricognizione non
ha osservato un suo file descriptor sotto Chroma.

La scansione dei file descriptor visibili all'utente `football` ha rilevato un
processo `python` con almeno un descriptor rivolto sotto la root Chroma. La
ricognizione non ha acquisito una correlazione probatoria fra quel PID e una
specifica unità systemd; la contemporanea attività dell'API rende la relazione
plausibile ma non dimostrata.

Nessuna riga cron utente e nessun file cron di sistema accessibile ha
corrisposto ai termini circoscritti. La copertura della scansione `/proc` è
limitata ai processi e descriptor visibili senza privilegi aggiuntivi; non
prova l'assenza universale di altri utilizzatori.

L'output temporale di `systemctl --user list-timers` non è utilizzabile per
attribuire le scadenze, perché la formattazione del parser ha selezionato
colonne non corrispondenti ai nomi delle unità. I nomi e gli stati dei timer
restano invece confermati dalla lista delle unità. Non è stato eseguito alcun
retry.

## 4. Staging proposto

Catena osservata:

- `/home/football`: `750`;
- `.local`, `.local/share`, `.local/share/football-data-lab`: `775`;
- `.local/share/football-data-lab/evidence`: `700`;
- `.local/share/football-data-lab/evidence/ussia`: non presente.

Il parent `evidence` è idoneo come confine riservato grazie al mode `700` e si
trova sullo stesso filesystem con 41,79 GB liberi. La directory Ussia non è
stata creata. La capacità resta non dimostrata finché non viene acquisita, con
autorizzazione distinta, la dimensione totale della sorgente da copiare.

## 5. Metodo di snapshot raccomandato

In assenza di snapshot locale atomico dimostrato, la soluzione preferita è una
**cold copy applicativamente coerente** durante una breve finestra autorizzata:

1. sospendere l'avvio dei timer FIGC discovery e RAG maintenance;
2. fermare l'API RAG e qualsiasi altro processo autorizzato che mantenga file
   descriptor sotto Chroma;
3. verificare zero descriptor visibili sotto la root e assenza di processi
   pertinenti non riconciliati;
4. eseguire `sync`;
5. copiare integralmente la root Chroma nello staging riservato, senza aprire
   la collection;
6. verificare integrità pre/post secondo il piano approvato;
7. riavviare unità e timer originariamente attivi e verificarne lo stato.

Questi passi sono una proposta, non sono stati eseguiti e richiedono
autorizzazione B esplicita a stop/start, creazione staging, copia e hash. Una
copia live non è raccomandata. Un backup SQLite isolato non coprirebbe da solo
gli artefatti HNSW e non sostituisce la quiescenza dell'insieme Chroma.

## 6. Rischi e condizioni di arresto

- servizio ancora attivo o descriptor residui: arresto prima della copia;
- timer capace di riaprire/modificare la collection: sospensione autorizzata o
  arresto;
- utilizzatore non attribuibile: snapshot non certificabile;
- spazio staging insufficiente: nessuna creazione/copia;
- fallimento stop/start o mancato ripristino: rollback operativo e nessuna
  promozione del bundle;
- hash/invarianti discordanti: bundle non utilizzabile;
- contenuti o permessi fuori perimetro: arresto fail-closed.

## 7. Prerequisiti ancora mancanti

1. dimensione ricorsiva della root Chroma e spazio di sicurezza richiesto;
2. correlazione fra unità/PID e ogni descriptor Chroma;
3. conferma che nessun altro servizio o processo privilegiato acceda alla
   collection durante la finestra;
4. autorizzazione a fermare/riavviare API e timer pertinenti;
5. autorizzazione a creare staging `0700`, copiare e calcolare hash;
6. politica di custodia, accesso, retention e distruzione approvata;
7. perimetro esatto degli artefatti Ussia copiabili;
8. accettazione esplicita dell'eventuale bundle soltanto parziale.

## 8. Decisione e stati

Gate A: **ESEGUITO**. La cold copy con quiescenza è il metodo preferito; non è
ancora **VALIDATO** né autorizzato. Il percorso staging è idoneo sul piano dei
permessi, ma capacità e creazione restano **DA FARE**. Acquisizione bundle:
**DA FARE**. Snapshot probatorio, adapter reale e verifica collection runtime:
**BLOCCATO**. Nessuna attività nuova **INTEGRATA** o **CERTIFICATA**.

STOP: nessuna acquisizione o modifica successiva è autorizzata da Gate A.
