# RAG CORPUS PROVENANCE & INTEGRITY DESIGN 01

Data: 2026-10-28
Ramo: `codex/tactical-state-contract-v1`
Audit di base: commit `8650121`
Script: non applicabile — progettazione documentale

## 1. Stato riconciliato

`RD-RAG-DOCUMENTARY-GAP-AUDIT-01` ha dimostrato che il codice conserva lo
SHA-256 del PDF nel metadata di ingestion, ma i record Chroma V5 contengono
percorsi, testo, pagine e heading senza propagare l'hash dell'originale o
dell'estrazione. Il collegamento è quindi nominale e non completamente
verificabile.

Meccanismi esistenti da riutilizzare:

- `ingest_pdfs.py`: SHA-256 del PDF, dimensione, pipeline version e scrittura
  atomica dei metadata;
- `build_rag_index_v5_multisource.py`: ID chunk deterministico, metadata di
  provenienza, verifica fail-closed degli ID esistenti e collection isolate;
- `audit_v5_source_metadata.py`: lettura Chroma a batch e inventario dei campi;
- `inventory_runtime_evidence.py`: manifest di file con dimensione, hash e
  classificazione;
- `validate_relational_gold_preparation_v2.py`: canonicalizzazione RFC 8785
  ristretta, hash, dipendenze e controlli referenziali.

Il Provenance Registry Gold v2 non va riutilizzato come registro corpus: Gold
E/V descrive indipendenza e adjudication dei benchmark, mentre il manifest qui
proposto descrive artefatti della pipeline documentale. Si può riusare in
futuro la sola utility tecnica di canonicalizzazione, dopo estrazione in un
modulo comune con regressione degli hash.

Stato runtime storico riportato: collection operativa 6.410 record / 157 fonti.
Non è stato letto né riconfermato in questa attività.

## 2. Architettura proposta

### 2.1 Artefatti

Un solo bundle di snapshot, senza copiare PDF, JSON, testo dei chunk o vettori:

1. **Root manifest** `rag_corpus_integrity_manifest_v1`:
   identifica snapshot, collection, algoritmo di canonicalizzazione, documenti
   e hash aggregati.
2. **Document records** incorporati o suddivisi in shard deterministici:
   collegano originale, estrazione e chunk attesi.
3. **Verification report** separato:
   registra esiti della verifica read-only senza modificare il manifest
   dichiarativo.

Gli shard sono ammessi soltanto per dimensione; il root manifest deve elencarne
percorso, hash e intervallo ordinato di `document_id`. Non costituiscono un
secondo archivio di conoscenza.

### 2.2 Identità

- `document_id`: `sha256:<pdf_sha256>` soltanto quando il PDF è accessibile e
  l'hash è stato calcolato. Se non è accessibile si usa un `source_ref`
  provvisorio e `document_id=null`; non si promuove il nome file a identità.
- `extraction_id`: `sha256:<docling_json_sha256>`.
- `chunk_id`: ID esatto memorizzato in Chroma.
- `snapshot_id`: UUID o identificativo opaco generato una volta, distinto
  dall'hash del manifest.
- `manifest_sha256`: hash del documento canonicalizzato con il campo stesso
  escluso.

### 2.3 Stati di verifica

Ogni artefatto usa uno stato esplicito:

- `verified`: byte disponibili e hash ricalcolato;
- `declared`: valore importato da metadata ma non ricalcolato;
- `not_accessible`: percorso noto ma byte non disponibili;
- `not_declared`: informazione assente;
- `mismatch`: valore dichiarato diverso da quello ricalcolato.

`declared` e `not_accessible` non equivalgono a `verified`.

## 3. Schema normativo del manifest v1

Schema logico minimo:

