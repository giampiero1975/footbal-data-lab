# Stato RAG V5 e valutatori — 22 ottobre 2026

## Distinzione versioni
- **RAG V5**: versione del motore di retrieval e generazione; non modificata dagli esperimenti descritti.
- **Judge shadow V1/V2**: due versioni del valutatore sperimentale della pertinenza e fedeltà delle risposte RAG V5. Non sono versioni del motore.
- Etichette di riferimento dei dieci controlli: **provvisorie, non gold**.

## Evidenze
- V1: 10/10 controlli completati, zero errori, 6/10 accordi con riferimento provvisorio.
- V2: 10/10 controlli completati, zero errori, 6/10 accordi con riferimento provvisorio.
- Unico verdetto modificato: context_defense3 da direct a off_target; riferimento provvisorio contextual.
- Errori persistenti: negative_scope_q5, negative_pass, context_counterattack.
- Non chiamare il 6/10 accuratezza certificata; i controlli sono un piccolo insieme di sviluppo.

## Decisioni
1. Conservare RAG V5 e configurazione funzionante senza modifiche.
2. Non promuovere Judge V2; mantenere entrambi come esperimenti.
3. Non eliminare alcun JSON, baseline, report o controllo finché non esiste una politica di retention verificata.
4. Prima di ulteriori tuning, definire rubric di giudizio e holdout indipendente.
5. Usare la terminologia **RAG V5 / Judge shadow V1 / Judge shadow V2**.

## Documentazione tecnica ufficiale di riferimento
- https://docs.ollama.com/api/chat
- https://docs.ollama.com/capabilities/structured-outputs
- https://docs.pydantic.dev/latest/concepts/models/

I risultati derivano dai report caricati dall'utente, non da accesso diretto alla VPS.
