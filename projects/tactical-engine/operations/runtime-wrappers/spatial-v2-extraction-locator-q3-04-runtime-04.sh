ssh football-vps 'bash -s' <<'BASH'
set -Eeuo pipefail
umask 077

readonly EXPECTED_HEAD='13814c20d80bca4d9cb4cb08a288b6e7b31dac0d'
readonly STAGING_PARENT='/home/football/.local/share/football-data-lab/staging'
readonly STAGING="${STAGING_PARENT}/spatial-v2-dual-blocker-13814c2"
readonly PROJECT="${STAGING}/projects/tactical-engine"

readonly ARTIFACT_PARENT='/home/football/.local/share/football-data-lab/runtime-artifacts'
readonly ARTIFACT="${ARTIFACT_PARENT}/spatial-v2-extraction-locator-q3-04-runtime-04"
readonly LOCK_PARENT='/home/football/.local/share/football-data-lab/runtime-locks'
readonly LOCK_FILE="${LOCK_PARENT}/spatial-v2-extraction-locator.lock"

readonly PYTHON='/usr/bin/python3'
readonly OLLAMA_URL='http://127.0.0.1:11434'
readonly MODEL='qwen3.5:9b'
readonly EXPECTED_MODEL_DIGEST='56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90'

readonly INFERENCE_PATH='projects/tactical-engine/scripts/shadow_nli_spatial_relations_v2_inference.py'
readonly EXTRACTION_PATH='projects/tactical-engine/scripts/v5_tactical_semantic_support_s2_spatial_v2_extraction.py'
readonly VALIDATOR_PATH='projects/tactical-engine/scripts/v5_tactical_semantic_support_s2_spatial_v2.py'
readonly DATASET_PATH='projects/tactical-engine/eval/claim_fidelity_gold_v1.json'

readonly INFERENCE_BLOB='8ac93d07341e1079ee3ca6ff98327a8391b7ab5f'
readonly EXTRACTION_BLOB='1a64827b26fb30758773049eedeb342a2bb826b2'
readonly VALIDATOR_BLOB='0a8b92acbda67afeaee4bc057f89729e11e20ab5'
readonly DATASET_BLOB='4523eb746d666fdfb161c5d38d8db31f12e99b92'
readonly DATASET_LINUX_SHA256='8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c'

PHASE='bootstrap'
ATTEMPT_STATUS='not_started'
REASON_CODE='NONE'
GENERATION_STARTED='false'
GENERATION_COMPLETED='false'
TRANSPORT_ATTEMPTED='false'
TRANSPORT_CALLS='0'
RESPONSE_RECEIVED='false'
SUPERVISED_RC='null'
FINAL_RC=1
ARTIFACT_CREATED='false'
FINALIZED='false'

path_must_exist_without_symlink() {
    local checked_path=$1
    local error_code=$2

    test ! -L "$checked_path" ||
        fail 'E_PATH_SYMLINK' "$error_code"
    test -e "$checked_path" ||
        fail 'E_PATH_MISSING' "$error_code"
}

path_must_be_absent_including_dangling_symlink() {
    local checked_path=$1
    local error_code=$2

    test ! -L "$checked_path" ||
        fail 'E_PATH_DANGLING_OR_SYMLINK' "$error_code"
    test ! -e "$checked_path" ||
        fail 'E_PATH_ALREADY_EXISTS' "$error_code"
}

write_progress_state() {
    local temporary="${ARTIFACT}/attempt_progress.json.tmp"

    test "$ARTIFACT_CREATED" = 'true' || return 0
    test ! -L "$ARTIFACT" || return 91
    test -d "$ARTIFACT" || return 92

    printf '%s\n' \
        '{' \
        '  "record_type": "non_final_progress",' \
        '  "finalization_complete": false,' \
        "  \"phase\": \"${PHASE}\"," \
        "  \"attempt_status\": \"${ATTEMPT_STATUS}\"," \
        "  \"reason_code\": \"${REASON_CODE}\"," \
        "  \"generation_started\": ${GENERATION_STARTED}," \
        "  \"generation_completed\": ${GENERATION_COMPLETED}," \
        "  \"transport_attempted\": ${TRANSPORT_ATTEMPTED}," \
        "  \"transport_calls\": ${TRANSPORT_CALLS}," \
        "  \"response_received\": ${RESPONSE_RECEIVED}," \
        "  \"supervised_exit_code\": ${SUPERVISED_RC}," \
        '  "promotion_authorized": false' \
        '}' > "$temporary" || return 93

    mv -- "$temporary" "${ARTIFACT}/attempt_progress.json" || return 94
}

record_finalization_error() {
    local component=$1
    local error_code=$2

    test "$ARTIFACT_CREATED" = 'true' || return 0
    test ! -L "$ARTIFACT" || return 0
    test -d "$ARTIFACT" || return 0

    printf '%s component=%s exit_code=%s\n' \
        "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
        "$component" \
        "$error_code" >> "${ARTIFACT}/finalization_errors.log" 2>/dev/null ||
        true
}

write_payload_hash_inventory() {
    test "$ARTIFACT_CREATED" = 'true' || return 0
    test ! -L "$ARTIFACT" || return 95
    test -d "$ARTIFACT" || return 96

    (
        cd "$ARTIFACT" || exit 97
        find . -maxdepth 1 -type f \
            ! -name 'hashes.sha256' \
            ! -name 'hashes.sha256.digest' \
            ! -name 'attempt_state.json' \
            ! -name 'attempt_state.json.tmp' \
            ! -name 'attempt_state.sha256' \
            ! -name 'attempt_state.sha256.tmp' \
            -printf '%P\0' |
            sort -z |
            xargs -0 -r sha256sum > hashes.sha256 &&
        sha256sum hashes.sha256 > hashes.sha256.digest
    )
}

