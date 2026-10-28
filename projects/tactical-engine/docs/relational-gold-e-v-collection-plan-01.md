# Piano di raccolta indipendente Gold E / Gold V

Data: 2026-10-28  
Attività: `RD-RELATIONAL-GOLD-E-V-COLLECTION-PLANNING-01`  
Ramo: `codex/tactical-state-contract-v1`  
HEAD iniziale riconciliato: `7fbda2f992673b9c0f3b6bd17e3777df55e00e21`  
Perimetro: pianificazione e ricognizione, senza raccolta, annotazione, freeze,
inferenza o benchmark.

Revisione indipendente ChatGPT sul commit `cbece0f`: **APPROVABILE CON
CORREZIONI**. La presente revisione recepisce C1–C6 senza modificare
numerosità, quote di provenienza o perimetro operativo.

## 1. Stato e risorse già disponibili

La preparazione metodologica `RD-RELATIONAL-GOLD-E-V-PREPARATION-01` è
`VALIDATO offline`. Sono già disponibili e non vengono duplicati:

- protocollo `docs/relational-gold-e-v-protocol-v1.md`;
- schemi `relational_gold_e_v1` e `relational_gold_v_v1`;
- template Gold E/Gold V vuoti e manifest di freeze draft in
  `evaluation/annotations/`;
- validatore statico e cinque test della sola preparazione;
- precedenti metodologici per worksheet atomico, manifest SHA-256, holdout e
  claim-evidence;
- registro degli esperimenti e TODO come fonti autorevoli degli stati.

Il planner/audit dispone di casi di regressione, ma non di un gold
indipendente. I controesempi delle sette remediation, i test unitari, Drive11
e Coverciano V10 restano esclusi dall'independent set. Non sono stati trovati
altri piani di raccolta equivalenti già completati.

Le attività `RD-RAG-DOCUMENTARY-GAP-AUDIT-01` e
`RD-SUPERVISED-AUTO-LEARNING-DESIGN-01` sono registrate come `DA FARE`: questo
piano ne documenta soltanto le dipendenze e non le implementa.

## 2. Dimensione proposta

### 2.1 Pilot procedurale: 12 domande

Prima del gold principale si propone un pilot di **12 domande** per verificare
chiarezza delle istruzioni, tempi, accordo fra revisori e adeguatezza degli
strumenti. Il pilot non viene usato per misurare il sistema e, dopo eventuali
correzioni alla procedura, entra permanentemente nel regression/process set.
Non può essere promosso retroattivamente a gold indipendente.

### 2.2 Gold E principale: 60 domande

Si propone un minimo di **60 domande**, sei per ciascuna famiglia:

1. costruzione e uscita dalla pressione;
2. possesso organizzato contro blocco medio/basso;
3. rifinitura, ampiezza, profondità e attacco dell'area;
4. pressing, blocco e fase di non possesso;
5. difesa dell'area, cross e seconde palle;
6. transizione positiva;
7. transizione negativa e riaggressione;
8. palle inattive e riprese di gioco;
9. gestione gara e cambio di sistema;
10. compiti individuali, rotazioni e relazioni fra reparti.

La selezione usa la seguente matrice di copertura. Le celle sono controlli di
presenza/assenza e concentrazione, non obblighi da attribuire a una domanda che
non li esprime.

