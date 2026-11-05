# Audit readiness pannello e runtime VPS

## Identita e perimetro

- Attivita: `RD-PANEL-RUNTIME-READINESS-AUDIT-01`.
- Baseline documentale: `4d9fa912e28fc902e694b7dfd1506b381b009238`.
- Data della ricognizione: 2026-11-05.
- Perimetro: letture statiche del repository e una sessione SSH read-only tramite
  alias `football-vps`; nessun test E2E, inferenza, deploy, riavvio, modifica di
  configurazione o accesso diretto a Chroma/SQLite.

## Sintesi esecutiva

Il pannello pubblico e il suo control plane sono **operativi nello stato legacy
attualmente distribuito**: HTTPS `/panel` risponde 200, API locale `/healthz`
risponde 200, worker vivo, coda vuota, catalogo caricato, collection candidata
FIGC5 a 6.410 chunk e 157 documenti, Nginx/API/Ollama attivi e nessuna unita
fallita. CPU, RAM e disco non mostrano pressione al momento della fotografia.

Questa disponibilita non equivale alla disponibilita del percorso TSC recente.
Il servizio usa `/opt/football-data-lab`, detached su `1a80fe0c...`, con file non
tracciati. In quel checkout sono assenti TSC V1, TSC V2, handoff generativo V2 e
checker semantico S1; i relativi commit non sono presenti nell'object database.
L'API costruisce inoltre il comando del runner senza alcun flag TSC. Pertanto il
pannello pubblico non consuma oggi TSC V1/V2, D3/S1 o Gold S2.

La strada minima per un pannello affidabile entro 7-14 giorni non e un'attivazione
diretta di TSC. E: (1) stabilizzare e rendere riproducibile il runtime esistente;
(2) verificare con una sola smoke controllata il percorso pubblico legacy gia
integrato; (3) progettare separatamente un canale opt-in TSC in staging, con
rollback e gate runtime propri. S2/Gold S2 resta fuori dal cammino critico.

## Evidenze osservate

### Repository autorevole

- Branch locale e remoto GitHub: `codex/tactical-state-contract-v1`.
- HEAD riconciliato: `4d9fa912e28fc902e694b7dfd1506b381b009238`.
- Working tree locale iniziale pulito.
- Il ramo contiene TSC V1/V2, handoff generativo V2, D3 dual-output, checker S1,
  schema/validator Gold S2 e relativo inventario fonti.
- TSC V2/D3/S1 sono validati solo nei rispettivi perimetri offline; il Gate
  runtime V2 e rimasto `blocked` con fail-closed osservato. Gold S2 reale e S2
  restano BLOCCATO.

### VPS e risorse

| Controllo | Evidenza osservata | Valutazione |
|---|---|---|
| Host/utente | `football-data-lab.localdomain`, utente `football` | conforme all'alias approvato |
| Uptime/load | 10 giorni 23 ore; load `0.00 0.00 0.00` | nessuna pressione osservata |
| CPU/RAM | 6 CPU; 15 GiB RAM, circa 14 GiB disponibili | margine ampio nello snapshot |
| Disco | `/dev/vda1` 58 GiB, 19 GiB usati, 39 GiB disponibili (33%) | margine ampio |
| Swap | 1,5 GiB, 245 MiB usati | da osservare, non bloccante nello snapshot |
| Unita fallite | zero system e zero user | sano |

### Servizi, processi e rete

- `football-rag-api.service` e una unita systemd utente, `active/running`,
  `enabled`, `MainPID=76562`, `NRestarts=0`, attiva dal 2026-10-28.
- L'API esegue
  `/opt/football-data-lab/projects/tactical-engine/api/rag_v5_api.py` con la
  virtualenv operativa e working directory `/opt/football-data-lab`.
- Timer maintenance e FIGC sono `active/waiting` ed enabled.
- `ollama serve` e attivo; nessun modello risultava caricato al momento dello
  snapshot. Sono installati `qwen3.5:9b`, `qwen3-embedding:0.6b` e
  `nomic-embed-text`.
- Nginx e `active/enabled`; porte pubbliche 80/443 e servizi 8088/11434 solo su
  loopback, coerentemente con il disegno documentato.

### Pannello, API e catalogo

- `https://football-lab.byoursite.com/panel`: HTTP 200, circa 63 ms nella
  rilevazione.
