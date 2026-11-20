# Qwen27 mmap — Controllo di ammissione del modello su LIGA

## Attività

Il 20 novembre 2026, nell’attività `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`, è stato autorizzato un Gate Linux sintetico dell’isolamento, subordinato al controllo in sola lettura del modello con l’account dedicato. La baseline GitHub `ec5c194167b1ec60a10aeb14a897abdc6be703a5` attesta la predisposizione dell’account e della directory di stato. Il [Gate precedente](rag-v5-qwen27-ollama-isolation-linux-gate-01.md) si era fermato al preflight quando entrambi mancavano. Il nuovo controllo riguarda il binding del modello e l’accesso con l’UID ora disponibile. Non sono stati ripetuti Gate02 o le fixture Windows.

## Script e commit

`qwen27_isolation_model_access_01.py`, commit tecnico locale `c04b2e6c33de4d47961eb2b776701047634d1b87`, esegue in sola lettura `check_model_access` del codice di isolamento e rileva l’identità dei servizi prima e dopo. Compilazione Python in memoria e `git diff --cached --check` riusciti. Una connessione SSH con chiave host vincolata. [Invocazione e hash dei sorgenti](qwen27-isolation-model-access-01/invocation.json) · [Risultato grezzo](qwen27-isolation-model-access-01/result.json).

## Risultato

- Account `football-qwen27` risolto a UID `997`. La verifica si è arrestata con `E_MODEL_MANIFEST_DIGEST`, codice remoto `41`.
- Il file `manifests/registry.ollama.ai/library/qwen3.8/27b` nello store `/usr/share/ollama/.ollama/models` non corrisponde al digest del binding storico `aaee06c39dcf2437cde036998d960e1fc1494b8191be7cc9657d01e509097813`. Lo script registra il mismatch, senza acquisire l’hash osservato. I controlli blob e i test `test -r` sotto UID 997 vengono dopo il digest e non sono stati raggiunti. I permessi di lettura dei pesi restano quindi indeterminati.
- Ollama e RAG erano `active` prima e dopo, con PID e `InvocationID` invariati. Zero unità transitorie, POST, caricamenti, download o inferenze. Nessuna modifica a configurazione, account o permessi.
- Stop selettivo, namespace, sentinella e persistenza dell’interdizione su Linux restano da verificare. La tenuta dei 4 GB con mmap rimane indeterminata.

## Decisione e stato

Arresto prima del caso sintetico, senza retry. Il digest fissato resta invariato. Per rimuovere il blocco occorre riconciliare il manifest effettivo con quello storico confrontando digest e dimensione di ogni layer. Un’eventuale adozione di un artefatto diverso richiede un nuovo binding esplicito prima di verificare accesso ai pesi e STOP. Controllo di ammissione **ESEGUITO**, Gate sintetico Linux e Qwen27 mmap **BLOCCATO**. Il risultato riguarda questa configurazione VPS e non misura la qualità delle risposte tattiche.
