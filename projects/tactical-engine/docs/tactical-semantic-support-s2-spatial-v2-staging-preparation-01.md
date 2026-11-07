# RD-TSC-V2-D3-S2-SPATIAL-V2-STAGING-PREPARATION-01

## Attività e baseline

Preparazione dello staging Git indipendente per la futura diagnosi controllata
Spatial V2 del caso `q3_04`. Baseline runtime congelata:
`009f76e71c0351da9d2b797ad3c9ff1928671a4e`. Il commit documentale iniziale
era `ab8feec876d2cda1e14adbea246bdc6450ac4032`.

Il confronto Git tra i due commit mostra esclusivamente modifiche a TODO,
experiment register e report del preflight; nessuna differenza tecnica è stata
promossa nella baseline runtime.

## Metodo di acquisizione e isolamento

Parent staging già autorizzato:
`/home/football/.local/share/football-data-lab/staging`.

Clone finale:
`/home/football/.local/share/football-data-lab/staging/spatial-v2-q3-04-009f76e`.

Prima della creazione il target risultava assente, inclusi symlink. Nessun
repository già presente nel perimetro VPS conteneva il commit richiesto. Il
repository GitHub era raggiungibile in sola lettura via HTTPS e il branch remoto
puntava ad `ab8feec`; è stato quindi creato un clone autonomo `--no-checkout` e
successivamente un checkout detached del commit esatto. Non è stato usato
`git worktree` e non sono stati modificati checkout operativo o staging storici.

## Verifiche Git

- HEAD: `009f76e71c0351da9d2b797ad3c9ff1928671a4e`;
- detached HEAD: confermato;
- working tree: pulito prima e dopo i controlli;
- Git directory e common directory: entrambe interne al clone;
- `git fsck --full --no-dangling`: PASS;
- dipendenza dal checkout operativo: assente.

Il checkout operativo è rimasto a `1a80fe0c6261b10f748a36c2b4fd96e8e2253971`.
Gli staging preesistenti hanno conservato i rispettivi HEAD osservati:
`f2a77de`, `0d40719`, `3fa3a18` e `965d6b6`. Sono stati soltanto letti.

## Integrità del codice e del caso canonico

Presenti come file regolari:

- `scripts/v5_tactical_semantic_support_s2_spatial_v2.py`;
- `scripts/shadow_nli_spatial_relations_v2_inference.py`;
- `tests/test_v5_tactical_semantic_support_s2_spatial_v2.py`;
- `eval/claim_fidelity_gold_v1.json`;
- closeout R1/R2 della baseline.

Il dataset contiene una sola occorrenza di `q3_04` in `cases[3]`, fonte
`verticalizzazione_Bonacini`, pagina 2. Sul filesystem Linux il file contiene
139 LF e zero CRLF; SHA-256 byte-level
`8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c`.
Il blob Git e il file materializzato hanno entrambi object ID
`4523eb746d666fdfb161c5d38d8db31f12e99b92`. Il precedente digest Windows
`fdd6d938...` appartiene alla materializzazione CRLF già documentata e non è
stato usato per alterare dataset, fixture o runner.

## Controlli runtime non generativi

- Python disponibile: `/usr/bin/python3`, versione 3.12.3;
- dipendenze effettive del percorso importato: `json` e `urllib.request`
  disponibili;
- import del contratto e del judge: PASS con bytecode disabilitato;
- contratto: `nli_spatial_relations_v2` versione `2.0.0`;
- schema disponibile e di tipo `object`;
- endpoint non generativo Ollama `/api/tags`: disponibile;
- modello: `qwen3.5:9b`;
- digest modello:
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
- `/api/ps`: zero modelli caricati;
- snapshot processi: solo `/usr/local/bin/ollama serve`, nessun Gate o processo
  Spatial V2 concorrente osservato;
- filesystem: 39 GiB disponibili; memoria disponibile: circa 14 GiB.

L'assenza di concorrenza nello snapshot non garantisce una futura finestra
esclusiva. Non sono stati chiamati endpoint generativi, runner o test.

## Risultato, decisione e stati

Numero di chiamate/generazioni: **0**. Nessun servizio, modello, collection,
database, checkout operativo o staging storico è stato modificato.

| Componente | Stato |
|---|---|
| Clone staging Spatial V2 | **IMPLEMENTATO** |
| Verifiche Git e ambientali | **ESEGUITO** |
| Isolamento e integrità Git | **VALIDATO** |
| Diagnosi runtime `q3_04` | **BLOCCATO** |
| Efficacia semantica | **BLOCCATO** |
| Gate, integrazione S2 e certificazione | **BLOCCATO** |

Decisione: staging pronto per una futura richiesta distinta. La preparazione non
autorizza inferenze, Gate, benchmark o correzioni semantiche.
