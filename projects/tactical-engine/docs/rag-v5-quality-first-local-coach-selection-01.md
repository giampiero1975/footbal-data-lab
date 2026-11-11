# Selezione dell'allenatore locale — qualità prima della fattibilità

Data: 2026-11-11. Attività: `RD-RAG-V5-LOCAL-COACH-QUALITY-FIRST-SELECTION-01`.

## Risposta alla domanda decisiva

**Nessun candidato ha evidenze sufficienti per prevedere 28/30 in tattica.**
La priorità di potenziale generale è **Qwen3.8 27B**, come ipotesi di lavoro:
riunisce risultati pubblici su ragionamento, istruzioni e compiti complessi.
Non è un vincitore tattico dimostrato né un primato globale fra tutti gli
open-weight. Per il **compromesso da mettere per primo alla prova sulla
CPX52** indico **Gemma 4 26B-A4B**, con riserva esplicita di RAM e latenza.

Il motivo non è che occupi meno del 12B: occupa di più. La sua tabella di
famiglia riporta vantaggi sul 12B in diversi test di ragionamento, mentre
il MoE offre una prospettiva di calcolo attivo ridotto rispetto al dense 27B.
Sono indizi pertinenti alla qualità e all'efficienza, non una misura del
costo per risposta utile. Non è dimostrato che il 26B regga con i servizi
sui 24 GB; se non regge, la raccomandazione è falsificata, non si autorizza
un upgrade o una sostituzione automatica con il 12B.

**Correggo quindi la priorità precedente**: Gemma 12B resta candidato e termine
di confronto, non vincitore qualitativo o scelta automatica. Il nuovo mandato
accetta di valutare un compromesso più impegnativo quando esiste un vantaggio
qualitativo documentato da verificare. Non è una migrazione approvata.

## Riconciliazione e perimetro

HEAD locale e GitHub iniziale `d52feaeacf9563da73e22e6baf8f551ac3e7fde9`, branch
`codex/tactical-state-contract-v1`, working tree iniziale pulito. TODO, registro
e i due report richiesti confrontati byte-per-byte con GitHub allo SHA esatto.
Consultati inventari storici, rubrica holdout, `compare_frozen_thinking_rd01.py`
e caller `chat()` in `smoke_test_rag_v5_e2e.py`, senza import o esecuzione.
Il caller contiene `think=false`, sanitizzazione e possibili repair: i suoi
risultati non equivalgono a misure del potenziale in thinking o del solo raw.

Differenza sostanziale: target strategico **28/30**, capacità pesate prima
della RAM, nuove evidenze comparative e quattro alternative aggiuntive.
Nessun audit o test storico ripetuto. Questo report integra la decisione;
non riscrive risultati, soglie, prompt, codice o report precedenti.

Metodo/script: analisi statica, GET pubbliche di documenti e piccoli metadati,
confronti Git e hash locali; nessuno script applicativo nuovo. Inventario:
[`local-coach-quality-first-evidence-01.json`](local-coach-quality-first-evidence-01.json).
Revisioni esatte e SHA-256 delle risposte pubbliche conservati; snapshot dei
soli metadati/config in `local-coach-quality-first-sources-01/`. Le card e due
pagine HTML sono state lette, non ripubblicate integralmente; i loro hash sono
hash della risposta acquisita, non hash di un file locale inesistente.
Nessun peso, tokenizer o eseguibile scaricato/eseguito.

**DOCUMENTATO (D)**: risultato dichiarato dal produttore, studio indipendente
o evidenza storica identificati come tali. **STIMATO (S)**: inferenza tecnica
condizionale. **MISURATO (M)**: nessuna nuova misura locale di qualità, RAM o
velocità. Queste classi e la dicitura **EVIDENZA INSUFFICIENTE (EI)** descrivono
le prove, non sono stati operativi del progetto.

## Fase A — matrice delle cinque capacità

I pesi 35/25/20/15/5 guidano la ricerca; non moltiplico benchmark eterogenei
per ottenere un punteggio. Il 35% riguarda tattica: GPQA/AIME sono soltanto
proxy di ragionamento generale. Anche con proxy disponibili, il livello
professionale di ogni dimensione resta da dimostrare.

