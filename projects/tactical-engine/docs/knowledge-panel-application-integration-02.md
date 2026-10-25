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
- help operativo visibile con recupero amministrativo del token;
- stato di connessione esplicito e pulsanti domanda/ricerca disabilitati fino a
  un'autenticazione riuscita;
- errore `401` tradotto in un'indicazione concreta per reinserire il token.

## Sicurezza e privacy

Il bearer token resta solo in memoria. Domande, risposte e cronologia non vengono salvate dal browser. Il rendering dei dati dinamici usa escaping HTML o `textContent`.

## Biblioteca PDF

Il catalogo espone per ogni documento una classificazione editoriale derivata
da titolo, intestazioni e contenuto: `tattica`, `tecnica`, `allenamento` o
`altro`. Sono conservati categoria primaria, categorie pertinenti e punteggi
trasparenti. Il pannello mostra conteggi, titolo, copertura, pagine osservate e
filtri client-side per testo e categoria. La classificazione non modifica
chunk, embedding, retrieval o collection.

Validazione VPS: 157/157 documenti esposti; categorie primarie 120 tattica, 27
tecnica e 10 allenamento. Le categorie pertinenti non esclusive coprono 153
tattica, 91 tecnica e 42 allenamento. Suite combinate catalogo/API 19/19 e
smoke HTTPS autenticato superati.

## Stato

**VALIDATO e INTEGRATO**. La validazione iniziale 9/9 resta storica. Dopo la
pubblicazione HTTPS, la correzione differenziale dell'onboarding ha superato
13/13 test sulla VPS; lo smoke pubblico mostra help e controlli disabilitati,
mentre l'endpoint catalogo restituisce 200 con token e 401 senza token. Servizio
attivo; nessuna nuova generazione necessaria per la sola UI.