| Famiglia | Sottotemi da monitorare | Dimensioni relazionali da censire | Target |
|---|---|---|---:|
| Costruzione/pressione | prima costruzione, uomo libero, uscita laterale/centrale, pressione alta | attore, compito, spazio, trigger, finalità | 6 |
| Possesso/blocco | blocco medio/basso, superiorità, ampiezza/profondità, circolazione | attore, compito, fase, spazio, finalità | 6 |
| Rifinitura/area | half-space, cross, tagli, occupazione area, seconde palle offensive | attore, compito, spazio, trigger | 6 |
| Non possesso | pressing, schermatura, scivolamenti, altezza del blocco | attore, compito, fase, trigger, ambito | 6 |
| Difesa area | cross, duelli, coperture, secondo palo, seconde palle difensive | attore, compito, spazio, finalità, polarità | 6 |
| Transizione positiva | prima giocata, sostegno, attacco profondità, consolidamento | attore, compito, fase, trigger, finalità | 6 |
| Transizione negativa | riaggressione, protezione profondità, preventive, ripiegamento | attore, compito, fase, trigger, spazio | 6 |
| Palle inattive | organizzazione offensiva/difensiva, ribattute, ripresa rapida | attore, compito, trigger, spazio, ambito | 6 |
| Gestione gara | punteggio/tempo, cambi, inferiorità, cambio sistema | attore, compito, fase, trigger, polarità | 6 |
| Ruoli/rotazioni | scambi, sotto-ruoli, catene, relazioni fra reparti | attore, compito, fase, spazio, finalità | 6 |

Per ogni riga il registro segnala sottotemi assenti, presenti e
sovrarappresentati. Un'assenza non autorizza a inventare una domanda: si cerca
un nuovo candidato indipendente oppure si conserva e dichiara il limite.

Per ogni famiglia il target è:

- due domande semplici a singola richiesta;
- due domande multi-parte o multi-fase;
- due scenari aperti/ambigui con più soluzioni tattiche ammissibili;
- almeno due richieste esplicite e due aperte;
- presenza bilanciata, sull'intero set, di attore, compito, fase, trigger,
  spazio, finalità, polarità e ambito propria/avversaria.

Le dimensioni sono quote di selezione, non etichette forzate. Se una domanda
non esprime una dimensione, il gold non la inventa.

Sessanta casi non danno una certificazione universale, ma consentono un primo
benchmark indipendente con sei osservazioni per famiglia e revisione umana
sostenibile. Risultati per sottogruppi con denominatori piccoli saranno
descrittivi, non conclusivi.

### 2.3 Gold V principale: 60 risposte naturali

Dopo il freeze Gold E e una distinta decisione del titolare, si acquisisce una
sola risposta RAG per ciascuna delle 60 domande, con runtime e input congelati.
Il primo Gold V contiene quindi **60 risposte naturali**. Non vengono create
risposte artificiali per bilanciare TP/FP/TN/FN.

La distribuzione delle etichette viene pubblicata. Se una classe relazionale è
troppo rara per una stima utile, il limite viene dichiarato; un eventuale
challenge set separato richiederà una nuova decisione, fonti indipendenti e
metriche separate dal prevalence set naturale.

Le analisi restano distinte:

1. **per risposta/domanda**, dove ogni caso pesa una volta e comprende anche
   esito tecnico della generazione;
2. **per requisito relazionale**, dove una risposta può contribuire più
   osservazioni.

I requisiti della stessa risposta non sono indipendenti. Le metriche micro per
requisito sono quindi accompagnate da risultati macro per risposta e, quando
si stimano intervalli, da ricampionamento o aggregazione con cluster sul
`case_id`, non trattando ogni requisito come domanda autonoma.

Timeout, errore di generazione e risposta vuota restano nel denominatore
complessivo per risposta come fallimenti tecnici distinti. Non vengono
trasformati in falsi giudizi relazionali: il denominatore per-requisito indica
se il contenuto era valutabile e il report pubblica entrambi i conteggi. Non si
garantisce a priori numerosità sufficiente per TP/FP/TN/FN o singola famiglia.

## 3. Fonti proposte per Gold E

Le domande non vengono generate da Codex, Qwen o dall'audit. La quota proposta
per i 60 casi principali è:

