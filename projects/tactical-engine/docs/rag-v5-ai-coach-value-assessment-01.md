# Valore reale dell'allenatore AI — decisione prima del rinnovo VPS

Data: 2026-11-11. Attività: `RD-RAG-V5-AI-COACH-VALUE-ASSESSMENT-01`.

## Verdetto e raccomandazione unica

**Qwen mostra conoscenze tattiche parziali, ma le evidenze non dimostrano un
allenatore autonomo affidabile al livello richiesto.** Non è corretto dire
che sa soltanto produrre JSON: esistono risposte naturali e risultati
documentali positivi. Non è altrettanto corretto trasformarli in prova di
competenza generale, né sostenere che Qwen sia incapace in assoluto.

**Raccomandazione C: sospendere lo sviluppo operativo e preservare il progetto,
senza assumere un altro rinnovo VPS come costo giustificato dal valore tattico
già dimostrato.** Il materiale basta per questa decisione prudenziale di
spesa; non basta per decretare il limite intrinseco di Qwen, scegliere un
modello sostitutivo o promettere un prodotto migliore di ChatGPT.
Non sono disattivati servizi, rinnovi o risorse. Prima di un'eventuale
dismissione effettiva, dati e artefatti presenti soltanto sulla VPS devono
essere preservati con un intervento separato autorizzato: il repository
locale non è dichiarato backup completo della VPS.

## Riconciliazione e metodo

Baseline iniziale locale e GitHub
`4f8c9f6630e7032547324882c1cde87afddf5e68`, branch
`codex/tactical-state-contract-v1`, remote corretto, working tree pulito.
TODO e Experiment Register ufficiali consultati anche mediante raw GitHub
al commit congelato e confrontati coi blob. Nessuna verifica equivalente
del valore economico/tattico conclusa alla baseline: riutilizzate, senza
rieseguirle, le precedenti valutazioni tecniche, di autonomia e Coverciano.

Nuova attività documentale: riconciliare risposte naturali, voti indipendenti
riportati, risultati strutturati e controlli automatici per decidere sul
valore del prodotto. Nessun test applicativo, nuova risposta, inferenza,
SSH, benchmark, valutatore esterno o modifica applicativa.

Inventario verificabile:
[`ai-coach-value-evidence-inventory-01.json`](ai-coach-value-evidence-inventory-01.json).
Contiene 55 file di caso delle iterazioni Coverciano, percorsi/hash e domanda,
modello dichiarato, presenza/hash della risposta, indicazione di repair e
gate; dieci percorsi del set logico finale; 22 fonti documentali/artefatti
con dimensione e SHA-256. I 55 file **non sono 55 domande indipendenti né
il conteggio delle inferenze**. Non sono inventati contenuti assenti o voti.

## Materiale effettivamente disponibile

| Categoria | Evidenza recuperata | Uso corretto e limite |
|---|---|---|
| Risposte tattiche complete naturali | 55 file in evaluation/coverciano-remediation-v6, v7, v8, v9, v10, v10-1, v10-2; question/answer/evidence e modello qwen3.5:9b | Dieci tracce ripetute nello sviluppo, talvolta con repair o post-processing: valutabili come testi conservati, non holdout indipendente o prima risposta invariata |
| Risposte naturali su fonti nuove | Sei risposte in evaluation/runtime-archive/rag_v5_external_drive11_holdout_v1.json; report v5-external-drive11-holdout-01.md | Adjudication interna 6/6 sulle sei domande/fonti; prova circoscritta di estrazione e sintesi documentale, non voto Coverciano |
| Risposta naturale a contesto congelato | evaluation/rd-think-01-result.json, thinking_off.first.answer | Risposta completa con errori relazionali; confronto controllato già concluso, da non ripetere |
| Risposte strutturate JSON | Runtime Spatial/extraction precedenti e raw della singola API q3_04, già diagnosticato | Classificazione/grounding di una coppia, non piano d'allenamento o consiglio completo all'allenatore |
| Incomplete o bloccate | RD-THINK-01 thinking on senza risposta finale; q3_04 genera JSON ma non un witness validato | Non eliminare i fallimenti né trattare l'arresto corretto come competenza positiva; JSON completo e risposta coaching completa sono proprietà diverse |
| Deterministico senza nuova generazione | Suite offline e gate di contratto/locator, inclusi remediation A/R1 | Dimostrano esclusivamente le proprietà controllate; non assegnano competenza tattica |
| Valutazioni esterne storiche | Benchmark RAG-only dieci casi, voti Gemini Cloud nel report; trascrizioni RD-001/RD-002 | Valutazioni di altra AI, non commissione FIGC o giudizio umano certificato; non riassegnate alle risposte di versioni successive |
| Revisioni tecniche indipendenti | Review dei contratti/schema/ABI/grounding già pubblicate | Indipendenza tecnica del revisore non equivale a valutazione indipendente della capacità di allenare |

