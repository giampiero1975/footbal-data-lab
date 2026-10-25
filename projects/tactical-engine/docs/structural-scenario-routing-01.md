# Routing strutturale per scenari tattici complessi

Data: 2026-10-25. Stato: **VALIDATO e INTEGRATO** nel solo profilo API.

## Attività

Correggere risposte applicative che recuperavano fonti lessicalmente vicine ma
incompatibili con sistema di partenza, ruoli e geometria richiesta. Il profilo
locked e il relativo perimetro certificato restano invariati.

## Evidenza iniziale

Tre risposte reali della sequenza Coverciano hanno mostrato:

- principi corretti ma generici e una citazione `F10` con sole sei evidenze;
- trasformazione 4-3-3→3-5-2/3-4-2-1 incoerente, con un inesistente
  “centrocampista esterno” nel sistema di partenza;
- inversione tra compiti offensivi e difensivi e mancata identificazione del
  dilemma creato ai braccetti.

Il catalogo conteneva già estratti pertinenti su 4-3-3 contro 3-5-2, catene
terzino–mezzala–ala e inserimento del terzino nello spazio creato dall'ala.

## Correzione

- estrazione generica di moduli, ruoli e principi dalla domanda;
- riserva massima di tre fonti strutturali distinte sui sei estratti API;
- riconoscimento dell'intento di corsa sincronizzata/profondità;
- guida generativa `ruolo iniziale → movimento → spazio → dilemma`;
- condizioni già dichiarate trattate come vincoli, senza riaprire alternative;
- divieto di trasferire istruzioni difensive alla squadra in possesso;
- wrapper API fail-closed per citazioni assenti o fuori intervallo.

## Risultati

- suite offline combinate: 33/33 e successiva suite mirata 19/19;
- retrieval-only v3: fonti sul 3-5-2, dilemma quinto/braccetto e combinazioni
  ala–terzino del 4-3-3; collection 6410 invariata;
- generazione v1: 106,69 s, citazioni valide, nucleo migliorato ma scelta del
  braccetto riaperta impropriamente; valutazione interna 6/10;
- generazione v2 dopo vincolo fixed-choice: 96,43 s, arresto `stop`, citazioni
  F1/F3/F4/F5/F6 tutte valide, corsa diagonale del terzino nello spazio alle
  spalle del braccetto esplicitata; valutazione interna 8,5/10;
- nessuna modifica all'indice e nessuna estensione della certificazione locked.

## Decisione

Integrare il routing nel profilo API e non ripetere questa domanda senza una
nuova differenza tecnica. Il risultato è una validazione circoscritta, non prova
su tutte le trasformazioni tattiche. Una futura verifica deve usare scenari
strutturali diversi e indipendenti.

## Verifica indipendente 3-4-2-1 contro 4-2-4 — 2026-10-25

Una domanda nuova ha chiesto come difendere l'ampiezza di un 4-2-4 senza
abbassare entrambi gli esterni e senza lasciare i centrali in parita contro due
punte. Il job API `e890ef205ae342868a610ef819b3020a` e terminato in 189
secondi con stato applicativo `succeeded`, indice invariato e citazioni F1-F4
formalmente valide.

La qualita tattica non e validata: la risposta chiama “terzino” un componente
della linea a tre, dichiara di evitare il 5-4-1 ma propone una “difesa a 5”,
mantiene alto l'esterno debole invece di farlo stringere e reintroduce il
“libero”. Due evidenze su quattro riguardano triangoli e sovrapposizioni in
possesso e sono estranee al quesito.

Il revisore esterno Google AI Mode, nella conversazione fornita dal titolare,
ha rilevato le stesse criticita e ha proposto braccetto di parte in uscita,
scivolamento centrale, esterno debole dentro e mediano opposto a schermo. Il
voto conversazionale 27/30 e un segnale non calibrato: la stessa revisione
descrive errori strutturali incompatibili con un risultato quasi pieno.

**Decisione:** stato `ESEGUITO`, non `VALIDATO`. Prima di una nuova generazione
serve una differenza tecnica documentata: separazione possesso/non possesso nel
pool dei candidati, riserva per scivolamento della linea a tre e lato debole,
piu telemetria del routing nel report. Il giudizio esterno resta shadow e non
estende la certificazione locked.
