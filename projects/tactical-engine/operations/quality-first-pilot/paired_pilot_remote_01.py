"""Future stdin-only Linux worker: one loopback POST after durable local GO.

Not invoked during local preparation. No model/tokenizer/library loading by
this program, no installation, no remote artifact or lock-file creation.
"""
import base64
import fcntl
import hashlib
import http.client
import json
import os
import pwd
import re
import socket
import stat
import subprocess
import sys
import threading
import time

LOCK = "/home/football/.local/share/football-data-lab/runtime-locks/spatial-v2-extraction-locator.lock"
output_lock = threading.Lock()


def emit(kind, **fields):
    with output_lock:
        print(json.dumps(dict(event=kind, monotonic=time.monotonic(), **fields)), flush=True)


def encode(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def get(path):
    connection = http.client.HTTPConnection("127.0.0.1", 11434, timeout=10)
    try:
        connection.request("GET", path)
        result = connection.getresponse()
        if result.status != 200:
            raise RuntimeError("E_DIAGNOSTIC_HTTP")
        return json.loads(result.read())
    finally:
        connection.close()


def counters(path):
    result = {}
    with open(path) as handle:
        for line in handle:
            parts = line.replace(":", "").split()
            if len(parts) >= 2 and parts[1].isdigit():
                result[parts[0]] = int(parts[1]) * (1024 if len(parts) == 3 and parts[2] == "kB" else 1)
    return result


def resources():
    mem = counters("/proc/meminfo")
    vm = counters("/proc/vmstat")
    processes = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            with open("/proc/" + pid + "/comm") as handle:
                comm = handle.read().strip()
            if any(name in comm for name in ("ollama", "llama", "runner")):
                status = counters("/proc/" + pid + "/status")
                processes.append({"pid": int(pid), "comm": comm,
                                  "rss_bytes": status.get("VmRSS"), "hwm_bytes": status.get("VmHWM")})
        except (OSError, ValueError):
            pass  # Process race: report samples, never claim an exact continuous peak.
    return {"available_bytes": mem["MemAvailable"],
            "swap_used_bytes": mem.get("SwapTotal", 0) - mem.get("SwapFree", 0),
            "swap_in": vm["pswpin"], "swap_out": vm["pswpout"], "processes": processes}


def service_states(services):
    states = []
    for item in services:
        if item["scope"] not in ("system", "user") or not re.fullmatch(r"[A-Za-z0-9_.@-]+", item["unit"]):
            raise RuntimeError("E_SERVICE_BINDING")
        argv = ["systemctl"] + (["--user"] if item["scope"] == "user" else [])
        result = subprocess.run(argv + ["is-active", item["unit"]], capture_output=True, text=True, timeout=5)
        if result.returncode != 0 or result.stdout.strip() != "active":
            raise RuntimeError("E_REQUIRED_SERVICE")
        states.append({"unit": item["unit"], "scope": item["scope"], "state": "active"})
    return states


def concurrent_processes():
    process = subprocess.run(["ps", "-eo", "pid=,pgid=,args="],
                             capture_output=True, text=True, check=True, timeout=5)
    active = []
    for line in process.stdout.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) < 3 or int(parts[1]) == os.getpgrp():
            continue
        if any(name in parts[2] for name in (
                "run_rag_v5_query.py", "smoke_test_rag_v5_e2e.py",
                "spatial-v2-extraction-locator", "official_api_single_case_01.py",
                "paired_pilot_01.py")):
            active.append(line)
    return active


