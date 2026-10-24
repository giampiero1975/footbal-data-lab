# DRIBBLING V5 — Piano operativo, checklist e registro delle evidenze

> **Documento di riferimento operativo** · Riconciliato il 2026-10-23 · Repository: `giampiero1975/footbal-data-lab` · Ambito: `projects/tactical-engine/` e VPS `/opt/football-data-lab`.
>
> **Attenzione:** una casella spuntata documenta l'attività descritta, non la certificazione dell'intero RAG. I risultati riportati come comunicati dalla VPS non equivalgono a un accesso diretto dell'assistente alla VPS. Preservare baseline V4, indici e configurazioni prima di qualunque intervento.

## Stato operativo corrente — 2026-10-23

**Fonte autorevole:** [Registro esperimenti](docs/experiment-register.md). Prima di proporre un test, consultare attività → script → commit → report → risultato → decisione → stato. Nessun rerun equivalente senza una motivazione tecnica registrata. **VALIDATO shadow non significa INTEGRATO né CERTIFICATO.**

### P0 — Uniche attività residue per chiudere il filone exact-reference V5

- [x] Recupero e generalizzazione dei riferimenti esatti, reranking e replay di priorità su quattro casi nuovi; commit `21cdb18`, `547da5c`, `eaad637`, `3d10d7f`, `b570abd`.
- [x] Analizzato report `rag_v5_reference_priority_shadow_v1.json` (2026-10-23): fig.9 F5→F1, Ussia 6/B F1+F2, Ussia 4/B F1, fig.20 F1; invariati gli ID top8 e nessun accesso Chroma.
- [x] Analizzata nuova risposta figura 20: distingue scambio 4/3, movimento 7 e copertura 6; una lieve ambiguità nell'attribuzione dell'incrocio resta da sorvegliare in regressione. Esito **VALIDATO solo shadow mirato**.
- [x] Implementare priorità controllata **opt-in** nel percorso di retrieval live source-aware (`rag_v5_fresh_reference_e2e_shadow_v1.py --priority-exact`, commit `bbb9b7b`); **IMPLEMENTATO**, non ancora VALIDATO runtime né INTEGRATO nel candidato locked/produzione. Rollback: omettere il flag.
- [ ] Validare runtime la priorità opt-in, poi decidere l'eventuale integrazione nel candidato V5 effettivo; non modificare il candidato locked senza evidenza.
- [ ] Eseguire **una sola verifica mirata non duplicativa** sul nuovo flag live (differenza rispetto al replay offline già validato), inclusa la figura 20; registrare report, digest e decisione.

- [x] **IMPLEMENTATO parzialmente** flag `--priority-exact` nel runner effettivo `smoke_test_rag_v5_e2e.py`, commit `a0301b6`, default off; nessun report runtime di questa nuova modifica.
- [x] **IMPLEMENTATO** inoltro opt-in del flag dal wrapper `run_rag_v5_locked_candidate_v2.py` al runner V5, commit `2a2ceb9`; default invariato e rollback omettendo il flag.
- [x] **VALIDATO** probe retrieval-only nel runner effettivo: Foscarini figura 20 F1, 5319→5319, nessuna generazione; commit `a8cfef6`, report `rag_v5_effective_priority_probe_v1.json`, SHA-256 `e52c802051873703c197e8b28123a580a3b56a2268a2309b11e4d5f764f6bbda`. Preflight wrapper superato; non è test E2E del wrapper.
- [ ] **DA FARE** decisione su integrazione E2E del wrapper opt-in e valutazione qualità risposta, senza ripetere benchmark gold.

### P1 — Gate distinti dalla chiusura del retrieval

- [x] ESEGUITO: audit autore delle 10 domande fresh_01–fresh_10 il 2026-10-22 (source_claim_audit e coverage_audit nel candidato v2); non ripetere.
- [x] Revisione indipendente e freeze del candidato gold V5 già preparato (commit `641f61e`, audit `db9abab`); non rigenerare un gold equivalente. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.
- [x] IMPLEMENTATO: protocollo di revisione indipendente `docs/rag-v5-independent-review-gate-v1.md` (commit `0c79578`); candidato invariato.
- [x] IMPLEMENTATO: client Gemini separato `scripts/review_rag_v5_gemini.py` (commit `ca8383b`), guida `docs/gemini-independent-review-v1.md` (`25ef94d`), esclusione materiale privato (`24e8ac6`); nessun benchmark eseguito.
- [ ] DA FARE: acquisire estratti originali verificati Ussia pagine 21–23 e predisporre bundle privato per `fresh_01`; poi preflight e una richiesta Free Tier autorizzata.
- [x] ESEGUITO: freeze e certificazione V5 in attesa di revisore indipendente e fingerprint runtime. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.
- [x] Certificazione E2E 9/10 con blind adjudication e confronto controllato V4/V5. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.
- [ ] Completare gate NLI V2 e l'eventuale integrazione shadow, riutilizzando i benchmark esistenti.

### P2 — Manutenzione e pulizia

- [ ] Riconciliare inventario runtime, report VPS non versionati, dipendenze e classificazione degli script.
- [ ] Consolidare soltanto dopo test reversibili, backup e autorizzazioni necessarie.

## Archivio storico e checklist dettagliate

Le sezioni seguenti preservano la storia tecnica. Le caselle non aggiornate nelle sezioni storiche **non costituiscono una seconda lista operativa**: il piano attivo è quello sopra, con stato puntuale nel registro. Non rieseguire attività storiche senza identificare una nuova differenza tecnica.

## Come usare questo documento

1. **Prima di lavorare:** leggere le regole nella sezione 1 e la fotografia dell'ambiente in [docs/environment.md](docs/environment.md), [docs/components.md](docs/components.md), [docs/decisions.md](docs/decisions.md) e [docs/verification.md](docs/verification.md).
2. **Per scegliere il prossimo lavoro:** seguire le priorità qui sotto e le dipendenze; non ripetere verifiche già documentate senza una modifica effettiva.
3. **Per chiudere una voce:** annotare fonte ufficiale/versione, commit o report, risultato, limiti, decisione e rollback quando applicabile. `[x]` = evidenza registrata; `[ ]` = aperta o non ancora certificata.
4. **Per i benchmark:** distinguere *development*, *stress test con fonti riutilizzate*, *holdout prospettico*, *gold revisionato* e *validazione end-to-end*. Un risultato NLI non equivale alla qualità del RAG completo.
5. **Per la VPS:** il repository non dimostra lo stato runtime corrente; utilizzare soltanto controlli mirati ai dati mancanti o cambiati.



