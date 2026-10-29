# RAG Corpus Provenance & Integrity — chiusura offline 01

Data: 2026-10-29  
Ramo: `codex/tactical-state-contract-v1`  
Commit tecnico: `66752e0aad42f89e28d6aed8a2b33357abb72f0b`

## Attività

Sono state chiuse esclusivamente le tre osservazioni residue della revisione
indipendente del percorso Corpus Integrity offline. La differenza tecnica
rispetto ai 22 test precedenti è documentata dai tre nuovi controesempi:
duplicato nell'estrazione sintetica, estrazione sintetica indisponibile ed
evidenza integra ma non pertinente.

## Correzioni

### 1. Duplicati nell'estrazione sintetica

`_reconstruct_synthetic_chunks()` rileva ogni `chunk_id` già incontrato prima
dell'inserimento nel dizionario. Il secondo record non sovrascrive più il
primo e produce l'anomalia bloccante `METADATA_INCOMPLETE`; l'integrità finale
resta `not_verified`.

### 2. Estrazione indisponibile

Per `synthetic-fixture-v1`, un percorso di estrazione assente o inaccessibile
conserva l'anomalia `NOT_ACCESSIBLE` emessa dalla verifica dell'artefatto e
aggiunge `UNVERIFIABLE_RELATION` per la derivazione Docling→chunk. Il percorso
del chunker reale `rag-v5-docling-hybrid-v1` rimane invariato e bloccato in
assenza dell'adapter esatto.

### 3. Qualificazione delle evidenze

La verifica delle evidenze distingue ora esplicitamente nel report tecnico:

- `accessible`;
- `hash_verified`;
- `content_pertinent`;
- `guarantee_qualified`.

Il file deve essere un oggetto JSON tipizzato
`rag_corpus_integrity_evidence_v1`. Un'attestazione di consistenza snapshot è
legata a `snapshot_id`, collection e metodo; un'attestazione di identità
storica è legata a `document_id` e SHA-256 dell'originale. Soltanto un contenuto
pertinente con `qualification_status=qualified`, oltre a percorso e hash
verificati, qualifica la garanzia. Un file arbitrario integro fallisce in modo
chiuso e lo snapshot resta `SNAPSHOT_NOT_CERTIFIABLE`.

Questa è una qualifica deterministica del contratto sintetico, non una prova
della consistenza della collection reale.

## Evidenze

```text
python -m unittest projects/tactical-engine/tests/test_validate_rag_corpus_integrity_v1.py
25 test — OK

python -m unittest projects/tactical-engine/tests/test_validate_relational_gold_preparation_v2.py
21 test — OK

python -m py_compile projects/tactical-engine/scripts/validate_rag_corpus_integrity_v1.py projects/tactical-engine/tests/test_validate_rag_corpus_integrity_v1.py
OK

git diff --check
PASS
```

I test 23–25 dimostrano rispettivamente il rifiuto del duplicato prima della
costruzione del dizionario, la doppia qualifica `NOT_ACCESSIBLE` /
`UNVERIFIABLE_RELATION` e il rifiuto di evidenza formalmente integra ma non
pertinente. La regressione Gold E/V passa 21/21; nessun file Gold è stato
modificato.

## Decisione e stati

- Codice: **IMPLEMENTATO**.
- Test differenziali e regressioni: **ESEGUITO**.
- Controlli sintetici dimostrati: **VALIDATO**.
- Chunker reale e runtime: **BLOCCATO**.
- Non **INTEGRATO** o **CERTIFICATO**.

Nessun accesso VPS, Chroma operativo, Qwen, embedding, indicizzazione,
inferenza, benchmark, merge o deploy è stato eseguito.
