# Qwen27 mmap su LIGA — Verdetto V10-02

## Attività, script e commit

Il 20 novembre 2026, nell’attività `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`, è stato autorizzato il completamento della prova V10-02. Baseline GitHub `8cea949f23b6750d89cd79885243902ec8dcc513`. Il [tentativo precedente](rag-v5-qwen27-mmap-attempt-01.md) era terminato con zero POST per il catalogo v2 assente. Il commit `e0ba8e6` ha predisposto il catalogo e la prova locale mirata ha verificato che la rimozione del cgroup, corroborata da systemd, non causa un KILL spurio. La verifica preparatoria `qwen27-mmap-on-26112005` ha rifiutato il tag v2 perché il catalogo di produzione lo implementa come symlink. Zero avvii del supervisore e zero POST in quella fase. Il commit `bd49f6c` ha corretto il riferimento v2, vincolandolo al blob attestato e creando un link interno al solo deposito isolato. Launcher `qwen27_mmap_attempt_03.py`. Payload V10-02 invariato rispetto alla precedente autorizzazione mmap, SHA-256 `331530c85dac2e0030e5c8d3489cee9c4ea0ee5e53486667e95b00096304451e`.

## Risultato

- Attempt `qwen27-mmap-on-26112006`. Ollama 0.40.5 ha riconosciuto il tag, il digest storico e la quantizzazione Q4_K_M. La custodia attesta il GO e una sola POST. Il journal della sola unità isolata attesta che `llama-server` ha avviato il caricamento e riporta `load_tensors: loading model tensors, this can take a while... (load_mode = mmap)`, seguito dai buffer `CPU_Mapped`.
- A 43,393 s dall’inizio del supervisore, la RAM disponibile è scesa a **3.847.450.624 byte** contro la riserva obbligatoria di **4.000.000.000 byte**. Arresto `E_MEMORY_RESERVE` durante l’avvio del modello. Zero risposte HTTP per la POST, zero frammenti di risposta e nessuna risposta tattica. Il journal documenta l’interruzione del caricamento. Nessun retry.
- Quiete attestata 1,803 s dopo l’attivazione della guardia, con TERM, cgroup rimosso e PID azzerato. RAM recuperata a 16.043.102.208 byte. Custodia verificata e barriera chiusa. Disarmati i due timer residui e verificate assenti le unità del tentativo. Ollama e RAG di produzione hanno mantenuto PID e ID di invocazione.

[Preflight preparatorio](../evaluation/quality_first_qwen27_mmap_on_02/result.json) · [Esito, soglia e custodia](../evaluation/quality_first_qwen27_mmap_on_03/result.json) · [Chiusura delle unità](../evaluation/quality_first_qwen27_mmap_on_03/timer-cleanup.json).

## Decisione e stato

Tentativo **ESEGUITO**. Qwen27 27B Q4_K_M con mmap **BLOCCATO** su questa VPS, con questo payload e con la riserva di 4 GB. Chiudere questa strada sulla configurazione corrente. La qualità di Qwen27 resta indeterminata, perché la prova si è fermata durante il caricamento. Gemma26 ha già completato V10-02 in circa 13 min 51 s remoti e resta un riferimento per la qualità offline. [Esito Gemma26](../evaluation/gemma_mmap_on_02/summary.json).
