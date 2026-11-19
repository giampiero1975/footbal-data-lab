# RAG V5 — fattibilità hardware e ottimizzazione senza upgrade

Data: 2026-11-19, Europe/Rome. Attività esistente:
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.

## Decisione sulle tre domande

1. **Sì: la VPS è utilizzabile per sviluppare FOOTBALL-DATA-LAB senza spendere
   altro, mantenendo Qwen3.5 9B già installato e il RAG esistente.** Il9B ha
   completamenti documentati, ma non qualità tattica28/30 certificata.
2. **Per Gemma26 esiste una sola ipotesi nativa documentata che merita una
   verifica separata: `options.use_mmap=true`. Non è una soluzione già validata.**
   Il sorgente release sceglie senza mmap per CPU quando l'opzione non è
   esplicita. La mappatura potrebbe cambiare la memoria recuperabile, soprattutto
   nel MoE, ma restano working set, repacking e latenza da verificare.
   **Per Qwen27 Q4_K_M non emerge una configurazione sostenibile dimostrata**
   entro la riserva4GB: il modello dense deve accedere ai pesi di ogni strato.
   Non prometto che mmap risolva entrambi.
3. **La migliore scelta operativa oggi a costo aggiuntivo zero è Qwen3.5 9B
   corrente, conservando il RAG e i suoi controlli.** È l'unica scelta locale
   già disponibile con completamenti verificabili, non un vincitore tattico
   dimostrato. Non promuoverla a sistema autonomo professionale senza evidenze.

Non richiedo un upgrade. Più RAM è la via conservativa per la piena residenza
dei grandi Q4 con margine; non è dimostrato che sia l'unica possibilità teorica
prima di valutare mmap. Se l'unica ipotesi nativa fallisse, non resterebbe una
soluzione zero-costo dimostrata per gli stessi artefatti e lo stesso margine.
Un modello/quantizzazione diverso cambia anche il quesito qualitativo. Il
fallimento dei grandi non rende inutilizzabile l'intero progetto.

## Tracciamento, riconciliazione e perimetro

Attività → script `operations/quality-first-pilot/hardware_feasibility_audit_01.py`
→ commit tecnico delle evidenze **594159f24b158f046fda2046b6604811c4eb8b74**
→ questo report → matrici/evidenze → decisione sopra → audit
**ESEGUITO**, analisi **VALIDATO** solo nel perimetro documentale/read-only.
Configurazioni ottimizzate e qualità non validate. Il commit documentale che
introduce il report comprende TODO e registro, ed è restituito nella consegna.

Baseline locale/GitHub `185a7f33dfa3dd523156a427aecfbe62c7c5d04c`, branch corretto,
tree pulito. Letti TODO, Experiment Register, intero report protocollo, script e
ledger01/03/Qwen isolato; riutilizzati ricognizione backend, dossier H1-G2,
completamento Qwen9, diagnosi grounding e riconciliazione RAG. Nessun audit
equivalente con questa matrice risultava completato. Nuove letture limitate a
hardware, configurazione e contabilità mancanti: non benchmark né attestazione
ABI ripetuta. Nessuna suite37/13/16/5/32/17 o inferenza rieseguita.

Evidenze in [inventory.json](hardware-feasibility-audit-01/inventory.json):
script remoto/invocazione/stdout/exit/stderr, quattro file cgroup supplementari,
fonti ufficiali con URL/hash, input storici/hash e `analysis-facts.json`.
Snapshot esterni mutabili sono hashati, non spacciati per URL immutabili.
Whitespace dei sorgenti esterni mantenuto: non correggere raw per far passare
una verifica stilistica. Le permission negate sono evidenze, non aggirate.

## 1. Hardware effettivo