| Candidato esatto | Ragionamento tattico/problem solving 35% | Coerenza logica/spaziale/temporale 25% | Grounding/non invenzione 20% | Istruzioni/scenari 15% | Italiano tecnico 5% |
|---|---|---|---|---|---|
| Qwen/Qwen3.5-9B | D: GPQA Diamond 81,7; tattica storica parziale, non 28/30 | D: MultiChallenge 54,5; errori di fase/grounding nei nostri artefatti | D: AA-LCR 63,0 è comprensione, non fedeltà; fallimento locale q3_04 | D: IFEval 91,5 / IFBench 64,5 | D: multilingue; EI sulla qualità professionale italiana |
| google/gemma-4-12B-it | D: GPQA Diamond 78,8, AIME26 77,5; EI tattica | D: BBEH 53,0; EI ruoli e trasformazioni calcistiche | D: MRCR 43,4 a 128K; EI fedeltà per-claim | D: tool use pubblicato; EI confronto diretto di istruzioni complesse del coach | D: MMMLU 83,4 aggregato; EI prosa tattica italiana |
| Qwen/Qwen3-30B-A3B originale | D: card/relazione originaria, modalità ibrida; EI confronto omogeneo col nostro assetto | EI per coerenza tattica; non eredita automaticamente i risultati 2507 | EI fedeltà sul nostro input | D: thinking attivabile/disattivabile; EI trasferimento ai vincoli del coach | D: multilingue dichiarato; EI italiano tecnico |
| Qwen/Qwen3-30B-A3B-Instruct-2507 | D: GPQA 70,4, non-thinking; EI tattica | D: ZebraLogic 90,0, proxy logico; EI calcio | EI grounding e astensione sulle fonti tattiche | D: IFEval 84,7 | D: MMLU-ProX 72,0 aggregato; EI italiano tecnico |
| Qwen/Qwen3-30B-A3B-Thinking-2507 | D: GPQA 73,4 / AIME25 85,0, thinking-only; EI tattica | D: LiveBench 20241125 76,8 aggregato; EI dinamica calcistica | EI fedeltà tattica; long-context non basta | D: IFEval 88,9, modalità diversa da Instruct | D: MMLU-ProX 76,4 aggregato; EI italiano tecnico |
| google/gemma-4-26B-A4B-it | D: GPQA Diamond 82,3 / AIME26 88,3; EI tattica | D: BBEH 64,8, vantaggio di famiglia sul 12B; EI calcio | D: MRCR 44,1 a 128K; studio TruthfulQA è veridicità, non grounding RAG | D: Tau2 68,2, non misura completa delle istruzioni del coach | D: MMMLU 86,3 aggregato; EI prosa professionale |
| Qwen/Qwen3.8-27B | D: GPQA Diamond 89,2 / HLE 30,8; EI tattica | D: compiti agentici e multi-step; EI ruoli/lati/fasi calcistici | EI: lavoro con documenti e ricerca non prova citazioni fedeli o astensione | D: IFBench 79,5; CoWorkBench è anche valutazione interna del produttore | D: modello multilingue; EI confronto professionale italiano |
| mistralai/Ministral-3-14B-Reasoning-2512 | D: GPQA Diamond 71,2 / AIME25 85,0; EI tattica | D: proxy STEM/coding; EI coerenza calcistica | EI fedeltà alle fonti e incertezza calibrata | D: supporto system dichiarato; non trasferire punteggi Instruct alla variante Reasoning | D: italiano fra lingue supportate; EI qualità tattica |
| nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16 | D: GPQA no-tools 73,0 / AIME25 89,1; EI tattica | D: Multi Challenge 38,5; EI calcio | D: AA-LCR 35,9, RULER sono proxy; EI fedeltà | D: IFBench 71,5; non domina in tutte le prove | D: italiano dichiarato; EI esposizione tecnica |
| zai-org/GLM-4.7-Flash | D: GPQA 75,2 / HLE 14,4; EI tattica | D: Tau2/agentic, EI trasformazioni calcistiche | D: BrowseComp è ricerca, non fedeltà RAG; EI astensione | D: Tau2 79,5 con protocollo specifico; EI generalizzazione | EI italiano tecnico; card marcata inglese/cinese, non prova di incapacità italiana |
| Qwen/Qwen3.6-35B-A3B | D: GPQA 86,0 nella tabella del produttore; EI tattica | D: DeepPlanning 25,9; EI calcio | EI grounding delle risposte autonome | D: coding/agent e preservazione thinking; EI coach | D: multilingue; EI italiano professionale |