| Canale | Casi | Condizioni |
|---|---:|---|
| Domande originali prospettiche di allenatori/docenti indipendenti | 24 | Minimo quattro autori, massimo sei domande per autore; nessuna visione del sistema o dei suoi errori |
| Domande reali de-identificate da corsi, club o percorsi per match analyst | 18 | Permesso d'uso documentato, data/origine verificabili, mai usate nel progetto |
| Scenari formulati da match analyst indipendenti a partire da situazioni reali documentabili | 18 | Autore umano, riferimento alla situazione, nessun output del motore, nessuna derivazione dai casi di remediation |

I limiti si applicano trasversalmente ai tre canali: massimo sei casi per
autore, massimo dodici per organizzazione e massimo sei per un'unica origine
comune (`origin_cluster_id`, ad esempio corso, archivio o evento). Un'eccezione
richiede motivazione e decisione del titolare prima di G1; non può essere
introdotta dopo aver osservato prestazioni. Ogni record conserva autore,
organizzazione e origine comune anche quando il testo è de-identificato.

Autori e organizzazioni dichiarano ogni coinvolgimento precedente nello
sviluppo, nella remediation o nella valutazione di FOOTBALL-DATA-LAB. Chi
conosce i failure mode dell'audit non contribuisce al gold indipendente.

Materiale pubblico federale o attribuito a Coverciano può essere incluso solo
se autenticità, diritto d'uso, testo originale e provenienza sono verificati.
Non si presenta una domanda come ufficiale per la sola somiglianza stilistica.

Il pilot usa canali analoghi ma autori/casi distinti dal set principale. Le
quote possono essere corrette prima della raccolta soltanto con decisione
documentata; non dopo aver visto le prestazioni dell'audit.

## 4. Inclusione, esclusione e indipendenza

### Inclusione

- domanda tattica comprensibile senza informazioni personali;
- testo originale conservabile e provenienza verificabile;
- consenso o licenza compatibile con uso di valutazione;
- scenario sufficientemente definito oppure ambiguità intenzionale annotabile;
- nessun utilizzo precedente nello sviluppo di FOOTBALL-DATA-LAB;
- categoria e complessità utili alle quote congelate.

### Esclusione

- duplicato o parafrasi sostanziale di casi di sviluppo;
- domanda generata o corretta dal sistema valutato;
- contenuto con provenienza o diritti non verificabili;
- caso che espone dati personali non necessari;
- quesito puramente regolamentare, medico o atletico fuori dal perimetro
  tattico;
- domanda scritta conoscendo l'output o l'errore dell'audit;
- Drive11, Coverciano V10 e controesempi delle sette remediation.

### Screening

1. registro candidati con `source_id`, autore/canale, data, trasformazioni e
   dichiarazione di uso precedente;
2. hash e confronto testuale esatto con regression set e candidati;
3. confronto lessicale normalizzato;
4. revisione umana cieca delle coppie semanticamente sospette;
5. decisione `unique`, `possible_duplicate`, `duplicate` o esclusione, con
   riferimenti agli ID correlati;
6. freeze della lista di inclusione prima dell'annotazione e prima di
   qualsiasi esecuzione dell'audit.

Un `possible_duplicate` non entra nel gold fino all'adjudication. Il controllo
semantico non usa le decisioni del verificatore da valutare.

### Esclusioni tardive e sostituzioni

Un caso divenuto inutilizzabile conserva ID, provenienza, momento e motivazione
dell'esclusione. Prima del freeze può essere sostituito soltanto da un
candidato della stessa quota, sottoposto integralmente a screening e controllo
d'indipendenza; il change log collega escluso e sostituto.

Dopo G3 nessuna sostituzione è silenziosa. Una modifica alla selezione produce
una nuova versione del manifest. Dopo il freeze Gold E, la sostituzione
richiede nuova annotazione A/B/C e nuovo freeze; la versione precedente resta
immutabile. Nessuna esclusione o sostituzione può dipendere dalla prestazione
del sistema, dal risultato dell'audit o dalla comodità di migliorare le
metriche.

## 5. Ruoli e competenze

### Autori delle domande

