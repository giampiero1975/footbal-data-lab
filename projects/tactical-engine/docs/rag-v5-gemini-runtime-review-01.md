# Revisione Gemini nel flusso applicativo RAG V5

Data: 2026-10-25. Stato corrente: **IMPLEMENTATO**, collaudo VPS **DA FARE**.

## Attivita e perimetro

L'API applicativa avvia, dopo una risposta RAG formalmente riuscita, una
revisione indipendente con `gemini-3.6-flash`. A Google vengono inviati solo
domanda, risposta ed estratti delle evidenze gia selezionate. Token, chiavi e
PDF completi non fanno parte del payload. La pipeline locked e le collection
non vengono modificate.

Il pannello distingue ora tre condizioni:

- revisione verificata, con modello, voto, verdetto, errori strutturali,
  problemi delle evidenze e correzione minima;
- revisore temporaneamente non disponibile, con risposta RAG esplicitamente
  indicata come non verificata;
- revisione disattivata nella configurazione del servizio.

Un errore o timeout Gemini non cancella la risposta RAG. Il log applicativo
registra soltanto stato tecnico e motivo sintetico, senza contenuti o segreti.

## Configurazione

L'attivazione e opt-in tramite:

```text
RAG_GEMINI_REVIEW_ENABLED=1
RAG_GEMINI_REVIEW_MODEL=gemini-3.6-flash
RAG_GEMINI_REVIEW_TIMEOUT_SECONDS=240
RAG_GEMINI_REVIEW_DAILY_LIMIT=100
```

Il modello e stato scelto perche la probe e una revisione reale hanno
restituito HTTP 200, mentre `gemini-3.8-flash` ha restituito HTTP 503 per alta
domanda. Evidenza precedente:
`evaluation/gemini_coverciano_runtime_case01_stable36_v6.json`.

## Benchmark Coverciano 100

Prompt base fornito dal titolare e conservato integralmente:

> fammi 100 domande da commissione all'esame da allenatore a coverciano sulla tattica

Il generatore aggiungera soltanto vincoli macchina per numerazione, unicita,
copertura bilanciata e rubrica nascosta. Obiettivo: 100 risposte disponibili,
zero citazioni invalide e media Gemini almeno 8/10. Tempi, problemi, vantaggi e
limiti saranno riepilogati nel report conclusivo sulla base dei report runtime.

## Decisione

Eseguire test offline e deploy VPS; poi una sola domanda nuova di smoke per
validare l'intero passaggio RAG -> Gemini -> pannello. Non ripetere le domande
gia valutate. Solo dopo avviare la generazione congelata delle 100 tracce.

