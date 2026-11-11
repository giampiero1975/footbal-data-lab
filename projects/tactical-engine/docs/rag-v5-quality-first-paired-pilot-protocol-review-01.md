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


## Addendum — riconciliazione definitiva RAG e decisione sul pilot

Data: 2026-11-11. Base documentale di questa riconciliazione:
`93fcbd173b2d41a1e5210c2d4658dec78cde2616`. Attività e pilot restano
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`, **DA FARE**, non autorizzato.
Questo addendum qualifica le evidenze storiche; **non riscrive il protocollo**.

### Evidenze e baseline distinte

TODO, registro e versione precedente di questo report confrontati con GitHub
allo SHA iniziale; branch corretto, working tree pulito. Confrontati commit,
report e artefatti V5/V10, chiusure relazionali, extraction A/R1, caller, runner
e API; solo letture statiche e hash. Nessun test, re-audit applicativo o runtime.
Fatti riproducibili, versioni e SHA-256 in
[`quality-first-pilot-rag-state-reconciliation-01.json`](quality-first-pilot-rag-state-reconciliation-01.json).

La certificazione storica locked riguarda il runtime/manifest congelato a cui
si riferisce, non ogni file del checkout attuale. L'ultimo commit applicativo
nel perimetro scripts/API è `5bfa4897e93d5d8edef0bc79371aa36b1b1409ae` (R1);
le modifiche successive pertinenti sono documentali/operative. La singola
prova A/R1 pubblicata in `4c4682f` ha usato quei file applicativi invariati,
ma su **q3_04**, non sui tre casi del pilot. Il checkout Git più recente non è
una misura del deployment attualmente attivo: **VPS attuale NON VERIFICATO**,
nessuna SSH. NON VERIFICATO è qualifica dell'evidenza, non nuovo stato progetto.

### Che cosa è stato completato e resta valido

| Ambito e difetto originario | Correzione / commit | Evidenza verificata e stato nel perimetro | Limite e decisione attuale |
|---|---|---|---|
| V5 locked: copertura fonti, heading, filtri e guida | `040c6a5`, closeout `e2c093a` | `v5-certification-closeout-01.md`: regressione integrata 10/10, freeze e rollback; **CERTIFICATO** per manifest/runtime/CLI locked | Non riaprire il benchmark; certificazione non estesa al coach universale o alla collection 6410 |
| Retrieval: scelta fonte semanticamente vicina ma incompleta | `30b04d4` ranking rilevanza/copertura; filtro autore `33749bf`, guida `9a1a903` | `v5-source-hybrid-rank-v4.md`: 5/5 offline, fresh03 retrieval+generazione validati; `v5-named-source-context-filter-01.md`: V2 con fonte corretta. Integrazione successiva del profilo attestata dal closeout locked | Vecchie voci «non integrato» dei singoli shadow non annullano l'integrazione successiva. Nessuna nuova patch motivata qui |
| Estensione corpus Drive11/FIGC5 | Implementazione holdout `21eaada`, riconciliazione `936b4c4` | Drive11 **VALIDATO 6/6**, raw Git SHA corrispondente al report; FIGC5 **VALIDATO e INTEGRATO**, 214 chunk aggiunti, regressione composita 10/10 e rollback 6196 | Non sono risultati delle tre domande V10 né certificazione di tutte le fonti. Conservare corpus/indici |
| Coverciano V6–V10: omissioni, fase, ruoli e falsi gate | Query/anchor `8a9a7ce`, gate `55e01e1`, residui `5b2df05`, trasformazione `0f9f87f`, closeout `77824c9` | `rag-coverciano-remediation-v10-runtime-01.md`: V10 incompleto, poi rerun solo 5/6/8/10 e re-audit lessicale; set finale 10/10 **VALIDATO** tecnicamente | Non cancellare il lavoro chiamandolo ancora V10 fallito; non attribuirgli un voto esterno28/30 mai documentato |
| Relazioni attore/compito/fase/spazio/trigger/obiettivo | `0d69be6`, `b4a5f64`, fino a `084cb5b` | Consolidata105/105 nei rispettivi moduli; settima verifica planner/audit 50/50, **VALIDATO** offline | Audit relazionale non bloccante; `complete` legacy non diventa certificatore semantico. Nessuna prova di correzione generativa di tutti i casi |
| Grounding strutturato e incoerenze extraction | Dual-blocker `56a7b72`, A `0ea62c0`, R1 `5bfa489` | 37/37, nuovi 16/16 e 5/5 nei report dedicati, **VALIDATO** offline. Singola API A/R1: risposta strutturale accettata, locator respinge frammenti fuori lato; fail-closed documentato | Errore generativo q3_04 ancora osservato, witness/validation assenti; non è bug dimostrato del locator. Nessuna correzione automatica giustificata dalla diagnosi `4f8c9f6` |
| API e panel: blocco da gate Coverciano nel default | `7c018f9`, regressione dedicata `4532eb6`; API `9472564` e successive integrazioni | Registro27/10: rimozione tactical-plan dal default, ripristino panel **VALIDATO e INTEGRATO**; runner attuale conserva profili opt-in separati | Non riattivare il gate Coverciano su tutte le domande; nessun nuovo intervento API/panel richiesto |

Le quantità sono **risultati storici letti**, non test appena eseguiti. Il raw
Drive11 versionato ha SHA-256
`e7cbcfcaaf1e069c45551c8a9e7fcfd3deb08fa31e310acc263af3c035b6f04a`,
uguale al report. Per il locked si preservano attestazioni e hash del closeout:
non tutti i raw storici citati sono presenti come file versionati in questo
checkout. Non ricostruisco o ripeto quei test per colmare una copia mancante.

Il Gate TSC V2 successivo e il percorso Spatial hanno esiti propri: ad esempio
`docs/tactical-state-contract-v2-runtime-gate-01.md` documenta un arresto
fail-closed, non una promozione. Il successivo stato A/R1 non autorizza a
considerare risolti tutti quei gate. Viceversa il loro blocco **non revoca** la
certificazione locked o le validazioni di retrieval/FIGC5 già raggiunte.

### Riconciliazione puntuale dei tre input contestati

| Input | Versione e problema storico | Correzione successiva effettivamente documentata | Cosa è dimostrato oggi / riuso |
|---|---|---|---|
| V10 case02 | Campagna27/10; pubblicato in `5b2df05`, preparazione V10 nel parent `55e01e1`. Contaminazione cross della V9 già affrontata, ma nel testo V10 restano rilievi sul 2v1/2v2 e sullo scope blocco basso/pressing alto | `55e01e1` introduce il test di contaminazione costruzione/cross; nessun successivo rerun02 pubblicato qui dimostra la chiusura degli esatti rilievi fini di scope | Limite osservato del testo storico. Presenza dello stesso difetto sulla baseline più recente: **NON VERIFICATO**. Fonti riusabili per confronto a input fisso, con limite di copertura già dichiarato |
| V10 case03 | Stessa campagna/pubblicazione. Rilievi su postura offensiva citata per difesa cross e condizioni del portiere | Copertura scenario cross-defence e test planner esistono; non è individuata una prova successiva che chiuda specificamente questi due rilievi per quel caso | Non dichiararlo risolto solo perché il gate è PASS; non dichiararlo ancora presente oggi senza prova. **NON VERIFICATO** sulla baseline recente; input storico riusabile |
| V10.2 case10 | Artefatto pubblicato con `77824c9`, parent Git `0f9f87f`. Succede al V10 con trasformazione di ruoli respinta | `5b2df05` rafforza audit ruoli, `0f9f87f` esplicita geometria, `77824c9` corregge comando/comandi e segnale/segnali; report chiude il set tecnico 10/10 con re-audit | Il difetto noto fu **affrontato e validato tecnicamente nel suo perimetro**. Il raw gate=false è precedente al re-audit e non va sostituito. I rilievi più fini del testo non sono una nuova bocciatura del closeout né prova di difetto attuale: **NON VERIFICATO** |

I JSON non incorporano un'attestazione completa del commit runtime: commit di
pubblicazione e parent ricostruiscono la cronologia Git, non sono una firma del
codice effettivamente eseguito. La raccolta non inventa tale identità.

Le patch posteriori a V10 introducono contratti/audit e handoff dedicati; non
ho trovato una nuova esecuzione delle tre domande che ne misuri il risultato
sulla baseline A/R1. La funzione `chat()` di prosa naturale è inoltre identica
come sorgente fra `5b2df05` e HEAD; questo confronto statico **non dimostra**
identità dell'intera pipeline, degli input o degli output del modello.

Le fonti congelate hanno ancora esattamente i byte del loro artefatto storico;
nessuna correzione successiva del codice aggiorna retroattivamente un F1–F6
già salvato. Le osservazioni sulle loro lacune descrivono **quei pacchetti**,
non un nuovo retrieval della produzione. Non impongono una ricostruzione RAG.

### Componenti riutilizzabili e accoppiamenti reali

| Componente preservato | Indipendenza documentabile dal generatore | Adattamento eventualmente necessario, non eseguito |
|---|---|---|
| Corpus, chunk e database vettoriale | Dati/documenti non sono pesi del generatore; nessun motivo per reindicizzare cambiando soltanto la generazione | Integrità e formato restano contratti distinti; non si certifica oggi lo stato live |
| Embedding | `smoke_test_rag_v5_e2e.py:525` usa `qwen3-embedding:0.6b`, distinto da `--model` generativo | Nessun cambio embedding necessario; condivide Ollama/RAM con gli altri processi |
| Retrieval/reranking | Fasi precedenti a chat, dense24→reranker→contesto; possono essere escluse dal pilot usando il contesto congelato | Il runner coordina risorse/caricamenti: non è un servizio completamente separato. Non cambiarlo per il pilot |
| Generazione | `--model` del runner e `RAG_API_MODEL` dell'API rendono configurabile l'identità | Transport, template, thinking, tokenizer, stop token e post-processing richiedono verifica del modello esatto; non basta cambiare una stringa |
| Contratti/validatori | Controlli deterministici sul contenuto strutturato, distinti dai pesi | Handoff/schema e capacità di produrre quel contratto sono dipendenti dal modello; natural-language pilot non valida TSC/Spatial |
| API/panel | Worker passa il modello configurato al runner; la UI può conservare il contratto risposta/fonti | Parametri, tempi, errori, compatibilità del worker e contatori andranno verificati per una futura integrazione autorizzata, non durante questa selezione |
| Rubriche, raw e benchmark | Evidenze e criteri riutilizzabili e immutabili, non da riscrivere per un candidato | Separare giudizio umano, gate tecnico e target 28/30; niente re-rating retroattivo qui |

Quindi il generatore è sostituibile **come componente**, ma l'integrazione
non è già dimostrata come plug-and-play. Questa distinzione protegge gli asset
senza attribuire alla sola sostituzione del modello la soluzione di ogni errore.

### Decisione operativa unica

**Procedere verso il pilot esistente senza ricominciare lo sviluppo del RAG.**
Gli input restano quelli storici, identici per entrambi; nessuna correzione
di fonti o nuova estrazione è necessaria nel mandato corrente. Il significato
resta confronto preliminare di generatori a evidenza fissa, non benchmark del
retrieval attuale. Modificare oggi gli input aprirebbe una variabile ulteriore
e richiederebbe un congelamento distinto, senza prova che sia indispensabile.
La qualifica storica è la correzione minima della lettura dei dati, non dei dati.

**Singolo prossimo passo:** autorizzare la preparazione/congelamento del driver
e il preflight minimo del medesimo pilot. Nessun nuovo esperimento RAG o
protocollo da inventare. Restano indispensabili, già previsti:

- Identità e supporto effettivo dei due artefatti/build/template/thinking,
  rendering e budget nel contesto senza tagli; niente ABI C++ o harness vecchi.
- Input/parametri e ledger congelati, assenza di un tentativo preesistente,
  host key, lock/concorrenza e raccolta/supervisione single-shot affidabili.
- Memoria/servizi/spazio compatibili senza swap o costi extra; nessuna
  installazione o modifica a runtime/RAG/panel implicitamente permessa.
- Revisore cieco, rubriche e tolleranza operativa concordati prima dei sei
  output; qualità valutata separatamente da prestazioni, senza promessa 28/30.

Il consenso per le generazioni/download/caricamenti resta distinto e deve
rispettare i gate del protocollo già pubblicato. Non vengono avviati ora
né driver né preflight remoto. Nessun nuovo benchmark o controllo RAG è un
prerequisito aggiunto per accedere a questa fase.

### Risposte definitive nel perimetro delle prove

1. **Sì, il lavoro RAG resta valido e riutilizzabile**, con certificazione
   locked e validazioni Drive11/FIGC5, chiusura tecnica V10.1/V10.2 e contratti
   offline nei rispettivi perimetri. Non va ricostruito.
2. **I tre casi sono storici, non una misura attuale**: il difetto noto del
   caso10 è stato affrontato; gli esatti rilievi fini 02/03 e l'eventuale loro
   persistenza sul codice più recente restano NON VERIFICATI. La prova A/R1
   q3_04 osserva un altro problema generativo, correttamente respinto.
3. **Sì, possiamo avanzare al confronto Gemma26/Qwen27** con input invariati e
   stesso identificativo, dopo autorizzazione e soli prerequisiti tecnici già
   previsti. Non emerge una ragione documentata per una nuova patch RAG.

Riconciliazione **ESEGUITO**; risultati precedenti preservati; pilot **DA FARE**.
Target28/30, Gate generativi non superati e certificazione generale restano
**BLOCCATO**, senza revocare il **CERTIFICATO** locked storico. Pubblicazione
contestuale di questo addendum, inventario, TODO e registro; verifica GitHub e
working tree, poi STOP. Nessuna attività esecutiva, costo, merge o deploy.


## Addendum — preparazione tecnica locale del pilot

Data: 2026-11-11. Attività invariata
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`, pilot **DA FARE**.
Mandato limitato a driver/manifest e controlli locali, nessuna autorizzazione
SSH o generativa. Baseline iniziale locale/GitHub `227a862dedf5f36c947ec63dface69c723af1e99`,
branch corretto, tree pulito; TODO/registro/report ufficiali confrontati con
GitHub. Nessun driver equivalente o tentativo locale del pilot individuato;
l'assenza remota non è stata verificata. Riconciliazione RAG conclusa, nessuna
nuova selezione o modifica del protocollo qualitativo.