publish_final_state() {
    local reported_rc=$1
    local inventory_digest
    local state_tmp="${ARTIFACT}/attempt_state.json.tmp"
    local digest_tmp="${ARTIFACT}/attempt_state.sha256.tmp"

    test "$ARTIFACT_CREATED" = 'true' || return 0
    test ! -L "$ARTIFACT" || return 98
    test -d "$ARTIFACT" || return 99

    inventory_digest="$(
        awk '{print $1}' "${ARTIFACT}/hashes.sha256.digest"
    )" || return 100

    test -n "$inventory_digest" || return 101

    printf '%s\n' \
        '{' \
        '  "record_type": "final_attempt_state",' \
        '  "finalization_complete": true,' \
        '  "attempt_id": "spatial-v2-extraction-locator-q3-04-runtime-04",' \
        "  \"phase\": \"${PHASE}\"," \
        "  \"attempt_status\": \"${ATTEMPT_STATUS}\"," \
        "  \"reason_code\": \"${REASON_CODE}\"," \
        "  \"generation_started\": ${GENERATION_STARTED}," \
        "  \"generation_completed\": ${GENERATION_COMPLETED}," \
        "  \"transport_attempted\": ${TRANSPORT_ATTEMPTED}," \
        "  \"transport_calls\": ${TRANSPORT_CALLS}," \
        "  \"response_received\": ${RESPONSE_RECEIVED}," \
        "  \"supervised_exit_code\": ${SUPERVISED_RC}," \
        "  \"wrapper_exit_code\": ${reported_rc}," \
        "  \"payload_inventory_sha256\": \"${inventory_digest}\"," \
        '  "promotion_authorized": false' \
        '}' > "$state_tmp" || return 102

    (
        cd "$ARTIFACT" || exit 103
        sha256sum attempt_state.json.tmp |
            sed 's/attempt_state\.json\.tmp/attempt_state.json/' \
            > attempt_state.sha256.tmp
    ) || return 104

    mv -- "$digest_tmp" "${ARTIFACT}/attempt_state.sha256" ||
        return 105
    mv -- "$state_tmp" "${ARTIFACT}/attempt_state.json" ||
        return 106
}

publish_failed_finalization_state() {
    local original_rc=$1
    local finalization_rc=$2
    local temporary="${ARTIFACT}/attempt_state.failed.tmp"

    test "$ARTIFACT_CREATED" = 'true' || return 0
    test ! -L "$ARTIFACT" || return 0
    test -d "$ARTIFACT" || return 0

    rm -f -- \
        "${ARTIFACT}/attempt_state.json.tmp" \
        "${ARTIFACT}/attempt_state.sha256.tmp" \
        "${ARTIFACT}/attempt_state.sha256" 2>/dev/null || true

    printf '%s\n' \
        '{' \
        '  "record_type": "finalization_failure",' \
        '  "finalization_complete": false,' \
        "  \"original_wrapper_exit_code\": ${original_rc}," \
        "  \"finalization_exit_code\": ${finalization_rc}," \
        '  "promotion_authorized": false' \
        '}' > "$temporary" 2>/dev/null || return 0

    mv -- "$temporary" \
        "${ARTIFACT}/attempt_state.failed.json" 2>/dev/null || true
}

finalize() {
    local incoming_rc=$?
    local result_rc=$FINAL_RC
    local inventory_rc=0
    local state_rc=0
    local finalization_rc=0

    test "$FINALIZED" = 'false' || exit "$incoming_rc"
    FINALIZED='true'

    trap - EXIT ERR INT TERM HUP
    set +e

    if test "$incoming_rc" -ne 0 && test "$result_rc" -eq 0; then
        result_rc=$incoming_rc
    fi

    write_payload_hash_inventory
    inventory_rc=$?

    if test "$inventory_rc" -ne 0; then
        finalization_rc=$inventory_rc
        record_finalization_error \
            'write_payload_hash_inventory' "$inventory_rc"
    else
        publish_final_state "$result_rc"
        state_rc=$?

        if test "$state_rc" -ne 0; then
            finalization_rc=$state_rc
            record_finalization_error \
                'publish_final_state' "$state_rc"
        fi
    fi

    if test "$finalization_rc" -ne 0; then
        publish_failed_finalization_state "$result_rc" "$finalization_rc"

        if test "$result_rc" -eq 0; then
            result_rc=90
        fi
    fi

    exit "$result_rc"
}

on_unhandled_error() {
    local error_code=$1

    if test "$GENERATION_STARTED" = 'true'; then
        ATTEMPT_STATUS='incomplete'
        REASON_CODE='E_UNHANDLED_RUNTIME_ERROR'
    else
        ATTEMPT_STATUS='blocked_preflight'
        REASON_CODE='E_UNHANDLED_PREFLIGHT_ERROR'
    fi

    FINAL_RC=$error_code
}

handle_signal() {
    local signal_name=$1
    local error_code=$2

    if test "$GENERATION_STARTED" = 'true'; then
        ATTEMPT_STATUS='incomplete'
    else
        ATTEMPT_STATUS='blocked_preflight'
    fi

    REASON_CODE="E_SIGNAL_${signal_name}"
    FINAL_RC=$error_code
    exit "$error_code"
}

fail() {
    local reason_code=$1
    local error_code=$2

    REASON_CODE=$reason_code
    FINAL_RC=$error_code

    if test "$GENERATION_STARTED" = 'true'; then
        ATTEMPT_STATUS='incomplete'
    else
        ATTEMPT_STATUS='blocked_preflight'
    fi

    printf 'BLOCKED: %s\n' "$reason_code" >&2
    exit "$error_code"
}

trap finalize EXIT
trap 'on_unhandled_error $?' ERR
trap 'handle_signal INT 130' INT
trap 'handle_signal TERM 143' TERM
trap 'handle_signal HUP 129' HUP

# ----------------------------------------------------------------------
# 1. BOOTSTRAP
# ----------------------------------------------------------------------

for checked_path in \
    '/home' \
    '/home/football' \
    '/home/football/.local' \
    '/home/football/.local/share' \
    '/home/football/.local/share/football-data-lab'
do
    path_must_exist_without_symlink "$checked_path" 40
    test -d "$checked_path" || fail 'E_ANCESTOR_NOT_DIRECTORY' 41
done

if test -L "$ARTIFACT_PARENT"; then
    fail 'E_ARTIFACT_PARENT_SYMLINK' 42
