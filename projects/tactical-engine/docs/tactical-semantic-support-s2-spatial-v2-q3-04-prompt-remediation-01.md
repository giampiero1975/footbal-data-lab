# RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-PROMPT-REMEDIATION-01

## Baseline e causa

- baseline GitHub iniziale:
  `7b461ebb710809b21d1b46d09e7b6622a07ff742`;
- root cause:
  `tactical-semantic-support-s2-spatial-v2-q3-04-witness-root-cause-01.md`;
- perimetro: handoff normativo del prompt Spatial V2, esclusivamente offline.

Il witness runtime completo aveva 16 anchor con span presenti ma offset errati e
quantificatori `explicit/absent/[]`. Specifica e validatore erano coerenti; il
prompt effettivo non trasmetteva tutte le regole deterministiche.

## Modifica tecnica

File funzionale modificato:
`scripts/shadow_nli_spatial_relations_v2_inference.py`, costante `INSTRUCTION`.
`build_prompt()` e ogni altra funzione sono invariati.

Il prompt ora dichiara esplicitamente:

1. sorgente esclusiva: testo originale del rispettivo claim/evidence;
2. offset Unicode code-point, zero-based, intervallo semiaperto `[start,end)`;
3. `source_text[start:end] == exact_span`, case-sensitive;
4. divieto di offset del prompt, token o byte e di stime, approssimazioni,
   normalizzazioni o correzioni implicite;
5. quantificatore non osservato `implicit/none/null/[]`;
6. sentinella distinta `absent/absent/null/[]`;
7. condizioni per `explicit`, `ambiguous`, `unknown` e `numeric`;
8. divieto esplicito di `explicit/absent/""/[]`;
9. obbligo congiunto di schema JSON e vincoli deterministici.

Non sono stati modificati `SPATIAL_V2_SCHEMA`, validatore, specifica, parsing,
classificazioni, modello, temperatura, contesto, `num_predict`, timeout o
fail-closed. Non sono stati introdotti offset automatici, repair, retry,
fallback o chiamate aggiuntive.

## Test differenziale

Eseguito esclusivamente:

```text
test_20_runtime_prompt_handoff_and_known_invalid_witness_fail_closed
```

Risultato: **1/1 PASS**, Python 3.13, trasporto mock e zero rete.

Il test intercetta il payload e verifica regole normative, claim/evidence
invariati, `qwen3.5:9b`, schema identico, temperatura 0, contesto 4096,
`num_predict=2048`, timeout default 180, una chiamata e descrittore con
retry/repair/fallback false. Un witness mock con anchor errato e
`explicit/absent/[]` resta `not_evaluable`, contiene entrambi i codici previsti
e mantiene `promotion_authorized=false`.

Le suite storiche non sono state ripetute: schema, validatore e relativi rami
sono immutati.

## Limiti e decisione

Il test dimostra che le regole sono trasmesse al modello e che il fail-closed è
preservato; non dimostra che Qwen le rispetterà, né validità semantica o
prestazioni runtime. Una nuova generazione richiede autorizzazione separata.

Flusso: Attività = remediation prompt; Script = judge e singolo test mock;
Commit = commit dedicato; Report = questo documento; Risultato = 1/1 PASS;
Decisione = sottoporre la remediation alla revisione indipendente, senza
runtime.

| Componente | Stato |
|---|---|
| Correzione prompt | **IMPLEMENTATO** |
| Test differenziale offline | **ESEGUITO** |
| Handoff normativo interessato | **VALIDATO** offline |
| Nuova generazione q3_04 | **DA FARE** previa autorizzazione |
| Efficacia Qwen, semantica, promozione, Gate, integrazione, certificazione | **BLOCCATO** |