### Chiusura campagna diagnostica V5 — 2026-10-22
- [x] Campagna diagnostica V5 chiusa e registrata in [docs/rag-v5-test-campaign-closure-20261022.md](docs/rag-v5-test-campaign-closure-20261022.md), commit `647fb85`.
- [x] Report prospettico 10/10 generazioni, 0 ID citazioni invalidi, indice 5319→5319; valutazione qualitativa preliminare 9/10, **non PASS gold**. Domanda 02 contestata nella formulazione; non attribuire automaticamente il difetto al modello.
- [x] Nessun rerun di diagnostici o vecchi holdout: conservare come regressione.
- [x] Certificazione **separata**: gold indipendente con pagine/claim/revisore e SHA congelati prima del run; singolo benchmark nuovo, adjudication in cieco, confronto V4/V5, decisione finale. Non dichiarare questi check chiusi senza evidenza. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.

### Aggiornamento Passage Shadow V1 — 2026-10-22
- [x] Analizzato report `rag_v5_phase_passage_shadow_v1.json` (holdout_06 e holdout_10, citazioni ID invalide 0/2).
- [x] Registrata revisione qualitativa e limiti in [docs/rag-v5-phase-passage-shadow-v1-review-20261022.md](docs/rag-v5-phase-passage-shadow-v1-review-20261022.md).
- [x] Completata revisione atomica **mirata, non indipendente** di 06/10: [docs/rag-v5-phase-passage-atomic-adjudication-20261022.md](docs/rag-v5-phase-passage-atomic-adjudication-20261022.md). 06 REVIEW; 10 FAIL semantico.\n- [ ] Adjudication **indipendente** su nuovo gold, confronto con ablation/baseline e regressione separata; non promuovere V5 sulla sola analisi shadow.
- [x] Definito gate prospettico e distinta valutazione NLI da qualità end-to-end: [docs/rag-v5-quality-prospective-grounding-gate-20261022.md](docs/rag-v5-quality-prospective-grounding-gate-20261022.md).
- [x] Create 10 domande candidate nuove: [evaluation/rag_v5_prospective_holdout_candidate_v1.json](evaluation/rag_v5_prospective_holdout_candidate_v1.json).\n- [x] Creato gate di validazione manifest: [scripts/validate_rag_v5_prospective_manifest_v1.py](scripts/validate_rag_v5_prospective_manifest_v1.py).\n- [ ] Associare fonti e pagine effettivamente verificate, claim obbligatori e revisore indipendente; congelare il manifest soltanto dopo il gate. Nessuna esecuzione o punteggio prima del gold.
- [ ] Consultare documentazione ufficiale delle API coinvolte prima di nuovi test implementativi; V4 e Chroma invariati.

### Priorità storiche (2026-10-21; sostituite dal piano corrente)

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
- [x] Revisionare indipendentemente le gold label, soprattutto quantificatori, numeri non documentati, negazioni e equivalenze semantiche; correggere eventuali ambiguità con motivazione e traccia. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.
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
- [x] Validare estrazione dei claim e associazione semantica alle fonti su gold indipendente, prima di qualsiasi hook nel generatore. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.
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

### Benchmark prospettico RAG V5 — 2026-10-22
- [x] Dieci domande candidate associate a fonti; corrette premesse non documentate e riferimenti incongrui (`evaluation/rag_v5_prospective_holdout_candidate_v1.json`).
- [x] Manuali FOOTBALL-DATA-LAB riconosciuti come fonti ufficiali interne complementari; provenienza distinta da fonti federali e tesi esterne.
- [x] Creato runner `scripts/run_rag_v5_prospective_holdout_v1.py` e corretto import anticipato di Chroma (`022f0c4`).
- [x] Aggiunta modalità `--diagnostic` per eseguire candidate senza falsificare il gate gold (`613cd45`).
- [ ] Eseguire sulla VPS in `.venv` il diagnostico E2E con output JSON nuovo; preservare collezione V5 e baseline V4.
- [x] Verificare pagina precisa per tutte le fonti, gold atomici e revisione indipendente; solo dopo congelare manifest e misurare PASS/10. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.
- **Non attestato:** 9/10 end-to-end. I test diagnostici non sono holdout certificati.


## Appendice — aggiornamenti preesistenti del 2026-10-22 (conservati)

### Audit copertura gold V5 (2026-10-22)
- [x] Audit copertura delle 10 domande nuove: inclusi blocco basso, cambio modulo in gara, zone di recupero, multisorgente e astensione; candidate v2 aggiornato (commit `db9abab`).
- [x] Verifica puntuale claim→testo di tutte le domande da revisore indipendente; non dichiarare reviewer inesistente. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.
- [ ] Freeze del gold prima di qualsiasi run; versione runtime e hash da registrare.
- [x] Run read-only VPS V5, blind adjudication e confronto V4/V5; nessun accesso remoto alla VPS disponibile negli strumenti connessi. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.


### Nuovo candidato certificazione V5 (2026-10-22)
- [x] Creato `evaluation/rag_v5_independent_candidate_v2.json` (commit `641f61e`): 10 nuove domande con fonti/pagine verificate direttamente su Drive, criteri obbligatori/vietati; nessun output del RAG generato su questi quesiti.
- [x] **Non ancora gold**: revisione indipendente, controllo copertura richiesta (inclusi casi multisorgente e cambio modulo), freeze SHA e configurazione prima di generare. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.
- [ ] Esecuzione V5 read-only su VPS, revisione in cieco, confronto V4 e decisione 9/10. Il connettore GitHub non offre accesso SSH alla VPS; non segnare test eseguiti.


### Priorità riferimenti esatti V5 — verifica VPS 2026-10-23
- [x] **VALIDATO** retrieval live source-aware con flag `--priority-exact`, script `scripts/rag_v5_fresh_reference_e2e_shadow_v1.py`, commit `bbb9b7b`. Report `rag_v5_live_priority_integration_v1.json` (allegato chat, non ancora archiviato Git), SHA-256 `0503e2dcc94be563a7176f0768b869360a6a2465411d4e454688f06fa21512fc`. Ussia 4/B F1→F1, Ussia 6/B F1+F5→F1+F2, Foscarini fig9 F5→F1, fig20 F1→F1. Tutti i top8 preservati come insieme; Chroma 5319→5319, zero scritture, zero generazioni.
- [ ] **DA FARE** verificare la correttezza della risposta generata per fig20 con evidenza specifica (il report live non genera risposte); non ripetere retrieval/benchmark già validati.
- [ ] **DA FARE** identificare e aggiornare l'entry point V5 effettivo, dopo regressione controllata e rollback. La modalità opt-in shadow è VALIDATA, **non INTEGRATA** nel candidato locked/produzione; V4 e indice invariati.

