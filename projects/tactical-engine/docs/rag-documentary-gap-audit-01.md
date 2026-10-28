# RD-RAG-DOCUMENTARY-GAP-AUDIT-01

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
HEAD iniziale: `91ba2f57f765768c3c3a68d08a71b9b4861b4e2a`  
Script: non applicabile — ricognizione statica e documentale

## 1. Obiettivo e stato iniziale

L'attività ricostruisce la catena documentale del RAG e distingue lacune
accertate, casi storici risolti, ipotesi e informazioni non verificabili dal
repository. Non modifica corpus, indici, retrieval, prompt, Qwen o runtime.

Lo stato GitHub riconciliato registra:

- collection storica V5: 5.319 chunk da 141 fonti;
- candidato Drive11: 6.196 record;
- cinque PDF FIGC aggiunti in collection candidata poi promossa: 6.410 record
  e 157 fonti;
- collection 6.410/157 riportata come operativa nei report e nei risultati
  V8–V10 conservati nel repository;
- Gold E/V v2 validato soltanto come contratto offline vuoto: non è un gold
  documentale reale e non dimostra la copertura del corpus;
- `RD-SUPERVISED-AUTO-LEARNING-DESIGN-01` resta separato e **DA FARE**.

I valori runtime sono evidenze storiche versionate, non una nuova lettura della
VPS. La presenza fisica corrente di originali, estrazioni e collection non è
stata verificata in questa attività.

## 2. Audit preesistenti riutilizzati

Non esisteva un audit end-to-end equivalente. Sono stati riutilizzati senza
ripetere prove:

- riconciliazione nominale corpus Drive/VPS/Chroma;
- audit metadata V5 riportato come 5.319/5.319 record validi;
- mapping Ussia 4/A e audit statico del chunker;
- inventario e perdita degli heading del manuale transizioni;
- trace dense/rerank e targeted coverage per `fresh_03`/`fresh_10`;
- source ranking V3/V4;
- manifest delle evidenze runtime e inventario degli script;
- integrazioni candidate Drive11 e FIGC5;
- audit di citazioni e risposte conservati nei report storici.

Alcuni JSON runtime citati dal manifest non sono presenti nel checkout. Il
manifest ne conserva percorso, dimensione, classificazione e SHA-256, ma non
consente di riesaminarne il contenuto. Tali risultati sono quindi
**storicamente riferiti**, non nuovamente validati.

## 3. Catena documentale ricostruita

### 3.1 Originale → estrazione

`scripts/ingest_pdfs.py` opera per default su:

- originali: `/opt/football-data-lab/knowledge/sources`;
- estrazioni: `/opt/football-data-lab/knowledge/processed`.

Per ogni PDF calcola SHA-256 e dimensione, usa Docling per produrre il JSON
strutturato, registra pipeline version 2 e può estrarre figure con pagina e
coordinate. Le scritture metadata sono atomiche.

Verificato nel repository: codice, campi previsti e percorsi predefiniti.
Non verificato qui: file fisici correnti, corrispondenza 1:1 fra ogni PDF e il
relativo JSON/meta, qualità OCR/testo per tutte le 157 fonti.

### 3.2 Estrazione → chunk

`scripts/build_rag_index_v5_multisource.py` legge JSON Docling e usa:

- `HybridChunker` con `merge_peers=True`;
- `HuggingFaceTokenizer` Nomic, massimo 512 token;
- testo `contextualize(chunk)`;
- pagine da `doc_items[*].prov[*].page_no`;
- ID SHA-256 di percorso relativo, indice e testo contextualizzato.

Metadati del record: `source`, `source_json`, `source_relative`, `source_pdf`,
`page_numbers`, `headings`, `raw_text`, `chunk_index`, `version` ed
`embedding_model`.

Limite accertato: i metadata del chunk non incorporano l'hash del PDF o del
JSON di estrazione. Il percorso è tracciato, ma il legame originale → chunk non
è verificabile crittograficamente dal solo record Chroma.

### 3.3 Chunk → embedding → indice

Lo stesso builder dichiara `qwen3-embedding:0.6b`, vettori prodotti tramite
Ollama e collection Chroma persistente con spazio cosine e metadata pipeline
`v5_multisource`. La scrittura è fail-closed su contenuto/metadata diversi per
un ID già esistente; le collection candidate copiano la baseline senza
sovrascriverla.

`docs/components.md` riporta storicamente Docling 2.140.0, docling-core
2.101.1, Chroma 1.5.9, LlamaIndex core 0.14.25 e wrapper Ollama embedding
0.10.0. Queste versioni non sono state rilette dal runtime e non vanno trattate
come fingerprint corrente.

### 3.4 Query → retrieval → evidenze

Il percorso effettivo è composto da `run_rag_v5_query.py` e
`smoke_test_rag_v5_e2e.py`:

