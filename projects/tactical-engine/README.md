# DRIBBLING — indice operativo

Questo repository documenta configurazioni, verifiche e sperimentazioni del RAG tattico. **Non assumere che il codice Git corrisponda allo stato runtime della VPS senza un controllo di sincronizzazione.**

## Pipeline operativa certificata

- branch operativo: `main`;
- entry point CLI: `scripts/run_rag_v5_locked_candidate_v2.py`;
- profilo predefinito: V5 integrato;
- rollback applicativo: `--legacy-profile`;
- embedding: Ollama `qwen3-embedding:0.6b`;
- generazione: Ollama `qwen3.5:9b`;
- reranker: `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`;
- collection: `dribbling_tactics_v5_multisource` (5319) e
  `dribbling_tactics_v5_exercise_candidate_v1` (34).

Esecuzione dalla root del repository VPS:

```bash
projects/tactical-engine/.venv/bin/python \
  projects/tactical-engine/scripts/run_rag_v5_locked_candidate_v2.py \
  --execute
```

Il comando esegue il manifest locked; non è ancora un servizio HTTP. Prima di
un uso diverso consultare `docs/v5-certification-closeout-01.md`. Non ripetere
il benchmark certificato senza una differenza tecnica documentata.

## Punto di partenza (evitare controlli ripetuti)
1. Leggere [todo.md](todo.md) per priorità e attività aperte.
2. Leggere [docs/environment.md](docs/environment.md) per l'ultima fotografia verificata della VPS e la sua validità.
3. Leggere [docs/components.md](docs/components.md) per modelli, versioni, abbinamenti e stato dei componenti.
4. Leggere [docs/verification.md](docs/verification.md) per verificare **solo** i dati mancanti o scaduti.
5. Consultare [experiments/README.md](experiments/README.md) prima di ripetere un benchmark.
6. Leggere [docs/decisions.md](docs/decisions.md) per evitare di riaprire scelte già motivate.

**Non cancellare collection o modelli operativi durante un audit.** I report di
sola lettura possono essere versionati dopo revisione per escludere segreti e
dati personali. I file voluminosi e gli indici restano fuori da Git.

Classificazione completa degli script:
`docs/script-classification-v2.md`. Manifest hash delle evidenze runtime:
`evaluation/runtime_evidence_manifest_v1.json`.