Il report RAG-only conserva i voti della baseline, ma le sue dieci risposte
integrali originali con giudizi completi non sono state individuate negli
artefatti versionati consultati. Si usa quindi il risultato come **riportato
nel report storico**, senza fingere una nuova adjudication dei raw mancanti.
Le risposte delle remediation sono invece direttamente leggibili nei JSON.
Esistono anche artefatti storici citati soltanto su VPS: non sono stati
recuperati e non si presume il loro contenuto.

## Rubriche esistenti: nessuna modifica o nuovo voto

Protocollo Coverciano adottato:
`coverciano-rag-only-100-protocol-01.md`: risposta RAG immutata, voto esterno
in trentesimi, media almeno 26/30, esclusione dei contributi sostitutivi
della spalla. Le rubriche nascoste/giudizi integrali di ogni domanda della
baseline non sono ricostruiti a memoria.

La rubrica tattica esplicitamente congelata in RD-THINK-01 è presente nel
JSON originale e nel report: **correttezza tattica 35%, copertura 25%, coerenza
squadra/ruolo/lato/fase 20%, supporto documentale 15%, vincoli 5%**.
Si mantengono pesi e significati; qui si usano soltanto come assi di lettura,
senza inventare sottovoti, conversioni o nuovi punteggi ufficiali. Non è una
rubrica ufficiale FIGC/Coverciano.

Il protocollo distinto `rag-v5-quality-9of10-validation-protocol-v1.md`
richiede almeno nove domande PASS su dieci in un holdout indipendente;
la sua rubrica 0–2 per pertinenza, fedeltà, completezza, coerenza e tracciabilità
non va convertita in un voto medio /30. La rubrica holdout di adjudication
impone inoltre di lasciare non verificata la fedeltà quando non sono state
lette tutte le coppie affermazione-fonte: qui non si dichiara quell'audit
completo sulle 55 risposte.

## Valutazioni indipendenti già disponibili

Da `coverciano-rag-only-100-report-01.md` (2026-10-26), voto alla sola bozza
RAG, senza spalla: **26, 18, 25, 23, 20, 22, 24, 21, 0, 20 su 30**.
Totale riportato 199/300, media **19,90/30**, un caso su dieci almeno 26/30.
Il divario storico dal target medio è **6,10 punti su 30**. Non è una misura
della distanza residua dell'ultima versione, che non ha un nuovo voto esterno
comparabile. Un'astensione per retrieval insufficiente valeva 0/30 nel compito
di risposta all'esame, pur potendo essere prudente sul piano documentale.

Esempi di giudizi già attribuiti, senza nuovi voti:

- transizione negativa: 26/30, fondamentali corretti, lacune su preventive e
  condizioni situazionali;
- difesa del cross: 25/30, buoni postura e duello, coordinamento incompleto;
- costruzione contro uomo: 18/30, confusione di fase e trattamento inadeguato
  di portiere/terzo uomo;
- fuorigioco: 0/30, domanda non affrontata per retrieval insufficiente.

I 29–30/30 dell'audit autonomia non vanno attribuiti a Qwen: riguardavano
risposte riscritte dalla spalla. La prova 16 includeva addirittura un voto
su un segnaposto al posto della risposta. `revisione_domande.md` documenta
anche un 30/30 dopo che Gemini aveva scritto il completamento mancante:
nessun miglioramento autonomo dimostrato da quel voto. I giudizi esterni
sono dunque evidenze da controllare nell'attribuzione, non autorità infallibili.

## Lettura tattica delle risposte conservate

Osservazioni qualitative, **non una nuova commissione né nuovi voti**.
I percorsi seguenti si riferiscono a file originali dell'inventario.

