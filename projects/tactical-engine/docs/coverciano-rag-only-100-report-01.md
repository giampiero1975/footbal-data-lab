# Benchmark Coverciano RAG-only — baseline 10 casi

Data: 2026-10-26  
Stato: **ESEGUITO (10/10), non VALIDATO**

Protocollo originario: `coverciano-rag-only-100-protocol-01.md`. Il titolare ha
ridotto esplicitamente la baseline a dieci casi e richiesto l'arresto esatto al
caso 10. La risposta valutata è sempre la bozza RAG non modificata. Il revisore
OpenRouter è rimasto disabilitato. Gemini Cloud ha formulato le domande e
assegnato voto e giudizio, senza correggere la risposta prima della valutazione.

## Risultato consolidato

| Caso | Tema | Voto | Tempo RAG | Token | Evidenze | Esito sintetico |
|---:|---|---:|---:|---:|---:|---|
| 1 | Transizione negativa: contro-pressing o ripiegamento | 26/30 | 122,40 s | 506 | 3 | Fondamentali corretti; mancavano preventive/densità, zona, avversario e palla coperta/scoperta. |
| 2 | Costruzione dal basso contro pressing uomo su uomo | 18/30 | 161,40 s | 575 | 6 | Inversione possesso/non possesso; portiere e terzo uomo non trattati correttamente. |
| 3 | Difesa della porta su cross laterale | 25/30 | 159,68 s | 642 | 6 | Buona postura e 1vs1; “libero” anacronistico, contatto e coordinazione col portiere incompleti. |
| 4 | Scaglionamento offensivo contro blocco medio-basso | 23/30 | 169,61 s | 577 | 6 | Buoni ampiezza e principi; preventive e geometria 2-3-5/3-2-5 insufficienti. |
| 5 | Sotto-blocco e scivolamento sul cambio gioco | 20/30 | 161,39 s | 560 | 6 | Fasi confuse, comportamento dell'esterno omesso e geometria di reparto contraddittoria. |
| 6 | Contro-pressing uomo/spazio | 22/30 | 172,60 s | 575 | 6 | Visione troppo passiva; “zona luce” impropria, preventive e regola 5/6 secondi mancanti. |
| 7 | Rifinitura e ricezioni tra le linee | 24/30 | 161,14 s | 614 | 6 | Buona base; rifinitura confusa con half-space, smarcamenti e codici collettivi troppo generici. |
| 8 | Costruzione alta contro blocco basso | 21/30 | 164,70 s | 549 | 6 | Sequenze numeriche rigide; assenti geometria del riempimento area e segnali visivi del cross. |
| 9 | Trappola del fuorigioco | 0/30 | 96,85 s | 489 | 2 | Retrieval fallito; risposta astensiva completa e domanda non affrontata. |
| 10 | Sostituzioni e tattica in itinere | 20/30 | 142,40 s | 419 | 6 | Corretta distinzione principi/sistemi, ma applicazione, comunicazione e impatto emotivo astratti. |

- Totale: **199/300**.
- Media: **19,90/30**; mediana: **21,50/30**.
- Minimo/massimo: **0/30** e **26/30**.
- Casi almeno a 26/30: **1/10**; target medio 26/30: **non raggiunto**.
- Tempo RAG totale: **1.512,17 s**; media **151,22 s** (circa 2 min 31 s).
- Token totali: **5.506**; media **550,6** per risposta.
- Errori applicativi: **0/10**; tutti i job sono terminati `succeeded`.
- Costo OpenRouter: **$0**, perché il revisore era disabilitato. Gemini Cloud è
  stato usato dall'interfaccia web e non produce una metrica API attribuibile.

## Diagnosi

1. **Retrieval non allineato ai sottoproblemi.** Nei casi 2 e 5 compaiono
   fonti o concetti della fase opposta. Il caso 9 recupera soltanto due pagine
   generiche sulla gestione della gara e non materiale sulla linea difensiva.
2. **Assenza di copertura obbligatoria della traccia.** Le risposte non
   verificano di avere affrontato ogni richiesta: portiere, terzo uomo,
   preventive, segnali del cross, quattro zone di attacco area, comandi della
   linea e impatto emotivo vengono omessi senza un gate.
3. **Generazione descrittiva invece che applicativa.** Il modello ripete
   definizioni o coreografie numeriche, ma raramente esplicita chi fa cosa,
   dove, quando, con quale innesco e quale copertura transizionale.
4. **Astensione eccessiva.** Quando il retrieval non copre la domanda, il
   prompt porta il RAG a dichiarare l'assenza di fonti invece di fornire una
   risposta tattica autonoma chiaramente separata dalle affermazioni documentali.
   Il caso 9 dimostra che questo comportamento può azzerare il voto.
5. **Terminologia non normalizzata.** Sono riutilizzati termini anacronistici o
   geometricamente imprecisi (`libero`, rifinitura = half-space, `zona luce`)
   senza un controllo semantico finale.
6. **Qualità e infrastruttura sono problemi distinti.** Pannello, coda,
   autenticazione e job hanno funzionato 10/10; la latenza resta elevata, ma il
   mancato target dipende soprattutto da retrieval, copertura e generazione.

## Decisione

La baseline è **ESEGUITA**, ma l'ipotesi “RAG autonomo >=26/30” è respinta e non
può essere marcata VALIDATA. Non proseguire oltre dieci casi e non riattivare la
spalla per mascherare il risultato. Prima di una nuova versione del benchmark:

1. scomporre la domanda in fase, ruoli, spazi, inneschi, rischi e richieste;
2. fare retrieval separato per ciascun sottoproblema e penalizzare fonti della
   fase opposta;
3. introdurre un gate di copertura delle richieste e una struttura applicativa
   `chi-cosa-dove-quando-perché-copertura`;
4. distinguere con chiarezza conoscenza tattica generale e affermazioni
   documentali, evitando sia invenzioni sia astensioni totali;
5. normalizzare terminologia e coerenza geometrica prima dell'output;
6. congelare un piccolo set differenziale tratto dagli errori osservati e
   ripeterlo solo dopo modifiche tecniche documentate.

La spalla resta disabilitata. La pipeline locked certificata, gli indici e i
risultati precedenti non sono stati modificati da questa esecuzione.
