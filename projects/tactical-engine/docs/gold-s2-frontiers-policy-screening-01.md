# Gold S2 — policy minima proposta e screening Frontiers

Attivita: `RD-S2-FRONTIERS-POLICY-SCREENING-01`

Data: 2026-11-05

Baseline: `76f9e81c05aeaff954de868cd51ae6c0d5557343`

## Attivita → Script → Commit → Report → Risultato → Decisione → Stato

- Attivita: predisporre una policy minima e riesaminare l'eleggibilita della
  fonte Frontiers con le sole evidenze gia disponibili.
- Script: nessuno; Candidate Registry e validatore invariati.
- Commit: unico commit documentale.
- Report: questo documento.
- Risultato: policy proposta, screening completato, nessuna promozione possibile.
- Decisione: screening **ESEGUITO**; policy **DA FARE**; candidato **BLOCCATO**.

## 1. Evidenze riconciliate

La fonte e la version of record inglese dell'articolo Frontiers DOI
`10.3389/fspor.2022.1019990`. Identita, provenienza e PDF da 654208 byte con
SHA-256 `8742bfaa21170df3a63ad53c7486ee62e6b39ceef168d6c3bdeab29fdb04bc31`
erano gia verificati e non sono stati riacquisiti.

La pagina ufficiale Frontiers conferma copyright 2022 degli autori e licenza
Creative Commons Attribution. La dichiarazione consente uso, distribuzione e
riproduzione con credito agli autori e titolari e citazione della pubblicazione:

- `https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.1019990/full`;
- `https://creativecommons.org/licenses/by/4.0/legalcode.en`.

CC BY 4.0 consente riproduzione, condivisione e adattamento in ogni formato,
soggetti ad attribuzione, link alla licenza, indicazione delle modifiche e
divieto di restrizioni aggiuntive. La licenza copre soltanto i diritti che il
licenziante puo concedere; diritti morali, privacy, publicity ed eventuali
materiali di terzi possono richiedere verifiche separate.

Non e stata identificata nelle evidenze esaminate una marcatura specifica che
escluda singoli elementi dell'articolo dalla licenza. Questo dato non dimostra
che ogni possibile contenuto di terzi sia utilizzabile senza ulteriori controlli.

## 2. Policy minima proposta — non approvata

1. Uso esclusivamente interno per qualificazione e futuro sviluppo Gold S2.
2. Accesso ai byte e ai derivati limitato ai soggetti autorizzati e registrato.
3. Conservazione in deposito controllato per una durata ancora da approvare;
   nessuna durata viene presunta da questo report.
4. Registrazione obbligatoria di origine, DOI/versione, digest, licenza,
   attribuzione completa e modifiche apportate.
5. Procedura di cancellazione o ritiro in caso di errore di identita/licenza,
   revoca applicabile, scadenza di policy o decisione del titolare; gli esiti
   derivati vengono ritirati/versionati, non riscritti silenziosamente.
6. Nessuna pubblicazione esterna di PDF, estratti, annotazioni o dataset senza
   autorizzazione separata e verifica delle condizioni applicabili.
7. Custode dei diritti, revisori scientifici e responsabile del freeze sono ruoli
   distinti. Nessuna persona viene nominata da questo report.

`approval_status=not_approved`, custode nullo e permessi operativi `unknown`
restano corretti fino a decisione umana attribuibile.

## 3. Politica di indipendenza proposta — non approvata

- escludere i 157 documenti indicizzati da calibration e holdout;
- escludere le nove fonti web storicamente esposte;
- mantenere versioni, traduzioni, estratti e quasi duplicati nello stesso cluster
  finche una revisione documentata non dimostri il contrario;
- applicare author-disjoint stretto a calibration e holdout;
- registrare ogni esposizione nota mediante evidence refs;
- non convertire l'assenza di match esatti in prova di indipendenza;
- destinare a development soltanto fonti con diritti operativi approvati e
  screening attribuibile, accettando che development non sia holdout.

## 4. Screening Frontiers

| Requisito | Esito | Evidenza o limite |
|---|---|---|
| identita bibliografica | verificato | DOI, titolo, autori, rivista e data ufficiali |
| versione | verificato | version of record inglese |
| integrita | verificato | digest byte gia registrato |
| dichiarazione CC BY | verificato | pagina Frontiers e licenza CC BY 4.0 |
| retention operativa | dipende da approvazione | licenza compatibile in linea tecnica; custode, durata e deposito non approvati |
| annotazione interna | dipende da approvazione | adattamento consentito in linea tecnica; policy e attribuzione non approvate |
| pubblicazione | dipende da approvazione | CC BY consente condivisione a condizioni; progetto vieta pubblicazione senza decisione separata |
| materiali di terzi | non verificabile integralmente | nessuna esclusione specifica osservata; altri diritti non coperti restano possibili |
| match esatti inventario 34 | verificato assente | confronto DOI/titolo/autori gia registrato |
| match esatti catalogo 157 | verificato assente | confronto metadata-only gia registrato |
| esposizione storica completa | non verificabile | registri incompleti per citazioni, estratti e usi non tracciati |
| source disjoint | non verificabile | assenza nominale non prova cluster disgiunto |
| document disjoint | non verificabile | nessun confronto completo di estratti/quasi duplicati |
| version disjoint | non verificabile | traduzioni e versioni indirette non inventariate integralmente |
| author disjoint | non verificabile | autorita/autori del catalogo 157 non disponibili |
| compatibilita development | verificata con limite | pertinente a analytics/coaching; pilot circoscritto, non fonte tattica universale |

La fonte non puo essere promossa a calibration o holdout. Development e una
destinazione potenziale, non assegnata, subordinata a policy, diritti e decisione
umana sul rischio di esposizione residuo.

## 5. Candidate Registry

Il file `evaluation/gold_s2_source_candidate_registry_v1.json` non e stato
modificato. Non esiste nuova evidenza attribuibile sufficiente per cambiare:

- `policy.approval_status=not_approved`;
- `rights_custodian_id=null`;
- retention, annotazione e pubblicazione `unknown`;
- disjointness ed esposizione `unknown`;
- `proposed_split=null`;
- `eligibility_decision=blocked_unknown`.

Poiche il registro e byte-invariato, il validatore non e stato rieseguito.

## 6. Decisioni riservate al titolare

1. nominare il custode dei diritti;
2. approvare durata, deposito, accessi e cancellazione della retention policy;
3. approvare o negare annotazione interna e definire l'attribuzione obbligatoria;
4. mantenere vietata o autorizzare separatamente la pubblicazione esterna;
5. approvare la policy di indipendenza e autorizzare uno screening attribuibile
   per decidere l'eventuale sola eleggibilita development.

## 7. Stati

- Policy minima: **DA FARE** fino ad approvazione.
- Screening documentale Frontiers: **ESEGUITO**.
- Identita, versione, digest e dichiarazione CC BY: **VALIDATO** nel perimetro
  documentale gia acquisito.
- Diritti operativi e indipendenza: **BLOCCATO**.
- Candidato Frontiers: `blocked_unknown`, **BLOCCATO**.
- Annotazione, split, freeze e Gold S2: **BLOCCATO**.
- Accuratezza S2, Gate, integrazione e certificazione: **BLOCCATO**.

Nessun download, scraping, annotazione, test, inferenza, benchmark, runtime,
VPS, Chroma, API, pannello, freeze o modifica tecnica e stato eseguito.