| Capacità esaminata | Evidenza positiva osservabile | Limite o errore concreto | Valutazione consentita |
|---|---|---|---|
| Comprensione della situazione | Il caso 1 V10 distingue riaggressione/ripiegamento e richiama prossimità, densità e palla coperta/scoperta | Associa anche scelte a condizioni genericamente formulate senza dimostrare sempre il nesso | Sa esporre criteri; non prova capacità costante di decidere nello scenario |
| Sistemi e ruoli | Caso 10 V10.2 descrive inizialmente ala fuori, centrale dentro, terzini quinti, ala residua seconda punta | Nello stesso testo un centrocampista poi scende; in RD-THINK off l'ala esce per diventare terzino e il centrale entra come ala/centrocampista | Conoscenza della nomenclatura e di uno schema possibile; pianificazione relazionale non affidabile |
| Movimenti e occupazione spazi | Caso 4 V10 nomina cinque corridoi, triangoli e preventive; caso 7 ricezioni tra le linee | Geometrie spesso non assegnate a giocatori; frasi come profondità all'indietro e concatenazioni non motivate richiedono revisione | Lessico e principi presenti, applicazione non stabilmente dimostrata |
| Costruzione/pressione/transizione | Caso 1 e Drive11 danno principi riconoscibili; il testo sul recupero palla espone l'attacco rapido | Caso 2 V10 propone palla forte e radente verso la testa e combina sequenze poco coerenti; baseline già penalizzata per inversioni di fase | Non è sufficiente aggiungere terzo uomo/portiere come parole per superare il problema |
| Difesa e cross | Caso 3 V10 espone postura semiaperta e coordinamento col portiere | Formulazioni assolute e riferimenti allo specchio/duello non costituiscono un piano affidabile per ogni situazione | Elementi utili, senza certificare ogni prescrizione |
| Contraddizioni tattiche | Il sistema deterministico riconosce e blocca alcuni errori; non è capacità dimostrata di Qwen | q3_04 propone supported pur assegnando all'evidence frammenti del claim; label osservata resta nulla | La capacità del modello di distinguere opposizioni spaziali resta non dimostrata |
| Concretezza e motivazione | V10 aggiunge chi/cosa/dove/innesco/rischio e riferimenti alle fonti | RD-THINK off copre formalmente tali voci ma costruisce una trasformazione impraticabile; caso 8 V10 usa una coreografia numerica non ancorata alla traccia | Struttura espositiva migliorata, ragionamento causale insufficiente a garantire una soluzione |

I casi più recenti della remediation non vengono confusi con la prima
risposta autonoma: alcune uscite hanno repair selezionato o sanitizzazione.
Il set logico V10/V10.1/V10.2 è dichiarato 10/10 tecnicamente nel suo report,
ma il file V10.2 caso 10 conserva il gate di quell'esecuzione non completo;
il report descrive un successivo re-audit deterministico. Nessuno dei due
è un nuovo voto tattico esterno. Non si riscrive quel risultato né si riesegue
il gate per attribuirgli un significato diverso.

Le osservazioni di errori nel testo sono controllabili anche senza accettare
come gold tutte le prescrizioni del valutatore Gemini. Non viene dichiarata
errata ogni risposta o privo di valore il corpus.

## Tabella sintetica del verdetto

| Indicatore | Evidenza disponibile | Esito |
|---|---|---|
| Comprensione tattica | Principi riconosciuti e caso baseline 26/30; errori di scenario in altri casi | Parziale, non affidabilità generale dimostrata |
| Correttezza dei principi | Posture, densità, transizioni e fonti Drive11; inversioni e trasferimenti impropri | Alcune capacità dimostrate, coerenza insufficiente |
| Capacità di ragionamento | Risposte articolate, ma trasformazioni contraddittorie a contesto congelato | Ragionamento applicativo robusto non dimostrato |
| Qualità delle soluzioni | Miglior copertura formale V9/V10, senza nuova valutazione esterna | Valore pratico non dimostrato al target |
| Affidabilità delle risposte | Baseline 19,90/30; astensione; gate falsamente positivi; q3_04 non valutabile | Insufficiente per affidare autonomamente consigli tattici |
| Confronto con ChatGPT | Nessuna coppia omogenea con giudizio confrontabile individuata nelle fonti consultate | Superiorità o inferiorità non dimostrate |
| Obiettivo 9/10 e media 26/30 | Locked prima 9/10, poi regressione 10/10 nel proprio closeout; Coverciano storico 19,90/30; nessun nuovo holdout tattico generale certificato | Locked preservato; target generale e media Coverciano non dimostrati |

## Modello, architettura e confronto con ChatGPT

**Entrambi contribuiscono al problema osservato, senza una separazione causale
quantificata.** Errori di ruoli e relazioni sono già nelle risposte di Qwen;
RD-THINK a contesto congelato mostra che il solo completamento del gate non
garantisce coerenza. Non prova però che un altro modello con gli stessi input
farebbe meglio, né che il problema sia esclusivamente intrinseco a Qwen.

Le precedenti analisi documentano anche retrieval di fase/prospettiva
sbagliata, grounded-only che limita l'applicazione, follow-up senza cronologia
e gate che controllano citazioni/copertura più facilmente della tattica.
Le remediation successive hanno affrontato parti di questi problemi:
non si propone di aggiungere un parser o un gate come se fossero assenti.
I contratti più recenti non hanno ancora una dimostrazione end-to-end di
qualità del coach. Il singolo test extraction non può misurare l'intera
architettura né sostituire una risposta tattica completa.

