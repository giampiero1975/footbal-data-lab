# DRIBBLING V5 — Piano operativo, checklist e registro delle evidenze

> **Documento di riferimento operativo** · Aggiornato il 2026-10-21 · Repository: `giampiero1975/footbal-data-lab` · Ambito: `projects/tactical-engine/` e VPS `/opt/football-data-lab`.
>
> **Attenzione:** una casella spuntata documenta l'attività descritta, non la certificazione dell'intero RAG. I risultati riportati come comunicati dalla VPS non equivalgono a un accesso diretto dell'assistente alla VPS. Preservare baseline V4, indici e configurazioni prima di qualunque intervento.

## Come usare questo documento

1. **Prima di lavorare:** leggere le regole nella sezione 1 e la fotografia dell'ambiente in [docs/environment.md](docs/environment.md), [docs/components.md](docs/components.md), [docs/decisions.md](docs/decisions.md) e [docs/verification.md](docs/verification.md).
2. **Per scegliere il prossimo lavoro:** seguire le priorità qui sotto e le dipendenze; non ripetere verifiche già documentate senza una modifica effettiva.
3. **Per chiudere una voce:** annotare fonte ufficiale/versione, commit o report, risultato, limiti, decisione e rollback quando applicabile. `[x]` = evidenza registrata; `[ ]` = aperta o non ancora certificata.
4. **Per i benchmark:** distinguere *development*, *stress test con fonti riutilizzate*, *holdout prospettico*, *gold revisionato* e *validazione end-to-end*. Un risultato NLI non equivale alla qualità del RAG completo.
5. **Per la VPS:** il repository non dimostra lo stato runtime corrente; utilizzare soltanto controlli mirati ai dati mancanti o cambiati.

### Priorità operative attuali

| Ordine | Attività | Dipendenza / criterio |
| --- | --- | --- |
| P0 | Concludere e verificare il benchmark NLI V2 FIGC/FA da 30 claim | Report JSON completo e analisi degli errori; non ancora dichiarato superato |
| P0 | Revisionare gold NLI e validare fonti realmente nuove e testi più lunghi | Nessuna ottimizzazione del prompt sui casi di test |
| P0 | Definire criteri e gold end-to-end, inclusi fedeltà, completezza, citazioni e astensione | Prima di promuovere DRIBBLING V5 |
| P1 | Validare retrieval/reranking H09 e filtro tattico su holdout indipendente | Baseline V4 intatta; misurare latenza e regressioni |
| P1 | Integrare NLI V2 in modalità shadow reversibile | Solo dopo i gate di validazione del giudice |
| P1 | Confrontare V4 e V5 con domande reali, figure e fonti multiple | Stesso gold, condizioni controllate, nessuna modifica in-place |
| P2 | Consolidare architettura, documentazione e pulizia componenti | Dopo inventario dipendenze, backup e rollback verificati |

### Legenda delle evidenze

- **Ufficiale:** documentazione del produttore/progetto per la versione pertinente.
- **Codice verificato:** stato letto su GitHub, non necessariamente deployato.
- **VPS riportata:** output o report di esecuzioni VPS forniti in chat, senza accesso remoto diretto.
- **Esperimento:** benchmark controllato con limiti espliciti; non implica promozione.
- **Da verificare:** attività aperta o gold/risultato non sufficientemente indipendente.

## 1. Regole operative e criteri di accettazione

### Regole operative vincolanti

- [ ] Prima di ogni diagnosi o modifica tecnica consultare, nell'ordine: documentazione ufficiale aggiornata, guide installazione/configurazione, best practice, requisiti, changelog e repository ufficiali; solo dopo issue e community.
- [ ] Rilevare le versioni REALMENTE installate sulla VPS e verificare compatibilità con le indicazioni ufficiali.
- [ ] Distinguere sempre: **ufficiale**, **verificato sul codice**, **verificato sulla VPS**, **ipotesi**, **esperimento**.
- [ ] Conservare configurazioni validate, prompt, risultati e indici prima delle modifiche; predisporre rollback e test reversibili.
- [ ] Nel troubleshooting eseguire **un comando alla volta**, attendendo l'output prima di proseguire.
- [ ] Nessuna cancellazione o migrazione di dati/modelli senza inventario, controllo dipendenze, backup verificato e approvazione.
- [ ] Non dichiarare un miglioramento sulla base di una singola risposta o di sole citazioni formalmente valide.

### 6. Criteri di completamento

- [ ] Una pipeline operativa chiaramente identificata e documentata.
- [ ] Configurazioni/versioni tracciate e compatibilità verificata sulle fonti ufficiali.
- [ ] Baseline V4 ripristinabile e regressioni controllate.
- [ ] Benchmark riproducibili con gold evidence e valutazione semantica.
- [ ] Codice storico separato dal codice operativo, senza dipendenze spezzate.
- [ ] Nessun componente scartato rimasto installato **senza motivo documentato**.
- [ ] Collection, cache e modelli censiti; rimozioni effettuate soltanto in sicurezza.
- [ ] Decisioni e risultati registrati su Git per evitare di ripetere analisi già svolte.

## 2. Stato attuale, inventario e baseline V4

### 1. Inventario e stato reale — prima di ottimizzare

