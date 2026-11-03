# TSC V2 — prerequisiti runtime collection e ambiente

## Identità

- Attività: `RD-TSC-V2-RUNTIME-PREREQUISITES-01`
- HEAD GitHub iniziale: `c1cac51f4284bfb9ee249c09ed0e3c4a382fbff7`
- Staging:
  `/home/football/.local/share/football-data-lab/staging/tsc-v2-965d6b6`
- HEAD staging: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`, detached e pulito

## Metodo collection metadata-only

Non è stato usato `PersistentClient`. Dopo avere verificato directory regolare e
assenza di file WAL/SHM, il database
`/opt/football-data-lab/knowledge/rag/chroma/chroma.sqlite3` è stato aperto con la
stdlib Python `sqlite3` usando URI `mode=ro&immutable=1` e `PRAGMA query_only=ON`.
Questa modalità impedisce scritture, creazione di sidecar e migrazioni.

L'ispezione iniziale dello schema ha verificato esclusivamente tabelle e colonne:

- `collections(id,name,dimension,database_id,config_json_str,schema_str)`;
- `segments(id,type,scope,collection)`;
- `embeddings(id,segment_id,embedding_id,seq_id,created_at)`.

La misura aggregata ha collegato collection, segmenti ed embeddings senza leggere
documenti, metadati documentali, vettori o contenuti.

## Collection attestata

- Nome: `dribbling_tactics_v5_multisource_drive11_figc5_candidate_v1`
- Dimensione vettoriale dichiarata: 1024
- Count logico: **6410** `embedding_id` distinti
- Segmenti: metadata SQLite, 6410 righe; vector HNSW persisted, nessuna riga nella
  tabella SQLite degli embeddings
- Percorso: `/opt/football-data-lab/knowledge/rag/chroma`

Attendibilità: il conteggio deriva dalla relazione effettiva
`collections → segments → embeddings` dello schema osservato, non da un valore
configurato. Non prova equivalenza semantica dei contenuti.

## Assenza di modifiche Chroma

Prima e dopo la lettura, nello stesso processo:

- dimensione: `254545920` byte;
- mtime ns: `1793714107765581124`;
- SHA-256:
  `0d19fbea4df3c4f418e7b55c182c0e268862a53d4f903ddc6cd8a7fe8e74a35b`;
- sidecar `chroma.sqlite3-*`: assenti.

I valori sono identici. API PID 76562 e Ollama PID 812 sono rimasti osservabili;
la lettura non assume esclusività futura e non ha modificato servizi.

## Compatibilità Python

- Interprete:
  `/opt/football-data-lab/projects/tactical-engine/.venv/bin/python`
- Versione: Python 3.12.3
- `chromadb`: 1.5.9
- `llama-index-embeddings-ollama`: 0.10.0
- `sentence-transformers`: 6.1.0
- `/usr/bin/time` e `/usr/bin/timeout`: presenti

Sono stati letti soltanto metadata delle distribuzioni e analizzati via `ast.parse`
runner, wrapper, planner e moduli TSC V1/V2 dello staging: sei file presenti e
sintatticamente validi. Nessun modulo applicativo è stato importato; Chroma,
Ollama, embedding e modelli non sono stati inizializzati. Il repository non espone
un `pyproject.toml` o requirements nella radice del tactical engine; le dipendenze
necessarie osservabili risultano comunque installate nella virtualenv prevista.

## Comando Gate

La revisione statica conferma il comando del precedente report impostando:

`TSC_V2_GATE_ROOT=/home/football/.local/share/football-data-lab/staging/tsc-v2-965d6b6`

Sono coerenti baseline, evaluation, artefatti, `--legacy-profile`,
`--tactical-state-contract-v2`, collection, `--expected-count 6410`, modello
`qwen3.5:9b`, context 8192, massimo 4096 token, `--keep-alive 0`, timeout interno
900 s ed esterno 960 s/kill-after 30 s. Il codice prevede massimo una generazione,
zero retry/repair e promozione solo `validated`. Nessuna rettifica è necessaria.

## Invarianza finale

- staging V2: HEAD esatto, status SHA-256 vuoto
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- checkout operativo: HEAD `1a80fe0`, status SHA-256 invariato
  `3877d2b2bb6f9d39300327e58e412c5178089811b9f2db77c716482f35795d06`;
- staging V1: HEAD `3fa3a18`, status SHA-256 invariato
  `dc8be9804101288dcf13ce53c8b9d7ab535ebdb5ef65dd1b75e4ed2f36c74a4d`;
- quattro artefatti Gate: assenti, inclusi symlink dangling;
- servizi: non modificati.

Due tentativi iniziali di ispezione schema sono falliti localmente per quoting
PowerShell prima di eseguire SQL; la successiva trasmissione via stdin ha completato
la sola lettura autorizzata. Non vi sono effetti runtime associati ai tentativi.

## Decisione e stato

- bundle e staging: **VALIDATO**;
- prerequisiti runtime: **VALIDATO**;
- Gate runtime: **DA FARE**, subordinato ad autorizzazione esplicita;
- integrazione: **BLOCCATO**;
- certificazione: **BLOCCATO**.

Nessuna inferenza, query semantica, retrieval, test E2E o Gate è stato eseguito.