1. embedding della domanda con Qwen3 embedding 0.6b;
2. recupero dense dei primi 24 candidati;
3. espansioni opt-in/default documentate per fonte nominata, coverage, heading,
   esercizi e priorità esatta;
4. reranking CPU `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`, massimo 512
   token, salvo il percorso tactical-plan;
5. collapse degli alias e selezione top 8;
6. evidenze numerate F1–F8 con ID, fonte, percorso relativo, pagine e testo.

Il report conserva candidati finali ed evidenze, ma non ogni esecuzione storica
conserva l'intero pool pre-rerank. L'osservabilità è quindi migliorata nel
tempo ma non uniforme retroattivamente.

### 3.5 Evidenze → risposta → citazioni

Le evidenze vengono inserite nel prompt di Qwen. La risposta usa riferimenti
`[F<n>]`; il runner verifica che gli ID citati siano nell'intervallo delle
evidenze e che esista almeno una citazione. Questo controllo prova la validità
formale, non il supporto semantico claim → passaggio. Audit tattici e
relazionali successivi sono separati e, dove indicato, offline/non bloccanti.

## 4. Provenienza e qualità verificabile

| Aspetto | Evidenza disponibile | Limite |
|---|---|---|
| Titolo/origine operativa | `source`, percorsi PDF/JSON e percorso relativo nei chunk | `source` può essere uno stem normalizzato, non un record bibliografico autorevole |
| Integrità originale | SHA-256 nel metadata prodotto da `ingest_pdfs.py` | hash non propagato nel record Chroma; file metadata correnti non presenti nel repository |
| Pagine | provenance Docling → `page_numbers` → evidenza | pagine possono essere PDF e non numerazione stampata |
| Struttura | heading Docling nel chunk | perdite di heading dimostrate per Ussia 4/A e manuale transizioni |
| Autore/versione | talvolta inferibili da nome/titolo | non esiste un catalogo bibliografico completo verificato per le 157 fonti |
| Diritti/licenze | nessun campo corpus autorevole individuato | non verificabili; il Provenance Registry Gold v2 è un template separato e vuoto |
| Duplicati | controlli editoriali specifici FIGC e confronto nominale Drive | nessun controllo globale content-hash documentato per l'intero corpus operativo |
| Citazioni | ID F, source, pagina e testo nel report | validità numerica distinta dal reale supporto semantico |

## 5. Matrice delle lacune verificabili

Le lettere A–F sono categorie diagnostiche, non stati ufficiali.

| ID | Categoria | Evidenza | Classificazione e stato |
|---|---|---|---|
| GAP-001 | B — presente ma non recuperato | `fresh_03`: fonte manuale transizioni assente dai 24 candidati dense; trace e report V5 | Accertato storicamente; retrieval heading-aware successivamente VALIDATO sul caso |
| GAP-002 | B — presente ma escluso dalla selezione | `fresh_10`: Ussia pagina 17 presente nel pool al rango 9, fuori dalla top 8 | Accertato storicamente; targeted coverage successivamente ESEGUITO con pagina promossa |
| GAP-003 | C — evidenza insufficiente | primo recupero mirato `fresh_03`: pagina 5 pertinente al tema ma incapace di sostenere confronto dei moduli e inferenza causale | Accertato; sostituito da recupero F1–F4 pagina 4, validato limitatamente al retrieval |
| GAP-004 | B/C — struttura persa | Ussia 4/A: corpo a pagina 14, ma heading del chunk solo `SVOLGIMENTO`; il retrieval recuperava anche il riferimento d'indice pagina 48 | Accertato; candidato exercise-aware ha validato il recupero puntuale, senza prova universale sul chunking |
| GAP-005 | B/C — heading persi | manuale transizioni: quattro etichette di modulo presenti nel PDF/JSON ma assenti nei quattro chunk corpo | Accertato; correzione di routing validata sul caso, indice originale non ricostruito |
| GAP-006 | E — interpretazione modello | risposta storica Foscarini definiva il 7 “mediano” nonostante l'evidenza sui ruoli | Accertato e corretto nel prompt specifico; non prova assenza della fonte né soluzione generale |
| GAP-007 | F — non determinabile | completezza bibliografica, diritti, licenze e hash originali collegati ai chunk per tutte le 157 fonti | Mancano registry corpus compilato e accesso ai metadata/originali correnti |
| GAP-008 | F — non determinabile | stato fisico corrente collection 6.410/157 e coerenza completa originali → processed → Chroma | GitHub conserva report/risultati, non la collection o tutti gli originali/estratti |

Nessun documento specifico è classificato A “assente”: il repository da solo
non è l'inventario autorevole dei file sulla VPS. Non è stata individuata una
contraddizione D sufficientemente circoscritta e documentata da registrare
come lacuna corrente; differenze di principio tattico vanno contestualizzate
prima di essere classificate come conflitto.

