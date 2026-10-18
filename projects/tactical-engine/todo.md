# DRIBBLING — TODO audit, qualità RAG e pulizia

> Stato: piano di lavoro, NON attestazione di verifiche completate.
> Principio: preservare la baseline V4 e i dati prima di ogni intervento.
> Repository: `giampiero1975/footbal-data-lab`
> Ambito: `projects/tactical-engine/` e ambiente VPS `/opt/football-data-lab`.

## Regole operative vincolanti

- [ ] Prima di ogni diagnosi o modifica tecnica consultare, nell'ordine: documentazione ufficiale aggiornata, guide installazione/configurazione, best practice, requisiti, changelog e repository ufficiali; solo dopo issue e community.
- [ ] Rilevare le versioni REALMENTE installate sulla VPS e verificare compatibilità con le indicazioni ufficiali.
- [ ] Distinguere sempre: **ufficiale**, **verificato sul codice**, **verificato sulla VPS**, **ipotesi**, **esperimento**.
- [ ] Conservare configurazioni validate, prompt, risultati e indici prima delle modifiche; predisporre rollback e test reversibili.
- [ ] Nel troubleshooting eseguire **un comando alla volta**, attendendo l'output prima di proseguire.
- [ ] Nessuna cancellazione o migrazione di dati/modelli senza inventario, controllo dipendenze, backup verificato e approvazione.
- [ ] Non dichiarare un miglioramento sulla base di una singola risposta o di sole citazioni formalmente valide.


## PRIORITÀ MASSIMA — Startup: scegliere e configurare la migliore architettura supportata da evidenze

**Obiettivo principale prima di pulizia o nuovi sviluppi:** stabilire se l'architettura RAG sia la più appropriata per DRIBBLING, scegliere i componenti migliori per requisiti e hardware reali e configurarli **secondo documentazione ufficiale aggiornata e fonti tecniche autorevoli verificabili**, non per tentativi arbitrari.

- [ ] Formalizzare requisiti funzionali e non funzionali: precisione tattica e fedeltà alle fonti, italiano, PDF/figure, citazioni verificabili, latenza, memoria, CPU/GPU, manutenzione e costi.
- [ ] Rilevare versioni e hardware effettivi; identificare la baseline operativa prima di giudicare le alternative.
- [ ] Confrontare **l'architettura nel suo insieme** con i pattern ufficiali documentati per ingestion, retrieval, reranking, generation, grounding/citazioni e valutazione; non assumere che i componenti già scelti siano necessariamente ottimali.
- [ ] Per ogni componente confrontare opzioni supportate e alternative pertinenti: Docling/parsing, chunker/tokenizer, embedding, vector store, retriever, reranker, LLM, synthesizer, valutazione; giustificare anche la scelta di mantenerlo.
- [ ] Per ogni abbinamento verificare versioni compatibili, tokenizer e token budget, API supportate, istruzioni dei modelli, metriche, limiti hardware, parametri raccomandati e documentazione ufficiale/versionata.
- [ ] Distinguere **raccomandazioni ufficiali**, evidenze di benchmark riproducibili, fonti autorevoli indipendenti e ipotesi ancora da testare; annotare URL, data, versione e grado di attendibilità.
- [ ] Identificare personalizzazioni e codice scritto autonomamente che aggirano, duplicano o contraddicono funzionalità ufficiali; mantenere soltanto ciò che è necessario e misurabilmente utile.
- [ ] Produrre una **matrice decisionale architetturale**: requisito → componente/alternative → fonti ufficiali → compatibilità → qualità → risorse → decisione motivata.
- [ ] Definire una **configurazione di riferimento raccomandata**, versionata e riproducibile (componenti, versioni/digest, parametri, prompt, dipendenze e diagramma), senza sostituire automaticamente la V4.
- [ ] Validare le scelte su benchmark già disponibili e gold evidence corretti, con confronti controllati e test reversibili; evitare di replicare prove storiche già conclusive.
- [ ] Soltanto **dopo** la validazione architetturale: consolidare codice e configurazioni, dismettere componenti scartati e ripulire gli indici secondo il piano di rollback.

**Criterio di uscita dalla fase startup:** architettura e abbinamenti motivati da fonti ufficiali e risultati riproducibili; configurazione di riferimento documentata; baseline preservata; componenti non necessari identificati e rimossi in sicurezza.