Allenatori, docenti o match analyst con esperienza documentata. Non ricevono
prompt, output, failure mode o vocabolari dell'audit. Un autore non può essere
l'unico annotatore o revisore delle proprie domande.
Deve dichiarare anche appartenenza organizzativa, origine comune dei materiali
e qualsiasi precedente coinvolgimento nel progetto; la conoscenza dei failure
mode determina esclusione dal gold indipendente.

### Annotatore A

Competenza tattica documentata: qualifica da allenatore pertinente oppure
esperienza professionale equivalente di almeno cinque anni in
allenamento/match analysis. Completa Gold E senza vedere risposta, planner,
audit o annotazione B.

### Revisore B

Competenza comparabile e indipendenza da A e dall'autore. Produce una seconda
annotazione prima di vedere quella di A. Non si limita ad approvare.

### Adjudicator C

Profilo tattico senior, preferibilmente qualifica superiore o esperienza
documentata nella formazione di allenatori. Risolve i soli disaccordi con
motivazione; non riscrive silenziosamente entrambe le annotazioni.

### Revisore documentale D

Per Gold V verifica provenienza, locator e supporto claim-fonte. Può coincidere
con C soltanto se possiede entrambe le competenze e il conflitto è dichiarato.
Non trasforma la validità dell'ID di citazione in supporto semantico.
Può contestare e motivare il supporto documentale, ma non modifica
autonomamente le annotazioni tattiche di A/B/C: un conflitto torna
all'adjudication e resta tracciato.

Tutti usano ID pseudonimi, dichiarano competenze, rapporti con il progetto e
conflitti d'interesse. Nessuna qualifica viene presentata come approvazione
ufficiale Coverciano senza prova.

### Accordo umano e accettazione del pilot

Prima di G2 si registrano versione e hash delle istruzioni e si scelgono le
misure: accordo percentuale per campi/etichette, Cohen's kappa per categorie
nominali quando applicabile e tasso/tipologia dei disaccordi critici. La
dimensione ridotta del pilot e le classi degeneri vengono dichiarate; nessuna
soglia è presentata come standard universale.

G0 deve fissare soglie operative specifiche del progetto. Il pilot è accettato
soltanto se:

- tutti i 12 casi sono annotati indipendentemente e validi rispetto allo
  schema;
- ogni disaccordo critico su inclusione, atomizzazione, attore-compito,
  fase/trigger o ambito è risolto e motivato da C;
- non restano istruzioni interpretate in modo incompatibile da A e B;
- metriche, casi non valutabili e tempo di annotazione sono documentati;
- A, B e C firmano l'idoneità della versione delle istruzioni.

Se l'accordo non raggiunge la soglia preregistrata o emerge un errore
sistematico, il pilot non passa: si versionano istruzioni e motivazioni, si
usa un nuovo pilot indipendente e il precedente resta nel process/regression
set. Non si modifica il gold principale perché non è ancora iniziato.

## 6. Flusso operativo proposto

### G0 — Decisioni del titolare

Approvare numerosità, canali, gestione dei diritti, ruoli, budget/tempi e
criteri di esclusione; limiti autore/organizzazione/origine; matrice di
copertura; misure e soglie operative del pilot; procedura per sostituzioni;
unità statistiche Gold V; policy privacy, diritti, accessi e conservazione.
Senza G0 non inizia la raccolta.

### G1 — Registro candidati

Acquisire metadati e testi in un'area di staging non dichiarata gold. Non
eseguire Qwen, planner o audit. Applicare screening e quote.

### G2 — Pilot procedurale

Annotare i 12 casi pilota con A/B/C. Correggere soltanto istruzioni, strumenti
o schema se necessario. Calcolare le misure preregistrate, risolvere i
disaccordi critici e applicare i criteri di accettazione. Versionare ogni
modifica con hash e motivazione; ritirare i 12 casi dal gold. Se il pilot non
passa, ripeterlo su nuovi casi senza riutilizzare quelli esaminati.

