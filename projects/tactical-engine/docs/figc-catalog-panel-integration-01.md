# Catalogo FIGC nel pannello — integrazione read-only

Data: 2026-10-26. Stato: **VALIDATO e INTEGRATO**.

## Attività

Esporre nel pannello il catalogo prodotto dal monitor FIGC, mantenendolo
separato dall'inventario della collection. Il nuovo endpoint autenticato
`/v1/knowledge/figc` legge una proiezione priva di percorsi locali e distingue
documenti scoperti, verificati, scaricati e già presenti nel corpus.

La UI dichiara esplicitamente che un PDF scaricato non è automaticamente
indicizzato. Nessun record viene aggiunto alla collection e nessun file del
monitor viene modificato.

## Verifiche offline

- catalogo mancante gestito come sorgente opzionale;
- proiezione di stato senza esposizione di `local_path` o `existing_path`;
- suite catalogo/API: 25/25 PASS;
- compilazione Python: PASS;
- sintassi JavaScript del pannello: PASS.

## Criterio runtime

La promozione richiede pull VPS, suite verde, servizio active, endpoint
autenticato coerente col catalogo reale e verifica del pannello pubblico. Non
estende la certificazione locked e non autorizza ingestion automatica.

## Esito runtime

Il commit `5b55967` è stato allineato sulla VPS. La suite ha confermato 25/25
test e il servizio è rimasto `active`. L'endpoint autenticato ha restituito
schema `figc_catalog_projection_v1`, 10 documenti, zero errori e nessun campo
`local_path`/`existing_path`. Il pannello HTTPS espone correttamente la sezione
“Monitor FIGC” e la distinzione fra scoperto, scaricato e già presente.

Decisione: vista **VALIDATA e INTEGRATA**. Conversione e ingestion dei candidati
restano processi separati e non sono implicitamente autorizzati.