fi
if test ! -e "$ARTIFACT_PARENT"; then
    mkdir -- "$ARTIFACT_PARENT" ||
        fail 'E_ARTIFACT_PARENT_CREATE' 43
fi
test ! -L "$ARTIFACT_PARENT" ||
    fail 'E_ARTIFACT_PARENT_SYMLINK_AFTER_CREATE' 44
test -d "$ARTIFACT_PARENT" ||
    fail 'E_ARTIFACT_PARENT_NOT_DIRECTORY' 45
test -w "$ARTIFACT_PARENT" ||
    fail 'E_ARTIFACT_PARENT_NOT_WRITABLE' 46

if test -L "$LOCK_PARENT"; then
    fail 'E_LOCK_PARENT_SYMLINK' 47
fi
if test ! -e "$LOCK_PARENT"; then
    mkdir -- "$LOCK_PARENT" ||
        fail 'E_LOCK_PARENT_CREATE' 48
fi
test ! -L "$LOCK_PARENT" ||
    fail 'E_LOCK_PARENT_SYMLINK_AFTER_CREATE' 49
test -d "$LOCK_PARENT" ||
    fail 'E_LOCK_PARENT_NOT_DIRECTORY' 50

lock_parent_owner="$(stat -c '%u' "$LOCK_PARENT")" ||
    fail 'E_LOCK_PARENT_STAT' 51
current_uid="$(id -u)" ||
    fail 'E_CURRENT_UID' 52
test "$lock_parent_owner" = "$current_uid" ||
    fail 'E_LOCK_PARENT_OWNER' 53

chmod 700 "$LOCK_PARENT" ||
    fail 'E_LOCK_PARENT_MODE' 54

path_must_be_absent_including_dangling_symlink "$ARTIFACT" 55

mkdir -- "$ARTIFACT" ||
    fail 'E_ARTIFACT_CREATE' 56
ARTIFACT_CREATED='true'
PHASE='preflight'
ATTEMPT_STATUS='preflight_in_progress'
FINAL_RC=56

write_progress_state ||
    fail 'E_INITIAL_PROGRESS_STATE' 57

# ----------------------------------------------------------------------
# 2. LOCK
# ----------------------------------------------------------------------

test ! -L "$LOCK_FILE" ||
    fail 'E_LOCK_FILE_SYMLINK_BEFORE_OPEN' 58

exec 9>>"$LOCK_FILE" ||
    fail 'E_LOCK_FILE_OPEN' 59

test ! -L "$LOCK_FILE" ||
    fail 'E_LOCK_FILE_SYMLINK_AFTER_OPEN' 60

test -f "/proc/$$/fd/9" ||
    fail 'E_LOCK_FD_NOT_REGULAR' 62

lock_fd_identity="$(stat -Lc '%d:%i' "/proc/$$/fd/9")" ||
    fail 'E_LOCK_FD_IDENTITY' 63
lock_path_identity="$(stat -Lc '%d:%i' "$LOCK_FILE")" ||
    fail 'E_LOCK_PATH_IDENTITY' 64
test "$lock_fd_identity" = "$lock_path_identity" ||
    fail 'E_LOCK_PATH_REPLACED' 65

flock -n 9 ||
    fail 'E_CONCURRENT_COMPLIANT_RUNTIME' 66

ps -eo pid=,ppid=,etimes=,comm=,args= \
    > "${ARTIFACT}/process_snapshot_before.txt" ||
    fail 'E_PROCESS_SNAPSHOT' 67

# ----------------------------------------------------------------------
# 3. PREFLIGHT STAGING
# ----------------------------------------------------------------------

for checked_path in \
    "$STAGING_PARENT" \
    "$STAGING" \
    "$PROJECT" \
    "${PROJECT}/scripts" \
    "${PROJECT}/eval"
do
    path_must_exist_without_symlink "$checked_path" 68
    test -d "$checked_path" ||
        fail 'E_STAGING_PATH_NOT_DIRECTORY' 69
done

actual_head="$(git -C "$STAGING" rev-parse HEAD)" ||
    fail 'E_STAGING_HEAD_READ' 70
test "$actual_head" = "$EXPECTED_HEAD" ||
    fail 'E_STAGING_HEAD_MISMATCH' 71

if git -C "$STAGING" symbolic-ref -q HEAD >/dev/null 2>&1; then
    fail 'E_STAGING_NOT_DETACHED' 72
fi

git -C "$STAGING" status --porcelain=v1 --untracked-files=all \
    > "${ARTIFACT}/git_status_before.txt" ||
    fail 'E_STAGING_STATUS_BEFORE' 73

test ! -s "${ARTIFACT}/git_status_before.txt" ||
    fail 'E_STAGING_DIRTY_BEFORE' 74

printf '%s\n' "$actual_head" > "${ARTIFACT}/git_head_before.txt" ||
    fail 'E_HEAD_ARTIFACT_BEFORE' 75

test "$(git -C "$STAGING" rev-parse "HEAD:${INFERENCE_PATH}")" = \
    "$INFERENCE_BLOB" ||
    fail 'E_INFERENCE_BLOB' 76
test "$(git -C "$STAGING" rev-parse "HEAD:${EXTRACTION_PATH}")" = \
    "$EXTRACTION_BLOB" ||
    fail 'E_EXTRACTION_BLOB' 77
test "$(git -C "$STAGING" rev-parse "HEAD:${VALIDATOR_PATH}")" = \
    "$VALIDATOR_BLOB" ||
    fail 'E_VALIDATOR_BLOB' 78
test "$(git -C "$STAGING" rev-parse "HEAD:${DATASET_PATH}")" = \
    "$DATASET_BLOB" ||
    fail 'E_DATASET_BLOB' 79

dataset_file="${STAGING}/${DATASET_PATH}"
path_must_exist_without_symlink "$dataset_file" 80
test -f "$dataset_file" ||
    fail 'E_DATASET_NOT_REGULAR' 81

actual_dataset_sha256="$(sha256sum "$dataset_file" | awk '{print $1}')" ||
    fail 'E_DATASET_SHA_READ' 82