## 6. Schema del registro delle lacune

Un futuro registro versionato può usare un unico record per rilievo:

```json
{
  "gap_id": "RAG-GAP-0001",
  "topic": "transizione negativa",
  "category": "B",
  "official_status": "ESEGUITO",
  "source_refs": [{"source": "...", "pages": [17], "chunk_ids": ["..."]}],
  "evidence_refs": [{"path": "docs/...", "sha256": "..."}],
  "verification_scope": "historical_report|repository|runtime",
  "impact": {"severity": "high", "reason": "..."},
  "priority": {"level": "P1", "reason": "..."},
  "proposed_action": "...",
  "approval_owner": "titolare",
  "resolution": {"decision": null, "commit": null, "report": null},
  "created_at": "...",
  "updated_at": "..."
}
```

Regole:

- `category` A–F non sostituisce `official_status`;
- ogni conclusione richiede almeno un riferimento verificabile;
- F non può essere promosso ad A–E senza nuova evidenza;
- una correzione non cancella il record: aggiunge decisione, commit, report e
  risultato differenziale;
- nessun feedback utente modifica automaticamente registro, corpus o regole;
- non creare il registro operativo prima di definire collocazione, schema e
  responsabile dell'approvazione.

## 7. Procedura controllata futura

1. **Segnalazione:** creare un candidato con domanda, risposta, evidenze e
   versione runtime, stato **DA FARE**.
2. **Verifica documentale:** controllare originale, estrazione, chunk, indice e
   retrieval; classificare A–F oppure F.
3. **Diagnosi:** distinguere aggiunta di conoscenza, correzione di
   estrazione/chunking, ranking/retrieval o interpretazione Qwen.
4. **Proposta:** definire un solo delta misurabile, collection candidata e
   rollback; non modificare in-place il corpus operativo.
5. **Approvazione umana:** titolare e revisore documentale approvano diritti,
   fonte, impatto e prova.
6. **Versionamento:** hash di originali/estrazioni, manifest di collection,
   commit e report.
7. **Verifica differenziale:** retrieval e fedeltà claim→passaggio su caso
   congelato e casi indipendenti; preservare il gold.
8. **Promozione autorizzata:** integrazione separata, smoke e rollback.

L'aggiunta o correzione di documenti/chunk modifica la conoscenza recuperabile
del RAG. Il fine-tuning modifica i pesi di Qwen ed è un processo distinto, non
giustificato automaticamente da una lacuna documentale.

## 8. Priorità operative

1. **P0 — manifest di provenienza del corpus operativo:** collegare per ogni
   fonte PDF hashato, estrazione hashata, chunk e collection; includere diritti
   e custodia. Richiede accesso runtime e decisioni del titolare.
2. **P0 — snapshot read-only della collection corrente:** conteggi, metadata
   mancanti, fonti e campione di linkage; nessuna query tattica o inferenza.
3. **P1 — registro lacune versionato:** implementarlo soltanto dopo approvazione
   di collocazione/schema, riutilizzando i riferimenti esistenti.
4. **P1 — controllo qualità estrazione/chunking campionato:** priorità a heading,
   pagine e tabelle/figure; non reindicizzare senza candidato isolato.
5. **P1 — supporto semantico delle citazioni:** separare ID valido, pertinenza e
   reale sostegno della claim su un gold indipendente.
6. **P2 — catalogo bibliografico:** autore, titolo, versione, organizzazione,
   licenza e duplicati content-hash.

## 9. Questioni bloccate

- Completezza e stato attuale della VPS/Chroma: **BLOCCATO** senza snapshot
  read-only autorizzato.
- Diritti e licenze delle fonti: **BLOCCATO** senza evidenze e custode.
- Copertura tattica complessiva: **BLOCCATO** senza tassonomia e gold
  indipendente compilato.
- Correzioni di corpus, retrieval o Qwen: fuori perimetro e non autorizzate.
- Auto-learning: attività separata **DA FARE**; nessun feedback è apprendimento.

## 10. Decisione e stato

La catena documentale è stata ricostruita a livello di codice e prove
versionate. Sono state consolidate cinque lacune storiche di retrieval/chunking
accertate, una di interpretazione del modello già corretta e due aree non
determinabili. Non è stata dichiarata alcuna nuova assenza documentale.

Decisione: chiudere la ricognizione statica come **ESEGUITO**. Lo schema del
registro e la procedura sono documentati nel report; la loro implementazione è
**DA FARE**. Le
verifiche runtime, il registro operativo e ogni remediation restano **DA FARE**
o **BLOCCATO** come indicato. Nulla è **VALIDATO**, **INTEGRATO** o
**CERTIFICATO** da questa sola attività documentale.