```json
{
  "schema_version": "rag_corpus_integrity_manifest_v1",
  "manifest_version": "1.0.0",
  "snapshot_id": "opaque-id",
  "snapshot_kind": "runtime_readonly|synthetic_fixture",
  "created_at": "RFC3339",
  "created_by": "operator-or-tool-id",
  "canonicalization": "RFC 8785 restricted profile",
  "manifest_sha256": null,
  "collection": {
    "name": "collection-name",
    "declared_version": "version-or-null",
    "chroma_version": null,
    "record_count": 0,
    "record_count_status": "declared",
    "distance_metric": null,
    "collection_metadata_sha256": null,
    "sorted_record_ids_sha256": null,
    "embedding": {
      "model": "qwen3-embedding:0.6b",
      "model_digest": null,
      "dimensions": null,
      "vector_fingerprint_mode": "not_collected|float32_le_sha256"
    }
  },
  "documents": [],
  "aggregate": {
    "document_count": 0,
    "expected_chunk_count": 0,
    "verified_chroma_record_count": 0,
    "duplicate_pdf_groups": [],
    "duplicate_chunk_content_groups": []
  },
  "parent_manifest_sha256": null,
  "supersedes_manifest_sha256": null
}
```

Record documento:

```json
{
  "source_ref": "stable-inventory-reference",
  "document_id": "sha256:<pdf-hash>|null",
  "original": {
    "relative_path": "formations/file.pdf",
    "size_bytes": 123,
    "sha256": "64-hex|null",
    "verification_status": "verified|declared|not_accessible|not_declared|mismatch"
  },
  "extraction": {
    "relative_path": "formations/file.json",
    "size_bytes": 456,
    "sha256": "64-hex|null",
    "verification_status": "...",
    "pipeline_name": "docling",
    "pipeline_version": "2",
    "docling_version": null,
    "docling_core_version": null,
    "configuration_sha256": null
  },
  "bibliography": {
    "title": null,
    "authors": [],
    "organization": null,
    "edition": null,
    "publication_date": null,
    "verification_status": "not_declared"
  },
  "rights": {
    "status": "verified|declared|unknown|restricted|expired",
    "license": null,
    "evidence_refs": [],
    "custodian": null
  },
  "chunks": []
}
```

Record chunk:

```json
{
  "chunk_id": "exact-chroma-id",
  "chunk_index": 0,
  "content_sha256": "sha256-of-exact-stored-document",
  "raw_text_sha256": "sha256-or-null",
  "metadata_sha256": "sha256-of-canonical-metadata",
  "pages": [1, 2],
  "headings": ["heading"],
  "source_relative": "formations/file.json",
  "chroma_presence": "present|missing|not_checked",
  "embedding_sha256": null,
  "verification_status": "verified|declared|not_accessible|not_declared|mismatch"
}
```

### 3.1 Regole normative

1. Oggetti canonicalizzati; array non riordinati da RFC 8785. Ordinamento
   semantico definito prima: documenti per `document_id/source_ref`, chunk per
   `chunk_id`, pagine numeriche crescenti. Gli heading preservano l'ordine.
2. Hash in minuscolo, 64 caratteri esadecimali; nessun placeholder.
3. `verified` richiede byte/record letto e hash ricalcolato nella stessa
   esecuzione.
4. `document_id` non nullo richiede PDF `verified`.
5. Un chunk appartiene a un solo document record nello snapshot. Contenuti
   duplicati possono comparire, ma devono essere segnalati.
6. `content_sha256` usa esattamente il campo `documents` restituito da Chroma,
   codificato UTF-8 senza normalizzazione.
7. `metadata_sha256` usa i metadata Chroma canonicalizzati; non ricostruisce
   valori mancanti.
8. `embedding_sha256` è facoltativo. Se usato, encoding normativo float32
   little-endian e dimensione obbligatoria; conversioni da float JSON non
   possono essere dichiarate equivalenti ai byte originali senza prova.
9. Bibliografia e diritti mancanti restano null/unknown.
10. Il manifest non contiene testo integrale, vettori, credenziali o percorsi
    assoluti.

## 4. Specifica del verificatore read-only

### 4.1 Input

