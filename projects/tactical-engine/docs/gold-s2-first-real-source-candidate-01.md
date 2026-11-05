# Gold S2 — prima fonte reale candidata

Attivita: `RD-S2-FIRST-REAL-SOURCE-CANDIDATE-01`

Data: 2026-11-05

Baseline: `96e80187a25884b80bbc3924604eac6bf770603e`

Commit record: `ac7dfe8b2f13dbd72412022d4f8e6f55ae3b1bcd`

## Attivita → Script → Commit → Report → Risultato → Decisione → Stato

- Attivita: qualificare una sola fonte scientifica autorizzata e registrarla nel
  Candidate Registry V1.
- Script: validatore esistente
  `scripts/validate_gold_s2_source_candidate_registry_v1.py`.
- Commit: record preliminare nel commit sopra indicato; documentazione separata.
- Report: questo documento.
- Risultato: identita, versione ufficiale, byte PDF e dichiarazione CC BY
  verificati; match nominali zero nei due registri esistenti; diritti operativi,
  esposizione completa e indipendenza non ancora attestati.
- Decisione: candidato registrato con `blocked_unknown`, nessuno split.
- Stato: registrazione **ESEGUITO**; struttura del record **VALIDATO**;
  eleggibilita Gold **BLOCCATO**.

## 1. Identita bibliografica verificata

- Titolo: *Shortcomings of applying data science to improve professional
  football performance: Takeaways from a pilot intervention study*.
- Autori: Mat Herold, Matthias Kempe, Ludwig Ruf, Luis Guevara, Tim Meyer.
- Rivista: *Frontiers in Sports and Active Living*, volume 4, Brief Research
  Report, sezione Elite Sports and Performance Enhancement.
- Pubblicazione: 12 ottobre 2022.
- DOI: `10.3389/fspor.2022.1019990`.
- Versione: version of record in inglese.
- Pagina ufficiale:
  `https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.1019990/full`.
- PDF ufficiale:
  `https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.1019990/pdf`.

Pagina e PDF ufficiali concordano su titolo, autori, data, rivista e DOI.

## 2. Integrita dei byte

Il file indicato dall'utente non era presente nei percorsi locali controllati.
E stata quindi scaricata una singola copia temporanea dall'URL PDF ufficiale e
verificata localmente, senza aggiungere il PDF al repository:

- dimensione: `654208` byte;
- SHA-256: `8742bfaa21170df3a63ad53c7486ee62e6b39ceef168d6c3bdeab29fdb04bc31`;
- confronto con i valori forniti: corrispondenza esatta.

Il record usa `verification_status=verified_bytes`. La verifica riguarda i byte
ricevuti dall'URL ufficiale e non certifica diritti o indipendenza.

## 3. Licenza e ambiti operativi

Il PDF dichiara articolo open access distribuito sotto Creative Commons
Attribution (CC BY), con uso, distribuzione o riproduzione consentiti a condizione
di attribuire autori e titolare e citare la pubblicazione, nel rispetto delle
pratiche accademiche.

La dichiarazione e registrata come evidenza verificata. Tuttavia il progetto non
ha ancora un custode dei diritti, una policy retention/pubblicazione approvata o
una decisione umana attribuibile sui tre ambiti del registro. Per questo:

- retention: `unknown`;
- annotazione: `unknown`;
- pubblicazione: `unknown`.

Il validatore non svolge consulenza legale e la mera accessibilita pubblica non
promuove gli ambiti a `verified`.

## 4. Pertinenza e limiti come evidenza

L'articolo e pertinente al calcio professionistico e tratta positional tracking,
analisi delle prestazioni, efficacia dei passaggi, difensive disruption, avversari
superati, video feedback e trasferimento dei risultati data-science al coaching.

La sua utilita probatoria e circoscritta. E un pilot con 24 giocatori, un disegno
pre/post, una breve esposizione video e risultati senza miglioramenti
significativi per le metriche principali. Puo sostenere claim specifici sul
metodo, sulle metriche osservate e sui limiti del trasferimento alla pratica; non
e una fonte generale per prescrivere principi tattici universali, ruoli, trigger
o relazioni operative non documentate.

Non sono stati generati claim, domande, label o annotazioni Gold.

## 5. Controllo duplicati, esposizione e indipendenza

Sono stati confrontati DOI, titolo completo e i cinque autori con:

- `evaluation/gold_s2_source_inventory_v1.json`: 34 fonti note, comprese nove
  fonti web storiche; SHA-256 del registro
  `43dfad66ca0e8915f7d47adab758c8a729bc67d53b6d825ed9889ced85f6df43`;
- `evaluation/gold_s2_catalog_metadata_export_v1.json`: 157 identita
  metadata-only; SHA-256
  `6749bc8ea8245aa7a41e7b06008639114679073b399eeb734a58ad79a456c174`.

Risultato deterministico: zero match esatti per DOI, titolo e nomi completi degli
autori in entrambi i file. Non sono emerse query esterne storiche specifiche per
questa fonte da riutilizzare.

Limiti: i metadati non escludono citazioni interne, abbreviazioni, versioni,
traduzioni, estratti, quasi duplicati, esposizione non registrata o affiniti
autoriali indirette. Pertanto ledger e source/document/version/author
disjointness restano `unknown`; il mancato match nominale non e indipendenza.

## 6. Record e validazione mirata

Record:
`evaluation/gold_s2_source_candidate_registry_v1.json`.

Il registro contiene un solo candidato reale, nessun record fittizio e nessuno
split. Comando eseguito con Python 3.13 locale:

```text
python.exe scripts/validate_gold_s2_source_candidate_registry_v1.py --registry evaluation/gold_s2_source_candidate_registry_v1.json
```

Risultato:

```text
STATUS VALID
ERRORS 0
UNVERIFIABLE 0
```

`VALID` attesta conformita del record preliminare al contratto, compresa la
decisione conservativa. Non equivale a eleggibilita, indipendenza o Gold validato.
Nessuna suite storica e stata ripetuta.

## 7. Decisioni ancora necessarie

1. Nominare il custode dei diritti e approvare policy retention/pubblicazione.
2. Valutare umanamente CC BY per i tre ambiti operativi e registrare una decisione
   attribuibile.
3. Approvare esclusione dei 157 documenti e delle nove fonti web.
4. Approvare la policy author-disjoint.
5. Completare ledger di esposizione e screening di duplicati/versioni/autori.
6. Autorizzare separatamente eventuale annotazione e assegnazione di split.

Fino ad allora il candidato resta `blocked_unknown`, `proposed_split=null` e
`gold_s2_provenance_record_id=null`.

## 8. Stati ufficiali

- Registrazione della prima fonte: **ESEGUITO**.
- Conformita strutturale del record: **VALIDATO**.
- Verifica byte PDF: **VALIDATO**.
- Verifica sostanziale diritti e indipendenza: **BLOCCATO**.
- Selezione, annotazione, Gold S2, freeze e S2: **BLOCCATO**.

Nessuna VPS, Chroma, collection, embedding, RAG, inferenza, benchmark, panel o
deploy e stato modificato o eseguito.
