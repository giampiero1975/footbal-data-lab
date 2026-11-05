# TSC V2 D3 — design Gold S2 indipendente

Attività: `RD-TSC-V2-D3-S2-INDEPENDENT-GOLD-DESIGN-01`

Data: 2026-11-05

Baseline: `c9131d7304b64fb12f960f35d61a0df4d7ca407c`

## Attività → Script → Commit → Report → Risultato → Decisione → Stato

- Attività: progettazione documentale di un Gold S2 claim-evidence indipendente.
- Script: nessuno eseguito; sole letture statiche di contratti, dataset, codice e
  report già presenti.
- Commit: commit esclusivamente documentale di report, TODO e registro.
- Report: questo documento.
- Risultato: definiti record, tassonomia, split, indipendenza, doppia revisione,
  adjudication, freeze, protocollo futuro e carico di annotazione.
- Decisione: il design è completo; popolamento e valutazione richiedono decisioni e
  autorizzazioni separate.
- Stato: design **VALIDATO**; raccolta, annotazione, freeze e S2 **BLOCCATO**.

## 1. Riconciliazione

Branch e HEAD locale coincidevano con la baseline, il working tree era pulito e il
remoto autorevole era `github`. Sono stati letti TODO, experiment register, readiness
S2, recupero probatorio, design semantic support e implementazione S1. Sono stati
ispezionati contratti Gold E/V v1/v2, provenance registry, ledger A/B/C, manifest di
freeze, worksheet umano, set claim-fidelity e campagne NLI documentate.

Non esiste un Gold S2 equivalente. I template Gold E/V v2 hanno zero casi e misurano
estrazione/verifica relazionale. I set claim-fidelity presenti contano 16, 18, 24 e
20 casi, ma sono stati usati nello sviluppo o nella diagnostica e non hanno insieme
doppia revisione cieca, adjudication, freeze e indipendenza. Gli undici originali
NLI/alignment cercati nel closeout precedente sono `NON_REPERITO`; le metriche
aggregate storiche non vengono promosse né ricostruite.

Nessun test, modello, benchmark, retrieval, Chroma, annotazione o caso Gold è stato
eseguito o prodotto.

## 2. Gold E/V e Gold S2

| Oggetto | Unità | Domanda scientifica | Etichette/esito |
|---|---|---|---|
| Gold E | domanda e requisiti | i requisiti tattici sono stati estratti correttamente? | atomi, provenienza e relazioni |
| Gold V | risposta e requisiti Gold E | la risposta soddisfa e rappresenta le relazioni richieste? | satisfied/not demonstrated/contradicted/ambiguous |
| Gold S2 | claim atomico ed evidenza congelata | l'evidenza dimostra, contraddice o non determina l'intero claim? | supported/contradicted/insufficient |

Gold E/V non diventa automaticamente Gold S2. Sono riutilizzabili soltanto
l'infrastruttura di provenienza, identità pseudonime dei revisori, ledger A/B/C,
adjudication, manifest content-addressed, freeze e principio del worksheet non
distruttivo. Non sono riutilizzabili senza conversione semantica le etichette, i
denominatori o le decisioni Gold E/V.

## 3. Contratto minimo del record

Il futuro schema deve essere versionato separatamente, ad esempio
`tactical_semantic_support_gold_s2_v1`. Il seguente è il record normativo proposto;
non è stato creato alcun file dataset.

```json
{
  "schema_version": "tactical_semantic_support_gold_s2_v1",
  "case_id": "s2:...",
  "case_version": "1.0.0",
  "provenance_record_id": "provenance:...",
  "source": {
    "source_id": "source:...",
    "document_id": "document:...",
    "document_version": "...",
    "author_group_id": "author-group:...",
    "location_refs": ["page-or-section:..."],
    "source_sha256": "sha256:..."
  },
  "evidence": {
    "text": "testo congelato",
    "normalization": "utf8_nfc_lf_v1",
    "evidence_sha256": "sha256:...",
    "context_before": "",
    "context_after": "",
    "composition": "single_source"
  },
  "claim": {
    "text": "proposizione tattica atomica",
    "claim_sha256": "sha256:...",
    "context": "",
    "conditions": [],
    "quantifiers": [],
    "actors": [],
    "phase": "unknown",
    "relation_refs": [],
    "requirement_refs": []
  },
  "taxonomy": {
    "primary_category": "direct_literal_support",
    "cross_cutting_properties": []
  },
  "gold_label": "supported",
  "gold_rationale": {
    "evidence_spans": [{"start": 0, "end": 0}],
    "explanation": "motivazione verificabile",
    "scope_notes": "",
    "ambiguity": "none"
  },
  "reviews": {
    "review_a_id": "ledger:...:A",
    "review_b_id": "ledger:...:B",
    "adjudication_id": "ledger:...:C"
  },
  "freeze": {
    "status": "draft",
    "case_sha256": "sha256:...",
    "split_id": "holdout:...",
    "dataset_version": "..."
  }
}
```

