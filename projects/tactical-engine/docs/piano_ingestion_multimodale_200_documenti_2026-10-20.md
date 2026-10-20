# Piano di ingestion multimodale generalizzabile — 20 ottobre 2026

## Decisione
Il JSON Glerean `evaluation/glerean_figure_evidence_v2.json` è **solo un caso studio/gold di controllo**: vietato utilizzarlo come contenuto di produzione o iniettare manualmente la sua mappa ruoli nel retriever. Nessuna regola specifica Glerean nella pipeline per gli altri ~200 documenti.

## Evidenze ufficiali
- Docling pipeline options: https://docling-project.github.io/docling/reference/pipeline_options/
- Docling picture description: https://docling-project.github.io/docling/_generated/examples/pictures_description/
- Docling enrichments: https://docling-project.github.io/docling/usage/enrichments/
- Docling chunking: https://docling-project.github.io/docling/concepts/chunking/

Le opzioni documentate includono `generate_picture_images`, `do_picture_classification`, `do_picture_description`, `picture_description_options`, `picture_area_threshold`, `images_scale`. La descrizione automatica è normalmente **disabilitata di default**. Le opzioni e i preset pubblicati potrebbero essere diversi nella versione Docling 2.140.0 installata storicamente: verificare in quell'ambiente prima di adottarli. Non presumere che una descrizione visiva generica comprenda diagrammi tattici.

## Flusso candidato, non ancora validato
1. Inventario automatico PDF e metadati (ID, autore, titolo, disciplina tattica/tecnica/allenamento, checksum).
2. Conversione Docling senza alterare l'originale; preservare struttura, didascalie, pagina, figure, tabelle.
3. Estrarre immagini con opzioni native. Se una figura è ignorata dal parser, registrare un fallback a rendering di pagina, **non** inventare una descrizione.
4. Valutare descrizione VLM tramite API/runtime Docling documentati, solo su figure rilevanti, in job offline separato e con limiti di memoria/tempo. I risultati sono *generati*, non verità di fonte.
5. Associare ciascuna descrizione alla pagina e all'immagine, distinguendo testo estratto, caption originale e descrizione VLM; assegnare ID stabile.
6. Costruire un indice **alternativo** separato da V4, senza sovrascrivere chunk o collection attuali.
7. Testare retrieval, completezza, errori di ruoli/frecce e citazioni su Glerean **e almeno un altro autore**. Aggiungere holdout non visto e casi senza figura.
8. Promuovere solo con miglioramento verificato su fedeltà/completezza e senza regressioni tattiche critiche; rollback = abbandonare indice alternativo e mantenere V4.

## Gate di validazione
- G0: API/opzioni confermate nella versione installata; memoria CPU e modelli disponibili rilevati.
- G1: su PDF campione, numero figure rilevate e copertura pagina/caption misurati; errori di estrazione elencati.
- G2: descrizioni VLM valutate contro immagini e testo senza accesso al gold durante la generazione.
- G3: retrieval A/B a corpus, query, top-k e reranker controllati; verificare supporto semantico delle citazioni.
- G4: test end-to-end su fonti differenti, latenza, costo per documento e throughput su CPU; decisione motivata prima di elaborare 200 PDF.

## Stato
**Solo studio architetturale documentato**; non eseguiti nuovi test VPS, nessuna installazione, nessun reindex e nessuna modifica V4. Il benchmark arricchito manualmente già svolto non dimostra che l'arricchimento automatico funzionerà.