### Attività → Script → Commit → Report → Risultato → Decisione → Stato

Script separati dall'applicazione in `operations/quality-first-pilot/`:
`paired_pilot_01.py`, worker futuro `paired_pilot_remote_01.py` e lettore
`static_review_01.py`; istruzioni nel README della stessa directory.
Commit tecnico congelato: **3449db8f1d1c68d07fb76b5ff753b6676270bfef**.
Evidenza dei controlli:
[`quality-first-pilot-local-preparation-static-01.json`](quality-first-pilot-local-preparation-static-01.json).
Report: presente addendum, TODO/registro pubblicati contestualmente.

Il controller ha modalità prepare/check, execute con dossier e autorizzazione
separati, export cieco dopo completamento. Eseguite **soltanto prepare e check**
e il lettore statico. Worker e modalità execute/anonymize **mai eseguiti**.
Preparati i tre input con whitelist domanda+evidenze, sei payload identici nel
contenuto per ogni coppia, ordine Gemma/Qwen–Qwen/Gemma–Gemma/Qwen, hash di casi,
richieste e codice. Nessun answer storico, Gold, tactical_plan, repair o voto
entra nei messaggi. Template di valutazione vuoto; nessun output fittizio.

Predisposti, non validati in runtime: ledger canonico esclusivo senza resume,
prenotazione xb+flush/fsync prima di GO, un solo call site POST fuori da cicli
nel worker, massimo sei slot nel controller; raw NDJSON e stdout/stderr,
inventario finale e verifica prima dell'export anonimo. Riutilizzato il pattern
fsync/GO e lock storico del single-case `9fcc212`, senza importare quel driver
o alcun modulo RAG. Gli ID di revisione sono opachi e la mappa custode resta
fuori da blind. La riservatezza richiede consegnare al revisore soltanto blind,
non log o mappa; eventuale autoidentificazione nel content non viene cancellata.

