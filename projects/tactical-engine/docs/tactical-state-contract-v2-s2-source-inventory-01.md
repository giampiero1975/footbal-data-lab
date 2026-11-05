# TSC V2 D3 — inventario fonti Gold S2

Attività: `RD-TSC-V2-D3-S2-SOURCE-INVENTORY-01`

Data: 2026-11-05

Baseline: `93695fbdd27833dff8d9d5ff51cb6f14960ede76`

## Attività → Script → Commit → Report → Risultato → Decisione → Stato

- Attività: ricognizione repository-only, documentale e metadata-only delle fonti
  già note al progetto.
- Script: nessun test o runtime; sola lettura e riconciliazione di JSON, report,
  manifest e registri Git.
- Commit: unico commit documentale con inventario, report, TODO e registro.
- Report: questo documento.
- Risultato: 34 fonti nominalmente identificabili; 5 con metadati verificati nel
  perimetro definito, 29 con metadati parziali, zero con diritti verificati e zero
  holdout certificabili.
- Decisione: ricognizione completa per le evidenze accessibili; selezione e
  fattibilità dei Gold 390/606 non dimostrate.
- Stato: inventario **VALIDATO**; selezione fonti e Gold **BLOCCATO**.

## 1. Riconciliazione

Branch, HEAD e working tree coincidevano con la baseline. Sono stati letti TODO,
experiment register, design Gold S2, report schema/validator, readiness, historical
recovery, contratti Gold E/V, dataset claim-fidelity/NLI presenti, manifest e report
di corpus Drive11/FIGC5.

Non esisteva un inventario Gold S2 equivalente. Il provenance registry Gold v2 è un
template con zero record reali. Gli undici output NLI/alignment restano non reperiti;
questa attività non ne ha riaperto la ricerca.

Manifest prodotto:
`evaluation/gold_s2_source_inventory_v1.json`.

## 2. Metodo e perimetro

Sono state incluse soltanto identità nominali collegabili a file Git accessibili:

- dataset claim-fidelity e NLI;
- report di adjudication atomic/contrastive;
- pilot H10 e Gold Glerean;
- riconciliazione e holdout Drive11;
- review editoriale e integrazione FIGC5;
- report collection/corpus già pubblicati.

Non sono stati letti testi di manuali o tesi, interrogati indici/collection, eseguiti
download, scraping, retrieval o modelli. URL sensibili e percorsi privati non sono
stati copiati nel manifest.

Livelli usati:

- `verified`: identità o uso cross-confermato da un artefatto accessibile che
  registra ispezione diretta della fonte/originale verificato;
- `documented_partial`: identità/uso documentato, ma versione, digest, diritti o
  storia completa non verificabili;
- `not_verifiable`: identità sorgente non stabile; nessun caso nel perimetro
  nominale, mentre gli aggregati non scomponibili restano separati.

`verified` non significa diritti verificati, indipendenza o idoneità Gold.

## 3. Risultati numerici

| Misura | Conteggio |
|---|---:|
| Fonti individuali identificate | 34 |
| Metadati verificati nel perimetro | 5 |
| Metadati documentati ma parziali | 29 |
| Identità non verificabile fra i record inclusi | 0 |
| Diritti verificati | 0 |
| Candidata sviluppo | 6 |
| Candidata calibrazione | 9 |
| Candidata adversarial | 3 |
| Candidata holdout | 0 |
| Non assegnabile | 16 |

I conteggi sono ricalcolabili direttamente dal manifest. Tutte le 34 fonti hanno
almeno un `documented_references` esistente nel repository.

Due aggregati non sono conteggiati come fonti individuali:

- baseline storica: 141 PDF/source documentati;
- collection FIGC5: 157 fonti documentate.

Il repository non contiene un export individuale completo e autorizzato che ne
consenta identità, versioni, digest e uso storico per fonte. Il numero 157 non viene
trasformato artificialmente in 157 record Gold candidati.

## 4. Gruppi di fonti

| Gruppo | Record | Evidenza principale | Stato metadata | Candidabilità preliminare |
|---|---:|---|---|---|
| claim-fidelity storico italiano | 5 | quattro dataset `eval/claim_fidelity_*` e adjudication | 2 verified, 3 partial | sviluppo/adversarial; contaminato |
| FA/UEFA/FIGC web usato da claim-fidelity/NLI | 9 | external/fresh/source-disjoint dataset | 9 partial | calibrazione soltanto; già benchmark |
| Tesser atomic | 1 | adjudication NLI | verified | adversarial; contaminato |
| Glerean/Foscarini/Ussia | 3 | H10, Gold Glerean, Gate Ussia | 2 verified, 1 partial | sviluppo; ampiamente esposto |
| Drive11 | 11 | corpus reconciliation e holdout | 11 partial | non assegnabile senza storia/diritti completi |
| FIGC5 | 5 | review editoriale e integrazione | 5 partial | non assegnabile; già integrato/remediation |

## 5. Matrice di utilizzo storico

Il dettaglio per ciascuna fonte è nel JSON. La matrice aggregata non sostituisce i
record individuali.

