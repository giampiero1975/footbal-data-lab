# Tactical State Contract v1 — prima patch deterministica

Data: 2026-10-28  
Ramo: `codex/tactical-state-contract-v1`  
Base sincronizzata: `1afcd594180ceb29f10b6228c10ea533fd993b28`  
Commit implementazione e test: `c1c2b233f048873368b94900dad779cf14649679`

## Attività

Implementare soltanto schema, derivazioni conservative, normalizzazione,
validazione strutturale/relazionale e rendering del Tactical State Contract v1.
La patch deve rimanere fuori da Qwen/Ollama, runner, API, pannello, profilo locked,
Chroma e corpus. Non comprende feedback o apprendimento.

## Script

- `scripts/v5_tactical_state_contract_v1.py`: schema e funzioni pure;
- `scripts/v5_tactical_query_plan_v1.py`: `analyse()` resta l'unico ingresso e
  allega `state_contract` al piano esistente;
- `tests/test_v5_tactical_state_contract_v1.py`: 17 verifiche deterministiche;
- `tests/test_v5_tactical_query_plan_v1.py`: 18 verifiche storiche riutilizzate
  come regressione del pianificatore.

## Schema implementato

Il contratto separa:

- `actor_ref`: riferimento a una persona esplicitamente citata;
- `role_ref`: ruolo citato senza identità personale;
- `position_slot`: posizione astratta derivata dalla formazione, mai occupante
  implicito;
- `candidate_actor`: ipotesi tattica la cui disponibilità deve essere confermata.

Ogni informazione significativa usa `explicit`, `derived`, `assumed` o `unknown`.
I valori `derived` devono indicare `rule_id`; un valore `unknown` è sempre nullo.
Il piano comprende eventi tipizzati `substitution`, `rotation` ed `expulsion`,
stati distinti per fase e campi di collegamento futuri a job, risposta, modello,
valutazione e correzione. Questi ultimi riutilizzano gli identificativi esistenti:
non è stato creato un archivio di feedback parallelo.

## Invarianti ed evidenze

| Invariante | Test nuovo |
|---|---|
| giocatore esplicito distinto dallo slot astratto | `test_explicit_player_is_not_formation_slot` |
| dati ignoti non promossi a fatti | `test_unknowns_are_not_promoted_to_facts` |
| `analyse()` unico ingresso | `test_analyse_is_the_single_planning_entrypoint` |
| sostituzione coerente a cardinalità invariata | `test_coherent_substitution_preserves_cardinality` |
| attore uscito non riutilizzabile | `test_exited_player_cannot_be_reused` |
| rotazione a cardinalità invariata | `test_rotation_does_not_change_cardinality` |
| espulsione esplicitamente successiva riduce gli effettivi | `test_expulsion_reduces_known_cardinality` |
| ruoli differenti ammessi fra fasi diverse | `test_roles_can_differ_between_phases` |
| doppia assegnazione simultanea bloccata | `test_simultaneous_incompatible_assignments_are_blocking` |
| 4-3-3→3-5-2 verificato come relazione, non ricetta universale | `test_433_to_352_checks_relations_without_prescribing_solution` |
| geometria incompleta qualificata, non falsamente completata | `test_incomplete_formation_geometry_requires_qualification` |
| solo alias sicuri normalizzati | `test_safe_normalization_and_arbitrary_value_rejection` |
| disponibilità candidato ignota qualificata | `test_candidate_availability_is_qualified` |
| risposta parziale conserva fatti validi | `test_partial_render_keeps_valid_facts_and_qualifies_error` |
| rendering non aggiunge giocatori o disponibilità | `test_renderer_does_not_add_players_or_availability` |
| derivazione priva di `rule_id` bloccata | `test_derived_values_require_rule_id` |
| tracciabilità predisposta senza nuovo archivio | `test_trace_is_ready_without_creating_a_feedback_archive` |

