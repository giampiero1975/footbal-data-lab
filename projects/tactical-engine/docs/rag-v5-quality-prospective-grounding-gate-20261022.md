# RAG V5 — Gate prospettico per fedeltà semantica (2026-10-22)

## Decisione
**Non riutilizzare holdout_06 e holdout_10 come holdout indipendente.** Sono stati analizzati ripetutamente, dunque sono casi di regressione *development* (06 REVIEW; 10 FAIL). Il test prospettico deve avere nuove domande, nuove evidenze e criteri fissati prima di eseguire il modello. Non attribuire alcun punteggio a risposte non generate.

## Inventario già disponibile
- `eval/claim_fidelity_fresh_sources_holdout_v1.json`: casi claim↔evidence con tre etichette (supported, contradicted, insufficient) e fonti The FA. **È un dataset per il giudice di fedeltà, non un holdout di risposte complete RAG**; non sostituisce il target 9/10.
- `docs/rag-v5-quality-9of10-validation-protocol-v1.md`: gate per risposte complete, cinque dimensioni 0–2 e vincoli PASS.
- `docs/rag-v5-quality-holdout-adjudication-rubric-20261022.md`: revisione atomica, controllo fase/causalità/quantificatori e separazione judge/RAG.
- `docs/rag-v5-phase-passage-atomic-adjudication-20261022.md`: errori noti da mantenere nella regressione, **non** nel nuovo holdout.

## Requisiti vincolanti del nuovo set
- Minimo 10 domande nuove, mai impiegate per tuning; generazione singola dopo congelamento di domande, fonti, criteri e hash.
- Copertura predefinita: transizione positiva/negativa; confine transizione/possesso; recupero alto/medio/basso; confronto di principi; blocco basso; cambio modulo *durante* la gara; multisorgente; quantificatori; fonte di esercitazione vs prescrizione di gara; astensione.
- Per ogni domanda: scenario, fonti e pagine ammissibili, claim obbligatori e vietati, condizioni d'astensione, revisore, SHA256 del manifest.
- Separare errori di retrieval (estratto incongruo) da errori di generazione (inferenza indebita su estratto pertinente).
- Valutare 5 dimensioni: pertinenza, fedeltà, completezza, coerenza tattica, tracciabilità. PASS se totale >=9, pertinenza/fedeltà/coerenza =2, nessuna allucinazione grave. Gate >=9 PASS/10; un pilota di 10 non dimostra robustezza statistica.
- Registrare latenza, modello, prompt, opzioni, collection, versione codice e hash dei report; conservare baseline V4.
- Nessuna modifica di Chroma, prompt di produzione o motore V5 finché non è fissato il gold.

## Check prima dell'esecuzione
- [x] Protocolli e rubriche esistenti identificati.
- [x] Set NLI fresco identificato e distinto da holdout end-to-end.
- [x] Casi 06/10 esclusi dal futuro gold indipendente.
- [ ] Selezionare e verificare documenti sorgente/pagine per 10 domande realmente nuove.
- [ ] Congelare manifest JSON con criteri atomici, SHA256 e revisione indipendente.
- [ ] Consultare le API ufficiali Ollama/Chroma pertinenti alle versioni runtime effettive.
- [ ] Eseguire il RAG read-only su VPS e revisionare gli output in cieco.
- [ ] Confrontare con baseline V4 su condizioni controllate.

**Stato**: protocollo pronto, dataset end-to-end non ancora congelato né eseguito. Nessuna pretesa di 9/10.
