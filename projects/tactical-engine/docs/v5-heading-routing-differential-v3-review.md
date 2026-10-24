# V5-HEADING-ROUTING-INTEGRATION-03 — differenziale VPS V3

## Attività

Verificare sulla VPS la selezione semantica del manuale introdotta dopo il
differenziale V2 non validato. Il nuovo test era consentito perché V3 sostituisce
il ranking basato principalmente sul numero di intestazioni con un cross-encoder
applicato al titolo e agli estratti indicizzati dei manuali.

## Script

- `scripts/v5_source_semantic_rank_v3.py`
- `scripts/v5_heading_reservation_v2.py`
- `scripts/smoke_test_rag_v5_e2e.py`
- `scripts/run_rag_v5_locked_candidate_v2.py`

Comando eseguito sulla VPS, sul ramo
`codex/v5-heading-routing-integration` al commit `eef7e3c`:

```bash
projects/tactical-engine/.venv/bin/python \
  projects/tactical-engine/scripts/run_rag_v5_locked_candidate_v2.py \
  --execute \
  --heading-routing \
  --only-ids fresh_03 \
  --output projects/tactical-engine/evaluation/v5_heading_routing_generic_fresh03_v3.json
```

Prima dell'esecuzione, i tre script modificati sono stati verificati con
`python3 -m py_compile`.

## Commit

Implementazione verificata: `cb8cdb1`, `af903d1`, `df514a3`, `4c8bb24`,
`362e6cd`; stato del ramo al test: `eef7e3c`.

## Report

Output VPS:
`projects/tactical-engine/evaluation/v5_heading_routing_generic_fresh03_v3.json`.

SHA-256:
`b5ebc372a7a1155b88fd217054b1030114c3d1e88593b66b7f1db2deb9cd4e6a`.

## Risultato

- Esecuzione completata: `1/1`, elapsed `136.03 s`.
- Modello: `qwen3.5:9b`.
- Collection: `dribbling_tactics_v5_multisource`.
- Chroma invariato: `5319 -> 5319`; `index_unchanged=true`.
- Citazioni emesse: F1, F2, F3, F6, F7, F8; citazioni invalide: `0`.
- Fonte scelta da V3: `Manuale_Diagonali_Difensive`.
- Fonte pertinente attesa dalle evidenze già validate:
  `Transizioni Offensive e Difensive`.
- Heading riservati: `4-2-3-1`, `4-3-3`, `4-4-2`.
- Copertura richiesta dalle evidenze precedenti: `4-3-3`, `4-4-2`, `3-5-2`,
  `3-4-2-1`.
- La risposta esplicita correttamente che descrizioni statiche prive di dati
  comparativi non dimostrano un effetto causale del cambio di modulo sul rischio.
- La risposta non copre però l'insieme dei quattro moduli richiesto.

Il ranking semantico migliora V2, perché non seleziona più
`FOOTBALL_DATA_LAB_Attacco_della_Profondita_Manuale`, ma ottimizza la somiglianza
lessicale con i concetti di difesa e rischio e continua a scegliere una fonte
diversa da quella necessaria per la copertura tattica validata.

## Decisione

V3 non è validato. Non integrare il comportamento nella pipeline ordinaria e
non modificare il benchmark locked, che resta `5/10`. Non ripetere lo stesso
test. Un'eventuale V4 richiede prima una differenza tecnica documentata che
separi pertinenza semantica della fonte e copertura delle intestazioni
necessarie, senza hardcoding di ID benchmark o delle quattro formazioni.

## Stato

`ESEGUITO`. Non `VALIDATO`, `INTEGRATO` o `CERTIFICATO`.
