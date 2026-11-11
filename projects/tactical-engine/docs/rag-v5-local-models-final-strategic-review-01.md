# Revisione strategica finale — motore locale e open-weight

Data: 2026-11-11. Attività:
`RD-RAG-V5-LOCAL-MODELS-FINAL-STRATEGIC-REVIEW-01`.

## Decisione unica

**VERIFICA DECISIVA**, esclusivamente locale, con **Gemma 4 12B** come unico
candidato da sottoporre eventualmente a confronto. Non è una migrazione
approvata né un test autorizzato. Le evidenze non consentono di promettere
26/30 o di dichiarare il progetto irrimediabilmente irrecuperabile.

Il mandato è stato corretto durante la sessione: autonomia completa del
motore, pesi scaricabili e nessun fornitore remoto di inferenza. La ricerca
precedente sui servizi proprietari è esclusa dalla decisione; la relativa
bozza di evidenza, mai committata o pubblicata, è stata rimossa. Nessun suo
candidato, prezzo o budget è usato qui. Il confronto proposto è tra motori
eseguiti autonomamente, con valutazione umana indipendente, non un servizio
cloud o un'altra AI che completa la risposta.

La raccomandazione resta subordinata a **nessun nuovo rinnovo VPS necessario
soltanto per tentare il confronto**. Usare eventualmente il periodo già
pagato. Se mancano tempo residuo, risorse, compatibilità del runtime o un
revisore sostenibile, fermarsi e preservare gli asset; non sostituire il
vincolo locale con un servizio esterno o con nuovo hardware acquistato.

## Riconciliazione ed evidenze

Branch `codex/tactical-state-contract-v1`, HEAD iniziale locale e GitHub
`9c5178891eac8adc00299009a86a88a9aca2ceb0`, working tree iniziale pulito.
TODO/Experiment Register ufficiali confrontati anche con raw GitHub al commit
esatto. Consultati report sul valore del coach e inventario, dieci risposte
finali, raw q3_04 e diagnosi già conclusa, report V9/V10, RD-THINK, rubriche,
caller RAG, embedding/reranker e percorsi opt-in dei contratti. Nessuna suite,
inferenza, scansione VPS, benchmark o attestazione ABI ripetuti.

Evidenza nuova:
[`local-models-final-strategic-review-evidence-01.json`](local-models-final-strategic-review-evidence-01.json),
con fonti ufficiali, revisioni pubbliche dei tre modelli, licenze dichiarate,
dieci file storici e hash, limiti di memoria/costo e autorizzazioni false.
Le tre risposte pubbliche di metadati e il testo LICENSE Qwen acquisito sono
conservati byte-per-byte in `docs/local-models-public-metadata-01/`; non
contengono pesi del modello e non attestano il binario Ollama installato.
La differenza rispetto al report precedente è la verifica di candidati
**locali** e fattibilità sulla macchina dichiarata, non una rivalutazione
numerica arbitraria delle risposte già esaminate.

Le dieci risposte conservate sono: V10 casi 1,2,3,4,7,9; V10.1 casi 5,6,8;
V10.2 caso 10, sotto `evaluation/coverciano-remediation-*`. Percorsi esatti
nell'inventario nuovo e in quello precedente. Hanno domanda, risposta e
sei evidenze ciascuna; non hanno incorporato il payload completo originale.
Alcune risposte hanno repair o sanitizzazione: non sono dieci nuove domande
indipendenti né dieci prime risposte incontaminate.

Stato noto da documenti, **non stato live rilevato oggi**: Qwen 3.5 9B,
Ollama 0.40.5, retrieval locale, embedding Qwen separato, reranker CPU e
validazioni Python. La baseline Coverciano resta 19,90/30 come dato storico;
V9/V10 hanno successi tecnici senza nuova media esterna. Locked e Drive11
mantengono i propri risultati circoscritti. I contratti recenti non hanno
ancora dimostrato qualità generale del coach.

## Quattro cause: fatti, incertezze e possibilità di risoluzione

