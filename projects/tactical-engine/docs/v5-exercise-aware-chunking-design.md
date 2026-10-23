# V5-EXERCISE-CHUNK-DESIGN-01

Stato: ESEGUITO (progettazione documentale soltanto).

## Evidenze
I controlli V5-USSIA-4A-MAP-01 e V5-USSIA-4A-CHUNK-CODE-01 sono gia eseguiti e non vanno ripetuti. Il JSON originale Ussia a pagina 14 contiene il titolo Esercitazione 4/A e il relativo svolgimento. Il chunk Chroma 10 contiene lo svolgimento insieme a materiale 3/A, ma non conserva il titolo 4/A tra le intestazioni. Il builder V5 usa HybridChunker con merge_peers e identificativi dipendenti dal testo.

## Proposta tecnica
Creare un estrattore separato e opt-in che riconosca le intestazioni delle esercitazioni nella sequenza strutturata Docling. Associare titolo, sottotitoli e svolgimento fino al successivo confine di esercitazione, preservando provenienza, pagine e riferimenti agli elementi originali. Non considerare una voce del sommario come descrizione completa di un esercizio. Se occorre suddividere un esercizio lungo, replicare il titolo nei sottochunk senza unirlo ad altri esercizi. Non alterare il builder V5 corrente.

## Sicurezza e rollback
Mantenere intatta la collection V5 attuale di 5319 record, insieme ai runner e ai benchmark esistenti. Eventuali nuovi embedding andranno esclusivamente in una collection candidata separata, con identificativi versionati e rollback mediante ritorno alla collection originale. Nessuna scrittura a Chroma e nessuna promozione a produzione senza evidenze distinte.

## Accettazione futura
Prima verifica nuova consentita: controllo deterministico offline che dimostri associazione di titolo e contenuto 4/A, separazione da 3/A e 4/B, pagina 14 corretta e assenza di false corrispondenze dal sommario. Non ripetere mapping e differenziali retrieval gia completati.

Decisione: implementare estrattore opt-in e verifiche offline come attivita successiva DA FARE. Questo documento non certifica miglioramenti retrieval.
