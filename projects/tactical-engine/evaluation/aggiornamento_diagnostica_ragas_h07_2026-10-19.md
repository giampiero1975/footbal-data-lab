# Aggiornamento diagnostica Ragas — 2026-10-19

## Nuova evidenza: test DiscreteMetric H07
Report `diagnostica_ragas_discrete_h07_v1.json` fornito dall'utente:
- Ragas 0.4.3, openai 1.109.1, qwen3.5:9b.
- `DiscreteMetric.ascore` fase `fidelity_only`: **successo**.
- Predizione `contraddittorio`, gold `contraddittorio`: corrispondono.
- Tempo 145.22 secondi.
- Coverage non testata.

## Implicazioni e limiti
Il precedente `IncompleteOutputException` su H07 nel benchmark completo non è riproducibile in questa singola chiamata isolata. Non è corretto attribuirlo con certezza a un bug strutturale di Ragas, a troncamento o a timeout. Il trasporto Ollama e il JSON schema erano già risultati funzionanti. Prossimo esperimento: eseguire separatamente la metrica coverage H07, conservare traceback completo in caso di errore, e non sovrascrivere i report.

Nessuna modifica alla V4, ai gold o al benchmark originale.