- [ ] Confrontare codice GitHub con file e commit effettivamente presenti sulla VPS; verificare branch e modifiche locali non versionate.
- [ ] Identificare entry point, script invocati, import, servizi systemd, cron, processi e automazioni attive.
- [x] Censire Python/venv, dipendenze e versioni di Docling, docling-core, LlamaIndex (core e plugin), ChromaDB, Ollama, Transformers, sentence-transformers, PyMuPDF e PyTorch. Evidenze in `docs/environment.md`; interprete venv ancora da verificare.
- [x] Censire modelli Ollama installati, tag/versioni e modelli caricati al momento del controllo. Dimensioni dei modelli registrate; consumo RAM/VRAM **sotto carico** ancora da misurare in un test dedicato.
- [x] Censire i repository di embedding/reranking presenti nella cache Hugging Face e l'occupazione aggregata (11 repository; Hub 5,0 GB; cache utente 5,2 GB), con verifica specifica Alibaba GTE 600 MB tramite `du -shL`. **Dimensioni reali di tutti gli altri modelli e dipendenze runtime ancora aperte.** Evidenze in `docs/environment.md` (seconda PuTTY, 2026-10-21).
- [ ] Censire tutte le collection ChromaDB: nome, numero record, dimensioni, metrica, metadati, modello embedding, sorgente e ultima utilizzazione (quando verificabile). **Parziale verificato 2026-10-19:** V3 e V4 86 record ciascuna, V3 cosine/768D e V4 L2/1024D; collection ulteriori, spazio e utilizzo da completare.
- [ ] Censire file temporanei, report, output di test, cache e dataset locali, separando sorgenti originali da artefatti rigenerabili.
- [x] Registrare **i risultati dell'audit hardware, Python e Ollama già effettuato** nel repository (`docs/environment.md`, 2026-10-19), senza credenziali, dati sensibili, PDF o indici pesanti. **Inventario completo Chroma/cache/servizi ancora aperto.**

### 3. Baseline, esperimenti e qualità