### Verifiche effettive, senza generazioni

**32 controlli statici/di manifest superati**, zero errori nel risultato finale:
AST e compile in memoria dei due programmi (nessun import del worker), assenza
di import applicativi/modelli/ctypes, reachability locale prepare/check senza
trasporto, tre hash di origine e testi preservati, sei slot unici/ordine,
uguaglianza messaggi, whitelist, limiti e hash payload, freeze codice/blob,
file pending con autorizzazione false, ledger assente, unico call site POST,
assenza di loop attorno alla POST, ordine prenotazione→GO→POST, lock read-only,
presenza guardie memoria/swap/deadline, contratto del conteggio e export cieco.
Il lettore statico iniziale ha avuto un errore nel matcher testuale GO, corretto
usando AST; non è stato eseguito alcun trasporto o test applicativo per correggerlo.

`prepare/check` verificano identità/struttura locale, non il comportamento del
trasporto. Il package congelato ha SHA-256 canonico **9c790029ac269c77c6d5946669ed9560df2f73ff1c47dfca38eb402df7eb919d**. Gli hash e
Git blob dei due sorgenti sono nell'evidenza. Nessun controllo storico è stato
ripetuto. Il confronto Git conferma nessuna modifica a scripts/API/RAG.

Lettura della sola metadata delle distribuzioni nell'interprete Python 3.9.5:
transformers/tokenizers/ollama/gguf non risultano installati. Nessuna installazione,
tokenizer o peso caricato. I config e le fonti normative versionate documentano
capacità nominali, non il rendering/token budget del servizio. Non è stata
prodotta alcuna stima token da byte, né invocato il vecchio percorso ABI.