- `http://127.0.0.1:8088/healthz`: HTTP 200.
- `/v1/metrics`, letto con credenziale gia configurata senza esporla: worker
  vivo, queue depth 0, `catalog_loaded=true`, collection
  `dribbling_tactics_v5_multisource_drive11_figc5_candidate_v1`, expected count
  6.410.
- `/v1/knowledge/stats`: stessa collection, 6.410 chunk e 157 documenti.
- Il valore osservato e uno snapshot; queue depth zero non garantisce esclusivita
  futura e `expected_count` da solo non e un conteggio effettivo. Qui il conteggio
  effettivo e corroborato separatamente dalle statistiche del catalogo in memoria.

### Log e superficie pubblica

- Nessun warning/error systemd dell'unita API nei sette giorni interrogati.
- I log delle ultime 24 ore mostrano numerose scansioni Internet verso path
  comuni (`.env`, PHPUnit, Solr, OWA ecc.), respinte prevalentemente con 401/429
  o 404. Non e emersa compromissione, ma l'esposizione pubblica riceve traffico
  ostile ordinario e richiede monitoraggio continuo.
- Le richieste read-only dell'audit a panel, health, metrics e stats sono
  registrate con 200.

## Stato reale del percorso applicativo

### Percorso pubblico attuale

`api/rag_v5_api.py` costruisce il comando con runner, domanda, request ID,
output, collection, expected count, evidence limit, token output, modello e
context window. Non aggiunge `--tactical-state-contract`,
`--tactical-state-contract-v2` o `--tactical-state-contract-v2-dual-output`.
Il wrapper applica quindi il profilo default storico. Il pannello consuma job,
risposte, fonti, catalogo, eventi e metriche dell'API; non contiene un collegamento
al nuovo percorso TSC.

Percorso ricostruito:

| Tratto | Implementazione effettiva | Gestione/limite |
|---|---|---|
| Browser → panel | Nginx HTTPS serve `api/knowledge_panel.html` tramite `/panel` | token lato utente; scansioni pubbliche respinte |
| Panel → API | chiamate a catalogo, metriche, job, eventi e query | autenticazione bearer e rate limit |
| API → runner | `rag_v5_api.py` avvia `scripts/run_rag_v5_query.py` con `subprocess.run` | worker seriale; timeout configurato; stderr limitato nel dettaglio job |
| Runner → retrieval | wrapper locked e profilo default source/exercise/coverage/routing | collection e expected count dalla configurazione API |
| Retrieval → modello | runner E2E usa Ollama/Qwen | nessun modello caricato nello snapshot; nessuna inferenza nell'audit |
| Modello → risposta | report JSON validato per indice e citazioni, poi esposto nel job/panel | TSC non richiesto dal comando API corrente |

L'errore storico `INCOMPLETE: tactical_quality_gate_failed` e documentato come
incidente del 2026-10-27 causato dall'attivazione di `--tactical-plan` nel profilo
default. La rimozione del flag e registrata come `VALIDATO e INTEGRATO`. Il codice
corrente conserva correttamente il controllo quando un `tactical_plan` e presente,
ma il comando API osservato non abilita il flag. L'audit non ha eseguito una query:
quindi non lo qualifica come problema attuale e non ne dichiara una nuova
risoluzione runtime.

### Divergenza Git/runtime

- Checkout operativo: detached a
  `1a80fe0c6261b10f748a36c2b4fd96e8e2253971`.
- Working tree operativo: non pulito per numerosi artefatti `evaluation/` e
  `index/` non tracciati. L'audit non li ha modificati.
- Assenti nel checkout: `v5_tactical_state_contract_v1.py`,
  `v5_tactical_state_contract_v2.py`, `v5_tactical_state_generation_v2.py` e
  `v5_tactical_semantic_support_s1.py`.
- I commit campione `3fa3a18`, `ac4100d` e `de457a9` non sono presenti nel
  repository operativo.
- HEAD e status del checkout operativo non sono stati modificati dalla
  ricognizione.

Questa divergenza e il principale rischio operativo: la documentazione GitHub
descrive capacita offline piu recenti che il pannello pubblico non possiede.

## Readiness per componente