### G3 — Freeze della selezione principale

Congelare elenco, provenienza, esclusioni, quote e hash delle 60 domande prima
di mostrare qualsiasi output del sistema. Ogni esclusione/sostituzione tardiva
segue il change log e crea una nuova versione del manifest quando necessario.

### G4 — Gold E cieco

A e B annotano indipendentemente domanda, request parts, requisiti, dimensioni
e ambiguità. Registrare accordo pre-adjudication, disaccordi critici e
decisioni C secondo la versione congelata delle istruzioni.

### G5 — Freeze Gold E

Validare schema e completezza, ordinare/canonicalizzare, creare hash per caso e
dataset, firmare manifest e rendere immutabile la versione. Correzioni future
creano una nuova versione; esclusioni e sostituzioni non sovrascrivono il
campione congelato e non possono basarsi sulle prestazioni.

### G6 — Acquisizione risposte

Solo dopo autorizzazione successiva: fissare commit, modello, parametri,
corpus/index fingerprint e input; generare una risposta per domanda senza
mostrare Gold E alla generazione. Conservare output originale, timeout,
errori e risposte vuote senza rimuoverli dal denominatore complessivo.

### G7 — Gold V cieco

A/B valutano per requisito le relazioni contro Gold E congelato. Separano
completezza, coerenza relazionale, correttezza tattica e supporto documentale.
D verifica claim-fonte. C adjudica. Un sospetto errore Gold E sospende il caso
e apre una revisione versionata, senza modifica locale. L'accordo è riportato
sia per risposta sia per requisito; i requisiti restano raggruppati per
`case_id`. D non modifica le etichette tattiche senza adjudication.

### G8 — Freeze Gold V

Validare riferimenti al manifest Gold E, provenienza risposta/evidenze,
annotazioni, disaccordi e hash. Congelare una nuova versione immutabile.

### G9 — Benchmark

Resta una fase separata e `BLOCCATO` fino a entrambi i freeze. Richiede una
decisione esplicita e non è parte di questo piano.

## 7. Dati necessari per l'audit documentale futuro

Per distinguere errore di risposta e lacuna delle fonti, G6/G7 dovranno
conservare, senza implementarli ora:

- commit e fingerprint di modello, runtime, corpus e indice;
- domanda e hash Gold E;
- query di retrieval e candidati considerati;
- chunk selezionati, source ID, locator, score e testo effettivamente fornito;
- inventario delle fonti disponibili al momento dell'esecuzione;
- claim atomici, citazioni dichiarate e giudizio umano di supporto;
- classificazione diagnostica separata:
  `document_absent`, `document_present_not_retrieved`,
  `retrieved_evidence_insufficient`, `conflicting_sources`,
  `context_dependent`, `generation_error`, `not_determinable`.

La classificazione non viene dedotta dalla sola risposta. Un documento non
recuperato non è automaticamente assente; una fonte recuperata non è
automaticamente sufficiente. `RD-RAG-DOCUMENTARY-GAP-AUDIT-01` dovrà
riconciliare inventario, originali, estrazioni, chunk, indici, provenienza e
diritti prima di dichiarare una lacuna. Rimane `DA FARE`.

## 8. Separazione dall'auto-learning

Gold E e Gold V congelati sono read-only e servono alla valutazione. Non
alimentano automaticamente prompt, regole, corpus, retrieval o pesi Qwen.

Un errore osservato nel gold può generare, dopo decisione umana, una
**correzione candidata** in un development set separato. Da quel momento il
caso interessato è contaminato per lo sviluppo e deve essere marcato
`retired_from_independent` nelle valutazioni future; la versione storica e il
suo risultato restano immutabili e auditabili.

Il futuro ciclo supervisionato dovrà applicare:

