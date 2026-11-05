# Gold S2 — piano operativo per fonti indipendenti

Attivita: `RD-TSC-V2-D3-S2-INDEPENDENT-SOURCE-ACQUISITION-PLAN-01`

Data: 2026-11-05

Baseline: `b09e1e0e823ec2e2e68139ce8373963a2a11b39e`

## Attivita → Script → Commit → Report → Risultato → Decisione → Stato

- Attivita: definire il percorso operativo per acquisire e qualificare fonti
  indipendenti destinate a un futuro Gold S2.
- Script: nessuno; sola riconciliazione documentale di contratti e risultati.
- Commit: unico commit documentale con report, TODO e registro.
- Report: questo documento.
- Risultato: politica di ammissibilita, canali, registro candidati, ruoli, gate,
  roadmap e modello di capacita definiti senza creare candidati.
- Decisione: partire solo dopo le decisioni del titolare su diritti, esclusione
  del corpus noto, ruoli e budget; volume 390/606 rinviato al pilot misurato.
- Stato: pianificazione **ESEGUITO**; acquisizione **DA FARE**; selezione e Gold
  S2 **BLOCCATO**.

## 1. Stato probatorio consolidato

- Catalogo operativo: 157/157 identita, 6.410 chunk, provenienza operativa
  completa nel perimetro API.
- Inventario storico: 34 fonti, di cui 25 riconciliate col catalogo e nove fonti
  web esterne gia esposte a benchmark.
- Nuove identita catalogo rispetto all'inventario: 132.
- Digest esposti dal catalogo: zero; diritti verificati: zero; holdout attestati:
  zero.
- Tutti i 157 documenti sono gia indicizzati. Possono sostenere sviluppo e
  diagnostica, ma non sono automaticamente indipendenti.
- Schema, manifest e validatore Gold S2 V1 sono **IMPLEMENTATO** e **VALIDATO
  offline** sulle proprieta deterministiche. Nessun caso reale o freeze esiste.
- TSC V2/D3/S1 conserva i propri stati offline; Gold S2 non autorizza la
  ripetizione dei relativi test.

Decisione metodologica applicata: assenza di prova di contaminazione non equivale
a indipendenza. Una fonte con diritti non verificati non entra nella raccolta Gold.

## 2. Politica di ammissibilita proposta

### 2.1 Requisiti obbligatori prima della raccolta

| Requisito | Evidenza minima | Fail-closed |
|---|---|---|
| identita | titolo, autore/organizzazione, tipo e ID stabile | identita ambigua → esclusa |
| versione | edizione/versione, lingua e data o dichiarazione motivata di univocita | versione ignota → non selezionabile |
| provenienza | fonte originaria e catena di acquisizione | provenienza indiretta/non verificabile → esclusa |
| integrita | SHA-256 dei byte autorizzati, dimensione e data acquisizione UTC | digest mancante → nessun freeze |
| diritti | licenza o autorizzazione firmata/riferibile con ambito esplicito | `unknown` → raccolta Gold vietata |
| conservazione | custode, luogo, durata, accesso e cancellazione | policy assente → acquisizione sospesa |
| annotazione | permesso di estrarre passaggi e creare label/derivati interni | permesso assente → annotazione vietata |
| pubblicazione | permesso o divieto esplicito per dataset, estratti, hash e report | stato ignoto → nessuna pubblicazione |
| esposizione | ledger di uso pregresso in RAG, benchmark, remediation e modelli | storia incompleta → holdout vietato |
| duplicazione | hash esatti e cluster dichiarato per versioni/traduzioni/estratti | cluster incerto → split sensibili vietati |
| indipendenza | source/document/version disjoint; policy autore applicata | conflitto → sviluppo soltanto o esclusione |
| responsabilita | revisore e data della decisione con evidence refs | decisione anonima → non valida |

### 2.2 Requisiti desiderabili

- metadati bibliografici pubblici e persistenti;
- licenza standard machine-readable;
- fonte primaria anziche copia o aggregatore;
- diversita per fase, livello, genere, contesto, scuola e organizzazione;
- documentazione editoriale e numerazione stabile;
- disponibilita pluriennale e condizioni di revoca definite;
- autore/organizzazione non presenti nei cluster di sviluppo.

I desiderabili migliorano qualita e riproducibilita ma non sostituiscono alcun
obbligo. Una fonte pubblicamente scaricabile senza licenza resta non autorizzata.