### V5-REF-07 — Risposta generata runner effettivo
- [x] IMPLEMENTATO: abilitata domanda singola con generazione nel runner effettivo, commit `00c3a77`.
- [x] ESEGUITO: risposta figura 20 acquisita; F1 e citazione corretti, Chroma invariato; attribuzione del ruolo al giocatore 7 non supportata.
- [x] IMPLEMENTATO: correzione prompt per ruoli e soggetti, commit f22ade7.
- [x] VALIDATO: verifica differenziale figura 20 con prompt modificato, report `rag_v5_effective_priority_answer_fig20_promptfix_v1.json`, SHA-256 `d2d071ca77ec43b9132fff19a553f191d0e19f17129466f1a715eafb1e81f05a`; corretto ruolo 7, F1 valido, Chroma 5319 invariato. Restano digressioni F2/F4 non richieste; nessuna certificazione E2E.

### V5-GEM-01 — Revisione indipendente Gemini
- [x] **ESEGUITO** estrazione Ussia originale pp. 21–23: bundle privato `evaluation/fresh_01_sources.json`, PDF SHA-256 `6aa542e55dc88527c4d47c0e7696bb8872c71ee262120509e7dbc0fd2e683772`; registro `19aff49`.
- [x] **IMPLEMENTATO** import `pymupdf` al posto di `fitz`, commit `34ba249`.
- [x] **VALIDATO** preflight locale `fresh_01` PASS, manifest e bundle SHA256 verificati, blind=true, zero richieste API; registro commit `eca6203`.
- [x] **ESEGUITO** un tentativo Gemini `fresh_01` (ledger 2026-10-23: 1), report `gemini_fresh_01_review_v1.json`: **BLOCCATO** per `UNVERIFIABLE_QUOTE`, nessun verdetto tattico; registro `1e1577b`.
- [x] **IMPLEMENTATO** persistenza risposta grezza e diagnosi puntuale delle citazioni senza allentare il gate; commit `16b5a08`, `9cc3a53`, registro `fd7a8d7`.
- [x] **IMPLEMENTATO** test regressione offline citazioni e report diagnostico, commit `3aefe66`, registro `126151a`.
- [x] **VALIDATO** test diagnostico offline sulla VPS, conferma utente di esito positivo, API_REQUESTS=0; registro `f51e118` (verifica sintetica, non end-to-end API).
- [x] **ESEGUITO** seconda richiesta Gemini `fresh_01` v2, ledger=2, `raw_review.decision=PASS`, ma validatore **BLOCCATO** su ellissi nella citazione; registro `32c8d63`.
- [x] **IMPLEMENTATO** audit offline delle citazioni con frammenti letterali ordinati e ellissi esplicite, commit `6a6a4c2`.
- [x] **VALIDATO** audit documentale fresh_01 v2: 9/9 evidenze, Gemini PASS, zero API; registro b24d0a3. Freeze globale **BLOCCATO**.
- [x] **ESEGUITO** riconciliazione fresh_02-fresh_10: nessuna revisione indipendente verificata nel registro; fonti Drive accessibili; registro ac98eab.
- [x] **IMPLEMENTATO** script bundle offline per fresh_02-fresh_10 (7ad9ee6; registro c686bb7).
- [x] **ESEGUITO** preflight VPS: BLOCCATO su Foscarini pagina stampata 22, PDF di 11 pagine.
- [x] **IMPLEMENTATO** mapping esplicito indice PDF Foscarini, commit fba8b96, registro 5cf8f57.
- [x] **VALIDATO** mapping Foscarini p22 = PDF 2 (b45d01f).
- [x] **ESEGUITO** nove bundle generati offline, zero API; registro d9b07b6.
- [x] **ESEGUITO** audit 9/9; correzione fresh_09 IMPLEMENTATO (c3df934).
- [x] **VALIDATO** fresh_09 pagina 3: bundle aggiornato e verificato, backup conservato, zero API.
- [x] **IMPLEMENTATO** reviewer fresh_02-fresh_10 `954cfd4`; registro `39fe1c3`.
- [x] **VALIDATO** SHA manifest e dry-run fresh_02 sulla VPS; registro `0cd26ce`, zero API.
- [x] **ESEGUITO** riconciliazione ledger: fresh_01 v1/v2 BLOCCATO su citazioni; v2 risposta Gemini confermata, registro `c978e9e`.
- [ ] **BLOCCATO** fresh_02: tentativo HTTP 503, ledger=3, registro a114e90; report v1 conservato.
- [x] **ESEGUITO** revisione indipendente dei casi residui. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.

- [x] **VALIDATO** REQ-GEM-01 per skip budget su VPS (`57c5692`, `30fdeeef`), report fresh_03, registro `b9e2427`; HTTP 503 runtime DA FARE: indisponibilita Gemini non interrompe il flusso operativo, skip tracciato senza PASS implicito (protocollo `222fdac`, registro `08ed219`).
- [ ] **DA FARE** implementare REQ-GEM-02: controllo preliminare leggero e contabilizzazione delle chiamate di prova, senza retry automatici; validare con test differenziale offline.

- [x] **VALIDATO** riscontro AI Studio: Free Tier Gemini 3 Flash 3/20 RPD, errore HTTP 503; registro `93af115`.
- [x] **VALIDATO** preflight locale quota Pacific read-only (`1456abf`), VPS 3/20, zero API; registro `d553188`.
- [x] **VALIDATO** contatore Pacific nel revisore principale (`ad08e57`); preflight VPS ESEGUITO 3/20, rollover offline 5/5 VALIDATO, zero API (registro `840639d`).

- [x] **VALIDATO** test differenziale offline rollover Pacific e migrazione UTC (`dfc4f37`), VPS 5/5, ledger reale invariato, zero API; registro `840639d`.

- [x] **VALIDATO** hash SHA-256 manifest gold candidato V5 su GitHub e VPS (`c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71`); protocollo corretto `553f050`, registro `5498948`. Manifest invariato; revisione indipendente e freeze BLOCCATO.

- [x] **VALIDATO** revisione tecnico-documentale interna rubriche V5; non equivale a revisione indipendente (`b4dbaf7`).
- [x] **IMPLEMENTATO** allineamento SHA wrapper al manifest verificato (`2090c10`); verifica VPS DA FARE.
- [x] **ESEGUITO** fingerprint statico parziale runner V5 su output VPS (`b4dbaf7`); fingerprint runtime completo DA FARE.

- [x] **VALIDATO** risorse VPS V5 e hash script, senza generazione; registro `65ffe1e`. Nessuna ripetizione richiesta. Commit HEAD VPS non acquisito; freeze BLOCCATO.

- [x] **ESEGUITO** riconciliazione offline report E2E V5 gia prodotto: 4/10 su mandatory gold, non 9/10 (`96fdc9b`). Nessuna nuova inferenza. Interventi mirati DA FARE; certificazione BLOCCATO.

