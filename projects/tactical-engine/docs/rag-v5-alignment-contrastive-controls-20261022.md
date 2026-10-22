# RAG V5 — benchmark contrastivo di pertinenza e scope (2026-10-22)

## Documentazione ufficiale verificata

- Ollama API Chat: https://docs.ollama.com/api/chat — `format` JSON Schema, `stream`, `think`, `options`.
- Ollama Structured Outputs: https://docs.ollama.com/capabilities/structured-outputs — passare JSON Schema in `format`, validare l'output, temperatura bassa per ripetibilità.
- Pydantic Models: https://docs.pydantic.dev/latest/concepts/models/ — validazione di tipi, vincoli e struttura, **non** verifica semantica della correttezza delle etichette.

## Obiettivo e stato

Separare supporto testuale NLI, pertinenza alla domanda e fedeltà allo scope della fonte. Le 13/13 coppie `supported` di Q4/Q5 non dimostrano la pertinenza della risposta. Il precedente report diagnostico identifica Q5 come criticità, con 4 claim `contextual` e 2 `off_target` (etichette provvisorie).

## Nuovo esperimento

`scripts/build_rag_v5_alignment_controls_v1.py` costruisce 10 controlli contrastivi dal report già acquisito `evaluation/reports/rag_v5_shadow_nli_q4_q5_results_v2.json`. Il risultato è `evaluation/reports/rag_v5_alignment_controls_v1.json`.

- Quattro controlli NLI positivi (`supported`).
- Un controllo NLI di generalizzazione indebita (`insufficient`, non necessariamente `contradicted`).
- Cinque controlli di pertinenza: uno `direct`, due `contextual`, due `off_target`.
- Le evidenze sono copiate dal report NLI esistente; nessuna nuova ricerca documentale o inferenza.
- File scritto in modalità esclusiva `x`, senza sovrascrivere risultati precedenti.

## Validazione e limiti

Le etichette sono **ipotesi di revisione**, non gold validato. Il benchmark è diagnostico e non rappresentativo dell'intero RAG V5. Prima di usare un giudice automatico per misurare accuratezza, occorre un'adjudication indipendente dei controlli, con criteri di errore espliciti e separati per NLI e pertinenza. Non confrontare direttamente `supported` e `direct`: rispondono a compiti differenti.

Nessuna modifica a Chroma, embedding, reranking, prompt RAG, baseline o pipeline di produzione è autorizzata da questo esperimento. Il builder è stato caricato su GitHub; l'esecuzione sulla VPS resta da verificare.
