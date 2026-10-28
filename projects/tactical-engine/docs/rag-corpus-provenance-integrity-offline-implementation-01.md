# RAG CORPUS PROVENANCE & INTEGRITY OFFLINE IMPLEMENTATION 01

Data: 2026-10-29
Ramo: `codex/tactical-state-contract-v1`
Specifica approvata: commit `38df9c5`
Commit tecnico: `d12d636fa33411f24a390fe5d2666b08f3f9316a`

Revisione correttiva indipendente: commit tecnico `f77cb9dfa694367430719022c1e01cb143168ada`.
Le evidenze aggiornate sono descritte in
`rag-corpus-provenance-integrity-offline-corrections-01.md`.

## 1. Attività e perimetro

È stato implementato il percorso offline isolato progettato in
`rag-corpus-provenance-integrity-design-01.md`. La patch opera soltanto su
fixture o copie esportate come JSON e su file sotto una root esplicitamente
fornita. Non importa Chroma, Ollama o modelli di embedding e non accede alla
VPS o alla collection operativa.

Il collegamento verificato dal contratto è:

`PDF/hash → estrazione Docling/hash → chunk dichiarato → record snapshot/hash`.

La presenza del collegamento non certifica pertinenza semantica, qualità del
retrieval o correttezza tattica di una risposta.

## 2. Componenti implementati

- `evaluation/corpus_integrity/rag_corpus_integrity_manifest_schema_v1.json`:
  JSON Schema versionato del manifest.
- `evaluation/corpus_integrity/rag_corpus_integrity_manifest_template_v1.json`:
  template conservativo con inventario `unknown` e snapshot
  `not_certifiable`.
- `scripts/validate_rag_corpus_integrity_v1.py`: validatore e CLI offline.
- `tests/test_validate_rag_corpus_integrity_v1.py`: fixture sintetiche e test
  differenziali.

La canonicalizzazione viene importata direttamente da
`validate_relational_gold_preparation_v2.py`; non ne sono stati copiati o
modificati algoritmi, schemi o hash.

## 3. Contratti e invarianti

Il validatore applica:

- identità PDF corrente o storicamente verificata con evidenza stabile;
- divieto di promuovere hash dichiarati a identità verificata;
- hash e dimensioni di PDF ed estrazione;
- collegamento di ogni chunk alla relativa estrazione;
- unicità di `source_ref`, `document_id` e `chunk_id`;
- verifica facoltativa del self-hash del manifest;
- confronto fra ID attesi e ID dello snapshot;
- `ORPHAN_RECORD` soltanto con inventario `complete` ed evidenza di
  completezza; altrimenti `UNRECONCILED_RECORD`;
- hash dell'esatto testo UTF-8 e dei metadata canonicalizzati;
- rilevamento di mancanti, mismatch, duplicati e metadata incompleti;
- fail-closed per versione chunker non supportata;
- derivazione Docling → chunk riproducibile per il solo contratto sintetico;
  il chunker reale senza adapter esatto produce `UNVERIFIABLE_RELATION`;
- applicazione completa del sottoinsieme JSON Schema effettivamente usato dal
  contratto, incluse proprietà aggiuntive, required, tipi, enum e pattern;
- verifica tramite file/hash delle evidenze di consistenza snapshot e identità
  storica;
- `SNAPSHOT_NOT_CERTIFIABLE` quando manca una garanzia documentata;
- ordinamento totale di documenti, chunk, record e anomalie;
- separazione `verified_content` / `run_metadata`;
- esclusione di timestamp e durata dall'hash tecnico.

`ReadOnlySnapshotAdapter` espone `count`, `records` e `get`. I metodi `add`,
`upsert`, `update`, `delete` e `create_collection` rifiutano sempre l'operazione.
Il CLI rifiuta sovrascritture e scrive il report atomicamente in un output
separato.

## 4. Esiti riconosciuti

Il report può contenere:

- `MATCH` implicito nell'assenza di anomalie per la relazione verificata;
- `MISMATCH`;
- `NOT_ACCESSIBLE`;
- `NOT_DECLARED`;
- `MISSING_RECORD`;
- `ORPHAN_RECORD`;
- `UNRECONCILED_RECORD`;
- `DUPLICATE_CONTENT`;
- `METADATA_INCOMPLETE`;
- `UNSUPPORTED_VERSION`;
- `UNVERIFIABLE_RELATION`;
- `SNAPSHOT_NOT_CERTIFIABLE`.

L'integrità assume valore `verified` soltanto in assenza di anomalie.

## 5. Test differenziali

Comando:

```text
python -m unittest projects/tactical-engine/tests/test_validate_rag_corpus_integrity_v1.py
```

Risultato iniziale: **16/16 OK**. Dopo la revisione indipendente e la patch
correttiva: **22/22 OK**, 0 errori, 0 fallimenti.

Copertura dimostrata:

1. catena valida;
2. hash PDF differente;
3. PDF inaccessibile con identità storicamente verificata;
4. hash soltanto dichiarato;
5. chunk atteso mancante;
6. record orfano con inventario completo;
7. record non riconciliato con inventario parziale;
8. contenuto duplicato;
9. metadata incompleti;
10. versione chunker non supportata;
11. hash tecnico stabile con timestamp differenti;
12. snapshot non certificabile;
13. rifiuto di tutte le operazioni mutanti;
14. schema e template conservativo;
15. verifica di hash manifest e ID ordinati;
16. esecuzione CLI con report separato.
17. mismatch derivazione Docling → chunk con hash individuali corretti;
18. violazioni JSON Schema su required, tipi, enum, proprietà e hash;
19. evidenza snapshot dichiarata ma non verificata;
20. evidenza storica non risolvibile o con hash differente;
21. hash degli ID sulla sequenza completa con duplicati preservati;
22. chunker reale privo di adapter esatto qualificato non verificabile.

È stata inoltre eseguita la compilazione Python del nuovo script con Python
3.13.15: **OK**.

## 6. Compatibilità Gold E/V

Prima della patch e dopo la patch è stato eseguito:

```text
python -m unittest projects/tactical-engine/tests/test_validate_relational_gold_preparation_v2.py
```

Risultato in entrambi i casi: **21/21 OK**. Il test comprende le regressioni
di immutabilità v1. Il diff tecnico fra `38df9c5` e `d12d636` contiene soltanto
i quattro nuovi file elencati nella sezione 2: nessuno schema, template,
validatore o test Gold E/V è stato modificato.

## 7. Limiti residui

- Nessuna collection reale è stata letta o verificata.
- I valori storici 6.410 record / 157 fonti non sono riconfermati.
- Lo snapshot operativo futuro richiede un meccanismo consistente e
  documentato; uguaglianza di conteggio/ID non è sufficiente.
- Il validatore ricostruisce soltanto il contratto sintetico. Il chunker reale
  richiede ancora un adapter esatto per versione Docling, tokenizer e
  configurazione: fino ad allora la relazione restituisce
  `UNVERIFIABLE_RELATION` e non può contribuire a un'integrità completa.
- Bibliografia e diritti richiedono evidenze umane verificabili.
- Nessun risultato autorizza remediation, indicizzazione o promozione.

## 8. Decisione e stato

- Schema, template, verificatore e test: **IMPLEMENTATO**.
- Test differenziali e regressione Gold E/V: **ESEGUITO**.
- Percorso offline su fixture sintetiche: **VALIDATO**.
- Verifica runtime della collection: **BLOCCATO**.
- Nessun componente è **INTEGRATO** o **CERTIFICATO**.

La fase termina qui. Per snapshot o verifica runtime serve una nuova decisione
operativa; questa attività non la implica.
