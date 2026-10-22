# RAG V5 — giudice shadow NLI e pertinenza (2026-10-22)

## Fonti ufficiali consultate

- Ollama /api/chat: https://docs.ollama.com/api/chat — model, messages, format, stream, think, options.
- Ollama structured outputs: https://docs.ollama.com/capabilities/structured-outputs — JSON Schema in format, temperatura bassa, validazione dell'output.
- Pydantic Models: https://docs.pydantic.dev/latest/concepts/models/ — model_json_schema() e model_validate_json(). Validazione dello schema non certifica la correttezza semantica.

## Implementazione

- Runner: scripts/judge_rag_v5_alignment_controls_v1.py.
- Input: evaluation/reports/rag_v5_alignment_controls_v1.json (10 controlli provvisori).
- Output: evaluation/reports/rag_v5_alignment_judge_results_v1.json (nuovo file esclusivo).
- Modello: qwen3.5:9b, Ollama locale, think=false, stream=false, temperature=0, num_ctx=4096, num_predict=200.
- Contratti Pydantic separati: NLI supported/contradicted/insufficient; pertinenza direct/contextual/off_target.
- Ogni controllo conserva etichetta, motivazione, durata, confronto con etichetta provvisoria ed eventuale errore.
- Richiede --execute; non accede a Chroma né modifica pipeline RAG.

## Interpretazione

Accordo con etichette provvisorie non equivale ad accuratezza gold. Non aggregare NLI e pertinenza in un punteggio unico. Revisionare negative_scope_q5, negative_zone, negative_pass e le motivazioni. Per tuning del prompt utilizzare controlli separati per evitare overfitting.

## Verifiche

- Locali: sintassi Python compilata; schema Pydantic validato; input contiene 10 controlli.
- VPS ancora da verificare: dipendenze, runtime Ollama, inferenze e verdetti.