### Profili predisposti e blocchi concreti all'invio

Package con contesto 8192/output 4096, finale 350 parole, temperatura 1/top_p0.95,
top_k 64 Gemma  / 20 Qwen, seed 42 senza ricerca del seed, stream=true/keep_alive=0.
Qwen esplicita i restanti parametri pubblicati; i default effettivi Gemma vanno
attestati. Il supporto seed/opzioni deve essere provato, non dedotto dal payload.
Le due richieste usano think=true: **non è verificata** la risoluzione del
booleano al profilo Gemma e a Qwen xhigh. Nessun downgrade automatico a medium.

`remote_binding.pending.json` e `execution_authorization.pending.json` non
abilitano invii. Il primo richiede evidenze reali revisionate, hash, identità
modelli/template/tokenizer e sei conteggi legati ai payload; il secondo deve
riferirsi agli hash esatti di piano e dossier. Un flag verified non è una prova:
la revisione del dossier è necessaria prima di autorizzarlo.

**Blocco concreto:** non è disponibile in questa fase un metodo attestato di
rendering/conteggio pre-POST equivalente alla build installata. Il controller
richiede prompt_tokens<=4096 per riservare output 4096 in contesto 8192 e rifiuta
prove mancanti; il contatore restituito dopo una generazione non può colmare
questa lacuna preventiva. `/api/show` da solo non conta il prompt. Se non esiste
un'interfaccia attendibile già disponibile senza generazione/caricamento pesi,
STOP: niente ABI, tokenizer alternativo o aumento automatico del budget.

Restano non verificati digest completi Q4_K_M e disponibilità dei due modelli,
versione/capacità reali, mapping thinking/template, parser stream/contatori,
supervisione e concorrenza, risorse/servizi. Il worker contiene guardie sul lock
esistente, processi/modelli osservabili, MemAvailable>=4 GB decimali e swap;
sono controlli predisposti, non misure VPS né prova di isolamento completo.

Il controller ha tetti 900s/slot e 5400s totali; GNU timeout remoto 900s con cleanup
kill-after15s. Il cleanup può durare ulteriori 15s; non si dichiara la
cancellazione del modello entro 900s. Socket chiuso o SSH terminato non
certificano arresto Ollama: conservazione dello stato ambiguo e STOP senza
invii successivi. Cadenza nominale 1s/massimo campionato e reazione ai limiti
vanno verificati nel perimetro remoto prima della prova, non presentati come
picco continuo o comportamento dinamico già validato.

### Operazioni esatte da autorizzare per il solo preflight remoto

1. Connessione `football-vps` con host key autorizzata e StrictHostKeyChecking=yes,
   nessuna accettazione automatica o modifica della configurazione SSH.
2. GET diagnostiche `/api/version`, `/api/tags`, `/api/ps` sul loopback e, se
   necessario, POST **non generativa** `/api/show` dei due modelli già presenti;
   rilevazione digest/formato/quantizzazione/capacità e template effettivi.
3. Sole letture di metadata/config/template e dell'eventuale interfaccia di
   rendering/tokenizzazione già installata, senza caricamento pesi o richiesta
   chat; attestare il metodo e i sei conteggi o registrare il blocco.
4. Letture di memoria/swap/processi, stato servizi, spazio disponibile, metadata/
   symlink/proprietario/permessi del lock storico e tracce di tentativi preesistenti;
   nessuna creazione, acquisizione/modifica del lock o modifica dei servizi.
5. Raccogliere localmente il dossier diagnostico e confrontarlo con manifest e
   hash congelati. Nessuna installazione, trasferimento di modelli o esecuzione
   del worker generativo implicita nel preflight.

