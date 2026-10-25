# Benchmark Gemini Coverciano 100

Data: 2026-10-25. Stato: **DA FARE**. Obiettivo del titolare: far creare a
Gemini 100 domande da esame allenatore stile Coverciano, far rispondere il RAG
e raggiungere una media esterna verificata di almeno 8/10.

## Diagnosi Gemini ufficiale

La configurazione storica del progetto era obsoleta:

- `gemini-3.1-flash-lite-preview` e stato spento il 25 maggio 2026;
- `gemini-3-flash-preview` e preview/deprecato, con sostituzione consigliata
  `gemini-3.6-flash`;
- la chiave VPS vede tramite `models.list` i modelli stabili
  `gemini-3.6-flash`, `gemini-3.7-flash` e `gemini-3.8-flash`.

Google definisce HTTP 503 `UNAVAILABLE`: servizio temporaneamente sovraccarico
o non disponibile, distinto dal 429 di quota. La guida ufficiale raccomanda
backoff esponenziale con jitter e retry solo sugli errori transitori. Per
valutazioni offline su larga scala Google raccomanda Batch API: richieste
asincrone, code con retry gestito e target di completamento entro 24 ore.

Riferimenti ufficiali:

- https://ai.google.dev/gemini-api/docs/models
- https://ai.google.dev/gemini-api/docs/deprecations
- https://ai.google.dev/gemini-api/docs/api-errors
- https://ai.google.dev/gemini-api/docs/troubleshooting
- https://ai.google.dev/gemini-api/docs/batch-api
- https://ai.google.dev/gemini-api/docs/rate-limits

Un `models.list` riuscito dimostra che la chiave esiste e vede il catalogo, ma
Google precisa che non garantisce l'abilitazione dell'inferenza o del tier.
Quote effettive e billing devono essere controllati nel progetto AI Studio.

## Protocollo del benchmark

1. Gemini 3.6 Flash genera e congela 100 tracce, ciascuna con categoria,
   difficolta, vincoli e rubrica nascosta.
2. Il manifest deve coprire costruzione, sviluppo, rifinitura, transizioni,
   pressing, blocco basso/medio/alto, palle inattive, gestione risultato,
   adattamenti strutturali e metodologia d'allenamento, evitando duplicati.
3. Il RAG riceve soltanto la domanda. Rubrica, soluzione attesa e giudizio
   Gemini restano separati.
4. Ogni risposta conserva report, evidenze, citazioni, tempi, commit e hash.
5. Gemini valuta in richieste isolate o Batch API con scala 0-10 e motivazione
   strutturale. Il punteggio medio e calcolato localmente.
6. Una nuova iterazione e consentita solo dopo una modifica tecnica
   documentata; si rigenerano soltanto i casi falliti o una regressione
   congelata giustificata.
7. Criterio finale: 100/100 risposte disponibili, zero citazioni invalide,
   media >=8.0/10. Il risultato non estende automaticamente la certificazione
   locked esistente.

## Stato corrente

Il revisore comparativo e disponibile ma i quattro tentativi storici non hanno
prodotto una baseline valida: un endpoint spento, due 503 e un output respinto
per ID. Ledger locale: 4/10. Non consumare altro budget sui modelli preview.
Prossimo gate: una probe minima su `gemini-3.8-flash`, poi generatore manifest
e Batch API con output separati e senza sovrascrittura.

## Probe modello stabile

La chiave VPS ha elencato `gemini-3.8-flash` fra i modelli con
`generateContent`. Una revisione isolata del caso 1 ha comunque restituito
HTTP 503. La successiva probe minima senza dati del progetto, contenente solo
“Rispondi esclusivamente con OK”, ha restituito:

`This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.`

La causa era indisponibilita di capacita su quello specifico endpoint, non il
payload tattico. La probe successiva a `gemini-3.6-flash` stabile ha restituito
HTTP 200/`OK`. Lo stesso modello ha poi valutato realmente il primo report RAG
in 27,8 secondi: 3,0/10, `REVISIONE`, identificando citazione F10 invalida,
preventiva geometricamente errata e fonti troppo generiche. Report VPS:
`evaluation/gemini_coverciano_runtime_case01_stable36_v6.json`.

**Decisione:** seconda AI operativa. Usare `gemini-3.6-flash` come primario,
`gemini-3.1-flash-lite` come fallback da collaudare soltanto in caso di 503 e
Batch API per le 100 domande. `gemini-3.8-flash` resta sospeso finche segnala
alta domanda.

## Prompt del titolare

Prompt base da conservare integralmente:

> fammi 100 domande da commissione all'esame da allenatore a coverciano sulla tattica

Al prompt saranno aggiunti soltanto vincoli di formato necessari per produrre
100 identificativi univoci, copertura bilanciata, difficolta e rubriche nascoste
separate dalle domande mostrate al RAG. Questo evita duplicati e rende la media
riproducibile senza alterare l'intento del titolare.

## Integrazione applicativa

Il collegamento RAG -> Gemini -> pannello e **IMPLEMENTATO** nel codice e
documentato in `docs/rag-v5-gemini-runtime-review-01.md`. Test e deploy VPS
restano DA FARE prima di qualunque dichiarazione INTEGRATO. La generazione del
manifest delle 100 domande non e ancora iniziata.