Campi testuali e span sono congelati prima della valutazione. La forma canonica usa
il profilo v2 già implementato quando i tipi restano compatibili; il nuovo schema
deve avere il proprio ID e validatore, senza alterare gli hash Gold E/V.

### 3.1 Etichette

- `supported`: l'evidenza congelata dimostra l'intero claim nello stesso attore,
  fase, polarità, scope, condizioni e quantificatori. Una composizione multi-fonte è
  ammessa solo se dichiarata e ogni premessa necessaria è attribuibile.
- `contradicted`: l'evidenza afferma una proposizione incompatibile con almeno una
  componente necessaria del claim, nello stesso contesto e scope. Deve esistere una
  controaffermazione positiva; il silenzio non basta.
- `insufficient`: l'evidenza non dimostra l'intero claim e non lo contraddice
  positivamente, oppure il contesto è ambiguo, parziale o non attribuibile.

Un claim plausibile non è `supported`. Evidenza pertinente ma incompleta è
`insufficient`. I claim composti devono essere atomizzati prima del freeze; se una
composizione è mantenuta come caso adversarial, `supported` richiede supporto per
tutte le proposizioni, `contradicted` richiede una contraddizione positiva di una
componente necessaria e ogni altro misto è `insufficient`.

## 4. Tassonomia

Per evitare doppi conteggi, ogni caso ha una sola categoria primaria e zero o più
proprietà trasversali.

### 4.1 Categorie primarie

1. `direct_literal_support`: supporto diretto letterale;
2. `faithful_paraphrase`: parafrasi semanticamente fedele;
3. `partial_or_missing_support`: parafrasi parziale o evidenza pertinente ma
   insufficiente;
4. `explicit_incompatibility`: contraddizione positiva;
5. `valid_multi_source_support`: supporto congiunto lecito e attribuibile;
6. `invalid_multi_source_composition`: conclusione non implicata dalle fonti;
7. `context_dependent`: giudizio dipendente da contesto documentale congelato;
8. `terminological_ambiguity`: termine non risolvibile senza interpretazione non
   documentata.

### 4.2 Proprietà trasversali

- negazione;
- quantificatore universale/assoluto o ristretto;
- condizione necessaria, sufficiente od omessa;
- causalità corretta o invertita;
- attore corretto o errato;
- fase corretta o errata;
- scope/generalizzazione;
- relazione tattica complessa;
- claim multiproposizionale usato soltanto come controllo adversarial;
- quasi duplicato o variazione contrastiva;
- fonte singola o multipla;
- ambiguità terminologica;
- dipendenza dal contesto.

Le 24 classi richieste sono quindi tutte coperte, ma negazione, quantificatori,
condizioni, causalità, attore, fase, scope, complessità e composizione non generano
conteggi primari multipli. La matrice di selezione deve imporre copertura incrociata:
non sono ammessi split dominati da esempi letterali facili.

## 5. Numerosità e distribuzione

### 5.1 Proposta raccomandata

| Split | Casi | Etichette | Copertura | Indipendenza | Carico iniziale A+B |
|---|---:|---|---|---|---:|
| sviluppo | 72 | 24/24/24 | tutte le primarie; proprietà ad alta priorità | document-disjoint dagli altri split; non usato per stime finali | 24–36 h |
| calibrazione | 144 | 48/48/48 | matrice primaria × proprietà, incluse condizioni/scope | source/document-disjoint da sviluppo e holdout | 48–72 h |
| holdout indipendente | 300 | 100/100/100 | tutte le primarie e trasversali con quote pre-fissate | source- e document-disjoint; author-disjoint ove fattibile | 100–150 h |
| adversarial | 90 | 30/30/30 | contrasti minimi, composizione, quantificatori, causalità, ambiguità | famiglie/source cluster disjoint dal tuning | 30–45 h |
| **Totale** | **606** | **202/202/202** | — | — | **202–303 h** |

Il carico è una stima di pianificazione, non un costo approvato: 10–15 minuti per
ciascuna delle due revisioni indipendenti per caso. Non include selezione, diritti,
adjudication, QA o freeze. Un pilot temporale separato deve sostituire la stima con
misure osservate prima di impegnare il volume completo; il pilot non entra nel Gold.

