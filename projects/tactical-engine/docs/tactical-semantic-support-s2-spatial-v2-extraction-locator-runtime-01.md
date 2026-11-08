# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-01

## Identità e perimetro

- data: 2026-11-08;
- branch: `codex/tactical-state-contract-v1`;
- baseline autorizzata: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- tentativo: `spatial-v2-extraction-locator-q3-04-runtime-01`;
- caso previsto: `q3_04`, Gold `contradicted`;
- comando: wrapper Bash integralmente approvato, eseguito una sola volta;
- retry, repair, fallback e seconde esecuzioni: zero.

L'autorizzazione consentiva una sola esecuzione, subordinata al superamento del
preflight. Il wrapper si è arrestato nel preflight prima di contattare Ollama o
avviare Qwen. Non è stato effettuato alcun rilancio.

## Risultato del preflight

Il controllo sul file descriptor del lock ha prodotto
`E_LOCK_FD_NOT_REGULAR`. Il wrapper confronta esattamente l'output di
`stat -Lc '%F' /proc/$$/fd/9` con `regular file`; sul sistema il lock creato è
un file regolare vuoto e `stat` lo descrive come `regular empty file`.

Il controllo ha quindi operato fail-closed, ma ha respinto un file regolare a
causa della classificazione testuale più specifica restituita da GNU `stat`.
Non sono stati raggiunti i successivi controlli di staging, modello e
concorrenza, né la generazione.

## Evidenze finalizzate

Directory artefatti:
`/home/football/.local/share/football-data-lab/runtime-artifacts/spatial-v2-extraction-locator-q3-04-runtime-01`.

| Artefatto | Byte | SHA-256 / verifica |
|---|---:|---|
| `attempt_progress.json` | 385 | `13718ded76bc00ab77080888dc451754869008d1a46263fe5a312540ed44b27f`, PASS |
| `attempt_state.json` | 589 | `e1d3d8b8ad9874bbdc938b95d8e0f9de19af7e896ae5a65f7fa267a117b03f08`, PASS |
| `hashes.sha256` | 88 | `32b2146417017015a8ce3a10414a10cf85012fb212c089706959cbed31d06d96` |
| `attempt_state.sha256` | 85 | verifica PASS |
| `hashes.sha256.digest` | 80 | presente |

`attempt_state.json` registra:

- `finalization_complete=true`;
- `phase=preflight`;
- `attempt_status=blocked_preflight`;
- `reason_code=E_LOCK_FD_NOT_REGULAR`;
- `generation_started=false` e `generation_completed=false`;
- `transport_attempted=false`, `transport_calls=0` e
  `response_received=false`;
- `supervised_exit_code=null`, `wrapper_exit_code=62`;
- `promotion_authorized=false`.

Il lock è stato verificato come `regular empty file`, modo `0600`, proprietario
`football:football`. `sha256sum -c` ha verificato sia l'inventario disponibile
sia lo stato finale.

Sono assenti, coerentemente con l'arresto pre-inferenza:
`request_payload.json`, `raw_response.json`, `result.json`,
`generation_record.json`, `decision.json`, `stdout.log` e
`time_stderr.log`. La loro assenza non è perdita di evidenza runtime: la
generazione non è mai iniziata.

## Classificazione

| Dimensione | Esito |
|---|---|
| Finalizzazione del tentativo | **VALIDATO** per l'arresto preflight osservato |
| Preflight completo | **BLOCCATO** |
| Chiamate Qwen/Ollama | 0 |
| Successo tecnico generativo | non valutabile, generazione non avviata |
| Witness | non prodotto, non valutabile |
| Correttezza semantica | non valutabile |
| Fail-closed | **VALIDATO** per questo singolo arresto |
| Runtime Extraction Locator | **BLOCCATO** |
| Gate, integrazione e certificazione | **BLOCCATO** |

## Decisione

L'unica esecuzione autorizzata è consumata e conclusa con arresto fail-closed
nel preflight. Non è autorizzato alcun secondo tentativo. Il runtime non è
promosso e nessuna proprietà generativa o semantica viene dichiarata validata.

Flusso: Attività = singolo tentativo runtime autorizzato; Script = wrapper Bash
approvato; Commit = documentale; Report = questo documento; Risultato =
`blocked_preflight`, zero generazioni; Decisione = nessun retry e nessuna
promozione; Stato = **BLOCCATO**.
