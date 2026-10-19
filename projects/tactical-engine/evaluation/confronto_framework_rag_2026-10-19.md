# Scelta framework di valutazione DRIBBLING — 2026-10-19

## Obiettivo
Confrontare soluzioni consolidate prima di sviluppare ulteriormente il giudice semantico personalizzato. Non installare nulla nella venv V4 fino a test di compatibilita' isolato.

## Evidenze ufficiali consultate
- Ragas quickstart Ollama: https://docs.ragas.io/en/stable/getstarted/quickstart/
- Ragas metrics: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/
- Ragas Context Precision: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/
- Ragas Context Recall: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/
- DeepEval Ollama: https://deepeval.com/integrations/models/ollama
- DeepEval Faithfulness: https://deepeval.com/docs/metrics-faithfulness
- DeepEval citation faithfulness: https://deepeval.com/docs/metrics-citation-faithfulness

## Compatibilita' documentata
- **Ragas**: quickstart ufficiale supporta Ollama tramite endpoint OpenAI-compatible `http://localhost:11434/v1` e `llm_factory`. Offre Faithfulness, Context Precision, Context Recall e altre metriche RAG. Alcune metriche richiedono risposte di riferimento o contesti recuperati. API in evoluzione: usare versione fissata e API collections dopo verifica.
- **DeepEval**: integrazione ufficiale `OllamaModel(model=..., base_url=..., temperature=0)`; Faithfulness richiede `input`, `actual_output`, `retrieval_context`. Consente metriche, classificatori e test di regressione. Il supporto a citazioni `[N]` va adattato/verificato per ID stabili `[GLEREAN-C018]`.
- **Entrambi**: usano anche LLM-as-judge. Nessuno garantisce da solo il riconoscimento delle inversioni di ruoli osservate con Qwen3.5:9b.

## Ambiente gia' inventariato (non ricontrollare senza cambi)
Da `docs/environment.md`: Python sistema 3.12.3; venv `projects/tactical-engine/.venv`, `chromadb==1.5.9`, `llama-index-core==0.14.25`, `ollama==0.6.3`, `pytest==9.1.1`, `numpy==2.5.4`; Ollama server 0.40.5; Qwen3.5:9b Q4_K_M; VPS 6 vCPU, 15 GiB RAM, CPU-only. Versione interprete della venv non attestata. `pip check` pulito al momento dell'inventario. Versioni Ragas/DeepEval e transitive NON verificate come compatibili con questa venv.

## Decisione e piano reversibile
1. **Ragas** candidato principale per metriche di retrieval/grounding; **DeepEval** candidato complementare per test automatizzati e citazioni.
2. Prima di ogni installazione, costruire ambiente Python **separato** dalla venv V4 e registrare `pip freeze`, `pip check`, versioni effettive e latenza.
3. Confrontare framework su un campione bloccato: risposte originali del benchmark citazioni, contesti recuperati, gold Glerean, casi avversariali H07/H09/H10 e T03. Non confondere la metrica Faithfulness con la completezza.
4. Confrontare accuratezza del giudice sui casi etichettati e costi/tempi, non solo la presenza di una metrica.
5. Nessuna modifica a Chroma, reranker, embedding, LLM o script V4; nessuna promozione prima di validazione.

## Stato
Verificata **compatibilita' documentale di integrazione Ollama** per entrambi. **Non** verificata compatibilita' delle dipendenze con l'ambiente Python esistente; nessuna installazione o esecuzione framework effettuata. Nessun risultato di confronto misurato.