Se modelli o supporto mancano, STOP; download/caricamenti/lock esecutivo e sei
POST richiedono le successive autorizzazioni appropriate. Nessun altro audit
RAG, selezione o benchmark diventa prerequisito. Driver preparato **IMPLEMENTATO**;
controlli **ESEGUITO** e **VALIDATO** soltanto nel perimetro statico/manifest;
esecuzione non autorizzata e prerequisiti non attestati **BLOCCATO**, pilot
**DA FARE**. RAG, API/panel, corpus, indici e risultati storici preservati.
**Generazioni effettuate 0; POST generative 0; SSH 0.** STOP dopo pubblicazione.


## Addendum — preflight remoto diagnostico, esito BLOCCATO

Data: 2026-11-11. Attività invariata
`RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`. Baseline iniziale locale/GitHub
`7eb32bb403c8d5a7f8b32123e681779e5bbbe499`, branch corretto, tree pulito.
TODO/registro/report e i due sorgenti del driver confrontati con GitHub;
commit tecnico `3449db8f1d1c68d07fb76b5ff753b6676270bfef` riconciliato.
I 32 controlli statici non sono stati ripetuti. Nessuna modifica al driver,
al package pending, al protocollo o al RAG per aggirare un gate.

### Attività → Script → Commit → Report → Risultato → Decisione → Stato

Script diagnostico separato:
`operations/quality-first-pilot/remote_preflight_diagnostic_01.py`.
Autorizzato solo questo preflight read-only/non generativo, non il worker.
Script e corpo stdin controllati soltanto per sintassi prima dell'accesso;
nessuna importazione/esecuzione del worker. Commit di pubblicazione: quello
che introduce questo script, inventario e addendum con TODO/registro contestuali,
identificabile dalla storia Git e restituito nella consegna.

Evidenze riproducibili in
[`quality-first-pilot-remote-preflight-01/inventory.json`](quality-first-pilot-remote-preflight-01/inventory.json):
invocazione, hash del corpo diagnostico/sorgente, stdout JSON con risposte HTTP
anche in byte base64, stderr, exit code e summary. La sessione remota osservata
va da `2026-11-11T20:34:17.801053+00:00` a `20:34:17.874187+00:00` secondo
l'orologio remoto; non si assume sincronizzazione con il PC.

### Accesso e operazioni effettive

SSH alias `football-vps`, configurazione esplicita del profilo giamp, destinazione
163.5.26.155:22, utente football, IdentitiesOnly e sola identità v3 configurata;
BatchMode, StrictHostKeyChecking=yes, UpdateHostKeys=no, host key ED25519
`SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks` confrontata con known_hosts.
Nessuna nuova chiave accettata o privata stampata. Il profilo separato sandbox
non risolveva l'alias: è stato verificato in lettura il profilo già autorizzato,
non creata/modificata una configurazione. Exit SSH 0, stderr vuoto.

Una sola sessione diagnostica: GET `/api/version`, `/api/tags`, `/api/ps` prima
e dopo (quattro GET 200); help di Ollama e show, letture /proc, stato dei due
servizi, spazio disco, metadata lock e percorso noto del pilot. Nessuna POST:
`/api/show` non necessario per tag assenti. Nessun endpoint tokenize ipotetico
provato, nessuna scansione ricorsiva di sorgenti/binari, compilazione, ABI,
nuovo server o strumento scaricato. Le directory d'installazione note sono
state enumerate solo al primo livello per identificare interfacce esistenti.

### Matrice capacità documentate / osservate / mancanti

| Proprietà | Evidenza osservata | Cosa dimostra e limite |
|---|---|---|
| Ollama | GET version 0.40.5, CLI `/usr/local/bin/ollama` | Versione dichiarata osservata; commit/build completa e capacità dei candidati non attestati dal solo numero |
| Gemma26 / Qwen27 | Tag `gemma4:26b` e `qwen3.8:27b` assenti in /api/tags | Modelli selezionati non disponibili come tag del servizio; nessun digest completo/template/thinking dei candidati osservabile. Non è una ricerca di eventuali blob orfani su tutto il disco |
| Baseline conservata | Presenti qwen3.5:9b Q4_K_M con digest 56671c2a…3c90, qwen3-embedding:0.6b e nomic-embed-text | Identità e quantizzazioni nel raw; nessun modello modificato, cancellato o sostituito |
| Modelli caricati | /api/ps restituisce models=[] prima e dopo | Nessun modello residente osservato nei due istanti, nessun caricamento effettuato |
| Rendering/tokenizer pre-POST | Help Ollama/show senza comando di conteggio; llama-tokenize/llama-cli/llama-server/ollama-tokenize non risolti sul PATH | Nessuna interfaccia supportata che produca i sei conteggi esatti è stata attestata; non è prova di impossibilità assoluta della build |
| Componenti installati | `/usr/local/lib/ollama/llama-server` presente come file fuori PATH | Non equivale a un endpoint tokenizzazione disponibile nel servizio attivo. Non è stato avviato un server né eseguito quel binario o fatto loading per esplorarne capacità |
| RAM visibile | MemTotal 16720678912 byte = 15,572 GiB; MemAvailable circa 14,711 GiB | Diverge dai 24 GB dichiarati. È la memoria esposta al sistema osservato, non un'attestazione del piano commerciale o dell'host fisico |
| Disco visibile | Disk usage dei due percorsi: totale 61285326848 byte = 57,076 GiB, libero 41388630016 byte | Non conferma i 480 GB dichiarati; è la vista filesystem di /home/football e /opt, non inventario completo dei dispositivi |
| Swap | Occupati 257712128 byte; contatori cumulativi pswpin 27006, pswpout 164826 | Esiste uso storico/occupazione; un solo campione dei contatori non dimostra paging attivo durante la sessione |
| Servizi | football-rag-api.service utente e ollama.service entrambi active | Stato osservato, nessun riavvio o modifica; non collaudo di convivenza sotto carico |
| Lock | Regolare, uid 1000, 0600, percorso senza symlink, nessun record corrispondente osservato in /proc/locks; metadata prima/dopo uguali | Nessuna acquisizione. L'assenza di record non certifica futura acquisibilità, che qui era vietato provare |
| Tentativi e concorrenza | Ledger canonico locale assente; percorso speculare noto remoto assente; nessun processo pilot noto osservato | Nessun tentativo in questi riferimenti; non prova globale su percorsi sconosciuti o richieste future |

