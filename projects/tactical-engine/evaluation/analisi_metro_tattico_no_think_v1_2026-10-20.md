# Esito benchmark metro tattico no-thinking v1 — 2026-10-20

## Report ricevuto
`projects/tactical-engine/benchmark_metro_tattico_no_think_v1.json`, prodotto sulla VPS dall'utente. Script `scripts/benchmark_metro_tattico_no_think_v1.py`; modello `qwen3.5:9b`, API nativa Ollama, `think=false`, JSON vincolato, temperature 0. Durata 151,03 secondi.

| Asse | Accordo con Gold preliminare |
|---|---:|
| Fedeltà | 12/12 = 100% |
| Completezza | 10/12 = 83,33% |
| Entrambi | 10/12 = 83,33% |
| Errori tecnici | 0/12 |

## Disaccordi verificati
- **H05 / V3**: Gold completezza `parziale`; giudice `completo`. La frase parla dell'appoggio arretrato dei centrocampisti prima che il compagno abbia assicurato il possesso, ma omette l'inserimento verticale breve nello spazio centrale.
- **H10 / P1**: Gold completezza `parziale`; giudice `completo`. La frase prescrive passaggio immediato e rischioso anziché protezione; inverte la preferenza per il controllo sicuro. Il giudice identifica correttamente la contraddizione ma considera trattati tutti i nuclei. Questa etichetta di copertura è meno netta: la frase non esplicita l'aspetto della gestione/protezione del pallone per guadagnare tempo. Serve revisione del criterio Gold, non modifica retroattiva opportunistica.

## Interpretazione e limiti
L'esito prova che il trasporto locale e la generazione strutturata funzionano senza errori sui 12 casi. Il 100% di fedeltà è **accuratezza del giudice su questo piccolo holdout sintetico**, non qualità delle risposte RAG, né accuratezza generale stimata. La copertura non è sufficientemente calibrata; H05/H10 meritano audit umano del Gold e dei nuclei essenziali. Non sono state valutate risposte reali, retrieval, citazioni, figure, robustezza su documenti diversi. Il verificatore è custom, **non Ragas né DeepEval**.

## Decisione
Conservare immutati report e gold; non toccare Chroma V4. Prima di introdurre uno score unico di DRIBBLING, validare giudizi su risposte RAG reali con rubriche e citazioni; presentare separatamente fedeltà, completezza, validità delle citazioni e recupero delle fonti. Non dichiarare certificato il giudice.

## Documentazione ufficiale API
- https://docs.ollama.com/capabilities/thinking
- https://docs.ollama.com/capabilities/structured-outputs
