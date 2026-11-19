"""One authorized Linux synthetic gate. This module never calls a model.

Operations are explicit: preflight/status only read; run is exclusive once;
export only reads a terminal attempt. No RAG locks or application imports.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import pwd
import signal
import stat
import subprocess
import sys
import threading
import time

ATTEMPT = "controller-remote-gate-20261119-01"
PARENT = Path("/home/football/.local/share/football-data-lab")
ROOT = PARENT / ATTEMPT
DEADLINE = 12
GRACE = 15
NAMES = ("remote_supervision_gate_01.py", "remote_gate_synthetic_01.py", "pilot_supervision_01.py")


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def stamps():
    return {"monotonic": time.monotonic(), "utc_ns": time.time_ns()}


def identity():
    if os.name != "posix" or pwd.getpwuid(os.getuid()).pw_name != "football":
        raise RuntimeError("E_IDENTITY")
    if not PARENT.is_dir() or PARENT.resolve() != PARENT:
        raise RuntimeError("E_PARENT_IDENTITY")


def processes():
    ancestors=set()
    cursor=os.getpid()
    while cursor>0 and cursor not in ancestors:
        ancestors.add(cursor)
        try:
            status=(Path('/proc')/str(cursor)/'status').read_text()
            cursor=int(next(x.split()[1] for x in status.splitlines() if x.startswith('PPid:')))
        except (OSError,StopIteration,ValueError):
            break
    matches = []
    concurrency = []
    runners = []
    for p in Path("/proc").iterdir():
        if not p.name.isdigit() or int(p.name) in ancestors:
            continue
        try:
            argv = (p/"cmdline").read_bytes().split(b"\0")
            argv = [x.decode(errors="replace") for x in argv if x]
            comm = (p/"comm").read_text().strip()
            item = {"pid": int(p.name), "comm": comm, "argv": argv[:8]}
            if any(str(ROOT) in arg for arg in argv):
                matches.append(item)
            if any(any(key in arg for key in (
                "run_rag_v5_query.py", "smoke_test_rag_v5_e2e.py",
                "spatial-v2-extraction-locator", "official_api_single_case_01.py",
                "paired_pilot_01.py", "gemma_mmap_on_01.py", "qwen27_single_case_01.py"))
                   for arg in argv):
                concurrency.append(item)
            if "llama-server" in comm or "runner" in comm or (
                    argv and Path(argv[0]).name == "ollama" and "runner" in argv):
                runners.append(item)
        except (OSError, ValueError):
            pass
    return {"synthetic_processes": matches, "concurrent_tests": concurrency,
            "runner_processes": runners}


def snapshot():
    identity()
    import http.client
    conn = http.client.HTTPConnection("127.0.0.1", 11434, timeout=5)
    try:
        conn.request("GET", "/api/ps")
        response = conn.getresponse()
        if response.status != 200:
            raise RuntimeError("E_DIAGNOSTIC_HTTP")
        resident = json.loads(response.read(1024*1024))
    finally:
        conn.close()
    services = []
    for user, unit in ((True,"football-rag-api.service"), (False,"ollama.service")):
        r = subprocess.run(["systemctl"]+(["--user"] if user else [])+
                           ["is-active",unit], capture_output=True, text=True, timeout=5)
        services.append({"unit":unit,"scope":"user" if user else "system",
                         "returncode":r.returncode,"state":r.stdout.strip(),"stderr":r.stderr})
    memory = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        key, rest = line.split(":",1)
        if key in ("MemTotal","MemAvailable","SwapTotal","SwapFree"):
            memory[key+"_bytes"] = int(rest.split()[0])*1024
    vfs = os.statvfs(PARENT)
    return dict(stamps(), user="football", hostname=os.uname().nodename,
                memory=memory, disk_available_bytes=vfs.f_bavail*vfs.f_frsize,
                services=services, api_ps=resident, **processes())


def require_idle(state):
    if (state["synthetic_processes"] or state["concurrent_tests"] or state["runner_processes"]
            or state["api_ps"].get("models") != []
            or any(s["state"]!="active" or s["returncode"]!=0 for s in state["services"])
            or state["memory"]["MemAvailable_bytes"] < 4000000000
            or state["disk_available_bytes"] < 100*1024*1024):
        raise RuntimeError("E_REMOTE_PREFLIGHT")


def preflight():
    state = snapshot()
    state["attempt_exists"] = os.path.lexists(ROOT)
    state["attempt_id"] = ATTEMPT
    state["synthetic_timeout_seconds"] = DEADLINE
    state["grace_seconds"] = GRACE
    state["production_timeout_unchanged_seconds"] = 900
    errors = []
    if state["attempt_exists"]:
        errors.append("E_ATTEMPT_EXISTS")
    try:
        require_idle(state)
    except RuntimeError as error:
        errors.append(str(error))
    state["ok"] = not errors
    state["errors"] = errors
    return state


def install(package):
    # Called once after local preflight, code frozen and published first.
    identity()
    if os.path.lexists(ROOT):
        raise RuntimeError("E_ATTEMPT_EXISTS")
    if set(package["files"]) != set(NAMES):
        raise RuntimeError("E_SOURCE_NAMES")
    decoded = {}
    for name, item in package["files"].items():
        raw = base64.b64decode(item["base64"],validate=True)
        if len(raw)>100000 or hashlib.sha256(raw).hexdigest()!=item["sha256"]:
            raise RuntimeError("E_SOURCE_HASH")
        decoded[name] = raw
    os.umask(0o077)
    ROOT.mkdir(mode=0o700,exist_ok=False)
    for name, raw in decoded.items():
        with (ROOT/name).open("xb") as f:
            f.write(raw);f.flush();os.fsync(f.fileno())
    manifest = {"technical_commit":package["technical_commit"],"attempt_id":ATTEMPT,
                "files":{name:{"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)}
                         for name,raw in decoded.items()},**stamps()}
    with (ROOT/"code-manifest.json").open("xb") as f:
        f.write(encoded(manifest)+b"\n");f.flush();os.fsync(f.fileno())
    return manifest


def verify_sources():
    identity()
    if ROOT.resolve()!=ROOT or stat.S_IMODE(ROOT.stat().st_mode)!=0o700:
        raise RuntimeError("E_ROOT_PERMISSIONS")
    manifest=json.loads((ROOT/"code-manifest.json").read_bytes())
    for name,item in manifest["files"].items():
        if name not in NAMES or (ROOT/name).is_symlink():
            raise RuntimeError("E_SOURCE_TYPE")
        raw=(ROOT/name).read_bytes()
        if len(raw)!=item["bytes"] or hashlib.sha256(raw).hexdigest()!=item["sha256"]:
            raise RuntimeError("E_INSTALLED_CODE")
    return manifest


def run():
    manifest=verify_sources()
    if (ROOT/"session-started.json").exists() or (ROOT/"custody").exists():
        raise RuntimeError("E_ALREADY_ATTEMPTED")
    before=snapshot()
    require_idle(before)
    sys.path.insert(0,str(ROOT))
    import pilot_supervision_01 as core
    core.exclusive(ROOT/"session-started.json",dict(before=before,pid=os.getpid(),
                   pgid=os.getpgrp(),sid=os.getsid(0),manifest=manifest,**stamps()))
    signal.signal(signal.SIGHUP,signal.SIG_IGN)
    authorized=threading.Event()
    blocked=threading.Event()
    never_release=threading.Event()
    holder={}
    sample_count=0

    def sink(event):
        nonlocal sample_count
        raw=core.encoded(event)+b"\n"
        if event.get("event")=="sample":
            sample_count+=1
        if sample_count==3:
            # Deliberately blocked optional relay: journal/control must continue.
            os.write(1,core.encoded({"event":"transport_cut_ready",**stamps()})+b"\n")
            blocked.set()
            holder["supervisor"].note({"event":"relay_blocked",**stamps()})
            never_release.wait()
        while raw:
            raw=raw[os.write(1,raw):]

    relay=None
    supervisor=core.Supervisor(ROOT/"custody",
        [sys.executable,"-B","-I",str(ROOT/"remote_gate_synthetic_01.py"),ATTEMPT],
        attempt_id=ATTEMPT,expected_payload=manifest["files"]["remote_gate_synthetic_01.py"]["sha256"],
        timeout=DEADLINE,grace=GRACE,authorize=authorized.is_set)
    holder["supervisor"]=supervisor

    def control():
        while True:
            line=sys.stdin.buffer.readline()
            if line==b"GO\n" and not authorized.is_set():
                authorized.set()
                supervisor.note({"event":"client_GO_received",**stamps()})
            elif not line:
                supervisor.note({"event":"transport_EOF",**stamps()})
                if not authorized.is_set():supervisor.cancel("E_NO_GO")
                return
            else:
                supervisor.cancel("E_CONTROL_PROTOCOL")
    def custody_started(instance,ack):
        nonlocal relay
        relay=core.NonBlockingEmitter(sink,lambda _:None)
        instance.relay=relay
        threading.Thread(target=control,daemon=True).start()
    supervisor.on_custody_ready=custody_started
    result=supervisor.run()
    # Result includes post-cleanup receipt, unlike the pre-cleanup journal terminal.
    result["relay_deliberately_blocked"]=blocked.is_set()
    result["synthetic_only"]=True
    result["ollama_cancellation_verified"]=False
    result["relay_close_completed"]=relay.close(timeout=0.2)
    core.durable_file(ROOT/"supervisor-result.json",core.encoded(result)+b"\n")
    return 0 if (result["reason"]=="E_CONTROLLER_DEADLINE"
                 and result["custody_terminal_verified"] and not result["cleanup"]["child_alive"]
                 and not result["cleanup"]["writer_alive"]) else 41


def export():
    verify_sources()
    sys.path.insert(0,str(ROOT))
    import pilot_supervision_01 as core
    bundle=core.export_custody(ROOT/"custody")
    extras={}
    for name in ("code-manifest.json","session-started.json","supervisor-result.json"):
        raw=(ROOT/name).read_bytes()
        extras[name]={"base64":base64.b64encode(raw).decode(),"sha256":hashlib.sha256(raw).hexdigest()}
    return {"custody":bundle,"extras":extras,"state_after":snapshot()}


if __name__=="__main__":
    if sys.argv[1]=="run":
        raise SystemExit(run())
    if sys.argv[1]=="export":
        print(encoded(export()).decode())
    elif sys.argv[1]=="status":
        print(encoded(snapshot()).decode())
    else:
        raise SystemExit("E_OPERATION")