## 1. Inventario e stato reale — prima di ottimizzare

- [ ] Confrontare codice GitHub con file e commit effettivamente presenti sulla VPS; verificare branch e modifiche locali non versionate.
- [ ] Identificare entry point, script invocati, import, servizi systemd, cron, processi e automazioni attive.
- [ ] Censire Python/venv, dipendenze e versioni di Docling, docling-core, LlamaIndex (core e plugin), ChromaDB, Ollama, Transformers, sentence-transformers, PyMuPDF e PyTorch.
- [ ] Censire modelli Ollama installati, tag/versioni, modelli caricati, consumo RAM/VRAM/disco.
- [ ] Censire modelli di embedding/reranking presenti in cache e relativa occupazione.
- [ ] Censire tutte le collection ChromaDB: nome, numero record, dimensioni, metrica, metadati, modello embedding, sorgente e ultima utilizzazione (quando verificabile).
- [ ] Censire file temporanei, report, output di test, cache e dataset locali, separando sorgenti originali da artefatti rigenerabili.
- [ ] Registrare inventario e risultati nel repository, senza credenziali, dati sensibili, PDF o indici pesanti.

## 2. Audit architetturale secondo fonti ufficiali

- [ ] Ricostruire la pipeline realmente attiva: PDF → Docling → chunking → embedding → ChromaDB → retrieval → reranking → generazione → citazioni.
- [ ] Verificare Docling: conversione PDF, lettura di tabelle/figure, struttura esportata, provenienza/pagine e limiti delle immagini non interpretate.
- [ ] Verificare HybridChunker e contextualization rispetto alle API ufficiali e alle versioni installate.
- [ ] Controllare l'allineamento tokenizer/chunking con Qwen3-Embedding 0.6B: V3 usa tokenizer Nomic; V4 riutilizza gli 86 testi V3. **Ipotesi da misurare, non errore dimostrato.**
- [ ] Verificare indicazioni ufficiali del modello Qwen3-Embedding: input, eventuali istruzioni query/documento, limiti token, normalizzazione e compatibilità con Ollama/LlamaIndex.
- [ ] Verificare ChromaDB: metrica effettiva, embedding coerenti tra scrittura e query, filtri metadata, persistenza e gestione collection.
- [ ] Verificare LlamaIndex: VectorStoreIndex, DoclingNodeParser, ChromaVectorStore, OllamaEmbedding, retriever, filtri, CitationQueryEngine e response synthesizer.
- [ ] Riesaminare `citation_chunk_size=2048`, `citation_chunk_overlap=0`, `response_mode='compact'`, prompt QA/refine e gestione del contesto **rispetto alla versione installata**; non assumere che valori predefiniti diversi siano automaticamente migliori.
- [ ] Verificare Ollama/Qwen3.5 9B: tag/modello realmente usato, context window effettiva, parametri generation, thinking, timeout, template e limiti hardware.
- [ ] Verificare reranker mMARCO e alternative BGE: API ufficiali, lingua, truncation/max_length, scoring e compatibilità hardware.
- [ ] Identificare componenti sviluppati manualmente che duplicano funzionalità ufficiali; valutarne motivazione e impatto prima di sostituirli.
- [ ] Produrre matrice componente/versione/configurazione/fonte ufficiale/esito/azione.

## 3. Baseline, esperimenti e qualità

- [ ] Identificare senza ambiguità quale pipeline sia la baseline V4 operativa; distinguere script storici, V4 con Nomic/BGE e V4 con Qwen3-Embedding/mMARCO.
- [ ] Congelare baseline: commit, configurazioni, prompt, parametri, checksum degli input e identificativi delle collection.
- [ ] Recuperare dai test già eseguiti i risultati utili, evitando di ripetere benchmark già conclusi senza motivo.
- [ ] Consolidare un set di domande rappresentative, includendo Q8 ampiezza offensiva e casi con differenze tra fase, zona, ruolo e autore.
- [ ] Costruire/validare gold evidence con riferimenti ai passaggi reali; correggere gold provvisori e casi senza gold.
- [ ] Separare metriche di retrieval (es. recall@k, MRR), reranking, fedeltà semantica, completezza, citazioni e latenza.
- [ ] Verificare semanticamente ogni affermazione: citazione presente ≠ affermazione sostenuta.
- [ ] Diagnosticare se gli errori nascono da estrazione, chunking, retrieval, reranking, assemblaggio contesto o generazione.
- [ ] Confrontare esperimenti **una variabile alla volta**, a parità di domande, fonti e criteri; conservare report riproducibili.
- [ ] Testare eventuali alternative in collection/configurazioni separate; non sovrascrivere V4.
- [ ] Registrare decisioni: ipotesi, test, risultati, costi, regressioni, esito e rollback.

