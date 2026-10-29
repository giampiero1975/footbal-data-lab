# RAG Corpus — Real Chunker Pilot Bundle Acquisition Plan 01

Data: 2026-10-29  
Ramo: `codex/tactical-state-contract-v1`  
Baseline approvata: `3137c6f88af58d5759a69174586c027363f62f3e`

## 1. Obiettivo e perimetro

Questo documento prepara l'acquisizione futura, read-only e separatamente
autorizzata, di un solo bundle probatorio per
`rag-v5-docling-hybrid-v1`. Non acquisisce dati, non accede a VPS o Chroma e
non riapre la decisione **Caso B**.

Sono stati riconciliati TODO, registro esperimenti, i report adapter/readiness,
gli script diagnostici read-only e gli artefatti GitHub disponibili. Non sono
necessari un nuovo inventario, un altro verificatore o la ripetizione delle
suite Corpus Integrity e Gold E/V.

## 2. Documento pilota proposto

### Candidato provvisorio: `Transizioni.Ussia`

Il candidato è motivato esclusivamente dalle evidenze GitHub:

- sorgente Docling nominale:
  `knowledge/processed/formations-and-systems/Transizioni.Ussia.json`;
- `source_relative` osservato:
  `formations-and-systems/Transizioni.Ussia.json`;
- elementi Docling già identificati `#/texts/151`–`#/texts/154`, con pagina,
  label e testo previsti dal diagnostico;
- record target completo
  `ece84a07265cfef1078c9fdd42027511dd8d27053d014dfe2b98e49e52c465b6`;
- altri ID storici visibili nel holdout, fra cui `600e2713...` e
  `988b5491...`;
- due strumenti read-only già esistenti:
  `inspect_ussia_4a_chunk_mapping_v1.py` (`6d2930d`) e
  `inspect_ussia_4a_index_v1.py` (`3fba6c3`);
- report mapping inventariato con 9.358 byte e SHA-256
  `d661ec2d738928c5594a470e660acee4bb11803f15983407ce1d823f9a5020a5`.

Questi elementi rendono Ussia il candidato con il maggior numero di punti di
riconciliazione già nominati. **Non ne dimostrano ancora l'idoneità
probatoria**: PDF, sidecar, JSON Docling e report mapping non sono pubblicati
nel checkout e non è disponibile il loro legame con il commit builder
effettivamente eseguito.

### Cancello di selezione

Ussia diventa il pilota soltanto se, nella futura ricognizione autorizzata,
risultano contemporaneamente accessibili senza modifica:

1. JSON Docling e relativo sidecar/riferimento PDF;
2. tutti i record filtrati per lo stesso `source_relative`;
3. evidenza storica sufficiente ad attribuire builder, ambiente e tokenizer
   alla medesima elaborazione.

Se il terzo punto manca, il materiale può formare soltanto un bundle
**parziale**. Non si seleziona automaticamente un altro documento: si applica
la stessa graduatoria (hash PDF esplicito, JSON e hash, export completo,
builder/run, ambiente/tokenizer, linkage) e si documenta l'eventuale assenza di
un candidato utilizzabile.

## 3. Procedura futura di acquisizione

### G0 — autorizzazione e area isolata

- autorizzazione separata con percorsi e sorgenti esatti;
- directory di staging riservata, fuori dal repository e dagli artefatti
  operativi;
- filesystem o snapshot coerente documentato; una scansione live con conteggi
  invariati non basta a certificare consistenza;
- nessuna rete durante la successiva verifica offline.

### G1 — originali ed estrazione

1. Leggere senza modificare JSON Docling, sidecar e PDF/riferimento originale.
2. Registrare percorso relativo, dimensione e SHA-256 prima della copia.
3. Copiare nello staging riservato e ricalcolare dimensione/SHA-256.
4. Conservare separatamente contenuto riservato e manifest pubblicabile.
5. Se manca il PDF, preservare l'identità storica solo quando esiste evidenza
   tracciabile; non promuovere un hash dichiarato a verifica corrente.

### G2 — export documentale dei record

