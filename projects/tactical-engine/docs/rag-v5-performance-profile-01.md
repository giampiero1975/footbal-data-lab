# RAG V5 performance profile 01

## Attività

Ridurre la latenza applicativa del RAG V5 senza modificare il profilo locked certificato, la collection o gli algoritmi di retrieval/ranking.

## Differenza tecnica

Il campione applicativo Coverciano ha richiesto 292,61 secondi, di cui 285,42 nel modello, con 3.155 token di prompt e 1.310 token generati. Il nuovo profilo è esplicitamente opt-in e combina:

- sei evidenze anziché otto, per ridurre il prompt ridondante;
- istruzione di completezza concisa entro 500 parole;
- limite di sicurezza a 700 token generati;
- telemetria Ollama estesa (`done_reason` e durate prompt/generazione).

I default restano otto evidenze e nessun limite, quindi il runner locked e i benchmark certificati non cambiano.

## Gate

Un solo confronto sulla medesima domanda Coverciano già misurata è autorizzato dalla differenza tecnica sopra documentata. La promozione richiede: risposta completa ai due quesiti, citazioni presenti e valide, `done_reason=stop`, indice 6196 invariato e miglioramento materiale della latenza. In caso contrario il profilo resta non integrato.

## Primo gate VPS

Test offline 9/9. Il primo confronto ha ridotto la latenza da 292,61 a 193,54 secondi (-33,8%), il prompt da 3.155 a 2.588 token e l'output da 1.310 a 700 token; sei evidenze, citazioni F1–F5 valide e indice 6196 invariato. Il risultato non supera il gate: `done_reason=length` e la seconda parte è troncata.

## Correzione

La guida viene resa vincolante sul formato: nessuna premessa, massimo 350 parole, una sezione per ogni punto e priorità alla copertura completa prima dei dettagli. Il limite tecnico resta 700 token. Un secondo confronto è ammesso perché corregge direttamente il failure mode osservato.

## Stato

Il secondo confronto termina naturalmente (`done_reason=stop`) in 161,09 secondi: -45,0% rispetto ai 292,61 secondi iniziali. Genera 534 token, cita tutte le sei evidenze, non produce citazioni invalide, risponde a entrambi i punti e lascia la collection a 6196 record. SHA-256 JSON: `de7c9fee020a67db43c1ef2d4c0bb001c9a65eececcd070a4e63cfa98ab019d2`.

Il profilo è configurato nel solo servizio API locale tramite `RAG_API_EVIDENCE_LIMIT=6` e `RAG_API_MAX_OUTPUT_TOKENS=700`; servizio riavviato attivo, health 200. Il rollback consiste nel ripristinare 8 e 0. Il runner locked conserva i default precedenti.

**VALIDATO e INTEGRATO** nel profilo API. Valutazione prestazioni/servizio: **9/10** (prima 8,5/10). Non è una certificazione universale della qualità per domande arbitrarie.
