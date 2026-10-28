# RAG CORPUS PROVENANCE & INTEGRITY — CORREZIONI OFFLINE 01

Data: 2026-10-29
Ramo: `codex/tactical-state-contract-v1`
Commit di partenza: `7618de1`
Commit tecnico correttivo: `f77cb9dfa694367430719022c1e01cb143168ada`

## Attività

Sono state corrette esclusivamente le cinque lacune concrete emerse dalla
revisione indipendente del percorso offline. Nessun componente runtime o Gold
E/V è stato modificato.

## Correzioni

### 1. Derivazione Docling → chunk

Il chunker `synthetic-fixture-v1` ricostruisce dal JSON di estrazione identità,
testo, metadata, pagine e heading, confrontandoli con i chunk del manifest.
Hash individualmente corretti non bastano più a superare la verifica se il
chunk non deriva dall'estrazione.

`rag-v5-docling-hybrid-v1` è riconosciuto ma, in assenza dell'adapter esatto,
produce `UNVERIFIABLE_RELATION`. Versioni ignote producono
`UNSUPPORTED_VERSION`. Nessuna delle due può ottenere integrità `verified`.

### 2. Contratto JSON Schema

Il validatore applica genericamente tutti i keyword usati dallo schema:
`$ref` locale, `type`, `const`, `enum`, `required`, `properties`,
`additionalProperties=false`, `items`, `pattern`, `minLength` e `minimum`.
Keyword assertivi sconosciuti falliscono in modo chiuso. I controlli semantici
relazionali rimangono separati e aggiuntivi.

### 3. Consistenza snapshot

Il contratto include ora `verification_status` ed `evidence_sha256`. Lo stato
`certifiable` richiede evidenza `verified`, percorso relativo sicuro, file
accessibile e hash corrispondente. Metodo o riferimento soltanto dichiarati
producono `SNAPSHOT_NOT_CERTIFIABLE`.

### 4. Identità storica

`document_id` e hash dell'originale devono coincidere. L'identità corrente
richiede originale `verified`. L'identità storica conserva l'identificativo ma
il verificatore risolve il file di evidenza e ne confronta l'hash; evidenza
assente o divergente impedisce l'integrità completa.

### 5. Hash degli ID

L'hash usa la lista completa degli ID ordinati, non un insieme deduplicato.
Gli ID ripetuti restano quindi nell'impronta e sono inoltre segnalati
separatamente come errore di metadata.

## Evidenze

```text
python -m unittest projects/tactical-engine/tests/test_validate_rag_corpus_integrity_v1.py
22 test — OK

python -m unittest projects/tactical-engine/tests/test_validate_relational_gold_preparation_v2.py
21 test — OK

python -m py_compile projects/tactical-engine/scripts/validate_rag_corpus_integrity_v1.py
OK
```

I sei test aggiunti coprono derivazione incoerente, violazioni JSON Schema,
snapshot dichiarato ma non verificato, evidenza storica assente/mismatch, ID
ripetuto e chunker reale senza adapter.

Il diff tecnico modifica esclusivamente schema/template Corpus Integrity,
validatore Corpus Integrity e relativi test. I file Gold E/V sono invariati.

## Limiti e stato

- Correzione codice: **IMPLEMENTATO**.
- Test differenziali e regressione: **ESEGUITO**.
- Controlli offline sintetici coperti: **VALIDATO**.
- Derivazione con chunker reale e collection runtime: **BLOCCATO**.
- Nessun componente è **INTEGRATO** o **CERTIFICATO**.

Non sono stati eseguiti accessi VPS, Chroma operativo, Qwen, embedding,
indicizzazioni, inferenze, benchmark, merge o deploy.
