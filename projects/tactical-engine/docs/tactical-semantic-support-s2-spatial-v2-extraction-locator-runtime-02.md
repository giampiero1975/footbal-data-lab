# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-02

## Attività e identità

- data: 2026-11-08;
- branch: `codex/tactical-state-contract-v1`;
- HEAD documentale iniziale: `5d3eed936629829192dfaa21e70246c0616e105f`;
- baseline applicativa richiesta: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- tentativo: `spatial-v2-extraction-locator-q3-04-runtime-02`;
- wrapper: `spatial-v2-extraction-locator-q3-04-runtime-02.sh`;
- wrapper SHA-256 verificato prima dell'avvio:
  `5bcc18266daadb984f5dc8b6256f2bb1a8d095eecab8a03948bef14c8fbcfcaf`;
- esecuzioni effettive del wrapper: una;
- retry, repair, fallback e ulteriori tentativi: zero.

TODO ed Experiment Register su GitHub non contenevano una precedente esecuzione
di `runtime-02`; HEAD locale e remoto coincidevano con il commit documentale
iniziale e il working tree era pulito.

## Script e preflight

Il wrapper approvato è stato avviato senza modifiche. Il lock corretto ha
superato la fase che aveva bloccato `runtime-01`: sono stati prodotti lo
snapshot processi e gli artefatti di avanzamento. Il preflight si è poi
arrestato con `E_PATH_MISSING`, exit wrapper `68`, nel controllo dei percorsi di
staging.

La verifica read-only successiva ha identificato il prerequisito mancante:

- parent `/home/football/.local/share/football-data-lab/staging`: presente e
  directory;
- staging richiesto
  `/home/football/.local/share/football-data-lab/staging/spatial-v2-extraction-locator-db3ad66`:
  assente;
- di conseguenza assenti anche `projects/tactical-engine`, `scripts` ed `eval`
  sotto tale staging.

Il wrapper non ha raggiunto i controlli Git della baseline, il controllo del
modello o la fase generativa. Non sono state effettuate modifiche per creare o
correggere lo staging.

## Artefatti e integrità

Directory:
`/home/football/.local/share/football-data-lab/runtime-artifacts/spatial-v2-extraction-locator-q3-04-runtime-02`.

| Artefatto | Byte | SHA-256 / verifica |
|---|---:|---|
| `attempt_progress.json` | 385 | `13718ded76bc00ab77080888dc451754869008d1a46263fe5a312540ed44b27f`, PASS |
| `process_snapshot_before.txt` | 12092 | `0493f5e44cef9767f97fb2dcb782f47685d74db7d5894470be10a04afce2dcb5`, PASS |
| `attempt_state.json` | 582 | `24fdd2da0dca8b809abb09e2fab031117a2d426c2261cbbf4463115f13824bc2`, PASS |
| `hashes.sha256` | 182 | `56b424068cdd735e18b85d03734c128a49ec5a76fd9886602118e77c0b8d913b` |
| `hashes.sha256.digest` | 80 | presente |
| `attempt_state.sha256` | 85 | verifica PASS |

Lo stato finale registra:

- `finalization_complete=true`;
- `phase=preflight`;
- `attempt_status=blocked_preflight`;
- `reason_code=E_PATH_MISSING`;
- `generation_started=false` e `generation_completed=false`;
- `transport_attempted=false`, `transport_calls=0` e
  `response_received=false`;
- `supervised_exit_code=null`, `wrapper_exit_code=68`;
- `promotion_authorized=false`.

Nessun processo generativo relativo al tentativo era osservabile nella verifica
conclusiva. Gli artefatti di richiesta, risposta, extraction, witness,
validazione e decisione non esistono perché la generazione non è stata avviata.

## Risultato, decisione e stato

| Dimensione | Risultato |
|---|---|
| Integrità wrapper | **VALIDATO** rispetto al digest autorizzato |
| Correzione lock | superata nel percorso osservato |
| Finalizzazione del singolo tentativo | **VALIDATO** |
| Preflight completo | **BLOCCATO** per staging assente |
| Generazioni Qwen | 0 |
| Successo tecnico generativo | non valutabile |
| Witness | non prodotto, non valutabile |
| Correttezza semantica | non valutabile |
| Fail-closed del singolo arresto | **VALIDATO** |
| Runtime Extraction Locator | **BLOCCATO** |
| Gate, integrazione e certificazione | **BLOCCATO** |

L'unico tentativo autorizzato è consumato. Non è stato effettuato né è
autorizzato un terzo tentativo. La preparazione di uno staging conforme richiede
un incarico distinto; questo report non la autorizza.

Flusso: Attività = singolo runtime diagnostico autorizzato; Script = wrapper
approvato con digest verificato; Commit = documentale; Report = questo
documento; Risultato = `blocked_preflight`, exit 68, zero generazioni;
Decisione = nessun retry e nessuna promozione; Stato = **BLOCCATO**.