test "$actual_dataset_sha256" = "$DATASET_LINUX_SHA256" ||
    fail 'E_DATASET_SHA_MISMATCH' 83

test -x "$PYTHON" || fail 'E_PYTHON_UNAVAILABLE' 84
command -v curl >/dev/null 2>&1 || fail 'E_CURL_UNAVAILABLE' 85
command -v timeout >/dev/null 2>&1 || fail 'E_TIMEOUT_UNAVAILABLE' 86
command -v flock >/dev/null 2>&1 || fail 'E_FLOCK_UNAVAILABLE' 87
test -x /usr/bin/time || fail 'E_TIME_UNAVAILABLE' 88

# ----------------------------------------------------------------------
# 4. PREFLIGHT OLLAMA — NESSUNA GENERAZIONE
# ----------------------------------------------------------------------

curl --fail --silent --show-error \
    "${OLLAMA_URL}/api/tags" \
    > "${ARTIFACT}/ollama_tags_before.json" ||
    fail 'E_OLLAMA_TAGS_PREFLIGHT' 89

curl --fail --silent --show-error \
    "${OLLAMA_URL}/api/ps" \
    > "${ARTIFACT}/ollama_ps_before.json" ||
    fail 'E_OLLAMA_PS_PREFLIGHT' 90

set +e
"$PYTHON" - "$MODEL" "$EXPECTED_MODEL_DIGEST" \
    "${ARTIFACT}/ollama_tags_before.json" <<'PY'
import json
import pathlib
import sys

model, expected_digest, source = sys.argv[1:]
payload = json.loads(pathlib.Path(source).read_text(encoding="utf-8"))
matches = [
    item for item in payload.get("models", [])
    if item.get("name") == model or item.get("model") == model
]
if len(matches) != 1:
    raise SystemExit("model unavailable or ambiguous")
if matches[0].get("digest") != expected_digest:
    raise SystemExit("model digest mismatch")
PY
model_check_rc=$?
set -e

test "$model_check_rc" -eq 0 ||
    fail 'E_MODEL_IDENTITY' 91

ATTEMPT_STATUS='preflight_passed'
REASON_CODE='NONE'
write_progress_state ||
    fail 'E_PREFLIGHT_PROGRESS_STATE' 92

# ----------------------------------------------------------------------
# 5. SINGOLA GENERAZIONE
# ----------------------------------------------------------------------

PHASE='generation'
ATTEMPT_STATUS='generation_in_progress'
GENERATION_STARTED='true'
GENERATION_COMPLETED='false'
TRANSPORT_ATTEMPTED='false'
TRANSPORT_CALLS='0'
RESPONSE_RECEIVED='false'
SUPERVISED_RC='null'
FINAL_RC=93

write_progress_state ||
    fail 'E_GENERATION_START_STATE' 93

export PYTHONDONTWRITEBYTECODE=1
export PYTHONNOUSERSITE=1
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

set +e
/usr/bin/time -v \
timeout --signal=TERM --kill-after=15s 450s \
"$PYTHON" - "$PROJECT" "$ARTIFACT" \
    > "${ARTIFACT}/stdout.log" \
    2> "${ARTIFACT}/time_stderr.log" <<'PY'
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import time
from datetime import datetime, timezone

project = pathlib.Path(sys.argv[1]).resolve(strict=True)
artifact = pathlib.Path(sys.argv[2]).resolve(strict=True)
scripts = project / "scripts"
dataset_path = project / "eval" / "claim_fidelity_gold_v1.json"

sys.path.insert(0, str(scripts))

import shadow_nli_spatial_relations_v2_inference as judge
import v5_tactical_semantic_support_s2_spatial_v2_extraction as extraction_contract

ATTEMPT_ID = "spatial-v2-extraction-locator-q3-04-runtime-04"
CASE_ID = "q3_04"
MODEL = "qwen3.5:9b"

def write_json(name, value):
    target = artifact / name
    temporary = artifact / f"{name}.tmp"
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(target)

def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()

dataset_bytes = dataset_path.read_bytes()
dataset = json.loads(dataset_bytes.decode("utf-8"))

if not isinstance(dataset, dict) or not isinstance(dataset.get("cases"), list):
    raise SystemExit("dataset structure invalid")

cases = [
    item for item in dataset["cases"]
    if isinstance(item, dict) and item.get("id") == CASE_ID
]
if len(cases) != 1:
    raise SystemExit("q3_04 missing or ambiguous")

case = cases[0]
claim = case["claim"]
evidence = case["evidence"]
gold_label = case["gold"]
prompt = judge.build_extraction_prompt(claim, evidence)

write_json("input.json", {
    "attempt_id": ATTEMPT_ID,
    "case_id": CASE_ID,
    "claim": claim,
    "evidence": evidence,
    "gold_label": gold_label,
    "source": case.get("source"),
    "page": case.get("page"),
    "dataset_path": str(dataset_path),
    "dataset_sha256": sha256_bytes(dataset_bytes),
})

write_json("config.json", {
    "contract_id": extraction_contract.CONTRACT_ID,
    "contract_version": extraction_contract.CONTRACT_VERSION,
    "model": MODEL,
    "temperature": 0,
    "num_ctx": 4096,
    "num_predict": 2048,
    "http_timeout_seconds": 360,
    "external_timeout_seconds": 450,
    "external_kill_after_seconds": 15,
    "extraction_locator": True,
    "single_generation": True,
    "retry": False,
    "repair": False,
    "fallback": False,
    "promotion_authorized": False,
})

