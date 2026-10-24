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
- `9a1a903` — `fix: complete lateral-zone attribution`.

## Report

Output VPS: `evaluation/v5_named_source_context_fresh07_v1.json`.
SHA-256: `4298e32bdff76615fa1cd0369e2bb36ee928a96c611b8bb70245b2c1d812230f`.

## Risultato

- Test offline complessivi: `8/8` superati.
- Compilazione sintattica: superata.
- Runtime VPS: `COMPLETE 1/1` in 97.32 s.
- Quattro evidenze estranee escluse; contesto finale composto da quattro
  estratti Foscarini, citazioni invalide 0, indici 5319/34 invariati.
- Pressioni laterali e perdita in zona pericolosa presenti.
- Mandatory claim incompleto: la risposta non menziona i playmaker braccati.
- Formulazione non supportata/ambigua: definisce la zona «molto pericolosa per
  l'avversario», mentre la fonte non attribuisce così il destinatario del
  pericolo.

## Decisione

Il filtro di fonte è verificato, ma la risposta V1 non è validata. Non ripetere
la stessa configurazione. La prossima variante è consentita soltanto con una
differenza tecnica che richieda completezza fra difficoltà dei playmaker e dei
laterali, mantenga neutra l'attribuzione del pericolo e impedisca di trasformare
il rischio situazionale in divieto universale.

La differenza è implementata in `9a1a903`; i test offline complessivi sono ora
`9/9` e la compilazione è superata. È autorizzata una sola generazione V2 in
`evaluation/v5_named_source_context_fresh07_v2.json`.

## Stato

Filtro V1 `ESEGUITO`; guida V2 `IMPLEMENTATO`. Non `VALIDATO`, `INTEGRATO` o
`CERTIFICATO`.