Le capacità nominali di Gemma thinking e Qwen xhigh restano **documentate** nelle
fonti del protocollo, ma **non osservate** per questi modelli sulla VPS: sono
assenti i tag necessari per interrogare i rispettivi metadata. Il dossier
pending non è stato trasformato in verified=true e nessun numero token è stato
inserito. Nessuna estrapolazione da byte o dal Qwen9 storico.

### Decisione e arresto

**Preflight BLOCCATO.** Mancano due prerequisiti concreti:

1. I due modelli selezionati non sono installati come tag utilizzabili del
   servizio. Download/installazione non autorizzati e non eseguiti.
2. **Conteggio esatto pre-POST non disponibile come capacità attestata nel
   perimetro consentito.** Non è stato identificato un ingresso supportato che
   renda e tokenizzi i messaggi dei due artefatti senza generazione/caricamento.
   `/api/show` da solo non fornirebbe tale conteggio; un eseguibile server
   presente non basta. Questo è un prerequisito non verificabile con le
   interfacce osservate, non una dimostrazione che ogni possibile componente
   interno della build sia incapace di tokenizzare. Nessun percorso alternativo
   viene aperto per trasformare l'assenza di evidenza in un PASS.

Si aggiunge la divergenza delle risorse rispetto alla baseline dichiarata,
che impedisce di assumere sostenibilità sui 24 GB. Non si deduce la RAM dei
modelli dal peso del file né si dichiara impossibilità universale di eseguirli.
La sessione si arresta senza ulteriori ricerche, infrastrutture, installazioni,
reverse engineering o esperimenti. Nessuna proposta automatica alternativa.

Diagnostica **ESEGUITO**, prerequisiti preflight **BLOCCATO**, pilot **DA FARE**:
nessuna delle sei generazioni autorizzata. Quattro GET, zero POST generative,
zero POST show, zero caricamenti, zero acquisizioni lock, zero worker.
Nessuna modifica a modelli, servizi, RAG, API/panel, staging o configurazioni.
Protocollo/driver e risultati precedenti preservati; target 28/30 e Gate restano
**BLOCCATO**. Pubblicazione delle sole evidenze locali, TODO/registro e verifica
GitHub/working tree, poi STOP.


## Addendum — autorizzazione operativa, download completati, arresto ai gate

Data: 2026-11-11. Attività invariata `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`.
La successiva autorizzazione esplicita dell'utente comprende download dei due
modelli e massimo sei generazioni, subordinate ai gate del protocollo. L'utente
ha inoltre confermato **163.5.26.155** come destinazione effettiva: 6 vCPU,
15,572 GiB RAM esposta, disco virtuale 60 GiB. La discrepanza con l'hardware
inizialmente dichiarato non lascia più ambiguo il bersaglio. Le precedenti
frasi «generazioni/download non autorizzati» descrivono la sessione storica,
non il consenso attuale. Non occorre chiedere nuovamente la stessa autorizzazione.

### Attività → Script → Commit → Report → Risultato → Decisione → Stato

Baseline pubblicata riconciliata `ab467b3d581ab1852a87eb688cf6943a28569ad5`;
branch invariato. Script separato `operations/quality-first-pilot/authorized_model_downloads_01.py`,
congelato prima dell'esecuzione nel commit tecnico **b358976a8aea1c2a43c71b86011abaea0efa44c8**.
Nuova differenza tecnica: installazione dei due artefatti già selezionati,
prima assenti e ora autorizzati, con verifica dei digest completi; nessuna nuova
selezione, campagna o ripetizione dei 32 controlli statici. Prima dell'esecuzione
sono state controllate la sintassi del nuovo script/corpo stdin, le identità dei
manifest pubblici e le risorse per conservare i download. Il solo `--help` del
llama-server già presente è stato letto, senza avvio server, modello o converter.
Non è stato adottato il vecchio percorso ABI.

Evidenze e inventario: `docs/quality-first-pilot-authorized-readiness-01/`.
I manifest ufficiali congelati provengono da
`https://registry.ollama.ai/v2/library/gemma4/manifests/26b` e
`https://registry.ollama.ai/v2/library/qwen3.8/manifests/27b`;
sono fonti mutabili, qui identificate anche dagli hash locali, non dal solo tag.
Raw JSONL dei download, metadata show, risorse prima/dopo, stderr ed exit code
sono conservati senza riscrittura. Il commit di pubblicazione documentale è
quello che introduce questo addendum, summary e inventario con TODO/registro;
il suo identificativo viene restituito nella consegna e risolto dalla storia Git.