(artifact / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")

started_at = datetime.now(timezone.utc).isoformat()
started = time.monotonic()
transport_calls = 0
raw_response = None

# Indicatore indipendente dal valore JSON deserializzato. JSON null
# corrisponde a raw_response=None ma a risposta effettivamente ricevuta.
response_received_flag = False

write_json("transport_state.json", {
    "attempted": False,
    "transport_calls": 0,
    "response_received": False,
    "generation_completed": False,
})

def recording_transport(url, payload, timeout):
    global transport_calls, raw_response, response_received_flag

    transport_calls += 1
    write_json("transport_state.json", {
        "attempted": True,
        "transport_calls": transport_calls,
        "response_received": False,
        "generation_completed": False,
    })

    if transport_calls != 1:
        raise RuntimeError("more than one transport invocation attempted")

    write_json("request_payload.json", {
        "url": url,
        "timeout": timeout,
        "payload": payload,
    })

    raw_response = judge._default_transport(url, payload, timeout)

    # Il ritorno normale dal trasporto dimostra la ricezione della
    # risposta anche quando il JSON deserializzato è null/None.
    response_received_flag = True

    generation_completed = (
        isinstance(raw_response, dict)
        and raw_response.get("done_reason") == "stop"
    )

    write_json("raw_response.json", raw_response)
    write_json("transport_state.json", {
        "attempted": True,
        "transport_calls": transport_calls,
        "response_received": response_received_flag,
        "generation_completed": generation_completed,
    })
    return raw_response

result = judge.judge_pair(
    claim,
    evidence,
    model=MODEL,
    ollama_url="http://127.0.0.1:11434",
    timeout=180,
    max_tokens=2048,
    transport=recording_transport,
    q3_04_timeout_360=True,
    extraction_locator=True,
)

elapsed = time.monotonic() - started

if response_received_flag and isinstance(raw_response, dict):
    message = raw_response.get("message")
    content = message.get("content") if isinstance(message, dict) else None

    if isinstance(content, str) and content:
        try:
            write_json("extraction.json", json.loads(content))
        except json.JSONDecodeError:
            write_json("extraction_parse_failure.json", {
                "status": "invalid_json",
                "raw_content_sha256":
                    sha256_bytes(content.encode("utf-8")),
            })

if result.get("localization") is not None:
    write_json("provenance.json", result["localization"])
if result.get("witness") is not None:
    write_json("witness.json", result["witness"])
if result.get("validation") is not None:
    write_json("validation.json", result["validation"])

write_json("result.json", result)
write_json("generation_record.json", {
    "attempt_id": ATTEMPT_ID,
    "started_at_utc": started_at,
    "finished_at_utc": datetime.now(timezone.utc).isoformat(),
    "elapsed_seconds": elapsed,
    "transport_calls": transport_calls,
    "transport_attempted": transport_calls == 1,
    "response_received": response_received_flag,
    "generation_completed": (
        isinstance(raw_response, dict)
        and raw_response.get("done_reason") == "stop"
    ),
    "evaluation_status": result.get("evaluation_status"),
    "reason_codes": result.get("reason_codes", []),
    "promotion_authorized": result.get("promotion_authorized"),
    "contract": judge.extraction_descriptor(),
})

if transport_calls != 1:
    raise SystemExit("transport call count is not exactly one")
if result.get("promotion_authorized") is not False:
    raise SystemExit("promotion_authorized invariant violated")
PY
SUPERVISED_RC=$?
set -e

printf '%s\n' "$SUPERVISED_RC" \
    > "${ARTIFACT}/supervised_exit_code.txt" ||
    fail 'E_SUPERVISED_EXIT_ARTIFACT' 94

set +e
transport_observation="$("$PYTHON" - "${ARTIFACT}/transport_state.json" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
if not path.is_file():
    print("false 0 false false")
    raise SystemExit(0)

value = json.loads(path.read_text(encoding="utf-8"))
attempted = value.get("attempted") is True
calls = value.get("transport_calls")
response = value.get("response_received") is True
completed = value.get("generation_completed") is True

if type(calls) is not int or calls < 0:
    raise SystemExit("invalid transport call count")

print(
    ("true" if attempted else "false"),
    calls,
    ("true" if response else "false"),
    ("true" if completed else "false"),
)
PY
)"
transport_observation_rc=$?
set -e

test "$transport_observation_rc" -eq 0 ||
    fail 'E_TRANSPORT_OBSERVATION_INVALID' 95

read -r TRANSPORT_ATTEMPTED TRANSPORT_CALLS RESPONSE_RECEIVED \
    GENERATION_COMPLETED <<EOF
$transport_observation
EOF

if test "$SUPERVISED_RC" -ne 0; then
    ATTEMPT_STATUS='incomplete'

    case "$SUPERVISED_RC" in
        124)
            REASON_CODE='E_EXTERNAL_TIMEOUT'
            ;;
        137)
            REASON_CODE='E_EXTERNAL_KILL_AFTER'
            ;;
        129|130|143)
            REASON_CODE='E_INTERRUPTED'
            ;;
        *)
            REASON_CODE='E_GENERATION_PROCESS'
            ;;
    esac

    FINAL_RC=$SUPERVISED_RC
    exit "$FINAL_RC"
fi

# ----------------------------------------------------------------------
# 6. VERIFICA CONDIZIONALE DEI PERCORSI
# ----------------------------------------------------------------------

PHASE='verification'
ATTEMPT_STATUS='verification_in_progress'
FINAL_RC=100

set +e
"$PYTHON" - "$PROJECT" "$ARTIFACT" <<'PY'
from __future__ import annotations

import json
import pathlib
import sys

project = pathlib.Path(sys.argv[1]).resolve(strict=True)
artifact = pathlib.Path(sys.argv[2]).resolve(strict=True)
sys.path.insert(0, str(project / "scripts"))

import v5_tactical_semantic_support_s2_spatial_v2_extraction as extraction_contract

def exists(name):
    return (artifact / name).is_file()

def read_json(name):
    path = artifact / name
    if not path.is_file():
        raise ValueError(f"missing artifact: {name}")
    return json.loads(path.read_text(encoding="utf-8"))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def canonical(value):
    return extraction_contract.canonical_json(value)

def require_diagnostic_provenance(result, claim, evidence):
    require(exists("provenance.json"), "diagnostic provenance missing")
    provenance = read_json("provenance.json")
    require(
        result.get("localization") == provenance,
        "diagnostic provenance differs from result",
    )
    require(
        provenance.get("status") == "not_evaluable",
        "diagnostic provenance status is not fail-closed",
    )

    source_digests = provenance.get("source_text_sha256")
    require(
        isinstance(source_digests, dict),
        "diagnostic source digests missing",
    )
    require(
        source_digests.get("claim") ==
        extraction_contract.digest_text(claim),
        "diagnostic claim digest mismatch",
    )
    require(
        source_digests.get("evidence") ==
        extraction_contract.digest_text(evidence),
        "diagnostic evidence digest mismatch",
    )
    return provenance

