# Revisione differenziale del pilot Gemma26 / Qwen27

Data: 2026-11-11. Attività esistente:
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`. Fase: revisione documentale.
Pilot **DA FARE**, non autorizzato. Nessun nuovo identificativo sperimentale.

## Giudizio indipendente

**Adeguato con correzioni per triage e preferenza preliminare; insufficiente
per scegliere definitivamente il miglior allenatore o dimostrare 28/30.**
Il rischio di scegliere il modello sbagliato rimane: tre casi noti, una sola
estrazione stocastica per coppia e fonti parziali non identificano il potenziale
tattico generale. Perfezionare il protocollo serve soprattutto a evitare una
falsa vittoria per memoria, template, troncamento, abbellimento o fonti migliori.

Non confermo un vantaggio iniziale di Gemma nella decisione del pilot. Le
priorità della selezione precedente restano ipotesi; non entrano nella scheda
cieca. Qwen migliore e sostenibile prevale anche se più lento; Gemma può
prevalere a qualità indistinguibile sul campione soltanto con efficienza
osservata e limiti espliciti. Nessuno parte con un voto o un bonus economico.

## Riconciliazione, delta e tracciamento

HEAD iniziale locale/GitHub `8d5b0466ab7ca52ef51496b0526e9df703a31cdb`, branch
`codex/tactical-state-contract-v1`, working tree pulito. TODO, registro e
report di selezione confrontati byte-per-byte con GitHub allo SHA esatto.
L'attività risulta proposta, non eseguita; nessun tentativo di questo pilot
individuato nei documenti/artifatti versionati pertinenti. Non è una verifica
della VPS, oggi vietata: l'assenza remota di tentativi andrà verificata soltanto
nel successivo perimetro autorizzato, prima dell'invio.

Consultati i tre JSON congelati, caller `chat()` e rubrica in
`compare_frozen_thinking_rd01.py`, rubrica holdout e report qualitativi già
pubblicati. Nessun import, test o riesecuzione dei benchmark. Metodo/script:
lettura statica dei campi JSON/codice, riferimenti puntuali e hash; nessun driver
preparato. Evidenza nuova in
[`quality-first-paired-pilot-review-evidence-01.json`](quality-first-paired-pilot-review-evidence-01.json).

Correzioni sostanziali: audit della capacità discriminante delle fonti; rischio
contesto già segnalato dai contatori storici; separazione fra esito tecnico e
qualità; profili nativi e campionamento espliciti; giudizio cieco, censura del
confronto e regole di preferenza conservative. Nessuna nuova shortlist,
attività equivalente o revisione di risultati. Questo differenziale perfeziona
la sezione pilot del report precedente senza riscriverla.

Attività → metodo statico/script di analisi documentale → commit contestuale
report/evidenza/TODO/registro → questo differenziale → rilievi e protocollo
proposto → decisione di triage condizionato → revisione **ESEGUITO**; pilot
**DA FARE**. Il commit è quello che introduce questo file, recuperabile da Git.
Non viene inventato uno SHA autoreferenziale.

## I tre casi: discriminanti reali e lacune

Gli originali, hash e JSON Pointer sono nell'inventario. Non assegno nuovi voti
o una gravità ufficiale ai testi storici; i rilievi seguenti sono osservazioni
statiche che spiegano la scelta dei casi, non una nuova adjudication completa.

| Caso congelato | Difetto osservabile e prova nel file | Capacità che può discriminare | Limite delle evidenze |
|---|---|---|---|
| V10 case_02, costruzione contro pressing alto uomo su uomo | Answer tratta il passaggio da 2v1 a 2v2 come beneficio; F1 lo descrive come rischio contro blocco basso. Combina lancio del portiere e zona14 da fonti di scenari diversi | Ruolo portiere, terzo uomo, condizioni corta/lunga, coerenza spaziale e riconoscimento dello scope | F1/F5 riguardano blocco basso; F3 esercitazioni; F4 è una didascalia e F6 pressione a due. Non forniscono una soluzione completa contro uomo a tutto campo |
| V10 case_03, difesa su cross | Postura semiaperta attribuita a F3, che tratta ricezione offensiva. Answer presenta la copertura porta come alternativa a portiere fermo, mentre F4 la propone anche con portiere in uscita | Relazione difensore/attaccante/portiere/porta, spazio, traiettoria, decisioni condizionali e correttezza delle citazioni | F4 è direttamente pertinente; F1 mescola possesso/non possesso; F3 è offensivo; F6 è titolo/sottotitolo, non una trattazione posturale completa |
| V10.2 case_10, vantaggio e cambio 4-3-3/3-5-2/4-2-3-1 | Prima mantiene i tre centrocampisti nel reparto, poi fa scendere un centrale nello spazio liberato senza chiarire tempi e compiti; cita F3 sulla ricezione per motivare la trasformazione | Conservazione dei giocatori/ruoli, sequenze prima-dopo, sostituzione, comunicazione live, equilibrio transizionale | F1/F2/F5/F6 sostengono principi e comunicazione, non una mappa completa del cambio. F4 descrive un 4-4-2: non prova la sicurezza di ogni 3-5-2 |

Sono casi complementari per costruzione, difesa e gestione gara: coprono ruoli,
posizioni, condizioni, fonti e completezza; il caso10 è l'unico cambio sistema
esplicito e la sequenza temporale è soprattutto discussa, non simulata. Non
coprono rappresentativamente tutte le trasformazioni, avversari, fasi,
incertezze e profondità richieste a un professionista. Non aggiungo casi.

**Rilievo decisivo:** fonti uguali isolano il retrieval come variabile fra i
due candidati, ma non rendono il retrieval adeguato. I casi02/10 possono premiare
la gestione dell'insufficienza più della costruzione di una soluzione completa.
Un'astensione motivata o una proposta dichiarata come inferenza non equivale a
una citazione inventata, ma neppure a una prova di capacità completa 28/30.
Se entrambi si fermano correttamente dove le fonti non bastano, esito non
discriminante; non aumentare il voto per compensare una lacuna del materiale.

Prima delle generazioni il revisore deve congelare per ciascuna richiesta una
mappa di supporto: direttamente documentato, inferenza tattica ammissibile da
segnalare, non determinabile dalle fonti. Questa mappa resta nascosta ai modelli;
non contiene una risposta modello da copiare. Non correggere o sostituire F1–F6.
La precedente risposta Qwen e i suoi gate non sono Gold né input dei candidati.
Case10 reca un repair selezionato e un gate non superato: non usarlo come
baseline single-shot, e non rigenerarlo.

## Protocollo finale proposto: stesso pilot, massimo sei risposte

### Ingresso e isolamento

Tre domande e sei fonti di ogni caso preservate come testo, ordine, label,
provenienza e pagine, senza normalizzazione OCR. I payload dei due candidati
devono contenere identico contenuto semantico e vincoli. Sono ammesse soltanto
le differenze di rendering/token speciali richieste dal template nativo.

Il futuro driver separato deve usare una whitelist: domanda ed evidenze,
istruzioni generali comuni approvate, senza answer storico, giudizi, Gold,
rubriche nascoste, soluzioni/repair o diagnostica di copertura. Non serializzare
l'intero JSON di caso o iniettare automaticamente `tactical_plan` e
`generation_contract`: potrebbero contaminare la prova. Nessun nuovo retrieval,
embedding, reranker, corpus, accesso Internet o strumento per il modello.

Nessun nuovo driver viene implementato oggi. Il caller applicativo attuale
non è riutilizzabile alla cieca: `chat()` forza thinking off, sanitizza e può
inviare repair. Il protocollo deve conservare la prima risposta grezza e
separare solo i canali mediante il parser nativo, senza riscrivere contenuti.

### Reasoning e opportunità: capacità pubblica, runtime ancora non verificato

| Aspetto | Scelta proposta prima dell'esecuzione | Limite da registrare |
|---|---|---|
| Identità | Gemma26 e Qwen27 Q4_K_M del report, digest completo, build, template e tokenizer congelati | Gli hash brevi del catalogo non identificano da soli l'installazione |
| Gemma26 | Thinking nativo attivo, system/user supportati, controllo nativo risolto | La card documenta `enable_thinking`; non dimostra come la build Ollama installata lo mappi |
| Qwen27 | Thinking nativo attivo; profilo default xhigh, se rappresentabile/verificabile nel runtime | Non equiparare `think=true` a xhigh senza evidenza; non abbassare a medium per farlo finire |
| Campionamento | Raccomandazioni thinking delle card: entrambi temperatura1/top_p0,95; top_k64 Gemma, top_k20 Qwen. Qwen min_p0/presence_penalty0/repeat_penalty1; default restanti risolti e congelati | Confronto di profili nativi, non esperimento a identico decoder; una sola estrazione non misura varianza |
| Seed | Un valore registrato se effettivamente supportato, senza ricerca del seed migliore | Stesso seed non significa stessi campioni o determinismo fra architetture |
| Storia | Una richiesta indipendente per caso, senza turni precedenti o ragionamenti riutilizzati | Il preserve_thinking multi-turn di Qwen non crea un vantaggio su un turno singolo |

Fonti specifiche, non evidenze della VPS:
[Gemma26 alla revisione congelata](https://huggingface.co/google/gemma-4-26B-A4B-it/blob/4d7ae4984b7db7de8f8457170b3f1a419ee76d52/README.md),
[Qwen27 alla revisione congelata](https://huggingface.co/Qwen/Qwen3.8-27B/blob/37561816e66b5b9153b1b64c10968c18c1e6f4a0/README.md).
Non si applicano al Gemma4 istruzioni generiche di formatter di generazioni
precedenti che escludono il ruolo system. Non costruire manualmente un prompt
misto con delimitatori di famiglie diverse.

La [documentazione Ollama thinking](https://docs.ollama.com/capabilities/thinking)
prevede controlli dipendenti dal modello e metadata `/api/show`; livelli non
supportati possono ricadere sul default. Questo fallback del servizio non è
accettabile come configurazione verificata. Prima dell'invio serve prova del
profilo effettivo e del parsing nella build reale: i campi potrebbero mancare
nella 0.40.5. L'assenza di metadata da sola non dimostra né supporto né assenza
di thinking. Nessuna equivalenza ABI o compatibilità remota è attestata qui.
Se i profili non sono verificabili senza una generazione di prova, non fare
quella generazione: fermarsi prima delle sei richieste autorizzabili.

### Budget: limiti di una prova operativa, non identità di ragionamento

Mantengo come **proposta condizionata** contesto 8192 e massimo 4096 token totali
generati per richiesta, reasoning incluso. Nessuna riserva per la risposta
finale ottenuta forzando la chiusura del pensiero, nessuna continuazione o
seconda chiamata. Il meccanismo effettivo di conteggio va documentato per la
build: contatori aggregati non dimostrano una ripartizione identica fra canali.
Un token dei due tokenizer non rappresenta lo stesso lavoro o contenuto.

**Gate di contesto prima di ogni invio:** contare il prompt realmente renderizzato
con tokenizer/template equivalenti al servizio, special token inclusi; verificare
`prompt + budget totale di output <=8192` secondo la contabilità effettiva del
runtime. Nessuna stima da byte/caratteri e nessun conteggio di Qwen9 trasferito
ai nuovi modelli. Il caso10 storico riporta 4146 token del **repair selezionato**,
non del primo prompt: il caller restituisce i contatori dell'oggetto scelto.
Sommando 4096 si ottiene 8242, oltre 8192; questa aritmetica non prova overflow
del futuro single-shot. Serve soltanto a non riusare contatori storici come
attestazione del budget. Non basta che il prompt da solo entri nel contesto.

Se il conteggio non è attendibile o il gate fallisce: STOP prima della POST.
Niente taglio delle fonti, riduzione del reasoning di un solo candidato,
riassunto automatico o ampliamento del contesto senza consenso. Una diversa
coppia contesto/budget richiede una revisione dichiarata dello stesso pilot,
con verifica risorse e autorizzazione prima degli output; non un tuning sui
primi risultati. Nessun tokenizer alternativo o vecchio harness ABI viene
introdotto per aggirare questo gate.

Risposta finale richiesta entro 350 parole, contata separatamente dal thinking
con regola di conteggio congelata; conservare tutto il testo. Sforamento è
violazione dell'istruzione, non autorizza taglio o riscrittura. Incompleta o
priva di finale è osservazione censurata per il confronto di potenziale:
non assegnare automaticamente zero al ragionamento che il limite ha impedito
di osservare. Si registra comunque l'inutilizzabilità operativa di quella
risposta nel punto di budget scelto.

Timeout massimo 900 secondi per richiesta, **inclusi caricamento/prefill/decoding**;
massimo 5400 secondi per sei richieste, nessun warm-up. È un tetto della prova,
non uno SLA d'uso già approvato. La tolleranza reale di attesa del titolare va
concordata prima, senza introdurre pesi economici. Un timeout non prova da
solo inferiorità tattica; nessun retry, repair, routing o secondo tentativo.
Non trasformare timer HTTP o socket chiuso in prova di cancellazione remota:
supervisione e rilevazione di eventuale attività residua devono essere definite
prima; con stato ambiguo STOP dell'intero pilot, senza invii successivi.

Correzione di osservabilità proposta: una POST streaming per caso/modello,
registrazione append-only degli eventi grezzi, stdout/stderr ed evento finale;
conserva anche contenuto parziale. Non crea più generazioni. Dalla
[API chat](https://docs.ollama.com/api/chat) raccogliere done/reason, load_duration,
prompt_eval_duration/count, eval_duration/count e durate totali. Valori e
presenza effettivi vanno verificati, non inventati. Se non distinguibili,
conteggi thinking/finale restano non disponibili; non dedurli dalle parole.

Parità perfetta non esiste: quantizzazione con lo stesso nome, cap di token,
native top_k/effort e tokenizer differenti possono favorire un'architettura.
Questo pilot confronta **due punti operativi dichiarati entro un tetto comune**,
non il massimo potenziale assoluto. Un limite attivo impedisce una graduatoria
di capacità generali. Non cercare dopo il risultato un budget che faccia
vincere il candidato preferito.

### Risorse, concorrenza e condizioni di arresto

Prima dell'avvio: identità SSH/host key, integrità input/modelli, build e
prerequisiti, assenza di tentativi precedenti, servizi richiesti e contesto;
ledger persistente esclusivo, lock condiviso esistente acquisito senza attesa
solo se autorizzato. Nessuna creazione/correzione del lock o dei permessi.
Qualunque invio già presente o ambiguo impedisce la ripetizione del pilot.

Un modello di pilot alla volta, nessuna concorrenza generativa. Sequenza
predefinita: caso02 Gemma/Qwen, caso03 Qwen/Gemma, caso10 Gemma/Qwen. Tre
coppie non bilanciano perfettamente l'ordine: registrarlo come limite. Non
caricare/unloadare altri modelli o fermare servizi per far entrare i candidati.
Gestione proposta delle sole richieste del pilot: `keep_alive=0`, se supportato,
per rilascio dopo ciascuna risposta, senza POST aggiuntive di warm-up/unload.
Misurare il caricamento separatamente e annotare cache filesystem: non chiamare
«cold disk» una richiesta solo perché il modello non era residente.

Con strumenti già presenti e letture soltanto: memoria prima/durante/dopo,
MemAvailable minimo, RSS/PSS/HWM quando accessibili, swap occupata e contatori
swap-in/out, processi modello/servizi, tempi di carico/prefill/generazione,
primo token/finale, token e conclusione. Definire cadenza prima del test
(proposta un secondo); riportare **massimo osservato campionato**, non picco
continuo garantito. RSS di processi e cache condivisa non vanno sommati due
volte. Nessuna installazione di profiler o agente. Non inviare richieste di
controllo che generino testo e non cambiare API/panel.

Margine prudenziale proposto: MemAvailable almeno 4 GB decimali, unità esplicita,
oltre alla conservazione dei servizi; non è RAM minima dimostrata del modello.
Swap già occupata va distinta da paging attivo; nuovo swap-in/out durante la
prova rende la sostenibilità non dimostrata e impone STOP, non un successo
perché «il modello si carica». Stop anche per saturazione o impatto osservabile
sui servizi. Nessun workaround, quantizzazione alternativa, upgrade, costo
aggiuntivo, rinnovo VPS o cambio runtime automatico.

## Valutazione cieca e responsabilità

Un revisore tattico umano qualificato valuta gli output con codici anonimi,
ordine di presentazione distinto da quello di esecuzione, senza identità,
benchmark, priorità iniziale, ragionamento interno, tempi o consumi. Vede domanda,
fonti complete e **testo finale esatto**; il raw completo resta conservato.
Chi custodisce l'associazione codice-modello non guida il voto. Nessuna
sanitizzazione del contenuto; un'autodichiarazione del modello nel testo va
registrata come possibile rottura del cieco, non cancellata silenziosamente.

Per ciascuna risposta, scheda documentale, non framework nuovo:

- Voto /30 e motivazione con rubrica RD-THINK esistente: correttezza 35,
  copertura 25, coerenza ruolo/lato/fase 20, supporto 15, vincoli 5. Non è rubrica
  federale attestata. Se ancore/griglia completa del voto mancano, congelarle
  con il revisore e approvazione prima dell'invio; niente conversione dei 0–2.
- Cinque assi strategici 35/25/20/15/5 come commento qualitativo separato:
  nessun secondo totale numerico che sostituisca /30.
- Ruoli/posizioni, fase/sequenze, contraddizioni, supporto per ogni affermazione,
  completezza, spiegazione italiana, errori gravi e richieste non determinabili.
- Distinzione fra dato di fonte e inferenza esplicitamente dichiarata: nessun
  bonus per dettagli inventati che rendano una risposta apparentemente completa.
- Causa proposta per rilievo: **A generatore**, **B evidenze**, **C interazione**,
  oppure mista/non determinabile. Le classi causali non sono stati del progetto.
  Identificare passaggio di fonte/output/log che sostiene l'attribuzione.

A: fonte pertinente correttamente disponibile ma output la contraddice; B: pezzo
necessario assente/fuori scope; C: template, rendering o contesto alterano la
fruizione. C non si dimostra soltanto da una risposta sbagliata; una singola
osservazione spesso non separa cause concorrenti. Non imputare al generatore
la mancanza di una mappa completa nelle fonti, né giustificare con B una sua
citazione inventata o contraddizione dimostrabile.

Revisore chiude i voti prima di vedere risorse e identità. Un secondo esperto
adjudica solo controversie sostanziali prima della decisione; non si risolvono
con un giudice automatico o scegliendo il voto favorevole. Nessun voto oggi.

## Regole decisionali congelate prima del pilot

Sono regole conservative per una **priorità successiva**, non un test di
significatività o un nuovo score. Interpretazione in ordine: integrità del
confronto → qualità in cieco → sostenibilità/efficienza senza compensazioni.
Un errore tattico grave del candidato impedisce la sua priorità nel pilot;
F prevale su qualsiasi tie-break economico. Risposte equivalenti ma entrambe
inadeguate non giustificano la scelta di un allenatore per il solo costo.

| Esito | Decisione predefinita |
|---|---|
| A: vantaggio tattico chiaro e sostenibile | Preferenza preliminare solo con tre coppie interpretabili, zero gravi del candidato, superiorità sostanziale motivata in almeno due coppie e nessuna inferiorità sostanziale nella terza, concordata dal revisore/adjudicator. Non basta la media più alta di pochi decimali |
| B: qualità indistinguibile e costo inferiore | Prima documentare stessi limiti critici, completezza e supporto; equivalenza solo sul campione, non dimostrata statisticamente. Con costo attribuibile davvero minore si può preferire il più efficiente; se si conosce solo il tempo, dichiarare efficienza temporale, non euro risparmiati |
| C: qualità migliore ma più lento | Prevale il migliore se la latenza rientra nell'uso accettato dal titolare e risorse/costi sono sostenibili. Nessun bonus velocità nel voto tattico |
| D: insostenibilità tecnica | Registrare misure e STOP dell'intero pilot; nessun workaround. Il confronto incompleto non fa vincere automaticamente il superstite |
| E: insufficienza/contraddizioni/pareggio | Nessun vincitore. Vale anche con fonti non discriminanti, truncation/timeout asimmetrici, profili non verificabili o giudizi controversi |
| F: gravi errori di entrambi | Nessuna promozione, anche se uno è meno lento o ha una media più alta |

L'eventuale voto zero per una risposta incompleta, se previsto dalla rubrica,
va distinto da un confronto di potenziale non identificabile per troncamento:
non usare un unico voto per cancellare il limite metodologico. Dati mancanti
non vengono imputati o esclusi dalla media senza dichiarazione. Calcolare
medie soltanto come descrizione delle risposte effettivamente valutabili,
indicando sempre denominatore e coppie mancanti. Nessuna media di due casi
rinominata «media sui tre» o proiezione su un holdout professionale.

Per economia: fattura VPS, lavoro/revisore e costo integrazione separati;
nessun peso monetario inventato. A canone fisso già pagato una risposta più
veloce non riduce automaticamente la fattura. Costo per risposta utilizzabile
richiede qualità giudicata e costi attribuibili, non token/s. Target futuro
media 28/30 e zero gravi, lode qualitativa su 30/30; vecchi 9/10 e 26/30 intatti.
Anche tre 30/30 non certificano autonomia professionale o generalizzazione.

## Autorizzazioni esecutive ancora necessarie

Nessuna richiesta esecutiva è implicita nella presente revisione. Lo stesso
identificativo resta **DA FARE**. Un mandato separato dovrebbe autorizzare
esattamente, con stop ai gate mancanti:

1. Preparazione locale e verifica statica del piccolo driver single-shot,
   manifest di input/profili/parametri, ledger, anonimizzazione e raccolta;
   congelamento commit/blob/hash, senza modificare il codice applicativo.
2. SSH tramite alias/host key autorizzati, diagnostica read-only minima della
   build, template/capacità, tentativi precedenti e servizi; GET diagnostiche
   e, se necessario, POST **non generativa** `/api/show`. Niente prove chat.
3. Solo se i due artefatti esatti mancano, download locale sulla VPS dei due
   modelli approvati con spazio e hash verificati, senza cambio del modello
   del panel. Nessuna installazione/aggiornamento runtime incluso: se richiesto,
   STOP e distinta decisione del titolare.
4. Misura attendibile del rendering/token budget tramite interfaccia esistente
   supportata, senza pesi o generazione di prova; nessun ritorno al percorso
   ABI. Se non disponibile, non aggirare il gate.
5. Acquisizione/rilascio del lock esistente non bloccante, monitoraggio read-only,
   supervisione controllata, caricamento sequenziale dei soli candidati e
   rilascio tramite le stesse richieste, senza fermare servizi o altri modelli.
6. Massimo sei POST generative /api/chat sul loopback remoto, una per coppia,
   senza retry/repair/continuazioni; raccolta dei raw e giudizio umano cieco
   con costo revisore esplicitamente sostenibile, pubblicazione dei risultati.

Se le identità, il contesto o i profili non sono congelabili, autorizzare
«sei POST» non rende il protocollo eseguibile. Le autorizzazioni possono essere
condizionate ai gate; oggi non viene chiesto o presunto consenso per eseguirle.

## Chiusura

Revisione **ESEGUITO**, proposta corretta solo nel suo perimetro documentale;
pilot **DA FARE**, non **VALIDATO**, non eseguito e senza autorizzazione.
Risorse/compatibilità installata e target 28/30 non dimostrati; Gate,
integrazione e certificazione generale restano **BLOCCATO**. Nessuna SSH,
installazione, modello, inferenza, benchmark o modifica a RAG/applicazione/
panel/VPS/runtime, merge, deploy o costo aggiuntivo. Pubblicazione contestuale
con TODO/registro e verifica GitHub/working tree, poi STOP.
