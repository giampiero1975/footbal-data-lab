# TSC V2 — preflight del primo Gate runtime controllato

## Identità

- Attività: `RD-TSC-V2-RUNTIME-GATE-PREFLIGHT-01`
- Branch: `codex/tactical-state-contract-v1`
- Baseline: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`
- Implementazione: `307064c2a2a2da0dd32cdedde0a136709f79560a`
- Remediation: `8a16a731caf7689e4b1dba3cdb9597d43b36d458`

La ricognizione è esclusivamente statica. Nessuna risorsa runtime è stata
inizializzata e nessuna query Chroma, API o inferenza è stata eseguita.

## Differenza rispetto al Gate FIGC5 V1

Il candidato V2 verifica proprietà non presenti nel Gate FIGC5: proiezione dei
`relation_requirements`, materializzazione deterministica
`state:phase:negative_transition`, trasporto `operational_relations`, copertura V2 e
blocchi canonici. Non ripete domanda, diagnostica o schema del Gate precedente.

## Percorso statico verificato

- `--tactical-state-contract-v2` è opt-in e assente da `DEFAULT_PROFILE_FLAGS`.
- Il wrapper lo rende mutuamente esclusivo con il flag V1 prima di
  `locked.select_runtime()`; il runner lo rende mutuamente esclusivo con V1 e
  `--tactical-plan` prima di aprire Chroma.
- `--legacy-profile` evita l'attivazione implicita del profilo pubblico, ma non
  disattiva il flag V2 esplicito.
- Il question plan è prodotto una volta dal planner V1; il preflight V2 precede il
  trasporto e può fermare l'esecuzione con zero chiamate.
- Il solo trasporto è `_ollama_chat_once()`; non esistono retry o repair.
- Raw output, envelope, controlli e motivazioni restano nella diagnostica. Solo
  `overall_status=validated` promuove `answer` e soddisfa il wrapper.
- Default runner: timeout interno 900 s, modello `qwen3.5:9b`, context 8192.
- Il comando esplicita output massimo 4096 token e `keep_alive=0`.
- Chroma usa il percorso operativo assoluto
  `/opt/football-data-lab/knowledge/rag/chroma` tramite `PersistentClient`.

## Candidato diagnostico

`Alla perdita l'ala deve coprire il lato debole per evitare la ripartenza?`

Il planner già usato dalle fixture offline classifica una relazione esplicita e
rappresentabile: attore `ala`, compito `coprire`, spazio `lato debole`, trigger
`alla perdita`, finalità `evitare la ripartenza`, fase canonica
`negative_transition`. Non richiede posizione tipizzata, evento o attore inventato;
non appartiene ai Gold E/V e non coincide col caso FIGC5.

## Comando candidato non eseguito

`TSC_V2_GATE_ROOT` deve indicare un checkout isolato già creato e verificato alla
baseline esatta. Il comando si arresta prima delle redirezioni o dell'inferenza se
la variabile, il checkout, `evaluation/` o uno degli artefatti non sono conformi.