1. Da uno snapshot coerente e isolato della collection, estrarre separatamente
   sia i record con `source_relative` esatto sia quelli con
   `source="Transizioni.Ussia"`. Il builder reale produce `source_relative`,
   mentre i diagnostici storici Ussia filtrano per `source`: nessuno dei due
   insiemi può essere assunto completo o usato soltanto come controllo
   secondario.
2. Esportare per ogni risultato `id`, `document`, metadata completi e posizione
   nell'ordine restituito; non usare un insieme deduplicato.
3. Registrare collection, conteggio totale osservato, conteggio del documento,
   criterio di filtro e metodo di snapshot.
4. Confrontare i due insiemi per ID e classificare esplicitamente: record
   riconciliati; record con `source` corretto ma `source_relative` assente;
   record con valori discordanti; record presenti in uno solo dei due filtri.
5. Verificare che gli ID siano unici e che l'ID noto atteso sia presente quando
   pertinente. Qualunque divergenza irrisolta impedisce di dichiarare completa
   la raccolta documentale.
6. Calcolare hash sia del file canonicale sia della sequenza ordinata degli ID.

La completezza così ottenuta riguarda **soltanto tutti i record restituiti per
quel documento nello snapshot dichiarato**. Non dimostra la completezza
dell'intera collection. Per dichiarare completo il documento serve inoltre un
inventario affidabile del perimetro atteso o la ricostruzione esatta della
stessa run; in sua assenza l'esito resta parziale. Il conteggio di uno o di
entrambi gli export filtrati non dimostra da solo la completezza della
collection.

### G3 — provenienza della run

Raccogliere, senza inferire valori mancanti:

- `run_id`, log/comando o manifest storico;
- commit builder effettivamente eseguito;
- Python, Docling, docling-core e Transformers effettivi;
- configurazione materializzata del converter e del chunker;
- revisione immutabile del repository tokenizer;
- elenco e SHA-256 dei file tokenizer realmente caricati;
- identità e SHA-256 del codice remoto caricato con
  `trust_remote_code=True`;
- hash della configurazione canonicalizzata e del fingerprint ambiente.

Un `pip freeze` o una cache acquisiti oggi descrivono lo stato acquisito oggi;
sono attribuibili alla run storica solo con evidenza che sia lo stesso ambiente
immutato. Altrimenti sono utili per un replay nuovo, non per la provenienza
storica.

### G4 — relazione estrazione/record

Nel manifest registrare:

`PDF/sidecar → extraction_sha256 → source_relative → ordered record IDs →
record_export_sha256`.

La relazione è probatoria solo se gli artefatti e la provenienza G3 si
riferiscono alla stessa elaborazione. Il ricalcolo deterministico con un
ambiente nuovo è un esperimento separato: può dimostrare riproducibilità, non
che i record storici siano stati prodotti da quella nuova esecuzione.

### G5 — manifest content-addressed

Produrre un manifest con:

- schema/versione, `bundle_id`, `run_id` e stato del bundle;
- percorsi relativi sicuri, dimensioni e SHA-256;
- oggetti source/extraction/records/builder/environment/tokenizer/config;
- provenienza di ogni valore: `verified_current`, `verified_historical`,
  `declared`, `not_accessible`, `unknown`;
- sequenza completa degli ID, conteggi e hash;
- evidenze e limiti di attribuzione;
- hash canonicale del manifest senza campi circolari;
- metadati di esecuzione separati dal contenuto tecnico riproducibile.

## 4. Evidenze recuperabili e limiti retroattivi

| Evidenza | Recuperabile in linea di principio | Attribuzione storica certa |
|---|---|---|
| JSON Docling, sidecar, PDF se ancora presenti | sì, read-only | solo con hash/evidenza storica corrispondente |
| Record filtrati da snapshot della collection | sì | prova lo snapshot acquisito, non da sola la run originaria |
| ID/testo/metadata e sequenza | sì | sì per lo snapshot, non automaticamente per il builder storico |
| Commit builder | da log/manifest storico | no se scelto soltanto dalla cronologia Git |
| Versioni dipendenze | da ambiente o fingerprint | no se non legate alla stessa run |
| Configurazione esplicita | in parte dal sorgente | default effettivi non attribuibili senza fingerprint |
| Revision/hash tokenizer e remote code | dalla cache congelata, se preservata | no se cache rigenerata o aggiornata |
| PDF→Docling→record | ricostruibile come relazione | probatoria solo con evidenze coeve della stessa elaborazione |

