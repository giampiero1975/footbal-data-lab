# TSC V2 generative handoff — incompatibilita phase-state 01

Data: 2026-11-03
Attivita: `RD-TSC-V2-GENERATIVE-HANDOFF-IMPLEMENTATION-01`
Baseline: `6b60e2aefbd91adcf8bd3a7f9888d109a8474082`

## Attivita e arresto

La sessione era autorizzata a implementare l'handoff generativo TSC V2
offline, con arresto obbligatorio davanti a un'incompatibilita concreta con il
dominio o con il contratto approvato. La riconciliazione statica ha rilevato
l'incompatibilita prima di modificare i quattro file tecnici. Nessun test,
inferenza o runtime e stato eseguito.

## Evidenza nel codice

`v5_tactical_query_plan_v1.relation_requirements()` deriva termini di fase
espliciti dalle facet della domanda, inclusi `alla perdita` e `transizione
negativa` (`scripts/v5_tactical_query_plan_v1.py`, righe 253-283).

Separatamente, `v5_tactical_state_contract_v1.build_question_plan()` costruisce
sempre un solo stato iniziale:

```text
phase_states = [state("state:initial", ...)]
```

`state()` usa per default `phase="unknown"` (`scripts/v5_tactical_state_contract_v1.py`,
righe 386-397 e 470-487). Non viene creato uno stato `negative_transition`
quando la domanda contiene `alla perdita`.

`v5_tactical_state_contract_v2.project_relation_requirements()` puo invece
classificare il requisito come `explicit_representable`, perche verifica che il
termine di fase sia risolvibile nella tabella V2, non che esista gia un
`phase_state` corrispondente nel question plan (`scripts/v5_tactical_state_contract_v2.py`,
righe 160-185).

Il validatore V2 consente che il piano applicato generato contenga uno stato di
fase risolvibile e verifica poi `phase_state_ref` e coerenza della fase. Il
contratto implementativo approvato e piu restrittivo: il preflight deve usare
soltanto stati gia presenti nel question plan e deve vietare sia la derivazione
di un nuovo state ID sia il completamento automatico di `phase_states`.

## Incompatibilita

Per una domanda con requisito esplicito di fase, per esempio `alla perdita`, il
question plan contiene:

- requisito relazionale con fase `negative_transition`;
- soltanto `state:initial` con fase `unknown`.

Non esiste quindi un `phase_state_ref` completo e univoco che soddisfi il
preflight approvato. Le sole alternative sarebbero:

1. restituire sempre `not_evaluable` per tali requisiti, rendendo inefficace
   l'handoff sulle relazioni di fase;
2. inventare o derivare un nuovo state ID nel modulo generativo, vietato dal
   contratto approvato;
3. modificare planner o dominio per materializzare lo stato richiesto,
   intervento fuori dal perimetro autorizzato.

Nessuna delle tre alternative puo essere scelta autonomamente senza alterare
la decisione contrattuale.

## Risultato e decisione

**Attivita**: riconciliazione pre-implementativa.
**Script**: nessuna modifica.
**Commit**: solo closeout documentale del blocco.
**Report**: questo documento.
**Risultato**: incompatibilita statica verificabile fra question plan e regola
preflight sui riferimenti di fase.
**Decisione**: arresto fail-closed; richiedere al titolare di scegliere se
autorizzare una regola deterministica di materializzazione dello stato o una
modifica versionata del planner. Non introdurre correzioni arbitrarie.
**Stato**: handoff generativo TSC V2 **BLOCCATO**; dominio TSC V2 precedente
resta **VALIDATO offline**; runtime, integrazione e certificazione **BLOCCATO**.

TSC V1, planner V1, dominio V2, retrieval, runner, prompt, API e pannello sono
invariati. Nessun test, inferenza, Ollama, Chroma, API, retry, repair, deploy o
merge e stato eseguito.