- [x] **ESEGUITO** diagnosi top8 dei dieci casi E2E esistenti, report `docs/rag-v5-e2e-failure-analysis-2026-10-23.md` (`374c2cd`), registro `f0d4272`. Nessuna nuova generazione.
- [x] **IMPLEMENTATO** delta tecnico source-aware opt-in nel runner V5 (`9170f83`, correzione `aa2586e`); resta **DA FARE** la verifica di pertinenza 4/A e degli altri gap, senza ripetere shadow V5-REF-05.

- [x] **IMPLEMENTATO** source-aware opt-in nel runner e wrapper V5 (`9170f83`, `03a5e0f`), read-back GitHub confermato, registro `c6a2ce1`. Default invariato; nessun benchmark ripetuto.
- [x] **ESEGUITO** test differenziale mirato del flag --source-aware sulla VPS per Ussia 4/A; risultato nel registro V5-SOURCE-AWARE-DIFF-03 (`5a3a0bf`); fingerprint runtime completo resta **DA FARE**. Valutazione holdout nuovo e revisione indipendente **DA FARE**; certificazione **BLOCCATO**.

- [x] **ESEGUITO** differenziale VPS source-aware iniziale: baseline e flag top8 identici, source_hint null, indice 5319 invariato; difetto regex identificato, registro `cd29d2a`.
- [x] **IMPLEMENTATO** correzione regex boundary autore in runner (`aa2586e`), verifica VPS successiva DA FARE.
- [x] **ESEGUITO** differenziale mirato dopo pull di `aa2586e`: fonte riconosciuta, 2/8 chunk Ussia (F3 pp. 15-16, F8 pp. 35-37) contro 0/8 baseline, indice invariato; registro V5-SOURCE-AWARE-DIFF-03 (`5a3a0bf`).
- [ ] **DA FARE** individuare il contenuto esatto di Ussia figura 4/A (F3 riguarda 4/B; F8 riguarda esercizio 19), senza ripetere benchmark. Sistema non INTEGRATO né CERTIFICATO.

- [x] **ESEGUITO** V5-USSIA-4A-MAP-01: Docling pagina 14 e chunk Chroma 10 verificati; intestazione 4/A assente da headings, testo presente; report `evaluation/ussia_4a_chunk_mapping_v1.json`, script commit `6d2930d`; registro aggiornato.
- [ ] **DA FARE** ispezionare codice chunking V5 per preservare intestazione esercitazione e pagine; non ripetere mapping o benchmark, non reindicizzare senza decisione documentata.

- [x] **ESEGUITO** V5-USSIA-4A-CHUNK-CODE-01: audit statico builder V5 e cause strutturali del mapping intestazioni; report `docs/v5-ussia-4a-chunking-code-audit-2026-10-23.md` (`c67866b`). Nessun test duplicato.
- [ ] **DA FARE** progettare preservazione gerarchia esercitazioni in variante isolata del chunking, senza `--write` sulla collection V5 corrente; definire prima migrazione e rollback.

- [x] **ESEGUITO** V5-EXERCISE-CHUNK-DESIGN-01: progettazione variante gerarchica opt-in documentata in `docs/v5-exercise-aware-chunking-design.md` (commit `4fb3f8f`), registro aggiornato (`724c2c5`). Nessuna scrittura su Chroma e nessun test ripetuto.
- [ ] **DA FARE** implementare estrattore gerarchico isolato e controlli offline deterministici su 3/A, 4/A e 4/B; collection V5, runner e gold invariati.

- [x] **IMPLEMENTATO** V5-EXERCISE-EXTRACT-IMPLEMENT-01: estrattore Docling isolato `scripts/extract_exercise_units_v1.py` (`b599e3e`); registro aggiornato (`c459a3f`). Nessun indice o runner modificato.
- [ ] **DA FARE** controllo offline deterministico del nuovo estrattore su 3/A, 4/A, 4/B e sommario; acquisire report in `evaluation/`, senza ripetere test esistenti.

- [x] **ESEGUITO** V5-EXERCISE-EXTRACT-OFFLINE-01: report V1 `evaluation/ussia_exercise_units_v1.json` esaminato; 4/A preservata, riscontrati refuso esercizio 10, confini sezioni psicocinetica/portiere e ID ricorrenti; registro aggiornato (`61e1c07`). Nessun test ripetuto.
- [x] **IMPLEMENTATO** V5-EXERCISE-EXTRACT-V2-01: `scripts/extract_exercise_units_v2.py` (`23cc0db`), confini e ID distinti per riferimento Docling. Non integrato nella pipeline.
- [x] **ESEGUITO** V5-EXERCISE-EXTRACT-V2-OFFLINE-01: report `ussia_exercise_units_v2.json` analizzato (34 unita); corrette separazioni esercizio 10, 11/B e 21, 4/A invariata; registro commit `7327574`. Nessuna reindicizzazione Chroma.

- [ ] **DA FARE** valutare robustezza dei confini dell'estrattore V2 su fonti diverse prima di un indice candidato isolato; non ripetere controlli Ussia gia eseguiti.

- [x] **IMPLEMENTATO** V5-EXERCISE-HEADING-COVERAGE-01: inventario statico read-only `scripts/audit_exercise_heading_coverage_v1.py` (`a240657`), registro `9a218b7`. Non equivale a verifica di estrazione su altre fonti.
- [x] **ESEGUITO** V5-EXERCISE-HEADING-COVERAGE-OFFLINE-01: inventario `evaluation/exercise_heading_coverage_v1.json` su 141 documenti, 3 compatibili V2 e 38 con altre convenzioni (183 intestazioni); registro `994c627`. Nessun benchmark o modifica Chroma.

- [x] **ESEGUITO** V5-EXERCISE-HEADING-FAMILIES-DESIGN-01: tassonomia intestazioni e confini documentata in `docs/v5-exercise-heading-families-design.md` (commit `2ee613a`), registro `806f312`. Nessun test duplicato.

- [x] **ESEGUITO** V5-EXERCISE-HEADING-ACCEPTANCE-PLAN-01: piano campione e 8 criteri in `docs/v5-exercise-heading-acceptance-plan.md` (`541ccc3`), registro `8d693ec`; nessun test eseguito.

- [x] **IMPLEMENTATO** V5-EXERCISE-HEADING-CONTEXT-IMPLEMENT-01: ispezione read-only delle tre fonti del piano in `scripts/inspect_exercise_heading_context_v1.py` (commit `8dd613f`); registro `2a182b2`. Nessuna indicizzazione.