def require_boundary_result(result, code, claim, evidence):
    expected = extraction_contract.boundary_failure(
        code,
        claim_text=claim,
        evidence_text=evidence,
    )
    require(
        canonical(result) == canonical(expected),
        f"boundary result mismatch for {code}",
    )
    return require_diagnostic_provenance(
        result, claim, evidence
    )

input_record = read_json("input.json")
config = read_json("config.json")
result = read_json("result.json")
generation_record = read_json("generation_record.json")
transport_state = read_json("transport_state.json")

require(
    config.get("contract_id") == extraction_contract.CONTRACT_ID,
    "unexpected extraction contract id",
)
require(
    config.get("contract_version") == extraction_contract.CONTRACT_VERSION,
    "unexpected extraction contract version",
)
require(
    config.get("promotion_authorized") is False,
    "config promotion invariant violated",
)
require(
    result.get("promotion_authorized") is False,
    "result promotion invariant violated",
)
require(
    generation_record.get("promotion_authorized") is False,
    "generation record promotion invariant violated",
)

claim = input_record.get("claim")
evidence = input_record.get("evidence")
gold_label = input_record.get("gold_label")

require(isinstance(claim, str) and bool(claim), "claim invalid")
require(isinstance(evidence, str) and bool(evidence), "evidence invalid")
require(
    gold_label in {"supported", "contradicted", "insufficient"},
    "Gold label invalid",
)

attempted = transport_state.get("attempted")
calls = transport_state.get("transport_calls")
response_received = transport_state.get("response_received")
generation_completed = transport_state.get("generation_completed")

require(type(attempted) is bool, "transport attempted invalid")
require(type(calls) is int and calls >= 0, "transport call count invalid")
require(type(response_received) is bool, "response received invalid")
require(type(generation_completed) is bool, "generation completed invalid")
require(calls <= 1, "more than one transport call observed")
require(attempted == (calls == 1), "transport attempt/count mismatch")
require(
    generation_completed is False or response_received is True,
    "completed generation without response",
)

require(
    generation_record.get("transport_calls") == calls,
    "generation record transport count mismatch",
)
require(
    generation_record.get("transport_attempted") == attempted,
    "generation record attempted mismatch",
)
require(
    generation_record.get("response_received") == response_received,
    "generation record response mismatch",
)
require(
    generation_record.get("generation_completed") == generation_completed,
    "generation record completion mismatch",
)

evaluation_status = result.get("evaluation_status")
reason_codes = result.get("reason_codes", [])

require(
    evaluation_status in {"evaluated", "not_evaluable"},
    "unknown evaluation status",
)
require(isinstance(reason_codes, list), "reason_codes is not a list")

raw_response = read_json("raw_response.json") if response_received else None
raw_response_is_dict = isinstance(raw_response, dict)
raw_content = None
parsed_extraction = None
json_valid = False

if response_received:
    if raw_response_is_dict:
        message = raw_response.get("message")
        raw_content = (
            message.get("content") if isinstance(message, dict) else None
        )

        if generation_completed:
            require(
                raw_response.get("done_reason") == "stop",
                "completed generation without done_reason stop",
            )
        else:
            require(
                raw_response.get("done_reason") != "stop",
                "incomplete generation unexpectedly reports stop",
            )
    else:
        require(
            generation_completed is False,
            "non-object response marked as completed",
        )

if isinstance(raw_content, str) and raw_content:
    try:
        parsed_extraction = json.loads(raw_content)
        json_valid = True
    except json.JSONDecodeError:
        json_valid = False

extraction_present = exists("extraction.json")
provenance_present = exists("provenance.json")
witness_present = exists("witness.json")
validation_present = exists("validation.json")

localization_status = None
observed_label = None
semantic_match = None
wrapper_exit_code = 80

# ------------------------------------------------------------------
# A. Trasporto senza risposta
# ------------------------------------------------------------------

if attempted and not response_received:
    require(
        evaluation_status == "not_evaluable",
        "transport failure was promoted",
    )
    require(
        len(reason_codes) == 1 and reason_codes[0] in {
            "E_JUDGE_TIMEOUT",
            "E_JUDGE_TRANSPORT",
        },
        "transport failure reason code invalid",
    )
    require(not extraction_present, "transport failure has extraction")
    require(not witness_present, "transport failure has witness")
    require(not validation_present, "transport failure has validation")

    reason = reason_codes[0]
    provenance = require_boundary_result(
        result, reason, claim, evidence
    )
    localization_status = provenance.get("status")
    classification = (
        "fail_closed_timeout"
        if reason == "E_JUDGE_TIMEOUT"
        else "fail_closed_transport"
    )

# ------------------------------------------------------------------
# B. Risposta ricevuta ma generazione incompleta.
#    Include JSON null e qualsiasi altro valore JSON non-object.
# ------------------------------------------------------------------

elif response_received and not generation_completed:
    require(
        evaluation_status == "not_evaluable",
        "incomplete response was promoted",
    )
    require(
        reason_codes == ["E_JUDGE_RESPONSE_INCOMPLETE"],
        "incomplete response reason code invalid",
    )
    require(not extraction_present, "incomplete response has extraction")
    require(not witness_present, "incomplete response has witness")
    require(not validation_present, "incomplete response has validation")

    provenance = require_boundary_result(
        result,
        "E_JUDGE_RESPONSE_INCOMPLETE",
        claim,
        evidence,
    )
    localization_status = provenance.get("status")
    classification = "fail_closed_response_incomplete"

# ------------------------------------------------------------------
# C. Generazione completata ma contenuto assente/vuoto
# ------------------------------------------------------------------