### 2.3 Decisioni di eleggibilita

- `eligible_development`: diritti e identita validi; indipendenza non richiesta o
  esposizione ammessa.
- `eligible_calibration`: disgiunta dallo sviluppo secondo policy approvata, ma
  destinata a taratura e quindi non a stime finali.
- `eligible_holdout`: tutti i requisiti PASS, nessuna esposizione proibita e
  cluster disgiunti.
- `eligible_adversarial`: requisiti PASS e famiglia disgiunta dalle remediation;
  puo essere ritirata se usata per correggere il sistema.
- `ineligible`: conflitto dimostrato o diritti incompatibili.
- `blocked_unknown`: informazione obbligatoria assente. Non equivale a eleggibile.

## 3. Canali di acquisizione

| Canale | Reperimento futuro | Prova diritti | Costo/tempo indicativo | Qualita/diversita | Rischi e criterio di esclusione |
|---|---|---|---|---|---|
| documentazione federale | accordo con federazione/settore tecnico o catalogo ufficiale | licenza/lettera che copra annotazione e derivati | lead time esterno, spesso settimane o mesi; costo variabile | alta autorita, possibile concentrazione di scuola | pubblico non significa riutilizzabile; escludere se permesso ambiguo |
| pubblicazioni didattiche con licenza | editori/repository con licenza esplicita | testo licenza, versione e URL persistente | giorni-settimane; costo basso/medio | buona riproducibilita, qualita variabile | licenze non compatibili con estratti/derivati; copie non ufficiali |
| materiali formativi autorizzati | enti, corsi, accademie | accordo dell'ente e titolarita dei contributi | settimane; costo/negoziazione medi | casi applicativi ricchi, rischio di omogeneita | partecipanti/autori non autorizzati o materiale confidenziale |
| contributi originali di tecnici | call o incarico con brief neutro | cessione/licenza firmata e consenso alla valutazione | settimane; compenso professionale | alta diversita controllabile | autore esposto al sistema o brief orientato ai difetti noti |
| concessione diretta autore | contatto individuale sul documento esistente | autorizzazione nominativa, versione e ambiti | variabile, dipendenza forte dalla risposta | fonte primaria e chiarimenti disponibili | catena diritti incompleta, coautori/editori non coperti |
| open access verificato | repository istituzionali/DOI | licenza esatta per versione e derivati | giorni per screening; costo basso | ampiezza potenziale, lingue/qualita eterogenee | etichetta open access generica, licenza revocata o versione diversa |
| casi originali commissionati | produzione cieca da esperti indipendenti | contratto su testo, annotazione, conservazione e pubblicazione | costo piu alto; pianificabile in settimane | massimo controllo su copertura e novita | contaminazione se il brief espone output/modello o se gli autori annotano i propri casi |

Priorita raccomandata per la prima fattibilita: combinare open access con licenza
verificabile, concessioni dirette e casi originali commissionati. Questo riduce la
dipendenza da un solo canale. Non e una selezione di fonti reali.

## 4. Procedura diritti e provenienza

1. Il responsabile acquisizione apre un record senza contenuto e indica canale,
   titolare presunto e versione.
2. Il custode verifica titolarita, coautori/editore e testo legale applicabile.
3. L'evidenza diritti riceve ID, digest, data, ambito e condizioni; il documento
   legale resta in deposito ad accesso ristretto, non necessariamente in Git.
4. Sono registrati separatamente permessi per conservazione, annotazione,
   trasformazioni, condivisione interna, pubblicazione di estratti e pubblicazione
   del dataset derivato.
5. Ogni permesso ha stato `verified`, `denied`, `expired` o `unknown`.
6. Solo tutti gli ambiti necessari `verified` consentono la fase pertinente.
7. Revoca/scadenza blocca nuovi usi e attiva la procedura di retention; non
   riscrive retroattivamente i risultati, che vengono ritirati/versionati.

Il validatore verifica riferimenti e digest, non interpreta il diritto: la decisione
resta umana e attribuibile.

## 5. Procedura di indipendenza

### 5.1 Evidenze obbligatorie

- digest byte e fingerprint normalizzato;
- `source_id`, `document_id`, versione, lingua, autore e organizzazione;
- cluster di traduzioni, edizioni, estratti e quasi duplicati;
- ledger di esposizione per dataset, retrieval, generazione, benchmark, NLI,
  alignment, claim-fidelity, Gold E/V, D3/S1, remediation e valutazioni;
