# Gold S2 — export metadata-only catalogo FIGC5

Attivita: `RD-TSC-V2-D3-S2-CATALOG-METADATA-EXPORT-01`

Data: 2026-11-05

Baseline: `42b57342c97e9b6127b5d77c9f33d5d67da0796a`

## Attivita → Script → Commit → Report → Risultato → Decisione → Stato

- Attivita: esportare via API i soli metadati individuali del catalogo FIGC5
  gia caricato in memoria.
- Script: nessun file operativo creato; proiezione in memoria durante una
  sessione SSH read-only.
- Commit: unico commit documentale con manifest, report, TODO e registro.
- Report: questo documento.
- Risultato: 157/157 identita operative uniche, somma 6.410 chunk, 25 match con
  l'inventario precedente e 132 identita catalogo nuove rispetto alle 34 note.
- Decisione: identita catalogo riconciliate; Gold 390/606 ancora non dimostrabile.
- Stato: export **ESEGUITO**, riconciliazione identita **VALIDATO**;
  selezione/Gold S2 **BLOCCATO**.

## 1. Riconciliazione e fonte nuova

Branch, HEAD e working tree locali coincidevano con la baseline. Sono stati
riconciliati TODO, registro, inventario 34 fonti, arricchimento 141/157, audit
panel/runtime, codice API e contratti del catalogo. Non esisteva un export
equivalente versionato.

La nuova fonte probatoria e il catalogo operativo gia caricato in memoria,
collection:
`dribbling_tactics_v5_multisource_drive11_figc5_candidate_v1`.

Non sono stati usati `PersistentClient`, SQLite, Chroma diretto, endpoint di
ricerca, testi, chunk, embedding, retrieval o generazione.

## 2. Endpoint e comportamento statico

Endpoint consultati:

- `/v1/metrics`: verifica preliminare `catalog_loaded=true` e worker vivo;
- `/v1/knowledge/stats`: collection, 6.410 chunk e 157 documenti;
- `/v1/knowledge/documents?offset=0&limit=100`;
- `/v1/knowledge/documents?offset=100&limit=100`.

`rag_v5_api.py` serve `documents[offset:offset+limit]` dal catalogo in memoria.
`knowledge_catalog.py` costruisce i documenti raggruppando i record per `source`.
L'endpoint documenti non restituisce il testo dei chunk, ma include percorsi
operativi. La proiezione locale ha quindi conservato esclusivamente:

- `source`;
- `chunk_count`;
- `page_count_observed`;
- `origin_complete`;
- categoria primaria e categorie editoriali derivate.

Sono stati esclusi `source_relative`, `source_pdf`, `source_json`, punteggi
editoriali, testi, chunk, embedding, credenziali e percorsi privati.

## 3. Metodo di acquisizione e integrita

Il token gia configurato e stato caricato nel processo remoto senza stamparlo.
Le risposte sono state proiettate in memoria e trasferite solo dopo la rimozione
dei campi esclusi. La paginazione ha richiesto esattamente due GET documentali.

Controlli acquisiti:

| Controllo | Risultato |
|---|---:|
| catalog loaded prima/dopo | true / true |
| worker alive prima/dopo | true / true |
| documenti stats prima/dopo | 157 / 157 |
| chunk stats prima/dopo | 6.410 / 6.410 |
| record esportati | 157 |
| `source` unici | 157 |
| somma `chunk_count` | 6.410 |
| `origin_complete=true` | 157 |

Checkout operativo osservato prima e dopo a `1a80fe0c...`; i file non tracciati
preesistenti sono rimasti tali. L'unita API era active/running con PID 76562.
Nessuna operazione mutativa e stata eseguita.

Nota operativa: la prima sessione ha completato export e controlli API ma il
comando conclusivo `systemctl --no-pager` ha ricevuto un carattere CR e ha
restituito exit 1 dopo i dati. Per evitare trascrizione manuale, e stata eseguita
una sola riacquisizione minima delle due pagine. La seconda acquisizione e
terminata con exit 0; nessun retry generativo o accesso alternativo e avvenuto.

## 4. Risultato individuale

Manifest:
`evaluation/gold_s2_catalog_metadata_export_v1.json`.

Ogni record conserva `source` come identita operativa esposta dall'API. Non e
stato creato un ID documentale artificiale. `ordinal` indica soltanto la posizione
deterministica nell'export ordinato e non e un identificatore Gold.

| Misura | Conteggio |
|---|---:|
| identita operative esportate | 157 |
| identita uniche | 157 |
| corrispondenze verificate con le 34 precedenti | 25 |
| identita nuove rispetto all'inventario precedente | 132 |
| fonti precedenti non presenti nel catalogo | 9 |
| duplicati esatti per `source` | 0 |

Le nove fonti precedenti non presenti sono le fonti web esterne usate nei set
claim-fidelity/NLI. La loro assenza dal catalogo operativo non dimostra che non
siano mai state esposte al progetto e non ne modifica la contaminazione storica.