Valori mancanti restano `unknown`; non vengono ricostruiti per plausibilità.

## 5. Criteri di accettazione

### Bundle completo e probatorio

Tutti gli artefatti risolvono e superano hash pre/post copia; export completo
del documento da snapshot consistente; ID/testo/metadata riconciliati;
builder, dipendenze, configurazione, tokenizer e remote code sono attribuiti
alla stessa run mediante evidenza verificabile; linkage G4 integro; nessun
duplicato, artefatto mancante o valore assunto.

### Bundle parziale

Gli artefatti disponibili sono integri e utili, ma almeno uno fra provenienza
della run, revisione tokenizer/remote code, configurazione effettiva o
completezza documentale non è dimostrabile. Può supportare diagnosi o un replay
separato; non sblocca l'adapter come prova della provenienza storica.

### Bundle non utilizzabile

Hash discordanti, snapshot non consistente, source ambiguo, record non
isolabili, duplicati non spiegati, file/evidenze essenziali inaccessibili o
assenza del nesso fra estrazione e record. Il processo fallisce chiuso e non
crea un bundle probatorio.

## 6. Isolamento e riservatezza

- sole letture e copia controllata da sorgenti dichiarate;
- la collection operativa non viene aperta direttamente durante
  l'acquisizione: si usa uno snapshot coerente, isolato e documentato;
- hash, dimensioni e altri invarianti dello snapshot vengono verificati prima
  e dopo la copia, fallendo chiuso su qualunque variazione;
- nessuna scrittura o lock applicativo sulla collection attiva;
- nessuna reindicizzazione, inferenza o generazione embedding;
- staging distinto da corpus, Chroma e repository;
- verifica offline senza rete e con cache congelata;
- PDF, JSON integrali, documenti Chroma e artefatti riservati non pubblicati su
  GitHub; su Git soltanto manifest redatto, hash e report non sensibili;
- accessi, custode, retention ed eventuale distruzione documentati;
- hash prima/dopo copia e report canonicale;
- fail-closed su evidenza insufficiente.

## 7. Strumenti esistenti da riutilizzare

Gli script Ussia esistenti sono diagnostici, non acquisitori probatori, e non
sono da eseguire in questa fase. Entrambi aprono l'archivio tramite
`chromadb.PersistentClient`: il fatto che il codice applicativo chiami soltanto
`get()` e `count()` non dimostra l'assenza di scritture interne, lock o
modifiche ausiliarie della libreria. Inoltre
`inspect_ussia_4a_index_v1.py` crea directory e scrive un report JSON su disco.

Per questo la futura acquisizione non deve aprire direttamente l'archivio
operativo come se fosse immutabile. Deve operare su uno snapshot coerente e
isolato, con integrità controllata prima e dopo la copia. Il futuro export può
riutilizzare la semantica dei due filtri e i controlli Corpus Integrity già
implementati, aggiungendo soltanto l'involucro content-addressed autorizzato.
Nessun adapter viene progettato o implementato in questa fase.

## 8. Decisione e stati

- piano di acquisizione: **ESEGUITO**;
- candidato Ussia: proposto, subordinato ai cancelli G1–G3;
- acquisizione bundle: **DA FARE**;
- verificatore sintetico precedente: **VALIDATO**;
- adapter reale: **BLOCCATO**;
- collection reale/runtime: **BLOCCATO**;
- nessuna nuova attività **IMPLEMENTATO**, **INTEGRATO** o **CERTIFICATO**.

Il passo successivo richiede autorizzazione separata per una ricognizione
read-only con percorsi esatti e staging riservato. Questo piano si ferma prima
di qualunque accesso o acquisizione.

