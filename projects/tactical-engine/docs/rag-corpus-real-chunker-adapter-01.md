# RAG Corpus Integrity — Real Chunker Adapter 01

Data: 2026-10-29  
Ramo: `codex/tactical-state-contract-v1`  
Baseline tecnica: `66752e0aad42f89e28d6aed8a2b33357abb72f0b`  
Baseline documentale: `31bc3c7c0cf0a14697d2bddcf355ecf1b5317c5a`

## 1. Attività e decisione

È stata riconciliata staticamente la catena reale PDF → Docling → chunk →
record Chroma, senza accedere alla VPS, al corpus o alla collection operativa.

Decisione: **Caso B — riproducibilità esatta non dimostrabile**.

Non è stato implementato un adapter approssimativo. Il validatore conserva
`UNVERIFIABLE_RELATION` per `rag-v5-docling-hybrid-v1`; adapter reale e runtime
restano **BLOCCATO**.

## 2. Codice reale ricostruito

### Estrazione PDF → Docling

`scripts/ingest_pdfs.py`, funzione `main()`:

- usa `DocumentConverter()` con opzioni predefinite non materializzate in un
  oggetto di configurazione versionato;
- esporta `document.export_to_dict()` come JSON UTF-8 indentato;
- registra nel sidecar l'hash e la dimensione del PDF e
  `pipeline_version=2`;
- la versione 2 descrive anche il backfill delle figure, ma non registra
  versione Docling/docling-core, configurazione del converter o digest
  dell'ambiente che ha prodotto ogni JSON.

### Docling → chunk → record

`scripts/build_rag_index_v5_multisource.py`, funzione `build_rows()`:

1. ordina i JSON selezionati da `inputs_under()`;
2. carica ogni JSON con `DoclingDocument.model_validate_json()`;
3. costruisce `HuggingFaceTokenizer` usando
   `AutoTokenizer.from_pretrained("nomic-ai/nomic-embed-text-v1.5",
   trust_remote_code=True)` e `max_tokens=512`;
4. usa `HybridChunker(tokenizer=..., merge_peers=True)`;
5. enumera `chunker.chunk(dl_doc=doc)` e calcola
   `chunker.contextualize(chunk).strip()`;
6. scarta il testo contextualizzato vuoto, mantenendo l'indice originario
   dell'enumerazione;
7. ricava le pagine da `item.prov[].page_no` e gli heading da
   `chunk.meta.headings`;
8. calcola l'ID come SHA-256 UTF-8 di
   `source_relative:index:contextualized`;
9. costruisce metadata `source`, `source_json`, `source_relative`,
   `source_pdf`, `page_numbers`, `headings`, `raw_text`, `chunk_index`,
   `version=v5_multisource` ed `embedding_model`;
10. passa ID, testo contextualizzato e metadata invariati a `collection.add()`;
    l'embedding è una fase successiva e non serve a ricostruire il record
    testuale.

La logica utile esiste quindi già e non deve essere duplicata: un futuro
adapter dovrà richiamare o estrarre in modulo condiviso `build_rows()`.

## 3. Evidenze disponibili

- Il codice Git dimostra algoritmo, costanti e forma dei metadata.
- `docs/environment.md` riporta storicamente Docling 2.140.0,
  docling-core 2.101.1 e Transformers 5.20.1 sulla VPS.
- `docs/v5-runtime-fingerprint-freeze-01.md` congela un ambiente runtime
  successivo, ma non lega per documento quelle versioni all'estrazione e al
  chunking originari.
- Nel checkout corrente `docling_core`, `transformers` e `chromadb` non sono
  installati.
- Nel repository non sono presenti un JSON Docling reale isolato e uno
  snapshot record corrispondente utilizzabili come prova differenziale esatta.

Le versioni riportate nei documenti sono evidenza storica utile, non un
contratto riproducibile del singolo indice.

## 4. Componenti mancanti e conseguenze

### 4.1 Tokenizer non content-addressed

