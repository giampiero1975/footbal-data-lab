# V5-NAMED-SOURCE-CONTEXT-FILTER-01

## Attività

Impedire che tassonomie omonime di fonti estranee contaminino risposte che
attribuiscono esplicitamente una tesi a un singolo autore. Il caso osservato è
la `zona B` di Foscarini confusa con la diversa `zona B` di Indiani.

## Script

- `scripts/smoke_test_rag_v5_e2e.py`
- `scripts/run_rag_v5_locked_candidate_v2.py`
- `tests/test_v5_source_hybrid_rank_v4.py`

Con `--source-aware`, una domanda che nomina un solo autore noto conserva nel
contesto finale soltanto gli estratti di quella fonte, purché ve ne sia almeno
uno. Le domande comparative o che richiedono il manuale interno restano
multi-fonte. Gli ID esclusi sono registrati nel report. Nessun ID benchmark,
pagina o tassonomia tattica è codificato.

## Commit

- `33749bf` — `fix: isolate explicitly named source context`.
- `8404495` — `fix: allow scoped locked diagnostics`.

## Report

Output VPS previsto: `evaluation/v5_named_source_context_fresh07_v1.json`.

## Risultato

- Test offline complessivi: `8/8` superati.
- Compilazione sintattica: superata.
- Runtime VPS: `DA FARE`.

## Decisione

Consentire una sola generazione differenziale `fresh_07` dopo test offline e
deploy. Validare soltanto se la risposta usa la tassonomia Foscarini, copre
pressioni laterali/perdita pericolosa/playmaker braccati, non universalizza il
divieto di costruzione laterale, non cita fonti estranee e lascia gli indici
invariati.

## Stato

`IMPLEMENTATO` dopo commit; non `ESEGUITO`, `VALIDATO`, `INTEGRATO` o
`CERTIFICATO`.
