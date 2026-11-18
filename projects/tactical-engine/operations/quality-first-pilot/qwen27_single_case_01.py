"""Authorized isolated Qwen27 V10-02, one transport, frozen existing worker."""
import importlib.util
import json
from pathlib import Path
import subprocess
import time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("paired",HERE/"paired_pilot_01.py")
pilot=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)
DOCS=pilot.PROJECT/"docs/quality-first-pilot-authorized-readiness-01"
LEDGER=pilot.PROJECT/"evaluation/quality_first_qwen27_single_case_01"


def main():
    if pilot.git("branch","--show-current").decode().strip()!="codex/tactical-state-contract-v1":
        raise ValueError("E_BRANCH")
    if pilot.git("status","--porcelain").strip():
        raise ValueError("E_DIRTY_TREE")
    pilot.check()  # Identity check only, not the historical static suite.
    frozen=pilot.read(DOCS/"qwen27_single_case_authorization_01.json")
    plan=pilot.read(pilot.PACKAGE/"pilot_manifest_01.json")
    call=next(x for x in plan["calls"] if x["candidate"]=="qwen" and x["case"]=="V10-02")
    binding=pilot.read(DOCS/"execution_binding_03.json")
    if (frozen.get("authorized") is not True or frozen.get("max_generations")!=1
            or frozen.get("activity")!=pilot.ACTIVITY
            or frozen.get("operation")!="QWEN27_V10_02_SINGLE_POST"
            or frozen.get("payload_sha256")!=call["payload_sha256"]
            or frozen.get("binding_sha256")!=pilot.sha(pilot.encoded(binding))):
        raise ValueError("E_AUTHORIZATION")
    for file,expected in frozen["code_sha256"].items():
        if pilot.sha((HERE/file).read_bytes())!=expected:
            raise ValueError("E_FROZEN_CODE")
    for proof in binding["evidence"]:
        if pilot.sha((DOCS/proof["path"]).read_bytes())!=proof["sha256"]:
            raise ValueError("E_DIAGNOSTIC_EVIDENCE")
    if call["payload"]["model"]!="qwen3.8:27b" or call["payload"]["think"]!="xhigh":
        raise ValueError("E_MODEL_PROFILE")
    known=subprocess.check_output(["ssh-keygen","-F","163.5.26.155","-f",r"C:\Users\giamp\.ssh\known_hosts"])
    fingerprints=subprocess.check_output(["ssh-keygen","-lf","-"],input=known).decode()
    if "SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks" not in fingerprints:
        raise ValueError("E_HOST_KEY")
    previous=pilot.PROJECT/"evaluation/quality_first_paired_pilot_03/STOP.json"
    if pilot.sha(previous.read_bytes())!=frozen["previous_stop_sha256"]:
        raise ValueError("E_PREVIOUS_ATTEMPT")
    LEDGER.mkdir(exist_ok=False)  # Fixed one-shot guard; no CLI alternative, reset or resume.
    pilot.save(LEDGER/"activity-created.json",{
        "activity":pilot.ACTIVITY,"scope":"isolated Qwen V10-02","max_generations":1,
        "HEAD":pilot.git("rev-parse","HEAD").decode().strip(),"utc_ns":time.time_ns(),
        "authorization_sha256":pilot.sha(pilot.encoded(frozen)),
        "previous_stop_sha256":frozen["previous_stop_sha256"],"no_resume":True})
    directory=LEDGER/"call-02"
    directory.mkdir(exist_ok=False)
    pilot.save(directory/"request.json",call)
    try:
        print("Starting isolated Qwen27 V10-02: maximum one POST",flush=True)
        result=pilot.one_remote(call,binding,directory,time.monotonic()+900)
        pilot.save(LEDGER/"complete.json",{"post_slots":1,"valid_answer":result["ok"],
            "outcome":result.get("outcome","response"),"promotion_authorized":False})
        print(json.dumps({"finished":True,"valid_answer":result["ok"]}),flush=True)
    except BaseException as error:
        pilot.save(LEDGER/"STOP.json",{"error":repr(error),"ambiguous":True,
            "no_further_calls":True,"utc_ns":time.time_ns()})
        raise


if __name__=="__main__":
    main()