| Gruppo | RAG/index | Retrieval/generator | NLI/claim-fidelity | Atomic/contrastive/alignment | Gold E/V | D3/S1 | Remediation |
|---|---|---|---|---|---|---|---|
| claim-fidelity italiano | parziale/unknown | unknown | sì | Bonacini/Pane noti; resto unknown | no | unknown | sì/parziale |
| FA/UEFA/FIGC web | non dimostrato | non dimostrato | sì | dettagli incompleti | no | unknown | parziale |
| Tesser | documentato | unknown | NLI sì | atomic sì | no | unknown | sì |
| Glerean/Foscarini/Ussia | sì | sì | unknown | unknown | no | unknown | sì |
| Drive11 | sì | sì | sei casi holdout RAG, non Gold S2 | unknown | no | unknown | sì |
| FIGC5 | sì | documentato/parziale | unknown | unknown | no | unknown | sì |

`unknown` è mantenuto quando i report non consentono attribuzione per singola fonte.
L'assenza degli originali NLI/alignment non prova assenza di utilizzo.

## 6. Indipendenza e contaminazione

Nessuna fonte è classificata come holdout. I principali blocchi sono:

1. tutte le fonti identificate compaiono in dataset, corpus, benchmark, pilot,
   retrieval o remediation già svolti;
2. l'esposizione esatta per singola fonte è spesso `unknown`;
3. non esiste registry reale con versioni, digest e cluster completi;
4. quasi duplicati sono documentati solo per FA wide areas, normalizzazione Ussia e
   doppia edizione di *Una nuova era*;
5. author group manca o è incompleto per varie fonti;
6. essere nel corpus RAG non dimostra utilizzo per tuning, ma neppure indipendenza;
7. un nome diverso non dimostra source/document disjointness.

Le classificazioni sviluppo/calibrazione/adversarial sono proposte conservative:
indicano dove una fonte già esposta potrebbe essere usata senza rivendicare
indipendenza. `not_assignable` indica che i metadati non sostengono una decisione.

## 7. Disponibilità, provenienza e diritti

Cinque fonti hanno metadati verificati nel perimetro: Pane, Bonacini, Tesser,
Glerean e Ussia. Solo Ussia dispone nel repository di un digest PDF storico
esplicito collegato al workflow; ciò non dimostra diritti d'uso per un nuovo Gold.

Per tutte le 34 fonti `rights_status=unknown`. Sito ufficiale, disponibilità Drive,
presenza nel corpus o precedente download non equivalgono a licenza, pubblicabilità,
retention o autorizzazione all'annotazione. Il provenance registry reale resta da
popolare previa decisione del titolare.

## 8. Fattibilità 390/606

| Ipotesi | Classificazione | Motivazione |
|---|---|---|
| Gold ridotto 390 | **non dimostrabile** | 34 identità note, ma zero holdout attestato, diritti 0/34 verificati, esposizione storica incompleta e nessuna evidenza sul numero di claim annotabili |
| Gold raccomandato 606 | **non dimostrabile** | stessi blocchi, aggravati dalla maggiore copertura richiesta; gli aggregati 141/157 non sono record individuali verificati |

Non è dimostrata incompatibilità assoluta: potrebbero esistere fonti idonee nei 141 o
157 documenti. Nel perimetro autorizzato non è però possibile identificarle,
verificarne i diritti o stimare claim senza leggere/generare nuovi contenuti. Per
questo non viene usato `preliminarmente plausibile`.

## 9. Limiti probatori

- Inventario limitato alle identità nominali presenti in Git.
- Nessuna verifica live di file, Drive, URL, collection o VPS.
- Nessun confronto semantico per quasi duplicati.
- Nessuna stima dei claim ricavabili.
- Nessuna metrica storica promossa; output originali NLI/alignment assenti.
- `rag_presence=yes` è documentale, non una query corrente.
- `unknown` non equivale a `no`.
- Nessuna fonte è selezionata, congelata o certificata indipendente.

## 10. Decisioni richieste al titolare

1. autorizzare o negare una fase separata di arricchimento metadata delle identità
   individuali dei corpus 141/157, senza contenuti e con metodo approvato;
2. definire fonti ammissibili, diritti, custodia, retention e pubblicabilità;
3. decidere se escludere integralmente ogni documento già indicizzato dal holdout;
4. approvare regole per versioni, traduzioni, estratti e cluster quasi duplicati;
5. autorizzare solo dopo tali decisioni un registro candidati, non annotazioni;
6. rinviare la scelta 390/606 finché esistono abbastanza fonti indipendenti e con
   diritti verificati;
7. decidere il requisito author-disjoint e le quote massime per autore/organizzazione.

## 11. Stati ufficiali

- Ricognizione e manifest inventory: **VALIDATO** nel perimetro metadata-only.
- Selezione definitiva delle fonti: **BLOCCATO**.
- Provenance registry reale e verifica diritti: **DA FARE** previa autorizzazione.
- Fattibilità 390/606: **BLOCCATO**, non dimostrata.
- Raccolta casi, annotazione A/B, adjudication C, QA D e freeze: **BLOCCATO**.
- Gold S2, S2 shadow, Gate, integrazione e certificazione: **BLOCCATO**.
- Schema/validator Gold S2: stato precedente **VALIDATO offline**, invariato.

L'inventario non autorizza la fase successiva.
