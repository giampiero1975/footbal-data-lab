# RAG Coverciano — diagnosi e remediation autonoma

Data avvio: 2026-10-26  
Ramo: `codex/rag-coverciano-remediation`  
Stato: V6 e V7 **ESEGUITE, NON VALIDATE**; V8 **IMPLEMENTATA e VALIDATA offline**, runtime **DA FARE**

## Obiettivo vincolante

Portare il RAG senza spalla ad almeno 26/30 medio sui dieci casi congelati.
26/30 e la soglia minima, non l'obiettivo massimo. OpenRouter resta disabilitato
durante diagnosi, sviluppo e misurazione della bozza RAG.

## Dataset congelato

I dieci job sono stati recuperati dalla cronologia autenticata del pannello e
riesposti integralmente: domanda, bozza RAG, fonti/pagine, tempo e token. Le
valutazioni Gemini gia acquisite restano l'oracolo storico; nessuna nuova
chiamata Gemini e necessaria durante lo sviluppo.

Baseline: 199/300, media 19,90/30, mediana 21,50/30. Caso 9: 0/30 per
retrieval generico e astensione completa.

## Metodo

Per ogni caso classificare separatamente:

1. copertura del corpus;
2. indicizzazione e metadata;
3. analisi strutturale della domanda;
4. dense retrieval e candidati;
5. reranking e riserve;
6. composizione del contesto;
7. prompt e politica grounded;
8. modello, budget e arresto;
9. copertura dei sottopunti;
10. coerenza di fase, ruoli, lati, geometria e terminologia.

Ogni rerun richiede una differenza tecnica documentata. Il confronto usa la
stessa domanda e verifica esplicitamente la risoluzione dei rilievi Gemini,
validita delle citazioni, assenza di invenzioni, integrita dell'indice, tempi e
token. Nessuna ottimizzazione viene promossa se migliora il voto occultando un
errore documentale.

## Cause iniziali gia dimostrate dalla baseline

- retrieval contaminato dalla fase opposta nei casi 2, 4, 5, 7 e 8;
- recupero insufficiente e generico nel caso 9;
- nessun gate sulla copertura completa della traccia;
- risposta definitoria o coreografica invece che applicativa;
- politica grounded che trasforma una lacuna di retrieval in astensione totale;
- termini e geometrie non normalizzati;
- profilo generativo non ancora dimostrato per scenari multi-vincolo.

## Diagnosi per caso e correzione associata

| Caso | Causa primaria | Evidenza baseline | Correzione tecnica |
|---:|---|---|---|
| 1 | copertura incompleta | preventive, zona, avversario e palla coperta/scoperta omessi | facet transizione/preventiva/fuorigioco, checklist e audit |
| 2 | contaminazione di fase | la costruzione diventa marcatura difensiva; portiere e terzo uomo assenti | penalità fase opposta e retrieval separato portiere/terzo uomo |
| 3 | terminologia e coordinazione | “libero”, contatto e portiere incompleti | contratto applicativo e copertura esplicita portiere/area |
| 4 | geometria non tradotta in compiti | cinque corridoi e preventiva non mappati; struttura residua errata | piano possesso/blocco/preventiva e schema chi-dove-copertura |
| 5 | prospettiva/fase invertita | esterno lato debole omesso e reparto contraddittorio | query non possesso/ampiezza e penalità opposizione di fase |
| 6 | retrieval/generazione generici | preventiva e finestra 5/6 secondi assenti | query dedicate transizione/preventiva e gate di copertura |
| 7 | tassonomia spaziale confusa | rifinitura assimilata all'half-space; codici vaghi | facet zona interna/terzo uomo e richiesta di innesco/geometria |
| 8 | coreografia senza criteri | zone area e segnali del cross mancanti | retrieval separato ampiezza/area e audit di entrambi i facet |
| 9 | fallimento retrieval | due pagine generiche e astensione completa | query specifica fuorigioco/palla coperta-scoperta/comandi; applicazione prudente dei principi |
| 10 | risposta astratta | movimenti, comunicazione e impatto emotivo omessi | facet sostituzioni/comunicazione/psicologia/preventiva |