- [x] **ESEGUITO** V5-EXERCISE-HEADING-CONTEXT-OFFLINE-01: report `exercise_heading_context_v1.json` analizzato su 3 fonti (22 candidati: 8 smarcamento, 6 Gritti, 8 Allegati). Tutti `review_required`, confini non validati. Registro commit `ee72879`; nessun test ripetuto.

- [x] **ESEGUITO** V5-EXERCISE-BOUNDARY-EVIDENCE-DECISION-01: riconciliato il report sulle 22 intestazioni con gli script; i confini non sono validati. Documento `docs/v5-exercise-boundary-evidence-decision.md` (`e114e95`), registro `b9ba79d`.
- [x] **ESEGUITO** V5-EXERCISE-BODY-INSPECTION-PLAN-01: piano read-only in `docs/v5-exercise-body-inspection-plan.md` (`beb05ba`), registro `6f8f9f0`. Nessun test eseguito.
- [x] **IMPLEMENTATO** V5-EXERCISE-BODY-INSPECTION-IMPLEMENT-01: script `inspect_exercise_body_context_v1.py`, commit `a07ebf2`, registro `287140a`.
- [x] **ESEGUITO** V5-EXERCISE-BODY-INSPECTION-OFFLINE-01: report `exercise_body_context_v1.json` analizzato, 22 su 22 candidati; Allegati esercitazione 16 con zero elementi intermedi. Registro `c186120`. Confini non validati.
- [x] **ESEGUITO** V5-EXERCISE-BOUNDARY-ANOMALY-REVIEW-01: anomalie revisionate nel documento `docs/v5-exercise-boundary-anomaly-review.md` (`f1118e8`), registro `eea96ec`. Confini ancora review_required.
- [x] **ESEGUITO** V5-EXERCISE-BOUNDARY-GAP-PLAN-01: piano di controllo mirato in `docs/v5-exercise-boundary-gap-plan.md` (`c2d83bd`), registro `0221dc1`. Nessun test eseguito.
- [x] **IMPLEMENTATO** V5-EXERCISE-BOUNDARY-WINDOWS-IMPLEMENT-01: script `inspect_exercise_boundary_windows_v1.py` (`bb02c68`), registro `cc2ed17`. Nessun test eseguito.
- [x] **ESEGUITO** V5-EXERCISE-BOUNDARY-WINDOWS-OFFLINE-01: quattro finestre analizzate; titoli di esercitazione in `text` e `caption`, esercitazione 16 non vuota. Report `docs/v5-exercise-boundary-windows-findings.md` (`398860d`), registro `187f126`.
- [x] **ESEGUITO** V5-EXERCISE-SEMANTIC-BOUNDARY-DESIGN-01: regole candidate documentate in `docs/v5-exercise-semantic-boundary-design.md` (`b74c496`), registro `d0302a3`. Nessun test eseguito.
- [x] **ESEGUITO** V5-EXERCISE-SEMANTIC-BOUNDARY-PROTOTYPE-01: script `propose_semantic_exercise_boundaries_v1.py` (`528d90b`), report operatore con 16 candidati tutti `review_required`; registro `9206a7a`. Nessuna integrazione V2 o Chroma.
- [x] **ESEGUITO** V5-EXERCISE-SEMANTIC-CANDIDATE-REVIEW-01: revisionati 16 candidati (8 inizi proposti, 4 sezioni, 1 sottotitolo, 3 ripetizioni ambigue); report `docs/v5-exercise-semantic-candidate-review.md` (`b5eae2b`), registro `b93e2ca`. Confini non validati.
- [x] **ESEGUITO** V5-SMARCAMENTO-RESIDUAL-BOUNDARY-DECISION-01: revisione conclusiva delle evidenze disponibili, senza nuovi test; report `docs/v5-smarcamento-residual-boundary-decision.md` (`7b7525d`), registro `cc1f0f6`. Riferimenti 109, 115 e 122 ancora `review_required`; confini non VALIDATI.
- [x] **VALIDATO** V5-SMARCAMENTO-ORIGINAL-LAYOUT-REVIEW-01: esaminato PDF originale pagina 6 (stampata 10); i riferimenti 109, 115 e 122 appartengono a una sola esercitazione con esempi illustrativi. Report `docs/v5-smarcamento-original-layout-review.md` (`c7a65b8`), registro `9d24a33`. Nessuna integrazione V2 o Chroma.

- [x] **IMPLEMENTATO** V5-EXERCISE-CANDIDATE-BUILDER-01: builder opt-in isolato `scripts/build_rag_v5_exercise_candidate_v1.py` (`d8e7741`), registro `4748442`. Nessuna esecuzione VPS, nessuna scrittura Chroma, nessuna integrazione nel runner.
- [x] **ESEGUITO** V5-EXERCISE-CANDIDATE-DRYRUN-01: VPS `Transizioni.Ussia.json`, 34 unità, dry-run senza Chroma/embedding/scritture; registro `2beef52`. Non equivale a retrieval o certificazione.
- [x] **ESEGUITO** V5-EXERCISE-CANDIDATE-CREATE-01: operatore conferma creazione collection isolata; output completo non acquisito, conteggi 34/5319 ancora da verificare (`f827797`). Nessuna promozione.
- [x] **IMPLEMENTATO** V5-EXERCISE-CANDIDATE-RETRIEVAL-IMPLEMENT-01: flag opt-in `--exercise-candidate` nel runner V5 (`0a7223d`) e wrapper (`bdd093b`); default invariato, nessun test runtime (`f827797`).
- [x] **ESEGUITO** primo controllo runtime opt-in: candidato parziale 12/34, arresto prima del retrieval; nessuna generazione. Registro `c6b3ef2`.
- [x] **IMPLEMENTATO** V5-EXERCISE-CANDIDATE-PARTIAL-RECOVERY-01: `--resume-candidate` verifica record esistenti e aggiunge solo quelli mancanti (`0d98281`), registro `c6b3ef2`.
- [x] **ESEGUITO** V5-EXERCISE-CANDIDATE-RESUME-01: output VPS `verified_existing=12 missing=22`, `CANDIDATE_COMPLETE rows=34 baseline_unchanged=5319`; registro `62ee7f6`. Nessuna promozione.
- [x] **ESEGUITO** V5-EXERCISE-CANDIDATE-PROBE-01: primo probe senza candidati per errore regex; report `v5_exercise_candidate_probe_v1.json`, registro `10922a6`.
- [x] **VALIDATO** V5-EXERCISE-CANDIDATE-PROBE-FIXED-01: fix `cf61e33`, report `v5_exercise_candidate_probe_fixed_v1.json`; 4/A Ussia pagina 14 F1, 24 ID candidati nel pool, 34/5319 invariati. Registro `a76f554`. Solo retrieval mirato, non generazione né integrazione default.
- [x] **IMPLEMENTATO** percorso opt-in combinato nel wrapper V5 esistente (`--source-aware --priority-exact --exercise-candidate`); nessun nuovo codice necessario. Registro gate `4718387`; non INTEGRATO di default.
- [x] **ESEGUITO** V5-LOCKED-INTEGRATION-GATE-01: E2E combinato completato con 10/10 risposte generate, citazioni formalmente valide, baseline 5319 e candidato 34 invariati; report `rag_v5_combined_candidate_v1.json`, registro commit `cda20ed`. Valutazione interna claim-per-claim ancora **DA FARE**; nessun punteggio 9/10 attestato, nessuna integrazione di default o certificazione.
- [x] **ESEGUITO** approvazione indipendente del gold e adjudication delle risposte; evitare duplicazione dei test storici. — Requisito di revisore esterno ritirato per decisione del titolare il 2026-10-23; non è attestata una revisione esterna. Restano obbligatori audit interno tracciato, evidenze e verifica 9/10.


