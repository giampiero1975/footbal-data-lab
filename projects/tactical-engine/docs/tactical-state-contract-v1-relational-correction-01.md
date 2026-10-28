# Tactical State Contract v1 — correzione relazionale deterministica

Data: 2026-10-28
Ramo: `codex/tactical-state-contract-v1`
Base revisionata con ChatGPT: `e338023ba83f51fb4b9ffed8d1a5c44b4771a194`
Commit codice e test: `947e667dc0b6de6cc469469401433514bc67de9d`

## Attività

Correggere le lacune relazionali individuate con revisione incrociata Codex–ChatGPT,
senza cambiare l'architettura e senza collegare il contratto a generazione, runner,
API, pannello, indici, corpus o feedback.

## Script

- `scripts/v5_tactical_state_contract_v1.py`, contratto deterministico v1.1;
- `tests/test_v5_tactical_state_contract_v1.py`, 17 casi originari adattati alle
  modifiche intenzionali dello schema e 24 casi differenziali distinti;
- `tests/test_v5_tactical_query_plan_v1.py`, 18 regressioni storiche riutilizzate.

`scripts/v5_tactical_query_plan_v1.py` non è stato modificato: `analyse()` resta
l'ingresso e tutti i campi precedenti del piano sono preservati.

## Correzioni e invarianti

| Area | Invariante | Evidenza differenziale |
|---|---|---|
| Presenza | citazione non implica presenza | `test_01_mentioned_actor_stays_unknown` |
| Sostituzioni | uscente off-field e entrante on-field bloccati | `test_02_*`, `test_03_*` |
| Severità | ignoto qualificato; azione eseguibile ignota bloccata | `test_04_*`, `test_05_*` |
| Stati | medesima fase in stati successivi ammessa | `test_06_*` |
| Timeline | ordine inverso e cicli bloccati; ordine assente non inventato | `test_07_*`–`test_09_*` |
| Riferimenti | kind verificato; slot vietato come attore concreto | `test_10_*`, `test_11_*` |
| Unicità | attore concreto non duplicabile nello stato | `test_12_*` |
| Continuità | nessun attore perso o aggiunto senza evento | `test_13_*`, `test_14_*` |
| Provenienza | `derived` annidato richiede `rule_id` | `test_15_*`, `test_16_*` |
| Espulsioni | squadra, temporalità e cardinalità coerenti | `test_17_*`–`test_20_*` |
| Rendering | evento bloccato omesso; fatto indipendente conservato | `test_21_*`, `test_22_*` |
| Geometria | mapping astratto separato dagli attori | `test_23_*` |
| Trasformazione | 11 attori unici e continui nel 4-3-3→3-5-2 | `test_24_*` |

La presenza è autorevole per stato (`on_field`, `off_field`, `unavailable`,
`unknown`). La timeline è un grafo parziale aciclico fra `state_id`; `sequence`
viene usata soltanto se disponibile. Le assegnazioni concrete richiedono
`subject_ref` tipizzato e `position_ref`; i mapping astratti usano esclusivamente
`from_slot_ref`/`to_slot_ref`. Un dato `derived` senza `rule_id` è bloccato a ogni
livello. L'espulsione distingue la squadra dell'evento e, se nota, quella
dell'attore. Il rendering mostra prima i blocchi e non presenta l'evento invalido.

## Comandi riproducibili ed esiti

```powershell
python -m unittest discover -s projects/tactical-engine/tests -p 'test_v5_tactical_state_contract_v1.py'
python -m unittest discover -s projects/tactical-engine/tests -p 'test_v5_tactical_query_plan_v1.py'
python -m py_compile projects/tactical-engine/scripts/v5_tactical_state_contract_v1.py projects/tactical-engine/scripts/v5_tactical_query_plan_v1.py projects/tactical-engine/tests/test_v5_tactical_state_contract_v1.py
git diff --check
```

Output:

```text
.........................................
----------------------------------------------------------------------
Ran 41 tests in 0.027s
OK

..................
----------------------------------------------------------------------
Ran 18 tests in 0.020s
OK
```

`py_compile`: PASS. `git diff --check`: PASS, esclusi i soli avvisi informativi
LF→CRLF del checkout Windows. Nessuna chiamata a modello, servizio o VPS.

## Risultato, decisione e stato

- schema/funzioni: **IMPLEMENTATO**;
- suite deterministiche: **ESEGUITO** 41/41 + 18/18;
- isolamento dal runtime: **VALIDATO**;
- invarianti relazionali coperti dai casi elencati: **VALIDATO offline**;
- integrazione generativa e qualità tattica: **DA FARE** e fuori perimetro.

Decisione: pubblicare il commit per una nuova revisione tecnica con ChatGPT come
collega indipendente. L'autorizzazione operativa appartiene al titolare; il
confronto con ChatGPT produce accordo o dissenso tecnico, non permessi operativi.
Nessun merge o deploy. La patch non è **INTEGRATO** né **CERTIFICATO**.

## Limiti residui

- I nomi propri non vengono estratti automaticamente.
- Una domanda senza ordine conserva eventi non collegati e qualificati.
- La continuità completa richiede `presence_complete=true`; non viene dedotta.
- `substitution_mode` resta `unknown` se non dichiarato; nessun default nascosto.
- Gli attori con squadra ignota restano qualificati negli eventi che richiedono
  la distinzione own/opponent.
- Il contratto verifica struttura e relazioni, non correttezza tattica, supporto
  documentale o qualità della prosa.
