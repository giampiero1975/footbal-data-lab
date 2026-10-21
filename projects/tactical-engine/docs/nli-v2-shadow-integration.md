# DRIBBLING V5 — Piano di integrazione NLI V2 in modalità shadow

Data: 2026-10-21. **Stato: progetto tecnico documentale; nessuna integrazione eseguita sulla VPS.**

## Evidenze di partenza

- **Pipeline candidata V5 (codice GitHub verificato):** `scripts/smoke_test_rag_v5_e2e.py`. Recupera da Chroma `dribbling_tactics_v5_multisource`, verifica attualmente un conteggio atteso di 5319 record, calcola embedding Qwen3 0.6B, recupera 24 candidati, applica mMARCO CPU (`max_length=512`), deduplica gli alias esatti e seleziona fino a 8 evidenze. Genera con `qwen3.5:9b`, `think:false`, `temperature:0`, `num_ctx:8192`. Controlla gli ID delle citazioni **solo sintatticamente**.
- **Classificatore V2 (codice GitHub verificato):** `scripts/benchmark_direct_three_label_nli_v2.py` importa il runner V1 e sostituisce soltanto l'istruzione; il runner V1 usa `NativeOllamaRagasLLM` con schema Pydantic a tre etichette: `supported`, `contradicted`, `insufficient`. Non contiene ancora estrazione di claim, attribuzione di fonti o un hook di produzione.
- **Risultato VPS riportato tramite JSON:** benchmark FIGC/FA 30 casi: 29/30 = 96,67% 3-way, 30/30 binario, zero errori; supported 9/9, contradicted 8/9, insufficient 12/12. Errore `novel_fa_wide_new_04`: fonte dichiara che la Germania supera la contropressione, mentre il giudice sceglie `insufficient` anziché `contradicted`. Il report originale non è ancora archiviato in GitHub; gold non revisionato indipendentemente.
- **Baseline:** mantenere intatte V4, V3 e le collection storiche. La pipeline `ask_dribbling.py` usa ancora la collection V1 e non è un entry point V5; non va sostituita implicitamente.

## Contratto shadow, separato dalla risposta all'utente

1. Eseguire la pipeline V5 **immutata** e salvare domanda, risposta, ID di fonte, testo esatto di ogni evidenza, pagine, configurazione e durata. Non intervenire su retrieval, reranking, prompt di generazione o risposta.
2. Suddividere la risposta in **claim atomici verificabili**, mantenendo i riferimenti alle citazioni originali e la posizione nel testo. Claim multipli in una frase devono essere separati. Non considerare una frase generica o un'etichetta come claim fattuale senza criterio esplicito.
3. Associare a ogni claim solo gli estratti realmente citati o una lista esplicita di fonti candidate; distinguere `no_citation`, `invalid_citation`, `citation_without_support`. **Non unire automaticamente tutte le evidenze in un solo blocco**: ciò può mascherare attribuzioni errate e superare il contesto NLI.
4. Chiamare NLI V2 su coppie `(claim, evidence)` mantenendo invariati modello, prompt, schema e parametri del benchmark. Se sono presenti più fonti, conservare i singoli verdetti e definire in anticipo una regola di aggregazione conservativa; non trattare una fonte `insufficient` come confutazione della fonte che supporta il claim.
5. Registrare per ogni claim `claim_id`, testo, `source_id`, `source_text_hash`, `nli_label`, errori, durata, e classificazione della citazione. Registrare separatamente la copertura dei claim e la correttezza dell'attribuzione.
6. Scrivere **soltanto un report separato**. Nessuna modifica della risposta mostrata, nessun filtro automatico, nessun blocco della generazione, nessuna scrittura in Chroma, nessun cambio di modelli o prompt della pipeline V5.

## Test reversibile, gate e criteri di stop

- **Fase A — contratto offline:** fixture sintetiche con claim atomici, multi-claim, più fonti, citazione inesistente, fonte pertinente ma non sufficiente, contraddizione esplicita, claim senza citazione. Unit test senza Ollama né Chroma. Verificare che risposta e fonti di input rimangano byte-identici.
- **Fase B — replay:** usare report V5 già esistenti, con evidence e risposta congelate; generare un report shadow separato. Non rilanciare il retrieval per la stessa fixture.
- **Fase C — shadow live isolato:** solo dopo revisione gold e audit runtime, eseguire poche domande di sviluppo sulla VPS; controllare integrità degli indici, latenza, errori, citazioni e risorse CPU. Non farlo durante altri benchmark Ollama.
- **Fase D — holdout indipendente:** gold revisionato per claim, citazioni e completezza; soglie concordate prima dell'esecuzione, confronto con pipeline senza shadow. Nessuna promozione automatica dal solo score NLI.
- **Stop/rollback:** in caso di errori, disabilitare semplicemente l'esecuzione shadow; la pipeline originale e gli indici restano invariati. Vietare qualsiasi sovrascrittura dei report sorgente.

## Rischi da misurare prima di implementare

- **Estrazione claim:** non esiste ancora un componente verificato per decomporre risposte tattiche in proposizioni atomiche; un giudice accurato su claim manuali non certifica claim estratti automaticamente.
- **Attribuzione multi-fonte:** l'esistenza di un ID citazione valido non dimostra che l'estratto sostenga il claim.
- **Latenza:** circa 18 secondi per claim nel test FIGC/FA riportato; una risposta con 5 claim potrebbe aggiungere ~90 secondi con esecuzione sequenziale, prima del costo di estrazione e gestione fonti. Stima, non misura end-to-end.
- **Generalizzazione:** dataset FIGC/FA composto da tre estratti riutilizzati in 30 claim; non è un holdout pienamente source-disjoint. Test su documenti lunghi, figure e nuove fonti restano aperti.
- **Classificazione delle contraddizioni:** il caso `novel_fa_wide_new_04` evidenzia il rischio di eccessiva prudenza anche in presenza di contraddizione esplicita.

## Decisione operativa

**Autorizzata la progettazione e l'implementazione di un runner shadow separato, offline-first, senza integrazione runtime e senza modificare gli script V4/V5 funzionanti.** Prima di scrivere un hook nel generatore, costruire fixture e verificare il contratto claim→citazione→estratto. Il giudice NLI V2 rimane candidato sperimentale, non gate di produzione.

## Documentazione ufficiale da verificare durante l'implementazione

- Ollama Chat API: https://docs.ollama.com/api/chat
- Ollama Structured Outputs: https://docs.ollama.com/capabilities/structured-outputs
- Sentence Transformers CrossEncoder: https://sbert.net/docs/package_reference/cross_encoder/model.html
- Chroma collections: https://docs.trychroma.com/docs/collections/configure

Le API e le versioni effettivamente in esecuzione devono essere confermate prima della fase C; i link ufficiali non attestano lo stato runtime.