| Proprietà | Misurato | Distinzione/limite |
|---|---|---|
| VPS | football@163.5.26.155:22, alias football-vps, host key autorizzata | LigaHosting è dichiarazione del titolare; contratto/piano non verificati. I vecchi12vCPU/24GB/480GB non sono corroborati |
| CPU |6vCPU x86_64; stringa AMD EPYC7702P64-Core; AVX/AVX2/FMA/F16C, nessun AVX512 esposto | CPUID guest, non64 core assegnati. Topologia6 socket virtuali non fisica; banda RAM e CPU dedicata non provate |
| RAM |16720678912 byte=15,572GiB, identica ai campioni precedenti | RAM esposta al guest, non inventario host fisico |
| Memoria idle |Available16002220032 byte, Free12809711616 | Available include cache recuperabile; non margine durante query RAG |
| Budget |Available−4000000000=12002220032 byte | Circa12,002GB incrementali; riserva4GB decimali, non4GiB, non quota permanente |
| Swap |`/swap.img`, file,1572860KiB=1610608640 byte, usati285344KiB=292192256, priorità−2 | Su filesystem guest, non RAM. `swapon --json` non supportato; dati da `/proc/swaps`, nessuna modifica |
| Storage |virtio vda64424509440 byte=60GiB; filesystem61285326848; liberi4771864576 byte | ext4/vda1. ROTA=1 virtuale non prova HDD né NVMe fisico; non480GB |
| GPU |Solo VGA virtuale PCI1234:1111, nessun `/dev/dri` o nvidia | Nessuna GPU di calcolo esposta osservata |
| Sistema |Linux6.8.0-147-generic Ubuntu, KVM full virtualization | Non LXC nei dati osservati |
| cgroup |v2; memory.max e memory.swap.max=max sui gruppi/antenati leggibili, cpu.max antenati=max100000 | Nessuna quota più stretta osservata; resta il limite guest; hypervisor non attestato |
| Runtime |Ollama GET version0.40.5, ps vuoto prima/dopo, servizi RAG/Ollama active | llama-server osservato nei run; commit incorporato620d2225c già documentato, non nuova prova ABI |

Daemon Ollama: RSS23460KiB, mentre MemoryCurrent cgroup≈2,87GB. La lettura
supplementare distingue file2821177344 byte, inactive_file2817101824 e anon9265152.
Non sono2,87GB di heap irrecuperabile: non sommarli nuovamente ad Available.
Memoria privata/environ del processo Ollama negate; nessun sudo/cambio ACL.

RAG: RSS12692KiB, PSS7238KiB, MemoryCurrent8048640 byte; ma SwapPss e
memory.swap.current circa244MB. **L'idle RSS non è il fabbisogno attivo del RAG.**
Rientro pagine, embedding/retrieval possono aumentarlo. I20 maggiori processi
visibili non mostrano un altro grande heap da liberare: non giustificano stop
servizi per recuperare diversi GB. Picchi sotto carico non misurati. Nessuna
pulizia cache/swap o servizio fermato.

## 2. Modelli, pesi e requisiti documentati

| Modello congelato | Download complessivo, byte | GGUF principale, byte | Architettura/extra |
|---|---:|---:|---|
|Gemma4:26b Q4_K_M, digest001e5daf…ca8c|18731025629|17074419072|MoE25,2B totali/3,8B attivi; projector1194828128, draft461766752 |
|Qwen3.8:27b Q4_K_M, digestaaee06c3…7813|17741872154|16810714464|Dense27,3B con attenzione ibrida; projector931146016, MTP nei default |
|Qwen3.5:9b Q4_K_M, digest56671c2a…3c90|6550825550|5629109120|9B, attenzione ibrida, extra multimodali separati |

**File, spazio virtuale, RSS/PSS, cache recuperabile e RAM necessaria non sono
equivalenti.** Overhead: KV/stati ricorrenti, allineamento/repacking, grafo/batch,
projector/draft, runtime e servizi. Non misurato integralmente prima degli STOP.
Gli esperti totali esistono anche se solo3,8B sono attivi per token: A4B non
significa pesi di un semplice4B.