elif generation_completed and (
    not isinstance(raw_content, str) or not raw_content
):
    require(
        evaluation_status == "not_evaluable",
        "missing response content was promoted",
    )
    require(
        reason_codes == ["E_JUDGE_RESPONSE_MISSING"],
        "missing response reason code invalid",
    )
    require(not extraction_present, "missing content has extraction")
    require(not witness_present, "missing content has witness")
    require(not validation_present, "missing content has validation")

    provenance = require_boundary_result(
        result,
        "E_JUDGE_RESPONSE_MISSING",
        claim,
        evidence,
    )
    localization_status = provenance.get("status")
    classification = "fail_closed_response_missing"

# ------------------------------------------------------------------
# D. Generazione completata, JSON malformato
# ------------------------------------------------------------------

elif generation_completed and not json_valid:
    require(
        evaluation_status == "not_evaluable",
        "invalid JSON was promoted",
    )
    require(
        reason_codes == ["E_JUDGE_JSON_INVALID"],
        "invalid JSON reason code invalid",
    )
    require(not extraction_present, "malformed JSON has extraction")
    require(not witness_present, "malformed JSON has witness")
    require(not validation_present, "malformed JSON has validation")
    require(
        exists("extraction_parse_failure.json"),
        "JSON failure diagnostic missing",
    )

    provenance = require_boundary_result(
        result,
        "E_JUDGE_JSON_INVALID",
        claim,
        evidence,
    )
    localization_status = provenance.get("status")
    classification = "fail_closed_json_invalid"

# ------------------------------------------------------------------
# E. JSON valida: extraction presente
# ------------------------------------------------------------------

elif generation_completed and json_valid:
    require(extraction_present, "valid JSON lacks extraction")
    extraction = read_json("extraction.json")

    require(
        canonical(parsed_extraction) == canonical(extraction),
        "extraction differs from raw response",
    )

    shape_errors = extraction_contract.extraction_shape_errors(
        extraction
    )

    # --------------------------------------------------------------
    # E1. Extraction JSON valida ma schema invalido
    # --------------------------------------------------------------

    if shape_errors:
        require(
            evaluation_status == "not_evaluable",
            "schema-invalid extraction was promoted",
        )
        require(
            reason_codes == ["E_EXTRACTION_SCHEMA_INVALID"],
            "schema-invalid extraction reason code invalid",
        )
        require(not witness_present, "schema-invalid extraction has witness")
        require(
            not validation_present,
            "schema-invalid extraction has validation",
        )
        require(
            provenance_present,
            "schema-invalid extraction lacks provenance",
        )

        reconstruction_errors = (
            extraction_contract.verify_materialization(
                result, extraction, claim, evidence
            )
        )
        require(
            not reconstruction_errors,
            "schema-invalid materialization mismatch: " +
            json.dumps(
                reconstruction_errors,
                ensure_ascii=False,
                sort_keys=True,
            ),
        )

        provenance = read_json("provenance.json")
        require(
            result.get("localization") == provenance,
            "schema-invalid provenance differs from result",
        )
        require(
            provenance.get("status") == "not_evaluable",
            "schema-invalid provenance status is not fail-closed",
        )
        require(
            result.get("details") == shape_errors,
            "schema diagnostics differ from shape errors",
        )

        localization_status = provenance.get("status")
        classification = "fail_closed_extraction_schema"

    # --------------------------------------------------------------
    # E1b. Shape valido, precontrollo semantico fallito prima del locator
    # --------------------------------------------------------------

    elif (semantic_errors := extraction_contract.extraction_semantic_errors(
        extraction
    )):
        require(
            evaluation_status == "not_evaluable",
            "semantic-invalid extraction was promoted",
        )
        require(
            reason_codes == ["E_EXTRACTION_SEMANTIC_INCONSISTENT"],
            "semantic-invalid extraction reason code invalid",
        )
        require(
            result.get("details") == semantic_errors,
            "semantic diagnostics differ from precheck errors",
        )
        require(result.get("witness") is None, "semantic failure has witness")
        require(result.get("validation") is None, "semantic failure has validation")
        require(not witness_present, "semantic failure has witness artifact")
        require(not validation_present, "semantic failure has validation artifact")
        provenance = require_diagnostic_provenance(result, claim, evidence)
        require(
            provenance.get("records") == [],
            "semantic failure unexpectedly has localization records",
        )
        require(
            not extraction_contract.verify_materialization(
                result, extraction, claim, evidence
            ),
            "semantic failure materialization/provenance mismatch",
        )
        require(
            observed_label is None and semantic_match is None,
            "semantic failure has observed label or semantic match",
        )
        localization_status = provenance.get("status")
        classification = "fail_closed_extraction_semantic"

    # --------------------------------------------------------------
    # E2. Shape e precontrollo semantico validi
    # --------------------------------------------------------------

    else:
        require(provenance_present, "valid extraction lacks provenance")
        provenance = read_json("provenance.json")

        reconstruction_errors = (
            extraction_contract.verify_materialization(
                result, extraction, claim, evidence
            )
        )
        require(
            not reconstruction_errors,
            "materialization/provenance mismatch: " +
            json.dumps(
                reconstruction_errors,
                ensure_ascii=False,
                sort_keys=True,
            ),
        )
        require(
            result.get("localization") == provenance,
            "provenance differs from result",
        )

        witness = result.get("witness")
        validation = result.get("validation")
        localization_status = provenance.get("status")

        # ----------------------------------------------------------
        # E2a. Localizzazione fallita
        # ----------------------------------------------------------

        if localization_status == "not_evaluable":
            require(
                evaluation_status == "not_evaluable",
                "localization failure was promoted",
            )
            require(
                reason_codes ==
                ["E_EXTRACTION_LOCALIZATION_NOT_UNIQUE"],
                "localization reason code invalid",
            )
            require(witness is None, "localization failure has witness")
            require(
                validation is None,
                "localization failure has validation",
            )
            require(
                not witness_present,
                "localization failure has witness artifact",
            )
            require(
                not validation_present,
                "localization failure has validation artifact",
            )

            classification = "fail_closed_localization"

        # ----------------------------------------------------------
        # E2b. Witness materializzato, validazione fallita
        # ----------------------------------------------------------

        elif (
            isinstance(witness, dict)
            and isinstance(validation, dict)
            and validation.get("technical_status") != "valid"
        ):
            require(
                evaluation_status == "not_evaluable",
                "invalid witness was promoted",
            )
            require(witness_present, "witness artifact missing")
            require(validation_present, "validation artifact missing")
            require(
                read_json("witness.json") == witness,
                "witness artifact differs from result",
            )
            require(
                read_json("validation.json") == validation,
                "validation artifact differs from result",
            )
            require(
                reason_codes ==
                list(validation.get("error_codes", [])),
                "validation reason codes were not preserved",
            )
            require(reason_codes, "invalid witness lacks reason codes")

            observed_label = witness.get("label")
            classification = "fail_closed_validation"

        # ----------------------------------------------------------
        # E2c. Witness valido
        # ----------------------------------------------------------

        else:
            require(
                evaluation_status == "evaluated",
                "valid witness is not evaluated",
            )
            require(
                localization_status == "materialized",
                "evaluated witness lacks materialized provenance",
            )
            require(
                isinstance(witness, dict),
                "evaluated witness missing",
            )
            require(
                isinstance(validation, dict),
                "evaluated validation missing",
            )
            require(
                validation.get("technical_status") == "valid",
                "evaluated witness is not structurally valid",
            )
            require(witness_present, "witness artifact missing")
            require(validation_present, "validation artifact missing")
            require(
                read_json("witness.json") == witness,
                "witness artifact differs from result",
            )
            require(
                read_json("validation.json") == validation,
                "validation artifact differs from result",
            )
            require(
                reason_codes in ([], None),
                "evaluated result contains failure reasons",
            )

            observed_label = witness.get("label")
            require(
                observed_label in {
                    "supported", "contradicted", "insufficient"
                },
                "witness label invalid",
            )

            semantic_match = observed_label == gold_label
            classification = (
                "completed_evaluated_semantic_match"
                if semantic_match
                else "completed_evaluated_semantic_mismatch"
            )
            wrapper_exit_code = 0 if semantic_match else 81