`AutoTokenizer.from_pretrained()` non specifica `revision`; il repository
Hugging Face e l'eventuale codice remoto autorizzato da
`trust_remote_code=True` non sono identificati tramite commit/digest. Non sono
registrati hash dei file tokenizer né della cache usata.

Conseguenza: token boundaries, split e merge non possono essere attribuiti in
modo verificabile allo stesso artefatto usato per costruire l'indice storico.

### 4.2 Ambiente del chunker non legato al manifest

Le versioni Docling/docling-core/Transformers sono documentate a livello di
ambiente, ma i record e i sidecar non conservano per la run:

- commit dello script builder;
- versioni effettive dei pacchetti;
- hash della configurazione completa;
- digest del tokenizer e del codice remoto.

Conseguenza: non è possibile dimostrare che una nuova esecuzione usi la stessa
semantica di `HybridChunker` e `contextualize()`.

### 4.3 Bundle di prova reale assente

Mancano nel checkout un'estrazione Docling reale, la relativa configurazione
congelata e un export JSON dei record effettivamente prodotti dalla medesima
run. Le dipendenze necessarie non sono disponibili localmente e non sono state
scaricate, in conformità al perimetro.

Conseguenza: non è possibile eseguire una prova offline di uguaglianza esatta
su ID, testo, metadata, pagine e heading.

### 4.4 Estrazione Docling non completamente fingerprintata

`ingest_pdfs.py` registra PDF e `pipeline_version`, ma non l'identità completa
del converter e delle sue opzioni effettive per ogni estrazione.

Conseguenza: l'hash del JSON prova l'identità dei byte già estratti, non rende
riproducibile da solo la trasformazione PDF → JSON.

## 5. Intervento minimo necessario

Per sbloccare un adapter esatto, senza toccare la collection attiva, servirà
un bundle offline read-only e content-addressed contenente:

1. un JSON Docling reale già esistente e il suo SHA-256;
2. un export JSON dei record corrispondenti, con ID, documenti e metadata;
3. commit esatto di `build_rag_index_v5_multisource.py` usato;
4. versioni esatte di Python, docling-core e Transformers;
5. revisione immutabile del tokenizer, hash dei relativi file e identificazione
   del codice remoto caricato;
6. configurazione esplicita `max_tokens=512`, `merge_peers=True` e ogni altro
   default rilevante, con SHA-256;
7. esecuzione in ambiente offline con cache già congelata, senza accesso a
   Chroma, Ollama o embedding.

Solo su quel bundle un adapter potrà riusare `build_rows()`, confrontare
esattamente ID/testo/metadata/pagine/heading e fallire su qualunque versione o
configurazione incompatibile. La futura acquisizione del bundle richiede una
decisione separata; non è stata eseguita in questa attività.

## 6. Test

Nessun test nuovo: l'adapter non è stato implementato e non sono state create
fixture artificiali per simulare la derivazione reale. Le suite Corpus
Integrity 25/25 e Gold E/V 21/21 non sono state ripetute, perché nessun codice
è cambiato e non avrebbero prodotto nuova evidenza.

Sono state eseguite esclusivamente verifiche statiche read-only sul codice e
la verifica locale di disponibilità dei moduli:

```text
docling_core: non disponibile
transformers: non disponibile
chromadb: non disponibile
```

Nessuna dipendenza è stata installata o scaricata.

## 7. Decisione e stati

- Ricostruzione statica del chunker: **ESEGUITO**.
- Verificatore sintetico precedente: **VALIDATO**.
- Adapter reale: **BLOCCATO**.
- Collection reale e runtime: **BLOCCATO**.
- Nessun elemento nuovo **IMPLEMENTATO**, **INTEGRATO** o **CERTIFICATO**.

Nessun accesso VPS, lettura Chroma operativa, indicizzazione, embedding,
inferenza Qwen/Ollama, benchmark, modifica retrieval/API/pannello, merge o
deploy è stato eseguito.
