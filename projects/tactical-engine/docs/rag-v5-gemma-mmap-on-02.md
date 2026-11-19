# Gemma26 mmap — unico tentativo02 dopo Gate02

Data: 2026-11-19. Attività esistente:
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
Baseline: `98211a31a944d61fbf16626a1f9f3de486bf7fe7`.
Commit tecnico pubblicato prima dell'invio:
`ea6779f97d79b49b677b036852670cfa7735aeb9`.

## Esito da distinguere

**Una POST. Gemma ha completato sul server entro il budget:** HTTP200,
`done=true`, `done_reason=stop`, risposta2173 caratteri/318 parole,
2036 token generati e1609 token prompt. Durata Ollama830.615765s; chiusura
worker832.287143s. Risposta e custodia remota complete recuperate read-only.
**Completamento remoto VALIDATO nel singolo perimetro tecnico.**

**Tentativo complessivo BLOCCATO:** il controller Windows ha invece registrato
`E_CONTROLLER_DEADLINE`, con azione tardiva rispetto alla propria deadline,
senza ricevere il finale nella raccolta live. Non trasformiamo questo errore
in PASS complessivo. La copia remota dimostra che il modello aveva già terminato
entro900s: non è un finale tardivo sul server. L'anomalia locale è distinta
dal completamento generativo e non viene attribuita senza prove a PC, rete,
sospensione, Ollama o modello.

Qualità tattica DA FARE; nessun punteggio28/30 o certificazione attribuiti.
Nessun retry, fallback, altra POST o prova Qwen avviati.

## Riconciliazione e tracciamento

TODO, Experiment Register, readiness, report Gemma mmap01/Gate02 e relativi
codici/manifest/ledger riconciliati. HEAD remoto/locale uguali alla baseline,
branch corretto e tree iniziale pulito. Attempt02 assente prima della creazione.

Attività → `operations/quality-first-pilot/gemma_mmap_on_02.py` → commit tecnico
sopra → questo report → completamento remoto e errore locale separati → fermarsi
senza nuova generazione → ESEGUITO, componente remoto VALIDATO, flusso completo
BLOCCATO. Readiness/binding/manifest nuovi in `docs/gemma-mmap-on-02-preparation`.

Differenza tecnica registrata prima del tentativo: payload storico identico,
ma controller/custodia corretti dopo Gate02, anziché raccolta dipendente dal
canale SSH del tentativo01 privo di finale verificabile. Non ripetute nove
fixture, Gate02, benchmark o suite concluse. Solo sintassi/AST del wrapper e
hash delle dipendenze controllati; nessun nuovo percorso generativo.

Il wrapper delega esattamente una volta a
`one_remote → remote_entry → Supervisor → GNU timeout → worker Ollama`.
Controller/core/worker byte-identici alla readiness, hash congelati nel manifest;
nessuna patch ai componenti durante il tentativo. Non eseguito l'observer
opzionale storico: campioni del worker e custodia remota indipendente forniscono
le prove; non è quindi attestato da una nuova osservazione maps/smaps l'assetto
mmap effettivo del runner. Richiesta mmaptrue e configurazione non modificate.

## Payload, identità e preflight

Payload SHA-256 invariato:
`7bc057b52a120ebbc5415ebd22da236f66fd1240421f4b114fcde629a6de97ce`.
Gemma4:26b Q4_K_M, digest
`001e5dafc3c77684c2307ebc6ab8e336e10c9b18eca52acf547d72fc83c3ca8c`.
Caso V10-02/ordinal1, stesse domande/fonti; use_mmaptrue, ctx8192,
predict4096, thinkingtrue, seed42, temperature1, top_p0.95, top_k64,
keep_alive0. Nessuna variazione di draft/batch/configurazione o modello.

