# Diagnosi Ragas H07 — 2026-10-19

## Evidenze verificate
- `diagnostica_ragas_coverage_h07_v1.json` fornito dall'utente: Ragas 0.4.3, OpenAI 1.109.1, qwen3.5:9b; coverage H07 fallisce dopo 396,25 s con `instructor.exceptions.IncompleteOutputException`.
- Traceback: `ragas.metrics.base.ascore` → `ragas.llms.base.agenerate` → `instructor.client` → `instructor.function_calls.from_response`. Non si tratta di un verdetto tattico errato: nessun punteggio coverage è stato prodotto.
- Diagnostica fidelity H07 Ragas riuscita in 145,22 s; due chiamate dirette Ollama compatibile OpenAI riuscite con JSON valido in circa 194–199 s.
- La causa precisa dell'output incompleto non è provata: nel report manca il contenuto di `last_completion` e il relativo `finish_reason`. Il traceback non dimostra da solo saturazione token o incompatibilità permanente.

## Decisione
1. Non considerare valido il benchmark Ragas v1 come certificazione del RAG: impiega `DiscreteMetric` personalizzata, non la metrica standard Faithfulness.
2. Non modificare Chroma V4, dataset Gold, venv principale, modelli Ollama o configurazione validata.
3. Fermare i test ripetitivi su CPU finché non si acquisiscono `last_completion`, `finish_reason`, `usage` e contenuto della risposta non elaborata.
4. Preferire un test diagnostico singolo e reversibile, con report JSON separato e mai sovrascritto; distinguere errore tecnico da errore semantico.
5. Dopo il test, valutare la configurazione documentata di Instructor per risposte strutturate (tool calling vs JSON) prima di un nuovo benchmark esteso.

## Documentazione di riferimento
- Ragas: https://docs.ragas.io/en/stable/getstarted/quickstart/
- Ragas metriche: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/
- Ollama compatibilità OpenAI: https://docs.ollama.com/api/openai-compatibility
- Ollama output strutturati: https://docs.ollama.com/capabilities/structured-outputs
- Instructor: https://python.useinstructor.com/

## Stato
Diagnosi parziale, causa non confermata. Nessun intervento sui sistemi di produzione.
