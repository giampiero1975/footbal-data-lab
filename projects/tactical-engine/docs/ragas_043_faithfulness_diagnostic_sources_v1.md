# Diagnostica Faithfulness Ragas 0.4.3 — verifica documentale

Data verifica: 2026-10-21. Ambito: FOOTBALL-DATA-LAB, DRIBBLING V5, Qwen3.5:9b CPU, Ollama 0.40.5, Ragas 0.4.3.

## Fonti primarie

1. Documentazione ufficiale Ragas Faithfulness: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/
2. **Sorgente versionato Ragas v0.4.3**, classe Faithfulness: https://github.com/vibrantlabsai/ragas/blob/v0.4.3/src/ragas/metrics/collections/faithfulness/metric.py
3. **Sorgente versionato Ragas v0.4.3**, modelli e prompt della metrica: https://github.com/vibrantlabsai/ragas/blob/v0.4.3/src/ragas/metrics/collections/faithfulness/util.py
4. Ollama API nativa: https://docs.ollama.com/api/chat
5. Ollama thinking: https://docs.ollama.com/capabilities/thinking

La fonte 2 è stata consultata direttamente e corrisponde al tag v0.4.3. La fonte 3 è identificata dall'import esplicito del modulo util.py nella fonte 2; il suo contenuto completo **non è ancora stato ispezionato direttamente**. Lo script di tracing cattura gli schemi Pydantic e i prompt effettivamente utilizzati nell'installazione.

## Comportamento accertato dalla sorgente Ragas 0.4.3

- La classe `ragas.metrics.collections.Faithfulness` usa una pipeline in **due chiamate LLM**: `_create_statements(question, response)` e `_create_verdicts(statements, context)`.
- `_create_statements` usa `StatementGeneratorInput(question, answer)`, `StatementGeneratorPrompt.to_string(...)` e `llm.agenerate(..., StatementGeneratorOutput)`. Il risultato è `result.statements`.
- `_create_verdicts` concatena i contesti con `"\\n".join(retrieved_contexts)`, usa `NLIStatementInput(context, statements)`, `NLIStatementPrompt.to_string(...)` e `llm.agenerate(..., NLIStatementOutput)`.
- `_compute_score` conta i verdict booleani veri e li divide per il numero di statement presenti in **NLIStatementOutput.statements**. Non calcola un giudizio a tre etichette; non verifica esplicitamente che il numero di verdict sia uguale al numero di statement estratti.
- In assenza di statement o verdict, il punteggio è NaN. Il benchmark esistente rifiuta score non finiti.
- Il risultato pubblico è `MetricResult(value=...)`: **non contiene** le affermazioni o i giudizi intermedi. Per diagnosticarli bisogna tracciare le chiamate LLM, senza alterare la metrica.

## Implicazioni per i due errori

- **q3_03**: gold supported, score 0.0. Possibili cause: estrazione di statement distorti, mancata inferenza semantica nel giudizio NLI, o instabilità tra esecuzioni. **Nessuna causa è ancora dimostrata.**
- **q5_04**: gold insufficient, score 0.5. Il valore implica, per la formula ufficiale, una frazione di verdict positivi pari a 1/2 (o multipli equivalenti). **Non dimostra da solo** quali affermazioni siano state estratte; verificare `StatementGeneratorOutput` e `NLIStatementOutput`.
- Non interpretare uno score 0.0 come `contradicted`: anche `insufficient` produce zero.
- La soglia >=0.5 del benchmark è esplorativa, non ufficiale né calibrata.

## Tracciamento predisposto

`projects/tactical-engine/scripts/trace_ragas_faithfulness_errors_v1.py` utilizza una sottoclasse di `NativeOllamaRagasLLM` che registra per ogni chiamata `agenerate` il prompt, lo schema Pydantic, l'output validato e la durata. Non cambia i prompt di Ragas, la formula, la configurazione di produzione o i dati. Il risultato viene scritto dopo ogni caso. Attenzione: una nuova esecuzione può differire dal benchmark originale.

## Stato delle verifiche

- **Verificato direttamente:** sorgente versionato `metric.py`, formule, ordine delle chiamate, API Ollama, contratto dell'adattatore installato, benchmark 16/16 completato.
- **Da verificare sperimentalmente:** output intermedi reali q3_03 e q5_04 mediante il trace già predisposto.
- **Non ancora ispezionato integralmente:** implementazione `util.py` del tag v0.4.3 (gli schemi e prompt effettivi saranno catturati dal trace).

## Regola di sicurezza

Nessuna modifica a DRIBBLING V5, Chroma, modello o benchmark gold. Il trace è un esperimento osservazionale. Qualsiasi modifica a prompt, adapter o soglia richiede prima un confronto reversibile sul benchmark e su un set indipendente.
