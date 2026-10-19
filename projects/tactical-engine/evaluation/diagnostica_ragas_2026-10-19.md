# Diagnostica Ragas 0.4.3 / Ollama — 2026-10-19

## Evidenza verificata (report VPS fornito dall'utente)
- Script: `scripts/diagnostica_ragas_output_v1.py`, caso H07, claim V4.
- `ragas==0.4.3`, `openai==1.109.1`, `qwen3.5:9b`.
- Richiesta OpenAI-compatible normale: `finish_reason=stop`, JSON valido, `fidelity=contraddittorio`, 1585 completion tokens, 198.73 s.
- Richiesta OpenAI-compatible con `response_format=json_schema`: `finish_reason=stop`, JSON valido, `fidelity=contraddittorio`, 1579 completion tokens, 193.58 s.
- Il benchmark `benchmark_ragas_holdout_v1.py` aveva prodotto `IncompleteOutputException` al primo caso H07 senza risultato. H09/H10/H06 non eseguiti.

## Interpretazione (ipotesi, NON verificata)
Il trasporto OpenAI-compatible di Ollama e la produzione di JSON valido funzionano in due richieste dirette. L'errore Ragas potrebbe essere legato al formato/alla validazione dell'output richiesto da DiscreteMetric, a un comportamento intermittente o a limiti di generazione. Le circa 3m15s per richiesta e ~1580 completion token suggeriscono elevato costo di inferenza; NON dimostrano troncamento. Occorre acquisire traceback completo del percorso Ragas prima di correggere prompt, modello o impostazioni.

## Integrità
- Nessuna modifica a Chroma V4, gold o baseline.
- La diagnostica produce file separati e non sovrascrive i report.
- Esito Ragas: NON VALUTABILE finché la chiamata DiscreteMetric fallisce.
