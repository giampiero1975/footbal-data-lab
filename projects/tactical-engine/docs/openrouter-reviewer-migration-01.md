# Migrazione del revisore applicativo a OpenRouter — 01

Data: 2026-10-26  
Stato: **IMPLEMENTATO** (offline; runtime e deploy ancora **DA FARE**)

## Obiettivo e perimetro

OpenRouter diventa l'unico trasporto esterno attivo del pannello. Le integrazioni
dirette Gemini e Groq sono state rimosse da worker, configurazione e interfaccia.
Script, report e risultati storici restano nel repository per audit e non sono
richiamati dal percorso applicativo.

La pipeline RAG V5 certificata, gli indici e i risultati precedenti non sono
stati modificati. Non è stata eseguita alcuna chiamata API reale.

## Flusso implementato

`domanda -> RAG e fonti -> OpenRouter -> revisione tattica -> verifica delle evidenze -> risposta migliorata`

Il copilot mantiene due passaggi separati e fail-closed. OpenRouter riceve un
elenco ordinato di modelli e può applicare il fallback solo tra endpoint che
supportano i parametri richiesti. È richiesta la non raccolta dei dati lato
provider (`data_collection=deny`). Prompt, estratti e credenziali non vengono
salvati nei report d'errore.

Configurazione prevista sulla VPS:

- `OPENROUTER_API_KEY` nel file privato del servizio;
- `RAG_OPENROUTER_COPILOT_ENABLED=1`;
- `RAG_OPENROUTER_COPILOT_MODELS` per la cascata ordinata;
- `RAG_OPENROUTER_COPILOT_TIMEOUT_SECONDS` per il limite applicativo.

## Modifiche

- nuovo adapter `scripts/openrouter_tactical_copilot_v1.py`;
- API e persistenza migrate a `openrouter_copilot` e file
  `*.openrouter-copilot.json`;
- rimossi dal runtime i doppi passaggi Gemini/Groq;
- pannello reso provider-neutral e collegato a OpenRouter;
- esempi di configurazione privi delle vecchie chiavi dirette;
- test specifici per fallback ordinato, preflight senza rete, chiave obbligatoria
  e report d'errore redatto.

## Evidenze offline

- compilazione Python: PASS;
- suite API + adapter OpenRouter: **22/22 PASS**;
- sintassi JavaScript pannello: PASS;
- ricerca nelle superfici attive di variabili e invocazioni dirette Gemini/Groq:
  zero occorrenze;
- chiamate API: **0**.

## Decisione

La migrazione è **IMPLEMENTATA**, non ancora **VALIDATA** né **INTEGRATA**.
Prima della promozione servono installazione della chiave solo sulla VPS,
deploy anti-conflitto, test offline VPS e una singola prova completa dal
pannello pubblico. I risultati storici Gemini/Groq non vanno cancellati.
