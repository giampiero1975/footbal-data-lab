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
