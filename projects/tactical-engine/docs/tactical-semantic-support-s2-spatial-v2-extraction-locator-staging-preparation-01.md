# RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-STAGING-PREPARATION-01

## Attività e riconciliazione

Preparazione controllata dello staging Git indipendente richiesto dal percorso
Extraction Locator Spatial V2.

- data: 2026-11-09;
- branch: `codex/tactical-state-contract-v1`;
- HEAD GitHub iniziale: `84c4261a0b88a8a56a8bc6dab3ff0824714381e0`;
- baseline applicativa: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- repository sorgente:
  `C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\codex-perf-worktree`;
- working tree sorgente iniziale: pulito;
- baseline presente e antenata dell'HEAD documentale: confermato.

TODO, Experiment Register e report `runtime-01`/`runtime-02` sono stati
riconciliati prima delle scritture. La preparazione non risultava già
completata; target e bundle remoto erano assenti, inclusi symlink.

## Bundle locale

Bundle autosufficiente creato dalla sola storia Git committata del branch:

- percorso:
  `C:\Users\Giampiero\Documents\FOOTBALL-DATA-LAB\spatial-v2-extraction-locator-db3ad66-84c4261.bundle`;
- dimensione: `2345406` byte;
- SHA-256:
  `d595c23a5c67b46d0329e038cc7f55376b654c7b686cab0e1ad339c201a60f08`;
- ref: `refs/heads/codex/tactical-state-contract-v1` a
  `84c4261a0b88a8a56a8bc6dab3ff0824714381e0`;
- `git bundle verify`: PASS;
- storia completa e nessun prerequisito Git esterno: confermato;
- baseline richiesta inclusa per ancestralità verificata.

Il bundle non include modifiche non committate e si trova fuori dal worktree
Git operativo.

## Trasferimento e verifica VPS

Connessione usata esclusivamente tramite alias `football-vps` come utente
`football`.

- parent staging:
  `/home/football/.local/share/football-data-lab/staging`;
- parent: directory reale, mode `700`, proprietario/gruppo `football`;
- bundle remoto:
  `/home/football/.local/share/football-data-lab/staging/spatial-v2-extraction-locator-db3ad66-84c4261.bundle`;
- dimensione remota: `2345406` byte;
- SHA-256 remoto:
  `d595c23a5c67b46d0329e038cc7f55376b654c7b686cab0e1ad339c201a60f08`;
- identità locale/remota: PASS;
- `git bundle verify` sulla VPS: PASS;
- ref remoto e storia completa: conformi;
- bundle conservato per la revisione, senza pulizia automatica.

La verifica VPS ha attestato esplicitamente l'autonomia del bundle, non soltanto
quella nel repository sorgente.

## Clone indipendente e integrità

Clone creato dal bundle, senza `git worktree`:

`/home/football/.local/share/football-data-lab/staging/spatial-v2-extraction-locator-db3ad66`

Verifiche:

- HEAD: `db3ad66f6254f43bcc625b605b68f2f181c1af69`;
- modalità: detached HEAD;
- index e working tree: puliti;
- SHA-256 dello status vuoto:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- common directory:
  `/home/football/.local/share/football-data-lab/staging/spatial-v2-extraction-locator-db3ad66/.git`, interna al clone;
- `objects/info/alternates`: assente;
- `git fsck --full`: PASS;
- origin: percorso del bundle remoto, non GitHub e non checkout operativo;
- directory target: reale, mode `775`, proprietario/gruppo `football`;
- file richiesti: regolari, non symlink, mode `664`, proprietario/gruppo
  `football`.

Blob Git verificati:

| Componente | Blob atteso e osservato |
|---|---|
| inference | `df9a7fb494956902e8af91860cab176c768992a2` |
| extraction | `97a666672c3a38897ff9570b03a4a749d32d0ead` |
| validator | `0a8b92acbda67afeaee4bc057f89729e11e20ab5` |
| dataset | `4523eb746d666fdfb161c5d38d8db31f12e99b92` |

SHA-256 Linux del dataset:
`8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c` — PASS.

## Isolamento e invarianza

Le fotografie Git prima e dopo coincidono per HEAD, branch/detached state,
SHA-256 dello status e common directory per:

- checkout operativo `/opt/football-data-lab`;
- `s2-first-controlled-b1946f8`;
- `s2-spatial-differential-0d40719`;
- `spatial-v2-q3-04-009f76e`;
- `spatial-v2-q3-04-360-69ec127`;
- `spatial-v2-q3-04-prompt-runtime-41d50fa`;
- `tsc-v1-3fa3a18`;
- `tsc-v2-965d6b6`.

Nessuno staging precedente è stato usato, corretto o alterato. Nessun servizio,
collection, configurazione, checkout operativo o codice applicativo è stato
modificato.

## Risultato, decisione e stato

Non sono stati eseguiti test applicativi, Ollama, Qwen, inferenze o runtime.
Non è stato materializzato né autorizzato `runtime-03`.

| Componente | Stato |
|---|---|
| Bundle autosufficiente | **VALIDATO** |
| Trasferimento e identità locale/remota | **VALIDATO** |
| Clone staging | **IMPLEMENTATO** |
| Verifiche Git, blob e filesystem | **ESEGUITO** |
| Isolamento e integrità dello staging | **VALIDATO** |
| Runtime Extraction Locator | **BLOCCATO** |
| Gate, integrazione e certificazione | **BLOCCATO** |

Decisione: staging pronto esclusivamente come prerequisito tecnico. La sua
validazione non autorizza alcuna generazione o ulteriore tentativo.

Flusso: Attività = preparazione staging Extraction Locator; Script = comandi Git
e shell inline non persistiti; Commit = documentale; Report = questo documento;
Risultato = clone indipendente e integro alla baseline richiesta; Decisione =
staging validato, runtime non autorizzato; Stato = **VALIDATO** per il solo
staging, runtime **BLOCCATO**.
