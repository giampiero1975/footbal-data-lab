# RAG Corpus — Real Chunker Evidence Readiness 01

Data: 2026-10-29  
Ramo: `codex/tactical-state-contract-v1`  
Baseline: `83b235ca5c06e078c6798dc98dc6d117c760ed8f`

## 1. Perimetro e risultato

È stato inventariato esclusivamente ciò che GitHub rende verificabile per un
futuro bundle probatorio del chunker reale `rag-v5-docling-hybrid-v1`. Non sono
stati consultati VPS, Chroma operativo, cache Hugging Face o corpus esterni.

**Decisione: Caso B — bundle parzialmente ricostruibile.** Non emerge alcuna
nuova evidenza che modifichi il Caso B della precedente ricognizione. Il codice
permette di ricostruire l'algoritmo nominale, ma GitHub non contiene gli
artefatti content-addressed della stessa esecuzione necessari a dimostrare la
catena reale Docling → chunk → record. Adapter reale e runtime restano
**BLOCCATO**.

## 2. Fonti GitHub riconciliate

- `scripts/ingest_pdfs.py`: hash PDF, sidecar e produzione JSON Docling.
- `scripts/build_rag_index_v5_multisource.py`: algoritmo reale di chunking,
  ID e metadata.
- `docs/rag-corpus-real-chunker-adapter-01.md`: precedente decisione Caso B.
- `docs/environment.md`: inventario storico dell'ambiente.
- `docs/v5-runtime-fingerprint-freeze-01.md`: riepilogo dei fingerprint
  runtime e dei conteggi 5319/34.
- `evaluation/runtime_evidence_manifest_v1.json`: inventario content-addressed
  di 87 file runtime, i cui contenuti non sono stati copiati nel repository.
- `docs/runtime-evidence-reconciliation-01.md`: limite esplicito del manifest.
- `docs/v5-tactical-corpus-drive11-candidate-01.md` e
  `evaluation/rag_v5_external_drive11_holdout_v1.json`: conteggi e campione
  Drive11, non export completo dei record.
- storico Git del builder: introduzione `70d4002`, estensione candidata
  `ed3bc50`, riserva manuali `21639cb`.

Il checkout non contiene PDF originali né i file runtime
`v5_integrated_runtime_fingerprint_v1.json`,
`v5_integrated_runtime_fingerprint_v2.json` e
`ussia_4a_chunk_mapping_v1.json`. Il manifest ne conserva percorso, dimensione,
hash e classificazione, non il contenuto.

## 3. Matrice delle evidenze

| Categoria | Stato | Fonte e valore verificabile | Ambito e affidabilità | Limite probatorio |
|---|---|---|---|---|
| 1. Hash JSON Docling | **MISSING** | Nessun JSON reale o relativo SHA-256 per documento nel checkout | GitHub corrente | I report attestano output validi, ma non consentono ricalcolo o associazione per file |
| 2. Hash PDF originali | **PARTIAL** | `ingest_pdfs.py` calcola SHA-256; Drive11 dichiara 11/11 hash coerenti | Meccanismo verificabile; esito storico documentato | PDF e valori per documento non sono presenti; nessun ricalcolo possibile |
| 3. Snapshot/export record Chroma | **PARTIAL** | Manifest runtime elenca audit/mapping con hash; holdout espone pochi ID/pagine | Evidenze storiche o diagnostiche | I file runtime non sono in Git; manca export completo ID/documento/metadata della stessa run |
| 4. Commit builder | **AVAILABLE & VERIFIABLE** per il codice; **PARTIAL** per la run | `70d4002`, `ed3bc50`, `21639cb` e contenuti Git | Storia del sorgente affidabile | Nessun record lega crittograficamente una specifica collection al commit effettivamente eseguito |
| 5. Versioni Python/Docling/docling-core/Transformers | **PARTIAL** | `environment.md`: Python storico e Docling 2.140.0, docling-core 2.101.1, Transformers 5.20.1; fingerprint: Python 3.12.3 | Snapshot/riepiloghi storici | Non sono legati per run all'estrazione e al chunking dei record esaminati |
| 6. Revisione tokenizer HF | **MISSING** | Modello nominale `nomic-ai/nomic-embed-text-v1.5` | Costante nel builder | `from_pretrained()` non imposta `revision`; nessun commit immutabile |
| 7. Hash tokenizer e remote code | **MISSING** | `trust_remote_code=True` verificabile nel codice | Configurazione nominale | Nessun inventario/hash della cache o del codice remoto realmente caricato |
| 8. Configurazione chunker | **PARTIAL** | `max_tokens=512`, `merge_peers=True`, `contextualize().strip()`, scarto vuoti e formula ID verificabili nel builder | Semantica del sorgente Git | Default di libreria, tokenizer materializzato e configurazione effettiva della run non congelati |
| 9. Fingerprint delle run | **PARTIAL** | Hash V1 `55a117...`, V2 `f5718a...`, conteggi 5319/34 e versioni riepilogati; manifest registra dimensioni/hash | Integrità dell'identificatore storico | JSON originali assenti; fingerprint orientato al runtime di query, non prova completa della run di chunking |
| 10. Collegamento estrazione → record | **MISSING** | Mapping Ussia e holdout citano ID/pagine | Campioni diagnostici | Nessun manifest della stessa run collega hash estrazione, sequenza chunk e export record completo |

