# RAG Coverciano — runtime remediation V6

Data: 2026-10-27  
Ramo: `codex/rag-coverciano-remediation`  
Stato: **ESEGUITO (10/10), NON VALIDATO**

## Perimetro

Rerun differenziale delle dieci domande congelate della baseline RAG-only.
OpenRouter e ogni altra spalla sono rimasti disabilitati. Non sono state fatte
nuove chiamate Gemini: il confronto qualitativo usa esclusivamente i rilievi
Gemini originali gia congelati nel report baseline. Collection invariata a
6.410 chunk.

Artefatti runtime: `evaluation/coverciano-remediation-v6/case_01.json` fino a
`case_10.json` e `run.log`.

## Risultato tecnico

| Caso | Tempo | Token output | Arresto | Citazioni invalide | Audit interno |
|---:|---:|---:|---|---:|---|
| 1 | 264,01 s | 486 | stop | 0 | incompleto: palla coperta/scoperta e preventiva |
| 2 | 322,05 s | 468 | stop | 0 | incompleto: fase/causa operativa |
| 3 | 380,73 s | 534 | stop | 0 | incompleto: dettagli area |
| 4 | 564,30 s | 550 | length | 0 | troncato |
| 5 | 369,49 s | 537 | stop | 0 | formalmente completo, non corretto semanticamente |
| 6 | 357,54 s | 408 | stop | 0 | incompleto: densita, palla, preventive |
| 7 | 157,66 s | 490 | stop | 0 | formalmente completo |
| 8 | 166,84 s | 428 | stop | 0 | formalmente completo |
| 9 | 176,02 s | 550 | length | 0 | falso positivo del gate semantico |
| 10 | 180,85 s | 520 | stop | 0 | formalmente completo, troppo astratto |

- Tempo totale: **2.939,49 s**; media **293,95 s**.
- Token output: **4.971**.
- Citazioni sintatticamente invalide: **0**.
- Indice: invariato in tutti i casi.
- Risposte troncate: **2/10**.
- Audit dichiarato incompleto: **4/10**; un quinto caso (9) passa il controllo
  lessicale pur contenendo una decisione tattica errata.

Rispetto alla baseline il tempo medio aumenta da 151,22 a 293,95 secondi
(**+94,4%**). L'aumento deriva da retrieval multi-query e contesto pi ampio,
ma non e compensato da qualita sufficiente.

## Confronto con i rilievi congelati

1. **Transizione negativa:** struttura pi operativa, ma continua a non usare
   palla coperta/scoperta e preventive come criteri decisionali. Gate non
   superato.
2. **Costruzione dal basso:** portiere e terzo uomo finalmente presenti;
   restano una formulazione impropria sull'abbassamento del baricentro e una
   gestione della seconda palla poco concreta. Miglioramento reale, da
   consolidare.
3. **Difesa del cross:** il portiere e presente, ma la risposta conserva ruoli
   numerici rigidi e non definisce contatto, postura semiaperta e punto di
   caduta con precisione. Non migliora il precedente 25/30.
4. **Scaglionamento:** introduce cinque corridoi e struttura 2+3/3+2, ma viene
   troncata. Non valutabile come risposta completa.
5. **Scivolamento:** continua a confondere scivolamento laterale e ripiegamento,
   non usa davvero il tempo di volo come finestra di traslazione e descrive in
   modo contraddittorio il nuovo lato forte. Problema non risolto.
6. **Contro-pressing:** distingue uomo/spazio solo in parte, mantiene concetti
   vaghi sulle zone luce, fa ripiegare subito i difensori e omette la finestra
   5-6 secondi. Problema non risolto.
7. **Rifinitura:** migliore distinzione di ruoli e trasmissioni, ma ricezione
   orientata, attacco della linea, scarico e inserimento non sono coordinati in
   una sequenza chiara. Miglioramento parziale.
8. **Costruzione alta/cross:** copre le quattro zone solo nominalmente; assegna
   il limite area al terzino opposto in modo rigido e non lega i movimenti ai
   segnali del portatore. Miglioramento parziale.
9. **Fuorigioco:** il retrieval non e pi astensivo, ma la risposta propone di
   risalire su palla scoperta e descrive la palla inattiva in modo errato.
   Questo e un errore tattico grave che il gate lessicale non riconosce.
10. **Tattica in itinere:** fonti migliori su cambio sistema e comunicazione,
    ma nessun cambio e descritto davvero ruolo per ruolo; il video viene
    impropriamente proposto come comunicazione durante la gara e l'impatto
    emotivo resta astratto.

## Diagnosi causale aggiornata

La V6 dimostra che retrieval multi-query e checklist sono necessari ma non
sufficienti. Le cause residue sono:

1. il controllo di copertura e eseguito **dopo** la generazione e non provoca
   alcuna correzione;
2. il controllo cerca parole isolate e non verifica relazioni decisionali
   (esempio: `palla scoperta` deve implicare `scappare`, non `salire`);
3. le query per facet sono generiche e non riservano sempre evidenze per il
   dettaglio richiesto;
4. un massimo di 550 token tronca le risposte multi-vincolo;
5. il contratto generativo contiene molte istruzioni generiche ma pochi vincoli
   scenario-specifici;
6. il modello locale 9B tende a riempire i vuoti con formule plausibili ma
   tatticamente scorrette.

## Decisione

La V6 e **ESEGUITA** ma non **VALIDATA**. Non esiste un nuovo voto Gemini e non
va inventato; il target medio 26/30 non e dimostrato e, sulla rubrica congelata,
non e ragionevolmente raggiunto.

La V7 introduce scenari generici (nessun ID benchmark), query prioritarie,
vincoli decisionali, audit relazionale e una sola rigenerazione correttiva
quando mancano requisiti o l'output e troncato. Prima del nuovo runtime devono
passare test offline e un controllo retrieval-only; solo dopo e ammesso un
rerun differenziale.

Il primo controllo retrieval-only sui casi 5, 6, 9 e 10 ha mostrato che la
ricerca semantica continuava a saltare passaggi esistenti nel corpus: manuali su
`tempo di volo`, fonti sulla regola dei cinque/sei secondi e documenti espliciti
su palla coperta/scoperta. La V7 aggiunge quindi un'espansione bounded per frasi
esatte e riserva al massimo tre fonti, sempre sottoposte al reranker e senza
regole legate agli ID del benchmark. Il runtime generativo resta DA FARE.
