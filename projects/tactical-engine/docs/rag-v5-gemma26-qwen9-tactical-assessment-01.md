# Valutazione tattica Gemma26 e confronto storico Qwen9B — 01

Data: 2026-11-19. Attività invariata:
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
Baseline: `3b68f98bd7f4b2a4ae51af7ade2b8c96121291ba`.
Commit inventario/script/evidenze: `c05712a90ea02eb92f74f8e4abecedaa44afc6a2`.

## Decisione

**Gemma non dimostra una qualità tattica sufficiente per giustificare oggi
circa14 minuti per risposta.** Migliora alcune contaminazioni del Qwen9B V10,
ma ripete un errore importante di attribuzione del ruolo e non sviluppa un
piano operativo completo. Non è dimostrata superiorità generale su Qwen9B.

**Voto /30 non attribuibile con la documentazione approvata disponibile.**
Esistono criteri/pesi, ma non la griglia completa con ancore per assegnare i
sottovoti. Non inventiamo un20/30, una scala0–5 o una conversione del rubric0–2.
Il giudizio qualitativo sotto è conclusivo nel proprio perimetro; la mancanza
del numero non impedisce di rilevare errori incompatibili col target zero gravi.

La scelta operativa è fermare la ripetizione di Gemma invariato. Fra i candidati
già selezionati, Qwen27 resta quello da considerare successivamente, **non da
eseguire ora**: il precedente tentativo sul server attuale ha violato la riserva
RAM. Nessuna nuova inferenza è giustificata nello stesso assetto senza una
soluzione tecnica distinta e un'autorizzazione. Non si presume che27B sia migliore.

## Riconciliazione, metodo e tracciamento

Consultati TODO/Experiment Register, report/runtime02, risposta finale esatta,
V10-02 con sei fonti, rubriche, risultati Qwen9B V6–V10, RD-THINK e report
storici. Branch corretto, HEAD locale/GitHub uguali alla baseline, tree iniziale
pulito. Nessuna valutazione equivalente di questa risposta già pubblicata.
Non modificati giudizi o risposte precedenti. Nessun test, SSH, POST o inferenza.

Attività → `collect_gemma_qwen9_tactical_review_01.py`, sola lettura di JSON e
sorgenti Git → commit evidenze sopra → questo report e matrice → diagnosi
qualitativa e confronto diretto limitato → nessuna prosecuzione automatica →
ESEGUITO / VALIDATO come analisi documentale; voto numerico e target BLOCCATO.

Revisore: Codex, analisi interna documentale non cieca. Non rappresenta una
commissione federale, una revisione umana esterna o una certificazione.
Valutata soltanto la risposta finale; thinking interno, latenza e dimensione
del modello non entrano nel giudizio tattico. Originali e SHA in
`docs/gemma26-qwen9-tactical-review-01/source-inventory.json`.

## Quesito e fonti effettive

> Il candidato analizzi la costruzione dal basso contro un avversario che attua
> un pressing alto, forte e orientato sull'uomo (pressione uomo su uomo a tutto
> campo). Ci illustri le strategie tattiche collettive e i codici di movimento
> (es. rotazioni, svuotamento di spazi, utilizzo del terzo uomo) idonei a superare
> la prima linea di pressione, specificando la gestione del rischio e il ruolo
> strategico del portiere in questo specifico scenario.

Non sono stabiliti modulo, numero di pressanti nella prima linea o una
superiorità3v2 già esistente. Non è una domanda sull'attacco del blocco basso.

| Fonte | Contenuto disponibile | Limite per il quesito |
|---|---|---|
|F1 Manuale Catene ESTESO v2, p14|Rotazioni, ampiezza/mezzo spazio e protezione centrale contro blocco basso|Non descrive il pressing uomo su uomo a tutto campo|
|F2 334_principi_Glerean, p14 nel record|Distribuzione del portiere, scelta e tecnica; anche uscite difensive|Non è un protocollo completo di prima costruzione contro uomo|
|F3 Allegati_255201293236, pp23–25|Combinazioni ed esercitazioni di conduzione/cross|Non dimostra automaticamente uscite di prima linea|
|F4 maldera_tesi-uefa-pro, p14|Didascalia portiere/costruzione bassa/principio terzo uomo|Non fornisce l'intera sequenza o condizioni di necessità|
|F5 Manuale Terzo Uomo, p8|Attacco posizionale contro7–8 difendenti, zona14, scarico/tiro|Scope blocco basso, non uscita dalla pressione alta|
|F6 Manuale Costruzione Dal Basso, p4|Pressione a due: portiere aggiunto oppure pivot che si abbassa, alternativa lunga e seconda palla|Non garantisce3v2 contro marcature uomo a tutto campo|

