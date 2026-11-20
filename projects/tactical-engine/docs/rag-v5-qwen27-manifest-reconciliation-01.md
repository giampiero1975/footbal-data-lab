# Qwen27 su LIGA — Identità del modello e accesso ai pesi

## Attività, script e commit

Il 20 novembre 2026, nell’attività `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`, una verifica differenziale ha indagato il mismatch rilevato dal [controllo di ammissione](rag-v5-qwen27-isolation-model-access-01.md), che non aveva acquisito gli identificativi effettivi né raggiunto la prova di lettura. Baseline GitHub `ec5c194167b1ec60a10aeb14a897abdc6be703a5`. Script `qwen27_manifest_reconcile_01.py`, commit locale `f013cd955b6542bfb58dbed6dda6d37e38515950`. Compilazione locale del codice remoto e verifica SHA-256 del manifest storico riuscite.

## Risultato

- Una SSH in sola lettura. Il manifest locale del tag `qwen3.8:27b` ha SHA-256 `b45285c1cc1fafaf0272e840a7b799cb11e1b4597c2dc47a2dc58a61942f408c`. I cinque riferimenti alla configurazione e agli strati storici coincidono per tipo, digest e dimensione. Tutti i file dichiarati sono presenti con dimensioni corrispondenti. Il manifest locale contiene anche due riferimenti di catalogo aggiuntivi, incluso quello con il digest storico `aaee06c39dcf2437cde036998d960e1fc1494b8191be7cc9657d01e509097813`. Il tag locale separato `27b-q4_K_M` non è presente nel percorso controllato.
- Il test sotto UID 997 ha negato la lettura del manifest e di tutti e sette gli oggetti riferiti. I file dei pesi non sono stati aperti e i digest dei loro contenuti non sono stati ricalcolati. [Evidenza](qwen27-isolation-model-access-01/manifest-reconciliation.json).
- Nessuna unità, avvio, modifica alla VPS, POST, inferenza o download. Il Gate sintetico e la tenuta RAM con mmap restano da verificare.

## Decisione e stato

**ESEGUITO** il confronto. Gate Linux e Qwen27 mmap **BLOCCATO**. Prima di un nuovo avvio occorre autorizzare l’accesso in sola lettura per l’account isolato, limitato al materiale Qwen richiesto, e adeguare la verifica d’identità locale affinché riconosca il manifest di catalogo attestato e verifichi il riferimento storico e i componenti vincolati. Conservare il digest storico e il comportamento fail-closed. Nessuna modifica eseguita a permessi, codice operativo d’isolamento o binding.
