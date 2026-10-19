# Diagnostica coverage H07 senza thinking — 2026-10-19

## Evidenza
Report VPS `diagnostica_coverage_no_think_h07_v1.json` consegnato dall'utente:
- Ollama API nativa `/api/chat`, modello `qwen3.5:9b`, `think=false`, `temperature=0`, `num_ctx=4096`, `num_predict=256`.
- H07 / V4: `value=completo`, gold `completo`, match true.
- `done_reason=stop`, `eval_count=15`, `prompt_eval_count=161`, `thinking=null`, durata 7,37 s.
- Test precedente Ragas 0.4.3 / Instructor: `finish_reason=length`, `completion_tokens=3072`, `content=""`, lunga traccia reasoning, durata 395,4 s.

## Interpretazione
La causa dell'eccezione Ragas precedente è confermata: output troncato prima del risultato finale, non fallimento del database V4. Il test diretto Ollama dimostra che una chiamata con thinking disabilitato produce il valore atteso in 7,37 s. **Non dimostra ancora** che il parametro sia propagato dal client Ragas/Instructor, né che il giudice sia accurato su tutto il benchmark.

## Decisione
Conservare report e baseline; non modificare Chroma, gold, venv principale o Ollama globale. Prossima verifica limitata a integrazione Ragas con impostazioni di generazione compatibili e tracciabili. Il caso H07 è un test diagnostico, non una certificazione di qualità RAG.

## Fonti ufficiali
- https://docs.ollama.com/capabilities/thinking
- https://docs.ollama.com/capabilities/structured-outputs
- https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/general_purpose/