| Livello | Evidenza verificabile | Impatto | Certezza e risoluzione concreta |
|---|---|---|---|
| A — Qwen 9B | RD-THINK off produce trasformazioni 4-3-3→3-5-2 incompatibili a contesto congelato; q3_04 duplica claim su evidence | Consigli non affidabili su ruoli, geometria e fedeltà; failure anche oltre il solo JSON | Alta sull'errore nell'output, non sulla causa intrinseca. Non dimostrato che un modello alternativo lo eviti: serve il confronto, non fine-tuning presunto |
| B — RAG | Audit autonomia e baseline mostrano retrieval di fase/prospettiva sbagliata, omissioni e astensione sul fuorigioco | Un modello migliore può ricevere comunque dati insufficienti o incongrui | Alta sui casi storici, non su ogni query attuale. Riutilizzare estratti già salvati per separare una prima valutazione del generatore, senza altro retrieval |
| C — Architettura | Prompt grounded-only, composizione di istruzioni, repair e gate che hanno ammesso risposte contraddittorie; ultimo locator respinge correttamente il fuori-lato | Vincoli possono limitare l'applicazione; gate formali non certificano il piano tattico | Alta sui comportamenti documentati; contributo causale di complessità/istruzioni non isolato. Provare il percorso naturale già esistente senza imporre extraction come prerequisito di qualità |
| D — Valutazione | Voti 29–30 talvolta riferiti a riscritture; dieci casi development; versioni diverse; confronto omogeneo assente | Sovrastima della competenza e impossibilità di misurare un progresso generale | Alta. Revisore umano indipendente, testi immutati e valutazione cieca possono correggere l'attribuzione; nessuna nuova infrastruttura AI necessaria |

Non è identificabile il contributo percentuale di ciascun livello. **Non è
dimostrato che Qwen sia il principale limite; l'architettura contribuisce
in modo sostanziale nei casi documentati.** Cambiare modello non risolve
automaticamente retrieval, prospettiva, fonti mancanti, rubriche o falsi PASS.

Già corretti nei rispettivi perimetri: correlazioni status/contenuto della
remediation A, testo numeric/literal dopo R1, diagnostica dei boundary,
numerosi difetti deterministici di scope e promozione. Non sono da rifare.
Ancora osservati: duplicazione fuori lato, errori relazionali e assenza della
prova indipendente del coach. Soltanto ipotesi: modello troppo piccolo,
prompt troppo complesso o contesto effettivamente troncato come causa dominante.

## Infrastruttura: 24 GB non sono un budget interamente disponibile al modello

Dati **forniti dal titolare**, non rilevati via SSH: Hetzner CPX52, 12 vCPU,
24 GB RAM, 480 GB NVMe, nessuna GPU dedicata. Unità GB/GiB, RAM realmente
disponibile, limiti cgroup, banda di memoria, contesa vCPU e spazio libero
non sono stati misurati. NVMe capiente e più vCPU non equivalgono a GPU o RAM.

Il picco fisico deve comprendere pesi residenti, KV/cache o stato ricorrente,
buffer e attivazioni, runtime, eventuale projector/draft MTP, embedding/reranker
se ancora caricati, Chroma, API/panel, sistema operativo e margine operativo.
Non sommare due volte pagine mmap condivise/page cache come se fossero memorie
distinte. Dimensione GGUF, spazio virtuale, RSS/PSS e memoria totale di sistema
sono misure diverse. Swap/paging su NVMe non rendono sostenibile un modello
che non rientra nel budget fisico richiesto.

