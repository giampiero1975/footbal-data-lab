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

## Integrazione col runtime corrente — 2026-10-28

Il branch UI è stato riallineato con `codex/rag-coverciano-remediation`. La nuova architettura visiva è stata preservata, mentre il contratto applicativo è stato aggiornato al profilo RAG-only e al revisore OpenRouter opzionale. Rimossi i riferimenti operativi obsoleti a Groq.

Il backend ora persiste lo stato di ogni job in un sidecar privato e ricostruisce anche i fallimenti dopo un riavvio. Ogni errore espone campi stabili (`phase`, `code`, `message`, `action`); la UI li mostra nella risposta, nella cronologia e nel monitor, evitando il precedente evento opaco “Job fallito”. I job storici privi di sidecar vengono recuperati dal registro eventi quando l'evidenza è disponibile.

Verifiche: suite completa **116/116 PASS**, `diff --check` PASS, assenza di marker di conflitto, anteprima browser desktop PASS su Panoramica, Analisi e Monitoraggio, navigazione hash PASS. Non sono state eseguite domande RAG né chiamate a provider. Stato: **VALIDATO offline e in anteprima**; deploy e smoke autenticata VPS **DA FARE**.