Testi integrali e risposte originali restano nei JSON; il confronto-inputs
conserva copie documentali senza sostituire gli originali. Lettura integrale
anche delle fonti: non deduciamo la fedeltà dalla semplice esistenza di[F1].

## Rubrica disponibile e limite numerico

`compare_frozen_thinking_rd01.py:RUBRIC`, `rd-think-01-result.json` e relativo
report congelano correttezza35%, copertura25%, coerenza ruolo/lato/fase20%,
supporto15%, vincoli5%. Il protocollo Coverciano storico richiede voto /30,
ma non contiene ancore complete per questa attribuzione.

Il protocollo del pilot, `rag-v5-quality-first-paired-pilot-protocol-review-01.md`
sezione «Valutazione cieca e responsabilità», richiede di congelare con il
revisore la griglia mancante **prima dell'invio**. Anche
`rag-v5-quality-first-local-coach-selection-01.md`, sezione «Come misurare28/30»,
vieta di inventarla dopo aver letto gli output. Nessuna griglia aggiuntiva
risulta nei manifest/risultati consultati. La rubrica holdout0–2 è distinta e
non viene convertita in trentesimi. Il tactical_answer_audit booleano non è un
voto e non dimostra correttezza sostanziale.

| Criterio ufficiale del progetto | Peso | Gemma / sottovoto | Qwen V10 / sottovoto |
|---|---:|---|---|
|Correttezza tattica|35%|Non assegnato; errore ruolo e superiorità non condizionata|Non assegnato; errori di ruolo, scenario e sequenza|
|Copertura|25%|Non assegnato; principi presenti, piano operativo incompleto|Non assegnato; voci presenti ma parte della concretezza è incoerente|
|Coerenza ruolo/lato/fase|20%|Non assegnato; scenario meglio preservato, pivot attribuito al portiere|Non assegnato; errore condiviso e contaminazione da blocco basso/cross|
|Supporto documentale|15%|Non assegnato; limiti riconosciuti, alcuni salti prescrittivi|Non assegnato; fonti di scope diverso usate come istruzioni dirette|
|Vincoli|5%|Non assegnato;318 parole, italiano e citazioni|Non assegnato;388 parole nel testo versionato, contro350 del caller documentato|
|Totale /30|100%|**Non attribuibile senza griglia completa**|**Non attribuibile senza griglia completa**|

I pesi sono quelli del progetto, non una rubrica ufficiale FIGC attestata.
Nessun dato hardware viene usato per sottrarre punti tattici.

## Esame indipendente Gemma: rilievi con testo esatto

**G1 — errore di ruolo, grave rispetto alla richiesta sul portiere.**
«può agire come terzo uomo della prima linea [F6] o come pivot che si abbassa [F6]».
La sintassi assegna entrambe le funzioni al portiere. F6 propone invece
l'alternativa del pivot che si abbassa; non specifica un portiere che diventa
quel centrocampista. Non è la parola pivot in astratto a essere vietata:
è l'identità e il movimento attribuiti nello scenario senza alcuna rotazione
che li renda coerenti. Lo stesso errore compare in Qwen V7–V10. Input F6
ellittico e risoluzione generata interagiscono; non si inferisce un meccanismo
interno del modello né si attribuisce tutto al retrieval.

**G2 — generalizzazione tattica non condizionata, rilevante e potenzialmente
 grave se applicata.** «L'impiego del portiere o di un pivot permette di
trasformare una situazione di parità in un 3 contro 2 nella prima fase di
costruzione [F6].» F6 riguarda pressione a due, la domanda non fissa due
pressanti. Un pivot seguito dal proprio marcatore non garantisce un uomo libero:
mancano condizioni e compensazioni. Il3v2 è una possibile struttura, non una
conseguenza automatica delle due alternative. Il testo non dichiara questa
estensione come ipotesi, pur usando altrove il tag inferenza.

