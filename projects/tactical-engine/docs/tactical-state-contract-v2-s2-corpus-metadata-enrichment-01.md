# Gold S2 — arricchimento metadata corpus 141/157

Attivita: `RD-TSC-V2-D3-S2-CORPUS-METADATA-ENRICHMENT-01`

Data: 2026-11-05

Baseline: `6e5d6bfcc17399e837ffa082b0fd2a076c8b913d`

## Attivita → Script → Commit → Report → Risultato → Decisione → Stato

- Attivita: riconciliazione metadata-only della linea corpus 141 → 152 → 157.
- Script: nessuno; sole letture di manifest, report e metadati Git esistenti.
- Commit: unico commit documentale con manifest, report, TODO e registro.
- Report: questo documento.
- Risultato: continuita aggregata ricostruita; 16 aggiunte individuali gia note;
  zero nuove identita e nessun export individuale dei 141 documenti storici.
- Decisione: la fattibilita Gold 390/606 resta non dimostrata.
- Stato: arricchimento **ESEGUITO**; selezione e Gold S2 **BLOCCATO**.

## 1. Riconciliazione Git e perimetro

Branch `codex/tactical-state-contract-v1`, HEAD e working tree coincidevano con la
baseline. Sono stati consultati TODO, registro, inventario Gold S2 precedente,
design/schema-validator Gold S2, readiness/recovery S2 e i report versionati dei
corpus 141, Drive11, FIGC5 e Knowledge Panel.

Non sono stati letti manuali, tesi o estratti; non sono stati interrogati Chroma,
VPS, API o Drive; nessun download, retrieval, modello, benchmark, caso Gold,
label o freeze. Gli 11 originali NLI/alignment gia dichiarati irreperibili non
sono stati ricercati nuovamente.

Manifest prodotto:
`evaluation/gold_s2_corpus_metadata_enrichment_v1.json`.

## 2. Fonti metadata consultate

Il manifest registra SHA-256 e ultimo commit di sette artefatti probatori:

- inventario precedente delle 34 fonti;
- riconciliazione nominale dei 141 PDF/source;
- integrazione candidata Drive11;
- integrazione FIGC5;
- audit API/catalogo a 152 documenti;
- integrazione panel/catalogo a 157 documenti;
- report dell'inventario Gold S2 precedente.

I file storici nominati `football_pdf_inventory.txt` e
`lista_pdf_indicizzati.log` non sono presenti nel checkout o nella storia Git.
Il report che li cita conserva conteggi e un'unica normalizzazione Ussia, non
l'elenco delle 141 identita.

## 3. Metodo di identificazione

Sono accettate come identita individuali soltanto quelle gia dotate di uno
`source_id` stabile nel manifest precedente e collegate a report versionati.
Sono distinti:

- `verified_match`: corrispondenza deterministica sostenuta dagli artefatti;
- `probable_not_demonstrated`: plausibile ma non probatoria;
- `ambiguous`: piu corrispondenze possibili;
- `not_reconstructable`: nessun record individuale recuperabile.

L'aritmetica dei conteggi non crea identita. `unknown` non viene convertito in
`no`; disponibilita o indicizzazione non dimostrano diritti o indipendenza.

## 4. Riconciliazione dei conteggi 141/157

| Stadio | Documenti | Chunk | Delta | Evidenza individuale |
|---|---:|---:|---:|---|
| baseline storica | 141 | 5.319 | — | elenco individuale non recuperabile da Git |
| Drive11 | 152 | 6.196 | +11 | 11/11 identita nominali gia nel manifest precedente |
| FIGC5 | 157 | 6.410 | +5 | 5/5 identita nominali gia nel manifest precedente |

La costruzione additiva 141 + 11 + 5 e documentata. Quindi l'overlap aggregato
fra baseline 141 e FIGC5 157 e 141, con 16 aggiunte documentate. Non e invece
dimostrabile una mappatura record-per-record dei 141: `individual_overlap_verified`
rimane zero. Questo non significa che i 141 documenti non siano gli antenati della
collection; significa che Git non conserva il loro inventario individuale.

## 5. Identita e sovrapposizioni

Le 16 aggiunte sono:

- Drive11: Italiano, Contran, Maldera, Lorenzon, Vulcano, Baldini, Principi di
  sistema di gioco, Prestigiacomo, Costruzione 343, Redazionale e Preview1;