Il holdout usa 100 casi per classe perché, nel caso binomiale peggiore, consente una
semiampiezza approssimativa del 95% di 9,8 punti percentuali per una proporzione di
classe. Sui 300 casi complessivi la semiampiezza peggiore è circa 5,7 punti. Questi
sono limiti descrittivi, non soglie di certificazione; stratificazione e dipendenza
fra casi possono ampliarli. Le classi rare e le analisi per categoria avranno
intervalli più larghi e devono essere pubblicate come esplorative.

### 5.2 Alternativa ridotta

Se il carico umano non è approvato: 60 sviluppo, 90 calibrazione, 180 holdout e 60
adversarial, bilanciati per classe (totale 390). Nel holdout 60 casi per classe danno
una semiampiezza peggiore approssimativa del 95% di 12,7 punti; non è idonea a stime
strette per sottocategoria. Il titolare deve scegliere volume raccomandato o ridotto
prima della selezione. Nessun numero è una soglia di accuratezza.

Fonti necessarie: documenti con diritti e versioni verificabili, distribuiti fra
famiglie/autori/organizzazioni e sufficienti a costruire esempi naturali delle tre
classi. La distribuzione effettiva per fonte va congelata prima di osservare modelli.

## 6. Indipendenza e contaminazione

1. Il registry registra uso storico della fonte, documento, estratto, claim e caso.
2. Holdout e adversarial escludono source/document cluster usati in sviluppo,
   calibrazione, claim-fidelity, atomic, contrastive, alignment e remediation.
3. `source-disjoint` significa nessun `source_id` o sua versione/quasi-duplicato;
   `document-disjoint` nessun documento o estratto dello stesso documento.
4. `author-disjoint` è obbligatorio come campo e obiettivo di campionamento; se non
   fattibile, la concentrazione va dichiarata e le metriche stratificate. Non va
   affermata senza evidenza.
5. Hash esatti, fingerprint normalizzati e revisione umana identificano quasi
   duplicati, traduzioni, edizioni e estratti sovrapposti.
6. Casi di tuning restano nello split sviluppo/calibrazione e non migrano al holdout.
7. Predizioni Qwen/NLI/reviewer sono nascoste ad A, B e C e non determinano label.
8. Dopo il freeze non si cambiano label guardando risultati: una correzione crea
   nuova versione, parent manifest e changelog; la versione precedente resta.
9. Un caso indipendente usato per remediation viene ritirato dalle future stime
   indipendenti.

## 7. Doppia revisione e adjudication

### 7.1 Review A/B

A e B lavorano separatamente e in cieco. Per ogni caso registrano label, span
probanti o controprobanti, motivazione, attore/fase, condizioni, scope,
quantificatori, ambiguità e confidenza categorica. Non vedono giudizio reciproco,
predizione del modello o split finale sensibile.

Il ledger conserva identità pseudonima, versione del caso, timestamp, conflitti e
digest dell'oggetto annotato. Il disaccordo comprende label diversa, span
incompatibile o motivazione che cambia scope/condizioni, anche se la label coincide.

### 7.2 Adjudication C e controllo D

C esamina caso, A, B e fonti, produce una decisione motivata e non usa maggioranza
automatica. D controlla completezza, indipendenza, riferimenti, digest e assenza di
conflitti; non riscrive il giudizio.

C distingue:

- errore documentato di A o B;
- ambiguità risolvibile con il contesto congelato;
- caso non adjudicabile, da escludere con reason code senza sostituirlo in modo
  opportunistico dopo aver visto il modello.

Le label iniziali restano nel ledger. Ogni modifica produce evento versionato. Il
titolare autorizza il freeze soltanto dopo: A/B complete, disaccordi adjudicati,
esclusioni motivate, controllo D, screening contaminazione, diritti/provenienza
attivi, hash ricalcolati e conteggi/split riconciliati.

## 8. Provenance, integrità e freeze

Sono riusati concettualmente provenance registry v2, ledger A/B/C e manifest v2,
estendendoli con dataset kind S2 senza modificare gli artefatti E/V esistenti.

- `source_sha256`: byte della fonte/versione autorizzata;
- `evidence_sha256`: testo evidenza normalizzato e contesto congelato;
- `claim_sha256`: claim, contesto, condizioni e quantificatori canonici;
- `case_sha256`: intero record normativo esclusi campi derivati del manifest;
- `dataset_sha256`: dataset canonico ordinato per `case_id` e riferito dal manifest.

Il manifest include schema/config fingerprint, case ID/hash, split, dipendenze,
esclusioni, parent/supersedes, stato `draft|frozen`, timestamp UTC e attestazione di
immutabilità. Integrità crittografica dimostra identità dei byte, non correttezza
scientifica, indipendenza o qualità dell'adjudication.