I numeri sono percentuali pubblicate salvo score aggregati esplicitamente
indicati; non sono nostri sottovoti. **EI sul calcio vale per tutte le righe**:
nessuna somma pesata né conversione in /30 è giustificata.

### Qualità e provenienza delle prove

Le card precise, tutte con revisioni nell'inventario, sono fonti **ufficiali del
produttore**, non valutazioni indipendenti:
[Qwen9](https://huggingface.co/Qwen/Qwen3.5-9B),
[Gemma12](https://huggingface.co/google/gemma-4-12B-it),
[Gemma26](https://huggingface.co/google/gemma-4-26B-A4B-it),
[Qwen27](https://huggingface.co/Qwen/Qwen3.8-27B),
[originale](https://huggingface.co/Qwen/Qwen3-30B-A3B),
[Instruct2507](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507),
[Thinking2507](https://huggingface.co/Qwen/Qwen3-30B-A3B-Thinking-2507),
[Ministral](https://huggingface.co/mistralai/Ministral-3-14B-Reasoning-2512),
[Nemotron](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16),
[GLM](https://huggingface.co/zai-org/GLM-4.7-Flash),
[Qwen35](https://huggingface.co/Qwen/Qwen3.6-35B-A3B).

**D, indipendente con limiti:** lo studio
[2604.07035v3, testo completo](https://arxiv.org/html/2604.07035v3)
confronta sette configurazioni su ARC/GSM8K/MATH/TruthfulQA; trova Gemma26
competitivo sotto protocollo comune. Usa H100, batch uno, BF16, non Q4 CPU;
non include Qwen3.8 27B o Gemma12. Segnala revisioni non congelate in origine,
correzioni al dataset a scelta multipla e sensibilità ai prompt. Abstract e
HTML restituiscono aggregati differenti: non uso quel totale nella selezione.
È un indizio indipendente circoscritto, non prova decisiva per questa VPS.

**D, valutatore indipendente:** la
[pagina Artificial Analysis](https://artificialanalysis.ai/models/releases/comparisons/qwen3-8-27b-vs-gemma-4-26b-a4b)
distingue xhigh/medium/low/non-reasoning per Qwen27; manca un indice Gemma26
comparabile nell'attuale tabella. Non invento il dato mancante. Tempi e prezzi
di provider non sono tempi o costi CPU locali, e non sono usati come tali.

**D, protocolli pertinenti, risultati mancanti:**
[BBEH](https://github.com/google-deepmind/bbeh) copre ragionamento difficile,
[IFBench](https://github.com/allenai/IFBench) istruzioni,
[FaithEval](https://github.com/SalesforceAIResearch/FaithEval) contesti incerti,
inconsistenti o controfattuali. Quest'ultimo sarebbe più pertinente a grounding
e astensione rispetto a MRCR, ma non ho una tabella controllata di questi
checkpoint. [Evalita-LLM](https://arxiv.org/abs/2502.02289) considera italiano
nativo e compiti generativi; non dispongo di risultati omogenei di tutti i
candidati esatti. Multilingue non equivale a terminologia UEFA A/Pro corretta.

### Modalità, quantizzazione e protocollo

Le release Instruct e Thinking Qwen30 sono distinte: `think=false` non rende
Thinking-2507 equivalente a Instruct. Qwen27 abilita thinking per default e
presenta livelli di effort; il livello corrispondente a ogni numero della
card non è integralmente ricostruito dalle note disponibili. La tabella
Gemma confronta la famiglia, ma non isola uniformemente budget e thinking
per ogni metrica. Non attribuisco quei numeri a `think=false` o a Q4_K_M.
Le card mostrano BF16/asset pubblici; precisione e budget esatti dei singoli
run non sono sempre verificabili. GLM dichiara per molte prove temperature 1,
top-p 0,95 e fino a 131072 nuovi token, molto diverso dai nostri limiti CPU.
I budget generosi non possono essere assunti gratuiti o mantenuti senza misure.

Non uso annunci come «frontier», «strongest» o «best-in-class» come benchmark.
Risultati di modelli Instruct/Base o con strumenti non vengono assegnati alla
variante Reasoning/no-tools. Nessun supporto osservato consente di predire
non-invenzione o capacità di riconoscere ogni insufficienza delle fonti.

### Graduatoria qualitativa parziale

1. **Qwen3.8 27B: priorità di potenziale generale**, per il quadro di
   ragionamento/istruzioni/compiti complessi pubblicato. È una sintesi
   documentale, non un rango numerico o una superiorità provata su Gemma26.
2. **Gemma26: co-finalista con evidenza di famiglia e indipendente utile**.
   Non può essere subordinato al 12B per la sola RAM. Il vantaggio non vale
   per ogni benchmark: la tabella Tau2, per esempio, non favorisce il 26B.
3. **Altri candidati non ordinabili globalmente**: Gemma12, Qwen9, Qwen30
   nelle tre versioni, Qwen35, Ministral, Nemotron e GLM hanno vantaggi o prove
   differenti; non emerge una superiorità tattica complessiva. Qwen35 resta
   interessante qualitativamente, non escluso perché più grande. Le tabelle
   Qwen mostrano inoltre Qwen9 competitivo con il vecchio Qwen30 Thinking:
   aumentare i parametri non è una correzione dimostrata del nostro problema.

La frontiera è parziale. Non esiste qui un'alternativa che domini dimostratamente
tutte le altre su qualità, costo e latenza. La ricerca include quattro nuove
alternative pertinenti, non pretende di censire tutti i checkpoint mondiali.
Release enormi non diventano sostenibili perché hanno pochi esperti attivi:
[Mistral Small 4](https://mistral.ai/news/mistral-small-4/) distingue 119B totali
e 6B attivi; i soli pesi teorici a 4 bit richiederebbero circa 59,5 GB, prima
degli overhead. Non è equivalente al piccolo Ministral qui esaminato.

## Fase B — fattibilità, dopo la qualità

Infrastruttura dichiarata, non rilevata nuovamente: CPX52, 12 vCPU, 24 GB RAM,
480 GB NVMe, nessuna GPU, Ollama storico 0.40.5. **Nessuna SSH autorizzata.**
La disponibilità di un tag/GGUF documenta un percorso locale; non dimostra il
funzionamento sulla build installata. Non confronto versioni con ordinamento
lessicografico né deduco il supporto da un numero di release.

| Candidato | D: artefatto locale concreto / licenza | S: RAM, calcolo, latenza e convivenza | Valutazione di fattibilità, non stato progetto |
|---|---|---|---|
| Qwen9 | `qwen3.5:9b`, baseline già utilizzata; Apache-2.0. Non rifaccio l'inventario del peso installato | Funzionamento storico D, picco/servizi attuali non rilevati. Dense con attenzione ibrida; non garanzia di qualità | Funzionamento storico verificato nel proprio perimetro; stato attuale non rilevato |
| Gemma12 | Q4_K_M catalogo circa 8 GB, Apache-2.0 | Dense 12B, carico inferiore di pesi rispetto ai 19 GB; picco, cache, draft e velocità non misurati | Plausibile, runtime/risorse da verificare |
| Qwen30 originale | Q4_K_M circa 19 GB, Apache-2.0 | 30,5B totali / 3,3B attivi; cache/buffer/OS oltre pesi, margine severo | Da verificare, nessuna impossibilità assoluta dichiarata |
| Qwen30 Instruct2507 | Tag esplicito Q4_K_M circa 19 GB, Apache-2.0 | Stesso rischio memoria, risposta diretta senza thinking; capacità distinta | Da verificare |
| Qwen30 Thinking2507 | Release scaricabile, famiglia Q4 circa 19 GB; alias generico non identità sufficiente, Apache-2.0 | Memoria non quella di un 3B; thinking aggiunge token/tempo; digest preciso da congelare prima di uso | Da verificare |
| Gemma26 | `gemma4:26b` llama.cpp Q4_K_M circa 19 GB, hash breve `001e5dafc3c7`, Apache-2.0 | 25,2B totali / 3,8B attivi; attenzione locale/globale, draft/projector da contabilizzare se presenti; margine incerto | Da verificare, prospettiva MoE credibile ma non sostenibilità dimostrata |
| Qwen27 | `qwen3.8:27b` llama.cpp Q4_K_M circa 18 GB, hash breve `aaee06c39dcf`, Apache-2.0 | 27,3B nel catalogo; dense, attenzione ibrida. Calcolo e traffico dei pesi possono rendere la CPU lenta | Da verificare, qualità potenziale contro latenza |
| Ministral Reasoning14 | GGUF ufficiale Q4_K_M 8239591488 byte, LFS SHA in inventario; Apache-2.0 | Dense 13,5B testo + 0,4B visione; cache e ragionamento non gratuiti. Il tag Ollama ordinario non identifica necessariamente Reasoning | Plausibile, import/runtime esatto da verificare |
| Nemotron Nano30 | Catalogo llama.cpp Q4_K_M circa 24 GB; NVIDIA Nemotron Open Model License, uso commerciale dichiarato, condizioni specifiche da conservare | MoE/Mamba/attenzione; non adottare il valore MLX 18 GB come peso llama.cpp. Pressione estrema nel profilo da 24 GB | Profilo esposto non giustificato sul budget attuale; altre quantizzazioni non validate, non impossibilità del modello |
| GLM Flash | `glm-4.7-flash:q4_K_M` circa 19 GB, MIT | MoE 30B-A3B; rischio memoria e token di thinking. Italiano/integrazione ancora incerti | Da verificare |
| Qwen35 | `qwen3.6:35b-a3b` Q4_K_M circa 23 GB, Apache-2.0 | 35,5B totali / circa 3B attivi; budget residuo altamente critico con RAG | Profilo Q4 senza margine dimostrato; non esclusione qualitativa né prova d'impossibilità |

Fonti catalogo: [Gemma26](https://ollama.com/library/gemma4:26b),
[Qwen27](https://ollama.com/library/qwen3.8:27b),
[Nemotron](https://ollama.com/library/nemotron-3-nano:30b),
[GLM](https://ollama.com/library/glm-4.7-flash),
[Qwen35](https://ollama.com/library/qwen3.6:35b-a3b),
[GGUF ufficiale Ministral](https://huggingface.co/mistralai/Ministral-3-14B-Reasoning-2512-GGUF).
Per le altre identità riuso il confronto precedente. Nessun GGUF scaricato.
Licenze dichiarate e pesi disponibili non sono prove di prestazioni; Nemotron
ha termini propri, non viene rinominato Apache. Nessun servizio cloud è candidato.

### Memoria operativa e costo computazionale

Il budget completo è `pesi residenti + cache/stato ricorrente + buffer + runtime
+ componenti ausiliari + OS + RAG/API/panel + margine`. Mmap non rende gratuiti
i pesi: paging e saturazione della banda possono rendere impraticabile una
configurazione che tecnicamente si avvia. Latenza e throughput non sono noti.
Più parametri attivi indicano più lavoro potenziale, non un rapporto esatto
fra token/s; i MoE non occupano la RAM dei soli parametri attivi.

I config esatti conservati mostrano Gemma26 con 25 layer sliding e 5 globali,
Qwen27 con 48 layer lineari e 16 full-attention. Sono ragioni per non usare
la formula di una cache full-attention omogenea su tutti i layer. Non sono
misure del risparmio della build presente. Riutilizzo, senza nuovo test, la
stima Qwen30 già pubblicata: 0,75 GiB di sola cache F16 ipotetica a 8192,
una sequenza. Non la trasferisco agli altri modelli.

Non fornisco picchi totali fittizi: formato cache, buffers, pesi residenti,
ausiliari e memoria dei servizi non sono noti. Il vaglio documentale può
classificare il rischio, non certificare che 18/19 GB lascino un margine reale.
Anche l'unità effettiva dei 24 GB e MemAvailable richiedono lettura autorizzata.
Per tutti: una sola generazione alla volta, risorse per servizi conservate,
nessun uso di swap come espediente per dichiarare un PASS. Se il runtime non
supporta il checkpoint senza modifiche autorizzate, la prova è **BLOCCATO**.

## Fase C — economia della qualità e scelta

Costo VPS mensile **P** da fattura, non noto: non stimo una tariffa pubblica al
posto del contratto. Nessun nuovo acquisto o rinnovo approvato. Per il periodo
già pagato il costo marginale di hosting può restare invariato, ma il costo
allocato del servizio, lavoro, revisore e integrazione non è zero.

`Costo per risposta utilizzabile = (hosting attribuibile + revisione +
integrazione attribuibile) / numero di risposte giudicate utilizzabili`.
Il denominatore richiede revisione tattica/fedeltà indipendente, non HTTP200 o
JSON valido. Senza volumi, latenza, fattura e tasso di utilità non calcolo euro
per risposta. Thinking lungo o interventi manuali possono annullare un vantaggio
apparente; un modello economico che produce errori non è economico per il coach.

| Alternativa | Rapporto qualità/risorse documentabile | Cosa impedisce una dominanza dimostrata |
|---|---|---|
| Qwen27 | Miglior priorità di potenziale generale nella selezione; pacchetto circa 18 GB | Dense CPU e modalità di reasoning; nessuna misura costo/utilità locale |
| Gemma26 | Miglior **ipotesi di compromesso**: segnali qualitativi sul 12B, MoE attivo ridotto, circa 19 GB | RAM severa e vantaggio CPU non misurato; può fallire il filtro |
| Gemma12 / Ministral14 | Candidati a pressione memoria più contenuta e capacità generali pubblicate | Non dimostrano qualità maggiore o sufficiente al nuovo obiettivo |
| Qwen9 | Integrazione storica e costo di cambiamento minimo | Fallimenti locali, nessuna media professionale 28/30 dimostrata |
| Qwen30 / GLM / Nemotron / Qwen35 | Compromessi reali di reasoning, istruzioni e sparsità | Nessun vantaggio tattico complessivo provato; memoria/precisione/template/budget da verificare |

**Scelta operativa eventuale:** porterei Gemma26 al primo confronto con Qwen27,
non introdurrei direttamente nessuno in produzione. Se obbligato a indicare
oggi un solo candidato per una CPX52 sostenibile, sceglierei **Gemma26** come
ipotesi da falsificare; se la domanda fosse soltanto potenziale generale,
indicherei **Qwen27**. Nessuna delle due frasi significa «raggiungerà 28/30».
Non esiste ancora un miglior costo per risposta corretta misurato.

Ribalterebbero la scelta: superiorità tattica in cieco del Qwen27 con RAM/tempi
sostenibili; insostenibilità Gemma26; oppure un candidato più leggero che,
a parità di fonti e budget, raggiunga lo stesso obiettivo a costo inferiore.
Il collo di bottiglia potrebbe restare nel retrieval o nei contratti: cambiare
modello non è una diagnosi causale, e non autorizza a modificare il RAG.

## Come misurare 28/30 senza riscrivere la storia

I cinque pesi strategici sono una matrice di selezione documentale distinta
dalla rubrica tattica RD-THINK già congelata: correttezza 35, copertura 25,
coerenza ruolo/lato/fase 20, supporto documentale 15, vincoli 5. Non sostituisco
questi ultimi con i nuovi pesi e non converto score 0–2 o benchmark in /30.

Una valutazione futura deve mantenere domande e criteri congelati, giudizio
umano esperto in cieco, voto /30 motivato con i criteri già esistenti e audit
per affermazione/fonte della rubrica holdout. Se la griglia completa per
attribuire /30 non è disponibile, va concordata prima: non inventarla dopo
aver letto gli output. Riportare voti individuali, media aritmetica e tutti
gli errori gravi; media almeno 28/30 **e zero errori gravi** è il nuovo criterio,
non un risultato. Fedeltà non verificata non riceve un PASS.

La lode rimane un riconoscimento qualitativo motivato del revisore su risposte
30/30, non 31 punti, non un moltiplicatore. I target storici 9/10 e 26/30
restano nelle attività originarie. Un pilot development o dieci casi noti
non certificano generalizzazione UEFA A/Pro o un vero holdout indipendente.

## Una sola prossima verifica minima — proposta, non eseguita

Identificativo **RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01**, stato **DA FARE**,
richiede autorizzazione separata. Confronto accoppiato **Gemma26 / Qwen27**
su tre casi storici difficili congelati: V10 case_02, V10 case_03 e V10.2
case_10, con domande/fonti versionate e hash dall'inventario storico. Sei
risposte autonome nuove al massimo, nessuna rigenerazione della baseline Qwen9.

Differenza tecnica preventiva: nessuno dei due motori/artefatti è stato
confrontato così; thinking esplicito entro un budget totale e nuovo target
28/30, al posto del precedente candidato Gemma12/direct-answer. Non è una
ripetizione di q3_04, extraction o suite deterministiche. I casi noti servono
solo a scegliere l'ipotesi, non a certificare il target professionale.

Metodo futuro: driver single-shot separato, **non implementato qui**; niente
uso cieco di `chat()` che forza thinking off e può riparare il raw. Stesse
fonti/domande/istruzioni semantiche, template nativo corretto per ciascun
modello, nessun Gold nel prompt, reasoning attivo per entrambi solo se
supportato verificabilmente. Un solo punto operativo predefinito, contesto
8192, massimo 4096 token complessivi di reasoning+risposta, risposta finale
entro 350 parole, limite 900 secondi per richiesta e massimo 5400 secondi
per sei richieste, zero retry/repair/routing. Sono tetti proposti, non misure
di sostenibilità né riproduzione dei budget dei benchmark pubblici.

Prerequisiti: periodo VPS già pagato sufficiente e extra canone/hardware zero;
revisore sostenibile; identità/digest/template e supporto locale verificabili;
prompt realmente contenuto nel contesto; servizi necessari attivi. Freeze di
payload, schema assente se non richiesto dal compito, parametri comuni e
specifiche native prima dell'invio. Qualsiasi incompatibilità di parametri va
risolta nel mandato separato, senza fallback o aggiornamento automatico.
Il nuovo driver e le verifiche risorse richiedono autorizzazione prima di
installazioni/download/SSH/inferenze; oggi nulla di tutto questo è stato fatto.

Evidenze attese: raw immutati, ledger delle sei richieste, completamento e
troncamenti, token/tempi, picco RAM/MemAvailable e swap con servizi, voti ciechi
motivati e verifica claim-fonte. L'ordine dei modelli va predefinito e alternato;
un solo modello caricato alla volta, senza interrompere servizi.

**PASS del pilot**: entrambi tecnicamente completi nel budget e senza violare
il margine prudenziale proposto di almeno 4 GB MemAvailable né swapping
persistente; emerge una preferenza tattica motivata senza errori gravi. Se
pari, nessun vincitore. **FAIL**: modello entro il perimetro ma output errati,
non fedeli, incompleti/troncati o fuori budget; non correggere per far passare.
**BLOCCATO**: prerequisiti, compatibilità, revisore o risorse mancanti; STOP
prima dell'invio interessato. Al primo rischio risorse/arresto tecnico fermare
il pilot, conservare evidenze, nessun altro modello di ripiego o retry.

Un risultato 28/30 su soli tre casi, anche ottenuto, non dimostra una media
professionale generalizzabile; il pilot discrimina la scelta e il costo
osservato per risposta utile, non integra o certifica l'allenatore.

## Tracciamento e stato finale

Attività → metodo/script di analisi documentale → commit contestuale con
report/evidenze/TODO/registro → questo report → graduatoria parziale e due
priorità esplicite → decisione di sostituire la selezione prudenziale con
l'ipotesi quality-first → analisi **ESEGUITO**. Il commit è quello che introduce
questo file, ricavabile da Git senza uno SHA autoreferenziale inventato.

Il pilot resta **DA FARE**, non autorizzato; il vecchio protocollo non è
riscritto o eseguito. Accuratezza 28/30, compatibilità/risorse dei candidati,
Gate, integrazione e certificazione generale restano **BLOCCATO** fino alle
rispettive evidenze. Nessuna SSH, installazione, pesi, inferenza, benchmark,
modifica al codice/prompt/RAG/corpus/API/panel/VPS/runtime, merge o deploy.
STOP dopo pubblicazione e verifica GitHub/working tree.
