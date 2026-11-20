# Qwen27 su LIGA — Deposito modello isolato

## Attività, script e commit

Nell’attività `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`, il 20 novembre 2026 è stato autorizzato l’accesso in sola lettura limitato a Qwen27. Baseline GitHub `ec5c194167b1ec60a10aeb14a897abdc6be703a5`. La verifica differenziale è motivata dal [diniego di accesso con UID 997](rag-v5-qwen27-manifest-reconciliation-01.md). Il confronto precedente non aveva predisposto accessi. Script `qwen27_isolated_store_01.py`, commit locale `67fa53293b27756ad38dc7bc002e59e63427f359`. Compilazione in memoria del sorgente remoto riuscita.

## Risultato

- Il preflight ha confermato che sorgente e destinazione sono sullo stesso filesystem e che il GID 987 appartiene al solo account dedicato. `setfacl` è assente. È stato scelto un deposito dedicato, senza interventi sui permessi dello store di produzione.
- Creata `/var/lib/football-qwen27-isolation/models-qwen27`, proprietà `root:987` e modo `0750`. Al suo interno, cinque hard link riusano gli inode dei blob verificati per dimensione. Il solo manifest storico è stato materializzato dal blob di catalogo dopo la verifica del suo SHA-256. Il piano futuro deve indicare questo percorso come `model_store`. Il validatore d’isolamento può conservare il digest storico e la protezione `ReadOnlyPaths`.
- Sotto UID 997 sono state verificate lettura e assenza di scrittura sul manifest e sui cinque blob, nonché l’assenza di accesso al deposito originale. I blob dei pesi non sono stati aperti. Ollama e RAG risultano attivi con gli stessi PID e ID di invocazione prima e dopo. Nessun riavvio, caricamento, download, POST o inferenza. [Evidenza](qwen27-isolation-model-access-01/isolated-store.json).

## Decisione e stato

Predisposizione **IMPLEMENTATO**, accesso al deposito dedicato **VALIDATO**. Il Gate Linux richiede ancora la propria evidenza sintetica. La prova Qwen27 mmap **BLOCCATO** fino al superamento del Gate e all’autorizzazione della generazione.