`Osservazione → diagnosi → correzione candidata → doppia review → approvazione
→ sviluppo separato → validazione su nuovo holdout → promozione controllata →
rollback disponibile`.

Nessuna correzione modifica automaticamente il corpus o i pesi. Fine-tuning e
aggiornamento della conoscenza RAG sono processi distinti. L'attività
`RD-SUPERVISED-AUTO-LEARNING-DESIGN-01` resta `DA FARE`.

### Policy preliminare privacy, diritti e accessi

- Testi originali, metadati identificativi e annotazioni hanno accessi
  separati per ruolo; A/B vedono solo quanto necessario e gli ID pubblicabili
  restano pseudonimi.
- I materiali sono classificati `redistribuibile`, `uso_riservato` o
  `metadati_soltanto`. GitHub riceve testo di terzi solo con diritto esplicito
  di redistribuzione; altrimenti conserva esclusivamente artefatti consentiti,
  hash e riferimenti non sensibili.
- G0 stabilisce base/permesso d'uso, durata di conservazione, responsabile,
  procedura di revoca/cancellazione e obblighi che impongano conservazione.
  Una revoca non altera silenziosamente un freeze: genera esclusione motivata
  e nuova versione, eliminando i dati quando consentito e dovuto.
- Un registro licenze collega fonte, titolare, usi consentiti, pubblicabilità,
  scadenza e restrizioni. De-identificazione e trasformazioni restano
  auditabili senza pubblicare identità non necessarie.
- Gold E, Gold V e staging sono esclusi da retrieval, training, feedback,
  ingestione e aggiornamenti automatici mediante configurazione e controllo
  d'accesso. Nessun connettore li indicizza implicitamente.
- Non si introduce ora alcun nuovo servizio o archivio: collocazione, accessi
  e retention operativi sono una decisione G0 precedente a G1.

### Compatibilità con gli schemi v1 approvati

La revisione documentale rileva due incompatibilità da risolvere con una
decisione versionata, non con campi informali:

1. `relational_gold_e_schema_v1.json` non dispone di campi distinti per
   autore, organizzazione, `origin_cluster_id`, classificazione di
   redistribuzione, licenza, retention e revoca; `additionalProperties: false`
   impedisce di aggiungerli ai casi v1 senza evolvere lo schema.
2. `relational_gold_v_schema_v1.json` richiede `answer` non vuoto e non espone
   uno stato di generazione; timeout, errori e output vuoti non possono quindi
   essere rappresentati correttamente come record Gold V v1.

Gli schemi non vengono modificati in questa fase. Prima di G1 il titolare deve
decidere una revisione compatibile e versionata dei metadati di provenienza;
prima di G6 deve approvare la rappresentazione versionata degli esiti tecnici.
Le versioni v1 e i relativi hash restano immutati e verificabili. Nessun dato
viene raccolto in campi provvisori o archivi paralleli per aggirare il problema.

## 9. Rischi e misure preventive

| Rischio | Misura |
|---|---|
| Contaminazione da casi già visti | Registro provenienza, screening contro regression set, lista congelata prima dell'audit |
| Dominio, autore o organizzazione dominante | Quote per famiglia, massimo 6/autore, 12/organizzazione e 6/origine comune salvo decisione pre-G1 |
| Domande costruite per favorire/far fallire il motore | Autori ciechi ai failure mode e selezione pre-audit |
| Un'unica scuola tattica trattata come verità | Domande aperte, alternative ammissibili, annotatori diversi e ambiguità esplicite |
| Leakage Gold E verso Qwen | Freeze separato e generazione senza requisiti/annotazioni gold |
| Gold V che riscrive Gold E | Riferimento hash immutabile; sospensione e nuova versione |
| Confusione relazione/correttezza/fonti | Quattro giudizi separati e revisore documentale |
| Selezione post-hoc delle classi | Prevalence set naturale; nessun backfill sintetico |
| Scarso accordo umano | Misure e soglie operative preregistrate, pilot escluso, versionamento istruzioni, nuovo pilot se necessario |
| Uso del gold per tuning | Read-only; retirement del caso e nuovo holdout per ogni sviluppo |
| Esclusione tardiva o sostituzione opportunistica | Change log, screening del sostituto, nuovo manifest e divieto di decisioni performance-based |
| Diritti o privacy | Accessi per ruolo, registro licenze, classificazione pubblicabile/riservato, retention e revoca definite a G0 |
| Dipendenza fra requisiti della stessa risposta | Analisi per risposta e requisito separate, aggregazione/ricampionamento per `case_id` |
| Timeout/errori rimossi dai risultati | Conservazione dei fallimenti e denominatori complessivo/valutabile entrambi espliciti |
| Denominatori insufficienti | Nessuna numerosità garantita; pubblicazione per classe/categoria e limiti, senza certificazione impropria |