- root read-only degli originali;
- root read-only delle estrazioni e metadata;
- root manifest dichiarativo;
- snapshot/copia read-only della collection oppure adapter Chroma in sola
  lettura;
- opzione `--fixture` per test sintetici;
- output nuovo per il report, mai dentro originali/processed/Chroma.

### 4.2 Fasi

1. Validare struttura e versione del manifest.
2. Ricalcolare hash e dimensioni dei file accessibili.
3. Controllare relazione PDF ↔ metadata ingestion ↔ JSON Docling.
4. Ricostruire in memoria i chunk attesi dal JSON con la versione esatta del
   chunker, senza embedding e senza scrittura.
5. Confrontare ID, contenuto e metadata attesi con i record Chroma a batch.
6. Calcolare insiemi `expected_ids` e `actual_ids`:
   - `expected - actual`: record mancanti;
   - `actual - expected`: record orfani;
   - intersezione: confronto contenuto/metadata.
7. Individuare duplicati PDF per hash, estrazioni per hash, contenuti chunk per
   hash e ID duplicati.
8. Calcolare l'elenco dei documenti realmente disponibili al retrieval: almeno
   un record presente e verificato. Questo non certifica rilevanza semantica.
9. Produrre JSON deterministico e riepilogo Markdown.

### 4.3 Esiti

- `MATCH`: hash/relazione verificati;
- `MISMATCH`: confronto possibile e differente;
- `NOT_ACCESSIBLE`: artefatto dichiarato ma non leggibile;
- `NOT_DECLARED`: riferimento o hash mancante;
- `MISSING_RECORD`: chunk atteso assente;
- `ORPHAN_RECORD`: record Chroma senza documento/estrazione risolvibile;
- `DUPLICATE_CONTENT`: stesso contenuto con identità differenti;
- `METADATA_INCOMPLETE`: campo normativo assente;
- `UNSUPPORTED_VERSION`: pipeline necessaria non riproducibile.

Il verificatore deve essere fail-closed sulla dichiarazione di integrità, ma
deve continuare a censire gli altri artefatti e distinguere mismatch da mancato
accesso.

### 4.4 Garanzie operative

- nessuna chiamata a Ollama/Qwen;
- nessuna `add`, `upsert`, `update`, `delete` o creazione collection;
- adapter Chroma espone soltanto `get/count/metadata`;
- output fuori dai dati sorgente e scrittura atomica;
- exit code 0 solo se schema valido e nessuna anomalia bloccante; exit code
  distinto per manifest invalido, mismatch e artefatti non accessibili;
- report con versioni tool, commit, argomenti redatti e hash degli input.

## 5. Integrità documentale e categorie A–F

Gli esiti tecnici non assegnano automaticamente una categoria semantica:

- A richiede inventario autorevole e assenza confermata, non un
  `NOT_ACCESSIBLE` locale;
- B richiede record verificato presente e trace retrieval pertinente che non lo
  recupera;
- C richiede giudizio sul sostegno documentale della risposta;
- D richiede confronto contestualizzato delle fonti;
- E richiede fonti sufficienti e valutazione dell'interpretazione Qwen;
- F si usa quando le evidenze non consentono A–E.

Il verificatore alimenta soprattutto la prova per A/B/F. Non valuta correttezza
tattica o qualità delle risposte.

## 6. Snapshot runtime futuro senza interferire con Qwen

Ordine raccomandato, subordinato a nuova autorizzazione:

1. registrare commit, configurazione dichiarata, collection e conteggio atteso;
2. acquisire snapshot filesystem/provider consistente di originali, processed
   e Chroma, oppure una copia verificata a servizio invariato;
3. eseguire il verificatore sulla copia, non sul path operativo;
4. se la copia non è disponibile, usare letture Chroma batch limitate e
   rate-limited in una finestra concordata, senza caricare Qwen;
5. confrontare conteggio/ID prima e dopo la sola lettura;
6. firmare/hashare manifest e report; non promuovere automaticamente nulla.

