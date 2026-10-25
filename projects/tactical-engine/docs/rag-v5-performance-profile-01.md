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

## Stato

**IMPLEMENTATO**. Test offline e confronto VPS DA FARE.