### Lettura della matrice

`AVAILABLE & VERIFIABLE` significa che valore e provenienza possono essere
controllati direttamente nei Git object. `PARTIAL` non autorizza a promuovere
un'attestazione narrativa a prova della stessa esecuzione. `MISSING` significa
che GitHub non permette il controllo richiesto; non significa che l'artefatto
non esista altrove.

## 4. Contratto minimo del futuro bundle offline

Un bundle idoneo deve essere immutabile, content-addressed e riferito a una
sola esecuzione. Deve contenere almeno:

1. `bundle_manifest.json` con versione schema, `bundle_id`, `run_id`, percorsi
   relativi sicuri e hash di ogni dipendenza;
2. almeno un JSON Docling reale già esistente, dimensione e SHA-256, con
   riferimento al PDF/sidecar e al relativo SHA-256 quando disponibile;
3. export read-only dei record prodotti dalla medesima esecuzione: ID,
   documento contextualizzato, metadata, ordine e conteggio;
4. commit Git esatto del builder e attestazione che quel commit è quello
   eseguito, non soltanto quello oggi presente;
5. versioni esatte di Python, Docling, docling-core e Transformers e hash del
   lock/fingerprint dell'ambiente;
6. repository e revisione immutabile del tokenizer, elenco ordinato dei file
   caricati con SHA-256, più identità e hash del codice remoto autorizzato;
7. configurazione completa e canonicalizzata del chunker: `max_tokens`,
   `merge_peers`, metodo di contextualizzazione, gestione dei vuoti, formula
   ID, normalizzazione dei percorsi e ogni default materializzato;
8. collegamento per documento `extraction_sha256 → ordered chunk IDs → record
   export`, con hash della sequenza che non nasconda duplicati;
9. attestazione che la prova viene eseguita offline con cache congelata e
   senza accesso a Chroma attivo, embedding, Ollama o rete.

Controlli minimi: risoluzione e hash di tutti i file; commit esistente;
versioni/configurazione esatte; unicità e ordine degli ID; ricalcolo della
formula ID; uguaglianza byte/logica di testo e metadata; nessun record
mancante o extra nel perimetro dichiarato; report tecnico canonicale separato
dai timestamp di esecuzione.

## 5. Limiti e decisione

I report Drive11 e i fingerprint dimostrano attività storiche utili, ma non
chiudono il nesso fra lo stesso JSON Docling, lo stesso ambiente chunker e lo
stesso export Chroma. Anche i 87 hash del manifest runtime certificano
l'identità dei file inventariati, non sostituiscono i contenuti assenti.

Pertanto:

- inventario GitHub: **ESEGUITO**;
- contratto probatorio minimo: **ESEGUITO** come progettazione documentale;
- adapter reale: **BLOCCATO**;
- acquisizione bundle e verifica offline reale: **DA FARE**;
- runtime/collection: **BLOCCATO**;
- nulla è **IMPLEMENTATO**, **VALIDATO**, **INTEGRATO** o **CERTIFICATO** da
  questa attività.

## 6. Unico prossimo intervento tecnico proposto

Con autorizzazione separata, acquisire **un solo bundle pilota read-only** da
una sorgente storica già esistente, senza reindicizzare: JSON Docling reale,
export dei soli record corrispondenti, commit/configurazione/ambiente e cache
tokenizer con revisioni e hash. Copiare gli artefatti in un'area offline,
congelarli nel manifest sopra definito e soltanto allora valutare l'adapter.

Questo intervento è il minimo che può convertire il Caso B in una prova
falsificabile. Non è stato eseguito.

## 7. Controlli eseguiti

Solo letture statiche di file e Git history. Le suite 25/25 Corpus Integrity e
21/21 Gold E/V non sono state ripetute perché non è cambiato codice e non
avrebbero aggiunto evidenza. Nessun accesso VPS, download, installazione,
indicizzazione, inferenza, embedding, benchmark, merge o deploy.
