# Qwen27 su LIGA — Gate Linux di arresto selettivo

## Attività, script e commit

Il 20 novembre 2026, nell’attività `RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01`, eseguito l’unico caso sintetico dopo la predisposizione del [deposito dedicato](rag-v5-qwen27-isolated-store-01.md). Il [Gate 01](rag-v5-qwen27-ollama-isolation-linux-gate-01.md) si era fermato prima delle unità. Gate02 di custodia e suite Windows non sono stati ripetuti. Baseline GitHub `ec5c194167b1ec60a10aeb14a897abdc6be703a5`. Script `qwen27_isolation_linux_gate_02.py`, commit tecnico `9cd3af077b0a27d35e39b42f83a58f97d40b4b92`. Compilazione locale del payload sintetico e controllo Git riusciti.

## Risultato

- Attempt `qwen27-mmap-on-26112002`, Linux `6.8.0-147-generic`, systemd `255.4-1ubuntu8.18`. UID dedicato e accesso al modello verificati con il preflight operativo, senza aprire i pesi. Controller remoto invocato una volta senza retry.
- Il bersaglio sintetico PID `263272` era nel cgroup esclusivo associato all’invocazione `cbc699e973f145a099785de6838722b1` e vedeva solo loopback. La sentinella PID `263266` era fuori dal cgroup, nel namespace host, ed era ancora in esecuzione dopo il KILL e la verifica di quiete.
- Budget sintetico 8 s e grace 2 s. Le soglie operative restano 900 s e 15 s. TERM ricevuto 61,1 ms dopo la deadline. Il supervisore è stato interrotto dopo il TERM. L’interdizione ha rifiutato una seconda prenotazione. KILL via `cgroup.kill` 57,6 ms dopo la scadenza della grace. Quiete attestata 74,2 ms dopo quella scadenza, con cgroup rimosso e PID principale zero. La barriera è stata rimossa solo dopo la ricevuta di quiete.
- Ollama e RAG erano attivi prima e dopo. Il Gate ha registrato lo stato dei servizi, senza misurare le loro identità di invocazione. Unità transitorie e area di prova rimosse. Zero caricamenti, POST, inferenze e pressione RAM/paging indotta. [Evidenze, tempi monotonic, inventario e hash](qwen27-isolation-linux-gate-02.json).

## Decisione e stato

Gate sintetico Linux **VALIDATO** per le proprietà osservate. Usare il deposito dedicato e mantenere il vincolo di una sola POST, zero retry, riserva di 4 GB e guardia paging invariata. Il Gate non misura la tenuta della RAM con Qwen27 mmap né la qualità di V10-02. Prova reale **DA FARE**, subordinata all’autorizzazione esplicita della generazione e ai suoi controlli immediati di ammissione.