## 9. Appendice pre-acquisizione — checklist operativa definitiva

Questa appendice rende eseguibile il piano senza introdurre un nuovo piano o
un adapter. Le caselle restano intenzionalmente non eseguite.

### 9.1 Percorsi e identità

#### Verificati in Git

- [ ] Baseline Git uguale al commit approvato dell'attività.
- [ ] Builder da esaminare:
  `projects/tactical-engine/scripts/build_rag_index_v5_multisource.py`.
- [ ] Ingestor storico:
  `projects/tactical-engine/scripts/ingest_pdfs.py`.
- [ ] Diagnostici, da non usare come acquisitori:
  `projects/tactical-engine/scripts/inspect_ussia_4a_chunk_mapping_v1.py` e
  `projects/tactical-engine/scripts/inspect_ussia_4a_index_v1.py`.
- [ ] Validatore offline:
  `projects/tactical-engine/scripts/validate_rag_corpus_integrity_v1.py`.
- [ ] Schema e template:
  `projects/tactical-engine/evaluation/corpus_integrity/rag_corpus_integrity_manifest_schema_v1.json`
  e `rag_corpus_integrity_manifest_template_v1.json`.

#### Storicamente attestati, da confermare prima di accedere

- [ ] JSON Docling nominale:
  `/opt/football-data-lab/knowledge/processed/formations-and-systems/Transizioni.Ussia.json`.
- [ ] Collection nominale: `dribbling_tactics_v5_multisource`.
- [ ] Archivio operativo nominale:
  `/opt/football-data-lab/knowledge/rag/chroma`; questo percorso **non deve
  essere aperto** dalla procedura di acquisizione.
- [ ] `source="Transizioni.Ussia"` e
  `source_relative="formations-and-systems/Transizioni.Ussia.json"`.
- [ ] ID di controllo
  `ece84a07265cfef1078c9fdd42027511dd8d27053d014dfe2b98e49e52c465b6`.

#### Da fornire o confermare nell'autorizzazione successiva

- [ ] Percorso esatto e accessibilità del PDF originale.
- [ ] Percorso esatto del sidecar `.meta.json`; la convenzione dell'ingestor
  non prova che il file storico sia ancora presente.
- [ ] Metodo e percorso di uno snapshot coerente già isolato della collection.
- [ ] Directory di staging riservata, custode, accessi, retention e procedura
  di distruzione; nessun valore viene scelto implicitamente.
- [ ] Percorsi di log/manifest della run, ambiente Python e cache tokenizer.
- [ ] Identità del record di autorizzazione e perimetro preciso dei contenuti
  che possono essere copiati.

### 9.2 Prerequisiti bloccanti

- [ ] Autorizzazione esplicita riferita ai percorsi confermati e a una sola
  acquisizione Ussia.
- [ ] Snapshot creato mediante meccanismo coerente documentato e già separato
  dall'archivio operativo; uguaglianza di soli conteggi/ID non basta.
- [ ] Staging riservato vuoto e distinto da repository, corpus e indici.
- [ ] Verifica che la fase offline possa essere eseguita senza rete.
- [ ] Regole di riservatezza approvate: nessun PDF, JSON integrale, testo record,
  cache o remote code riservato su GitHub.
- [ ] Spazio e permessi sufficienti verificati senza modificare le sorgenti.

Se uno di questi prerequisiti manca, l'acquisizione non inizia.

### 9.3 Sequenza di copia e hash

- [ ] Registrare per ogni sorgente percorso, dimensione, timestamp osservato e
  SHA-256 **prima** della copia.
- [ ] Copiare soltanto nello staging autorizzato, preservando il percorso
  relativo necessario alla provenienza.
- [ ] Ricalcolare dimensione e SHA-256 sulla copia; mismatch = arresto e nessuna
  promozione del bundle.
- [ ] Registrare separatamente valore corrente verificato, valore storico
  attestato e valore soltanto dichiarato.
- [ ] Ripetere gli invarianti dello snapshot al termine della copia; variazioni
  o garanzia non qualificabile = `snapshot_not_certifiable`.