## 4. Pulizia del codice e Git

- [x] Verificata nel repository la presenza di **36 script Python** in `projects/tactical-engine/scripts/` (inventario GitHub; non prova di utilizzo sulla VPS).
- [ ] Classificare ciascuno script: operativo, baseline, test riproducibile, sperimentale, storico, inutilizzato o stato incerto.
- [ ] Mappare import e riferimenti incrociati prima di spostare/rinominare file.
- [ ] Progettare struttura ordinata (`src/`, `config/`, `tests/`, `experiments/`, `archive/`, documentazione), adattandola alle dipendenze reali.
- [ ] Centralizzare configurazioni ripetute e documentare entry point ufficiale, senza introdurre nuove differenze di comportamento.
- [ ] Consolidare funzioni duplicate solo con test di regressione e rollback.
- [ ] Archiviare prima di eliminare; Git conserva lo storico del codice ma NON sostituisce backup di database, PDF o modelli.
- [ ] Controllare `.gitignore`, inclusa regola `*.txt`, per evitare esclusioni involontarie di test/requisiti e inclusione di dati pesanti o segreti.
- [ ] Aggiungere README tecnico, inventario, decision log e procedura riproducibile di esecuzione/valutazione.

## 5. Dismissione componenti scartati e pulizia dati

- [ ] Identificare modelli Ollama dismessi e verificare che non siano referenziati da script, servizi, test da mantenere o procedure di rollback.
- [ ] Identificare pesi di embedding/reranking in cache non più necessari, distinguendo cache condivise e dipendenze indirette.
- [ ] Identificare dipendenze Python inutilizzate senza rimuovere dipendenze transitive necessarie.
- [ ] Identificare collection ChromaDB obsolete e verificare assenza di riferimenti attivi.
- [ ] Identificare processi/servizi/cron dismessi e possibili consumi di risorse.
- [ ] Identificare cache, file temporanei, output duplicati e indici rigenerabili.
- [ ] Prima della rimozione: inventario → prova di non utilizzo → backup/rollback → approvazione → rimozione controllata → verifica post-rimozione.
- [ ] Misurare spazio, RAM/VRAM e prestazioni prima/dopo; distinguere risparmio disco da liberazione di memoria.
- [ ] Non eliminare PDF sorgenti, dati di knowledge base, gold set o baseline senza esplicita autorizzazione.

## 6. Criteri di completamento

- [ ] Una pipeline operativa chiaramente identificata e documentata.
- [ ] Configurazioni/versioni tracciate e compatibilità verificata sulle fonti ufficiali.
- [ ] Baseline V4 ripristinabile e regressioni controllate.
- [ ] Benchmark riproducibili con gold evidence e valutazione semantica.
- [ ] Codice storico separato dal codice operativo, senza dipendenze spezzate.
- [ ] Nessun componente scartato rimasto installato **senza motivo documentato**.
- [ ] Collection, cache e modelli censiti; rimozioni effettuate soltanto in sicurezza.
- [ ] Decisioni e risultati registrati su Git per evitare di ripetere analisi già svolte.

## Stato delle verifiche

- **Verificato sul repository GitHub:** esistono pipeline e test V1–V5; 36 script Python; V3 usa tokenizer Nomic e V4 Qwen reindicizza gli stessi testi; alcuni gold del benchmark reranker sono provvisori; la validazione V5 delle citazioni non garantisce correttezza semantica.
- **Non ancora verificato sulla VPS in questo audit:** versioni effettive, processi attivi, collection presenti, modelli installati, dipendenze runtime, spazio utilizzato e componenti realmente dismessi.
- **Da completare:** confronto puntuale con documentazione ufficiale aggiornata e changelog delle versioni installate.

> Aggiornare le checkbox solo dopo una verifica concreta, annotando evidenze e data. Non considerare una proposta come lavoro completato.
