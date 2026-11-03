# TSC V2 ↔ audit documentale V1 — revisione contrattuale

## Identità e metodo

- Attività: `RD-TSC-V2-AUDIT-CONTRACT-COMPATIBILITY-01`
- HEAD iniziale: `e6c7a2e5100a63a29cba4a46a640c0a8fee35594`
- Baseline tecnica analizzata: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`
- Gate di riferimento: `RD-TSC-V2-RUNTIME-GATE-01`
- Metodo: ispezione degli oggetti Git alla baseline e delle evidenze già conservate;
  nessun test, runtime, inferenza, retrieval o accesso Chroma/API.

Non esisteva nel TODO, nel registro o nei report una revisione equivalente già
conclusa. Il closeout forense precedente resta acquisito e non è stato ripetuto.

## Catena di chiamate effettiva

1. `run_rag_v5_query.py:93–98` inoltra il flag opt-in
   `--tactical-state-contract-v2`; `validate_report()` alle righe 37–56 accetta
   soltanto `overall_status=validated`, citazioni presenti e nessun ID invalido.
2. `smoke_test_rag_v5_e2e.py:496` costruisce il question plan mediante
   `tactical_analyse()`. Il ramo esclusivo V2 è selezionato alle righe 680–683.
3. `chat_tactical_state_v2_once()` (`smoke_test...:266–309`) chiama
   `prepare_generation_request()`, crea il prompt col piano autorizzato, effettua al
   massimo una chiamata `_ollama_chat_once()`, estrae l'explanation e invoca
   `audit_answer(explanation, question_plan)` prima di `generation_diagnostic()`.
4. `prepare_generation_request()` (`v5_tactical_state_generation_v2.py:33–113`)
   proietta i requisiti, materializza stati di fase e relazioni, quindi richiede
   validità V1 e copertura operativa V2.
5. `generation_diagnostic()` (`v5_tactical_state_generation_v2.py:211–272`)
   analizza envelope, dominio V1/V2, compatibilità domanda-piano, copertura,
   blocchi canonici e audit. Promuove l'explanation solo se tutti consentono
   `overall_status=validated`.

`audit_relations()` viene chiamato internamente da `audit_answer()`
(`v5_tactical_query_plan_v1.py:963–964`), ma il suo risultato è diagnostico:
`audit_relations()` dichiara `affects_legacy_gate=false` e non entra nella formula
`complete`. Il secondo audit a `smoke_test...:689` non si applica al ramo V2 perché
`tactical_plan` non è attivato dal flag V2.

## Contratto formale TSC V2

### Envelope e piano

`generation_transport_schema()` (`v5_tactical_state_generation_v2.py:116–123`)
riusa l'envelope V1 `{applied_plan, explanation}`, impone schema/versione V2 e rende
obbligatorio `operational_relations`. Il piano V2 conserva integralmente il dominio
V1 e aggiunge soltanto tale array (`v5_tactical_state_contract_v2.py:247–252`).

Ogni relazione richiede ID univoco, `requirement_ref`, fingerprint, `actor_ref`,
task, space, trigger, purpose, `phase_state_ref`, assertion mode, provenance e rule
ID (`v5_tactical_state_contract_v2.py:209–244`). I riferimenti sono tipizzati; i
termini contengono source term, normalizzazione, term ID e provenienza. Term ID e
normalizzazione sono ricalcolati; provenienza `derived` richiede una rule consentita
(`:255–340`).

`validate_operational_relations()` (`:343–450`) applica struttura, unicità,
risoluzione dei riferimenti, fingerprint e confronto esatto delle dimensioni
obbligatorie. Solo requisiti `explicit_representable` sono normativi; requisiti
ambigui, inferiti o non rappresentabili restano non valutabili. La validità V2
richiede insieme validità strutturale V1 e copertura operativa `passed` (`:453–466`).

### Presentazione canonica

Per ogni relazione `_canonical_blocks()`
(`v5_tactical_state_generation_v2.py:130–199`) ammette esclusivamente, nello stesso
ordine, otto righe:

```text
[REL <relation_id>]
Attore: <actor_ref.id>
Compito: <task.source_term>
Spazio: <space.term.source_term>
Trigger: <trigger.source_term>
Finalità: <purpose.source_term>
Fase: <phase canonica>
Evidenze: [F<n>] ...
```

Le prime sette righe sono confrontate esattamente. La riga evidenze deve contenere
almeno un ID compreso nell'insieme fornito. Qualunque testo residuo genera
`noncanonical_free_prose`. Questi sono vincoli di presentazione, non un audit della
verità documentale delle citazioni.

### Promozione

`generation_diagnostic()` distingue:

- strutturale: validità V1/V2 e riferimenti;
- semantico deterministico: copertura del requisito e confronto domanda-piano;
- presentazione/coerenza: blocchi canonici;
- documentale: risultato di `audit_answer()`.

Una failure dimostrata produce `blocked`; una verifica obbligatoria non valutabile
produce `not_evaluable`; soltanto `validated` copia l'explanation in
`promoted_answer` (`v5_tactical_state_generation_v2.py:239–269`).

## Contratto effettivo dell'audit V1

`audit_answer()` (`v5_tactical_query_plan_v1.py:868–966`) normalizza l'intera
explanation e applica controlli lessicali deterministici:

1. tutte le facet del question plan devono avere almeno un cue di `FACETS`
   (`:24–41`, `:871–874`);
2. rileva cinque dimensioni operative: `who`, `where`, `trigger`, `reason` e
   `coverage_or_risk` (`:875–884`);
3. per ogni facet richiede tutti i dettagli in `REQUIRED_DETAILS`, salvo tre
   eccezioni condizionate dal testo della domanda (`:68–111`, `:885–901`);
4. richiede tutti i dettagli degli scenari in `SCENARIO_DETAILS` (`:902–908`);
5. respinge pattern semantici noti, label interne, numeri rigidi non richiesti e,
   se esistono scenari, risposte sotto 150 parole (`:909–953`).

La condizione `complete` è:

- nessuna facet mancante;
- al massimo una delle cinque dimensioni operative mancante;
- nessun dettaglio obbligatorio mancante;
- nessuna semantic issue (`:954–965`).

Quindi non sono obbligatorie simultaneamente tutte le cinque dimensioni operative;
quattro bastano. I dettagli di facet/scenario sono invece tutti bloccanti quando
attivati. `where`, `trigger` e `reason` sono semplici cue lessicali, non una verifica
semantica generale. `audit_relations()` diagnostica co-occorrenza, polarità,
attore-compito e citazioni, ma non determina `complete` in questa baseline.

## Matrice di compatibilità

| Requisito audit V1 | Rappresentabile nel blocco V2 | Ammesso da V2 | Evidenza nel codice | Esito |
|---|---|---|---|---|
| Facet richieste | Solo se un source term/ID/fase contiene un cue | sì, incidentalmente | `FACETS`; righe canoniche 170–175 | compatibile ma non garantito |
| `who` | `actor_ref.id` può contenere un ruolo riconosciuto | sì | audit `:876`; blocco Attore | compatibile per vocabolari coincidenti |
| `where` | source term dello spazio può contenere zona/fascia/etc. | sì | audit `:877`; blocco Spazio | compatibile ma `lato debole` da solo non vale |
| `trigger` | source term del trigger | sì | audit `:878`; blocco Trigger | compatibile |
| `reason` | source term della finalità | sì | audit `:879–880`; blocco Finalità | compatibile se il cue coincide |
| `coverage_or_risk` | task/finalità possono contenere un cue | sì | audit `:881`; blocchi Compito/Finalità | compatibile se il cue coincide |
| Densità/prossimità | non ha un campo dedicato; solo dentro un source term | sì, ma solo se già parte del requisito | `REQUIRED_DETAILS:68–74` | non garantito |
| Palla coperta/scoperta | idem; regex richiede frase specifica | sì, ma solo se già nel requisito | audit `:898–901` | non garantito |
| Zona di campo | idem | sì, se compare in un source term | `REQUIRED_DETAILS` | non garantito |
| Struttura preventiva | idem | sì, se compare in un source term | `REQUIRED_DETAILS` | non garantito |
| Dettagli scenario | nessun campo generale; possono comparire accidentalmente nei termini | formalmente sì | `SCENARIO_DETAILS`, audit `:902–908` | spesso non rappresentati |
| Assenza di issue semantiche | il formato non forza pattern vietati | sì | audit `:909–953` | compatibile |
| Citazione valida | riga Evidenze con ID esistente | sì | canonical `:181–190` | compatibile formalmente |
| Supporto semantico della citazione | non verificato dal blocco canonico | non imposto | `audit_relations():819–857` | controllo incompleto/non bloccante |

Il contratto V2 non vieta source term lunghi che contengano i cue dell'audit; vieta
però di aggiungere una spiegazione separata per colmare ciò che il piano non contiene.

## Soddisfacibilità congiunta A ∩ B

### Dominio generale

L'intersezione generale è **dimostrabilmente non vuota** a livello statico. È
possibile un question plan valido le cui relazioni esplicite contengano, nei source
term autorizzati, ruolo riconosciuto, zona, trigger, finalità, copertura e tutti i cue
di facet/dettaglio attivati. Le otto righe canoniche riproducono tali stringhe senza
prosa aggiuntiva; nessuna regola di `_canonical_blocks()` le vieta e i controlli
lessicali di `audit_answer()` possono quindi risultare positivi.

Questa è una prova di esistenza, non una garanzia per ogni domanda. La compatibilità
dipende accidentalmente dal lessico dei requisiti estratti: V2 rappresenta relazioni,
mentre l'audit V1 pretende anche completezza didattico-documentale non proiettata nel
contratto.

### Piano specifico del Gate

Per il piano autorizzato di `tscv2gate01`, l'intersezione è **dimostrabilmente
vuota** senza modificare il piano o violare il formato canonico. Il blocco perfetto
deve usare esattamente:

- Attore `role:explicit:ala`;
- Compito `copr`;
- Spazio `lato debole`;
- Trigger `alla perdita`;
- Finalità `per evitare`;
- Fase `negative_transition`.

Queste righe coprono `who`, trigger e reason; coprono le facet negative transition e
width tramite “perdita” e “lato debole”. Non contengono però i quattro dettagli
obbligatori della facet negative transition: densità/prossimità, palla
coperta/scoperta, zona di campo e struttura preventiva. `missing_details` non può
essere non vuoto in un audit completo. Inoltre `where` e `coverage_or_risk` non sono
riconosciuti dai cue esatti, anche se una sola dimensione operativa mancante sarebbe
tollerata. Aggiungere tali dettagli come prosa genera `noncanonical_free_prose`;
alterare i source term genera mismatch col piano e/o identità dei termini.

Pertanto il Gate reale non poteva ottenere simultaneamente blocco canonico V2 e audit
V1 positivo, anche se Qwen avesse riprodotto perfettamente il piano.

## Interpretazione del Gate reale

| Fattore | Classificazione | Evidenza |
|---|---|---|
| Piano Qwen strutturalmente diverso e termini invalidi | causa dimostrata del blocco | artefatto Gate; report forense |
| Explanation non canonica | causa dimostrata del blocco | `[REL 0]` su una riga; `_canonical_blocks()` |
| Contenuto insufficiente per audit | causa dimostrata dell'audit negativo | `missing_operational`, `missing_details`, `complete=false` |
| Impossibilità del piano autorizzato di soddisfare i dettagli audit | incompatibilità per-caso dimostrata | termini fissi del piano vs `REQUIRED_DETAILS` |
| Incompatibilità universale TSC V2/audit V1 | falsa | esiste una classe teorica di piani lessicalmente soddisfacenti |

Il risultato `blocked` è quindi una combinazione di violazioni generative reali e di
un conflitto contrattuale indipendente per il caso. Non è un fallimento operativo.

## Opzioni architetturali

| Opzione | Modifiche | Vantaggi | Rischi/limiti | Impatto V1/fail-closed | Complessità |
|---|---|---|---|---|---|
| A — invariati | nessuna | zero delta | validabilità dipende casualmente dal lessico; il Gate analizzato resta insoddisfacibile | V1 invariato; fail-closed conserva un blocco inevitabile | bassa ma non accettabile |
| B — estendere blocco V2 | aggiungere campi/blocchi strutturati per dettagli audit | una sola rappresentazione controllata | gonfia il contratto relazionale con requisiti documentali variabili; migrazione schema | V1 invariato; nuovi check fail-closed | alta |
| C — audit V2 specifico | audit sui campi V2 e sulle evidenze | allinea il controllo alla rappresentazione | può ridurre indebitamente la completezza documentale; richiede nuova semantica di supporto | V1 invariato; fail-closed da preservare | media-alta |
| D — piano canonico + spiegazione documentale separata | mantenere piano/blocco canonico e aggiungere una sezione documentale distinta, con audit e coerenza indipendenti | separa esecuzione tattica e completezza documentale; riusa audit V1 | rischio divergenza piano/prosa e duplicazione; servono riferimenti espliciti alle relazioni e citazioni | V1 invariato; promozione solo se entrambi passano | media |

## Decisione raccomandata

È raccomandata **Opzione D**, con progettazione statica separata prima di qualsiasi
implementazione. Il piano applicato e il blocco relazionale rimangono canonici e
rigidamente validati; una `documentary_explanation` distinta può contenere i dettagli
richiesti dall'audit. Deve essere obbligatoriamente:

1. collegata tramite ID alle relazioni canoniche;
2. limitata alle evidenze recuperate e a citazioni valide;
3. sottoposta all'audit documentale;
4. confrontata deterministicamente col piano per attore, compito, spazio, trigger,
   finalità, fase e polarità;
5. fail-closed se manca, diverge, introduce claim non supportati o non supera l'audit.

Questa scelta non modifica V1 e non usa l'audit V2 come scorciatoia. L'Opzione B è
una seconda scelta se si decide che ogni dettaglio documentale debba diventare parte
normativa del dominio; l'Opzione C da sola non è raccomandata perché rischia di
eliminare requisiti di completezza invece di renderli rappresentabili.

L'intervento minimo successivo è esclusivamente una specifica del doppio output e del
controllo di coerenza; nessun codice o nuovo Gate è autorizzato da questa decisione.

## Diagnostica `omitted`

La futura distinzione `omitted` / `present_but_invalid` migliora attribuzione e
reporting, ma non cambia la soddisfacibilità: una relazione invalida non copre il
requisito e una spiegazione completa non sana il piano. La remediation resta separata.

## Limiti e stati

L'analisi prova la soddisfacibilità dal comportamento statico dei controlli, non la
probabilità che Qwen produca il testo richiesto. L'audit è lessicale: la presenza dei
cue non dimostra da sola verità o qualità tattica, e `audit_relations()` non è
bloccante in questa baseline. Non sono state verificate nuove evidenze documentali.

- revisione contrattuale: **VALIDATO**;
- Gate runtime TSC V2: **BLOCCATO**;
- integrazione runtime: **BLOCCATO**;
- certificazione runtime: **BLOCCATO**.

La raccomandazione architetturale è una decisione ancora da approvare e non autorizza
modifiche, test o nuove inferenze.