### Decisione vincolante V5 — revisore esterno (2026-10-23)

**ESEGUITO — modifica di governance, non validazione del gold.** Su decisione esplicita del titolare, il revisore indipendente esterno e la blind adjudication esterna NON sono prerequisiti del progetto. Le vecchie voci che li richiedono vanno lette come superate da questa decisione, non come verifiche completate. Non dichiarare mai che un revisore esterno ha approvato il gold. La valutazione V5 procede con rubriche e fonti già verificate internamente, manifest con SHA invariato, giudizio claim-per-claim documentato, confronto con evidenze pregresse e controllo runtime. Soglia 9/10 da dimostrare, non presunta. Non riproporre richieste di revisore esterno nelle prossime attività.

- [x] **ESEGUITO** V5-LOCKED-CANDIDATE-INTERNAL-ASSESSMENT-01: audit interno delle 10 risposte completato, **5/10 PASS**, soglia 9/10 non raggiunta. Report `docs/v5-locked-candidate-internal-assessment-01.md` (`506c4ba`), registro `4fc880c`. Nessun nuovo test, nessuna integrazione o certificazione.
- [x] **ESEGUITO** V5-LOCKED-CANDIDATE-FAILURE-ANALYSIS-01: analisi read-only di fresh_01/03/07/09/10, senza nuovi test; report `docs/v5-locked-candidate-failure-analysis-01.md`, commit `60bc141`. Distinti deficit di copertura retrieval, contaminazione fra fonti e completezza della generazione. Prossimo passo: diagnostica pre/post rerank mirata, senza modificare Chroma.

- [x] **ESEGUITO** V5-TACTICAL-CORPUS-RECONCILIATION-01: censimento nominale tattica Drive/VPS/Chroma; 141 PDF VPS, 141 source Chroma, 11 PDF calcistici Drive non trasferiti per decisione storica, file privato escluso. Report `docs/v5-tactical-corpus-reconciliation-2026-10-24.md`, commit `6f08d5a`. Nessuna indicizzazione.
- [ ] **BLOCCATO** V5-TACTICAL-CORPUS-CANDIDATE-REVIEW-01: escluso dal perimetro corrente per decisione esplicita del titolare. Non analizzare, scaricare o indicizzare PDF aggiuntivi da Drive. Priorità: diagnosi dei cinque FAIL V5 sul corpus VPS/Chroma invariato.

- [x] **ESEGUITO** V5-RERANK-TRACE-01: diagnostica read-only VPS fresh_03/fresh_10, script `scripts/diagnose_v5_rerank_failures_v1.py` (`c4ee2b5`), report `docs/v5-rerank-trace-01.md` (`adf47ee`); fresh_03 manuale Transizioni assente da dense24; fresh_10 Ussia pagina 17 al rango 9 del reranker, fuori top8. 5319/34 invariati. Nessun nuovo benchmark.

- [x] **IMPLEMENTATO** V5-SOURCE-COVERAGE-SHADOW-01: script isolato `scripts/v5_source_coverage_shadow_v1.py` (`c400bf0`) per selezionare evidenze da trace già esistente, senza modifica del runner principale, Chroma o generazione. Per fresh_03 segnala fonte assente dal pool; per fresh_10 promuove pagina 17 quando presente. Esecuzione VPS DA FARE; nessuna variazione al benchmark locked 5/10.

- [x] **IMPLEMENTATO** V5-TARGETED-COVERAGE-IMPLEMENTATION-01: opt-in `--targeted-coverage` per fresh_03 (pool filtrato sul manuale Transizioni) e fresh_10 (riserva Ussia p.17), helper `scripts/v5_targeted_coverage_v1.py` (`e75d3ca`), runner `71994e9`, wrapper `d70856f`, diagnostica scoped `b4d1ebf`, report implementazione `docs/v5-targeted-coverage-implementation-01.md` (`413bf4d`). Esecuzione VPS e verifica retrieval-only DA FARE; baseline 5319/34 e benchmark 5/10 non modificati.

- [x] **IMPLEMENTATO** V5-RUNTIME-IMPORT-FAILURE-01: errore VPS dopo LOCK_OK, `/usr/bin/python3` senza `chromadb`; nessun retrieval eseguito. Fix import reali nel selettore runtime (`779f4c3`), report `docs/v5-runtime-import-failure-01.md` (`1a70278`). Riesecuzione mirata DA FARE; benchmark 5/10 invariato.

- [x] **IMPLEMENTATO** V5-RUNTIME-SYMLINK-FIX-01: VPS conferma `chromadb` importabile nel `.venv` ma selettore confonde il symlink con `/usr/bin/python3` per `Path.resolve()`. Correzione `Path.absolute()` (`6faa907`), report `docs/v5-runtime-symlink-fix-01.md` (`d37c1c8`). Verifica VPS DA FARE, nessun retrieval eseguito, 5/10 invariato.

- [x] **ESEGUITO** V5-TARGETED-COVERAGE-RETRIEVAL-01: VPS retrieval-only fresh_03/fresh_10, `COMPLETE 2/2`, Chroma 5319/34 invariati. fresh_03 manuale Transizioni presente F8 p.5 ma evidenza non ancora sufficientemente pertinente ai moduli; fresh_10 manuale p.3 F5 e Ussia p.17 F8. Report `docs/v5-targeted-coverage-retrieval-01.md` (`62e71fc`), JSON VPS `evaluation/v5_targeted_coverage_retrieval_v1.json` fornito dall'operatore. Nessuna generazione o certificazione; benchmark 5/10 invariato.