else:
    raise ValueError("unclassified transport/response path")

decision = {
    "transport_attempted": attempted,
    "transport_calls": calls,
    "response_received": response_received,
    "raw_response_type": type(raw_response).__name__
        if response_received else None,
    "generation_completed": generation_completed,
    "json_valid": json_valid,
    "extraction_present": extraction_present,
    "provenance_present": provenance_present,
    "witness_present": witness_present,
    "validation_present": validation_present,
    "localization_status": localization_status,
    "evaluation_status": evaluation_status,
    "reason_codes": reason_codes,
    "gold_label": gold_label,
    "observed_label": observed_label,
    "semantic_match": semantic_match,
    "classification": classification,
    "promotion_authorized": False,
    "wrapper_exit_code": wrapper_exit_code,
}

temporary = artifact / "decision.json.tmp"
temporary.write_text(
    json.dumps(
        decision,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    ) + "\n",
    encoding="utf-8",
)
temporary.replace(artifact / "decision.json")
PY
verification_rc=$?
set -e

if test "$verification_rc" -ne 0; then
    ATTEMPT_STATUS='incomplete'
    REASON_CODE='E_CONTENT_VERIFICATION'
    FINAL_RC=100
    exit "$FINAL_RC"
fi

set +e
decision_values="$("$PYTHON" - "${ARTIFACT}/decision.json" <<'PY'
import json
import pathlib
import sys

value = json.loads(
    pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
)

code = value.get("wrapper_exit_code")
classification = value.get("classification")
reason_codes = value.get("reason_codes")

if type(code) is not int:
    raise SystemExit("decision exit code invalid")
if not isinstance(classification, str) or not classification:
    raise SystemExit("decision classification invalid")
if not isinstance(reason_codes, list):
    raise SystemExit("decision reason codes invalid")

print(code)
print(classification)
print(",".join(reason_codes) if reason_codes else "NONE")
PY
)"
decision_read_rc=$?
set -e

test "$decision_read_rc" -eq 0 ||
    fail 'E_DECISION_READ' 101

FINAL_RC="$(printf '%s\n' "$decision_values" | sed -n '1p')"
decision_classification="$(
    printf '%s\n' "$decision_values" | sed -n '2p'
)"
decision_reasons="$(
    printf '%s\n' "$decision_values" | sed -n '3p'
)"

case "$FINAL_RC" in
    0)
        ATTEMPT_STATUS='completed_diagnostic'
        REASON_CODE='EVALUATED_SEMANTIC_MATCH'
        ;;
    80)
        ATTEMPT_STATUS='completed_fail_closed'
        REASON_CODE="$decision_reasons"
        ;;
    81)
        ATTEMPT_STATUS='completed_semantic_mismatch'
        REASON_CODE='EVALUATED_SEMANTIC_MISMATCH'
        ;;
    *)
        ATTEMPT_STATUS='incomplete'
        REASON_CODE='E_DECISION_UNCLASSIFIED'
        FINAL_RC=102
        ;;
esac

# ----------------------------------------------------------------------
# 7. VERIFICA DI NON MODIFICA DELLO STAGING
# ----------------------------------------------------------------------

git -C "$STAGING" rev-parse HEAD \
    > "${ARTIFACT}/git_head_after.txt" ||
    fail 'E_STAGING_HEAD_AFTER' 103

git -C "$STAGING" status --porcelain=v1 --untracked-files=all \
    > "${ARTIFACT}/git_status_after.txt" ||
    fail 'E_STAGING_STATUS_AFTER' 104

test "$(cat "${ARTIFACT}/git_head_after.txt")" = "$EXPECTED_HEAD" ||
    fail 'E_STAGING_HEAD_CHANGED' 105

test ! -s "${ARTIFACT}/git_status_after.txt" ||
    fail 'E_STAGING_DIRTY_AFTER' 106

curl --fail --silent --show-error \
    "${OLLAMA_URL}/api/ps" \
    > "${ARTIFACT}/ollama_ps_after.json" ||
    printf '%s\n' '{"snapshot_status":"unavailable"}' \
        > "${ARTIFACT}/ollama_ps_after.json"

PHASE='complete'
exit "$FINAL_RC"
BASH