| Componente | Stato osservato | Limite |
|---|---|---|
| HTTPS/Nginx/pannello statico | pronto e operativo | traffico ostile ordinario da monitorare |
| API, worker, coda, catalogo | operativo nello snapshot | nessuna query generativa eseguita nell'audit |
| Collection FIGC5/catalogo | coerente 6410/157 in memoria | non e una certificazione universale del corpus |
| Runtime legacy | disponibile | checkout detached/sporco e non riproducibile dal ramo corrente |
| TSC V1/V2 nel pannello | assente | codice non distribuito e flag non inoltrati dall'API |
| D3/S1 | solo offline sul ramo GitHub | non distribuito; S1 copre solo exact atomic |
| Gold S2/S2 | BLOCCATO | nessun gold reale congelato; inventario non dimostra fattibilita 390/606 |

### Tracciabilita delle implementazioni recenti

| Componente | Commit principale/finale | Evidenza | Runtime pubblico |
|---|---|---|---|
| TSC V1 | `c1c2b23`, hardening `947e667`/`21bfd36` | validazioni offline e Gate FIGC5 fail-closed | assente |
| TSC V2 Operational Relations | `4cf91d6`, hardening finale `ac4100d` | test offline registrati | assente |
| Handoff generativo V2 | `307064c`, remediation `8a16a73` | test mock/offline | assente |
| D3 dual output | `f544589` | implementazione e verifica offline | assente |
| S1 semantic support | `de457a9` | 29/29 S1/D3 e 43/43 regressioni TSC V2 registrate | assente |
| Gold S2 schema/validator | `d0808df` | 18/18 sintetici; zero casi reali | non applicabile/BLOCCATO |

## Scenari decisionali

### A — Stabilizzare il pannello legacy esistente (raccomandato)

Obiettivo: rendere affidabile e riproducibile cio che e gia pubblico, senza
promuovere capacita TSC non integrate.

Passi minimi, soggetti ad autorizzazioni separate:

1. Congelare e documentare HEAD, configurazione non segreta, hash dei file
   applicativi e stato degli artefatti operativi.
2. Definire un checkout/deploy pulito e riproducibile con rollback, preservando
   gli artefatti runtime non tracciati fuori dal codice.
3. Eseguire una sola smoke autenticata dal pannello su caso minimo, con timeout,
   nessun retry, evidenze e verifica di queue/worker/index prima-dopo.
4. Verificare recovery del singolo job e leggibilita di risposta/fonti nel panel;
   non ripetere reboot o campagne gia validate.
5. Attivare una finestra breve di osservazione di error rate, timeout, latenza,
   disco e rinnovo TLS.

Beneficio: pannello utilizzabile subito con il perimetro legacy gia noto. Rischio:
qualita tattica non universale e latenza generativa storicamente elevata. Stima:
3-7 giorni lavorativi se il deploy riproducibile non incontra divergenze.

### B — Integrare TSC V2/D3/S1 nel pannello

Richiede prima un percorso opt-in separato nell'API e nel pannello, staging alla
baseline GitHub, compatibilita del runner, un Gate runtime nuovo e rollback. Il
Gate V2 precedente e rimasto bloccato; D3/S1 non risolve S2 e non va promosso come
validazione semantica generale.

Beneficio: diagnostica fail-closed e piano tattico strutturato. Rischio: elevato
per una finestra 7-14 giorni se unito alla bonifica del checkout produttivo.
Stima: possibile solo come pilot opt-in non pubblico in 7-14 giorni; non e
ragionevole promettere integrazione pubblica/certificazione nello stesso periodo.

### C — Attendere Gold S2 e validazione semantica completa

Non e compatibile con l'obiettivo temporale. Inventario, diritti/provenienza,
selezione disgiunta, annotazione, doppia review, adjudication e freeze reale sono
ancora mancanti. Beneficio alto per una validazione futura; nessun vantaggio
immediato per la disponibilita del pannello.

### Matrice operativa consolidata

| Componente | Stato attuale | Evidenza | Blocco | Intervento minimo | Rischio |
|---|---|---|---|---|---|
| Panel/Nginx | INTEGRATO storico, operativo osservato | HTTPS 200, listener 80/443 | nessuno nello snapshot | osservazione e smoke controllata | basso-medio |
| API/worker | INTEGRATO storico, operativo osservato | active/running, worker vivo, queue 0 | checkout non riproducibile | congelare baseline e separare artefatti | medio |
| Retrieval/FIGC5 | INTEGRATO storico | catalogo 6410/157 | nessuna query eseguita | smoke singola con indice prima/dopo | medio |
| Qwen legacy | disponibile | modello installato, Ollama attivo | qualita/latency non verificate oggi | smoke con timeout e nessun retry | medio-alto |
| TSC V2/D3/S1 | VALIDATO offline nei perimetri dichiarati | commit e report GitHub | assenti da produzione; Gate V2 bloccato | staging + API opt-in + nuovo Gate | alto |
| Gold S2/S2 | BLOCCATO | schema e inventario soltanto | fonti/diritti/gold/freeze mancanti | programma separato | alto/lungo termine |