**G3 — precisione e applicabilità insufficienti, non una sequenza dimostrata.**
«una sequenza di passaggi che scavalchi il giocatore sotto marcatura».
Non identifica portatore, appoggio e terzo destinatario, direzione del movimento
né innesco della corsa. Scavalcare il compagno marcato non spiega da solo come
renderlo raggiungibile indirettamente. La frase è ambigua, non si sostiene che
ogni uso del terzo uomo debba seguire un unico schema rigido.

**G4 — rischio/alternative, omissione e limite della fonte.**
«deve evitare di "appoggiarsi" troppo ai difensori vicini [F2]».
F2 sostiene la prescrizione generale, quindi non è una citazione inventata.
Ma mancano criteri per scegliere quando il corto attragga utilmente il pressing,
quando sia schermato e quando il lungo preparato sia preferibile. Il testo
dice «troppo»: non gli attribuiamo il divieto assoluto di ogni passaggio corto.

**G5 — posizionamenti e tempi non resi operativi.**
«creando spazi attraverso lo svuotamento di zone occupate».
Il principio è plausibile e dichiarato come inferenza; non dice chi svuota,
chi occupa dopo, cosa leggere se il marcatore segue/consegna né su quale passaggio
sincronizzare. È un'omissione, non prova che rotazioni e svuotamenti siano sbagliati.
Non serve inventare un modulo: servono relazioni e condizioni riconoscibili.

**G6 — transizioni/preventive soltanto nominate.**
«è fondamentale controllare la protezione centrale per non esporsi a transizioni
avversarie rapide [F1]». Corretto principio e fonte pertinente, ma non assegna
chi rimane a protezione, come si collega allo spostamento del pivot e chi
presidia/raccoglie la seconda palla. Il rischio è dichiarato, non organizzato.

**G7 — forza prescrittiva superiore al supporto.**
«L'utilizzo del "terzo uomo" [F4] è essenziale». F4 è una didascalia che nomina
il principio: non dimostra che sia sempre necessario. Supporto al concetto,
non alla forza della prescrizione; rilievo secondario rispetto aG1/G2.

### Elementi positivi e copertura dei dieci aspetti richiesti

Gemma riconosce correttamente lo scope limitato diF1/F5 eF3 e distingue
esplicitamente inferenze e fonti. Resta in costruzione/possesso, propone anche
palla oltre la pressione con seconda palla, ricorda protezione centrale,
non introduce la falsa convenienza2v1→2v2 del Qwen V10. È leggibile e nelle350
parole richieste. Questi miglioramenti sono reali nel testo, non equivalgono
alla capacità di allenare i movimenti sul campo.

Correttezza: G1/G2; precisione: G3/G7; coerenza scenario: migliore maG2;
applicabilità: G3–G6; posizioni: G1/G5; tempi/sincronizzazioni: G3/G5;
alternative: corta/lunga presenti maG4; transizioni/preventive: G6;
fedeltà: positivo riconoscimento scope, limitiG1/G2/G7;
completezza: quesito riconosciuto, codici esecutivi incompleti.

## Recupero storico Qwen9B e comparabilità — Caso A

Recuperate **cinque risposte effettive** a identica domanda nei JSON
`evaluation/coverciano-remediation-v{6,7,8,9,10}/case_02.json`.
Tutte registrano `model=qwen3.5:9b`, non Qwen27. Il digest non è nel singolo
record: non attribuiamo automaticamente al V10 quello osservato in RD-THINK
il giorno seguente. RD-THINK documenta9B Q4_K_M/digest56671c2a..., ma su
V10.2 caso10, altra domanda: è solo prova storica separata, non confronto diretto.

