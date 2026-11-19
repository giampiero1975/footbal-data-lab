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
# Fixed authorized revision03 attempt; never overwrite/resume the historical01 ledger.
LEDGER = PROJECT / "evaluation/quality_first_paired_pilot_03"
PREVIOUS_LEDGER = PROJECT / "evaluation/quality_first_paired_pilot_01"
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
    """Exclusive bounded persistence; retains fsync-before-GO semantics."""
    import pilot_supervision_01 as supervision
    supervision.durable_file(path, data)


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
                     (HERE / "paired_pilot_01.py", HERE / "paired_pilot_remote_01.py",
                      HERE / "pilot_supervision_01.py")},
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
            or binding.get("policy_revision") != "persistent-paging-03"
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
    """Existing transport, corrected custody/control; stale remote bindings fail closed."""
    import pilot_supervision_01 as supervision
    custody = binding.get("custody", {})
    if (custody.get("remote_write_authorized") is not True
            or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,80}", custody.get("attempt_id", ""))):
        raise ValueError("E_REMOTE_CUSTODY_AUTHORIZATION_REQUIRED")
    core = (HERE / "pilot_supervision_01.py").read_bytes()
    worker = (HERE / "paired_pilot_remote_01.py").read_bytes()
    package = {"core":base64.b64encode(core).decode(),
               "worker":base64.b64encode(worker).decode(),
               "request":{"call":call,"binding":binding},
               "custody":dict(custody,attempt_id=custody["attempt_id"]+"-call-%02d"%call["ordinal"])}
    # Send code/package on stdin: no Windows oversized command line.
    bootstrap = ("import sys,json,base64,types; p=json.loads(sys.stdin.buffer.readline()); "
                 "m=types.ModuleType('pilot_supervision_01');sys.modules[m.__name__]=m;"
                 "c=base64.b64decode(p['core']);exec(c,m.__dict__);"
                 "sys.exit(m.remote_entry(p,c,base64.b64decode(p['worker'])))")
    command = "/usr/bin/python3 -B -I -c " + shlex.quote(bootstrap)
    argv = ["ssh","-F",r"C:\Users\giamp\.ssh\config","-T","-o","BatchMode=yes",
            "-o","ConnectTimeout=10","-o","StrictHostKeyChecking=yes","-o","UpdateHostKeys=no",
            "-o","HostKeyAlgorithms=ssh-ed25519","-o","KexAlgorithms=curve25519-sha256",
            "football-vps",command]
    save(directory/"invocation.json",{"argv":argv,"package_sha256":sha(encoded(package)),
         "remote_attempt_id":package["custody"]["attempt_id"]})
    budget = min(900, overall_deadline-time.monotonic())
    if budget <= 0:
        raise RuntimeError("E_CONTROLLER_DEADLINE_BEFORE_START")
    result = supervision.Supervisor(directory/"custody",argv,
        attempt_id=package["custody"]["attempt_id"],expected_payload=call["payload_sha256"],
        initial=encoded(package)+b"\n",timeout=budget).run()
    save(directory/"supervision-result.json",result)
    if not result["ok"] or not result["custody_terminal_verified"]:
        raise RuntimeError(result["reason"] or "E_CUSTODY_INCOMPLETE")
    recovered = supervision.recover(directory/"custody")
    remote_terminal = [x["data"] for x in recovered["records"]
        if x["kind"]=="event" and x["data"].get("event")=="supervisor_terminal"]
    if (len(remote_terminal)!=1 or remote_terminal[0]["result"].get("ok") is not True
            or remote_terminal[0]["result"].get("custody_terminal_verified") is not True):
        raise RuntimeError("E_REMOTE_CUSTODY_TERMINAL_MISSING")
    final = result["terminal_event"]
    save(directory/"result.json",final)
    return final


def remote_recovery_command(attempt_id):
    """Prepare read-only recovery; this function does not connect or execute."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,100}", attempt_id):
        raise ValueError("E_ATTEMPT_ID")
    source = base64.b64encode((HERE / "pilot_supervision_01.py").read_bytes()).decode()
    path = "/home/football/.local/share/football-data-lab/runtime-evidence/" + attempt_id
    script = ("import sys,json,base64,types; p=json.loads(sys.stdin.buffer.readline());"
              "m=types.ModuleType('pilot_supervision_01');sys.modules[m.__name__]=m;"
              "exec(base64.b64decode(p['source']),m.__dict__);"
              "sys.stdout.buffer.write(m.encoded(m.export_custody(p['path']))+b'\\n')")
    argv = ["ssh", "-F", r"C:\Users\giamp\.ssh\config", "-T", "-o", "BatchMode=yes",
            "-o", "StrictHostKeyChecking=yes", "-o", "UpdateHostKeys=no",
            "-o", "HostKeyAlgorithms=ssh-ed25519", "-o", "KexAlgorithms=curve25519-sha256",
            "football-vps", "/usr/bin/python3 -B -I -c " + shlex.quote(script)]
    return {"argv": argv, "stdin": encoded({"source": source, "path": path})+b"\n",
            "executed": False, "local_import": "pilot_supervision_01.import_custody"}


def execute(binding_path, authorization_path):
    check()
    if git("branch", "--show-current").decode().strip() != "codex/tactical-state-contract-v1":
        raise ValueError("E_BRANCH")
    if git("status", "--porcelain").strip():
        raise ValueError("E_DIRTY_TREE")
    git("merge-base", "--is-ancestor", BASE, "HEAD")
    plan = read(PACKAGE / "pilot_manifest_01.json")
    binding = bind(plan, binding_path, authorization_path)
    if not (PREVIOUS_LEDGER / "STOP.json").is_file():
        raise ValueError("E_PREVIOUS_ATTEMPT_IDENTITY")
    # Revision03 fixed atomic duplicate guard. No reset or resume command.
    LEDGER.mkdir(exist_ok=False)
    save(LEDGER / "activity-created.json", {
        "activity": ACTIVITY, "plan_sha256": sha(encoded(plan)),
        "binding_sha256": sha(encoded(binding)), "HEAD": git("rev-parse", "HEAD").decode().strip(),
        "max_generations": 6, "utc_ns": time.time_ns(), "no_resume": True,
        "previous_ledger": str(PREVIOUS_LEDGER.relative_to(PROJECT)),
        "previous_stop_sha256": sha((PREVIOUS_LEDGER / "STOP.json").read_bytes())})
    deadline = time.monotonic() + 5400
    outcomes = []
    try:
        for call in plan["calls"]:  # Exactly six unique slots; never retries a slot.
            directory = LEDGER / ("call-%02d" % call["ordinal"])
            directory.mkdir(exist_ok=False)
            save(directory / "request.json", call)
            print("Starting slot %d: %s %s" % (call["ordinal"], call["candidate"], call["case"]), flush=True)
            result = one_remote(call, binding, directory, deadline)
            outcomes.append({"ordinal":call["ordinal"], "ok":result["ok"],
                             "outcome":result.get("outcome", "response")})
            print("Finished slot %d: %s" % (call["ordinal"], outcomes[-1]), flush=True)
        inventory = {f.relative_to(LEDGER).as_posix(): sha(f.read_bytes())
                     for f in sorted(LEDGER.rglob("*")) if f.is_file()}
        save(LEDGER / "complete.json", {"completed_slots": 6,
                                      "valid_answers": sum(x["ok"] is True for x in outcomes),
                                      "outcomes": outcomes, "promotion_authorized": False,
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
    if complete.get("valid_answers") != 6:
        raise ValueError("E_SIX_VALID_ANSWERS_REQUIRED")
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
