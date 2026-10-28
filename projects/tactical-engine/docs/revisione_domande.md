# revisione_domande — Diagnosi delle risposte RAG all'esame
Data: 2026-10-28. Attività: V5-REVISIONE-DOMANDE-01.
Stato raccolta e confronto documentale: ESEGUITO. Diagnosi causale e miglioramento: DA FARE.
Obiettivo richiesto: media autonoma almeno 26/30 alla prima risposta; distinguere dal successivo obiettivo >=28/30 già presente nel TODO.

## Problema e comportamento riferito
Il titolare segnala risposte iniziali poco precise o articolate, generalmente 21–22/30, seguite talvolta da 29–30/30 dopo rettifica/domanda mirata. Conferma che la domanda mirata chiarisce cosa sviluppare. Non sa se cambino le fonti o se la rettifica fornisca concetti mancanti.
Il salto 29–30 è un'osservazione del titolare, non ancora documentato da una coppia completa comparabile. Non attribuirlo automaticamente alla capacità autonoma di Qwen.

## Evidenze ricevute nella conversazione
Due trascrizioni domanda → risposta → disamina Gemini Cloud. Mancano job ID, timestamp di esecuzione, commit runtime, modello/parametri effettivi, prompt e testo F1–F6. Non è verificato se siano precedenti o successive a V10.2. I voti sono del valutatore conversazionale esterno, non della commissione ufficiale FIGC.

### RD-001 — 3-5-2 contro 4-2-3-1: 19/30
Scenario: possesso e costruzione dal basso; tre centrali marcati dai tre attaccanti, trequartista sul vertice basso. Richiesti varianti/rotazioni senza lancio lungo e comportamenti di tre centrali/centrocampo dopo perdita nella propria trequarti, inclusi scaglione e posture.
Risposta: usa terzini e ali senza spiegare adattamenti; sovrapposizioni/sovraccarico e terzo uomo non descritti come sequenza concreta; non considera il portiere. Attribuisce alla seconda punta l'abbassamento sul metodista avversario “per impedire il gioco centrale” [F5] durante la descrizione del proprio possesso. Alla perdita concentra i compiti sulle punte: “uno marca, uno copre”, gestione dei terzini e inversione delle punte [F5]. Non sviluppa i compiti richiesti di centrali e centrocampisti.
Rilievi osservabili: perdita dello scenario; possibile trasferimento di principi di non possesso nella costruzione; omissione sostanziale del secondo quesito; citazioni presenti ma fedeltà non verificabile senza estratti.
Disamina Gemini: critica ruoli, mancanza di superiorità in prima costruzione e centralità impropria delle punte nella transizione. Propone rotazione quinto/mezzala, punta che scende e play che sale, portiere aggiuntivo, pressione/coperture e protezione centrale.
Limiti del valutatore: distanza delle punte 60–70 metri non fornita dalla traccia; movimento del terzino avversario in risposta al quinto non automatico; arretrare e accorciare non intercambiabili. La soluzione non è un gold verificato.

### RD-002 — 4-4-2 contro 4-3-3, difesa laterale: 22/30
È una NUOVA domanda: cambia modulo, fase e scenario. Non è una rettifica controllata di RD-001 e non dimostra il salto 19→29–30.
Scenario: blocco medio 4-4-2; ala sinistra avversaria in 1vs1 sul terzino destro, punta tra i centrali, mezzala opposta a rimorchio. Richiesti compiti/posture/copertura dei quattro difensori e aiuto dell'esterno destro e dei due centrali di centrocampo.
Risposta: compattezza generica; terzino destro sull'ala, sinistro sul lato debole; centrali stretti, uno pronto a uscire sul terzino avversario [F4]; introduce trequartista o mezzala [F1]. Esterno destro sul terzino avversario [F3], scambi di marcatura sul fantasista/mezzala [F4]. Termina con “triangolo di collaborazione tra esterno, centrocampista e punta per verticalizzare sul movimento della mezzala avversaria” [F5].
Rilievi osservabili:
- non ricostruisce i quattro compiti rispetto alle minacce già indicate;
- uscita di un centrale sul terzino avversario non motivata dalla situazione;
- non assegna chiaramente controllo del taglio della punta, inserimento della mezzala e protezione del lato debole;
- aiuto all'1vs1 e controllo dello scarico non coordinati;
- frase finale sulla verticalizzazione estranea al compito difensivo;
- numerazione n.1–n.5 aggiunta senza necessità;
- manca una lettura esplicita della pressione sul portatore e della possibilità di giocare in profondità.
Disamina Gemini: penalizza assenza di palla coperta/scoperta, uscite dei centrali e mancanza di raddoppio; propone temporeggiamento, diagonali, protezione profondità/secondo palo e compiti del centrocampo.
Limiti del valutatore da sottoporre alle fonti: l'1vs1 da solo non documenta sempre tempo/libertà effettivi del portatore; “scappare sotto palla” non deve diventare un obbligo identico per tutti, incluso chi temporeggia; raddoppio e chiusura dello scarico vanno coordinati in base alle distanze, senza cancellare il secondo compito richiesto. Numeri non convenzionali possono essere semplici etichette, ma qui non aiutano. Non promuovere l'inserimento di parole chiave a prova di qualità.

