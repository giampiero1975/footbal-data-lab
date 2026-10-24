# V5-DEFAULT-PROMOTION-01

## Attività

Promuovere il profilo V5 integrato 10/10 a configurazione ordinaria del wrapper
CLI, conservando un rollback immediato e verificabile.

## Script

- `scripts/run_rag_v5_locked_candidate_v2.py`
- `tests/test_v5_source_hybrid_rank_v4.py`

Senza flag il wrapper usa il profilo integrato. `--integrated-candidate` resta
accettato per compatibilità; `--legacy-profile` ripristina il precedente
comportamento a flag disattivati. Nessun servizio di produzione RAG è attivo
sulla VPS: la promozione riguarda l'entry point CLI autorevole.

## Commit, report e decisione

Commit `040c6a5` — `feat: promote integrated V5 profile by default`. Test
offline complessivi 14/14, compilazione e diff check superati. Dopo deploy è
consentito un solo smoke test
post-promozione senza `--integrated-candidate`, limitato a `fresh_03`, per
verificare profilo, generazione, citazioni e indici. Rollback: ripetere un
eventuale uso operativo con `--legacy-profile`; non modificare le collection.

## Stato

`IMPLEMENTATO`; non ancora `ESEGUITO`, `VALIDATO`, `INTEGRATO` o `CERTIFICATO`.