| Artefatto Qwen9B | Domanda/fonti | Risposta registrata e storia | Metriche archiviate |
|---|---|---|---|
|V6 case02|Stessa domanda; fonti diverse|303 parole, sequenza portatore-appoggio-terzo uomo più concreta; nessun repair dichiarato|322.05s pipeline,468 token, stop|
|V7 case02|Stessa domanda e sei fonti Gemma|320 parole; pivot attribuito al portiere, zona14 e ruoli difensivi contaminano l'uscita; repair per copertura|251.77s pipeline,601 token finale, stop|
|V8 case02|Stessa domanda/fonti|338 parole; blocco basso e zona14/tiro importati; repair registrato, prima generazione selezionata|247.98s pipeline,521 token finale, stop|
|V9 case02|Stessa domanda/fonti|352 parole; cross, pali e area d'attacco usati per uscita dalla prima linea; nessun repair dichiarato|157.65s pipeline,547 token, stop|
|V10 case02|Stessa domanda/fonti|388 parole; espansione falsa2v1→2v2 come obiettivo, lancio radente/testa/zona14; nessun repair dichiarato|168.35s pipeline,616 token, stop|

Risposte integrali, fonti e metriche in `comparison-inputs.json` con link e hash
degli originali. PerV7–V10 il messaggio user ricostruito dal caller
(domanda+sei fonti) coincide byte-per-byte come stringa con quello inviato a
Gemma; V6 no. È una verifica di contesto documentale, non una nuova inferenza.

Il V10 è il confronto principale più recente sul caso. Non lo scegliamo per
fingere che tutte le altre versioni fossero peggiori: V6 aveva già una sequenza
più esplicita di Gemma con input diverso. I cinque risultati non sono cinque
campioni indipendenti dello stesso modello/prompt: sono versioni successive.

### Identità del prompt e parametri: cosa è attestato

Gemma: payload effettivo completo conservato, digest verificato nel runtime,
system «Rispondi in italiano tecnico ... entro350 parole», richiesta di
separare inferenze; temperature1, top_p0.95, top_k64, seed42, thinktrue,
ctx8192/predict4096, streamtrue, keep_alive0/mmaptrue.

Qwen V10: modello/question/evidence/answer/generation direttamente nel JSON.
Report V10 documenta ctx8192 e predict900; il caller nel commit di pubblicazione
`5b2df052b0260139acfa12684ae1267677fd7047` usa temperature0, thinkfalse,
streamfalse, SYSTEM DRIBBLING con istruzione «Rispondi esclusivamente in base
agli estratti numerati forniti», più scoped_guidance, generation_guidance,
generation_contract e concise in base alle opzioni. Queste condizioni sono
coerenti con i flag nel record, ma **il payload HTTP esatto e lo SHA del caller
eseguito non sono archiviati nel singolo caso**. L'estratto sorgente congelato
è in `historical-caller-source.json`, marcato source-only/non-wire.

Non presentiamo quella ricostruzione statica come richiesta originale
osservata. Seed, sampling di default, keep_alive e digest esatti del singolo
V10 restano non attestati. Anche perV6–V9 i parametri non riportati non sono
inventati. Il testo Qwen versionato è il finale del pipeline, che prevedeva
sanificazione: non è garantita l'identità col raw HTTP non conservato. Repair
V7/V8 espliciti; nessun repair dichiarato in V6/V9/V10 non significa assenza
assoluta di ogni postprocessing. Non ricostruiamo risposte assenti.

Non sono voti tattici precedenti i quality_gate_passed o complete del planner.
Il18/30 della prima baseline Coverciano e la media19.90/30 restano i loro dati
storici; non vengono incollati sul V10 o confrontati numericamente con Gemma.
Le valutazioni già pubblicate non sono alterate.

### Confronto diretto testuale, non benchmark causale

| Aspetto | Qwen9B V10 | Gemma26 | Conclusione supportata |
|---|---|---|---|
|Portiere/pivot|Stessa attribuzione incoerente|Errore mantenuto|Nessun miglioramento decisivo|
|Scope blocco basso|Prescrizioni applicate direttamente al pressing alto|Limiti e inferenze dichiarati|Gemma più disciplinato su questo testo|
|Superiorità|«trasformare un2v1 apparente in2v2» come obiettivo|Non ripete tale errore, ma3v2 automatico|Miglioramento circoscritto, problema numerico ancora aperto|
|Uscita lunga|Radente/testa/zona14 mescolati con altre fasi|Oltre pressione e seconda palla senza quella coreografia|Gemma più coerente, ancora senza condizioni operative|
|Terzo uomo|Nomina portatore-appoggio-terzomo ma concatena azioni incongrue|Più generico, meno concatenazioni sbagliate|Non dimostrata superiorità operativa|
|Preventive|Protezione centrale e rischio genericamente richiamati|Stesso limite|Nessun salto dimostrato|
|Vincoli/formulazione|388 parole, etichette operative ripetute|318 parole e limiti delle fonti chiari|Gemma più conciso e trasparente|

