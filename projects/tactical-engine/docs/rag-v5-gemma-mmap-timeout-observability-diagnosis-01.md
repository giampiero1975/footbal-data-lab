# Gemma mmap — diagnosi offline di timeout e osservabilità

Data: 2026-11-19. Attività esistente
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
Baseline: `aa15ed26d9c29ddb05eb950010e36cc065b9837e`.

## Giudizio e diagnosi

**Il controller attuale non è sufficientemente affidabile per autorizzare
tecnicamente un nuovo test con gli stessi requisiti di osservabilità.** Sono
dimostrabili difetti nella separazione tra logging, controllo delle risorse,
deadline e finalizzazione. Non è invece determinabile quale evento abbia
originato il gap specifico: mancano proprio le misure che lo distinguerebbero.

La causa immediata dell'errore registrato è certa: nel solo ramo che genera
`E_DEADLINE_AMBIGUOUS`, il controller trova `deadline - time.monotonic() <= 0`.
**Non è un reason code ricevuto da Gemma o Ollama.** Non è provato un timeout
HTTP, un crash del modello, una sospensione del PC o un guasto di rete.

I2.211,531s sono una differenza fra due timestamp wall-clock locali; STOP viene
costruito dopo il cleanup di `one_remote`, non al momento della rilevazione
della scadenza. Non misurano direttamente il timer monotonic900s. Mancano
timestamp monotonic locali di inizio, scadenza, ricezione, kill e cleanup.
Non è quindi dimostrato né che il timer sia stato controllato puntualmente,
né che tutti i2.211s precedano la rilevazione della scadenza.

La correzione necessaria riguarda il canale di controllo/custodia. **Non basta
alzare900s, indebolire la riserva4GB o ripetere Gemma.** Nessuna correzione è
applicata da questa diagnosi; nessuna nuova inferenza o SSH viene eseguita.

## Tracciamento e riconciliazione

Attività → lettura statica/analizzatore
`operations/quality-first-pilot/diagnose_gemma_mmap_timeout_01.py` → commit
diagnostico **d67df947224fbcf9f49cda99ab69f69b81043ce2** → questo report → fatti/timeline sotto → bloccare nuovi
runtime fino a correzione autorizzata e validazione locale → diagnosi
**ESEGUITO**, **VALIDATO** nel perimetro documentale; correzione **DA FARE**,
idoneità del controller e nuovo completamento generativo **BLOCCATO**.

GitHub/local HEAD e branch riconciliati alla baseline indicata, tree iniziale
pulito. Consultati TODO, Experiment Register, report gemma-mmap-on-01, quattro
script originali, ledger/raw/ZIP e diagnostica finale già versionati. Nessuna
diagnosi equivalente completata: il closeout precedente documentava l'ambiguità,
senza analisi del percorso di controllo e dei blocchi I/O. Nessuna suite storica
o test applicativo ripetuto; nessun import/esecuzione dei controller originali.

L'analizzatore legge JSON/ZIP, verifica hash e identità dei chunk, calcola
intervalli e raccoglie linee/funzioni con AST. La sintassi del nuovo parser è
stata corretta prima di produrre i fatti. Non è una correzione del controller.
Evidenze nuove in
[facts.json](gemma-mmap-timeout-diagnosis-01/facts.json),
[input-inventory.json](gemma-mmap-timeout-diagnosis-01/input-inventory.json) e
[piano proposto](gemma-mmap-timeout-diagnosis-01/proposed-validation-plan.json).
Il commit documentale che introduce questo report aggiorna contestualmente
TODO/registro ed è restituito nella consegna. Gli originali restano immutati.

## 1. Timeline ricostruita

I timestamp UTC dei ledger sono valori scritti nei record, non misure del
completamento di fsync. Il timestamp reserved-before-GO precede l'invio del
GO; il nome “GO→STOP” è una convenzione, non una misura esatta della POST.