- FIGC5: Soncin, Di Camillo/Iraola, Rausse/Red Bull,
  Gagliardi-Bordin/*Una nuova era* e Mastroianni/Leao.

Sono tutte gia comprese nelle 34 fonti precedenti. Nuove identita: **0**.
Rimane documentato il cluster di edizioni linguistiche di *Una nuova era*;
non sono stati creati nuovi cluster senza digest o contenuti autorizzati.

Le 34 fonti del precedente inventario provengono anche da dataset web/repository
e non equivalgono a una copertura 34/157 del corpus. Solo le 16 aggiunte hanno un
legame di stadio corpus deterministico in questa riconciliazione.

## 6. Metadati mancanti

Risultato invariato sulle 34 identita:

| Misura | Conteggio |
|---|---:|
| metadati verificati nel perimetro | 5 |
| metadati parziali | 29 |
| diritti verificati | 0 |
| holdout attestati | 0 |
| identita nuove | 0 |
| record individuali mancanti nella scomposizione 157 | 141 |

Per i 141 mancano almeno identificatore stabile, titolo normalizzato, autore,
organizzazione, edizione/versione, lingua, digest originale/processed, cluster
di versione, diritto d'uso e ledger di esposizione completo.

## 7. Esposizione storica

La matrice per le 34 fonti resta quella del manifest precedente. Non sono emerse
nuove evidenze capaci di promuovere campi `unknown` a `no` dimostrato.

Le 11 aggiunte Drive11 e le 5 FIGC5 risultano indicizzate e coinvolte nella
linea retrieval/generazione/remediation descritta dai report. Questo le rende
contaminate per un holdout indipendente, salvo una futura politica diversa
esplicitamente approvata; non prova l'esatto utilizzo di ogni fonte in ogni run.

Per i 141 record ereditati non e disponibile una matrice individuale. L'assenza
di un nome da un report non e prova di mancata esposizione.

## 8. Provenienza e diritti

Nessun nuovo digest per documento e stato recuperato. I report Drive11 attestano
storicamente hash coerenti per 11/11 PDF, ma non pubblicano nel repository una
mappa source→digest utilizzabile. FIGC5 registra pipeline e conteggi, non una
tabella bibliografica completa con diritti.

Diritti verificati: **0/34** e **0/157**. Presenza in Drive, indicizzazione,
accessibilita da un sito ufficiale o uso precedente non autorizzano annotazione,
retention, pubblicazione o impiego nel Gold.

## 9. Indipendenza e contaminazione

- source-disjointness: non dimostrabile per l'intero corpus;
- document-disjointness: non dimostrabile senza identita/digest dei 141;
- author-disjointness: non dimostrabile con autori mancanti;
- version/near-duplicate clusters: parziali e non globali;
- esposizione storica: incompleta per fonte;
- provenienza verificabile: insufficiente per una selezione Gold.

Nessuna fonte viene promossa a holdout o CERTIFICATO.

## 10. Fattibilita Gold 390/606

| Ipotesi | Esito | Motivazione |
|---|---|---|
| Gold ridotto 390 | **BLOCCATO / non dimostrabile** | zero holdout, zero diritti verificati, 141 identita mancanti e nessuna stima autorizzata di claim |
| Gold raccomandato 606 | **BLOCCATO / non dimostrabile** | stessi blocchi con fabbisogno maggiore; il conteggio 157 non misura capacita annotativa |

Non e dimostrata l'impossibilita assoluta. Non e pero lecito stimare claim
ricavabili senza esaminare contenuti, operazione fuori perimetro.

## 11. Informazioni minime ancora necessarie

1. Export metadata-only autorizzato dei 157 documenti con ID stabili.
2. Digest per originale ed estrazione, collegati alla versione corpus.
3. Autore, organizzazione, titolo, edizione/versione e lingua.
4. Evidenza per diritti, retention, annotazione e pubblicazione.
5. Cluster versioni/quasi duplicati basati su digest o metadata autorizzati.
6. Ledger completo dell'esposizione storica per fonte.
7. Autorizzazione separata all'ispezione contenuti prima di stimare claim e volume.

## 12. Decisioni richieste al titolare

1. Autorizzare o negare un export metadata-only dei 157 record dal catalogo gia
   caricato, senza testo/chunk e senza accesso diretto Chroma.
2. Nominare il custode delle evidenze sui diritti e definire retention/pubblicazione.
3. Decidere se ogni documento gia indicizzato debba essere escluso dal holdout.
4. Approvare regole di clustering per versioni, traduzioni e quasi duplicati.
5. Rinviare la scelta 390/606 finche identita, diritti e indipendenza non siano
   sufficienti; non autorizzare ancora selezione o annotazione.

## 13. Limiti probatori e stati

- La linea 141→152→157 e verificata solo come costruzione aggregata documentata.
- Nessuna identita individuale dei 141 e stata recuperata.
- Nessun accesso live ha riconfermato file o collection.
- Nessun contenuto e stato letto e nessuna capacita di claim e stata stimata.
- Inventario precedente delle 34 fonti: **VALIDATO** nel proprio perimetro.
- Arricchimento metadata: **ESEGUITO**.
- Provenienza e diritti reali: **DA FARE**.
- Selezione fonti, Gold 390/606, Gold S2, S2, Gate, integrazione e certificazione:
  **BLOCCATO**.

L'attivita non autorizza alcuna fase successiva.
