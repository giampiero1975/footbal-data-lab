# Qwen27 mmap su LIGA — Esito V10-02

## Attività, script e commit

Il 20 novembre 2026, nell’attività `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`, autorizzata una sola POST V10-02 senza retry, a valle del [Gate Linux sintetico](rag-v5-qwen27-ollama-isolation-linux-gate-02.md). Baseline GitHub `01ff87d5903a1ad3b3962973fb30ee90592be3b8`. Launcher `qwen27_mmap_attempt_01.py` e attesa del listener isolato nel commit `56bbe0a`. Verificate sintassi, serializzazione del trasporto e identità del payload. Unica differenza rispetto al precedente Qwen27: `use_mmap=true`. SHA-256 del payload `331530c85dac2e0030e5c8d3489cee9c4ea0ee5e53486667e95b00096304451e`. Deadline 900 s, grace 15 s, riserva 4.000.000.000 byte e guardia paging invariata.

## Risultato

- Attempt `qwen27-mmap-on-26112004`. Il daemon dedicato è partito in isolamento e ha risposto `200` a `GET /api/version`, confermando Ollama 0.40.5. Il log ha registrato `mkdir .../models-qwen27/manifests-v2: read-only file system`, seguito da `500` su `GET /api/tags`. Il controllo ha fermato la prova prima di GO. Custodia verificata, zero eventi POST, zero risposte e nessun caricamento dei pesi attestato.
- RAM disponibile al preflight 15.992.438.784 byte, minimo campionato 15.915.474.944 byte prima di qualsiasi generazione. Il limite RAM non è stato raggiunto in questa fase. La tenuta durante il caricamento e l’inferenza rimane indeterminata.
- Il TERM gestito da systemd ha fermato il servizio isolato. Il descrittore del cgroup rimosso ha poi restituito `ENODEV` durante un tentativo di escalation del supervisore. La quiete è stata corroborata da cgroup assente, unità inattiva e PID zero, con barriera rimossa solo dopo la ricevuta. Occorre correggere la classificazione dell’uscita ordinaria del cgroup prima di una successiva prova.
- Ollama e RAG di produzione hanno mantenuto stati, PID e ID di invocazione. Dopo la ricevuta di quiete sono stati disarmati solo i due timer transitori del tentativo. [Esito e catena di custodia](../evaluation/quality_first_qwen27_mmap_on_01/result.json) · [Verifica timer e unità](../evaluation/quality_first_qwen27_mmap_on_01/timer-cleanup.json).

## Decisione e stato

Tentativo **ESEGUITO**, Qwen27 mmap **BLOCCATO** al preflight del catalogo. Nessun retry. Prima di un’altra autorizzazione, predisporre il catalogo richiesto da Ollama 0.40.5 nel solo deposito isolato e verificarne formato, digest, tag e quantizzazione con diagnostica GET, senza caricamento. Verificare in parallelo la classificazione della rimozione ordinaria del cgroup. Nessuna risposta Qwen27 da giudicare. La [prova Gemma26](../evaluation/gemma_mmap_on_02/summary.json) resta il riferimento con una risposta V10-02 completa attestata in remoto.