def main():
    fd = None
    connection = None
    stop = threading.Event()
    aborted = threading.Event()
    monitor = None
    try:
        request = json.loads(sys.stdin.buffer.readline())
        call, binding = request["call"], request["binding"]
        payload = call["payload"]
        body = encode(payload)
        if hashlib.sha256(body).hexdigest() != call["payload_sha256"]:
            raise RuntimeError("E_PAYLOAD_HASH")
        if (payload["options"]["num_ctx"] != 8192 or payload["options"]["num_predict"] != 4096
                or payload["stream"] is not True or payload["think"] is not True
                or payload["keep_alive"] != 0 or not 1 <= call["ordinal"] <= 6):
            raise RuntimeError("E_FROZEN_LIMITS")
        if sys.platform != "linux" or pwd.getpwuid(os.getuid()).pw_name != "football":
            raise RuntimeError("E_REMOTE_IDENTITY")
        parent = os.getppid()
        with open("/proc/%d/cmdline" % parent, "rb") as handle:
            argv = [part.decode() for part in handle.read().split(b"\0") if part]
        if (os.path.basename(argv[0]) != "timeout" or argv[1:4] !=
                ["--signal=TERM", "--kill-after=15s", "900s"] or os.getpgrp() != parent):
            raise RuntimeError("E_REMOTE_SUPERVISOR")
        current = "/"
        for part in LOCK.strip("/").split("/"):
            current = os.path.join(current, part)
            if stat.S_ISLNK(os.lstat(current).st_mode):
                raise RuntimeError("E_LOCK_SYMLINK")
        fd = os.open(LOCK, os.O_RDONLY | os.O_NOFOLLOW)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid():
            raise RuntimeError("E_LOCK_IDENTITY")
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        version, tags, loaded = get("/api/version"), get("/api/tags"), get("/api/ps")
        model = binding["models"][call["candidate"]]
        matches = [x for x in tags.get("models", []) if x.get("name") == model["tag"]]
        if (version.get("version") != binding["version"] or len(matches) != 1
                or matches[0].get("digest", "").removeprefix("sha256:") != model["digest"]
                or matches[0].get("details", {}).get("quantization_level") != "Q4_K_M"
                or loaded.get("models") != []):
            raise RuntimeError("E_VERSION_MODEL_OR_CONCURRENCY")
        baseline = resources()
        services = service_states(binding["services"])
        if concurrent_processes():
            raise RuntimeError("E_CONCURRENT_PROCESS")
        if baseline["available_bytes"] < 4000000000:
            raise RuntimeError("E_MEMORY_BEFORE_SEND")
        emit("ready", payload_sha256=call["payload_sha256"], version=version,
             model=matches[0], services=services, resources=baseline,
             host=socket.gethostname(), supervisor_pid=parent, pid=os.getpid(),
             lock_before=list(info))
        if sys.stdin.buffer.readline() != b"GO\n":
            raise RuntimeError("E_NO_DURABLE_GO")
        connection = http.client.HTTPConnection("127.0.0.1", 11434, timeout=900)
        began = time.monotonic()

        def sample():
            try:
                tick = 0
                while not stop.is_set():
                    value = resources()
                    emit("sample", **value)
                    if (value["available_bytes"] < 4000000000
                            or value["swap_in"] != baseline["swap_in"]
                            or value["swap_out"] != baseline["swap_out"]
                            or time.monotonic() - began >= 900):
                        raise RuntimeError("E_RESOURCE_OR_DEADLINE")
                    if tick % 5 == 0:
                        service_states(binding["services"])
                        if concurrent_processes():
                            raise RuntimeError("E_CONCURRENT_PROCESS")
                    tick += 1
                    stop.wait(1)
            except Exception as error:
                aborted.set()
                emit("abort", error=repr(error), remote_cancellation_verified=False)
                if connection.sock:
                    try:
                        connection.sock.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass

        monitor = threading.Thread(target=sample, daemon=True)
        monitor.start()
        if aborted.is_set():
            raise RuntimeError("E_ABORT_BEFORE_POST")
        emit("post_started", transport_calls=1)
        # Sole generative call site; no redirect, retries, continuation or repair.
        connection.request("POST", "/api/chat", body=body, headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        emit("http", status=response.status, headers=response.getheaders())
        content = []
        thinking = []
        final = None
        index = 0
        while True:
            line = response.readline()
            if not line:
                break
            emit("wire", index=index, bytes_base64=base64.b64encode(line).decode())
            index += 1
            item = json.loads(line)
            if final is not None or item.get("error"):
                raise RuntimeError("E_STREAM_AFTER_DONE_OR_ERROR")
            message = item.get("message", {})
            content.append(message.get("content", ""))
            thinking.append(message.get("thinking", ""))
            if item.get("done") is True:
                final = item
        stop.set()
        monitor.join(timeout=6)
        end = resources()
        ok = (response.status == 200 and final is not None
              and final.get("done_reason") == "stop" and bool("".join(content).strip())
              and type(final.get("eval_count")) is int and 0 < final["eval_count"] <= 4096
              and final.get("prompt_eval_count") == binding["tokens"][str(call["ordinal"])]["prompt_tokens"]
              and end["available_bytes"] >= 4000000000
              and (end["swap_in"], end["swap_out"]) == (baseline["swap_in"], baseline["swap_out"])
              and not aborted.is_set() and not monitor.is_alive())
        services = service_states(binding["services"])
        # One diagnostic read; no polling/reload if unload remains ambiguous.
        if get("/api/ps").get("models") != []:
            ok = False
        if os.fstat(fd) != info:
            ok = False
        emit("finished", ok=ok, content="".join(content), thinking="".join(thinking),
             final_metadata=final, resources_after=end, services_after=services,
             lock_after=list(os.fstat(fd)),
             elapsed_seconds=time.monotonic() - began,
             final_words=len("".join(content).split()), promotion_authorized=False)
        return 0 if ok else 41
    except Exception as error:
        emit("error", error=repr(error), remote_cancellation_verified=False)
        return 40
    finally:
        stop.set()
        if connection:
            connection.close()
        if fd is not None:
            os.close(fd)


if __name__ == "__main__":
    sys.exit(main())
