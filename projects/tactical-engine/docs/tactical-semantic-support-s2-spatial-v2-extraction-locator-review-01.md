# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-REVIEW-01

## Baseline e perimetro

Revisione statica indipendente dell'implementazione extraction/locator Spatial
V2.

- baseline: `9bd8ee4e2c80739430e8f7c795386ebaec92f34c`;
- branch: `codex/tactical-state-contract-v1`;
- working tree iniziale: pulito;
- validatore Spatial V2: blob Git identico alla baseline precedente
  `0a8b92acbda67afeaee4bc057f89729e11e20ab5`;
- test già registrati, non rieseguiti: 12/12 extraction + 21/21 regressioni;
- nessuna inferenza, rete, VPS, benchmark, Gate o modifica applicativa.

Esaminati: commit implementativo, report, TODO, experiment register, modulo
extraction/locator, judge, validatore finale e le due suite interessate.

## Schema e conservazione delle informazioni

`EXTRACTION_SCHEMA` mantiene label, comparison e tutti gli slot semantici del
witness V2: subject, semantic_axis, reference, value, conditions, phase,
quantifier e polarity. Mantiene inoltre entity/condition ID e literal del
quantificatore. La sola sostituzione è `anchors` → `selected_fragments`.

La materializzazione copia senza conversioni:

- `status`, `entity_id` e `value` di ogni slot;
- `literal` del quantificatore;
- `condition_id` e status degli item;
- comparison e label.

Per ogni frammento produce esclusivamente l'anchor derivato. Non emerge perdita
di informazione semantica necessaria al validatore finale. Vincoli più forti
non duplicati nello schema extraction — pattern degli ID, combinazioni
status/value, axis/value e coerenza label/comparison — restano applicati da
`validate_spatial_v2()` dopo la materializzazione.

## Locator

`_occurrences()` usa `str.find(fragment, offset)` e incrementa l'offset di un
solo code point. Conta quindi anche match sovrapposti; non salta alla fine del
match e non seleziona la prima occorrenza. `_localize_fragments()` accetta solo
un conteggio uguale a uno, calcola `end=start+len(fragment)` e ricontrolla la
slice letterale.

Gli indici Python sono code point Unicode e l'intervallo è semiaperto. Non sono
presenti encode, casefold, normalizzazioni, regex, fuzzy matching o ricerca
alternativa. Il testo è scelto esclusivamente dal contenitore: claim ed
evidence sono passati separatamente a `_materialize_relation()`, che imposta
anche il `source` dell'anchor. Un frammento presente soltanto nel lato opposto
ha conteggio zero e resta `not_evaluable`.

## Semantica e fail-closed

Il locator non modifica status, value, quantifier, polarity, comparison o
label. `explicit/affirmed`, axis/value incompatibili e label incoerenti possono
essere materializzati, ma vengono respinti dal validatore invariato.

Percorsi di errore:

| Frontiera | Esito |
|---|---|
| trasporto, timeout, risposta incompleta/mancante | `not_evaluable`, nessuna promozione |
| JSON non valido | `not_evaluable`, witness nullo |
| shape/identità/tipi/frammenti invalidi | `not_evaluable`, witness nullo |
| zero o più match | `not_evaluable`, witness nullo |
| witness materializzato ma invalido | errori originali del validatore, `not_evaluable` |
| witness valido | `evaluated`, ma `promotion_authorized=false` |

Eccezioni di programmazione non intercettate non possono produrre un record
promosso: interrompono il chiamante. Non esiste fallback, retry o repair.

## Provenienza e limite crittografico

La provenienza contiene identità/versione, digest dell'estrazione, digest dei
due testi e, per ogni frammento, field ID, lato, digest sorgente, conteggio,
offset e risultato. `record_sha256` è calcolato sul record canonico con il
campo hash nullo. `verify_materialization()` ricalcola deterministicamente
l'intero risultato da extraction, claim ed evidence e confronta la
rappresentazione canonica: alterazioni di witness, diagnostica, record o digest
sono individuate rispetto agli input forniti.