- [x] **IMPLEMENTATO** V5-TARGETED-ANSWER-CORRECTNESS-01: fresh_03 preferenza per chunk del manuale contenenti moduli 4-3-3/4-4-2/3-5-2/3-4-2-1 (`e0018bf`); fresh_10 conserva Ussia p17. Piano di valutazione claim-level `docs/v5-targeted-answer-correctness-01.md` (`2a5707e`). Generazione scoped VPS DA FARE, benchmark 5/10 invariato.

- [x] **IMPLEMENTATO** V5-TARGETED-ANSWER-SYNTAX-FIX-01: SyntaxError import helper prima della generazione; corretto ramo fresh_03 in `scripts/v5_targeted_coverage_v1.py` (`0c89b47`), report `docs/v5-targeted-answer-syntax-fix-01.md` (`c0f6c63`). Parsing del ramo SYNTAX_OK, verifica VPS DA FARE. Benchmark 5/10 invariato.

- [x] **ESEGUITO** V5-TARGETED-ANSWERS-REVIEW-01: generazione scoped fresh_03/fresh_10 completata, report `docs/v5-targeted-answers-review-01.md` (`dbdb7ca`). fresh_03 NON VALIDATO: manca copertura moduli e limite causale; fresh_10 mandatory claims presenti ma revisione completa sospesa per digressione fuorigioco e distinzione pressing/riaggressione. 132.23s/138.54s, 5319/34 invariati. Baseline 5/10 invariata.

- [x] **ESEGUITO** V5-FRESH03-MANUAL-INVENTORY-01: script read-only `scripts/inspect_v5_fresh03_manual_v1.py` (`dc28977`) per enumerare i chunk indicizzati del manuale fresh_03, senza embedding/rerank/LLM. Report di implementazione `docs/v5-fresh03-manual-inventory-01.md` (`4e3eb53`). Ispezione VPS ESEGUITA: 62 chunk; zero etichette esplicite 4-3-3/4-4-2/3-5-2/3-4-2-1, pagina 4 con descrizioni non etichettate. Report aggiornato `54af77a`; corpus locked 5319 e benchmark 5/10 invariati.
- [x] **ESEGUITO PARZIALMENTE** V5-FRESH03-HEADING-LOSS-TRACE-01: confronto del PDF pagina 4 con i quattro chunk e ispezione del percorso Docling → `HybridChunker`; report `docs/v5-fresh03-heading-loss-trace-01.md`, script read-only `scripts/inspect_v5_fresh03_heading_loss_v1.py` (`1019592`). La causa si restringe alla gerarchia/associazione heading nel confine Docling–chunker, ma la classificazione degli elementi Docling non è disponibile nel workspace. **DA FARE VPS:** una sola esecuzione del trace sul JSON elaborato già esistente; poi implementare la patch sul passaggio dimostrato. Nessuna modifica Chroma, benchmark o generazione.

- [x] **IMPLEMENTATO** V5-FRESH03-HEADING-AWARE-RETRIEVAL-01: lettura metadata headings e quattro chunk modulo fuori dalla top24, commit `cfffe6a`, `68ca18d`; report `docs/v5-fresh03-heading-aware-retrieval-01.md` (`8d510f2`). Verifica VPS DA FARE; benchmark 5/10 invariato.

- [x] **VALIDATO** V5-FRESH03-HEADING-AWARE-RETRIEVAL-01 (solo retrieval): V2 recupera F1–F4 per i moduli 4-3-3, 4-4-2, 3-5-2, 3-4-2-1, tutti pagina 4; 5319 record invariati; report `docs/v5-fresh03-heading-aware-retrieval-v2-result.md` (`a5811c5`). Heading duplicati nel testo, generazione DA FARE; benchmark 5/10 invariato.

- [x] **ESEGUITO** V5-FRESH03-HEADING-AWARE-ANSWER-01: generazione mirata VPS, report `docs/v5-fresh03-heading-aware-answer-v1-review.md` (`1c16f88`); 4 moduli recuperati e heading deduplicati, ma risposta non cita esplicitamente i 4 moduli né dichiara l'assenza di evidenza causale sul cambio modulo. Non VALIDATO; benchmark 5/10 invariato.

- [x] **VALIDATO** V5-FRESH03-GENERATION-GUIDANCE-01 (solo generazione mirata): quattro moduli espliciti, citazioni F1–F4 corrette, limiti causali esplicitati, zero citazioni invalide, Chroma 5319 invariato; report `docs/v5-fresh03-generation-guidance-v1-review.md` (`064f120`). Benchmark locked 5/10 invariato; non INTEGRATO né CERTIFICATO.

- [x] **ESEGUITO** V5-HEADING-ROUTING-INTEGRATION-01: routing generico opt-in (`--heading-routing`) testato su VPS senza `--targeted-coverage`. Report `docs/v5-heading-routing-differential-v1-review.md` (83ef6b4); JSON `evaluation/v5_heading_routing_generic_fresh03_v1.json`. Manuale interno e quattro intestazioni assenti dalla top8, risposta incompleta; zero citazioni invalide, Chroma 5319 invariato. Decisione: non VALIDATO; modificare selezione/promozione evidenze prima di un nuovo test differenziale. Benchmark locked 5/10 invariato; non INTEGRATO né CERTIFICATO.

- [x] **ESEGUITO** V5-HEADING-ROUTING-INTEGRATION-02: differenziale VPS v2, report `docs/v5-heading-routing-differential-v2-review.md` (`76ae393`). Quattro heading riservati, ma manuale selezionato non pertinente: Attacco della Profondità anziché Transizioni Offensive e Difensive. Manca 4-4-2; citazioni invalide 0, Chroma invariato a 5319. Non VALIDATO, non INTEGRATO né CERTIFICATO. Nuovo test solo dopo correzione del ranking della fonte; benchmark locked 5/10 invariato.

- [x] **ESEGUITO** V5-HEADING-ROUTING-INTEGRATION-03: differenziale VPS V3 sul ranking semantico, report `docs/v5-heading-routing-differential-v3-review.md`; JSON VPS `evaluation/v5_heading_routing_generic_fresh03_v3.json`, SHA-256 `b5ebc372a7a1155b88fd217054b1030114c3d1e88593b66b7f1db2deb9cd4e6a`. V3 sceglie `Manuale_Diagonali_Difensive` anziché la fonte pertinente `Transizioni Offensive e Difensive`, riserva `4-2-3-1`, `4-3-3`, `4-4-2` e non copre i quattro moduli richiesti. Limite causale esplicitato, citazioni invalide 0, Chroma invariato a 5319, elapsed 136.03 s. Non VALIDATO, INTEGRATO o CERTIFICATO; benchmark locked 5/10 invariato. Non ripetere senza una nuova differenza tecnica documentata.