Una copia filesystem non consistente non è accettabile. L'apertura simultanea
di `PersistentClient` sul database operativo va valutata prima: “read-only” a
livello di intenzione non garantisce assenza di lock o file ausiliari.

## 7. Piano operativo futuro

### G0 — decisioni del titolare

- collocazione del manifest e degli eventuali shard;
- custode delle evidenze riservate sui diritti;
- retention, accessi e redazione dei percorsi;
- modalità snapshot Chroma ammessa.

### G1 — preflight offline

- schema JSON e template vuoto;
- utility canonicalizzazione condivisa, senza modificare hash Gold v2;
- adapter read-only e deny-list delle operazioni mutanti;
- fixture sintetiche: catena valida, file assente, hash mismatch, orfano,
  duplicato e metadata incompleto.

### G2 — snapshot autorizzato

- copia consistente;
- inventario e hash degli input;
- nessuna inferenza o query tattica.

### G3 — riconciliazione

- esecuzione sulla copia;
- report completo e review umana;
- anomalie candidate nel registro lacune, inizialmente **DA FARE**.

### G4 — eventuale remediation separata

- una causa e una modifica per volta;
- collection candidata, verifica differenziale e rollback;
- approvazione esplicita prima di integrazione.

Rollback: il manifest è append-only tramite `parent_manifest_sha256` e
`supersedes_manifest_sha256`; non modifica dati. Per una futura collection si
mantengono nome/versione precedenti e configurazione di ritorno documentata.

## 8. Limiti e dipendenze

- Le versioni runtime correnti non sono state verificate.
- Ricostruire i chunk richiede esattamente Docling/chunker/tokenizer e
  configurazione usati; in assenza l'esito è `UNSUPPORTED_VERSION`, non
  mismatch.
- Un record presente in Chroma è disponibile tecnicamente ma potrebbe non
  essere recuperabile per una domanda specifica.
- L'hash del vettore non prova che il modello dichiarato lo abbia prodotto.
  Servono modello/digest/configurazione e, se necessario, riproduzione separata;
  questa progettazione non autorizza rigenerazioni.
- Diritti e bibliografia richiedono evidenze umane esterne al contenuto dei PDF.
- Il profilo RFC 8785 esistente supporta solo tipi I-JSON limitati; gli eventuali
  float dei vettori non entrano nella canonicalizzazione JSON del manifest.

## 9. Test statici

Nessun test o validatore nuovo è stato implementato. Un test dello schema senza
schema eseguibile definitivo avrebbe duplicato parzialmente Gold v2 e creato
una falsa impressione di validazione. Le fixture elencate in G1 costituiscono
criteri per una futura patch tecnica separata.

## 10. Criteri di accettazione della futura patch

1. v1 e hash Gold invariati.
2. Manifest e report validano fixture positive e rifiutano i sei casi negativi.
3. Nessun testo/vettore duplicato nel manifest.
4. Nessun valore sconosciuto trasformato in verificato.
5. Distinzione MISMATCH/NOT_ACCESSIBLE dimostrata.
6. Orfani, mancanti e duplicati riportati con ID riproducibili.
7. Adapter incapace di invocare mutazioni Chroma.
8. Output deterministico a parità di input.
9. Nessuna dipendenza da Qwen o endpoint generativi.
10. Report collega commit, versioni e hash degli input.

## 11. Decisione e stato

Architettura, schema logico, verificatore read-only e piano futuro sono
documentati. Non è stato implementato codice perché la collocazione, la
custodia dei diritti e la modalità di snapshot richiedono decisioni preventive
e perché un validatore statico ora duplicerebbe soltanto controlli generici già
coperti da Gold v2.

Stato dell'attività di progettazione: **ESEGUITO**. Implementazione schema,
template, verificatore e fixture: **DA FARE**. Ricognizione runtime:
**BLOCCATO** in attesa di nuova autorizzazione e decisioni G0. Nulla è
**VALIDATO**, **INTEGRATO** o **CERTIFICATO** da questo documento.
