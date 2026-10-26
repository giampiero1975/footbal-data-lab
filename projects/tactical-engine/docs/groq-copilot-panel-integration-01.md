# Groq copilot e pannello operativo — integrazione isolata

Data: 2026-10-26. Stato pannello: **VALIDATO e INTEGRATO**. Stato copilot
Groq: **IMPLEMENTATO**; chiamata live e attivazione servizio **DA FARE**.

## Implementazione

`groq_tactical_copilot_v2.py` esegue, soltanto con `--execute` e conferma Free
Tier, due passaggi:

1. revisione tattica indipendente di domanda e bozza RAG;
2. verifica dei finding contro le evidenze e composizione della risposta finale.

La composizione può applicare soltanto finding classificati `SUPPORTATO`. Gli
altri devono comparire tra gli irrisolti. Il software verifica copertura degli
ID, partizione supportati/irrisolti e citazioni esclusivamente tra le label
disponibili. Nessuna modifica automatica viene scritta nel report RAG.

L'API espone il copilot dietro `RAG_GROQ_COPILOT_ENABLED=1`. Un errore esterno
non cancella la bozza RAG: il pannello la mostra come non revisionata. Gemini
API resta opt-in e disattivato; Gemini Cloud conserva il ruolo conversazionale
di esaminatore e valutatore esterno.

## Nuova interfaccia

Il pannello è stato riorganizzato attorno al compito principale:

- stato a quattro fasi: coda, RAG/fonti, copilot, risposta finale;
- risposta migliorata in primo piano e bozza RAG separata;
- finding, piano di miglioramento e richieste di ulteriori fonti;
- evidenze espandibili e export con entrambe le versioni;
- navigazione Analisi, Biblioteca e Diagnostica;
- layout responsive e gerarchia visiva più leggibile.

## Verifiche offline

- compilazione Python: PASS;
- Structured Output e gate copilot: 7/7;
- API, sicurezza, pannello e copilot: 25/25;
- sintassi JavaScript: PASS;
- nessuna chiave incorporata nel pannello o nel repository.

## Deploy e collaudo pubblico

Il commit applicativo `a77420e` è stato pubblicato, allineato sulla VPS e il
servizio `football-rag-api.service` è stato riavviato con esito `active`.
La suite VPS ha confermato 25/25 test; `/healthz` e `/readyz` autenticati hanno
restituito HTTP 200 e la pagina pubblica
`https://football-lab.byoursite.com/panel` ha restituito HTTP 200.

Il collaudo visivo e dell'albero accessibile ha verificato titolo, guida,
autenticazione, quattro fasi di analisi, risposta migliorata, bozza RAG,
evidenze, diagnostica e biblioteca. Il layout pubblico è quindi
**VALIDATO e INTEGRATO**. Questa decisione riguarda la UI e non promuove il
copilot esterno né estende la certificazione locked.

## Limiti

La chiave Groq non è persistita sulla VPS. Il copilot non viene dichiarato
`INTEGRATO` finché non vengono completati configurazione privata, singola smoke
live autorizzata e verifica dei log redatti. Il RAG
locale 9B mantiene la propria latenza: questa implementazione migliora il flusso
di revisione, non rende più veloce la bozza iniziale.