- confronto con le 157 identita operative, le nove fonti web e i registri futuri;
- decisione firmata del revisore indipendenza con riferimenti probatori.

### 5.2 Regole

1. `source-disjoint`: nessun source cluster comune.
2. `document-disjoint`: nessun documento, estratto sovrapposto o digest comune.
3. `version-disjoint`: traduzioni/edizioni/derivati restano nello stesso cluster
   finche una revisione umana non dimostra indipendenza sostanziale e legale.
4. `author-disjoint`: applicato come requisito assoluto o stratificazione secondo
   decisione preventiva del titolare; mai dichiarato se `author_group` e incompleto.
5. Sviluppo, calibrazione, holdout e adversarial hanno registri separati; nessun
   caso migra verso uno split piu indipendente.
6. Una fonte/caso usato per remediation viene ritirato dalle future stime holdout.
7. Modelli e predizioni restano nascosti durante A/B/C e non decidono eligibility.

Informazione mancante produce `blocked_unknown`; non si usa inferenza nominale o
somiglianza del titolo per promuovere la fonte.

## 6. Schema del futuro registro candidati

Contratto proposto, da implementare solo dopo approvazione:

```json
{
  "schema_version": "gold_s2_source_candidate_registry_v1",
  "candidate_id": "candidate:...",
  "source_id": "source:...",
  "title": "...",
  "author": [{"name": "...", "authority_id": null}],
  "organization": {"name": "...", "authority_id": null},
  "version": {"edition": "...", "date": "...", "language": "..."},
  "provenance": {"channel": "...", "origin_ref": "...", "acquired_at": null},
  "digest": {"algorithm": "sha256", "value": null, "verified": false},
  "rights_evidence": [{"evidence_id": "rights:...", "status": "unknown", "scope": []}],
  "retention_policy": {"policy_id": null, "status": "unknown"},
  "annotation_permission": "unknown",
  "publication_permission": "unknown",
  "historical_exposure": [{"system": "...", "status": "unknown", "evidence_refs": []}],
  "duplicate_cluster": null,
  "author_cluster": null,
  "proposed_split": null,
  "eligibility_decision": "blocked_unknown",
  "evidence_refs": [],
  "reviewer": null,
  "decision_date": null
}
```

Regole: nessun `candidate_id` senza una fonte reale acquisita legittimamente; ID
non implica eligibility; `null/unknown` fail-closed; nessuno split definitivo prima
della matrice e dello screening completi. Lo schema Gold S2 esistente non richiede
modifiche: il registro alimenta il provenance record prima della creazione casi.

## 7. Dimensionamento progressivo

Gli split validati restano invariati:

| Variante | Sviluppo | Calibrazione | Holdout | Adversarial | Totale |
|---|---:|---:|---:|---:|---:|
| ridotta | 60 | 90 | 180 | 60 | 390 |
| raccomandata | 72 | 144 | 300 | 90 | 606 |

Sequenza obbligatoria:

1. qualificazione metadata;
2. diritti;
3. indipendenza;
4. pilot di capacita/tempo escluso dal Gold;
5. scelta 390 o 606;
6. acquisizione controllata;
7. review A/B cieca;
8. adjudication C;
9. QA D;
10. freeze content-addressed;
11. S2 shadow con autorizzazione separata.

Il volume non viene scelto ora. Per 606 il design stima 202–303 ore per A+B,
esclusi selezione, diritti, C, D e freeze. Applicando la stessa ipotesi di 10–15
minuti per revisione indipendente, 390 richiede 130–195 ore A+B. Questa e una
derivazione di pianificazione, non un tempo osservato. Un pilot umano deve misurare
tempo mediano/p95, disaccordi, esclusioni e casi prodotti per documento.

## 8. Organizzazione umana

| Ruolo | Responsabilita | Separazione richiesta |
|---|---|---|
| custode fonti/diritti | conserva originali e prove legali, applica retention | non decide label scientifiche |
| responsabile acquisizione | contatti, versioni, digest e catena di custodia | non approva da solo diritti/holdout |
| revisore indipendenza | screening exposure e cluster | non autore della fonte ne sviluppatore del caso |
| annotatore A | label, span, rationale ciechi | indipendente da B e senza predizioni |
| annotatore B | seconda review cieca | indipendente da A e senza predizioni |
| adjudicator C | risolve disaccordi motivando | non sostituisce A/B; vede entrambi solo dopo chiusura |
| QA D | completezza, digest, split, diritti, conflitti | non riscrive label |
| responsabile freeze | canonicalizzazione, manifest e hash | opera solo dopo PASS di D e titolare |
| responsabile S2 | esecuzione shadow e report | non accede alle label holdout prima del freeze |

