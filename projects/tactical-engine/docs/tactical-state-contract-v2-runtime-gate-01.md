# TSC V2 — primo Gate runtime controllato

## Identità

- Attività: `RD-TSC-V2-RUNTIME-GATE-01`
- HEAD documentale iniziale: `edc44841bcf32b4e684c35e5f732ae8ab573767b`
- Baseline staging: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`
- Request ID: `tscv2gate01`
- Esecuzioni: una; nessun retry o repair

## Preflight immediato

PASS: identità `football@football-data-lab.localdomain`, staging detached alla
baseline esatta e pulito, evaluation scrivibile, quattro artefatti assenti inclusi
symlink dangling, nessun Gate concorrente osservato, modello `qwen3.5:9b`
disponibile, collection candidata presente con count metadata-only 6410.

## Esecuzione

È stato eseguito una sola volta il comando autorizzato. Durata del runner 361,28 s;
durata `/usr/bin/time` 6:22,73. Il client ha osservato una singola risposta Qwen con
`done_reason=stop`, `eval_count=1959`, `prompt_eval_count=2623`; `repair_reasons=[]`.
Il conteggio server-side delle richieste non è disponibile, ma il percorso invocato
contiene una sola chiamata e non sono stati eseguiti rilanci.

Exit code: `1`. Il wrapper ha terminato con
`INCOMPLETE: tactical_state_contract_v2_blocked` dopo avere scritto il report.

## Diagnostica TSC V2

- `overall_status`: `blocked`
- risposta promossa: assente (`answer` e `promoted_answer` vuoti)
- raw model content: presente, 5015 caratteri
- preflight V2: `ready`
- question compatibility: `passed`
- validazione strutturale V1/V2: non valida
- operational coverage: `failed`
- plan/prose alignment: `failed`
- audit documentale: incompleto/negativo

Motivazioni:

- `invalid_operational_term_identity`;
- `explicit_operational_requirement_omitted`;
- `canonical_relation_block_mismatch`;
- `noncanonical_free_prose`;
- `tactical_documentary_audit_failed`.

Il comportamento fail-closed è corretto: nessuna risposta è stata promossa e non è
stato tentato alcun repair.

## Classificazione

- **PASS tecnico limitato**: una generazione terminata normalmente, envelope
  parsabile, report e quattro artefatti prodotti, raw e diagnostica conservati.
- **PASS completo**: NO; i controlli obbligatori non sono positivi.
- **Fail-closed**: SÌ; `blocked`, answer vuoto, motivazioni verificabili.
- **FAIL operativo**: NO per timeout/inizializzazione/artefatti; è tuttavia presente
  l'anomalia di invarianza Chroma descritta sotto.

Questa classificazione non valida la qualità generativa né l'integrazione runtime.

## Artefatti

| Artefatto | Byte | SHA-256 |
|---|---:|---|
| JSON | 58076 | `85b578360639f8e154922d6e70cd753025874124483f9cb956e6f0da920ec22c` |
| stdout | 439 | `7d584972df4b8975b99dfc1354b7a85c920eafb32bf3d639e0cb1bb8ca4f4f97` |
| stderr/time | 1752 | `3b386ff45c874be0ecf6c35b3fe8ad8a8f571af8eba3c65f7a1d00561c2275be` |
| exit code | 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |

Collection count prima/dopo nel report: 6410/6410; `index_unchanged=true`.

## Invarianza e anomalia Chroma

- checkout operativo: HEAD e status fingerprint invariati;
- staging V1: HEAD e status fingerprint invariati;
- staging V2: HEAD invariato; il solo JSON appare non tracciato, mentre gli altri
  artefatti sono presenti ma ignorati dalle regole Git;
- nessun processo Gate residuo.

Il file `chroma.sqlite3` è rimasto della stessa dimensione (254545920 byte) e senza
sidecar, ma SHA-256 e mtime sono cambiati:

- prima: `0d19fbea4df3c4f418e7b55c182c0e268862a53d4f903ddc6cd8a7fe8e74a35b`;
- dopo: `0c563cc4cb57220aa54d4839c388c7eaac02e6247ca91d900c5a645484932b4f`.

Il count invariato non dimostra assenza di modifiche. La causa precisa non è
determinabile dalle evidenze autorizzate; non sono state effettuate correzioni o
ulteriori aperture diagnostiche.

## Decisione e stato

- esecuzione singola Gate: **ESEGUITO**;
- fail-closed del caso: **VALIDATO**;
- Gate runtime TSC V2 complessivo: **BLOCCATO**;
- integrazione runtime: **BLOCCATO**;
- certificazione: **BLOCCATO**.

Qualunque nuova inferenza o diagnosi dell'alterazione SQLite richiede una nuova
autorizzazione esplicita.
