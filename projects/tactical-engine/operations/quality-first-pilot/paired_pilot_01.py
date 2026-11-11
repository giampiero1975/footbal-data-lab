"""Prepare/check the existing six-call pilot. Execute requires separate approval.

No application imports. No SSH/network activity at import, prepare or check.
The remote evidence binding is deliberately unresolved in the prepared package.
Reuse: fsync-before-GO and exclusive existing-lock pattern from
operations/official_api_single_case_01.py; historical driver is not imported.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import secrets
import shlex
import subprocess
import threading
import time

ACTIVITY = "RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01"
BASE = "227a862dedf5f36c947ec63dface69c723af1e99"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PROJECT = ROOT / "projects/tactical-engine"
PACKAGE = HERE / "prepared"
# One activity-wide location, not a CLI-selectable output for a second attempt.
LEDGER = PROJECT / "evaluation/quality_first_paired_pilot_01"
CASES = (
    ("V10-02", "evaluation/coverciano-remediation-v10/case_02.json",
     "3e087f98795d69a3435e0a180b036c2494dcf4c6a05d788ad7d2cda445613135"),
    ("V10-03", "evaluation/coverciano-remediation-v10/case_03.json",
     "f422d7e6e4a27044f45d96fc545c4f8ff48b9e20b533aad16547ee90ce693fa8"),
    ("V10.2-10", "evaluation/coverciano-remediation-v10-2/case_10.json",
     "afb2a6c27d3ff46001d7a1b360501287858a3f583b57c947fd8250d34e6d59f9"),
)
SYSTEM = (
    "Rispondi in italiano tecnico alla domanda tattica, entro 350 parole. "
    "Mantieni distinti ruoli, lati, posizioni e fasi; motiva condizioni e sequenze. "
    "Usa le fonti fornite e cita [F1] ecc. solo quando sostengono l'affermazione. "
    "Dichiara le insufficienze delle fonti e distingui le tue inferenze tattiche "
    "dai contenuti documentati. Non inventare supporto o informazioni mancanti."
)
MODELS = {
    "gemma": {"tag": "gemma4:26b", "native_profile": "thinking-enabled",
              "catalog_llamacpp_digest_prefix": "001e5dafc3c7",
              "upstream": "google/gemma-4-26B-A4B-it",
              "revision": "4d7ae4984b7db7de8f8457170b3f1a419ee76d52", "top_k": 64},
    "qwen": {"tag": "qwen3.8:27b", "native_profile": "xhigh",
             "catalog_llamacpp_digest_prefix": "aaee06c39dcf",
             "upstream": "Qwen/Qwen3.8-27B",
             "revision": "37561816e66b5b9153b1b64c10968c18c1e6f4a0", "top_k": 20},
}


def encoded(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_new(path, data):
    """Exclusive durable file; no overwrite/resume/reset operation."""
    with Path(path).open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def save(path, obj):
    write_new(path, encoded(obj) + b"\n")


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def load_inputs():
    inputs = []
    for key, relative, expected in CASES:
        raw = (PROJECT / relative).read_bytes()
        if sha(raw) != expected:
            raise ValueError("E_CASE_IDENTITY: " + key)
        original = json.loads(raw)["questions"]
        if len(original) != 1:
            raise ValueError("E_CASE_CARDINALITY")
        item = original[0]
        # Construct new objects by whitelist. Never copy the original item.
        evidence = [{k: f[k] for k in ("label", "id", "source", "pages", "text")}
                    for f in item["evidence"]]
        if [f["label"] for f in evidence] != ["F%d" % n for n in range(1, 7)]:
            raise ValueError("E_EVIDENCE_LABELS")
        inputs.append({"case": key, "source": relative, "source_sha256": expected,
                       "question": item["question"], "evidence": evidence})
    return inputs


def make_plan():
    inputs = load_inputs()
    calls = []
    for index, item in enumerate(inputs):
        order = ("qwen", "gemma") if index == 1 else ("gemma", "qwen")
        text = "DOMANDA:\n" + item["question"] + "\n\nFONTI:\n" + "\n\n".join(
            "[%s] Fonte: %s | Pagine: %s\n%s" %
            (f["label"], f["source"], f["pages"], f["text"]) for f in item["evidence"])
        messages = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": text}]
        for name in order:
            options = {"temperature": 1.0, "top_p": 0.95,
                       "top_k": MODELS[name]["top_k"], "num_ctx": 8192,
                       "num_predict": 4096, "seed": 42}
            if name == "qwen":
                options.update(min_p=0.0, presence_penalty=0.0, repeat_penalty=1.0)
            payload = {"model": MODELS[name]["tag"], "messages": messages,
                       "think": ("xhigh" if name == "qwen" else True), "stream": True, "keep_alive": 0, "options": options}
            calls.append({"ordinal": len(calls) + 1, "case": item["case"],
                          "candidate": name, "payload": payload,
                          "payload_sha256": sha(encoded(payload))})
    return {"activity": ACTIVITY, "decision_base": BASE, "pilot_status": "DA FARE",
            "driver_status": "IMPLEMENTATO", "max_generations": 6,
            "models": MODELS, "inputs": inputs, "calls": calls,
            "limits": {"request_seconds": 900, "pilot_seconds": 5400,
                       "min_available_bytes": 4000000000, "sample_seconds": 1,
                       "context": 8192, "generation_tokens": 4096, "final_words": 350},
            "code": {p.name: sha(p.read_bytes()) for p in
                     (HERE / "paired_pilot_01.py", HERE / "paired_pilot_remote_01.py")},
            "execution_authorized": False, "runtime_verified": False}


def prepare():
    plan = make_plan()
    PACKAGE.mkdir(exist_ok=False)
    save(PACKAGE / "pilot_manifest_01.json", plan)
    save(PACKAGE / "remote_binding.pending.json", {
        "activity": ACTIVITY, "plan_sha256": sha(encoded(plan)), "verified": False,
        "version": None, "models": {}, "tokens": {}, "services": [], "evidence": [],
        "checks": {k: False for k in (
            "native_profiles", "effective_options_and_seed", "tokenizer_template_equivalence",
            "no_context_shift", "stream_parser_and_total_token_cap", "supervision",
            "runtime_readiness", "human_rubric_and_sources", "latency_and_cost")}})
    save(PACKAGE / "execution_authorization.pending.json", {
        "activity": ACTIVITY, "authorized": False, "max_generations": 6,
        "plan_sha256": sha(encoded(plan)), "binding_sha256": None,
        "operation": "EXECUTE_EXISTING_PILOT_ONCE"})
    save(PACKAGE / "blind_review_form.json", {
        "blind_id": None, "score_out_of_30": None, "technical_reason": None,
        "role_position_errors": [], "phase_sequence_errors": [], "contradictions": [],
        "unsupported_claims": [], "source_insufficiency": [], "completeness": None,
        "Italian_explanation": None, "serious_tactical_errors": [],
        "cause_A_B_C_or_undetermined": [], "reviewer": None})
    return check()


def check():
    plan = read(PACKAGE / "pilot_manifest_01.json")
    if plan != make_plan():
        raise ValueError("E_PREPARED_PACKAGE_CHANGED")
    if len(plan["calls"]) != 6 or len({(c["case"], c["candidate"]) for c in plan["calls"]}) != 6:
        raise ValueError("E_SCHEDULE")
    for item in plan["inputs"]:
        pair = [c for c in plan["calls"] if c["case"] == item["case"]]
        if pair[0]["payload"]["messages"] != pair[1]["payload"]["messages"]:
            raise ValueError("E_UNEQUAL_INFORMATION")
    return {"local_package": "VALIDATO", "scope": "identity and manifest structure only",
            "generations_performed_by_check": 0, "pilot_status": "DA FARE",
            "remote_compatibility_verified": False, "plan_sha256": sha(encoded(plan))}


def bind(plan, path, authorization_path):
    """Bind observed identities and explicit revised policy, not inferred compatibility."""
    binding, authorization = read(path), read(authorization_path)
    if (binding.get("activity") != ACTIVITY
            or binding.get("policy_revision") != "observed-token-budget-02"
            or binding.get("plan_sha256") != sha(encoded(plan))):
        raise ValueError("E_POLICY_BINDING")
    if (authorization.get("authorized") is not True or authorization.get("activity") != ACTIVITY
            or authorization.get("operation") != "EXECUTE_EXISTING_PILOT_ONCE"
            or authorization.get("max_generations") != 6
            or authorization.get("plan_sha256") != sha(encoded(plan))
            or authorization.get("binding_sha256") != sha(encoded(binding))):
        raise ValueError("E_SEPARATE_AUTHORIZATION_REQUIRED")
    if not binding.get("evidence") or not binding.get("services") or not binding.get("version"):
        raise ValueError("E_REMOTE_EVIDENCE_MISSING")
    for proof in binding["evidence"]:
        file = Path(path).resolve().parent / proof["path"]
        if sha(file.read_bytes()) != proof["sha256"]:
            raise ValueError("E_DOSSIER_EVIDENCE_HASH")
    for name in MODELS:
        model = binding["models"][name]
        if (not re.fullmatch(r"[0-9a-f]{64}", model["digest"])
                or model["tag"] != MODELS[name]["tag"]
                or not model["digest"].startswith(MODELS[name]["catalog_llamacpp_digest_prefix"])
                or model.get("quantization") != "Q4_K_M"
                or model["native_profile"] != MODELS[name]["native_profile"]
                or not re.fullmatch(r"[0-9a-f]{64}", model["template_sha256"])):
            raise ValueError("E_MODEL_BINDING")
    if (binding.get("exact_prepost_tokens_verified") is not False
            or binding.get("runtime_profile_application_verified") is not False
            or binding.get("context_policy") != "observe_service_counts_stop_over_4096_prompt"):
        raise ValueError("E_UNSUPPORTED_COMPATIBILITY_CLAIM")
    return binding


def one_remote(call, binding, directory, overall_deadline):
    worker = (HERE / "paired_pilot_remote_01.py").read_bytes()
    program = "import base64;exec(base64.b64decode('%s'))" % base64.b64encode(worker).decode()
    command = "timeout --signal=TERM --kill-after=15s 900s /usr/bin/python3 -B -I -c " + shlex.quote(program)
    argv = ["ssh", "-F", r"C:\Users\giamp\.ssh\config", "-T",
            "-o", "HostKeyAlgorithms=ssh-ed25519", "-o", "KexAlgorithms=curve25519-sha256", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
            "-o", "StrictHostKeyChecking=yes", "-o", "UpdateHostKeys=no", "football-vps", command]
    request = {"call": call, "binding": binding}
    save(directory / "invocation.json", {"argv": argv, "request_sha256": sha(encoded(request))})
    events = queue.Queue()
    stderr = (directory / "stderr.raw").open("xb")
    stdout = (directory / "stdout.raw").open("xb")
    process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr)

    def collect():
        try:
            for line in iter(process.stdout.readline, b""):
                stdout.write(line)
                stdout.flush()
                os.fsync(stdout.fileno())
                events.put(line)
        finally:
            events.put(None)

    thread = threading.Thread(target=collect, daemon=True)
    thread.start()
    deadline = min(time.monotonic() + 900, overall_deadline)
    process.stdin.write(encoded(request) + b"\n")
    process.stdin.flush()
    sent = False
    completed = False
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError("E_DEADLINE_AMBIGUOUS")
            try:
                line = events.get(timeout=min(remaining, 1))
            except queue.Empty:
                continue
            if line is None:
                break
            event = json.loads(line)
            if event["event"] == "ready":
                if sent or event["payload_sha256"] != call["payload_sha256"]:
                    raise RuntimeError("E_HANDSHAKE")
                save(directory / "reserved-before-GO.json", {
                    "activity": ACTIVITY, "ordinal": call["ordinal"], "utc_ns": time.time_ns(),
                    "possible_generations": 1, "payload_sha256": call["payload_sha256"]})
                sent = True  # Irreversible reservation even if the pipe write fails.
                process.stdin.write(b"GO\n")
                process.stdin.flush()
            elif event["event"] == "wire":
                write_new(directory / ("wire-%06d.raw" % event["index"]),
                          base64.b64decode(event["bytes_base64"], validate=True))
            elif event["event"] == "finished":
                if completed or not sent:
                    raise RuntimeError("E_FINALIZATION")
                save(directory / "result.json", event)
                if event.get("ok") is not True:
                    raise RuntimeError("E_FINALIZATION")
                completed = True
            elif event["event"] in ("blocked", "abort", "error"):
                raise RuntimeError("E_REMOTE_STOP: " + str(event))
        if process.wait(timeout=max(0.1, deadline - time.monotonic())) != 0 or not completed:
            raise RuntimeError("E_INCOMPLETE_OR_AMBIGUOUS")
        thread.join(timeout=1)
        if thread.is_alive():
            raise RuntimeError("E_CAPTURE_INCOMPLETE")
    finally:
        if process.poll() is None:
            process.kill()  # Does NOT establish that remote Ollama stopped.
        process.wait()
        thread.join(timeout=2)
        if not thread.is_alive():
            stdout.close()
        stderr.flush()
        os.fsync(stderr.fileno())
        stderr.close()


def execute(binding_path, authorization_path):
    check()
    if git("branch", "--show-current").decode().strip() != "codex/tactical-state-contract-v1":
        raise ValueError("E_BRANCH")
    if git("status", "--porcelain").strip():
        raise ValueError("E_DIRTY_TREE")
    git("merge-base", "--is-ancestor", BASE, "HEAD")
    plan = read(PACKAGE / "pilot_manifest_01.json")
    binding = bind(plan, binding_path, authorization_path)
    # mkdir is the activity-wide atomic duplicate guard. No resume command.
    LEDGER.mkdir(exist_ok=False)
    save(LEDGER / "activity-created.json", {
        "activity": ACTIVITY, "plan_sha256": sha(encoded(plan)),
        "binding_sha256": sha(encoded(binding)), "HEAD": git("rev-parse", "HEAD").decode().strip(),
        "max_generations": 6, "utc_ns": time.time_ns(), "no_resume": True})
    deadline = time.monotonic() + 5400
    try:
        for call in plan["calls"]:  # Exactly six unique slots; never retries a slot.
            directory = LEDGER / ("call-%02d" % call["ordinal"])
            directory.mkdir(exist_ok=False)
            save(directory / "request.json", call)
            one_remote(call, binding, directory, deadline)
        inventory = {f.relative_to(LEDGER).as_posix(): sha(f.read_bytes())
                     for f in sorted(LEDGER.rglob("*")) if f.is_file()}
        save(LEDGER / "complete.json", {"completed_slots": 6, "promotion_authorized": False,
                                      "plan_sha256": sha(encoded(plan)), "inventory": inventory})
    except BaseException as error:
        save(LEDGER / "STOP.json", {"error": repr(error), "ambiguous": True,
                                   "no_further_calls": True, "utc_ns": time.time_ns()})
        raise


def anonymize():
    """Final channel only, lossless; custodian map remains outside blind folder."""
    if not (LEDGER / "complete.json").is_file() or (LEDGER / "STOP.json").exists():
        raise ValueError("E_PILOT_NOT_COMPLETE")
    plan = read(PACKAGE / "pilot_manifest_01.json")
    complete = read(LEDGER / "complete.json")
    if complete["plan_sha256"] != sha(encoded(plan)):
        raise ValueError("E_REVIEW_PLAN_CHANGED")
    for relative, expected in complete["inventory"].items():
        if sha((LEDGER / relative).read_bytes()) != expected:
            raise ValueError("E_REVIEW_ORIGINAL_CHANGED")
    blind = LEDGER / "blind"
    blind.mkdir(exist_ok=False)
    calls = list(plan["calls"])
    secrets.SystemRandom().shuffle(calls)
    mapping = []
    # Save the private assignment before exporting any review material.
    for call in calls:
        mapping.append({"blind_id": secrets.token_hex(12), "ordinal": call["ordinal"],
                        "candidate": call["candidate"], "case": call["case"]})
    save(LEDGER / "custodian-map.json", mapping)
    for item in mapping:
        call = plan["calls"][item["ordinal"] - 1]
        result = read(LEDGER / ("call-%02d" % item["ordinal"]) / "result.json")
        source = next(x for x in plan["inputs"] if x["case"] == item["case"])
        form = read(PACKAGE / "blind_review_form.json")
        form["blind_id"] = item["blind_id"]
        save(blind / (item["blind_id"] + ".json"), {
            "blind_id": item["blind_id"], "question": source["question"],
            "evidence": source["evidence"], "answer": result["content"], "review": form})
    return {"blind_packets": 6, "scores_assigned": 0, "identity_map_private": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "check", "execute", "anonymize"))
    parser.add_argument("--binding", type=Path)
    parser.add_argument("--authorization", type=Path)
    args = parser.parse_args()
    if args.mode == "prepare":
        result = prepare()
    elif args.mode == "check":
        result = check()
    elif args.mode == "anonymize":
        result = anonymize()
    else:
        if not args.binding or not args.authorization:
            parser.error("execute requires separately reviewed binding AND authorization")
        execute(args.binding, args.authorization)
        result = {"pilot_execution": "ESEGUITO", "promotion_authorized": False}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