Le [indicazioni ufficiali Google](https://ai.google.dev/gemma/docs/core)
distinguono memoria di base e contesto; le cifre della loro tabella sono per
GPU/TPU, non misure di RAM CPU della CPX52. Per il modello MoE non basta
considerare i soli parametri attivi. Non si usa quindi quella tabella per
certificare che un tag Ollama entri nei 24 GB.
La [FAQ Ollama](https://docs.ollama.com/faq) documenta anche l'effetto di
contesto e parallelismo sulla memoria. Nessuna configurazione viene cambiata.

Il solo contatore `ollama ps` non sostituirebbe una misura del picco complessivo
di sistema. Eventuale misura futura: RAM disponibile, memoria del processo/
cgroup e servizi, picco durante prefill e decode, swap-in/out e latenza.
**Nessun consumo RAM esatto o token/s CPU è oggi verificato per i candidati.**

## Tre candidati realmente scaricabili

Fonti ufficiali consultate il 2026-11-11. I valori del catalogo sono dimensioni
approssimate degli artefatti, **mai stime di RAM totale**; i tag possono
selezionare runtime/quantizzazioni diversi. Escluse le varianti cloud e MLX
per questa VPS Linux x86-64 senza GPU.

| Candidato | Disponibilità e licenza | Variante locale osservata | Fattibilità e ruolo nella scelta |
|---|---|---|---|
| **Gemma 4 12B instruction-tuned** | [Google model card](https://huggingface.co/google/gemma-4-12B-it), Apache-2.0, revisione 43c9d014b231474fa7212dbb48a762566c2b255d | [Ollama gemma4:12b](https://ollama.com/library/gemma4:12b), ramo llamacpp Q4_K_M circa 8,0 GB; la pagina elenca anche projector e draft | **Unico preferito per la prova**: famiglia diversa e tag più contenuto, quindi margine di pianificazione migliore. Non prova superiorità tattica o latenza accettabile |
| Gemma 4 26B A4B instruction-tuned | [Google model card](https://huggingface.co/google/gemma-4-26B-A4B-it), Apache-2.0, revisione 4d7ae4984b7db7de8f8457170b3f1a419ee76d52 | [Ollama gemma4:26b](https://ollama.com/library/gemma4:26b), ramo llamacpp Q4_K_M circa 19 GB, con componenti aggiuntivi | MoE 4B attivi non significa RAM di un 4B. Margine più fragile su 24 GB condivisi col RAG; non selezionato, non proposto come secondo tentativo automatico |
| Qwen3.8-27B | [Qwen model card](https://huggingface.co/Qwen/Qwen3.8-27B), Apache-2.0, revisione 37561816e66b5b9153b1b64c10968c18c1e6f4a0 | [Ollama qwen3.8:27b](https://ollama.com/library/qwen3.8:27b), llamacpp Q4_K_M circa 18 GB più componenti | Aggiornamento reale di famiglia/dimensione, ma denso e più oneroso. Nessuna prova di vantaggio Coverciano né di sostenibilità CPU; non selezionato |

I modelli dichiarano capacità multilingue, ragionamento e comprensione di
documenti; tali capacità pubbliche non diventano voti tattici. Il confronto
proposto usa soltanto testo degli estratti, non immagini, audio o video.
Contesti pubblicizzati molto lunghi non sono il contesto da allocare sulla VPS:
si propone 8.192, come nei casi Coverciano conservati, non il massimo nominale.

Le model card e i metadati ufficiali dichiarano Apache-2.0. La
[licenza Apache](https://www.apache.org/licenses/LICENSE-2.0) consente in
principio uso autonomo anche commerciale, rispettando gli obblighi applicabili
di licenza/attribuzione/NOTICE e modifiche distribuite; non concede diritti
sui documenti del corpus o sui marchi. Il file LICENSE alla radice del repository
Gemma 12B non è stato trovato nel percorso provato: ciò non smentisce la
licenza esplicita della card e del catalogo. Nessuna attestazione legale
complessiva sui dati viene inventata.

La [guida Google per Ollama](https://ai.google.dev/gemma/docs/integrations/ollama)
documenta l'uso locale, ma non prova il supporto dell'artefatto esatto sulla
build installata 0.40.5. Prima di un uso futuro servono tag, manifest/layer/hash,
quantizzazione, template e compatibilità del runtime identificati. Non
riaprire l'ABI C++: usare l'interfaccia locale supportata del servizio.
Se è necessario un upgrade/installazione o una variante incompatibile, STOP
senza correzioni automatiche. Nessun modello è stato scaricato oggi.

## Riutilizzare il lavoro senza ricostruire la pipeline

| Componente | Dipendenza reale e riuso |
|---|---|
| Corpus e metadati | Riutilizzabili, salvo diritti e qualità dei contenuti; cambiare generatore non richiede riscriverli |
| Embedding | Il codice usa separatamente qwen3-embedding:0.6b via Ollama. Mantenendolo, non cambiano spazio vettoriale e indice; sostituirlo richiederebbe nuova indicizzazione, fuori proposta |
| Retrieval e reranker | Chroma, selezione delle fonti e mMARCO CPU sono separabili dal generatore. Per la prova usare gli estratti salvati, senza avviare questi componenti |
| Generazione | Endpoint loopback /api/chat, nome modello, template e opzioni Ollama sono i punti di adattamento. think/num_ctx/num_predict non sono universali fra famiglie |
| Contratti e validatori | Codice deterministico e rubriche conservabili; il supporto del decoder al loro schema non è trasferibile per presunzione. Nessun harness o nuovo contratto richiesto per giudicare una risposta naturale |
| API e panel | Riutilizzabili dopo un eventuale adapter e collaudo separato, non automaticamente compatibili o già integrati col nuovo modello |

`smoke_test_rag_v5_e2e.py` contiene già il percorso `chat()` in linguaggio
naturale, distinto dai percorsi opt-in TSC/extraction. La minima modifica
futura sarebbe un piccolo driver locale che invii domanda e fonti congelate
al solo modello alternativo e conservi la risposta integrale. Nessun nuovo
framework, corpus, gold, validatore o pipeline. Non implementato oggi.

**Il contratto extraction non è necessario per valutare la competenza del
coach.** I validatori rimangono disponibili come diagnostica; non vanno
usati per censurare o correggere il testo prima del giudizio umano. Non si
eliminano le salvaguardie di produzione: il confronto resta separato.

## Un solo confronto, eventuale e falsificabile

ID proposto: `RD-RAG-V5-LOCAL-COACH-DECISIVE-COMPARISON-01`, **DA FARE**,
non autorizzato. Preferito Gemma 4 12B locale; nessuna rotazione fra i tre
candidati in caso di esito negativo.

1. **Freeze offline prima di qualsiasi invio:** dieci file Qwen già individuati,
   relativi testi, sei estratti ciascuno nello stesso ordine, citazioni e hash;
   Qwen non viene rigenerato. Stesse domande e fonti per Gemma. Nessun retrieval,
   fonte aggiunta, suggerimento del revisore o nuova soluzione nel prompt.
2. **Istruzioni comparabili:** riusare la costruzione naturale versionata,
   senza nuove prescrizioni tattiche. Il codice storico permette una
   ricostruzione dichiarata, non la prova del payload esatto ricevuto allora.
   Non inventare prompt mancanti. Poiché alcuni Qwen conservati hanno repair/
   sanitizzazione, il confronto qualifica il candidato rispetto ai risultati
   disponibili, **non isola causalmente il solo peso del modello**.
3. **Mandato separato obbligatorio:** download/installazione del solo modello,
   eventuali operazioni effimere di caricamento/scaricamento, diagnostica di
   risorse e massimo dieci chiamate locali, giudizio umano e budget. Nessuna
   di queste azioni è autorizzata dal presente report.
4. **Prerequisiti risolvibili e arresti:** runtime esistente compatibile senza
   upgrade, manifest/licenza esatti, spazio libero sufficiente per download e
   temporanei, periodo già pagato sufficiente, fonti e revisore disponibili.
   Nessun fallback cloud, nuova GPU o servizio. In caso di mancanza, STOP.
5. **Risorse proposte da approvare, non misurate:** una richiesta alla volta,
   contesto 8.192, massimo 900 token generati, think=false soltanto se supportato
   dalla variante, risposta naturale entro il limite storico di 350 parole.
   Nessun modello Qwen generativo caricato contemporaneamente; conservare il
   RAG senza avviarlo per questa prova. Mantenere almeno 4 GB di MemAvailable
   come margine progettuale e monitorare il picco totale, senza swap-in/out
   persistente. Contare anche eventuali projector/draft caricati dal tag.
   Incompatibilità, OOM, paging sostenuto o impossibilità di rispettare il
   margine fermano la prova, senza cambiare quantizzazione/contesto al volo.
6. **Budget temporale:** massimo 900 secondi per chiamata e 9.000 secondi
   cumulativi di generazione (2,5 ore); zero retry/repair. È un limite proposto,
   non una previsione di token/s. Risposta vuota, troncata o timeout resta
   fallimento del tentativo; nessun secondo invio. Un arresto tecnico anticipato
   limita la conclusione alla sostenibilità sulla CPX52, non all'intelligenza
   intrinseca del modello.
7. **Valutazione cieca e autonoma:** venti testi originali, dieci per percorso,
   anonimizzati e presentati senza versione, gate o voti precedenti a un
   allenatore qualificato indipendente. Nessuna AI completa/corregge i testi.
   Usare le rubriche già adottate, senza nuove conversioni: voto Coverciano /30,
   criteri PASS del protocollo 9/10 e pesi RD-THINK conservati. Prima della prova
   il revisore deve avere la specifica di scoring completa e dichiarare
   indipendenza; se manca, non inventare voti.
8. **Successo fissato prima della prova:** candidato con almeno 9 risposte PASS
   su 10, media almeno 26/30 e zero errori tattici gravi; oltre a RAM/tempi nei
   limiti. Confrontare entrambi i percorsi con lo stesso revisore e non con la
   vecchia media Gemini di una versione diversa. Pubblicare raw, errori,
   consumi/picchi, tempi e tutti i voti, senza scartare i fallimenti.

Differenza tecnica rispetto ai test conclusi: cambia realmente la famiglia
del generatore, mantenendo le fonti; si valuta una risposta tattica completa
con un revisore indipendente, non JSON o copertura di parole chiave. Nessun
confronto locale di questo tipo è già dimostrato dalle evidenze riconciliate.

Se il candidato supera entrambe le soglie, zero errori gravi e limiti di
risorse, è razionale **EVOLVERE** nel perimetro locale con un investimento
successivo limitato; servirebbe comunque un vero holdout indipendente prima
di qualsiasi certificazione. Se fallisce o richiede risorse/rinnovi non
approvati, raccomandazione operativa **CHIUDERE** questo percorso sulla CPX52
e preservare gli asset, senza inseguire altri tag. Se anche Qwen supera la
revisione, non si dichiara dimostrata la necessità di cambiare modello:
la scelta successiva deve confrontare qualità e costo, senza migrazione
automatica. Le dieci tracce development non diventano holdout retroattivamente.

## Economia del solo percorso autonomo

Il prezzo mensile effettivo e la scadenza della CPX52 non sono forniti:
indicarli con **P** da fattura. Compenso del revisore **H**, ore interne **L**
e relativo costo opportunità non sono noti. Non sostituire questi dati con
un listino di un piano con nome simile o con prezzi di inferenza esterna.

| Scenario locale | Ricorrenti e costo di prova/uso | Lavoro, rischio e condizione razionale |
|---|---|---|
| A — Continuare Qwen 9B | P/mese più eventuali servizi/traffico; nessun costo per token di un fornitore AI. Latenze storiche di minuti, non SLA attuale | Non giustificato proseguire soltanto perché già installato: qualità autonoma non dimostrata |
| B — Candidato open-weight locale | Sempre P/mese se resta sulla stessa VPS; royalty del modello Apache-2.0 pari a zero, non costo operativo zero. Nel periodo già pagato il test non richiede un nuovo canone, salvo limiti/extra del contratto | Un giorno lavorativo massimo proposto per preparazione/identità/driver, fino a 2,5 ore di generazione, revisione H da preventivare. Non settimane di nuova architettura |
| C — Chiusura e preservazione | Nessun canone VPS dopo effettiva dismissione; eventuale storage/backup e attività di preservazione da quantificare | Preservare prima dati solo-VPS e fonti; un piano di dismissione separato non è eseguito né autorizzato qui |

**Tetto proposto per costi incrementali di hosting/hardware del confronto: 0**;
nessun rinnovo, aumento piano o acquisto. **Costi di inferenza remota: 0** per
vincolo, non perché si usi una quota gratuita. Il costo totale non è quindi
un numero verificato: è H più lavoro interno L ed eventuale traffico/storage
contrattuale da approvare prima; nessun costo attuale evitato viene inventato.
Se non si ottiene un preventivo sostenibile o il periodo pagato è insufficiente,
non iniziare. Il costo già sostenuto non giustifica altro investimento.

Per un uso continuativo il costo unitario dipende da P e dal numero di richieste
completate con qualità accettabile; non basta dividere P per un volume promesso.
Senza latenza, picco RAM e domanda d'uso misurati non è stimabile la capacità
mensile. Con il requisito locale, sostituire il modello **non elimina da solo
la necessità di un'infrastruttura di calcolo propria**.

## Risposte finali e stato

Non è stimabile con evidenze una probabilità di raggiungere 9/10 e 26/30.
Esiste un'alternativa tecnicamente plausibile per autonomia/licenza e taglia,
non una prova di qualità tattica superiore. Corpus, codice, retrieval,
rubriche e controlli sono asset riutilizzabili; gli errori architetturali
osservati possono persistere anche cambiando generatore.

Attività → analisi Git/file e documentazione ufficiale dei soli modelli locali
→ commit documentale → presente report/evidenza → fattibilità condizionale,
nessuna superiorità misurata → **VERIFICA DECISIVA** proposta → analisi
**ESEGUITO**, confronto **DA FARE** e non autorizzato. Gli stati del progetto
non sono sostituiti dalle etichette della decisione strategica.

Report, TODO, Experiment Register ed evidenza pubblicati nella stessa sessione;
commit identificabile nella storia del report e verificato su GitHub. Nessuna
implementazione, download di pesi, SSH, inferenza, test, modifica di runtime,
prompt/schema/Gold/validatori, VPS, merge o deploy. Certificazione locked
storica preservata nel proprio perimetro; qualità generale, Gate e
certificazione del coach **BLOCCATO**. STOP dopo la pubblicazione.