Questa è **integrità riproducibile**, non autenticità crittografica. Non esiste
firma, MAC o identità fiduciaria: un soggetto capace di sostituire insieme
risultato e input può produrre un nuovo insieme internamente coerente. Il limite
è appropriato al prototipo shadow offline, ma impedisce qualificazioni di
provenienza autenticata o certificata.

## Compatibilità legacy

Con `extraction_locator=False`:

- `INSTRUCTION`, `SPATIAL_V2_SCHEMA`, modello, opzioni, timeout 180/360 e
  messaggi del payload restano sul ramo storico;
- parsing, `validate_spatial_v2()` e forma del risultato restano quelli
  preesistenti;
- il nuovo modulo importato è puro e inerte;
- nessun call site pubblico è stato modificato.

Il solo nuovo controllo è il tipo del keyword aggiunto, il cui default booleano
è valido. Non emerge una variazione del comportamento per i chiamanti legacy.

## Copertura dichiarata e lacune nuove

Le 12 verifiche coprono tutti i criteri di accettazione principali: match
unico/assente/ripetuto/lato opposto, Unicode, semantica non riparata,
provenienza alterata, schema privo di location, opt-in single-call, legacy e
errori di boundary. Le 21 regressioni coprono il validatore e il judge storico.

Due limiti di copertura concreti ma non bloccanti:

1. il caso ripetuto usa occorrenze separate (`spazio spazio`), non un match
   sovrapposto come `aa` in `aaa`; il ciclo `offset=position+1` dimostra
   staticamente che entrambe le occorrenze sarebbero contate;
2. la fixture positiva localizza subject/axis/reference/value, mentre conditions
   esplicite, phase/quantifier con frammenti e liste multi-frammento non hanno
   ciascuno un test positivo dedicato. `_materialize_relation()` usa lo stesso
   helper per tutti gli slot e il validatore finale copre le relative regole.

Non emerge una differenza tecnica che giustifichi nuovi test in questa
revisione. I limiti vanno conservati come perimetro probatorio, non trasformati
in difetti o in certificazione generale.

## Difetti e rischi residui

**Difetti concreti rilevati: nessuno.**

Rischi residui:

- **medio, semantico:** uno span univoco può essere troppo ampio o irrilevante;
  il locator non prova supporto o verità;
- **basso, copertura:** branch espliciti/multi-frammento non tutti esercitati da
  fixture positive dedicate;
- **basso, probatorio:** overlap verificato staticamente ma non da test
  differenziale dedicato;
- **medio, autenticità:** SHA-256 rileva alterazioni rispetto agli input, ma non
  autentica autore o origine;
- **non determinato, runtime:** conformità e qualità di un output Qwen reale non
  sono ancora osservate nel nuovo percorso.

## Decisione

L'implementazione è idonea, sul piano statico e offline, a essere sottoposta a
**un singolo runtime diagnostico opt-in** con autorizzazione separata, artefatti
completi, una sola generazione e nessuna promozione. Tale runtime dovrà valutare
il comportamento reale di Qwen; non è un Gate di integrazione e non autorizza
panel o produzione.

Flusso: Attività = revisione statica; Script = nessuno eseguito; Commit =
documentale; Report = questo documento; Risultato = nessun difetto concreto,
due limiti di copertura minori; Decisione = implementazione offline confermata e
futuro singolo runtime proponibile, non autorizzato.

| Componente | Stato |
|---|---|
| Implementazione extraction/locator | **IMPLEMENTATO** |
| Test già registrati | **ESEGUITO** |
| Proprietà statiche/offline esaminate | **VALIDATO** |
| Singolo runtime diagnostico opt-in | **DA FARE**, non autorizzato |
| Gate | **BLOCCATO** |
| Integrazione pubblica | **BLOCCATO** |
| Certificazione | **BLOCCATO** |