## Ipotesi da distinguere
| Ipotesi | Indizio | Evidenza discriminante |
|---|---|---|
| Comprensione/pianificazione incompleta | sottocompiti omessi e ruoli incoerenti | domanda, piano estratto e requisiti attivati |
| Recupero/contesto incompatibile | citazioni associate a comportamenti di altre fasi | pool, selezione, estratti effettivi e ordine nel prompt |
| Generazione che usa male fonti pertinenti | principi concatenati senza geometria | confronto affermazione–estratto a contesto congelato |
| Effetto della rettifica | miglioramento riferito | stessa domanda prima/dopo, suggerimenti introdotti e fonti di entrambi |
| Valutazione conversazionale influenzata | lodi iniziali e prescrizioni assolute | rubrica, contesto del valutatore, giudizio sulla risposta completa |
| Versione runtime diversa dal ramo | correzioni già presenti in sviluppo | commit/hash deploy e configurazione del job |

Queste sono ipotesi, non cause dimostrate. Nessuna evidenza sufficiente per prescrivere fine-tuning o sostituzione di Qwen.

## Riconciliazione GitHub prima di intervenire
Consultati TODO ufficiale, experiment-register, report structural-scenario-routing e report V9/V10 sul ramo codex/rag-coverciano-remediation, head iniziale 9ac95258801c645ac1ce578abaaa164ba46cd097.
- Routing strutturale già VALIDATO/INTEGRATO in ambito API circoscritto; successivo scenario indipendente ha mostrato contaminazione di fase e ruoli incoerenti.
- Baseline RAG-only dieci casi: 19,90/30; non estendere la certificazione locked alle domande aperte.
- V6–V10.2 hanno già affrontato scomposizione, multi-query, fase/ruoli, copertura, contratto applicativo, repair e audit relazionale.
- V9 re-audit e V10.2 set logico 10/10 sono evidenze tecniche sui casi congelati, non media esterna >=26/30.
- Non proporre “aggiungere un parser”, “filtrare la fase” o “aggiungere un repair” come se fossero assenti. Prima localizzare perché il comportamento persiste o se i casi precedono le correzioni.
- Main e ramo remediation differiscono. Questa revisione è documentale sul ramo remediation; nessuna integrazione o distribuzione applicativa.

## TODO operativo
- [x] ESEGUITO — registrare RD-001/RD-002 e separare osservazione da ipotesi.
- [x] ESEGUITO — riconciliare con TODO/registro/report già presenti.
- [ ] DA FARE — associare i casi ai job esistenti e al commit/configurazione runtime.
- [ ] DA FARE — acquisire estratti F1–F6, prompt effettivo, piano/gate e risposta originale dei job, senza rigenerarli.
- [ ] DA FARE — classificare ciascuna affermazione: supportata e pertinente / supportata ma fuori scenario / non supportata / requisito omesso.
- [ ] DA FARE — acquisire una vera coppia stessa domanda → rettifica → seconda risposta → due valutazioni; annotare suggerimenti e differenze di contesto.
- [ ] DA FARE — confrontare il difetto dimostrato con implementazione e deploy correnti prima di prescrivere una patch.
- [ ] DA FARE — concordare rubrica stabile per accuratezza, copertura, coerenza di ruoli/fase, condizioni decisionali, applicabilità e supporto documentale; niente voto alto solo per citazioni o parole chiave.
- [ ] DA FARE — scegliere un solo intervento sulla causa dimostrata, con differenza tecnica documentata e verifica proporzionata; riusare risultati conservati dove sufficienti.

## Tracciamento e decisione
Attività → revisione documentale dei casi forniti.
Script → nessuno nuovo; lettura delle evidenze GitHub e delle trascrizioni in conversazione.
Commit → commit che introduce questo documento e aggiorna TODO/registro insieme.
Report → questo documento.
Risultato → due casi distinti a 19/30 e 22/30; ricorrenza di perdita dello scenario e contaminazione tra fasi; causa tecnica non isolata.
Decisione → raccogliere gli artefatti esistenti e la vera coppia prima/dopo; nessuna nuova inferenza o benchmark equivalente in questa sessione.
Stato → ESEGUITO per raccolta/confronto; DA FARE per diagnosi causale e miglioramento.