### 9.4 Export e riconciliazione del solo documento

Questa fase opera esclusivamente sulla copia isolata, mai sull'archivio
operativo.

- [ ] Esportare una volta tutti i record con
  `source="Transizioni.Ussia"`.
- [ ] Esportare separatamente tutti i record con
  `source_relative="formations-and-systems/Transizioni.Ussia.json"`.
- [ ] Conservare ID, documento, metadata completi e ordine; non deduplicare.
- [ ] Confrontare gli insiemi per ID e classificare: riconciliato,
  `source_relative` mancante, valore discordante, presente in un solo filtro.
- [ ] Verificare ID duplicati, ID di controllo e coerenza interna dei metadata.
- [ ] Qualunque divergenza irrisolta limita il bundle a parziale o non
  utilizzabile; nessun conteggio filtrato certifica l'intera collection.
- [ ] Calcolare SHA-256 del file canonicale e della sequenza ordinata completa
  degli ID, preservando i duplicati come anomalia.

### 9.5 Evidenze della stessa run

- [ ] Risolvere `run_id`, comando/log/manifest e commit builder effettivo.
- [ ] Risolvere versioni effettive di Python, Docling, docling-core e
  Transformers.
- [ ] Materializzare opzioni del converter, `max_tokens`, `merge_peers`,
  contextualizzazione, gestione vuoti, formula ID e normalizzazione path.
- [ ] Risolvere repository e revisione immutabile del tokenizer.
- [ ] Inventariare file tokenizer e remote code effettivamente caricati con
  dimensioni e SHA-256.
- [ ] Collegare ogni evidenza alla stessa run. Ambiente o cache osservati oggi
  senza tale legame restano evidenza di un possibile replay, non provenienza
  storica.

### 9.6 Manifest e verifica offline

- [ ] Partire dal template esistente, senza alterare schema o controlli.
- [ ] Dichiarare inventario del documento `complete`, `partial` o `unknown`
  soltanto secondo le evidenze G2–G4.
- [ ] Inserire riferimenti relativi sicuri, hash, dimensioni, provenienza,
  snapshot consistency, sequenza ID e limiti.
- [ ] Calcolare `manifest_sha256` con la canonicalizzazione esistente.
- [ ] Eseguire il validatore soltanto sullo staging offline con
  `--manifest`, `--snapshot`, `--input-root` e un `--output` nuovo e separato.
- [ ] Conservare `verified_content_sha256`, anomalie e stato; un esito
  strutturalmente valido non colma informazioni storiche mancanti.

Funzioni riutilizzabili senza duplicazione:

- `sha256_file`, `manifest_hash`, `technical_hash` e `normatively_order` per
  integrità e contenuto tecnico deterministico;
- `validate_manifest_contract` per il contratto JSON;
- `ReadOnlySnapshotAdapter` esclusivamente sull'export JSON isolato;
- `verify_integrity`, `_verify_artifact` e `_verify_evidence_file` per il
  controllo offline complessivo.

I diagnostici Ussia forniscono soltanto chiavi e confronti storici. Non sono
richiamati dalla checklist.

### 9.7 Arresto e classificazione finale

Arresto immediato prima o durante l'acquisizione se manca autorizzazione,
snapshot coerente, isolamento, riservatezza, corrispondenza degli hash o
isolabilità del documento. Record non riconciliabili impediscono la
completezza.

- **Completo/probatorio:** tutti i cancelli superati e stessa run dimostrata.
- **Parziale:** artefatti integri, ma provenienza storica o completezza non
  interamente attribuibile; nessuna certificazione o sblocco automatico.
- **Non utilizzabile:** integrità, isolamento o linkage essenziale falliti.

### 9.8 Condizioni minime per la prossima autorizzazione

Il titolare deve indicare o approvare esplicitamente: sorgenti confermate,
metodo/percorso dello snapshot isolato, staging riservato, custode e retention,
perimetro dei dati copiabili e finestra della singola acquisizione. Prima di
questi dati l'acquisizione resta **DA FARE** e non deve essere tentata.
