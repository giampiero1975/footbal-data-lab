# Knowledge Panel application integration 02

## Attività

Completare il flusso applicativo locale senza modificare runner, retrieval, collection o profilo locked.

## Modifiche

- stato del job con tempo trascorso e blocco dei doppi invii;
- risposta accompagnata da durata, token generati, motivo di arresto e numero citazioni;
- visualizzazione delle evidenze con fonte, pagine, provenienza ed estratto;
- cronologia effimera della sola sessione browser, mai persistita;
- messaggi distinti per successo, errore HTTP, payload invalido e fallimento del job;
- validazione client della lunghezza minima.

## Sicurezza e privacy

Il bearer token resta solo in memoria. Domande, risposte e cronologia non vengono salvate dal browser. Il rendering dei dati dinamici usa escaping HTML o `textContent`.

## Stato

**IMPLEMENTATO**. Test offline e smoke VPS DA FARE.