Nelle fonti consultate ChatGPT compare soprattutto come revisore tecnico
dei contratti. Questi scambi non sono risposte alle medesime tracce allenatore.
Mancano coppie di risposte ChatGPT/Qwen con stessa domanda, stessi estratti e
vincoli, modello/versione, budget e rubriche identici, oltre a giudizi ciechi
attribuibili. I voti Gemini o le riscritture Groq non sono quel confronto.
Non si genera qui una risposta tattica ChatGPT da usare retroattivamente
come concorrente. **Un prodotto migliore di ChatGPT non è oggi dimostrato;
non è nemmeno dimostrato impossibile.**

## Materiale sufficiente e minima verifica eventuale

Il materiale basta per **non finanziare altro sviluppo operativo alla cieca**:
ci sono fallimenti sostanziali osservati e manca la prova del valore promesso.
Non basta per una previsione definitiva su modello/mercato, sull'ultima
architettura o sulla superiorità rispetto a un'alternativa.

Se il titolare volesse ridurre questa incertezza prima di tornare a spendere,
la minima verifica nuova proposta è **una valutazione tattica umana indipendente
in cieco del set logico di dieci risposte già conservate** elencato
nell'inventario, con domanda ed evidenze originali, senza riscrivere i testi.
Nessuna nuova generazione e nessuna VPS necessarie. Non viene eseguita qui.

Differenza tecnica rispetto alle prove concluse: giudizio sostanziale di un
allenatore qualificato indipendente sulle ultime risposte naturali, non
re-audit automatico, vecchi voti sulla baseline o giudizio dopo completamento
della spalla. Conservare la rubrica esistente, inclusi i pesi RD-THINK, e
il protocollo Coverciano per i voti; nessuna conversione automatica fra scale.
Il revisore deve disporre della specifica applicabile completa prima di
assegnare punteggi; se manca una regola di scoring, non inventarla. Nascondere
versione, voti precedenti e risultato del gate; registrare hash, giudizio,
errori gravi, motivazioni e indipendenza dell'autore. Nessun voto qui assegnato.

La revisione darebbe una prima base di prosecuzione sui testi disponibili,
non un nuovo holdout: le dieci domande sono già development e non certificano
il 9/10 generale. Se il materiale restasse sotto il target o mostrasse errori
gravi, non autorizzerebbe altre settimane di remediation senza un'ipotesi
falsificabile. Un eventuale confronto con altro modello richiederebbe poi
mandato e dati omogenei separati; **non è la verifica proposta ora**.

## Decisione economica e tecnica

| Opzione | Valore conservabile | Cosa manca/rischio | Decisione |
|---|---|---|---|
| A — Proseguire Qwen/architettura attuale | Corpus, pipeline e controlli già sviluppati | Continuare costi senza prova indipendente recente del valore tattico; nuovo JSON valido non risolve il dubbio | Non raccomandata |
| B — Conservare asset e cambiare modello | RAG, conoscenze, rubriche e valutatori possono essere riutilizzati | Nessuna superiorità di un'alternativa dimostrata in confronto omogeneo; cambio può spostare i problemi e introdurre nuovi costi | Non selezionata senza evidenze |
| C — Sospendere operatività e preservare | Conserva lavoro e possibilità di ripresa, rende non obbligatoria ulteriore spesa VPS | Non certifica un prodotto e richiede custodia dei dati prima di eventuale dismissione | **Unica raccomandazione** |

Non sono disponibili prezzo del prossimo rinnovo, scadenza contrattuale,
valore commerciale misurato o inventario completo dei dati privati VPS.
Nessun risparmio monetario preciso, ROI o costo già evitato viene inventato.
La raccomandazione è di priorità tecnica e controllo della spesa futura,
non una dichiarazione che il lavoro già fatto sia perso.

## Tracciamento e stato

Attività → letture Git/Markdown/JSON e inventario inline di evidenze già
esistenti → commit documentale → questo report e inventario → capacità
parziali e insufficienza della prova di affidabilità → raccomandazione C →
analisi **ESEGUITO**. La qualità generale dell'allenatore non è **VALIDATO**,
**INTEGRATO** o **CERTIFICATO** da questa analisi. La certificazione storica
locked rimane nel suo perimetro e non viene revocata o ampliata.

Report, TODO, Experiment Register e inventario pubblicati nella stessa
sessione; commit identificabile nella storia di questo file. Pubblicazione
GitHub e working tree finale verificati. Nessun modello, prompt, schema,
validatore, dataset, risultato storico, pipeline, panel o VPS modificato;
nessuna SSH, inferenza, benchmark duplicato, compilazione, merge o deploy.
Gate generale, accuratezza generativa e certificazione del coach restano
**BLOCCATO**. Nessuna nuova verifica avviata automaticamente. STOP.