| Artefatto | Dimensione registrata, byte | Digest manifest completo | Esito |
|---|---:|---|---|
| gemma4:26b | 18731025629 | 001e5dafc3c77684c2307ebc6ab8e336e10c9b18eca52acf547d72fc83c3ca8c | Q4_K_M, download **VALIDATO** |
| qwen3.8:27b | 17741872154 | aaee06c39dcf2437cde036998d960e1fc1494b8191be7cc9657d01e509097813 | Q4_K_M, download **VALIDATO** |

SSH con configurazione/host key autorizzate e verifica rigorosa; nessuna nuova
chiave accettata. Due richieste `/api/pull` sequenziali, nessun retry applicativo;
GET diagnostiche e due POST `/api/show` non generative. Exit SSH 0, stderr vuoto.
Il servizio ha completato/verificato i download; i digest restituiti da tags
corrispondono agli esatti manifest congelati. Questo non è un hash indipendente
in lettura integrale di tutti i blob remoti. Originali Qwen9/embedding ancora
elencati, nessuna cancellazione o sostituzione richiesta. `/api/ps` vuoto prima
e dopo; nessun caricamento effettuato dal driver. Disco libero finale
4915421184 byte; MemAvailable finale 15867867136 byte. La riserva operativa
locale di 4 miliardi di byte su disco/memoria ha protetto il download: non
costituisce validazione del fabbisogno RAM dei modelli. Il peso dei file non
è stato usato come stima della RAM. Nessuna misura di qualità o convivenza
sotto carico è stata prodotta.

### Gate ancora aperti e decisione

1. Nessuna interfaccia supportata osservata fornisce il conteggio esatto
   pre-POST dei sei messaggi renderizzati con tokenizer/template effettivi.
   Metadata `/api/show`, template `{{ .Prompt }}` e help non lo dimostrano.
   Non sono stati inventati conteggi, rapporti byte/token o endpoint tokenizzazione;
   non è stata dichiarata impossibilità assoluta della build.
2. Gemma dichiara thinking `false/true`, default true. Qwen dichiara
   `false/low/medium/xhigh`, default medium. Il mapping del `think=true`
   congelato nel driver verso il profilo Qwen xhigh previsto non è attestato.
   I metadata non sono una prova di applicazione effettiva del profilo.

**Decisione: esecuzione BLOCCATO ai gate tecnici, pilot DA FARE.** Download
**ESEGUITO/VALIDATO** nel perimetro sopra descritto. L'autorizzazione dell'utente
resta acquisita; non risolve automaticamente i prerequisiti e non autorizza
ad alterare il protocollo o dichiarare verifiche mai effettuate. Nessun binding
verified=true o conteggio sintetico, nessuna riscrittura del driver congelato.
Un'eventuale decisione successiva deve affrontare precisamente questi gate,
non riaprire selezione modelli, ABI o riconciliazione RAG già completate.

**POST generative 0; generazioni 0; worker eseguiti 0; lock acquisiti 0.**
Nessuna modifica applicativa/RAG/retrieval/corpus/API/panel, servizi,
configurazioni, staging o wrapper. Unico cambiamento remoto autorizzato:
i due modelli aggiunti tramite pull. Nessuna compilazione, inferenza, merge,
deploy o infrastruttura aggiuntiva. Target 28/30 e proprietà generative non
sono dimostrati; risultati RAG storici preservati. STOP dopo pubblicazione.


## Revisione operativa 02 — token osservati e profili nativi espliciti

2026-11-11, stessa attività RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01.
Baseline GitHub/local 89b9d1d5292d644bcfc2bda44fe707ae3be0fb3a, branch corretto,
tree pulito prima del delta, ledger canonico assente. Il titolare ha accettato
la proposta mirata successiva ai blocchi con «oooohhhh e daiiii» e chiesto di
terminare il controllo. Restano autorizzati massimo sei invii, nessun retry,
nessuna variazione RAG o infrastrutturale. Non è una nuova campagna.

Differenza tecnica registrata prima della prova: Qwen usa think="xhigh"
esplicito (ammesso dai metadata installati), Gemma mantiene think=true.
Il precedente gate di conteggio esatto preventivo è sostituito da una prova
operativa limitata: API ufficiale con num_ctx8192/num_predict4096 invariati,
conservazione di tutti i messaggi/fonti, contatori del servizio osservati dopo
la risposta. Prompt_eval_count deve essere positivo e <=4096; eval_count
positivo <=4096, done_reason stop e finale non vuoto. In caso contrario STOP
senza nuovo invio. Questo controllo NON prova l'assenza di troncamento silenzioso
né l'equivalenza del tokenizer: il pilot non può certificare queste proprietà,
né una graduatoria definitiva. Non vengono inventati token preventivi.

Il binding revised registra falsi exact_prepost_tokens_verified e
runtime_profile_application_verified; non si compilano i vecchi booleani come
se fossero PASS. Identità/tag/digest/quantizzazione/template sono osservati;
applicazione effettiva di tutti i parametri, no-context-shift e profili non
sono attestati indipendentemente. Le verifiche dei controlli esecutivi sono
operazioni runtime, non prerequisiti già dichiarati superati. Restano invariati
input, parametri restanti, seed42, ordine sei slot, lock non bloccante,
memoria libera>=4GB, nessun nuovo paging, timeout900s/5400s, cattura append-only,
ledger fsync-before-GO e STOP su qualsiasi errore/ambiguità. Nessun warmup o
seconda POST per rimediare al primo fallimento. Rilevare un'insufficienza di
RAM non autorizza un upgrade, quantizzazione diversa o downgrade del profilo.
Chiudere il socket non dimostra cancellazione nel servizio: STOP totale.

