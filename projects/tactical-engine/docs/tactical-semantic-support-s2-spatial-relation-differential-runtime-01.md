# RD-TSC-V2-D3-S2-SPATIAL-RELATION-DIFFERENTIAL-01 — Fase B

## Attivita e ambiente

Singola esecuzione runtime autorizzata del Gate differenziale
`nli_spatial_relations_v1` 1.0. Baseline GitHub e staging:
`0d40719555d4ad13eb43ab2897cf26dea73ea47f`.

- Host: `football-data-lab.localdomain`, utente `football`, alias
  `football-vps` (`163.5.26.155:22`).
- Staging indipendente:
  `/home/football/.local/share/football-data-lab/staging/s2-spatial-differential-0d40719`.
- Interprete read-only:
  `/opt/football-data-lab/projects/tactical-engine/.venv/bin/python`.
- Python 3.12.3; Pydantic 2.14.1.
- Modello locale: `qwen3.5:9b`; Ollama attivo, nessun modello residente e zero
  processi Gate concorrenti al preflight.
- Dataset LF SHA-256:
  `8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c`.
- Contratto importato dallo staging:
  `nli_spatial_relations_v1`, istruzione SHA-256
  `861dbec3daac9ac34169356ad51a453f6267175afaa5d296f84c92586d2f3a00`.

Il preflight ha verificato HEAD detached, working tree pulito, moduli provenienti
esclusivamente dallo staging, fixture/runner conformi, output e log assenti,
risorse disponibili (circa 40,6 milioni KiB disco e 15,5 milioni KiB memoria),
modello presente e nessuna concorrenza osservabile.

Lo staging e stato creato da bundle Git completo, 2.153.145 byte, SHA-256
`78be7de6d4280be3c43f38b2f6584b7e8bfa931a92c8c59ad973cd1ce7ec4370`.
Il checkout operativo e rimasto a `1a80fe0c6261b10f748a36c2b4fd96e8e2253971`
con impronta status invariata
`038f601eac17db4f54c73860021c03d3f692a30b56282c9f60b1a15b2ea7da23`.

## Comando eseguito una sola volta

```bash
cd /home/football/.local/share/football-data-lab/staging/s2-spatial-differential-0d40719/projects/tactical-engine
/usr/bin/time -v timeout --signal=TERM --kill-after=30s 600s \
  env PYTHONDONTWRITEBYTECODE=1 \
  /opt/football-data-lab/projects/tactical-engine/.venv/bin/python -B \
  scripts/run_tactical_semantic_support_s2_spatial_relation_differential_v1.py \
  --fixtures evaluation/tactical_semantic_support_s2_spatial_relation_differential_fixture_v1.json \
  --output evaluation/tactical_semantic_support_s2_spatial_relation_differential_01.json \
  --model qwen3.5:9b \
  --ollama-url http://127.0.0.1:11434 \
  --timeout 180 \
  --max-tokens 1024 \
  --execute
```

Inizio `2026-11-05T19:49:11Z`, fine `2026-11-05T19:50:18Z`; durata di
`/usr/bin/time`: 66,35 secondi. Exit code 0. Timeout esterno non intervenuto.
Nessun retry, repair, fallback o chiamata NLI V2.

## Completamento tecnico

- `planned_evaluations=3`.
- `attempted_evaluations=3`.
- `completed_evaluations=3`.
- `run_complete=true`; `stopped_early=false`.
- Tre record `evaluation_status=evaluated` e `technical_pass=true`.
- S1 invariato 3/3; `promotion_authorized=false` nel report e nei tre record.
- `authoritative_outputs_modified=false`; nessun `not_evaluable`.

Il completamento tecnico e **VALIDATO** per questa singola esecuzione. I
contatori descrivono valutazioni applicative, non richieste HTTP osservate dal
server.

## Risultato semantico

| Caso | Ruolo | Gold | Spatial V1 | Corrispondenza |
|---|---|---|---|---|
| `q3_04` | regressione nota | `contradicted` | `supported` | no |
| `q5_06` | controllo distinto ma correlato | `contradicted` | `contradicted` | si |
| `q5_02` | protezione insufficient | `insufficient` | `insufficient` | si |

`q3_04` non e stato corretto: il risultato coincide con il falso positivo V2
storico (`supported`). `q5_06` mostra una corrispondenza sulla relazione
rapido/lento, senza provare generalizzazione indipendente. `q5_02` non mostra una
falsa contraddizione. Totale: 2/3 corrispondenze.

Il Gate e tecnicamente completo ma la corrispondenza semantica complessiva non e
**VALIDATO**. Non e dimostrato alcun miglioramento generale rispetto a V2.

## Artefatti

| Artefatto staging | Byte | SHA-256 |
|---|---:|---|
| `tactical_semantic_support_s2_spatial_relation_differential_01.json` | 13.138 | `a06ba357471681f2ac047af9cff8293d23e75f1c8c8e364f1b14fc4990f8c42d` |
| `tactical_semantic_support_s2_spatial_relation_differential_01.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `tactical_semantic_support_s2_spatial_relation_differential_01.time_stderr.log` | 1.214 | `e21c36daac4a806f19a2445a48c6ed458dfbda22992b32194fa543914ff9f60e` |
| `tactical_semantic_support_s2_spatial_relation_differential_01.exit_code.txt` | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |

Il JSON e stato copiato byte-identico in `evaluation/` e versionato. I tre log
diagnostici restano nello staging.

## Anomalia di provenienza testuale

Il report di primo livello identifica correttamente judge, contratto, versione e
digest spatial. Nei record S2, il bridge tecnico riutilizzato conserva tuttavia
il nome storico `shadow-nli-v2-s2-bridge` e la rationale fissa `NLI V2 returned
the recorded label`. Il runner non ha importato o chiamato il judge V2: il
callable iniettato era `shadow_nli_spatial_relations_v1_inference.judge_pair`,
come attestano `runtime_config`, descriptor e percorso importato.

L'anomalia non cambia i verdetti o il routing osservato, ma rende fuorviante la
provenienza testuale annidata. Non e stata corretta dopo il runtime, in conformita
al divieto di modifiche applicative. Richiede valutazione offline separata prima
di riutilizzare questo formato come evidenza autonoma.

## Isolamento e decisione

Checkout operativo invariato; staging precedenti, RAG, Chroma, corpus, panel,
API, servizi, NLI V2, S1, fixture, contratto e runner non modificati. Ollama ha
mantenuto il modello in cache dopo il run; nessun servizio e stato riavviato.

- Esecuzione Fase B: **ESEGUITO**.
- Completamento tecnico del singolo run: **VALIDATO**.
- Corrispondenza `q5_06` e `q5_02`: **VALIDATO** nel solo perimetro dei casi.
- Corrispondenza complessiva 3/3: **BLOCCATO** (`q3_04` errato).
- Affidabilita generale, integrazione e certificazione: **BLOCCATO**.

Unico prossimo passo: revisione indipendente offline del JSON e dell'anomalia di
provenienza del bridge, senza nuove inferenze. Nessun rerun e autorizzato.
