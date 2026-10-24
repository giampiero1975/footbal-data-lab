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

## Risultato

Smoke VPS `evaluation/v5_default_promotion_smoke_fresh03_v1.json`, SHA-256
`81481332bac25ab6cfdac60f72060e1dcb4f2cdff93fe95c402c69989deee472`.
Il wrapper senza flag dichiara `PROFILE integrated`; tutti i cinque flag del
profilo sono attivi. Risposta ed evidenze `fresh_03` sono identiche alla
regressione 10/10; citazioni invalide 0, indici 5319/34 invariati, 164.81 s.
Rollback verificato offline tramite `--legacy-profile` e test 14/14.

## Decisione

Promozione VALIDATA e profilo ordinario INTEGRATO nell'entry point CLI. Non
esiste un servizio RAG attivo sulla VPS da riavviare o riconfigurare.

## Stato

`INTEGRATO`. La certificazione complessiva è registrata nel closeout separato.