SSH football-vps con ED25519 trusted
`SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks`, BatchMode,
StrictHostKeyChecking=yes e UpdateHostKeys=no. Ollama0.40.5 e digest/Q4_K_M
verificati con GET; nessun modello/runner/test concorrente prima dell'invio.
Servizi RAG/Ollama active, memoria disponibile16020709376 byte,
disco4767604736 byte. Nessuna POST show/unload o warm-up.

Lock esistente regular football-owned, device64769/inode842518, senza symlink;
worker ha acquisito lock esclusivo non bloccante, senza crearne o modificarne
l'identità. Stat finale invariato. Directory remota esclusiva e inizialmente
assente:
`/home/football/.local/share/football-data-lab/runtime-evidence/gemma-mmap-on-02-call-01`.
Nuovo ledger locale `evaluation/gemma_mmap_on_02`, nessun reset/riuso01.

Journal remoto: custody_ready0, READY3, reserve_before_GO4, sola GO5,
post_started7, HTTP217, finished5133 e terminale5136. Lo stesso writer/ack prima
dei thread del Gate02 è usato nel percorso reale, non un worker alternativo.

## Tempi e risultato remoto

Tutte le differenze di tempo seguenti usano lo stesso clock remoto o i metadata
Ollama, mai sottrazioni dei clock PC/VPS.

| Misura | Secondi |
|---|---:|
|POST → HTTP200 / primo thinking|104.883883 /104.887139|
|POST → primo contenuto finale|661.323243|
|POST → done wire|830.617789|
|total_duration Ollama|830.615765|
|load_duration|37.027750|
|prompt_eval_duration|64.488451|
|eval_duration|727.648379|
|Worker fino a finished|832.287143|
|Supervisore remoto fino a terminale|832.901235|

1897 chunk wire con indici consecutivi,5765 caratteri thinking e2173 di risposta.
Finale done_reason stop; eval_count2036, prompt_eval_count1609, cache prompt0:
limiti4096/4096 e contesto8192 rispettati secondo i contatori restituiti.
Nessuna stima di token dai caratteri e nessuna nuova prova del tokenizer.

Il risultato worker è oktrue; supervisore remoto reason null, exit0, nessun
TERM/KILL/forced kill. Il finale remoto non è stato modificato o completato
artificialmente. File `answer.txt` separato dal thinking e dal raw originale,
confrontato col contenuto del finished remoto. Valutazione tattica non eseguita.

## Memoria, paging e swap

820 campioni per829.829656s, massimo intervallo osservato1.094232s.
Minimo disponibile6178926592 byte (**6.179GB decimali**), sopra4GB.
Ultimo sample6689107968 byte. Nessun evento abort/error delle guardie.

Paging globale massimo434046280.68 byte/s, persistenza qualificata0s:
la politica invariata richiede anche available<6GB, condizione non raggiunta.
**Non significa assenza di paging.** Swap usata fino1610608640 byte, pari al
totale configurato; delta1049001 pagine in e1317589 out, pagina4096 byte.
Non attribuiamo questi contatori globali esclusivamente a Gemma.

La memoria ha rispettato la guardia nel tratto osservato; questo non prova
margine universale, assenza di pressione o latenza pratica per altri casi.
La dimensione18.7GB del file modello non viene equiparata alla RAM residente.

## Custodia, recupero e anomalia locale

La raccolta live locale conserva1635 chunk, nessun finished o supervisor_terminal.
Il wrapper riceve E_CONTROLLER_DEADLINE e non lo ignora. Record locali:

- started_monotonic24899.359;
- deadline_monotonic25798.937;
- TERM registrato26743.312: **944.375s dopo la deadline locale**;
- tempo start→azione1843.953s; ended26744.875;
- SSH child exit1; writer locale terminato nel cleanup, exit-15;
- terminale custodia locale presente e hash valido, ma risultato okfalse.