## Piano operativo raccomandato (7-14 giorni)

1. **Giorni 1-2 — baseline operativa:** inventario riproducibile del checkout e
   separazione codice/artefatti; decisione sul commit legacy da congelare.
2. **Giorni 3-4 — staging e rollback:** clone indipendente pulito del commit
   scelto, configurazione non segreta confrontata, comando di rollback scritto e
   verificato staticamente. Nessuna sostituzione della produzione senza gate.
3. **Giorni 5-7 — smoke minima:** una sola query autenticata rappresentativa,
   osservazione di coda, timeout, artefatti, citazioni e rendering pannello;
   fail-closed su difformita. Nessun benchmark esteso.
4. **Giorni 8-10 — osservazione:** errori/timeout, risorse, timer, TLS e traffico
   anomalo; definizione SLO minimi basata sui dati osservati, non su soglie
   arbitrarie.
5. **Giorni 11-14 — decisione TSC opt-in:** solo se A e stabile, preparare patch
   API/panel separata e disattivata per default per TSC V2/D3/S1, senza S2 e senza
   dichiarazioni di integrazione. Il relativo Gate richiede autorizzazione nuova.

Valutazione per fase: ripristino/stabilizzazione panel **plausibile con condizioni
in 3-7 giorni**; verifica runtime minima **plausibile in 1-3 giorni aggiuntivi**;
pilot D3/S1 opt-in **plausibile ma non dimostrato in 7-14 giorni**; rilascio
pubblico TSC e S2 **non dimostrabile** nella finestra. Il percorso critico e la
riconciliazione del checkout operativo, non la capacita hardware.

## Rollback proposto

Il rollback va approvato e verificato staticamente prima di qualunque futura
modifica: conservare fingerprint della baseline operativa `1a80fe0c`, unit file e
configurazione non segreta; creare staging indipendente; non riusare il working
tree sporco; distribuire solo da commit congelato; preservare artefatti runtime
fuori dal checkout; in caso di smoke fallita ripristinare esclusivamente il
precedente symlink/percorso di release o unit ExecStart gia attestato e riavviare
solo con autorizzazione distinta. Nessun rollback e stato eseguito in questo audit.

## Decisioni richieste al titolare

1. Approvare o respingere Scenario A come priorita.
2. Scegliere il commit legacy da congelare e autorizzare uno staging indipendente.
3. Autorizzare separatamente una singola smoke generativa autenticata con evidenze
   e controllo indice prima/dopo.
4. Decidere se, dopo stabilizzazione, aprire un pilot TSC opt-in non pubblico.
5. Mantenere Gold S2 come programma separato, senza usarlo come prerequisito del
   ripristino legacy e senza promozioni premature.

## Criteri di promozione e arresto

Promuovere il pannello legacy a “operativamente pronto” solo con checkout
riproducibile, smoke completa, artefatti attribuibili, citazioni valide, nessuna
variazione dell'indice, recovery osservabile e finestra senza errori significativi.

Arrestare su: checkout non riconciliabile, modifica inattesa della collection,
timeout, output incompleto, worker/coda incoerenti, artefatti non attribuibili,
segreti nei log o impossibilita di rollback. Un HTTP 200 del pannello da solo non
dimostra la riuscita del percorso generativo.

## Decisione

Adottare **Scenario A**. Il pannello e raggiungibile e il control plane e sano,
ma la readiness generativa va confermata con un'attivita distinta e controllata.
Mantenere TSC V2/D3/S1 fuori dal pubblico finche non esistono staging, handoff API
opt-in e Gate runtime positivi. Non attendere Gold S2 per stabilizzare il legacy,
ma non presentare S1 come sostituto di S2.

Stato dell'audit: **ESEGUITO**. Piano operativo: **DA FARE**, in attesa di
approvazione del titolare. Nessuna integrazione o certificazione nuova e stata
attribuita.