- [ ] Identificare senza ambiguità quale pipeline sia la baseline V4 operativa; distinguere script storici, V4 con Nomic/BGE e V4 con Qwen3-Embedding/mMARCO.
- [ ] Congelare baseline: commit, configurazioni, prompt, parametri, checksum degli input e identificativi delle collection.
- [x] Recuperare dai test già eseguiti i risultati utili, evitando di ripetere benchmark già conclusi senza motivo. **Primo consolidamento esistente:** docs/status-2026-10-19.md ed evaluation/*, inclusi EXP-001, Q8 TOP5/TOP10, holdout e giudice no-thinking; mantenere aggiornato il registro.
- [ ] Consolidare un set di domande rappresentative, includendo Q8 ampiezza offensiva e casi con differenze tra fase, zona, ruolo e autore.
- [ ] Costruire/validare gold evidence con riferimenti ai passaggi reali; correggere gold provvisori e casi senza gold.
- [ ] Separare metriche di retrieval (es. recall@k, MRR), reranking, fedeltà semantica, completezza, citazioni e latenza.
- [ ] Verificare semanticamente ogni affermazione: citazione presente ≠ affermazione sostenuta.
- [ ] Diagnosticare se gli errori nascono da estrazione, chunking, retrieval, reranking, assemblaggio contesto o generazione.
- [ ] Confrontare esperimenti **una variabile alla volta**, a parità di domande, fonti e criteri; conservare report riproducibili.
- [ ] Testare eventuali alternative in collection/configurazioni separate; non sovrascrivere V4.
- [ ] Registrare decisioni: ipotesi, test, risultati, costi, regressioni, esito e rollback.

## 3. Architettura e componenti

### PRIORITÀ MASSIMA — Startup: scegliere e configurare la migliore architettura supportata da evidenze

**Obiettivo principale prima di pulizia o nuovi sviluppi:** stabilire se l'architettura RAG sia la più appropriata per DRIBBLING, scegliere i componenti migliori per requisiti e hardware reali e configurarli **secondo documentazione ufficiale aggiornata e fonti tecniche autorevoli verificabili**, non per tentativi arbitrari.

- [ ] Formalizzare requisiti funzionali e non funzionali: precisione tattica e fedeltà alle fonti, italiano, PDF/figure, citazioni verificabili, latenza, memoria, CPU/GPU, manutenzione e costi.
- [ ] Rilevare versioni e hardware effettivi; identificare la baseline operativa prima di giudicare le alternative.
- [ ] Confrontare **l'architettura nel suo insieme** con i pattern ufficiali documentati per ingestion, retrieval, reranking, generation, grounding/citazioni e valutazione; non assumere che i componenti già scelti siano necessariamente ottimali.
- [ ] Per ogni componente confrontare opzioni supportate e alternative pertinenti: Docling/parsing, chunker/tokenizer, embedding, vector store, retriever, reranker, LLM, synthesizer, valutazione; giustificare anche la scelta di mantenerlo.
- [ ] Per ogni abbinamento verificare versioni compatibili, tokenizer e token budget, API supportate, istruzioni dei modelli, metriche, limiti hardware, parametri raccomandati e documentazione ufficiale/versionata.
- [ ] Distinguere **raccomandazioni ufficiali**, evidenze di benchmark riproducibili, fonti autorevoli indipendenti e ipotesi ancora da testare; annotare URL, data, versione e grado di attendibilità.
- [ ] Identificare personalizzazioni e codice scritto autonomamente che aggirano, duplicano o contraddicono funzionalità ufficiali; mantenere soltanto ciò che è necessario e misurabilmente utile.
- [ ] Completare la **matrice decisionale architetturale** con benchmark, compatibilità esatta e decisioni definitive. **Bozza documentale con fonti ufficiali e prove da fare già registrata** in `docs/components.md`.
- [ ] Definire una **configurazione di riferimento raccomandata**, versionata e riproducibile (componenti, versioni/digest, parametri, prompt, dipendenze e diagramma), senza sostituire automaticamente la V4.
- [ ] Validare le scelte su benchmark già disponibili e gold evidence corretti, con confronti controllati e test reversibili; evitare di replicare prove storiche già conclusive.
- [ ] Soltanto **dopo** la validazione architetturale: consolidare codice e configurazioni, dismettere componenti scartati e ripulire gli indici secondo il piano di rollback.

**Criterio di uscita dalla fase startup:** architettura e abbinamenti motivati da fonti ufficiali e risultati riproducibili; configurazione di riferimento documentata; baseline preservata; componenti non necessari identificati e rimossi in sicurezza.

### 2. Audit architetturale secondo fonti ufficiali

**CHECK DI OTTIMIZZAZIONE COMPONENTI — DA ESEGUIRE, NON SPUNTARE IN ANTICIPO:** per ogni componente verificare documentazione ufficiale aggiornata e relativa versione, parametri raccomandati, compatibilità degli abbinamenti, eventuali personalizzazioni ridondanti, impatto su CPU/RAM e test comparativo rispetto alla V4. Registrare URL, data, esito e decisione (mantenere/modificare/sostituire). Solo una verifica documentale **e** sperimentale consente di dichiarare un'ottimizzazione validata.


- [ ] Ricostruire la pipeline **realmente attiva sulla VPS**: PDF → Docling → chunking → embedding → ChromaDB → retrieval → reranking → generazione → citazioni. **Ricostruzione statica degli script GitHub completata** in `docs/verification.md` A01–A04 e `docs/components.md`; entry point runtime ancora sconosciuto.
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
- [x] Produrre **prima matrice documentale** componente/versione/configurazione/fonte ufficiale/esito/azione (`docs/components.md`); compatibilità esatta delle release e benchmark restano aperti.

## 4. Ingestion, documenti e figure tattiche

### PRIORITÀ MASSIMA — Completezza delle fonti e figure tattiche

- [x] Audit visuale delle figure Glerean 12–14 e 18–21, con riscontro sulle pagine PDF originali. Vedi evaluation/audit_figure_glerean_v1.md.
- [x] Preparazione offline di descrizioni strutturate delle figure e sei contesti arricchiti; testi originali e hash conservati. Vedi evaluation/preparazione_benchmark_glerean_arricchito_v1.md.
- [x] Confronto sperimentale con contesti arricchiti, 12 esecuzioni Qwen/Gemma; documentati errori residui di ruoli, movimenti e citazioni. Vedi evaluation/audit_glerean_enriched_v1.md.
- [ ] Valutare il miglioramento rispetto ai contesti non arricchiti con gold indipendenti, evitando conclusioni causali non dimostrate.
- [x] Progettare una rappresentazione offline delle figure con pagina, numero, ruoli, movimenti, canali di evidenza e grado di certezza: `evaluation/glerean_figure_evidence_v2.json` (13 figure/sottofigure). La validazione del formato su retrieval reale resta separata.
- [ ] Integrare e validare le evidenze delle figure nel retrieval senza modificare V4 prima di benchmark e rollback.

**Decisione architetturale 2026-10-20:** il sidecar Glerean resta esclusivamente gold offline, non componente della produzione. Piano generalizzabile con API native Docling e gate di validazione in `docs/piano_ingestion_multimodale_200_documenti_2026-10-20.md`. Nessun indice modificato.\n\n**Aggiornamento 2026-10-20:** audit fonte di 14 claim concluso in `evaluation/audit_gold_glerean_14_claims_2026-10-20.md`; tutte le figure dei due gold set sono state esaminate, e il sidecar v2 è stato registrato. I risultati non dimostrano ancora un miglioramento end-to-end del RAG.\n\n**Diagnosi:** la perdita di informazione nei chunk testuali spiega parte degli errori; altri persistono anche nei contesti arricchiti. Non attribuire ogni difetto al modello o esclusivamente al corpus.

## 5. Retrieval e reranking — H09

### H09 — Decisione BM25 e politica anti-componenti inutilizzati (2026-10-21)

- [x] Confrontare BM25, Qwen3-Embedding e fusione RRF sul medesimo corpus H09 (23 evidenze, 3 query di sviluppo); self-test RRF 3/3. Output VPS 2026-10-20, commit `25c33041b40995bbd671fdfd2db4023acfa7deaa`, evidence SHA-256 `25bba4d1540124bcd6df54ae54ffd3a526c15b2f8012688df86c46852c60b01b`.
- [x] Decisione provvisoria: Qwen3-Embedding candidato H09; BM25 **escluso dal percorso candidato**, mantenuto solo come baseline di valutazione. MRR BM25 0.696970, dense 0.833333, hybrid RRF 0.733333; nessuna conclusione da 3 query sul corpus completo.
- [ ] Validare il contributo BM25 su benchmark indipendente, casi negativi e fonti differenti; valutare qualità, latenza e costi senza ottimizzare sui tre casi di sviluppo.
- [ ] Se BM25 non offre beneficio dimostrato, censire riferimenti runtime, import, script, configurazioni e dipendenze; predisporre backup e rollback; **rimuovere componenti BM25 inutilizzati** senza lasciare codice morto. Conservare risultati e motivazioni in Git, senza toccare la baseline V4 prima della validazione.
- [x] Eseguire benchmark H09 read-only Qwen3-Embedding vs Qwen3-Embedding + mMARCO su 23 evidenze e 3 query di sviluppo: dense Hit@1 2/3, Hit@5 3/3, MRR 0.833333; dense+mMARCO Hit@1 3/3, Hit@5 3/3, MRR 1.0; figura 15/a rank 2→1. Report VPS `/tmp/h09_dense_mmarco.json`, commit `4b4122dcb25ee45bd5884e3eceea3f2c07c14a2b`, evidence SHA-256 `25bba4d1540124bcd6df54ae54ffd3a526c15b2f8012688df86c46852c60b01b`, sentence-transformers 6.1.0, mMARCO CPU max_length=512 batch=1, top-N=15, 22.538 s totali. Riferimenti ufficiali: https://www.sbert.net/docs/cross_encoder/usage/usage.html ; https://sbert.net/docs/package_reference/cross_encoder/model.html ; https://docs.ollama.com/api/embed . Risultato **solo esplorativo**, non validato su holdout né contro V4.
- [ ] Validare mMARCO su holdout indipendente e altre fonti, misurando anche truncation, latenza per query e impatto sulle evidenze prima di promuoverlo.
- [x] Preparare probe read-only H09 Qwen3-Embedding → mMARCO → Qwen3.5, con contesto/citazioni/provenienza e formato JSON; script `scripts/probe_h09_grounded_generation.py`, commit `9ee562d56d2779b20c853c107f0fd26f2b01688a`. API ufficiali Ollama: https://docs.ollama.com/api/chat e https://docs.ollama.com/capabilities/structured-outputs .
- [x] Eseguire probe generazione H09 sulla VPS: 3/3 risposte prodotte, 139.366 s complessivi, Qwen3.5 9B, report `/tmp/h09_grounded_generation.json`, commit `3769422e045c01696dbad5ee638d9523db0078d9`, evidence SHA-256 `25bba4d1540124bcd6df54ae54ffd3a526c15b2f8012688df86c46852c60b01b`. `VALID_IDS 0/3` è falso negativo del validatore per prefisso `FIGURA `: tutte le 8 citazioni puntano a figure effettivamente nel contesto dopo normalizzazione. Non equivale a fedeltà semantica.
- [x] Prima revisione manuale H09: domanda 1 corretta nel nucleo fig.15/a ma mescola situazioni fig.21 e fig.8; domanda 2 corretta ma sintetica fig.15/b,20; domanda 3 corretta nel nucleo fig.17 ma omette appoggio centrocampo/difesa e aggiunge casi fig.12,21. Valutazione preliminare, non benchmark certificato.
- [ ] Correggere il validatore citazioni con normalizzazione controllata e test unitari, senza riscrivere i risultati originali; impedire la confusione tra identificativi validi e supporto semantico.
- [x] A/B H09 prompt focalizzato con contesti identici e validatore citazioni normalizzato: report VPS `evaluation/reports/h09_generation_focus_ab.json`, 3/3 ID citazioni validi, test unitari 2/2. Audit: caso 1 migliorato (solo fig.15/a); caso 2 formulazione ambigua sul rapporto portiere/difensore non possessore; caso 3 recupera appoggi fig.17 ma continua a mescolare fig.12 e fig.21. Nessuna promozione V4, voto cumulativo 7/10 provvisorio.
- [ ] Testare filtro deterministico della condizione tattica prima della generazione (fase/zona/possessore), mantenendo recupero/reranking invariati; confrontare su stesse domande, registrare falsi scarti e omissioni. Evitare ottimizzazione soltanto sulle 3 domande development.
- [ ] Validare su holdout indipendente, fonti multiple e confronto controllato V4; nessun voto certificato prima di questi passaggi.

### H09 — Esito Top-1 e obiettivo multi-fonte (2026-10-21)

- [x] Eseguita ablation H09 Top-1 su 3 domande development; report utente `evaluation/reports/h09_top1_context.json` (VPS, non ancora versionato in Git). Risposte coerenti con fig. 15/a, 15/b e 17; ID citazioni 3/3 validi; durate di generazione circa 17.54 s, 16.08 s, 22.41 s. Non equivale a test holdout o ragionamento multi-documento.
- [ ] Confrontare Top-1 e Top-5 con **identico prompt focalizzato**, stessi modelli/parametri e gold di correttezza semantica; l'attuale report Top-1 confronta anche prompt diversi rispetto alla baseline originaria.
- [ ] Priorità di prodotto: DRIBBLING deve spiegare **principi, movimenti, tempi, cause e condizioni del calcio** integrando fonti indipendenti; Glerean/3-3-4 è un caso e una fonte, non l'obiettivo. Evitare sia il vincolo permanente Top-1 sia il collage indiscriminato Top-5.
- [ ] Preparare benchmark multi-documento con fonti Drive primarie indipendenti (es. Glerean, Foscarini, Ussia) e domande su movimenti/contesti; etichettare condizioni tattiche, contributi complementari, divergenze e provenienza. Escludere manuali FOOTBALL-DATA-LAB derivati come conferme indipendenti; conservare V4.

## 6. Generazione, citazioni e qualità RAG

### PRIORITÀ MASSIMA — Qualità scientifica e tattica delle risposte

**Obiettivo:** risposte fedeli, complete, correttamente attribuite e verificabili, non soltanto citazioni formalmente valide o codice senza errori. Questa priorità procede insieme all'audit architetturale, non dopo.

- [ ] Definire criteri di accettazione espliciti e distinti per: correttezza/fedeltà tattica, completezza dei nuclei essenziali, recupero delle evidenze, attribuzione autore/fase/ruolo/zona, validità semantica delle citazioni, capacità di astenersi se le fonti non bastano, latenza e riproducibilità.
- [ ] Consolidare i gold già presenti in evaluation/, distinguendo gold verificati, preliminari e controversi; non correggere i gold per far migliorare artificialmente i punteggi.
- [ ] Costruire un benchmark rappresentativo di domande reali e avversariali, con evidenze letterali e casi negativi; includere Q8, H05, H07, H09, H10 e altri casi già studiati, senza ripetere prove concluse.
- [ ] Valutare separatamente retrieval, reranking, contesto finale, generazione e citazioni per localizzare le cause degli errori.
- [ ] Eseguire audit claim-by-claim: fonte realmente pertinente, implicazione semantica, ruoli, fasi, zone, condizioni, completezza; una citazione numericamente valida non è prova di correttezza.
- [ ] Calibrare il giudice semantico su risposte RAG reali etichettate e casi difficili, distinguendo fedeltà e copertura; verificare disaccordi H05/H10 e falsi positivi prima di automatizzare l'accettazione.
- [ ] Confrontare framework di valutazione ufficiali Ragas e DeepEval con la soluzione custom in ambiente isolato, secondo versioni e API ufficiali; non assumere che il framework garantisca qualità.
- [ ] Definire policy di regressione: non promuovere un componente/configurazione che migliori una metrica ma peggiori errori tattici critici o citazioni.
- [ ] Eseguire prove su fonti e autori differenti, con domande non viste e documenti nuovi, per misurare generalizzazione e robustezza.
- [ ] Registrare per ogni benchmark dataset, commit, digest modelli, parametri, gold, metriche, errori, tempi, fonti ufficiali, esito e decisione; riutilizzare i risultati storici.
- [ ] Stabilire soglie di qualità motivate dai casi d'uso, poi certificare il superamento su holdout indipendente prima di dichiarare DRIBBLING pronto.

**Evidenze già disponibili, non da confondere con qualità validata:** audit Q8 TOP5/TOP10 (errori di attribuzione e omissioni), benchmark due assi fedeltà/completezza, holdout Glerean, diagnosi Ragas H07, metro tattico no-thinking (12/12 fedeltà, 10/12 copertura su piccolo holdout sintetico), gold JSON e report in evaluation/. Consultarli prima di lanciare nuovi test.

## 7. Classificatore NLI V2

### NLI V2 — avanzamento benchmark e prossimi gate (2026-10-21)

**Ambito:** classificazione claim→evidenza in tre etichette (supported / contradicted / insufficient). Questi risultati NON certificano la qualità end-to-end di DRIBBLING V5. V4 e indici restano invariati.

- [x] Congelare la variante sperimentale NLI V2 come candidato da confrontare, conservando V1 e prompt precedenti nel repository; non promuovere automaticamente in produzione.
- [x] Eseguire confronto V1/V2 sul benchmark di sviluppo da 24 claim: V1 22/24 (91,67%); V2 23/24 (95,83%), con supported 8/8, contradicted 8/8, insufficient 7/8. Evidenza: report benchmark comunicati in chat; verificare archiviazione dei JSON in Git prima di considerarli artefatti riproducibili.
- [x] Eseguire benchmark successivo da 32 claim su fonti FA: V2 30/32 (93,75%), supported 8/8, contradicted 12/12, insufficient 10/12. Gold non indipendentemente revisionato.
- [x] Eseguire stress test da 100 claim su estratti già utilizzati: V2 93/100 (93%), supported 28/30, contradicted 29/30, insufficient 36/40. **Non indipendente per fonte**; gold ancora da revisionare. Dataset: `eval/tactical_nli_stress_100_v1.json`.
- [x] Preparare un ulteriore test prospettico da 30 claim FIGC/FA: `eval/tactical_nli_source_disjoint_30_v1.json`. Due URL nuovi e un passaggio nuovo da URL già usato: **non completamente source-disjoint**.
- [x] Acquisire e analizzare il report del test FIGC/FA da 30 claim: 30/30 completati, zero errori di esecuzione; 29/30 (96,67%) accuratezza 3-way, 30/30 (100%) binaria. Errore unico `novel_fa_wide_new_04`: gold contradicted, previsione insufficient; estratto FA dice esplicitamente che la Germania supera la contropressione. Evidenza: report JSON `benchmark_tactical_nli_source_disjoint_30_v2.json` ricevuto in chat il 2026-10-21, non ancora archiviato nel repository. Tempo inferenza cumulativo 540,05 s; mediana 17,735 s/claim. Il test non è completamente source-disjoint e il gold non è revisionato indipendentemente.
- [ ] Revisionare indipendentemente le gold label, soprattutto quantificatori, numeri non documentati, negazioni e equivalenze semantiche; correggere eventuali ambiguità con motivazione e traccia.
- [ ] Validare su fonti integralmente nuove, documenti più lunghi e domande reali, senza ottimizzare il prompt sui casi di verifica.
- [ ] Archiviare report completi, versioni/digest modello, configurazione Ollama, commit, tempi e matrice di confusione per confronti riproducibili.
- [ ] Integrare V2 soltanto in modalità shadow/reversibile, dopo superamento dei gate; valutare fedeltà claim-by-claim, completezza, retrieval, citazioni e latenza sull'intera pipeline.
- [ ] Qualificare il sistema end-to-end con benchmark indipendente e confronto controllato con baseline V4; soglia NLI di laboratorio >=90% totale e per categoria NON equivale a certificazione RAG.

### Integrazione NLI V2 — contratto shadow (2026-10-21)

- [x] Identificare nel codice GitHub la pipeline candidata V5 (`smoke_test_rag_v5_e2e.py`) e il giudice NLI V2 (`benchmark_direct_three_label_nli_v2.py`), distinguendoli dall'entry point storico `ask_dribbling.py` che usa V1.
- [x] Definire un contratto shadow separato, senza modifiche alle risposte, agli indici o ai prompt, con rischi, fasi offline/replay/live e rollback: [docs/nli-v2-shadow-integration.md](docs/nli-v2-shadow-integration.md).
- [x] Implementare runner offline-first con claim atomici **annotati manualmente**, citazioni, più fonti e report separato (`scripts/shadow_nli_v2_offline.py`) e quattro test unitari (`scripts/test_shadow_nli_v2_offline.py`). Il prototipo locale ha superato 4/4 test; **i file pubblicati su GitHub non sono ancora stati eseguiti sulla VPS/CI**. Nessuna estrazione automatica claim o chiamata NLI integrata.
- [x] Implementare adapter NLI V2 opt-in su coppie claim–evidence, con prompt e schema V2 invariati, output separato e gestione errori conservativa (`scripts/shadow_nli_v2_inference.py`). Aggiunti test con giudice simulato (`scripts/test_shadow_nli_v2_inference.py`). **Non ancora eseguiti su VPS/CI; nessuna inferenza reale validata.**
- [ ] Verificare l'esito reale della suite offline su GitHub Actions (`.github/workflows/tactical-shadow-nli-offline.yml`): workflow pubblicato, test ancora **non confermati PASS**. Il runner NLI legge il prompt canonico V2 via AST, evitando dipendenze RAGAS nella suite offline; test aggiuntivo sul prompt pubblicato. Non dichiarare 9/9 PASS prima di ottenere il log.
- [ ] Validare estrazione dei claim e associazione semantica alle fonti su gold indipendente, prima di qualsiasi hook nel generatore.
- [ ] Eseguire shadow isolato su VPS solo dopo gate documentali, gold e audit runtime; misurare latenza end-to-end e risorse.

## 8. Validazione end-to-end e confronto V4/V5

**Gate end-to-end (nuova checklist trasversale):** le attività dettagliate restano nelle sezioni di qualità, baseline e NLI; questa sezione raccoglie le condizioni di promozione.

- [ ] Definire e congelare il set di domande reali e avversariali con gold indipendenti e fonti documentali, incluse figure tattiche.
- [ ] Misurare separatamente retrieval, reranking, generazione, fedeltà claim-by-claim, copertura dei nuclei essenziali, citazioni semantiche, astensione e latenza.
- [ ] Confrontare baseline V4 e candidata V5 sulle stesse domande e sugli stessi criteri, preservando collection e configurazioni originali.
- [ ] Documentare esito, regressioni critiche, rollback, commit, digest, versioni e decisione finale prima di qualsiasi promozione.

## 9. Pulizia, dismissioni e consolidamento

### 4. Pulizia del codice e Git

- [x] Verificata nel repository la presenza di **40 script Python** in `projects/tactical-engine/scripts/` (inventario GitHub; non prova di utilizzo sulla VPS).
- [ ] Classificare ciascuno script: operativo, baseline, test riproducibile, sperimentale, storico, inutilizzato o stato incerto. **Inventario statico storico disponibile** in docs/script-inventory.md; resta da classificare l'utilizzo reale e gli script aggiunti.
- [x] Mappare staticamente import e riferimenti incrociati degli script Python su GitHub (40 script, CI verde); **invocazioni esterne e runtime VPS ancora da verificare**.
- [ ] Progettare struttura ordinata (`src/`, `config/`, `tests/`, `experiments/`, `archive/`, documentazione), adattandola alle dipendenze reali.
- [ ] Centralizzare configurazioni ripetute e documentare entry point ufficiale, senza introdurre nuove differenze di comportamento.
- [ ] Consolidare funzioni duplicate solo con test di regressione e rollback.
- [ ] Archiviare prima di eliminare; Git conserva lo storico del codice ma NON sostituisce backup di database, PDF o modelli.
- [ ] Controllare `.gitignore`, inclusa regola `*.txt`, per evitare esclusioni involontarie di test/requisiti e inclusione di dati pesanti o segreti.
- [ ] Aggiungere README tecnico, inventario, decision log e procedura riproducibile di esecuzione/valutazione. **Parziale:** README, inventario, decision log, checklist runtime e protocollo verifiche già presenti; riproducibilità end-to-end da completare.

### 5. Dismissione componenti scartati e pulizia dati

- [ ] Identificare modelli Ollama dismessi e verificare che non siano referenziati da script, servizi, test da mantenere o procedure di rollback.
- [ ] Identificare pesi di embedding/reranking in cache non più necessari, distinguendo cache condivise e dipendenze indirette.
- [x] Verifica statica preliminare Alibaba nella seconda PuTTY: nessuna corrispondenza nelle estensioni controllate in `projects/tactical-engine`; `gte-multilingual-reranker-base` ~600 MB, `new-impl` ~92 KB seguendo i link simbolici. **Solo candidato alla rimozione:** prima occorrono controllo servizi/progetti esterni, dipendenze dinamiche, backup e rollback.
- [x] Estendere la ricerca statica Alibaba all'intero repository tracciato con `git grep -n -i -E 'Alibaba-NLP|gte-multilingual-reranker|new-impl' -- ':!*.lock' ':!*.jsonl' | head -40`: **nessuna corrispondenza** (output seconda PuTTY, 2026-10-21). Il controllo esclude file non tracciati, `.lock`, `.jsonl`, riferimenti dinamici e servizi esterni; non autorizza la rimozione.
- [ ] Identificare dipendenze Python inutilizzate senza rimuovere dipendenze transitive necessarie.
- [ ] Identificare collection ChromaDB obsolete e verificare assenza di riferimenti attivi.
- [ ] Identificare processi/servizi/cron dismessi e possibili consumi di risorse.
- [ ] Identificare cache, file temporanei, output duplicati e indici rigenerabili.
- [ ] Prima della rimozione: inventario → prova di non utilizzo → backup/rollback → approvazione → rimozione controllata → verifica post-rimozione.
- [ ] Misurare spazio, RAM/VRAM e prestazioni prima/dopo; distinguere risparmio disco da liberazione di memoria.
- [ ] Non eliminare PDF sorgenti, dati di knowledge base, gold set o baseline senza esplicita autorizzazione.

## 10. Registro storico delle verifiche

### Evidenze recuperate il 2026-10-20 (senza ripetere controlli VPS)

- **Inventario software/hardware 2026-10-19:** Python sistema 3.12.3, venv individuata, Docling 2.140.0, ChromaDB 1.5.9, LlamaIndex core 0.14.25, Ollama server 0.40.5, VPS CPU-only con 6 vCPU e 15 GiB RAM. Fonte: docs/environment.md, output CLI precedentemente riportati dall'utente; non riconfermati oggi.
- **Collection V3/V4 già controllate:** 86 record ciascuna; V3 cosine/768D, V4 L2/1024D; V4 normalizzata. Fonte: docs/status-2026-10-19.md. Non ripetere senza cambio indice o evidenza di problema.
- **EXP-001 già concluso:** query instruction Qwen3 Embedding 0.6B peggiora MRR provvisorio (0,6354 → 0,4688 su 8 query) senza migliorare recall@15 (1,0); conservare baseline senza instruction per questo set. Fonte: docs/status-2026-10-19.md; gold provvisori.
- **Test Q8 TOP5/TOP10 già eseguito:** errori semantici di attribuzione delle citazioni, latenza 214,6 s vs 276,8 s. Non confondere validità numerica e correttezza tattica.
- **Benchmark giudice no-thinking già eseguito:** 12/12 fedeltà, 10/12 completezza su piccolo holdout sintetico; due casi da riesaminare, non certifica qualità end-to-end. Fonte: evaluation/analisi_metro_tattico_no_think_v1_2026-10-20.md.
- **CI:** workflow statico e test offline già esistenti; ultimo run #46 verificato success, non prova runtime VPS.
- **Inventario script:** il precedente conteggio di 36 è storico; il repository attuale contiene molti più script e test. Non riutilizzare quel numero come censimento corrente.

### Stato delle verifiche

- **Verificato sul repository GitHub:** esistono pipeline e test V1–V5; 36 script Python; V3 usa tokenizer Nomic e V4 Qwen reindicizza gli stessi testi; alcuni gold del benchmark reranker sono provvisori; la validazione V5 delle citazioni non garantisce correttezza semantica.
- **Verificato sulla VPS (output CLI, riepilogo 2026-10-19):** commit/branch e working tree, Python sistema e venv presente, pacchetti Python principali, `pip check`, 6 vCPU KVM AMD EPYC, RAM/swap e `vmstat` a riposo, VGA virtuale QEMU, Ollama server 0.40.5, modelli installati e dettagli `ollama show`, nessun modello caricato al controllo. Evidenze in `docs/environment.md`. **Non ripetere senza variazioni dell'ambiente.**
- **Seconda sessione PuTTY (2026-10-21), verificato da output CLI:** `df -hT` root ext4 58 GB, 27 GB utilizzati, 31 GB disponibili (48%); progetto 3,6 GB, cache Ollama 7,0 GB, cache utente 5,2 GB (Hugging Face 5,0 GB; pip 259 MB); 11 repository HF censiti; Alibaba GTE 600 MB reali con `du -shL`, `new-impl` 92 KB. `grep` statico nei file Python/YAML/JSON/TOML del motore tattico senza riferimenti ad Alibaba. **Alibaba candidato alla dismissione, NON autorizzato alla rimozione.** Tutto documentato in `docs/environment.md`; nessuna cancellazione o modifica VPS.
- **Ancora da verificare sulla VPS:** entry point e processi/servizi effettivi, collection e record Chroma, mappatura dipendenze runtime/esterne dei modelli in cache, dimensioni reali degli altri singoli modelli, backup e configurazioni runtime.
- **Da completare:** confronto puntuale con documentazione ufficiale aggiornata e changelog delle versioni installate.

> Aggiornare le checkbox solo dopo una verifica concreta, annotando evidenze e data. Non considerare una proposta come lavoro completato.

### Audit dipendenze script — preparato 2026-10-19

- [x] Creare scanner statico standard-library `scripts/audit_script_dependencies.py` per import locali, menzioni collection/modelli, API private, possibili scritture ed errori sintattici. **Codice creato, non eseguito sulla VPS**.
- [ ] Eseguire scanner su snapshot codice effettivo e salvare output revisionato senza segreti.
- [ ] Incrociare grafo statico con processi, cron, systemd e invocazioni esterne della VPS; classificare attivo / sperimentale / storico / candidato rimozione.
- [ ] Solo dopo approvazione e backup, consolidare o archiviare componenti inutilizzati; nessuna cancellazione anticipata.

- [x] Censire **tutti gli script Python presenti su GitHub** per ruolo, collection, modelli, scritture e dipendenze note: `docs/script-inventory.md`. **Inventario statico completato; utilizzo reale e removibilità NON verificati.**

### Esito verificato GitHub Actions — 2026-10-19

- [x] Creato controllo CI `.github/workflows/tactical-engine-static.yml`: compilazione di tutti gli script, test unitari offline con moduli simulati e verifica inventario AST.
- [x] Esecuzione CI **PASS**: 40 script compilati, 4 test unitari passati, nessun errore sintattico rilevato. Run: https://github.com/giampiero1975/footbal-data-lab/actions/runs/39216515588 (commit `7b83ac8`).
- [x] Corrette le sequenze di escape che rendevano non valido `audit_v4_runtime.py`; il CI ha verificato la correzione.
- [x] EXP-001: preflight directory DB, fonti, ID gold e filtro per fonte, alternanza ordine A/B, Q8 senza gold esclusa da recall/MRR. **Test funzionale con Chroma/Ollama reali ancora da eseguire.**
- [ ] Confrontare VPS e GitHub, rilevare entry point e stato dei servizi, snapshot e backup della baseline.
- [ ] Eseguire audit Chroma V3/V4 sulla VPS e interpretare configurazione metrica e norma dei vettori.
- [ ] Validare semanticamente gold, eseguire EXP-001, benchmark reranker e verifiche citazioni/latency con output versionati.
- [ ] Scegliere configurazione definitiva in base ai risultati, quindi consolidare/archiviare soltanto componenti provati inutilizzati. **Nessuna rimozione autorizzata prima di queste verifiche.**


## Aggiornamento shadow NLI — 2026-10-22

- [x] Rafforzato il controllo fail-closed delle annotazioni shadow: il testo della claim deve corrispondere allo span della risposta al netto delle citazioni, e gli offset booleani sono rifiutati; aggiunto test di regressione (commit `815878c`, `cb2dd68`).
- [x] Aggiornato trigger GitHub Actions shadow per includere modifiche al prompt NLI V2 canonico (commit `483c5cf`).
- [x] Verificato dai log GitHub Actions il PASS della suite shadow aggiornata: **10/10 test OK**, Python 3.12, commit `dfb07e40`, run `39750873565` (2026-10-22). Verifica esclusivamente offline; nessuna inferenza Ollama né E2E RAG certificati.

### Verifica runtime VPS shadow NLI e RAG V5 — 2026-10-22
- **Riportato da output PuTTY:** VPS inizialmente indietro di 30 commit rispetto a `origin/main`; `git fetch origin main` eseguito e successivo `git pull --ff-only` riferito come completato. Prima del pull risultavano 5 file tracciati eliminati localmente (README, tre TODO tematici e `todo.md`), oltre a virtualenv e report benchmark non tracciati. Non è ancora stato riesaminato lo stato post-pull: preservare gli artefatti locali.
- **Inferenza NLI V2 reale su Ollama, output PuTTY:** `supported` corretto in 20,38 s; `contradicted` corretto in 21,82 s; `insufficient` corretto in 11,95 s. Totale **3/3 casi dimostrativi**, media 18,05 s. È uno smoke test funzionale, **non** un benchmark di accuratezza né una verifica della fedeltà RAG.
- **RAG V5 non ancora eseguito:** ricerca `find` di report `*v5*json`/`*e2e*json` sotto `projects/tactical-engine` senza risultati. Lancio di `scripts/smoke_test_rag_v5_e2e.py` con `.venv-ragas-eval/bin/python` interrotto immediatamente da `ModuleNotFoundError: No module named 'chromadb'`; nessuna inferenza RAG o modifica Chroma effettuata.
- **Ambienti Python verificati tramite `find` su VPS:** `projects/tactical-engine/.venv-ragas-eval/bin/python` e `projects/tactical-engine/.venv/bin/python` (Python 3.12, inclusi collegamenti `python3` e `python3.12`). La prima ricerca `find -type f` non rilevava i symlink; corretta includendo `-type l`. **Da verificare** in `.venv` la disponibilità di `chromadb`, `llama_index.embeddings.ollama` e `sentence_transformers` prima di installare pacchetti.
- **Prossimo gate:** controllo import in `.venv`; solo dopo, smoke RAG V5 con report separato e shadow su claim annotati, mantenendo V4/V5 e Chroma invariati.

- **Gate dipendenze RAG V5 superato (output PuTTY):** l'interprete `projects/tactical-engine/.venv/bin/python` importa correttamente `chromadb` (versione **1.5.9**), `llama_index.embeddings.ollama.OllamaEmbedding` e `sentence_transformers.CrossEncoder`. Nessun pacchetto installato; lo smoke test V5 resta da eseguire con questo interprete.