Il titolare puo autorizzare una persona a piu ruoli non confliggenti, ma A/B devono
restare indipendenti; C e D devono essere distinti dalle decisioni che controllano.
Codex/Qwen possono assistere controlli meccanici, mai simulare doppia revisione umana.

## 9. Roadmap esecutiva a cancelli

| ID futuro | Obiettivo/evidenza nuova | Prerequisiti | Accettazione | Arresto | Stato iniziale/decisione |
|---|---|---|---|---|---|
| `RD-S2-SOURCE-POLICY-APPROVAL-01` | decisione firmata su corpus escluso, licenze, retention, pubblicazione e author policy | titolare + custode | policy versionata e proprietari nominati | qualsiasi ambito `unknown` | **DA FARE**; approvazione titolare |
| `RD-S2-CANDIDATE-REGISTRY-V1-01` | schema/validator del registro, zero candidati | policy approvata | fail-closed, evidence refs e compatibilita Gold S2 | incompatibilita concreta col contratto | **DA FARE**; autorizzazione tecnica |
| `RD-S2-SOURCE-CHANNEL-PILOT-01` | evidenze reali da piu canali, senza annotazione | budget/contatti/registro | identita, digest, diritti ed esposizione verificabili | download/licenza non autorizzati | **BLOCCATO**; autorizzazione acquisizione |
| `RD-S2-INDEPENDENCE-SCREEN-01` | matrice cluster/esposizione dei candidati | candidate records completi | decisioni attribuibili, unknown conservati | storia incompleta per holdout | **BLOCCATO**; policy autore/split |
| `RD-S2-CAPACITY-TIMING-PILOT-01` | misura umana di claim/caso, tempi e disaccordi; casi esclusi dal Gold | fonti autorizzate e ruoli A/B/C/D | statistiche osservate e nessun riuso holdout | campione non rappresentativo/diritti insufficienti | **BLOCCATO**; autorizzazione annotazione pilot |
| `RD-S2-VOLUME-DECISION-01` | scelta 390/606 con costi e fonti dimostrate | pilot completato | copertura/split/risorse finanziate | capacita insufficiente | **BLOCCATO**; decisione titolare |
| `RD-S2-GOLD-BUILD-01` | dataset A/B/C/D completo | volume e fonti approvati | ledger completo, QA PASS | conflitti/diritti/indipendenza | **BLOCCATO** |
| `RD-S2-GOLD-FREEZE-01` | manifest frozen content-addressed | build e QA completi | hash/riferimenti/split riconciliati e approvazione | dato non verificabile | **BLOCCATO** |
| `RD-S2-SHADOW-01` | valutazione S2 sul Gold congelato | freeze e protocollo approvati | report content-addressed, nessuna remediation sul holdout | leak/config divergente | **BLOCCATO** |

La roadmap evita passaggi puramente descrittivi: ogni fase futura deve produrre
policy approvata, contratti verificabili, prove diritti, record reali, misure umane
o artefatti congelati.

## 10. Matrice rischi

| Rischio | Probabilita/Impatto | Mitigazione | Stop |
|---|---|---|---|
| diritti ambigui | alta/critico | custode e scope separati | nessuna acquisizione/annotazione |
| contaminazione non documentata | alta/alto | ledger ed esclusione fail-closed | niente holdout |
| quasi duplicati/traduzioni | medio-alta/alto | digest + cluster + review umana | split sensibili bloccati |
| concentrazione autore/scuola | media/alto | quote congelate e metriche stratificate | volume non approvato |
| claim capacity insufficiente | ignota/alto | pilot escluso dal Gold | non scegliere 390/606 |
| disaccordo A/B elevato | ignota/medio-alto | misura pilot, C e tassonomia | sospendere scala |
| revoca licenza | medio/critico | policy retention/versioning | ritirare nuova versione |
| leak holdout | medio/critico | accessi separati e audit | ritirare casi compromessi |
| automazione spacciata per review | medio/critico | ruoli umani attribuiti | freeze vietato |
| costi/lead time esterni | alta/medio | canali multipli e gate progressivi | ridimensionare dopo pilot |