## RD-002-R1 — Seguito del caso 22/30, acquisito 2026-10-28
Stato analisi documentale: ESEGUITO. Il titolare ha fornito il seguito: il valutatore suggerisce esplicitamente la regola “palla scoperta: scappare; coperta: accorciare” e propone di rifare il caso con coperta/scoperta e scivolamento. Il testo effettivamente inviato al RAG e la conservazione dello scenario nel suo contesto non sono ancora verificati.

### Risposta RAG ricevuta
1. Definisce palla coperta e scoperta in termini di pressione, tempo e spazio [F1].
2. Le identifica come segnali visivi per organizzare il non possesso [F1,F2].
3. Collega genericamente i segnali ai movimenti collettivi e ai parametri tempo/spazio [F1,F2].
4. Dichiara che le fonti non specificano scivolamento o compiti dei singoli ruoli; non sviluppa quei comportamenti. Aggiunge una digressione su riconquista/possesso in assenza di pressioni estreme.
Non applica esplicitamente scappare/accorciare ai ruoli del caso, non descrive i quattro difensori o l'aiuto dei centrocampisti. Il limite delle fonti è dichiarato, ma non verificabile senza F1/F2.

### Attribuzione del 30/30
Gemini afferma prima che manca ancora l'applicazione al 4-4-2 contro 4-3-3. Poi SCRIVE autonomamente i compiti di terzino, centrali, lato debole, raddoppio e centrocampisti, nonché arresto/risalita della linea. Infine assegna 30/30 motivando che il candidato avrebbe legato i concetti alle reazioni di reparto.
Quell'applicazione è nel testo di Gemini, non nella risposta RAG trascritta. Pertanto il 30/30 è un voto conversazionale non attribuibile come prova autonoma alla risposta RAG. Nessun nuovo voto viene assegnato qui.

### Cosa cambia e cosa non è dimostrato
Il seguito è più focalizzato e meno dispersivo: tratta correttamente a livello definitorio i concetti sollecitati e dichiara limiti. Ma passa da una domanda applicativa a una risposta teorica ristretta; il completamento pratico è esterno.
La prima risposta cita F1–F6 e questa F1/F2: gli ID sono locali alla risposta e non provano né cambio né identità delle fonti.
Possibili cause da distinguere: domanda di follow-up priva dello scenario completo, assenza di memoria conversazionale nel pannello, retrieval ristretto alle definizioni, oppure mancata applicazione generativa a contesto sufficiente. Non dichiarare alcuna causa accertata senza richiesta effettiva e artefatti runtime.

### TODO aggiuntivo
- [x] ESEGUITO — acquisire una sequenza di seguito del caso RD-002 e distinguere contributo RAG/contributo Gemini.
- [ ] DA FARE — recuperare testo esatto inviato al pannello e verificare se scenario, risposta precedente e rettifica raggiungono il modello.
- [ ] DA FARE — confrontare estratti reali dei due turni; non confrontare soltanto etichette F.
- [ ] DA FARE — valutare la risposta RAG immutata prima di mostrare al valutatore soluzioni o riscritture; distinguere qualità teorica e copertura del caso iniziale. Nessuna nuova chiamata viene eseguita in questa revisione.
Decisione: il salto autonomo 22→30 non è dimostrato da questo esempio. Il limite applicativo persiste nel testo osservato. Conservare il caso come evidenza di attribuzione errata del miglioramento e come indizio di restringimento della domanda.

## RD-003 — Attacco 4-3-3 contro blocco basso e preventive; 21→29/30 dichiarati
Acquisito 2026-10-28. Stato analisi: ESEGUITO. Nessuna nuova inferenza.
Scenario: 4-3-3 contro 5-4-1 o 3-5-2 molto basso; nove avversari in meno di 15 metri. Richiesti organizzazione di ali/mezzali/punta per creare rifinitura e compiti specifici dei due centrali e del play sull'unica punta alta.

### Prima risposta, valutata 21/30
Mette “due esterni offensivi” sulla stessa fascia senza spiegare una rotazione; identifica il “quinto” con la mezzala; trasferisce catene e trasformazione in 5-4-1 alla propria squadra. Alle preventive sostituisce un racconto di centrale n.5, terzino n.3, centrocampista n.4 e aggiunta di un “quinto uomo” [F6]. Alla perdita parla di rientro dell'ala e trasformazione in 5-4-1 [F1].
Errori osservabili: identità delle squadre/ruoli non mantenuta; possibile importazione della struttura avversaria; preventive prima della perdita confuse con rientro successivo; compiti dei due centrali e play non assegnati. Fedeltà degli estratti non verificabile.

