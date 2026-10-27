# Revisione architettura UI Knowledge Panel — 2026-10-27

## Attività
Riorganizzazione della sola presentazione di `/panel` per eliminare la pagina monolitica e introdurre navigazione per compiti e progressive disclosure.

## Script e commit
`api/knowledge_panel.html` (nel repository sotto `projects/tactical-engine/`); commit `a78181f3a8786d404139eb0c987ffd594c09b163`, branch `ui/panel-information-architecture-20261027`.

## Modifiche
Menu laterale desktop / orizzontale mobile, panoramica, analisi tattica, esplora conoscenze, biblioteca, monitor FIGC, monitoraggio. Connessione sempre disponibile. Bozza documentale e fonti accessibili con dettagli espandibili. Testi introduttivi contestuali.

## Vincoli e verifiche
Il blocco JavaScript applicativo originale è stato preservato byte-per-byte; 43 occorrenze di ID HTML preesistenti conservate. Nessuna modifica a backend, endpoint, autenticazione, token, nomi di funzioni, retrieval, collection o pipeline. Aggiunto esclusivamente JavaScript di navigazione visiva. Controlli statici di integrità della trasformazione superati.

## Limiti
Non è stato eseguito un collaudo browser o smoke HTTPS della nuova UI. Non è stato effettuato deploy. La presenza del codice nel branch non equivale a integrazione runtime. Sono necessari revisione del diff e collaudo visuale/responsive prima del merge; non eseguire benchmark RAG o chiamate a provider per questa modifica.

## Risultato, decisione e stato
Risultato: UI riorganizzata su branch isolato, con logica applicativa originale invariata. Decisione: aprire PR draft, verificare rendering, navigazione e compatibilità DOM senza generazione. Stato: **IMPLEMENTATO**; validazione browser **DA FARE**; integrazione **DA FARE**.

## Verifica differenziale 2026-10-27

Confronto diretto via GitHub tra `main` e branch: 43/43 ID HTML originali conservati, nessun duplicato; 11/11 handler inline conservati; JavaScript applicativo originale identico; sintassi JavaScript applicativo e navigazione PASS; tag principali bilanciati (`main`, `section`, `div`, `details`, `nav`, `aside`, `header`, `button`, `table`, `tbody`, `script`, `style`); sei pagine riconosciute. Correzione differenziale deep-link storici `#ask` e `#diagnostics` nel commit `ccf4db3`. Nessuna chiamata a provider e nessun benchmark duplicato.

Risultato: **VALIDATO** limitatamente alla struttura statica, sintassi e preservazione dei contratti DOM; collaudo reale browser/responsive **DA FARE** perché non disponibile un browser collegato al branch, né deploy di staging. Decisione: non promuovere a **INTEGRATO** senza prova browser, mantenere PR draft e produzione invariata.