## 11. Tempi, risorse e dipendenze

Le finestre sono intervalli di pianificazione condizionati, non promesse:

| Fase | Lavoro umano | Automatizzabile | Dipendenza/ordine di grandezza |
|---|---|---|---|
| policy e ruoli | titolare, legale/custode | form/checklist | giorni se decisioni disponibili |
| reperimento | contatti e negoziazione | tracking | settimane; mesi per accordi istituzionali |
| verifica diritti | revisione legale/amministrativa | digest e coerenza campi | giorni-settimane per fonte/canale |
| screening indipendenza | giudizio cluster/esposizione | hash, join registri | giorni dopo metadata completi |
| pilot capacita | A/B/C/D | worksheet/metriche | durata da misurare; non stimabile ora |
| annotazione A+B | 130–195 h (390) o 202–303 h (606) | validazioni meccaniche | dopo decisione volume |
| adjudication C | dipende dal tasso di disaccordo osservato | code e ledger | formula: casi in conflitto × tempo mediano C |
| QA D | dipende da casi/esclusioni | schema/hash/referential checks | dopo C |
| freeze | approvazione e custody | canonicalizzazione/hash | giorni se tutti i gate PASS |

Risorse minime: custode/diritti, responsabile acquisizione, revisore indipendenza,
due annotatori, adjudicator, QA, responsabile freeze e responsabile S2. Servono
budget per licenze/commissioni, deposito controllato e tempo umano. Nessun modello
riduce legittimamente il fabbisogno A/B indipendente.

Valutazione: 390 e piu sostenibile come prima costruzione solo se il pilot dimostra
fonti, copertura e precisione compatibili con l'obiettivo; offre intervalli meno
stretti. 606 resta scientificamente preferibile secondo il design, ma non e
finanziabile o fattibile sulla sola evidenza corrente. Nessuna variante e approvata.

## 12. Percorso scientifico e percorso tecnico

**Scientifico:** nuove fonti → diritti → indipendenza → pilot → volume → A/B/C/D →
freeze → S2 shadow. Rimane BLOCCATO ai primi gate decisionali.

**Tecnico:** TSC V2/D3/S1 mantiene la validazione offline gia registrata. Puo
evolvere solo con incarichi separati e non viene promosso a INTEGRATO o CERTIFICATO
dal Gold. Nessun test TSC gia concluso deve essere ripetuto per giustificare la
raccolta fonti.

## 13. Condizioni generali di arresto

- identita/versione o titolarita ambigua;
- licenza non verificata o incompatibile con la fase;
- esposizione/cluster incompleti per un candidato holdout;
- conflitto di ruoli A/B/C/D;
- accesso delle persone alle predizioni prima del freeze;
- capacita annotativa o copertura non dimostrata;
- perdita della catena di custodia o digest divergente;
- richiesta di pubblicare dati oltre il permesso;
- tentativo di scegliere volume o split dopo aver osservato risultati modello.

Ogni stop conserva le evidenze e lo stato `blocked_unknown`/`ineligible`; non crea
candidati sostitutivi opportunistici.

## 14. Decisioni richieste al titolare

1. Escludere o meno tutti i 157 documenti e le nove fonti web dal holdout.
2. Approvare la politica obbligatoria di diritti, retention e pubblicazione.
3. Nominare custode, responsabile acquisizione, revisore indipendenza, A/B/C/D,
   freeze e S2; dichiarare conflitti.
4. Stabilire se author-disjoint sia assoluto o una stratificazione obbligatoria.
5. Approvare i canali e un budget massimo per il solo pilot di acquisizione.
6. Autorizzare separatamente schema/validator del registro candidati vuoto.
7. Autorizzare poi un pilot di canale senza annotazione; nessun download prima.
8. Rinviare 390/606 fino alle misure di capacita e costo umano.

## 15. Stati ufficiali

- Piano acquisizione fonti: **ESEGUITO**.
- Design e schema/validator Gold S2: stati precedenti **VALIDATO** / **VALIDATO
  offline**, invariati.
- Policy, ruoli e registro candidati: **DA FARE**.
- Acquisizione fonti: **DA FARE** previa autorizzazione.
- Selezione, annotazione, adjudication, QA, freeze, Gold S2 e S2 shadow:
  **BLOCCATO**.
- TSC V2/D3/S1: stati offline invariati; nessuna integrazione o certificazione.

Questo piano non autorizza alcuna fase operativa successiva.
