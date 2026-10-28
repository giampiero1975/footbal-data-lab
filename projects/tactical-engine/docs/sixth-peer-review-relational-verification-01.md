# Sesta verifica differenziale — audit tattico relazionale

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Commit iniziale: `952da4c8767157bd57f864feecc7b01ab41692f2`  
Commit codice/test: `9e63efc`

## Matrice diagnostica sulla baseline

| Verifica | Comportamento prima | Classificazione |
|---|---|---|
| A, risposta con `mentre` | requisito aperto soddisfatto | difetto riprodotto |
| A, azioni nella stessa clausola | requisito aperto soddisfatto | difetto riprodotto |
| B1, perdita/riconquista locali | entrambi i trigger su entrambi gli atomi | difetto riprodotto |
| B2, trigger iniziale comune | perdita condivisa | comportamento corretto |
| C, proposizione intermedia | relazione non soddisfatta | rischio non riprodotto |

I comportamenti sono stati acquisiti prima della modifica. I test aggiunti dopo
la patch non sono l'unica evidenza della diagnosi.

## Correzioni effettive

### Pertinenza e ambito dell'attore

Gli obiettivi ricavati dalla domanda sono conservati come gruppi distinti. Una
relazione candidata deve dimostrare almeno un'alternativa per ogni gruppo,
anziché prendere un termine qualsiasi dall'unione complessiva.

I requisiti aperti registrano inoltre l'ambito atteso:

- `own_or_unspecified` per una soluzione della propria organizzazione;
- `opponent` quando la domanda nomina esplicitamente l'avversario.

Le clausole diagnosticano `opponent` soltanto quando attore e qualificatore
avversario sono esplicitamente vicini. Una relazione avversaria non soddisfa
quindi una richiesta aperta sulla propria organizzazione. L'esito è osservabile
con `actor_scope_status`; non viene inventata un'identità obbligatoria.

Non è stata mantenuta una segmentazione aggiuntiva delle risposte su `mentre`:
la prima implementazione causava regressioni nelle finalità distribuite e nei
casi B1/B4 già validati. Il controllo conservativo dell'ambito è sufficiente
per i due controesempi A e non spezza relazioni corrette.

### Trigger e fasi locali

Per ogni segmento della domanda vengono prima ricercati trigger e fasi locali.
La cornice del primo segmento è ereditata dai successivi soltanto quando questi
non dichiarano un valore proprio. Ne consegue:

- perdita per il centrale e riconquista per l'ala nel caso B1;
- perdita condivisa da centrale e ala nel caso B2.

Gli identificativi di sottodomanda e relazione restano stabili nel formato
introdotto dalla quinta fase.

### Costrutto postverbale

Il nuovo caso C non produceva il falso collegamento già sulla baseline. Non è
stata applicata alcuna modifica a `_actor_task_link_status()`. È stato aggiunto
soltanto un test di non regressione che preserva il B3 positivo esistente.

## Test e regressione

Quattro controlli nuovi:

1. obiettivo non preso in prestito dall'azione dell'avversario, in due varianti;
2. trigger/fasi locali differenti sui due segmenti;
3. cornice iniziale condivisa soltanto in assenza di trigger locale;
4. proposizione intermedia B3 non collegata al centrale.

Planner/audit: **46/46 PASS** (42 baseline + 4 nuovi). Compilazione di script e
test: **PASS**. `git diff --check`: **PASS**.

Tactical State Contract e API non sono stati rieseguiti perché non condividono
file modificati. `audit_answer()["complete"]`, quality gate legacy, runner,
API, pannello, `DEFAULT_PROFILE_FLAGS`, corpus, indici e Qwen/Ollama sono
invariati. Nessuna VPS, inferenza, chiamata esterna, benchmark, merge o deploy.

## Limiti e decisione

- L'ambito dell'attore è una diagnosi esplicita e circoscritta, non risolve
  pronomi o appartenenza implicita.
- La pertinenza per gruppi resta limitata alla piccola mappa positiva già
  documentata; non dimostra correttezza tattica o supporto delle fonti.
- L'eredità della cornice copre `mentre` e valori locali espliciti, non una
  temporalità linguistica generale.
- La polarità multipla resta `AMBIGUOUS`, come deciso nella quinta fase.

Gold E e Gold V restano soltanto schemi. Drive11 non è rappresentativo e V10
non è indipendente dalla remediation: validazione indipendente **BLOCCATO**.

Decisione: correzioni A/B **IMPLEMENTATO**, test **ESEGUITO**, delta
**VALIDATO offline**. C è documentato come non riprodotto e non ha generato
patch. Audit ancora offline e non bloccante; non **INTEGRATO** o
**CERTIFICATO**.