```bash
set -euo pipefail

: "${TSC_V2_GATE_ROOT:?checkout isolato TSC V2 non definito}"
readonly expected_head='965d6b60b84d56c86fdc64c9c82583bfd2b1da2f'
readonly engine_dir="${TSC_V2_GATE_ROOT}/projects/tactical-engine"
readonly evaluation_dir="${engine_dir}/evaluation"
readonly report="${evaluation_dir}/tactical_state_contract_v2_runtime_gate_01.json"
readonly stdout_log="${evaluation_dir}/tactical_state_contract_v2_runtime_gate_01.stdout.log"
readonly stderr_log="${evaluation_dir}/tactical_state_contract_v2_runtime_gate_01.time_stderr.log"
readonly exit_file="${evaluation_dir}/tactical_state_contract_v2_runtime_gate_01.exit_code.txt"

test -d "${TSC_V2_GATE_ROOT}" && test ! -L "${TSC_V2_GATE_ROOT}" || exit 51
test -d "${engine_dir}" && test ! -L "${engine_dir}" || exit 51
test -d "${evaluation_dir}" && test ! -L "${evaluation_dir}" && test -w "${evaluation_dir}" || exit 51
test "$(git -C "${TSC_V2_GATE_ROOT}" rev-parse HEAD)" = "${expected_head}" || exit 53
test -z "$(git -C "${TSC_V2_GATE_ROOT}" status --porcelain=v1)" || exit 53
for gate_artifact in "${report}" "${stdout_log}" "${stderr_log}" "${exit_file}"; do
  test ! -e "${gate_artifact}" && test ! -L "${gate_artifact}" || exit 52
done

cd -- "${engine_dir}"
set +e
/usr/bin/time -v timeout --signal=TERM --kill-after=30s 960s \
  /opt/football-data-lab/projects/tactical-engine/.venv/bin/python \
  scripts/run_rag_v5_query.py \
  --question "Alla perdita l'ala deve coprire il lato debole per evitare la ripartenza?" \
  --request-id tscv2gate01 \
  --output "${report}" \
  --legacy-profile \
  --tactical-state-contract-v2 \
  --collection dribbling_tactics_v5_multisource_drive11_figc5_candidate_v1 \
  --expected-count 6410 \
  --evidence-limit 8 \
  --model qwen3.5:9b \
  --context-window 8192 \
  --max-output-tokens 4096 \
  --keep-alive 0 \
  >"${stdout_log}" 2>"${stderr_log}"
gate_rc=$?
set -e
printf '%s\n' "${gate_rc}" >"${exit_file}"
exit "${gate_rc}"
```

Il timeout interno rimane il default 900 s del runner; quello esterno è 960 s con
`--kill-after=30s`. `/usr/bin/time -v` misura il client, non il daemon Ollama.

## Matrice esiti

- **PASS tecnico**: un solo processo/generazione, quattro artefatti completi,
  trasporto parsabile, raw e diagnostica conservati, zero repair.
- **PASS completo**: PASS tecnico e `overall_status=validated`, controlli V1/V2,
  domanda-piano, copertura operativa, blocchi canonici e audit tutti positivi.
- **Fail-closed**: `blocked` o `not_evaluable`, `answer` vuoto, artefatti e motivi
  disponibili; non è successo generativo né integrazione.
- **FAIL operativo**: timeout/processo, inizializzazione, collection/count,
  artefatti o attribuzione non verificabili.

## Prerequisiti e rischi residui

1. Non è attestato un checkout runtime isolato alla baseline `965d6b6`; il precedente
   staging noto apparteneva a una baseline più vecchia.
2. La collection candidata e il conteggio 6410 derivano dalle evidenze del Gate
   precedente, non da una verifica live corrente. Il comando apre Chroma operativo:
   serve autorizzazione separata e conferma metadata-only immediatamente precedente.
3. Devono essere confermati interprete/virtualenv, modelli e compatibilità dello
   schema `format` nella finestra runtime.
4. Queue vuota non garantisce esclusività futura; occorre una finestra senza client
   concorrenti osservata immediatamente prima del Gate.
5. Non sono osservabili dal solo client il conteggio server-side delle richieste,
   picco RAM/CPU del daemon e rilascio effettivo del modello.
6. Le redirezioni producono quattro file nello staging; il runner non modifica
   volontariamente il repository, ma Chroma/Ollama possono avere effetti ausiliari
   propri del runtime.

## Decisione

La progettazione statica è conclusa, ma il Gate non è ancora autorizzabile: percorso
del checkout isolato alla baseline corrente e stato live della collection non sono
attestati. Stato: **BLOCCATO**. Occorre una successiva autorizzazione limitata alla
predisposizione/verifica dello staging e ai metadati runtime, prima di qualunque
inferenza.
