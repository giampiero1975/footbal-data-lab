# RAG V5 — Protocollo di validazione qualità 9/10, v1

## Scopo
Misurare la qualità **delle risposte complete del RAG V5**, non l'accuratezza dei giudici NLI/alignment. Target operativo: almeno 9 risposte su 10 accettabili in un holdout indipendente, con criteri predefiniti e nessun errore tattico grave. Questo target è una soglia di progetto, non un risultato misurato.

## Dataset e separazione
- **Development/diagnostica**: le cinque domande q1–q5 già utilizzate, gli undici casi NLI adversarial, i dodici contrastive, i dieci controlli alignment. Non sono holdout.
- **Holdout**: minimo 10 domande nuove, fissate prima della generazione e non usate per modificare prompt, retrieval o giudici. Includere domande mono-documento, multisorgente, confronto di principi, scenario specifico, domande con fonti insufficienti.
- Documentare per ogni domanda: query, scenario, fonti autorevoli ammissibili, fatti obbligatori, fatti vietati, limiti, pagine, criterio di accettazione e revisore.

## Rubric per ogni risposta (0–2 per dimensione)
1. **Pertinenza**: 0 non risponde; 1 parziale/contesto; 2 risponde esattamente alla richiesta.
2. **Fedeltà alle fonti**: 0 contraddizioni/invenzioni; 1 almeno un'affermazione non dimostrata o troppo generale; 2 affermazioni sostanziali tutte verificabili.
3. **Completezza**: 0 elementi essenziali mancanti; 1 copertura parziale; 2 tutti gli elementi obbligatori.
4. **Coerenza tattica e scenario**: 0 confonde fasi, sistemi, condizioni o causalità; 1 ambiguità; 2 distingue correttamente.
5. **Tracciabilità**: 0 citazioni assenti/errate; 1 parziali; 2 riferimenti puntuali alle fonti effettivamente usate.

Totale 0–10. **PASS domanda** se totale >=9, pertinenza=2, fedeltà=2, coerenza=2 e nessuna allucinazione tattica grave. Quindi 9/10 significa >=9 domande PASS su 10; non significa una media di 9 punti.

## Procedura
1. Congelare hash/configurazione RAG V5 e input holdout; preservare gli artefatti originali.
2. Eseguire retrieval+generazione read-only una volta per domanda, salvando output, contesto, fonti, latenza, versione modello.
3. Revisione manuale indipendente dei risultati, preferibilmente senza vedere predizioni del giudice.
4. Confrontare punteggi e disaccordi con judge shadow V1/V2 **solo dopo** la revisione.
5. Non effettuare tuning sull'holdout; ogni modifica richiede nuovo holdout e regression suite.
6. Riportare numeratore, denominatore, errori critici, confidenza e limiti. Dieci casi costituiscono un gate pilota, non una prova statistica robusta.

## Controlli di regressione obbligatori
- Fonte limitata a tre sistemi non supporta 'qualsiasi sistema'.
- Rischi di **cambiare modulo durante una partita** distinti dai rischi di un modulo fisso.
- Blocchi bassi: non invertire le indicazioni su ampiezza e verticalizzazione.
- Le linee di passaggio in una singola azione non equivalgono al cambio di sistema.
- Le fonti multisorgente devono riferirsi allo stesso scenario o essere esplicitamente differenziate.
- Astensione quando le fonti non consentono una risposta.

## Stato al 22/10/2026
Protocollo definito, **holdout non ancora costruito né eseguito**. Nessun nuovo risultato 9/10 rivendicato. RAG V5 invariato. Conservare tutti i JSON precedenti.

## Riferimenti tecnici ufficiali per la successiva esecuzione
- Ollama Chat API: https://docs.ollama.com/api/chat
- Ollama Structured Outputs: https://docs.ollama.com/capabilities/structured-outputs
- Chroma documentation: https://docs.trychroma.com/
- Pydantic: https://docs.pydantic.dev/latest/concepts/models/

Verificare versioni e parametri effettivi del runtime prima di lanciare nuovi test.