## 5. Riconciliazione delle 34 fonti

Le 25 corrispondenze sono sostenute da nome operativo esatto o alias gia
documentato nei report precedenti:

- sei fonti `repo` (inclusi Pane, Bonacini e Tesser);
- tre fonti Drive storiche (Glerean, Foscarini, Ussia);
- undici Drive11;
- cinque FIGC5.

Non sono state create corrispondenze fuzzy. Le restanti 132 identita sono
`new_catalog_identity`: nuove rispetto al manifest da 34, non nuove per il
corpus operativo.

## 6. Riconciliazione 141/157

L'export colma il precedente limite nominale: tutte le 157 identita operative
sono ora elencate. La linea storica resta:

- 141 documenti baseline;
- +11 Drive11 = 152;
- +5 FIGC5 = 157.

Le 16 aggiunte sono riconosciute individualmente. Le altre 141 identita sono
ora osservabili come `source` del catalogo, ma l'endpoint non espone un campo che
marchi esplicitamente lo stadio di ingresso. Non viene quindi assegnato a ciascuna
un `corpus_stage` dedotto soltanto per sottrazione.

## 7. Metadati disponibili e mancanti

| Campo | Copertura |
|---|---:|
| identita operativa `source` | 157/157 |
| chunk count | 157/157 |
| pagine osservate | 157/157 |
| provenienza operativa completa | 157/157 |
| categoria primaria | 157/157 |
| autore | 0/157 |
| organizzazione | 0/157 |
| edizione/versione | 0/157 |
| lingua esplicita | 0/157 |
| digest | 0/157 |
| diritti | 0/157 |

Categorie primarie: 120 tattica, 27 tecnica, 10 allenamento. Categorie non
esclusive: 153 tattica, 91 tecnica, 42 allenamento. Coincidono con il precedente
report applicativo e costituiscono un controllo di coerenza, non una valutazione
di idoneita Gold.

## 8. Duplicati, versioni e provenienza

Non esistono `source` duplicati esatti. L'endpoint non espone digest: duplicati di
contenuto, traduzioni, estratti e versioni non sono valutabili. Nomi simili o
suffissi `(1)` non vengono promossi a cluster di quasi duplicati.

`origin_complete=true` significa che il catalogo derivato possiede un collegamento
operativo al PDF; non fornisce nel manifest pubblico il percorso, il digest o una
catena bibliografica/probatoria completa.

## 9. Esposizione, contaminazione e diritti

Tutti i 157 record sono presenti nella collection operativa e quindi non possono
essere dichiarati holdout indipendenti per il solo fatto che un singolo report non
li nomini. La matrice storica dettagliata resta disponibile solo per le 34 fonti
precedenti; per le 132 nuove identita l'uso specifico in benchmark/remediation e
`unknown`, oltre alla presenza RAG verificata.

- diritti verificati: 0;
- holdout attestabili: 0;
- digest disponibili dall'endpoint: 0;
- fonti CERTIFICATE: 0.

Indicizzazione, categoria o provenienza operativa non dimostrano diritto di
annotazione, retention o pubblicazione.

## 10. Fattibilita Gold 390/606

L'export migliora sostanzialmente la conoscenza nominale da 34 a 157 identita,
ma non sblocca la fattibilita:

| Ipotesi | Stato | Blocco residuo |
|---|---|---|
| Gold ridotto 390 | **BLOCCATO / non dimostrabile** | zero diritti, zero holdout, nessun digest/version cluster, claim capacity ignota |
| Gold raccomandato 606 | **BLOCCATO / non dimostrabile** | stessi blocchi e maggiore fabbisogno di copertura |

Non e autorizzato stimare claim leggendo contenuti. Il numero di documenti non e
una misura del numero di casi indipendenti annotabili.

## 11. Decisioni richieste al titolare

1. Definire se un Gold indipendente debba escludere integralmente il corpus
   operativo; in tal caso nessuno dei 157 e holdout.
2. Nominare il custode delle prove di diritti/licenze e autorizzare un registro
   bibliografico separato.
3. Autorizzare, se necessario, un export futuro di digest gia esistenti da una
   fonte non invasiva; non autorizzare hash o accesso Chroma implicitamente.
4. Definire regole per versioni, traduzioni, estratti e quasi duplicati.
5. Non scegliere 390/606 e non iniziare annotazioni finche diritti,
   indipendenza e capacita di claim non sono dimostrati.

## 12. Stati e limiti probatori

- Export metadata API: **ESEGUITO**.
- Identita operative 157/157: **VALIDATO** nel perimetro dell'API.
- Inventario precedente: invariato; 25 match verificati.
- Provenienza bibliografica, digest e diritti: **DA FARE**.
- Selezione fonti, Gold 390/606, Gold S2 e S2: **BLOCCATO**.
- Nessuna integrazione o certificazione nuova.

L'export non autorizza selezione, annotazione, label, freeze, S2 shadow o Gate.
