# TSC V2 dual-output — specifica architetturale

## 1. Identità, baseline e stato

- Attività: `RD-TSC-V2-DUAL-OUTPUT-DESIGN-01`
- HEAD iniziale: `fe9ddca2570d46d5a8a68fdc21d0c49ba41d7106`
- Baseline tecnica osservata: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`
- Dipendenza: `RD-TSC-V2-AUDIT-CONTRACT-COMPATIBILITY-01`
- Perimetro: progettazione statica; nessuna implementazione o verifica eseguita.

TODO, registro, Gate, report forense, revisione contrattuale, handoff e remediation
sono stati riconciliati. Non esisteva una specifica dual-output equivalente.

## 2. Problema contrattuale dimostrato

Il piano `tscv2gate01` fissa un blocco canonico con attore, compito, spazio, trigger,
finalità e fase. L'audit V1 richiede anche densità/prossimità, palla
coperta/scoperta, zona di campo e struttura preventiva. Tali dettagli non sono nei
source term autorizzati; aggiungerli al blocco produce prosa non canonica, mentre
alterare i termini viola il piano. Per questo caso una risposta non può soddisfare
simultaneamente `_canonical_blocks()` e `audit_answer()`.

La soluzione deve conservare il piano normativo e spostare la completezza
documentale in una rappresentazione separata, senza permettere che essa corregga il
piano o diventi una via di promozione autonoma.

## 3. Decisione architetturale proposta: D3

Si propone una soluzione ibrida:

1. il planner materializza `authorized_applied_plan` V2;
2. il sistema ne calcola un fingerprint e rende `canonical_relations` senza Qwen;
3. Qwen riceve piano, fingerprint, requisiti documentali ed evidenze e genera una
   sola `documentary_explanation` strutturata;
4. il sistema assembla il risultato finale, applica controlli separati e conserva
   raw transport, piano, rendering, spiegazione e diagnostica;
5. soltanto l'esito congiunto positivo può promuovere la spiegazione documentale.

Il modello non restituisce né modifica `applied_plan` o `canonical_relations`.
Restituisce il fingerprint ricevuto e riferimenti espliciti: una divergenza blocca,
ma la sua eco non sostituisce il confronto con il piano autorevole.

## 4. Contratti distinti

### 4.1 Envelope di trasporto Qwen

```json
{
  "schema": "tactical_state_documentary_explanation_v1",
  "authorized_plan_fingerprint": "sha256:<64 hex>",
  "documentary_explanation": {
    "sections": [
      {
        "section_id": "section:<stable id>",
        "kind": "relation_explanation",
        "relation_refs": ["relation:<id>"],
        "requirement_refs": ["question_part:..."],
        "text": "...",
        "evidence_refs": ["F1"],
        "claims": [
          {
            "claim_id": "claim:<stable id>",
            "relation_refs": ["relation:<id>"],
            "dimensions": ["actor", "task"],
            "polarity": "affirmed",
            "evidence_refs": ["F1"],
            "support_mode": "direct",
            "evidence_anchors": [
              {"evidence_ref": "F1", "exact_text": "..."}
            ]
          }
        ]
      }
    ]
  }
}
```

Lo schema di trasporto ammette solo i campi sopra, con
`additionalProperties=false` a ogni livello. Limiti proposti: 1–64 sezioni; 1–32
claim per sezione e massimo 256 complessivi; 1–64 relation/requirement ref per
sezione, non oltre il numero di ID autorizzati; 1–8 evidence ref per claim; testo
1–12000 caratteri per sezione e massimo 32000 complessivi. Il superamento è
`blocked`; il troncamento è `not_evaluable`. `kind`, `dimensions`, `polarity` e
`support_mode` sono enum chiuse. `support_mode` ammette `direct`,
`bounded_inference`, `uncertainty`.

### 4.2 Risultato assemblato dal sistema

```json
{
  "schema": "tactical_state_dual_output_diagnostic_v1",
  "applied_plan": {},
  "authorized_plan_fingerprint": "sha256:<64 hex>",
  "canonical_relations": [
    {
      "relation_id": "relation:<id>",
      "rendered_lines": ["[REL ...]", "Attore: ...", "..."]
    }
  ],
  "documentary_explanation": {},
  "promoted_answer": "",
  "controls": {},
  "overall_status": "blocked",
  "reasons": [],
  "raw_model_content": ""
}
```

`applied_plan`, fingerprint, rendering, controlli, stato, reasons e promoted answer
sono prodotti dal sistema. Non devono essere accettati dal payload del modello.

### 4.3 Tabella dei campi

| Campo | Tipo/cardinalità | Obbligo | Origine/autorità | Validazione e failure |
|---|---|---|---|---|
| `applied_plan` | TSC V2, 1 | sì | planner/sistema, normativo | validatori V1+V2; invalido=`blocked` |
| plan fingerprint | SHA-256 canonical JSON, 1 | sì | sistema, normativo | confronto esatto; mismatch=`blocked` |
| `canonical_relations` | array 0..n, una per relazione | sì | renderer deterministico, normativo | corrispondenza biunivoca e ordine; errore=`blocked` |
| explanation sections | array 1..n quando esistono requisiti | sì | Qwen, documentale | schema, unicità, copertura; omissione=`not_evaluable` o `blocked` se dimostrata |
| `section_id` | stringa unica | sì | Qwen | non vuota/unica; invalida=`blocked` |
| `kind` | enum | sì | Qwen | `relation_explanation`, `conditional_detail`, `scenario_detail`, `uncertainty` |
| relation refs | array unico ≥1 salvo uncertainty globale | condizionale | Qwen cita; sistema risolve | sconosciuto/duplicato=`blocked` |
| requirement refs | array unico | sì per section normativa | Qwen cita; sistema risolve | sconosciuto=`blocked` |
| `text` | stringa non vuota | sì | Qwen, documentale | limite dimensionale e audit; mancante=`not_evaluable` |
| evidence refs | array unico ≥1 per claim tattico | sì | Qwen cita | ID inesistente=`blocked`; vuoto=`not_evaluable` |
| claims | array 1..32, totale ≤256 | sì | Qwen, documentale | ID unico, refs e dimensioni risolte; invalido=`blocked` |
| evidence anchors | array 1..8 per supporto direct | condizionale | Qwen cita; sistema verifica | testo esatto nella F indicata; assente/diverso=`blocked` |
| validation metadata | object | sì nel risultato | sistema, diagnostico | mai letto dal payload Qwen |

I campi normativi sono piano, fingerprint e rendering. Testo, sezioni e claim sono
documentali. Diagnostica e promozione sono esclusivamente sistemiche.

## 5. Autorità e responsabilità

### Planner/sistema

- produce e valida il question plan e l'applied plan V2;
- assegna ID, fingerprint, riferimenti, termini canonici e provenienza;
- rende il blocco canonico;
- ricava dal question plan le facet, i dettagli e gli scenari documentali richiesti;
- risolve tutti i riferimenti e applica audit, coerenza e promozione.

### Qwen

- genera una sola spiegazione documentale;
- cita soltanto ID del piano e delle evidenze ricevute;
- sviluppa dettagli condizionati realmente richiesti dal piano audit;
- marca come uncertainty ciò che non può sostenere;
- non crea attori, relazioni, requisiti, evidenze o vincoli normativi.

Informazioni aggiuntive senza relation/requirement/evidence refs sono invalide.
Informazioni referenziate ma semanticamente non verificabili sono `not_evaluable`.
Una sezione di uncertainty conserva il limite ma non soddisfa il requisito mancante.

## 6. Perché rendering deterministico

Far rigenerare a Qwen un piano già determinato non aggiunge autorità: introduce una
seconda rappresentazione mutabile e ha già prodotto divergenze nel Gate. Il rendering
sistemico elimina tale superficie senza nascondere la fedeltà generativa, che viene
misurata sulla capacità del modello di riferire correttamente relazioni, coprire i
requisiti e produrre una spiegazione coerente. Raw output e fingerprint eco restano
conservati.

Il rischio è che il Gate non misuri più la copia testuale del piano. Questo è
intenzionale: la copia non è una proprietà tattica utile. Restano verificati schema
del payload, riferimenti, copertura, coerenza, citazioni e audit.

## 7. Contratto della spiegazione documentale

### Sezioni

- `relation_explanation`: obbligatoria una o più volte fino a coprire ogni relazione
  normativa; deve esporre attore, compito, spazio, trigger, finalità, fase e polarità.
- `conditional_detail`: obbligatoria per ciascun dettaglio `REQUIRED_DETAILS`
  effettivamente attivato; collega almeno una relazione o un requirement.
- `scenario_detail`: obbligatoria per ogni dettaglio dello scenario attivo.
- `uncertainty`: facoltativa; segnala ambiguità e non produce copertura positiva.

Una sezione può coprire più requisiti solo se i riferimenti e i claim sono espliciti.
Duplicazioni incompatibili sono bloccanti; duplicazioni equivalenti sono diagnostiche
ma non aumentano la copertura.

### Dimensioni tattiche

Attore, compito, spazio, trigger, finalità e fase devono riferire le dimensioni della
relazione, non ridefinirle. Densità/prossimità, palla coperta/scoperta, zona di campo,
struttura preventiva e altri dettagli sono richiesti solo quando il question plan
audit li attiva. Non diventano campi universali del dominio V2.

### Evidenze e supporto

Ogni claim tattico richiede almeno un evidence ref esistente. Questo prova la
tracciabilità, non il supporto semantico. Sono distinti:

- `direct`: claim accompagnato da `evidence_anchors`; ogni `exact_text` deve essere
  una sottostringa non vuota dell'evidenza indicata dopo sola normalizzazione NFC e
  newline, senza casefold o similarità. Questo prova l'ancoraggio, non da solo
  l'equivalenza semantica dell'intero claim;
- `bounded_inference`: inferenza tattica esplicitamente qualificata, ammessa solo se
  un verificatore futuro ne dimostra le premesse; altrimenti `not_evaluable`;
- `unsupported` o ref solo formale: `blocked`.

La specifica non dichiara disponibile un verificatore semantico generale. Keyword e
overlap non possono promuovere da soli un claim.

## 8. Matrice di coerenza

| Controllo | Input | Regola | Evidenza necessaria | Violazione |
|---|---|---|---|---|
| fingerprint | echo + piano | uguaglianza byte del digest canonicale | canonical JSON | `blocked` deterministico |
| relation/requirement refs | sezioni + piano | ogni ref esiste e ha tipo corretto | registri ID | `blocked` deterministico |
| copertura relazioni | relazioni + sezioni | ogni relazione normativa ha claim/sezione | mappa ID | omissione dimostrata=`blocked` |
| relazioni extra | refs spiegazione | nessuna relazione sconosciuta | mappa ID | `blocked` |
| attore | claim + actor ref | stesso ID/kind; anchor lessicale controllato | piano + text span | mismatch ID=`blocked`; semantica incerta=`not_evaluable` |
| compito | claim + term ID | term ID/source term autorizzato | piano + span | mismatch=`blocked` |
| spazio | claim + term/position ref | riferimenti esatti | piano + span | mismatch=`blocked` |
| trigger/finalità/fase | claim + relation | ID/term/fase esatti, nessuna inversione nota | piano + span | mismatch=`blocked` |
| polarità | testo + task autorizzato | negazione/ambiguità tramite regole bounded esistenti | clause + relation | negata=`blocked`; ambigua=`not_evaluable` |
| contraddizione interna | sezioni/claim | nessun valore strutturato incompatibile per stesso ref | claim records | dimostrata=`blocked`; semantica incerta=`not_evaluable` |
| citazioni | evidence refs | ID esistenti e nel tentativo | evidence registry | inesistente=`blocked` |
| supporto diretto | claim + anchor | anchor esatto nell'evidenza e attribuibile | testo evidenza conservato | assente=`blocked` |
| inferenza | claim + evidenze | nessuna equivalenza per semplice similarità | controllo limitato/human evidence | non dimostrabile=`not_evaluable` |
| dettagli audit | question plan + sections | copertura di soli dettagli attivati | checklist audit | mancante=`blocked` se esito audit negativo |
| prosa/piano | testo completo + piano | audit e regole note, senza nuovi fatti strutturati | output controlli | negativo=`blocked`; incerto=`not_evaluable` |

I confronti di ID, tipo, cardinalità, fingerprint, exact anchor, enumerazioni e
polarità bounded sono deterministici. Verità generale, equivalenza parafrastica,
causalità tattica e supporto di inferenze non lo sono.

## 9. Adattatore audit V1

`audit_answer()` resta invariato. Un adattatore sistemico:

1. verifica lo schema documentale;
2. concatena in ordine solo `section.text`, escludendo rendering canonico, ID e label;
3. passa il testo e il question plan originale a `audit_answer()`;
4. conserva integralmente output V1 e `relational_audit`;
5. applica separatamente ref/citation/support/coherence controls.

Sono riusabili senza modifica facet, operational cues, required/scenario details e
semantic issues. Serve l'adattatore per evitare falsi positivi generati da label,
ID e termini tecnici del blocco canonico. `audit_relations()` resta diagnostico nella
baseline; non può essere promosso implicitamente a gate. L'audit V1 positivo è
necessario ma non sufficiente, perché la presenza di keyword non dimostra supporto.

## 10. Promozione e fail-closed

| Piano | Spiegazione | Audit | Coerenza | Decisione |
|---|---|---|---|---|
| valido | valida/completa | positivo | positiva e supporto valutato | `validated`, promozione possibile |
| invalido | valida | positivo | positiva | `blocked` |
| valido | invalida | positivo | positiva | `blocked` |
| valido | valida | negativo | positiva | `blocked` |
| valido | valida | positivo | negativa | `blocked` |
| valido | mancante/parziale | non valutabile | non valutabile | `not_evaluable`, nessuna promozione |
| valido | valida | positivo | supporto semantico non valutabile | `not_evaluable` |

`blocked` richiede una violazione dimostrata. `not_evaluable` indica assenza,
troncamento, ambiguità o controllo obbligatorio non conclusivo senza una violazione
positiva. `validated` richiede tutti i controlli obbligatori positivi e nessun scope
non valutato. Stati interni, PASS tecnico e fail-closed non sono stati ufficiali del
progetto e non implicano integrazione.

Nessuna partial answer è promossa. Raw, parsed transport, piano, rendering,
spiegazione e controlli sono conservati separatamente.

## 11. Impatto sui componenti

| Componente | Modifica progettata | Necessità/compatibilità | Rischio | Criterio futuro |
|---|---|---|---|---|
| planner V1 | nessuna | fonte invariata | nessuno | regressione byte/comportamento |
| TSC V1 | nessuna | invariato | nessuno | suite V1 invariata |
| dominio TSC V2 | nessuna semantica | piano invariato | nessuno | validatori esistenti passano |
| generazione V2 | nuovo transport documentale opt-in | necessaria | schema/prompt | una call, no repair |
| parser | parser envelope dual-output separato | necessaria | tipi/troncamento | malformed fail-closed |
| renderer | nuova funzione pura piano→blocchi | necessaria | drift formato | golden deterministici |
| coherence validator | nuovo controllo refs/claims | necessaria | falsa semantica | tre stati e scope esplicito |
| audit V1 | nessuna modifica | riuso via adapter | keyword false positive | output conservato, non sufficiente |
| diagnostica | nuovi controlli separati | necessaria | conflazione cause | passed/failed/unassessed distinti |
| runner | nuovo flag opt-in o versione esplicita | necessaria | regressione legacy | default invariato |
| API/pannello | nessuna prima fase | fuori perimetro | esposizione prematura | nessuna attivazione |
| report | nuovi campi separati | necessaria | segreti/dimensione | raw e diagnostica distinti |

## 12. D1/D2/D3

| Alternativa | Vantaggi | Limiti e rischi | Costo/verificabilità | Decisione |
|---|---|---|---|---|
| D1 Qwen genera piano e spiegazione | misura copia del piano in un solo output | duplica autorità, drift già osservato, più failure non tattiche | alto; più controlli | respinta |
| D2 sistema rende piano, Qwen solo prosa | minima superficie mutabile | può perdere linkage esplicito e misura di aderenza | medio; buona | ammissibile ma incompleta |
| D3 sistema rende piano, Qwen genera documento strutturato con digest/ref/claim | autorità unica, linkage verificabile, audit separato | nuovo schema e support checker; semantica generale resta limitata | medio-alto; migliore tracciabilità | raccomandata |

D3 non autorizza il modello a modificare il piano e conserva una misura utile della
fedeltà: riferimenti, copertura, polarità, citazioni e coerenza della spiegazione.

## 13. Strategia futura di verifica (non eseguita)

Solo casi differenziali nuovi:

1. assemblaggio deterministico piano/rendering con explanation valida;
2. digest errato;
3. relation/requirement/evidence ref inesistente o duplicato;
4. omissione di una relazione e aggiunta non autorizzata;
5. mismatch separati per attore, compito, spazio, trigger, finalità e fase;
6. polarità negata e ambigua;
7. dettaglio condizionale richiesto presente/assente;
8. audit V1 negativo su sola prosa documentale;
9. claim diretto con anchor valido/invalido e inferenza non valutabile;
10. envelope troncato/malformato, explanation mancante e output parziale;
11. matrice `blocked`/`not_evaluable`/`validated` e nessuna partial promotion;
12. una sola chiamata mock, zero repair;
13. regressione opt-in: V1, V2 corrente e profilo legacy invariati.

Non vanno ripetute campagne V1/V2 già concluse salvo regressioni direttamente
interessate e motivate dal delta.

## 14. Dipendenza diagnostica `omitted`

La distinzione `omitted` / `present_but_invalid` deve essere corretta separatamente
prima di usare i reasons come diagnosi dell'handoff. Non allenta la copertura: entrambe
le condizioni restano non promuovibili. Il dual-output usa una propria mappa di
copertura delle sezioni e non deve dedurre assenza dalla sola esclusione di record
invalidi.

## 15. Rischi residui e decisioni da approvare

Rischi:

- l'audit V1 resta lessicale e può accettare keyword senza verità documentale;
- un verificatore semantico generale non esiste; inferenze non dimostrate restano
  `not_evaluable`;
- granularità claim troppo fine può ridurre leggibilità, troppo ampia riduce
  attribuibilità;
- rendering e piano possono divergere per bug sistemico, da coprire offline;
- maggiore output può aumentare rischio di troncamento, sempre fail-closed.

Decisioni richieste al titolare prima dell'implementazione:

1. approvare D3 e il nuovo envelope documentale opt-in;
2. approvare che il piano non sia più rigenerato da Qwen;
3. approvare claim-level refs e policy `not_evaluable` per supporto semantico incerto;
4. approvare o rettificare i limiti proposti di cardinalità e dimensione del payload;
5. decidere se il supporto `bounded_inference` richieda revisione umana o un futuro
   verificatore esplicitamente autorizzato;
6. mantenere API/pannello fuori dalla prima implementazione.

## 16. Stati ufficiali

- specifica dual-output: **VALIDATO**;
- implementazione dual-output: **DA FARE** previa decisione;
- Gate runtime TSC V2: **BLOCCATO**;
- integrazione runtime: **BLOCCATO**;
- certificazione runtime: **BLOCCATO**.

Questa specifica non autorizza codice, test, inferenze o un nuovo Gate.
