# RD-TSC-V2-D3-S2-FIRST-CONTROLLED-RUNTIME-01 — Fase B

## Attivita

Prima esecuzione reale controllata del percorso D3 → S2 Shadow Adapter → NLI V2
Judge Bridge → Qwen 3.5 9B. L'esperimento e esclusivamente diagnostico e non
promuovibile.

## Script, commit ed ambiente

- Baseline e staging: `f2a77deb73b62acac5ec4c478129345196299179`.
- Staging: `/home/football/.local/share/football-data-lab/staging/s2-first-controlled-b1946f8`.
- Runner: `scripts/run_tactical_semantic_support_s2_first_controlled_runtime_v1.py`.
- Interprete read-only: `/opt/football-data-lab/projects/tactical-engine/.venv/bin/python`.
- Python 3.12.3; Pydantic 2.14.1; moduli applicativi caricati dallo staging.
- Modello: `qwen3.5:9b`; `temperature=0`, `num_ctx=4096`, `think=false`.
- Timeout interno: 180 secondi per chiamata; limite esterno: 600 secondi con
  TERM e `--kill-after=30s`; nessun retry e nessun repair.

Comando effettivo, eseguito una sola volta:

```bash
cd /home/football/.local/share/football-data-lab/staging/s2-first-controlled-b1946f8/projects/tactical-engine
timeout --signal=TERM --kill-after=30s 600s \
  env PYTHONDONTWRITEBYTECODE=1 \
  /opt/football-data-lab/projects/tactical-engine/.venv/bin/python -B \
  scripts/run_tactical_semantic_support_s2_first_controlled_runtime_v1.py \
  --fixtures evaluation/tactical_semantic_support_s2_first_controlled_runtime_fixture_v1.json \
  --output evaluation/tactical_semantic_support_s2_first_controlled_runtime_01.json \
  --model qwen3.5:9b \
  --ollama-url http://127.0.0.1:11434 \
  --timeout 180 \
  --max-tokens 1024 \
  --execute
```

## Preflight immediato

PASS alle `2026-11-05T17:58:30Z`: HEAD e working tree conformi, dataset
SHA-256 `8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c`,
fixture e tre casi invariati, output assente, import provenienti dallo staging,
Ollama e modello disponibili, nessun modello caricato o Gate concorrente,
circa 15,5 milioni KiB di memoria disponibile e 40,6 milioni KiB di disco.

## Risultato

- Inizio: `2026-11-05T17:58:30Z`.
- Fine: `2026-11-05T17:59:22Z`.
- Durata osservata: 52 secondi.
- Exit code: `0`.
- Inferenze effettive: 3/3.
- Arresto anticipato: no.
- Errori: nessuno.
- Valutazioni tecnicamente complete: 3/3.
- Corrispondenze con le label umane congelate: 2/3.

| Caso | Attesa | Judge | Esito |
|---|---|---|---|
| `q3_05` | `supported` | `supported` | corrisponde |
| `q3_04` | `contradicted` | `supported` | falso positivo rispetto alla label congelata |
| `q5_08` | `insufficient` | `insufficient` | corrisponde |

Il contratto storico restituisce soltanto la label: la rationale registrata
attesta la provenienza dal judge sulla coppia esatta, ma non fornisce una
spiegazione semantica del verdetto.

## Evidenza e invarianti

Artefatto:
`evaluation/tactical_semantic_support_s2_first_controlled_runtime_01.json`.

- Dimensione: 11.639 byte.
- SHA-256: `0768ca581b2bc6996d13f2b000600735663966ad9959695e11b54cd34c318afa`.
- Schema: `tactical_semantic_support_s2_first_controlled_runtime_report_v1`.
- Modalita: `shadow_only`.
- `promotion_authorized=false` a livello report e per tutti i casi.
- Assessment S1 invariato: 3/3.
- `overall_status` e `promoted_answer` non appartengono a questo runner isolato
  e non sono stati letti o modificati.

Checkout operativo, staging V1 e staging V2 hanno mantenuto HEAD e impronte del
working tree precedenti. Nessun accesso a Chroma, RAG, panel o API e stato
effettuato dal runner. Dopo l'esecuzione Qwen risultava ancora caricato nella
cache Ollama; nessun servizio e stato riavviato o modificato.

## Decisione e stato

- Fase B singola: **ESEGUITO**.
- Funzionamento tecnico, fail-closed disponibile, isolamento S1/S2 e
  non-promozione osservati: **VALIDATO** per questo solo tentativo.
- Correttezza semantica generale: **BLOCCATO**; 2/3 casi noti non costituiscono
  una misura di accuratezza e il falso positivo `q3_04` richiede analisi offline
  separata prima di qualsiasi decisione.
- Gold S2 indipendente, Gate, integrazione e certificazione: **BLOCCATO**.

Non e autorizzato alcun rerun. Il prossimo intervento tecnicamente giustificato
e una revisione forense offline del solo falso positivo `q3_04`, usando
l'artefatto conservato e senza chiamare modelli.