Le card ufficiali [Google](https://huggingface.co/google/gemma-4-26B-A4B-it),
[Qwen27](https://huggingface.co/Qwen/Qwen3.8-27B) e
[Qwen9](https://huggingface.co/Qwen/Qwen3.5-9B) non forniscono una garanzia numerica
applicabile a CPU-only/questa build/riserva4GB. CPU-only è supportato dal
[backend upstream](https://github.com/ggml-org/llama.cpp/blob/620d2225cc436ab0b001e3200e590e3b286ef9ab/README.md),
coerente con AVX2 e Qwen9 completato sul nostro host; per i grandi abbiamo solo
caricamenti interrotti. Nessun minimo RAM ufficiale inventato.

Distinguere formati degli autori e conversioni/catalogo Ollama: non ogni GGUF
è prodotto direttamente da Google/Qwen. Il [catalogo Gemma](https://ollama.com/library/gemma4/tags)
include Q4_K_M/Q8_0/BF16, QAT e MTP. Il [catalogo Qwen3.8](https://ollama.com/library/qwen3.8/tags)
consultato non offre Q2/Q3 da assumere ufficiali e già disponibili. Quant terze
Q2/Q3/IQ non sono automaticamente equivalenti o valide sul dominio/build.
Apache2.0 è dichiarata dalle card autori esaminate; non è parere legale su
trasformazioni terze. Nessun servizio AI remoto viene proposto.

### Cache e contesto

`num_ctx` riduce cache, non i tensori. Dal config Qwen27 congelato, la sola
componente standard K+V f16 dei16 layer full-attention,4KV head, head_dim256,
a8192 vale `2×16×8192×4×256×2=536870912` byte. Dimezzare contesto risparmia256MiB
**in quella componente**, escludendo48 layer GDN/stati ricorrenti, draft,
layout e buffer. Non è cache totale misurata. Gemma combina finestre locali,
globali e K=V: niente formula dense uniforme per tutti i layer. Nessun token
stimato dai byte. I raw non separano pesi/cache/buffer.

## 3. Ottimizzazioni: interfaccia, stato, impatto e intervento

Fonti release esatte: [API](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/api/types.go),
[envconfig](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/envconfig/config.go),
[scheduler](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/server/sched.go),
[launcher](https://github.com/ollama/ollama/blob/d919272e53593d1d55d40e1180eaa06dfbede3ac/llm/llama_server.go).
Supporto statico della revisione associata a0.40.5, **non attestazione integrale
del binario**. Nessuna riapertura H1-G2. Allowlist Environment systemd vuota,
environ Ollama negato: default del sorgente non prova l'eredità reale.

| Opzione | Supporto/versione e attuale documentato | Effetto/rischio | Intervento eventuale, non eseguito |
|---|---|---|---|
|num_ctx|API Runner; grandi8192,9B storico4096|Meno cache, rischio fonti perse/context shift; stessi pesi|Solo richiesta/driver, consenso prima |
|num_predict|API Options; grandi4096,9B2048|Cap output/tempo; non garantisce minor peak iniziale a contesto invariato|Richiesta; rischio finale incompleto |
|OLLAMA_NUM_PARALLEL|Env, default codice1; qwen35 forzato1 dal scheduler. Eredità non leggibile|Evita moltiplicare contesto, non pesi; nessun beneficio4→1 dimostrato per Qwen|Config/riavvio, non necessario ai payload sequenziali |
|OLLAMA_MAX_LOADED_MODELS|Env0=auto; override non osservato; un solo modello per run|1 evita co-residenza, non libera memoria del singolo|Config/riavvio; non corregge gli STOP osservati |
|OLLAMA_KV_CACHE_TYPE|Env→cache-type-k/v, default documentato f16; help installato elenca q8_0/q4_0 ecc.; tipo effettivo non osservato|Comprimi cache, non pesi; precisione/compatibilità architettura da verificare|Config/riavvio; non tutti i tipi garantiti sui modelli |
|OLLAMA_FLASH_ATTENTION|Env→on/off/auto nel launcher; supporto reale CPU/modello non attestato|Buffer/tempo potenzialmente minori, nessun beneficio CPU garantito|Config/riavvio; non cura universale |
|keep_alive|API;0 nei due payload grandi|Scarica dopo richiesta, non riduce peak; successivo cold load|Richiesta, già usato |
|mmap|API use_mmap, nil nei payload. Scheduler CPU sceglie false se non esplicito, righe1200–1205; launcher false→load-mode none|true lascia mappare al backend; file recuperabili, possibili copie/repack/page fault. Mode dei run non catturato|Per richiesta: unico differenziale proposto sotto |
|mlock|Non esposto nel Runner API esaminato. Help backend: load-mode mlock/mmap+mlock|Blocca pagine, non crea RAM; peggiora margine o fallisce sui limiti|Non inventare use_mlock o trasferire flag CLI nell'API |
|Draft/MTP|Default modello osservati Gemma3, Qwen4; API draft_num_predict e launcher spec-draft|Buffer/draft extra; disattivare non elimina pesi principali e cambia esperimento|Richiesta, non secondo test proposto |
|num_batch|API, default sorgente512; effettivo non misurato|Buffer/prefill più piccoli possono rallentare CPU; guadagno ignoto|Richiesta, non applicato |

Help installato storico: load-mode auto/mmap/none/mlock/mmap+mlock/dio e tipi
cache. Coerente col percorso pubblico, non prova del mode già utilizzato.
La [FAQ corrente](https://docs.ollama.com/faq) è riferimento generale, non
sostituisce la revisione0.40.5 o una prova specifica CPU/modello.

## 4. Causa dei precedenti STOP e riferimento9B

| Evidenza | Gemma26 | Qwen27 |
|---|---:|---:|
|Secondi all'arresto|28,308|32,352|
|MemAvailable minimo, byte|3763400704|3149516800|
|RSS runner massimo campionato, byte|12204212224|12878049280|
|Arresto paging persistente|No|No|
|Risposta HTTP completa|Nessuna|Nessuna|

**Dimostrato:** il monitor riserva4GB chiude il socket e ferma il test; richieste
separate, non due modelli contemporanei. Nessun OOM-killer, esaurimento totale
RAM, bug scheduler o rifiuto memoria Ollama osservato. Incrementi swap-out nei
campioni non raggiungono la guardia persistente. RSS è campionato, non peak
continuo né fabbisogno finale. Post-stop: ps vuoto, servizi active, non timestamp
esatto di cancellazione. Il protocollo ha imposto un limite operativo reale.

**Plausibile:** pesi/copie CPU, contesto e draft contribuiscono alla crescita;
il default CPU senza mmap del sorgente potrebbe spiegare memoria meno recuperabile.
**Non determinabile dai raw:** anon/file, mode effettivo, ripartizione KV/buffer,
projector, working set finale o latenza generativa. Nessun recupero tramite
nuove inferenze/log forensics. RSS alto non coincide necessariamente con basso
Available se file-backed: non introdurre una nuova soglia RSS implicita.

Il [Qwen9 storico](rag-v5-remediation-a-official-api-single-case-01.md) completò
HTTP200/done=stop in188,649s, prompt_eval_count1657/eval_count1001,4096/2048,
think=false. È eseguibilità sulla VPS, non SLA chat o prova8192/4096. Fallì
semanticamente q3_04: sette campi evidence riportavano frammenti del claim;
locator corretto, nessun witness/promozione. Non presentarlo già accurato.

La [riconciliazione RAG](quality-first-pilot-rag-state-reconciliation-01.json)
preserva V5locked/Drive11/FIGC5 e correzioni V10.1/V10.2 nei rispettivi ambiti.
Riutilizzare retrieval, ruoli/fasi, citazioni e fail-closed, senza rifare suite.
Un audit RAM non giustifica nuove patch applicative o promesse qualitative:
la supervisione umana resta necessaria finché l'accuratezza non è dimostrata.

## 5. Case history verificate

Corpi originali archiviati/hashati. Segnalazioni degli autori, non requisiti
ufficiali né dimostrazioni trasferibili a0.40.5/KVM16GB.

| Issue esistente | Ambiente/versione e tema reali | Applicabilità |
|---|---|---|
|[15704](https://github.com/ollama/ollama/issues/15704)|Gemma4:26b, Debian/Proxmox LXC32GiB CPU-only,0.20.5; rifiuto MemFree/cache|Utile per distinguere free/available; noi KVM/guardia Available, nessun rifiuto Ollama. Non stessa diagnosi |
|[6918](https://github.com/ollama/ollama/issues/6918)|Linux2024, modello non precisato, “latest mainline”, free memory/rifiuti intermittenti|Non patch attestata0.40.5 né autorizzazione al bypass |
|[15650](https://github.com/ollama/ollama/issues/15650)|Qwen3.6:35b-a3b, Docker Ubuntu15GiB+GPU16GB,0.20.7|Non Qwen3.8/CPU-only; errore500 di ammissione non osservato qui |
|[14501](https://github.com/ollama/ollama/issues/14501)|Qwen3.5 27B/35B, Windows/CUDA,0.17.0–0.17.4, secondo avvio500; host143,7GiB nei log|Non LinuxCPU16GB/0.40.5; chiusa duplicato, non prova della nostra causa |

La ricerca mirata non ha trovato una riproduzione primaria sufficientemente
equivalente Linux/CPU-only/≈16GB con stessa build/modelli/riserva4GB. Mac16GB,
GPU16GB e conversioni terze non sono benchmark trasferibili. Non ricavarne
token/s, qualità tattica o RAM minima. Nessuna ulteriore indagine aperta.

## 6. Scenari a costo zero e affidabilità delle stime

**Screening condizionale, non benchmark:** A0=16,002GB Available e12,002GB sopra
la riserva. Uso file principale W come proxy di piena residenza più overhead
**ipotetico** H=1–3GB (cache/buffer/projector/draft): footprint W+H, Available
A0−W−H. H non misurato/garantito e W non equivale a RAM. Negativi significano
assetto di piena residenza incompatibile, non RAM fisica negativa. Il calcolo
**non prova impossibilità via mmap/demand paging**, il cui working set è ignoto.

| Scenario | RAM runner di screening, GB decimali | Available/margine4GB | Latenza, paging, qualità | Affidabilità/mancanze |
|---|---|---|---|---|
|A Gemma26 Q4 corrente|18,074–20,074 piena residenza|Deficit contro riserva6,072–8,072GB|MoE non dense4B; paging possibile, nessuna risposta|Previsione bassa, STOP osservato certo; allocazioni finali ignote |
|A Gemma26 Q4 mmap=true|Non ricavabile dal file; RSS può includere file recuperabili|Deve restare Available≥4GB, nessun numero credibile preventivo|Page fault/reread e latenza possibili, stessi pesi non garantiscono stessi tempi|Ipotesi supportata dall'interfaccia, non validata; unico test proposto |
|B Qwen27 Q4 corrente o mmap|17,811–19,811 piena residenza|Deficit5,808–7,808GB|Dense tocca tutti gli strati, reread potenzialmente elevato; tempi ignoti|STOP certo, previsioni basse; nessun nuovo test Qwen proposto |
|C Gemma26 QAT catalogo|File14,439; screening15,439–17,439|Available−1,437…0,563GB, sotto4GB nello screening|Altro artefatto/precisione, qualità non garantita|Manifest projector1,195GB; nessun download, spazio insufficiente |
|C Gemma4 12B Q4_K_M|File7,381; screening8,381–10,381|Available5,621–7,621; margine+1,621…3,621|Candidato plausibile, confronto tattico9B sconosciuto|Previsione bassa, modello non installato né eseguito |
|C Qwen3.5 4B/Gemma E2B-E4B|Più piccoli nel catalogo, RAM non dal nome|Da verificare, non quote garantite|Possibile più margine; qualità rispetto9B non provata|Riserva documentale, non nuova shortlist/download |
|C quant terze Q2/Q3/IQ|Nessun artefatto congelato selezionato|Non stimabile senza identità/layout|Possibile perdita precisione, qualità non equivalente provata|Nessuna scorciatoia/test/download raccomandati |
|D Qwen3.5 9B esistente|File5,629; screening6,629–8,629|Available7,373–9,373; margine+3,373…5,373|Completamento noto, tempi dipendono da prompt/thinking; nessuna classifica tattica|Più affidabilità operativa; peak/RAG attivo e nuovo profilo ignoti |

Per D RAM guest totale ipotetica necessaria, **background idle e riserva inclusi**,
11,347–13,347GB; Gemma12,13,099–15,099GB. Sono budget condizionali, non requisiti
ufficiali o RAM misurata. Nessun token o benchmark inventato. Il margine non
sostituisce misure di RAG sotto carico o garanzie del provider.

[Manifest Gemma12Q4](https://registry.ollama.ai/v2/library/gemma4/manifests/12b-it-q4_K_M):
projector175115616 e draft465109152 byte, totale circa8,022GB.
[Manifest Gemma26QAT](https://registry.ollama.ai/v2/library/gemma4/manifests/26b-a4b-it-qat):
principale14,439GB e projector1,195GB. Con4,772GB liberi non si aggiungono questi
artefatti senza liberare spazio: nessun modello cancellato/sostituito.
Alias web possono selezionare MLX: contano runner/digest precisi; Qwen9 resta
56671c2a…3c90. Non scambiare il primo tab del catalogo per il file installato.

## 7. Economia e raccomandazione

| Classe | Scelta | Decisione |
|---|---|---|
|Zero costo, nessuna modifica|Qwen9 installato, RAG e controlli già sviluppati, richieste sequenziali|Scelta operativa immediata, qualità non certificata |
|Software senza hardware|mmap per richiesta; eventuali batch/cache/contesto/concorrenza|Serve perimetro approvato; solo mmap Gemma merita ora un differenziale, non cambiare tutto |
|Nuovo artefatto stesso piano|Gemma12 o altra quantizzazione|Richiede spazio/download e valutazione qualità; non “gratis e pronto” |
|Più hardware|RAM per piena residenza dei grandi Q4 e margine|Fuori budget; nessun preventivo, acquisto, upgrade o migrazione |

Qualità prima delle dimensioni: conservare fonti/ruoli/fasi/fail-closed, non
promuovere il9B fallito su q3_04, né sostituirlo con grandi senza output. La
guardia non prova un difetto Ollama né giustifica da sola una spesa. Non vendere
swap lenta come soluzione professionale o il12B come miglioramento automatico.

## 8. Un solo prossimo test, soltanto proposto

Fase descrittiva `gemma-mmap-on-01`, **DA FARE**, stessa attività; **non autorizzata
da questo mandato**. Nessun nuovo driver generativo preparato.

- **Delta:** solo `options.use_mmap=true` sull'identico payload Gemma V10-02
  revisione03. Stessi pesi/digest, fonti, draft/default,8192/4096, seed,900s e
  monitor03. Nuovo ledger fisso esclusivo collegato ai precedenti; max1 POST,
  nessun retry/warm-up. Non abbassare riserva4GB.
- **Ipotesi:** mappatura file-backed invece del default CPU senza mmap può
  preservare Available≥4GB durante caricamento/risposta. Più plausibile sul
  MoE che sul dense27B; non un risultato già ottenuto.
- **Prova precedente insufficiente:** opzione mai esplicita; raw non registra
  mode/anon/file e interrompe il caricamento. Non è la stessa prova con guardia
  disattivata. Compilazioni, ABI o un tokenizer alternativo non servono.
- **Prerequisiti:** consenso separato, host key/digest, nessun tentativo già
  iniziato, servizi active, lock esclusivo, memoria iniziale e nessun altro
  modello/runner; conservazione raw. Se leggibili, conservare log mode/buffer
  e campioni anon/file, senza nuovi privilegi/installazioni/configurazioni.
- **PASS operativo:** HTTP200 completo entro900s, finale non vuoto/done=stop,
  contatori nei cap, nessuna violazione memoria/paging/servizi campionata,
  modello/runner scaricato dopo. Non prova28/30 o latenza interattiva.
- **FAIL:** rifiuto esplicito opzione, soglia RAM/paging, timeout/budget o
  risposta incompleta. Nessun secondo invio. **BLOCCATO** prima invio per
  prerequisiti mancanti/duplicato. Ambiguità dopo invio: STOP e prove incomplete.
- **Limite causale:** se il mode reale non è osservabile, annotarlo senza
  inventarlo; separare eventuale completamento operativo. Non aprire altre
  indagini o varianti a catena dopo il test. Nessun cambio simultaneo contesto,
  draft o precisione per farlo finire.
- **Rischi:** repacking/copie possono annullare il beneficio; file reread e CPU
  possono aumentare molto la latenza. Available non è working set né SLA RAG.
  Protezioni campionate/socket chiuso non dimostrano cancellazione istantanea.

## Chiusura

Due SSH read-only: inventario con4 GET version/tags/ps prima/dopo, poi quattro
soli file cgroup per cache/anon/swap. Exit0, stderr SSH vuoti; allowlist ambiente,
nessun segreto/privata/ambiente completo registrato. Piccoli sorgenti/header
pubblici locali per analisi statica, nessuna toolchain o libreria caricata.

**Inferenze0, POST generative0, caricamenti0, lock acquisiti0, modelli scaricati0,
modifiche VPS0, costi aggiuntivi0.** Nessuna modifica RAG/panel/riserva.
Audit concluso, nuova fattibilità/qualità non validate. Report/TODO/registro
contestuali, pubblicazione e working tree verificati, STOP. Qualsiasi intervento
o test successivo attende autorizzazione esplicita del titolare.
