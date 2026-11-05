# Gold S2 Candidate Registry V1 — implementazione offline

Attivita: `RD-S2-CANDIDATE-REGISTRY-V1-01`

Data: 2026-11-05

Baseline: `301b9cdadd231f157186fe05a8f61a943564eadf`

Commit tecnico: `a49d0ee096a4d0592fb87d893aa1cdd2c5e6d1a9`

## Attivita → Script → Commit → Report → Risultato → Decisione → Stato

- Attivita: implementare il registro preliminare delle fonti candidate Gold S2.
- Script: `scripts/validate_gold_s2_source_candidate_registry_v1.py`.
- Commit: commit tecnico sopra indicato; commit documentale separato.
- Report: questo documento.
- Risultato: schema versionato, template vuoto, validatore fail-closed e 17 test
  sintetici differenziali.
- Decisione: infrastruttura **IMPLEMENTATO**, test **ESEGUITO**, proprieta
  deterministiche coperte **VALIDATO offline**; acquisizione **DA FARE** previa
  autorizzazione; candidati reali, Gold e S2 **BLOCCATO**.

## 1. Confronto con i contratti esistenti

Il validatore Gold S2 V1 gia validato controlla dataset, provenance record, casi,
review A/B/C, QA D e freeze. Non qualifica una fonte prima della costruzione dei
casi e non interpreta diritti, esposizione o indipendenza di un candidato.

Candidate Registry V1 e uno strato precedente e autonomo. Non modifica schema,
template o validatore Gold S2. Un futuro candidato qualificato puo dichiarare
`gold_s2_provenance_record_id`; il collegamento non crea automaticamente un
provenance record, un caso o uno split e resta soggetto al validatore Gold.

## 2. File implementati

- `evaluation/annotations/gold_s2_source_candidate_registry_schema_v1.json`:
  JSON Schema Draft 2020-12, versione
  `gold_s2_source_candidate_registry_v1`.
- `evaluation/annotations/gold_s2_source_candidate_registry_template_v1.json`:
  registro draft vuoto, policy conservative e zero candidati.
- `scripts/validate_gold_s2_source_candidate_registry_v1.py`: validatore Python
  offline senza nuove dipendenze.
- `tests/test_validate_gold_s2_source_candidate_registry_v1.py`: fixture solo
  sintetiche e 17 controlli differenziali.

## 3. Contratto e regole fail-closed

Il contratto registra identita bibliografica, versione, lingua, provenienza,
digest, prove dei diritti per ambito, retention, permessi, ledger di esposizione,
source/document/version/author disjointness, cluster, split proposto, decisione,
revisore, data e riferimenti probatori.

Una promozione `eligible_*` richiede congiuntamente:

- policy globale approvata e acquisizione autorizzata;
- custode dei diritti e policy retention/pubblicazione approvati;
- provenienza verificata;
- SHA-256 dei byte con evidenza verificata, distinto da digest dichiarato;
- diritti `verified` separati per retention, annotazione e pubblicazione;
- permessi e retention verificati;
- source/document/version disjointness `pass`;
- revisore, data, motivazione ed evidence refs risolvibili;
- corrispondenza esatta tra decisione e split.

Per calibration, holdout e adversarial sono inoltre obbligatori ledger con
assenza verificata di esposizione, policy autore approvata, esito autore coerente
ed esclusione approvata del corpus noto e delle fonti web note. Ledger vuoto o
`unknown` non prova assenza. Cluster duplicati non possono attraversare split;
con policy autore assoluta, neppure gli author cluster.

Il validatore verifica forma, riferimenti e dichiarazioni; non certifica la
validita legale sostanziale delle licenze e non inventa digest o autorizzazioni.

## 4. Policy non approvate

Il template conserva in modo esplicito:

- `approval_status=not_approved`;
- esclusione corpus e web `unknown`;
- author policy `not_approved`;
- custode non assegnato;
- retention e pubblicazione non approvate;
- acquisizione non autorizzata.

Il registro e tecnicamente utilizzabile in questo stato e il registro vuoto e
valido, ma nessun candidato puo essere promosso. Restano **DA FARE** decisioni su
157 documenti, nove fonti web, author-disjoint, custode, retention,
pubblicazione, budget e acquisizione.

## 5. Test differenziali

Comando effettivamente eseguito con Python 3.13 locale:

```text
python.exe -m unittest projects/tactical-engine/tests/test_validate_gold_s2_source_candidate_registry_v1.py -v
```

Risultato: **17/17 PASS** in 0,035 s.

I casi coprono: template vuoto; candidato sintetico positivo; ID duplicato;
riferimento mancante; digest malformato; digest dichiarato non verificato;
diritti assenti, scaduti o revocati; ledger vuoto; esposizione incompatibile;
conflitto duplicate cluster; author policy non approvata; policy globale
mancante; promozione holdout indebita; revisore mancante; decisione senza
evidenza; collegamento strutturale pre-caso al provenance Gold S2.

Non sono equivalenti ai test Gold S2 esistenti: operano sulla qualificazione
della fonte prima di provenance, casi e freeze. Nessuna suite storica e stata
rieseguita. Il tentativo iniziale con il launcher Windows `py -3` non ha eseguito
test perche il launcher non rilevava l'interprete; e stato usato l'interprete
Python 3.13 gia installato, senza installazioni.

## 6. Compatibilita Gold S2

- contratto e validatore Gold S2 esistenti: invariati;
- nessuna dipendenza runtime nuova;
- nessun popolamento automatico del Gold;
- nessun caso, label, split o freeze creato;
- `gold_s2_provenance_record_id` e solo un riferimento futuro esplicito e non
  promuove il candidato.

## 7. Limiti e decisioni richieste

Il controllo legale resta umano. Le date sono registrate ma la validita temporale
sostanziale e la revoca devono essere accertate dal custode. L'assenza verificata
nel ledger dipende dalla completezza dei sistemi dichiarati. La similarita
semantica e i quasi duplicati richiedono una fase separata autorizzata.

Prima di acquisire fonti il titolare deve approvare politica, esclusioni,
author-disjoint, custode, retention, pubblicazione, budget e canali. In seguito
serviranno autorizzazioni distinte per record reali, screening, annotazione,
freeze e S2.

## 8. Stati ufficiali

- Candidate Registry V1: **IMPLEMENTATO**.
- Test differenziali: **ESEGUITO**.
- Proprieta deterministiche testate: **VALIDATO offline**.
- Policy e nomine: **DA FARE**.
- Acquisizione fonti: **DA FARE**, non autorizzata da questa attivita.
- Candidati reali, selezione, Gold S2, freeze e S2: **BLOCCATO**.
- Integrazione e certificazione: non conseguite.

Nessun download, scraping, documento reale, inferenza, retrieval, Chroma,
benchmark, Gate, VPS, deploy, merge o modifica al panel e stato eseguito.
