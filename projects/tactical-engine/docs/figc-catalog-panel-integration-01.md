# Catalogo FIGC nel pannello — integrazione read-only

Data: 2026-10-26. Stato iniziale: **IMPLEMENTATO**; verifica VPS **DA FARE**.

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