### Correzione ricevuta
Richiesta mirata riportata: correggere struttura geometrica (ali, mezzali, centrali) e scaglione delle preventive.
La nuova risposta:
- nomina correttamente 4-3-3, ali, mezzali e centrali [F1–F3];
- tratta filosofia dell'allenatore e caratteristiche dei giocatori [F1,F5];
- sotto “fase difensiva” descrive sovrapposizione terzino/ala e angoli di sostegno al portatore [F6], mescolando ancora l'etichetta difensiva a comportamenti in possesso;
- introduce congelamento dell'errore da parte dell'allenatore [F4];
- richiama cross e occupazione dell'area senza una sequenza applicativa [F6];
- conclude con adattabilità del modulo e identità [F1,F5,F6].
NON specifica chi dei centrali marca la punta, chi copre, dove si colloca il play, quali linee protegge o come reagiscono alla perdita. NON sviluppa movimenti coordinati dei cinque offensivi contro il blocco indicato. La frase “se una mezzala si avvicina troppo al portatore, due avversari possono marcare lo stesso giocatore” resta ambigua.
Miglioramento dimostrato: rimozione di alcuni ruoli impropri e maggiore regolarità espositiva. Completezza del quesito non dimostrata; restano contaminazione di fase e digressioni.

### Valutazione Gemini: 29/30
Gemini premia maturità metodologica, identità, sostegni e didattica. Attribuisce alla risposta mezzali nei mezzi spazi, mentre il testo dice genericamente che gestiscono il centro; introduce “terzo uomo” come spiegazione valutativa senza una triangolazione esplicita nel testo. Riconosce l'omissione delle preventive ma la tratta come difetto minimo che la qualità espositiva compenserebbe. Scrive “mezzo punto mancante” pur assegnando 29/30: ulteriore incoerenza interna del commento.
Conclusione: il voto 29/30 non è evidenza affidabile del raggiungimento autonomo del target sulla domanda completa. Nessun voto sostitutivo viene inventato.

### Confronto col seguito RD-002
RD-002-R1: valutatore aggiunge materialmente la soluzione applicativa prima del 30.
RD-003-R1: valutatore amplifica contenuti generici e riduce il peso di un intero sottocompito omesso prima del 29.
Schema ricorrente nei due esempi: richiesta mirata → normalizzazione del lessico/focalizzazione → persistente incompletezza applicativa → voto conversazionale molto alto. I dati non dimostrano ancora il miglioramento autonomo di ragionamento attribuito inizialmente a Qwen.

### Limiti anche della “soluzione ideale”
La revisione Gemini non è un gold: “underlap” indica un movimento interno e non è sinonimo dello spazio “mezzo spazio”; un centravanti non vincola automaticamente tutti e tre i centrali; le prescrizioni sui terzini e sulle preventive vanno motivate dal contesto. Verificare sulle fonti prima di trasformare queste formulazioni in requisiti rigidi del generatore.

### TODO e decisione
- [x] ESEGUITO — registrare prima risposta, correzione e due voti; separare qualità lessicale da aderenza.
- [ ] DA FARE — acquisire richieste effettive e contesto che raggiunge il modello nei due turni, estratti e versione runtime.
- [ ] DA FARE — verificare per affermazione identità squadra, ruolo e fase; confrontare con controlli già implementati V6–V10.2.
- [ ] DA FARE — tracciare separatamente copertura del quesito offensivo e dei compiti centrali/play; citare il passaggio preciso che soddisfa ogni requisito, senza completarlo nella valutazione.
- [ ] DA FARE — stabilizzare rubrica e attribuzione prima di usare medie 26/30 come prova del miglioramento. Non accettare lessico o stile come compensazione automatica per omissioni strutturali.
Attività → analisi documentale RD-003; Script → nessuno nuovo; Commit → aggiornamento simultaneo di questo report/TODO/registro; Report → docs/revisione_domande.md; Risultato → miglioramento lessicale ma preventive omesse, 29/30 non probante; Decisione → recupero artefatti esistenti e diagnosi, nessun rerun; Stato → ESEGUITO, diagnosi tecnica DA FARE.

### Integrazione di RD-002-R1
Il titolare conferma che la domanda inviata era quella mirata riportata, non una trascrizione abbreviata inventata dall'analista. Resta da verificare se il pannello aggiunga automaticamente lo scenario precedente. Ulteriore contestazione “30?? ma è meritato?”: Gemini conferma il voto invocando lessico accademico e limiti delle fonti, senza colmare omissioni nella risposta RAG. Richiama inoltre il 19/30 di RD-001 invece del 22/30 di RD-002, mescolando i casi. Il giudizio confermativo non costituisce una rivalutazione indipendente.