Script: operations/quality-first-pilot/paired_pilot_01.py e worker omonimo
remote. Manifest aggiornato esplicitamente prima degli output, originale
conservato nella storia Git. Piano revised SHA256
56c89eefef60bd8f42f915015832e6dc3a3e75968f8d1ee61f4a8928b4dfaf72.
Binding/consenso e otto controlli nuovi del solo delta in
quality-first-pilot-authorized-readiness-01/*_02.json e
revision_02_delta_checks.json; 8 PASS statici, nessuna suite storica ripetuta.
Il driver ora usa esplicitamente la configurazione SSH autorizzata e preserva
anche un evento finished non valido prima dello STOP. Nessun codice applicativo
modificato. Commit tecnico: quello che introduce questa revisione, congelato
prima dell'invocazione e registrato nel ledger. Stato preparazione IMPLEMENTATO,
controlli ESEGUITO/VALIDATO solo staticamente. Pilot DA FARE fino all'invio.
Il risultato effettivo segue in un addendum nella medesima sessione.


## Esito esecutivo revisione02 — un invio, arresto al monitor swap

2026-11-11. Attività invariata RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01.
Commit tecnico congelato e pubblicato prima dell'invocazione: 078b8f16b8c41e02af3efe1dce6b5ef6a00f11dc.
Metodo: execute del driver versionato con execution_binding_02.json e
execution_authorization_02.json. Riconciliazione89b9d1d/GitHub, ledger assente
prima dell'avvio; creazione esclusiva del ledger canonico, nessun reset o
seconda esecuzione. Otto controlli del solo delta pubblicati nel commit tecnico,
non nuova esecuzione di suite storiche. Gli avvisi diff whitespace erano CRLF
nel JSON raw, non spazi nuovi nei sorgenti; controllo cr-at-eol nel closeout.

### Risultato osservato

Primo slot: Gemma4 26B, caso V10-02. Il worker ha verificato utente, supervisor
GNU timeout e process group, lock esistente e acquisizione non bloccante,
Ollama0.40.5, digest/Q4_K_M, nessun modello caricato, servizi active, memoria
iniziale15859093504 byte. Ledger fsync salvato prima del GO; un solo evento
post_started e invocazione POST /api/chat, nessuna seconda chiamata.

Dopo circa1,034 secondi il monitor rileva pswpin da27127 a27129; pswpout rimane
164839. È scattato E_RESOURCE_OR_DEADLINE per la regola già congelata di zero
nuovo paging. MemAvailable al campione15744802816 byte, ben sopra4GB; nessun
timeout900s e nessuna soglia di memoria superata osservata. È un incremento
di due pagine del contatore globale: non prova thrashing, memoria insufficiente
del modello né attribuzione causale certa al caricamento. Il processo
llama-server compare nel campione con RSS133599232 byte; nessuna inferenza
sulla futura occupazione dei pesi viene ricavata da questo dato.

Il monitor chiude il socket; segue RemoteDisconnected senza risposta HTTP,
stream o testo finale. Il controller conserva raw stdout/stderr, prenotazione
e STOP.json, interrompe l'intero pilot e non invia gli altri cinque slot.
**POST avviate1; risposte ricevute0; generazioni completate osservate0.**
Ricezione/completamento effettivi nel servizio non attestati: non si dichiara
che la generazione reale sia certamente zero. Nessun tentativo alternativo.

Una sola diagnostica successiva read-only GET version/ps e letture processi,
memoria, servizi e metadata lock: /api/ps vuoto, nessun llama-server/runner
osservato, solo daemon Ollama; football-rag-api e Ollama entrambi active.
Contatore swap-in27129, swap-out164839. Questo documenta lo stato quieto
successivo; non dimostra l'istante esatto di cancellazione. Nessun processo
ucciso manualmente, riavvio, unload POST o modifica di servizi/configurazioni.

### Evidenze, decisione e stato

Raw originali e manifest inventariati in
`evaluation/quality_first_paired_pilot_01/`: activity-created, request/invocation,
reserved-before-GO, stdout.raw/stderr.raw, STOP, diagnostica post-stop,
summary e inventory SHA256/dimensioni. Non sovrascrivere o riaprire questo
ledger. Non esiste complete.json, export cieco o scheda valutata perché
mancano sei risposte. Binding e controlli in docs/readiness preservati.

Pilot **ESEGUITO** come tentativo interrotto; completamento/confronto **BLOCCATO**.
Nessun vincitore, voto, fallimento tattico o insufficienza hardware dimostrati.
Non è un test di qualità del modello: il monitor ha fermato il tentativo
prima di una risposta. Il prossimo passo raccomandato, NON eseguito, è una
sola decisione sul criterio di paging: distinguere attività globale minima
osservata da pressione persistente, prima di autorizzare un nuovo tentativo
con delta dichiarato. Non abbassare la soglia RAM né riprovare questo ledger;
nessun nuovo acquisto, selezione, ABI o campagna suggeriti come conseguenza.

RAG, corpus, embedding, retrieval, panel, API, configurazioni, staging e modelli
installati preservati; nessuna modifica applicativa. Target28/30 non valutabile,
nessuna promozione, merge o deploy. Commit di pubblicazione closeout è quello
che introduce queste evidenze e l'aggiornamento contestuale TODO/registro,
restituito nella consegna. STOP dopo verifica GitHub/working tree.