- [x] **ESEGUITO** V5-SOURCE-RANKING-TRACE-04: trace opt-in dei punteggi semantici per fonte, commit `1355110`, report `docs/v5-source-ranking-trace-04.md`; JSON VPS `evaluation/v5_source_ranking_trace_fresh03_v1.json`, SHA-256 `c29689e627798bf88c4f4b64b7e72ba0aa5e51d52fa1ae798c76cb611b9639a9`. Retrieval-only `1/1` in 6.73 s, Chroma 5319 invariato. `Manuale_Diagonali_Difensive` vince a `-4.685579` con tre heading; `Transizioni Offensive e Difensive` è seconda a `-5.848974` e copre esattamente `3-4-2-1`, `3-5-2`, `4-3-3`, `4-4-2`. Dimostrato che V3 privilegia somiglianza lessicale senza considerare la copertura richiesta. Non ripetere; V4 solo con differenza generica documentata. Benchmark locked 5/10 invariato.

- [x] **VALIDATO** V5-SOURCE-HYBRID-RANK-V4: selezione generica relevance-gated e coverage-aware, commit `30b04d4`, report `docs/v5-source-hybrid-rank-v4.md`. Retrieval JSON SHA-256 `51f01a0280434501b6eb2f1d6fedc6adcd92198f88a7c6c26c19c7c145367ab2`: fonte corretta e quattro heading, 7.21 s. Generazione JSON `evaluation/v5_source_hybrid_generation_fresh03_v1.json`, SHA-256 `d446a18cf18ed9b7ec4fd7b6e8f751188b82fc222adda12927982e6196bf4a6e`: quattro moduli con F1–F4, limite causale corretto, citazioni invalide 0, 138.78 s. Chroma 5319 invariato. Non ripetere; regressione completa tecnicamente distinta prima dell'integrazione. Benchmark ufficiale 5/10 invariato fino alla valutazione completa; non INTEGRATO o CERTIFICATO.

- [x] **ESEGUITO** V5-HYBRID-CANDIDATE-INTERNAL-ASSESSMENT-02: audit composito senza rerun dei nove casi invariati, report `docs/v5-hybrid-candidate-internal-assessment-02.md`. `fresh_03` passa a PASS con evidenza V4; PASS interni `fresh_02/03/04/05/06/08`, FAIL `fresh_01/07/09/10`, totale composito 6/10. Valore ufficiale locked ancora 5/10 fino a integrazione e valutazione complessiva. Proseguire sui quattro FAIL residui senza test equivalenti.

- [x] **ESEGUITO** V5-POST-LOSS-PRESSURE-GUIDANCE-01: guida generica commit `8b62956`, report `docs/v5-post-loss-pressure-guidance-01.md`; JSON VPS `evaluation/v5_post_loss_pressure_fresh10_v1.json`, SHA-256 `d1cdad96dcdb7f5cd37fbd69e04f04f47807f2a4c6449a3c2898688d8bf321aa`. Mandatory claim presenti e distinzione finale corretta, ma la risposta include ancora la rimessa laterale fra le condizioni post-perdita: forbidden claim non completamente risolto. Citazioni invalide 0, Chroma 5319 invariato, 150.02 s. Non VALIDATO; prossima variante solo con omissione esplicita delle evidenze di pressing generale.

- [x] **VALIDATO** V5-POST-LOSS-CONTEXT-FILTER-02: filtro generico del contesto post-perdita, commit `ecad16b`, report `docs/v5-post-loss-context-filter-02.md`; JSON VPS `evaluation/v5_post_loss_context_fresh10_v2.json`, SHA-256 `25c19cf4497ff4205d016a24e14a55e24c164ddaa8c988d78bed61541c92dc60`. Mandatory claim Ussia e manuale presenti, forbidden claim assente, 5 evidenze generiche escluse, citazioni invalide 0, Chroma 5319/34 invariato, 93.89 s. `fresh_10` passa nell'audit composito, ora 7/10; valore ufficiale locked ancora 5/10 fino a integrazione e regressione complessiva. Non ripetere; non INTEGRATO o CERTIFICATO.

- [x] **IMPLEMENTATO** V5-NAMED-SOURCE-CONTEXT-FILTER-01: filtro generico di coerenza per domande attribuite a un singolo autore, commit `33749bf`; wrapper diagnostico esteso a tutti gli ID locked nel commit `8404495`; report `docs/v5-named-source-context-filter-01.md`. Esclude fonti estranee solo quando esiste evidenza dell'autore nominato; preserva confronti multi-fonte. Test offline 8/8 e compilazione superati. Una sola generazione differenziale `fresh_07` DA FARE; non INTEGRATO o CERTIFICATO.
- [x] **ESEGUITO** V5-NAMED-SOURCE-CONTEXT-FILTER-01: JSON VPS `evaluation/v5_named_source_context_fresh07_v1.json`, SHA-256 `4298e32bdff76615fa1cd0369e2bb36ee928a96c611b8bb70245b2c1d812230f`; quattro fonti estranee escluse, citazioni invalide 0, indici 5319/34 invariati, 97.32 s. Risposta non VALIDATA: omette i playmaker braccati e attribuisce ambiguamente il pericolo all'avversario. Non ripetere; variante successiva solo con guida concettuale differenziale.
- [x] **IMPLEMENTATO** V5-LATERAL-ZONE-ATTRIBUTION-02: guida concettuale generica per coprire playmaker e laterali, mantenere neutra l'attribuzione del pericolo e non universalizzare il rischio, commit `9a1a903`, stesso report. Test offline 9/9 e compilazione superati. Unica generazione V2 `fresh_07` DA FARE.
- [x] **VALIDATO** V5-LATERAL-ZONE-ATTRIBUTION-02: JSON VPS `evaluation/v5_named_source_context_fresh07_v2.json`, SHA-256 `9da89f8287a02504445501800fbf73df6c752603f30b9a043216ae51ee40b371`; playmaker braccati, laterali/pressione a invito/perdita pericolosa presenti, rischio situazionale, sole fonti Foscarini, citazioni invalide 0, indici 5319/34 invariati, 78.5 s. `fresh_07` passa; audit composito 8/10. Non ripetere; non INTEGRATO o CERTIFICATO.

- [x] **IMPLEMENTATO** V5-CONSOLIDATION-CONTEXT-RESERVATION-01: diagnostica read-only trova su pagina 3 i chunk `Quando è opportuno` e `Pro e contro`; riserva generica per concetti consolidamento/riconquista/accelerazione, commit `7004986`, report `docs/v5-consolidation-context-reservation-01.md`. Nessun ID benchmark/chunk hardcoded; test offline 10/10 e compilazione superati. Unica generazione `fresh_09` DA FARE; non INTEGRATO o CERTIFICATO.
