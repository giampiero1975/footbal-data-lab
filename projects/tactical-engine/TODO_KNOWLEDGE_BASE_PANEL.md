# TODO — Pannello Knowledge Base e provenienza delle conoscenze

## Obiettivo
Aggiungere a DRIBBLING un pannello consultabile che mostri quali documenti sono disponibili, quale parte è stata realmente indicizzata e quali estratti sostengono ogni concetto o risposta. Separare dati verificati da classificazioni o sintesi generate automaticamente.

## Vista 1: inventario documentale
- Identificativo stabile, titolo, autore, ente/editore, URL fonte ufficiale, percorso locale, categoria primaria (tattica/tecnica/allenamenti), categorie secondarie, licenza se nota.
- Provenienza e timestamp: primo rilevamento, acquisizione, ultimo controllo, ultima indicizzazione.
- Integrità: SHA256, MIME/PDF valido, pagine, esito Docling, eventuali errori.
- Stati distinti: scoperto, verificato, scaricato, convertito, segmentato, indicizzato, escluso, fallito.
- Evidenziare alias, duplicati binari e passaggi identici fra PDF diversi senza cancellare fonti.

## Vista 2: copertura dell'indice
- Numero PDF per stato e categoria; pagine e chunk per documento; percentuale documenti effettivamente indicizzati.
- Versione pipeline, collection Chroma, embedding model, chunk IDs, data indicizzazione.
- Segnalare incongruenze inventario/Chroma, chunk orfani, documenti con zero chunk, aggiornamenti pendenti.
- Distinguere fonti importate manualmente e scoperte dal futuro monitor FIGC.

## Vista 3: esplora conoscenze e provenienza
- Ricerca testuale e semantica per concetto, filtrabile per categoria, documento, autore e stato.
- Risultati come estratti testuali con titolo, pagina, ID chunk, punteggio, link al documento e pagina quando disponibile.
- Concetti/argomenti estratti automaticamente solo se corredati di passaggi sorgente e stato di validazione.
- Evidenziare concordanze e divergenze fra fonti; non equiparare numero di occorrenze a verità o affidabilità.
- Da risposta DRIBBLING a fonti originali (citation -> chunk -> documento -> pagina), senza inventare riferimenti.

## Vista 4: osservabilità e qualità
- Ultima ingestione, errori, ritentativi, risultati test retrieval, copertura query, duplicati nel contesto.
- Esiti benchmark e RAGAS distinti dall'inventario: valutazioni della risposta non sono quantità di conoscenza appresa.

## Implementazione sicura, per fasi
1. Censire gli schemi e i metadata reali di Chroma V5, il catalogo dei PDF e l'attuale applicazione frontend/backend (read-only).
2. Definire un contratto API read-only per inventario, dettaglio documento, statistiche e ricerca con provenienza.
3. Costruire un indice catalogo derivato/rigenerabile, senza mutare Chroma V5; paginazione e caching.
4. UI con viste Inventario, Copertura, Esplora, Qualità e link agli originali; controlli di accesso per contenuti non pubblici.
5. Test di corrispondenza tra PDF, chunk e metadati; distinguere valori verificati da inferiti.
6. Integrare il registro append-only delle acquisizioni FIGC quando disponibile.

## Criteri di accettazione
- Ogni chunk mostrato ha un'origine tracciabile oppure è esplicitamente marcato come origine incompleta.
- Nessuna sintesi viene presentata come fatto senza citazione del passaggio.
- Le statistiche corrispondono all'indice effettivo, non a stime.
- Le fonti duplicate rimangono consultabili separatamente.
- Nessuna modifica distruttiva al corpus o alla collection validata.

## Stato
Richiesta raccolta, specifica iniziale. Da verificare architettura applicativa e schema metadata prima di implementare.