| Dominio | Evento | Timestamp registrato / intervallo |
|---|---|---|
| Locale wall-clock | activity-created |2026-11-19 10:50:44.602593 UTC |
| Locale wall-clock | prenotazione prima di GO |10:50:45.587758 UTC |
| Remoto monotonic | observer_started |2156920.909713426 |
| Remoto monotonic | ready |2156920.998914255 |
| Remoto monotonic | post_started |2156921.040748629, origine relativa0 |
| Remoto monotonic | HTTP200 |2157026.698759227, +105,658011s |
| Header HTTP, altro wall-clock | Date fornita dal server |10:52:32 GMT, precisione al secondo |
| Remoto monotonic | primo wire |+105,659361s |
| Remoto monotonic | ultima osservazione observer |+395,495781s |
| Remoto monotonic | ultimo campione risorse |+397,188077s |
| Remoto monotonic | ultimo wire, indice706 |+397,338112s |
| Locale wall-clock | record STOP |11:27:37.118428 UTC; prenotazione→STOP2211,530670s |
| Locale wall-clock | diagnostica successiva inizio/fine |11:29:57.279740 /11:29:58.543614 UTC |
| Remoto wall-clock/monotonic | diagnostica successiva |11:29:59.746408 UTC /2159273.913784134; ps vuoto e servizi active |

393 sample: mediana intervallo1,005737s, massimo1,072606s. Observer:198
osservazioni più start, massimo intervallo2,016098s. Le707 righe wire coprono
291,678751s fra primo/ultimo chunk, senza done. Il prefisso ricevuto mostra
osservazioni regolari; **non mostra ciò che è accaduto dopo il taglio**.

I due canali SSH distinti terminano nel raw entro circa1,84s l'uno dall'altro
sullo stesso orologio remoto. È compatibile con un fattore comune, ma non lo
identifica né dimostra che la causa sia PC, disco, rete o server. Il contenuto
raw è un prefisso integro, non una registrazione continua dell'intera prova.

ZIP dei wire: prima data11:52:32, ultima11:57:22 del19novembre, precisione2s e
nessuna timezone nel formato. Coerenti, assumendo Europe/Rome, col prefisso
registrato; non sono timestamp monotonic di ricezione e non certificano fsync.

Nella diagnostica successiva il timestamp UTC remoto supera la fine locale
di1,203s: i record non consentono di presupporre un unico wall-clock sincronizzato.
Non usare questo offset come spiegazione del gap di mezz'ora. Il monotonic
remoto prosegue fra ultimo raw e diagnostica per1955,535s senza nostre
osservazioni intermedie. Non convertire quel vuoto in una storia causale.

## 2. Analisi del controller locale