## 10. Decisioni richieste al titolare

Prima di G1 occorre decidere esplicitamente:

1. approvare pilot 12 + gold principale 60;
2. approvare le tre quote di provenienza 24/18/18 oppure modificarle prima di
   vedere dati o risultati;
3. approvare matrice di copertura e limiti massimi 6/autore,
   12/organizzazione e 6/origine comune, incluse regole per eccezioni;
4. autorizzare il contatto/acquisizione e approvare policy preliminare su
   consenso/licenza, accessi, pubblicabilità, privacy, retention,
   revoca/cancellazione e registro diritti;
5. acquisire dichiarazioni sul precedente coinvolgimento di autori e
   organizzazioni, escludendo chi conosce i failure mode;
6. nominare o approvare A, B, C e D con competenze, responsabilità e conflitti
   documentati;
7. preregistrare misure e soglie operative di accordo, criteri di accettazione
   del pilot e procedura di nuovo pilot/versionamento istruzioni;
8. approvare tempo/budget della doppia annotazione e adjudication;
9. stabilire se materiale federale/pubblico possa essere usato e con quali
   prove di autenticità e diritti;
10. approvare procedura di esclusione tardiva, sostituzione, nuova versione del
    manifest e retirement dei casi usati successivamente nello sviluppo;
11. approvare analisi Gold V per risposta e requisito, dipendenza per
    `case_id` e trattamento di timeout/errori/risposte vuote;
12. confermare isolamento Gold E/Gold V da retrieval, training, feedback e
    aggiornamenti automatici;
13. decidere l'evoluzione versionata degli schemi per metadati C1/C6 prima di
    G1 e per timeout/errori/risposte vuote C5 prima di G6;
14. solo dopo freeze Gold E, decidere separatamente sulle 60 inferenze G6;
15. solo dopo freeze Gold V, decidere se avviare il benchmark G9.

## 11. Risultato e stato

Il piano operativo è documentato e riconciliato con protocollo, schemi e
attività collegate. Non sono stati raccolti o annotati casi; i template restano
vuoti e nessun test o modello è stato eseguito.

Decisione: registrare la pianificazione come **ESEGUITO**. Mantenere:

- raccolta, pilot, annotazione e freeze: **DA FARE**;
- G0, inclusa approvazione delle rettifiche C1–C6: **DA FARE**;
- G1–G5: **DA FARE** e non autorizzati;
- G6–G8: **DA FARE** e subordinati a decisione successiva;
- `RD-RELATIONAL-GOLD-E-V-01`: **BLOCCATO**;
- `RD-RAG-DOCUMENTARY-GAP-AUDIT-01`: **DA FARE**;
- `RD-SUPERVISED-AUTO-LEARNING-DESIGN-01`: **DA FARE**;
- Gold E/Gold V e audit: non **VALIDATO**, **INTEGRATO** o **CERTIFICATO**.

La fase successiva non parte senza le decisioni del paragrafo 10. G9 resta
**BLOCCATO** fino ai freeze e alla decisione esplicita del titolare.
