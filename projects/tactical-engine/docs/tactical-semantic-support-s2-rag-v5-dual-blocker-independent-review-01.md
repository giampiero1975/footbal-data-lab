# RAG V5 dual blocker — revisione indipendente della patch offline

Attività: `RD-TSC-V2-D3-S2-RAG-V5-DUAL-BLOCKER-INDEPENDENT-REVIEW-01`
Baseline revisionata: `99fb33724dc85edcb263742fa14116fbe88584cd`
Commit tecnico: `56a7b72135595e99a98ff2fb5b1bcc3d6a0c9ebf`

## Evidenze esaminate

- TODO ed Experiment Register allo HEAD di riferimento;
- report causale e report della remediation offline;
- delta del commit tecnico rispetto a
  `4a5ff711620970e02abbaf26c479d05cfd69260d`;
- contratto e validatore Spatial V2;
- 16 test extraction/locator e 21 regressioni Spatial V2 già registrati.

Le suite non sono state rieseguite. HEAD locale e remoto coincidevano con la
baseline e il working tree era pulito all'avvio.

## Revisione side-bound

Esito: **PASS statico**.

- `EXTRACTION_INSTRUCTION` definisce esplicitamente `claim_relation` come lato
  AFFERMAZIONE ed `evidence_relation` come lato FONTE; definisce inoltre
  `subject` e `reference` e vieta l'uso del lato opposto
  (`shadow_nli_spatial_relations_v2_inference.py:21`).
- Il prompt effettivo concatena tale istruzione a FONTE e AFFERMAZIONE
  (`build_extraction_prompt()`, righe 57–64).
- Lo schema trasmesso nel payload contiene descrizioni distinte dei due lati e
  del referente. Il test mock ne verifica la presenza nel payload.
- Il locator continua a cercare ogni frammento soltanto nel testo assegnato da
  `side` (`_localize_fragments()`, riga 322); non contiene spostamenti,
  normalizzazioni o repair. Il commit tecnico non lo modifica.
- Il test esistente per frammento sul lato opposto resta specifico e separato
  (`test_04_opposite_side_fragment_is_not_evaluable`, riga 107).

Queste evidenze dimostrano correttezza del contratto e comportamento
fail-closed, non la capacità di Qwen di rispettare l'handoff.

## Revisione semantica

Esito: **PASS statico con limiti diagnostici non bloccanti**.

- La matrice nel prompt coincide con `AXIS_VALUES` del contratto versionato
  (`v5_tactical_semantic_support_s2_spatial_v2.py:25`).
- `extraction_semantic_errors()` usa direttamente tale matrice e viene chiamata
  dopo lo shape check e prima del locator (righe 286 e 436).
- La coerenza di subject, reference, conditions, phase, quantifier, polarity e
  value viene verificata riusando `_comparison_errors()` del validatore
  versionato (riga 388), senza una seconda tabella comparison.
- Il controllo asse/valore replica soltanto il confine anticipato necessario,
  ma legge la stessa `AXIS_VALUES`; il validatore finale ripete il controllo sul
  witness materializzato e resta autorità (`validate_spatial_v2()`, riga 465).
- Nessuna label viene derivata, sostituita o corretta dal precontrollo.
  Un'incoerenza produce `E_EXTRACTION_SEMANTIC_INCONSISTENT`, witness nullo e
  `promotion_authorized=false`.

Per `q3_04`, la combinazione documentata `space_availability/between` e i
comparison `same` incompatibili con ID, condizioni e quantificatori sono ora
respinti prima della localizzazione. La regola è generale e usa vocabolari e
relazioni del contratto, non parole specifiche del caso.

## Copertura e lacune residue

I risultati registrati 16/16 e 21/21 coprono le proprietà dichiarate:
side-bound, asse/valore, comparison quantifier, percorso legacy, singola
chiamata, assenza di repair, referenti differenti e valori incompatibili sullo
stesso referente.

Non emergono difetti che consentano una promozione indebita. Restano due limiti
non bloccanti:

1. `_comparison_errors()` restituisce un codice aggregato; il precontrollo
   conserva quindi `path=comparison` ma non elenca le singole dimensioni
   incoerenti. Il raw extraction resta disponibile e il comportamento è
   fail-closed; l'impatto è diagnostico, non autorizzativo.
2. `test_15` ricostruisce la configurazione semantica documentata di runtime-03
   dentro la fixture, ma il raw artifact originale non è una fixture immutabile
   versionata nel repository. Il test prova le proprietà deterministiche, non
   l'identità byte-per-byte dell'artefatto storico.

Nessuno dei due limiti giustifica nuovi test equivalenti in questo closeout.

## Correttezza deterministica e accuratezza generativa

### Correttezza deterministica

**VALIDATO offline** nel perimetro osservato: extraction con coppie asse/valore
o comparison incoerenti non raggiungono il locator e non producono witness o
promozione; extraction localizzabili raggiungono ancora il validatore finale.

### Accuratezza generativa

**BLOCCATO**. Non esiste ancora evidenza runtime successiva alla patch che Qwen:

- scelga sempre frammenti dal lato corretto;
- distingua spazio davanti e dietro la linea;
- produca valori versionati incompatibili sullo stesso referente;
- assegni `contradicted` a `q3_04`;
- eviti false contraddizioni con referenti differenti.

Il fail-closed non equivale a risoluzione semantica.

## Piano della futura prova generativa

La prova è ammissibile soltanto dopo autorizzazione separata e predisposizione
di uno staging isolato allo HEAD applicativo che includa il commit tecnico
`56a7b72135595e99a98ff2fb5b1bcc3d6a0c9ebf`.

### Differenza tecnica rispetto a runtime-03

Runtime-03 usava il vecchio handoff e raggiungeva il locator con
`space_availability/between`. La nuova prova deve usare il prompt side-specific,
le descrizioni di schema e il precontrollo semantico introdotti dal commit
tecnico. Non è una ripetizione equivalente.

### Sequenza minima proposta

1. Tentativo primario `q3_04`, Gold `contradicted`.
2. Solo con autorizzazioni successive e identificativi distinti: un controllo
   guardia con referente differente, atteso `insufficient`, e un controllo con
   stesso referente e valori incompatibili, atteso `contradicted`.

Ogni invocazione deve consentire esattamente una generazione Qwen, senza retry,
repair o fallback. Nessun risultato di un tentativo autorizza automaticamente
il successivo.

### Artefatti obbligatori

- baseline, prompt e schema effettivamente inviati;
- request, raw response e extraction non modificata;
- esito del precontrollo e reason code;
- record di localizzazione, witness e validazione, quando prodotti;
- label modello, label derivata e Gold mantenuti distinti;
- conteggio trasporto/generazione, tempi, exit code e inventario SHA-256;
- `promotion_authorized=false` in ogni percorso.

### Criteri definiti prima dell'esecuzione

| Classe | Criterio |
|---|---|
| PASS tecnico | una risposta completa, una generazione, zero retry/repair/fallback, artefatti integri |
| PASS localizzazione | tutti i frammenti unici e presenti esclusivamente sul lato assegnato |
| PASS strutturale | extraction e witness superano i rispettivi controlli deterministici |
| PASS semantico `q3_04` | stesso referente rappresentato con valori versionati incompatibili e label derivata `contradicted`, concordante col Gold |
| Guardia referente differente | non viene derivato `contradicted`; esito atteso `insufficient` |
| Fail-closed corretto | input incoerente produce `not_evaluable`, nessun witness promosso e reason code conservato |
| FAIL generativo | label errata, lato errato, referente/asse/valore errato o esito non valutabile; anche se il fail-closed tecnico funziona |
| FAIL operativo | timeout, trasporto, finalizzazione o artefatti incompleti; non interpretabile come prova semantica |

## Decisione e stato

La patch offline è **VALIDATO** nel perimetro deterministico ed è ammissibile a
una futura prova generativa controllata. La prova resta **DA FARE** e
**BLOCCATO** fino ad autorizzazione esplicita, preflight e wrapper revisionato.
Gate, integrazione e certificazione restano **BLOCCATO**.