I 18 test storici del pianificatore non duplicano questi casi: verificano parsing,
facets, scenari, retrieval, contratti testuali e audit preesistenti. Sono stati
riutilizzati esclusivamente come regressione.

## Comandi ed esiti

Comando riproducibile con Python 3.12:

```powershell
python -m unittest discover -s projects/tactical-engine/tests -p 'test_v5_tactical_state_contract_v1.py'
python -m unittest discover -s projects/tactical-engine/tests -p 'test_v5_tactical_query_plan_v1.py'
python -m py_compile projects/tactical-engine/scripts/v5_tactical_state_contract_v1.py projects/tactical-engine/scripts/v5_tactical_query_plan_v1.py projects/tactical-engine/tests/test_v5_tactical_state_contract_v1.py
git diff --check
```

Output conclusivo:

```text
.................
----------------------------------------------------------------------
Ran 17 tests in 0.007s

OK
..................
----------------------------------------------------------------------
Ran 18 tests in 0.021s

OK
```

`py_compile`: PASS. `git diff --check`: PASS, salvo l'avviso informativo Git
LF→CRLF del checkout Windows.

### Tentativi non conclusivi documentati

1. L'alias Windows Store `python.exe` del sandbox non era eseguibile.
2. La forma `python -m unittest projects/tactical-engine/tests/...` è stata
   interpretata come nome modulo e ha prodotto `ModuleNotFoundError: projects`.
3. È stato usato il runtime Python 3.12.10 portabile già presente nel workspace e
   il comando `unittest discover` riportato sopra. Nessun fallimento del codice è
   rimasto aperto.

## Risultato

- Schema e validator deterministici: **VALIDATO offline** sui casi elencati.
- Regressione del pianificatore esistente: **VALIDATO offline**, 18/18.
- Integrazione Qwen/Ollama, structured output, qualità tattica e pannello:
  **DA FARE**, esplicitamente fuori da questa patch.
- Nessuna chiamata a modello o servizio, nessun benchmark, merge o deploy.

## Decisione e stato

La prima patch deterministica può essere sottoposta a revisione indipendente allo
stesso commit GitHub. Non è **INTEGRATO** né **CERTIFICATO**. La seconda patch
richiede autorizzazione separata dopo la revisione.

## Limiti residui

- L'estrazione conservativa riconosce come identità esplicite soltanto riferimenti
  numerici inequivoci; non tenta ancora di indovinare nomi propri.
- Gli slot 4-3-3 e 3-5-2 rappresentano topologia astratta, non disponibilità della
  rosa né una soluzione tattica prescritta.
- Un'espulsione estratta dal testo ha temporalità non determinabile e quindi
  `affects_current_count=null`; la cardinalità cambia soltanto quando la sequenza
  temporale è esplicita nel piano.
- `QUALIFICATION_REQUIRED` non rende strutturalmente invalido il piano, ma vieta
  di presentare l'informazione come certa.
- Nessun controllo semantico delle citazioni o della qualità della prosa è incluso.

## Confronto tecnico richiesto a ChatGPT

Per evitare una revisione passiva, chiediamo a ChatGPT di esaminare direttamente
il commit e rispondere motivatamente a quattro questioni:

1. È corretto usare `subject` per una trasformazione fra slot astratti e `actor`
   soltanto per identità note, oppure conviene imporre due strutture separate?
2. Concorda con la scelta conservativa di non estrarre nomi propri finché non
   esiste una regola che distingua giocatore, allenatore e avversario?
3. Concorda che un'espulsione senza temporalità esplicita non debba modificare un
   conteggio già dichiarato, evitando il doppio decremento?
4. Quali invarianti relazionali mancano ancora prima della seconda patch, senza
   trasformare il contratto in un catalogo rigido di soluzioni tattiche?

Le eventuali obiezioni dovranno essere confrontate con questi test e con il codice,
non accettate automaticamente.