La causa sistemica dominante è l'accoppiata **singola query globale + gate
soltanto sintattico**. Il modello riceveva evidenze semanticamente vicine ma non
necessariamente sufficienti per tutti i vincoli, poi poteva terminare con
citazioni valide anche lasciando fuori parti decisive.

## Implementazione isolata

- nuovo `v5_tactical_query_plan_v1.py`, privo di ID benchmark e di scritture;
- estrazione deterministica di fasi, ruoli, moduli e richieste;
- una query originale più query bounded per facet (massimo cinque);
- penalità alle evidenze esclusivamente della fase opposta;
- riserva di fonti distinte per coprire più facet prima della composizione;
- contratto generativo `CHI/COSA/DOVE/QUANDO-PERCHE/COPERTURA`;
- distinzione tra principio documentato e applicazione allo scenario;
- audit JSON `tactical_answer_audit`, con facet e dimensioni operative mancanti;
- attivazione di default soltanto nel wrapper applicativo; runner locked e
  `--legacy-profile` restano invariati.

## Verifica offline

- planner e dieci temi congelati: **6/6**;
- router strutturale preesistente: **5/5**;
- API: **19/19**;
- catalogo: **7/7**;
- totale suite interessata: **37/37**; compilazione Python e `git diff --check`
  superati.

Questa evidenza valida l'implementazione, non il voto tattico. Il rerun dei dieci
casi è ora giustificato dalla differenza tecnica, ma resta da svolgere sul
runtime con indice invariato, spalla disabilitata e confronto contro i rilievi
Gemini già congelati.

## Esito V6 e remediation V7

Il rerun V6 ha completato 10/10 casi con indice 6.410 invariato e zero
citazioni sintatticamente invalide, ma quattro audit incompleti, due output
troncati e più errori semantici residui. Il report completo e
`docs/rag-coverciano-remediation-v6-runtime-01.md`.

La V7 corregge il difetto sistemico emerso: il controllo non e pi soltanto
descrittivo. Introduce scenari tattici generici, query specifiche prioritarie,
requisiti relazionali (per esempio palla scoperta -> scappata), controllo dei
dettagli per scenario e una sola rigenerazione correttiva fail-closed in caso
di omissione o troncamento. Questa modifica richiede test offline e un nuovo
runtime differenziale prima di qualsiasi validazione.

Il runtime V7 ha completato 10/10 casi ma non ha chiuso il problema: repair
6/10, due troncamenti, tre sole risposte realmente complete e un falso positivo
grave nel caso 9. Dettagli in
`docs/rag-coverciano-remediation-v7-runtime-01.md`. La prossima differenza
tecnica necessaria e un audit relazionale fail-closed, non un altro rerun
equivalente.

## Remediation V8

La V8 implementa la differenza tecnica richiesta: audit delle associazioni
tattiche e delle contaminazioni di fase, selezione deterministica fra prima
risposta e repair, conservazione del candidato migliore, telemetria esplicita e
rifiuto fail-closed nel wrapper quando il risultato resta incompleto. La suite
planner/API/catalogo passa 43/43. Il nuovo ciclo usa contesto 8.192 per impedire
che prompt ed evidenze consumino lo spazio destinato all'output.

## Criterio di chiusura

Il lavoro non si chiude con un singolo miglioramento. Servono: diagnosi causale
per 10/10 casi, modifiche e test offline, rerun differenziali tracciati, media
prevista e poi osservata almeno 26/30, nessun errore strutturale grave e report
completo. Fonti mancanti devono essere identificate e integrate o registrate
con un piano concreto; non costituiscono motivo per interrompere l'analisi.