## 9. Compatibilità D3 e S1

Un record autonomo usa claim/evidence direttamente. Un record `d3_specific` aggiunge
un mapping immutabile:

| D3/S1 | Gold S2 |
|---|---|
| `statement` | `claim.text`, con digest verificato |
| `section_span` | localizzazione nella explanation, non nell'evidenza |
| `conditions` | `claim.conditions` |
| `relation_refs` | riferimenti opzionali del claim |
| `requirement_refs` | riferimenti opzionali del claim |
| `evidence_refs` | ID delle unità congelate |
| `evidence_anchors` | span verificabili nell'evidenza |
| `plan_fingerprint` | contesto D3 versionato, non richiesto nei record generali |
| assessment S1 | predizione da valutare, mai label Gold |

Gold autonomo e D3-specifico sono stratificati separatamente. Nessun piano D3 è
richiesto per NLI generale. S1 e il contratto D3 restano invariati.

## 10. Protocollo futuro di valutazione

Per ogni split e complessivo, senza esecuzione in questa attività:

- matrice di confusione 3×3;
- precision, recall e F1 per classe, macro e micro;
- numero e tasso dei falsi `supported`, con intervallo di confidenza;
- separazione `contradicted`↔`insufficient`;
- risultati per categoria primaria, proprietà, fonte/source cluster e split;
- intervalli binomiali dichiarati e bootstrap a cluster per dipendenze documentali;
- accordo A/B pre-adjudication, Cohen kappa quando applicabile, tasso di disaccordo,
  adjudication ed esclusione;
- copertura e tasso `not_evaluable` del sistema, separati dalla label Gold.

Le metriche non definiscono soglie di certificazione. Prima di ogni valutazione il
titolare approva modello/config, split, metriche primarie, metodo degli intervalli e
regola decisionale. I falsi `supported` hanno priorità di rischio, ma il relativo
limite accettabile non è fissato senza decisione esplicita.

## 11. Piano operativo successivo

| Fase | Attività | Dipendenze | Evidenze/cancello | Carico |
|---|---|---|---|---|
| A preparazione | schema S2, inventario fonti, diritti, matrice, screening contaminazione, pilot tempi escluso dal gold | decisioni su volume/fonti/ruoli | registry e manifest draft; zero casi valutati dal modello | tecnico + source curation, da misurare |
| B annotazione | selezione autorizzata e review A/B cieca | G0 schema/diritti/indipendenza PASS | ledger A/B completo, nessuna predizione visibile | 202–303 h raccomandate, esclusi overhead |
| C adjudication | C risolve; D controlla QA | A/B complete | disaccordi/esclusioni motivati e versionati | dipende dal tasso osservato |
| D freeze | canonicalizzazione, hash, riconciliazione split e approvazione titolare | provenance attiva, QA PASS | manifest frozen e dataset immutabile | tecnico/QA, da misurare |
| E S2 shadow | valutazione del candidato congelato, nessuna autorità di gate | nuova autorizzazione, Gold frozen | report content-addressed e metriche predefinite | runtime/costo non stimato qui |

Ogni fase richiede autorizzazione separata. Nessuna fase parte automaticamente dalla
precedente.

## 12. Decisioni richieste al titolare

1. scegliere volume raccomandato 606 o ridotto 390;
2. approvare fonti, diritti, retention e custodia delle evidenze congelate;
3. nominare A, B, C e D, requisiti di competenza e gestione conflitti;
4. decidere se author-disjointness è requisito assoluto o stratificazione obbligata;
5. approvare schema/validator S2 separato e riuso non distruttivo dell'infrastruttura
   Gold v2;
6. approvare matrice di copertura prima della selezione;
7. autorizzare separatamente preparazione, annotazione, adjudication e freeze;
8. solo dopo freeze, autorizzare modello/config e protocollo shadow; soglie e autorità
   di gate restano decisioni ulteriori.

## 13. Stati ufficiali

- Gold S2 design: **VALIDATO**.
- Schema/validator S2: **DA FARE**.
- Inventario fonti e screening: **DA FARE**.
- Raccolta casi, annotazione A/B, adjudication C/D e freeze: **BLOCCATO** fino alle
  decisioni e autorizzazioni del titolare.
- Gold S2 indipendente: **BLOCCATO** fino al freeze.
- NLI diretto V2: candidato shadow, non **VALIDATO** come S2.
- S2 shadow/gate, integrazione e certificazione: **BLOCCATO**.
- S1 deterministico: stato precedente **VALIDATO offline**, invariato.

La progettazione non autorizza raccolta, annotazione, adjudication, modello o
valutazione.