Il confronto CasoA è possibile; **non è una prova controllata dell'effetto del
modello**: cambiano system/scaffold, thinking, budget e sampling, e il finale
Qwen può essere postprocessato. Migliore disciplina del testoGemma non dimostra
superiorità generale né una media28/30. Non conosciamo la distribuzione degli
errori su casi inediti.

## Valutazione operativa separata

Gemma:830.616s Ollama,832.287s worker; eval2036 e prompt1609; min RAM disponibile
6178926592 byte,820 sample, massimo gap1.094s. Paging globale massimo circa
434MB/s, swap fino1.610608640GB; nessuna guardia attivata perché available
sempre sopra6GB per il criterio paging. Non è assenza di pressione e non si
attribuisce l'intero traffico globale a Gemma.

Qwen V10: total_duration Ollama156.336670s e168.35s pipeline;616 token output,
prompt2263, stop; load circa0.0011s contro37.028s Gemma. Per quel caso manca
una traccia RAM/swap equivalente. Quindi né memoria né latenza sono un confronto
hardware a condizioni identiche: warm/cold, thinking, token e pipeline differiscono.
Il risultato operativo resta che Gemma qui richiede circa14 minuti per318 parole.

Il flusso02 è rimasto BLOCCATO per deadline locale tardiva: non confondiamo
questa anomalia del client con qualità del contenuto o fallimento del modello
sul server, che ha completato entro900s. Nessuna penalità tattica per latenza,
paging o controller; questi pesano solo sulla convenienza operativa.

## Sei risposte finali richieste

1. **Voto giustificabile:** nessun numero /30 attribuito. Pesi disponibili,
   griglia/ancore approvate mancanti; giudizio qualitativo negativo rispetto
   all'obiettivo di risposte affidabili con zero errori gravi. Non è un voto0.
2. **Errori più gravi:** portiere confuso col pivot che si abbassa e3v2 presentato
   senza condizioni per una pressione uomo a tutto campo; seguono movimenti,
   inneschi e preventive non specificati. G1–G7 documentati con citazioni esatte.
3. **Migliore di Qwen9B?** Migliore del testoV10 su scope, trasparenza e alcune
   concatenazioni; non dimostrabilmente migliore in senso tattico generale,
   né causalmente per il solo cambio modello. V6 impedisce una narrativa di
   progresso uniforme su ogni aspetto.
4. **Vale14 minuti?** No, il vantaggio osservato non giustifica quel costo
   operativo per una risposta ancora carente sul ruolo centrale del quesito.
   Il voto tattico non è stato abbassato per la lentezza.
5. **Evidenze mancanti:** griglia completa per /30, confronto a prompt/config
   identici con risposte non postprocessate, risultati rappresentativi su casi
   inediti e memoria comparabile. Il voto potrebbe essere attribuito in futuro
   offline sugli stessi testi con una griglia legittima, senza nuova generazione;
   non viene creata retroattivamente qui.
6. **Proseguire?** Non ripetere Gemma invariato. Qwen27 è il successivo candidato
   condizionato, non un vincitore o un test autorizzato. Il precedente
   `qwen3.8:27b` aveva STOP RAM dopo32.352s, available3149516800<4GB, nessuna
   risposta: vietato riproporlo nello stesso assetto come se quel limite non
   esistesse. Riferimento: protocol-review sezione Qwen27 isolato e audit
   hardware. Serve eventuale scelta tecnica/autorizzazione separata, non un
   nuovo avvio automatico o una promessa basata sui parametri27B.

Report/TODO/registro pubblicati contestualmente. Analisi ESEGUITO/VALIDATO
solo documentale; voto numerico/qualità target/Gate/integrazione/certificazione
restano BLOCCATO. Originali e precedenti voti immutati. **STOP, zero SSH/POST,
inferenze, retry o nuovi test.**