Questi timestamp provano una gestione tardiva osservata sul client, non
l'esecuzione di una seconda generazione né una durata remota oltre900s.
Non è dimostrata la causa del ritardo: nessuna nuova scansione/indagine o
correzione automatica viene avviata qui. Resta un blocco dell'esito complessivo
anche se la risposta remota è disponibile. Non si dichiara VALIDATO il watchdog
locale per questa esecuzione. La precedente prova sintetica breve non copriva
ogni comportamento possibile del client lungo un tentativo reale.

Il recupero successivo è esclusivamente read-only, senza nuovo worker/GO/POST.
5137 record della custodia remota, sequenze/checkpoint/raw/terminale verificati
con export/import/recover già versionati; anche la catena locale è verificata.
Il terminale remoto contiene il finished completo e i relativi metadata.

- Hash terminale remoto:
  `db88fd25b241d316e0640bda473257b8cd99ead7132dfccb452fa07dac75f8cc`.
- Catena finale:
  `332c0bd926353a4e69c8d86e0da93df75e5469b0890617d90e7643e7cb559d80`.
- journal.ndjson SHA-256:
  `9b88b8e3c3ef88f6fefcc34681d9e9f96a6d6c87c9c00f49d3f8cb3e2c8d337d`.

`summary.json` distingue gli stati finali; STOP originale mantiene i dati grezzi
del wrapper e non è riscritto per promuoverlo. Inventario SHA-256/dimensioni
di190 file, timeline e tutti i raw/checkpoint/exit conservati nel ledger02.

## Stato finale e cancellazione

Diagnostica read-only finale: ps vuoto, nessun runner, supervisore effimero o
test concorrente; RAG e Ollama active. MemAvailable16041213952 byte,
swap usata309661696 byte, identità lock invariata. Nessun riavvio, kill del
daemon, unload, download, cambio servizio, RAG, panel, corpus, indici o hardware.

Quiete osservata sia nel percorso positivo del worker sia nello snapshot finale.
**È completamento naturale, non prova di cancellazione di un'inferenza.**
Il campo legacy worker remote_cancellation_verified=true deriva da oktrue e
controlli di quiete, non dimostra di aver cancellato un modello in esecuzione.
Cancellazione effettiva resta BLOCCATO/non verificata; non si trasferisce al
modello la garanzia di kill dei processi sintetici. Nessun secondo invio.

## Confronto con gemma-mmap-on-01 e decisione

| Proprietà | Attempt01 | Attempt02 |
|---|---|---|
|POST|1|1|
|HTTP / stream|200,707 chunk parziali|200,1897 chunk completi nel journal remoto|
|Finale Ollama|Assente nelle prove|done true / stop,2036 token|
|Risposta|0 caratteri|2173 caratteri,318 parole|
|Tempo remoto completo|Non dimostrato|830.616s Ollama,832.287s worker|
|RAM minima campionata|6156517376 byte fino circa397s|6178926592 byte su circa830s|
|Raccolta indipendente remota|Assente|Custodia integra, recupero riuscito|
|Controller locale|E_DEADLINE_AMBIGUOUS|E_CONTROLLER_DEADLINE con azione tardiva|
|Qualità tattica|Non valutabile senza risposta|DA FARE sulla risposta ora disponibile|

**Fattibilità generativa del singolo caso dimostrata**, entro budget remoto e
soglie impostate. Latenza circa13m51s non è una promessa di interattività o
scalabilità. Il miglioramento verificabile è la custodia indipendente che ha
salvato la risposta completa nonostante l'errore locale; il percorso completo
non viene dichiarato PASS, INTEGRATO o CERTIFICATO.

Non serve una nuova POST per ottenere questa risposta: è recuperata integralmente
e può essere valutata separatamente. L'anomalia locale richiede eventuale
analisi distinta autorizzata, senza ripetere la generazione o attribuire cause
non osservate. Nessuna valutazione tattica/28su30 eseguita o promozione.

Report, TODO ed Experiment Register contestuali; verifica GitHub e working tree
finale prima della consegna. Commit documentale è quello che introduce questo
report, restituito dopo pubblicazione. **STOP: nessun Qwen27 o altra prova.**
