# RAG V5 — Rubrica di valutazione qualitativa holdout (22 ottobre 2026)

## Ambito e vincoli
Input: `rag_v5_quality_holdout_pilot_results_v1.json` (10 domande, risposta, evidenze F1–F8). Questo è un **holdout pilota già esaminato**: non usarlo per ottimizzare prompt e poi dichiarare un risultato indipendente. Conservare il JSON originale. Nessuna modifica al motore RAG V5.

## Unità di valutazione
Per ogni domanda annotare (a) copertura della richiesta, (b) singole affermazioni atomiche, (c) corrispondenza tra ogni affermazione e **testo effettivo** delle fonti citate, (d) eventuali inferenze non documentate. Non confondere una citazione formalmente valida con una prova sufficiente.

## Rubrica per domanda
- **Aderenza**: 2 = risponde direttamente a tutti i vincoli della domanda; 1 = parziale o mescola fenomeni vicini; 0 = tratta un evento/concetto diverso.
- **Fedeltà**: 2 = affermazioni sostanziali sostenute da fonti citate con identico ambito; 1 = almeno una inferenza non esplicitata o supporto parziale; 0 = contraddizione o uso sistematico di fonti incongrue. Segnare `non_verificato` se non sono state lette tutte le coppie claim-fonte.
- **Precisione tattica**: 2 = terminologia, fase di gioco, ruoli, causalità e condizioni corrette; 1 = ambiguità o generalizzazione; 0 = confusione tattica determinante. Distinguere valutazione esperta da evidenza testuale.
- **Citazioni**: `valide` controlla solo l'identificativo; `pertinenti` richiede verifica testuale e per-claim. Non assegnare 2 per la sola assenza di ID invalidi.
- **Esito**: `pass` solo se aderenza=2, fedeltà=2 e precisione=2; `review` se una dimensione=1 o non verificata; `fail` se una dimensione=0. Non calcolare un tasso 9/10 senza adjudication completa.

## Controlli critici di scope
1. **Fase**: transizione positiva (riconquista) non equivale a transizione negativa (perdita); principi statici del modulo non dimostrano effetti del **cambio modulo durante la gara**.
2. **Evento/causalità**: distinguere caratteristiche di una disposizione dai vantaggi o rischi *causati dalla sua modifica*.
3. **Quantificatori**: 'nei tre sistemi' non implica 'in qualsiasi sistema'; distinguere condizioni necessarie da possibilità.
4. **Citazione**: la fonte deve sostenere esattamente la proposizione, non solo contenere parole tattiche correlate.
5. **Assenza di prove**: non inferire che un fenomeno non esiste perché i passaggi recuperati non lo trattano.

## Revisione iniziale: priorità, non voti gold
- holdout_01: confronto marcatura uomo/zona pertinente; controllare la generalizzazione del libero.
- holdout_02: rischio di ridurre il sostegno alla sola sovrapposizione.
- holdout_03: verificare distinzione costruzione corta/lunga e iniziatore dell'azione.
- holdout_04: pertinente; audit atomico ancora necessario.
- holdout_05: distinguere equilibrio preventivo e azione dopo perdita.
- holdout_06: rischio citazione diagonali difensive per zona di riconquista.
- holdout_07: pertinente; audit atomico ancora necessario.
- holdout_08: pertinente; audit atomico ancora necessario.
- holdout_09: verificare generalizzazioni e causalità del cambio modulo.
- holdout_10: distinguere prima giocata dopo recupero e transizione negativa.

## Protocollo di adjudication
1. Congelare il report originale e registrare identificatore/sha256 del file locale nel futuro audit.
2. Scomporre ogni risposta in affermazioni verificabili; riportare gli ID delle fonti citate per ogni affermazione.
3. Assegnare le tre dimensioni con citazioni letterali brevi e motivazione; se ambigua, `non_verificato`, non un voto inventato.
4. Revisione indipendente delle controversie, senza mostrare al revisore i voti preliminari.
5. Calcolare score aggregati solo dopo completamento di tutte le righe; annotare separatamente errori di retrieval e di generation.
6. Per un vero test futuro, creare un nuovo set **mai usato per tuning**, bloccare domande e criteri prima dell'esecuzione.

## Stato
Rubrica definita; non è una certificazione di qualità. I 10 output e le 0 citazioni formalmente invalide non equivalgono a 10 risposte corrette.