Riferimenti al
[controller congelato](https://github.com/giampiero1975/footbal-data-lab/blob/aa15ed26d9c29ddb05eb950010e36cc065b9837e/projects/tactical-engine/operations/quality-first-pilot/paired_pilot_01.py#L213).

- **Deadline, righe239–251:** è un controllo cooperativo nel loop. La coda viene
  attesa al massimo1s solo se il loop sta girando. Nessun watchdog indipendente
  applica quel budget durante le altre operazioni. Il timer è impostato prima
  di write/flush dello stdin, che possono bloccare senza un proprio limite.
- **Collettore,227–235:** readline stdout → write → flush → fsync → enqueue.
  Il controllo riceve l'evento soltanto dopo la persistenza. Una stasi I/O può
  ritardare la telemetria e riempire la pipe. Eccezioni del thread producono il
  sentinel None nel finally, ma non un errore strutturato e durevole nel ledger;
  traceback sulla console non equivale ad artefatto del test.
- **Wire,267–268:** ogni chunk viene scritto e fsync anche nel thread di
  controllo, senza limite alla durata I/O. Corretto l'intento di custodia,
  insufficiente la separazione dal controllo temporale.
- **Ordine del loop,247–253:** la deadline precede la lettura della coda.
  Dopo una pausa può vincere anche con EOF/errore/terminale già accodati.
  Il codice classifica la scadenza locale, non prova il momento dell'esito
  remoto. Non si deve invertire l'ordine e promuovere ciecamente un done tardivo.
- **Cleanup,286–295:** kill se vivo, wait senza timeout, join2s, flush/fsync
  stderr. Wait e I/O possono ritardare il ritorno all'outer catch; se il lettore
  rimane vivo, stdout non viene chiuso lì. PID, returncode, kill eseguito e
  durate delle fasi non vengono persistiti nel ramo d'errore.

Nel wrapper gemma_mmap_on_01.py, righe71–76, **STOP viene scritto dopo questo
finally ma prima di observation.finish**. Quindi il cleanup del solo observer
non spiega i2.211s del record STOP. Non si può invece escludere dal codice un
ritardo precedente nel loop o nel cleanup del generatore.

La distinzione fra monotonic e wall-clock è documentata da
[Python3.9 time](https://docs.python.org/3.9/library/time.html#time.monotonic):
non è corretto equipararli o sottrarre valori assoluti di host diversi. Un
cambio UTC da solo non modifica direttamente il test remaining su monotonic;
può però alterare la differenza wall-clock riportata dal ledger.

## 3. Worker remoto, HTTP, segnali e process group

[Worker congelato](https://github.com/giampiero1975/footbal-data-lab/blob/aa15ed26d9c29ddb05eb950010e36cc065b9837e/projects/tactical-engine/operations/quality-first-pilot/paired_pilot_remote_01.py#L130).

Il worker verifica parent argv GNU timeout900/kill-after15 e process group.
Questa protezione è presente, non è stata rimossa: limita il processo Python
remoto e il gruppo previsto. **Il runner Ollama è figlio del daemon**, come
mostra l'observer; non è automaticamente membro del gruppo del worker.
Terminare Python o SSH non dimostra la terminazione immediata del modello.

Sul lato Windows Popen non crea esplicitamente un nuovo process group/job.
`process.kill()` agisce sul child SSH; la
[documentazione subprocess](https://docs.python.org/3.9/library/subprocess.html#subprocess.Popen.kill)
distingue questa operazione dal controllo di un albero remoto. Il returncode
del canale generatore non è salvato: non possiamo ricostruire exit del timeout,
segnale, errore SSH o normale EOF a partire dal solo STOP.

HTTPConnection(timeout900), riga186, è un timeout delle operazioni bloccanti,
non un budget assoluto unico della conversazione:
[contratto HTTPConnection](https://docs.python.org/3.9/library/http.client.html#http.client.HTTPConnection).
Il reader readline253 può attendere una riga; stream periodico e budget totale
sono aspetti diversi. Il limite assoluto dovrebbe derivare da monitor e
supervisore, non dall'argomento HTTP da solo.

**Difetto di sicurezza concreto, indipendente dalla causa storica:** emit
righe25–27 usa output_lock e print/flush bloccanti. Il monitor,199–202, emette
sample **prima** di applicare la condizione di guardia. Sul ramo abort,212–215,
emette abort **prima** di shutdown del socket. Anche il reader emette wire
sullo stesso lock. Una pipe piena o un writer bloccato può quindi fermare sia
l'osservazione sia l'azione della guardia. GNU timeout resta separato, ma non
sostituisce la guardia4GB durante tutto il periodo.

Il codice non installa un handler che garantisca un terminale durevole su TERM;
una terminazione può impedire finally/finished. Errori e finali passano tutti
per lo stesso stdout, senza giornale remoto indipendente. La quiete successiva
osservata non ricostruisce gli eventi mancanti e non prova l'istante dell'arresto.

## 4. Observer e custodia

[Observer congelato](https://github.com/giampiero1975/footbal-data-lab/blob/aa15ed26d9c29ddb05eb950010e36cc065b9837e/projects/tactical-engine/operations/quality-first-pilot/gemma_mmap_observation_01.py#L11).

L'osservatore è una seconda SSH, non un canale di custodia indipendente dal PC:
stdout va su file locale; niente spool remoto. Usa time.time per la propria
durata e monotonic per i singoli eventi, senza un'origine/budget condiviso.
La raccolta journal è solo dopo il loop: nessun observer_finished ricevuto
implica che non si possa attestare nemmeno l'arrivo a quella fase.

Il wrapper finish72–76 può fare wait8s oppure kill/wait, ma salva soltanto
exit1. Manca forced_kill e l'azione precedente: **exit1 non identifica la causa**.
Non è prova di crash del programma remoto, né di una sua normale conclusione.

Maps/smaps sono tentati una sola volta, al primo PID, impostando subito seen.
Un processo appena nato può non aver ancora mappato i pesi; questa scelta
perde osservabilità anche se i permessi fossero sufficienti. Qui sono negati,
senza privilegi: il mode non va inventato. Campioni file-backed successivi
restano evidenze utili, ma non sostituiscono la prova dei singoli mapping.

Custodia positiva: ledger esclusivo/fsync-before-GO, raw prefisso,707 chunk,
ZIP e inventari risultano coerenti e hash verificati. Questo prova i byte
conservati, **non la completezza della raccolta**. Nessun timestamp locale
di ricezione o commit fsync per evento; nessuna sequenza durevole completa
remota, terminale garantito, errore del lettore o origine del cleanup.

## 5. Cosa è dimostrato e cosa resta aperto

| Classe | Conclusione |
|---|---|
| Dimostrato sul tentativo |1 POST, HTTP200,707 chunk thinking, nessun done/finale; ultimo sample397,188s e ultimo wire397,338s; codice locale emette E_DEADLINE_AMBIGUOUS |
| Dimostrato sul codice |Deadline cooperativa con I/O/cleanup non limitati; guardia subordinata a stdout; assenza custodia remota/exit strutturati; observer con clock e terminale deboli |
| Ipotesi compatibili, non diagnosi |Pausa/scheduling locale, stasi disco/fsync, perdita trasporto, variazione wall-clock, problemi di emissione remota; possibili combinazioni non distinguibili |
| Non determinabile |Chi ha fermato per primo la catena; istante deadline locale; eventuale completamento/modello nel gap; momento del timeout remoto/cancellazione; token prodotti non ricevuti |

Il taglio comune dei due canali suggerisce di rendere indipendente la custodia,
non di assegnare colpa a una macchina. Nessuna prova autorizza a classificare
il gap come inferenza durata2.211s o a bocciare Gemma per mancato rispetto900s.
Il risultato operativo precedente rimane non conclusivo, senza riscrivere
o invalidare retroattivamente gli artefatti.

## 6. Correzione minima proposta, non applicata

Un solo intervento coerente di robustezza controllo/custodia, in queste parti:

1. **Controllo e logging disaccoppiati.** Applicare guardia e cancellazione
   prima della telemetria; stdout non deve poter bloccare il controllo.
   Writer separato/coda limitata e politica di errore fail-closed; conservare
   fsync-before-GO, raw e checkpoint di custodia, senza eliminare la durabilità.
2. **Custodia sul lato che continua a lavorare.** Giornale remoto append-only
   delimitato per questo attempt ID, raw e terminale/manifest indipendenti dal
   trasporto; niente daemon o nuovo servizio. Il supervisor registra exit/segnali
   e stato della cancellazione. Permette recupero read-only senza seconda POST.
   Richiede futura autorizzazione esplicita alla scrittura degli artefatti remoti:
   nessuna directory o file VPS viene creato ora.
3. **Deadline e finalizzazione verificabili.** Watchdog indipendente dal reader/
   fsync, cleanup con limiti e azioni registrate; budget900 e grace15 invariati.
   Origini dei timer documentate, budget residuo non riavviato dopo preflight.
   Salvare wall+monotonic locali/remoti, clock_info, ricezione/durabilità,
   sequenza, PID/PGID, returncode/forced_kill e fasi prima/dopo cleanup.
4. **Classificazione e observer.** Distinguere deadline locale, timeout remoto,
   EOF/trasporto, errore custodia e risposta modello. Conservare un terminale
   arrivato in ritardo per forensics senza promuoverlo automaticamente a PASS.
   Observer sullo stesso budget monotonic, errori/kill propri registrati;
   evidenze mode quando disponibili durante la vita del PID, non solo all'avvio.

Non basta un controllo stale o il cambio dell'ordine della coda. Non promettere
una deadline locale hard se il sistema operativo non esegue il processo: il
lato remoto e la custodia devono funzionare anche quando il PC non raccoglie.
Socket chiuso/SSH morto non equivale a modello fermo: attestare quiete, oppure
registrare cancellazione non verificata e mantenere BLOCCATO ogni altro invio.
Nessun kill indiscriminato del daemon, riavvio o variazione soglie è proposto.

## 7. Piano locale non generativo — non eseguito

Nel JSON proposto ci sono nove fixture, da applicare soltanto dopo autorizzazione
alla correzione. Fake processi, clock, stream e sink locali: niente SSH/Ollama,
modelli o codice applicativo. Non sono una nuova suite semantica o benchmark.

| Fixture | Evidenza necessaria per accettare la correzione |
|---|---|
| NDJSON frammentato e terminale regolare |Byte identici, nessun chunk perso, sequenze e manifest completi |
| Output continuo oltre deadline |Budget assoluto rispettato nonostante traffico; nessun retry |
| Stdout bloccato mentre RAM supera la soglia |Guardia/cancellazione prima dello sblocco del writer |
| Fsync fermo o errore controllato |Errore di custodia esplicito, watchdog/cleanup limitati, raw recuperabile |
| Done/EOF accodato più salto del clock locale |Non perdere evidenza o inventare PASS retroattivo; errore classificato |
| Consumo locale sospeso/perdita trasporto simulata |Fake journal remoto continua entro budget, recupero senza seconda richiesta |
| Child ignora TERM |Escalation/grace ed exit/forced_kill persistiti, nessun falso “Ollama spento” |
| Observer/clock civile alterato |Budget monotonic non esteso; optional error non sovrascrive lo STOP principale |
| Guardie con sink bloccato |Stesse soglie4GB/64MiB/s/5s, azione indipendente dalla telemetria |

Nessuna simulazione del controller è stata eseguita in questa sessione:
soltanto analisi statica e parsing dei raw. Il piano non dimostra una correzione
e non aggiorna i risultati storici. Anche fixture tutte superate non attestano
la cancellazione reale del daemon o la qualità del modello: quei limiti restano
separati e non devono essere trasformati in una nuova campagna automatica.

## 8. Nuovo Gemma e implicazioni Qwen27 mmap

**Prima occorre autorizzare e validare la correzione non generativa**, non
una nuova richiesta modello. Un ulteriore Gemma avrebbe senso solo dopo tale
gate e con consenso distinto: i dati mancanti non si ricostruiscono offline,
ma non serve riprovare subito per diagnosticare i difetti del controller.
Restano un solo caso e una POST, nessun reset del vecchio ledger o retry.

Qwen27 con mmap è un esperimento separato non autorizzato. Il problema di
controllo/custodia è comune ai due modelli e va risolto prima; il suo precedente
STOP RAM senza opzione non prova l'esito mmap. Nessun vantaggio qualitativo,
residenza o latenza è trasferibile da Gemma al dense Qwen. Non avviare Qwen
come fallback, né riproporre Qwen9 come qualità adeguata contro il giudizio
del titolare. Qualità tattica, accuratezza/Gate e certificazione restano aperti.

**Conclusione: correzioni verificabili indispensabili prima di un altro test.**
Zero SSH, POST, caricamenti, nuovi modelli, modifiche VPS/RAG/servizi o patch
dei controller. Report/TODO/registro pubblicati insieme, working tree e
pubblicazione verificati. STOP, in attesa della decisione del titolare.
