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
import select
import socket
import stat
import subprocess
import sys
import threading
import time

LOCK = "/home/football/.local/share/football-data-lab/runtime-locks/spatial-v2-extraction-locator.lock"
ISOLATED_OPEN_ATTEMPT = "/var/lib/football-qwen27-isolation/open.json"
import pilot_supervision_01 as supervision
output_events = None


def emit(kind, **fields):
    if output_events is None or not output_events.emit(dict(
            event=kind, monotonic=time.monotonic(), utc_ns=time.time_ns(), **fields)):
        raise RuntimeError("E_EVENT_CUSTODY")


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


def pressure_step(previous, current, elapsed, persistent_seconds, page_bytes):
    """Global paging samples; not attribution to the current model."""
    if current["available_bytes"] < 4000000000:
        return persistent_seconds, "E_MEMORY_RESERVE", 0.0
    if elapsed <= 0 or page_bytes <= 0:
        return persistent_seconds, "E_RESOURCE_COUNTER", 0.0
    pages = (current["swap_in"] - previous["swap_in"],
             current["swap_out"] - previous["swap_out"])
    if min(pages) < 0:
        return persistent_seconds, "E_RESOURCE_COUNTER", 0.0
    rate = sum(pages) * page_bytes / elapsed
    stressed = rate >= 64 * 1024 * 1024 and current["available_bytes"] < 6000000000
    persistent_seconds = persistent_seconds + elapsed if stressed else 0.0
    reason = "E_PERSISTENT_PAGING" if persistent_seconds >= 5 else None
    return persistent_seconds, reason, rate


def runner_processes():
    result = subprocess.run(["ps", "-eo", "pid=,comm="], capture_output=True,
                            text=True, check=True, timeout=5)
    return [line for line in result.stdout.splitlines()
            if any(name in line for name in ("llama-server", "runner"))]


def worker_lock(isolation, payload_hash, model_digest):
    lock = os.lstat(LOCK)
    if not stat.S_ISREG(lock.st_mode) or lock.st_uid != os.getuid():
        raise RuntimeError("E_LOCK_IDENTITY")
    if isolation is not None:
        fd = isolation["lock_fd"]
        namespace = os.stat("/proc/self/ns/net")
        with open(ISOLATED_OPEN_ATTEMPT, "rb", opener=lambda path, flags:
                  os.open(path, flags | os.O_NOFOLLOW)) as marker_file:
            marker_stat = os.fstat(marker_file.fileno())
            if marker_stat.st_uid != 0 or not stat.S_ISREG(marker_stat.st_mode) or marker_stat.st_mode & 0o222:
                raise RuntimeError("E_ISOLATED_MARKER")
            marker = json.load(marker_file)
        if (os.getppid() != isolation["supervisor_pid"]
                or marker["supervisor"]["pid"] != os.getppid()
                or marker["attempt_id"] != isolation["attempt_id"]
                or marker["payload_sha256"] != payload_hash or marker["model_digest"] != model_digest
                or marker["deadline_ns"] != isolation["deadline_ns"]
                or marker["network_namespace"] != isolation["network_namespace"]
                or marker["lock"] != [lock.st_dev, lock.st_ino]
                or [namespace.st_dev, namespace.st_ino] != isolation["network_namespace"]
                or not os.path.samestat(os.fstat(fd), lock)
                or not stat.S_ISFIFO(os.fstat(isolation["stop_fd"]).st_mode)):
            raise RuntimeError("E_ISOLATED_LEASE")
        return fd

    fd = os.open(LOCK, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        if not os.path.samestat(os.fstat(fd), lock):
            raise RuntimeError("E_LOCK_IDENTITY")
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            os.lstat(ISOLATED_OPEN_ATTEMPT)
        except FileNotFoundError:
            return fd
        raise RuntimeError("E_ISOLATED_ATTEMPT_OPEN")
    except BaseException:
        os.close(fd)
        raise


def main():
    fd = None
    connection = None
    stop = threading.Event()
    aborted = threading.Event()
    monitor = None
    global output_events
    def cancel_without_logging(reason):
        aborted.set()
        if connection is not None and connection.sock:
            try:
                connection.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
    output_events = supervision.NonBlockingEmitter(
        lambda value: os.write(1, encode(value)+b"\n"), cancel_without_logging)
    try:
        request = json.loads(sys.stdin.buffer.readline())
        call, binding = request["call"], request["binding"]
        isolation = request.get("isolation")
        payload = call["payload"]
        body = encode(payload)
        if hashlib.sha256(body).hexdigest() != call["payload_sha256"]:
            raise RuntimeError("E_PAYLOAD_HASH")
        if (payload["options"]["num_ctx"] != 8192 or payload["options"]["num_predict"] != 4096
                or payload["stream"] is not True
                or payload["think"] != ("xhigh" if call["candidate"] == "qwen" else True)
                or payload["keep_alive"] != 0 or not 1 <= call["ordinal"] <= 6):
            raise RuntimeError("E_FROZEN_LIMITS")
        if sys.platform != "linux" or pwd.getpwuid(os.getuid()).pw_name != "football":
            raise RuntimeError("E_REMOTE_IDENTITY")
        parent = os.getppid()
        with open("/proc/%d/cmdline" % parent, "rb") as handle:
            argv = [part.decode() for part in handle.read().split(b"\0") if part]
        if isolation is None and (os.path.basename(argv[0]) != "timeout" or argv[1:4] !=
                ["--signal=TERM", "--kill-after=15s", "900s"] or os.getpgrp() != parent):
            raise RuntimeError("E_REMOTE_SUPERVISOR")
        current = "/"
        for part in LOCK.strip("/").split("/"):
            current = os.path.join(current, part)
            if stat.S_ISLNK(os.lstat(current).st_mode):
                raise RuntimeError("E_LOCK_SYMLINK")
        model = binding["models"][call["candidate"]]
        fd = worker_lock(isolation, call["payload_sha256"], model["digest"])
        info = os.fstat(fd)
        version, tags, loaded = get("/api/version"), get("/api/tags"), get("/api/ps")
        matches = [x for x in tags.get("models", []) if x.get("name") == model["tag"]]
        if (version.get("version") != binding["version"] or len(matches) != 1
                or matches[0].get("digest", "").removeprefix("sha256:") != model["digest"]
                or matches[0].get("details", {}).get("quantization_level") != "Q4_K_M"
                or loaded.get("models") != [] or (isolation is None and runner_processes())):
            raise RuntimeError("E_VERSION_MODEL_OR_CONCURRENCY")
        baseline = resources()
        services = service_states(binding["services"]) if isolation is None else []
        if isolation is None and concurrent_processes():
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

        def isolated_cancelled():
            return (time.monotonic_ns() >= isolation["deadline_ns"]
                    or bool(select.select([isolation["stop_fd"]], [], [], 0)[0]))

        def watch_isolated_stop():
            while not stop.is_set():
                if isolated_cancelled():
                    cancel_without_logging("E_ISOLATED_STOP")
                    return
                stop.wait(0.02)

        def sample():
            try:
                tick = 0
                previous, sampled_at, persistent = baseline, began, 0.0
                page_bytes = os.sysconf("SC_PAGE_SIZE")
                while not stop.is_set():
                    value = resources()
                    now = time.monotonic()
                    persistent, reason, rate = pressure_step(
                        previous, value, now - sampled_at, persistent, page_bytes)
                    reason = reason or ("E_DEADLINE" if now-began >= 900 else None)
                    supervision.guard_then_emit(reason, cancel_without_logging,
                        lambda value: emit(value.pop("event"), **value),
                        dict(event="sample", **value, paging_bytes_per_second=rate,
                             paging_persistent_seconds=persistent, page_bytes=page_bytes))
                    previous, sampled_at = value, now
                    if reason:
                        raise RuntimeError(reason)
                    if tick % 5 == 0:
                        service_states(binding["services"])
                        if concurrent_processes():
                            raise RuntimeError("E_CONCURRENT_PROCESS")
                    tick += 1
                    stop.wait(1)
            except Exception as error:
                cancel_without_logging(repr(error))
                try:
                    emit("abort", error=repr(error), remote_cancellation_verified=False)
                except RuntimeError:
                    pass


        if isolation is not None:
            if isolated_cancelled():
                raise RuntimeError("E_ABORT_BEFORE_POST")
            connection.connect()
        monitor = threading.Thread(target=sample if isolation is None else watch_isolated_stop,
                                   daemon=True)
        monitor.start()
        if aborted.is_set() or (isolation is not None and isolated_cancelled()):
            raise RuntimeError("E_ABORT_BEFORE_POST")
        emit("post_started", transport_calls=1)
        if isolation is not None and isolated_cancelled():
            raise RuntimeError("E_ABORT_BEFORE_POST")
        # Sole generative call site; no redirect, retries, continuation or repair.
        connection.request("POST", "/api/chat", body=body, headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        emit("http", status=response.status, headers=response.getheaders())
        if response.status >= 400:
            raw = response.read(1048577)
            emit("http_error_body", bytes_base64=base64.b64encode(raw).decode())
            if len(raw) > 1048576:
                raise RuntimeError("E_ERROR_BODY_LIMIT")
            stop.set()
            monitor.join(timeout=6)
            end = resources()
            services = service_states(binding["services"]) if isolation is None else []
            safe = (not aborted.is_set() and not monitor.is_alive()
                    and end["available_bytes"] >= 4000000000
                    and (isolation is not None or (get("/api/ps").get("models") == []
                         and not runner_processes() and not concurrent_processes()))
                    and os.fstat(fd) == info)
            emit("finished", ok=False, safe_to_continue=safe,
                 remote_cancellation_verified=isolation is None and safe, outcome="http_rejection",
                 http_status=response.status, error_body_base64=base64.b64encode(raw).decode(),
                 content="", thinking="", final_metadata=None, resources_after=end,
                 services_after=services, elapsed_seconds=time.monotonic()-began,
                 promotion_authorized=False)
            return 0 if safe else 41
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
              and type(final.get("prompt_eval_count")) is int
              and 0 < final["prompt_eval_count"] <= 4096
              and end["available_bytes"] >= 4000000000
              and not aborted.is_set() and not monitor.is_alive())
        services = service_states(binding["services"]) if isolation is None else []
        # One diagnostic read; no polling/reload if unload remains ambiguous.
        if isolation is None and (get("/api/ps").get("models") != [] or runner_processes()):
            ok = False
        if os.fstat(fd) != info:
            ok = False
        emit("finished", ok=ok, remote_cancellation_verified=isolation is None and ok,
             content="".join(content), thinking="".join(thinking),
             final_metadata=final, resources_after=end, services_after=services,
             lock_after=list(os.fstat(fd)),
             elapsed_seconds=time.monotonic() - began,
             final_words=len("".join(content).split()), promotion_authorized=False)
        return 0 if ok else 41
    except Exception as error:
        cancel_without_logging(repr(error))
        try:
            emit("error", error=repr(error), remote_cancellation_verified=False)
        except RuntimeError:
            pass
        return 40
    finally:
        stop.set()
        if connection:
            connection.close()
        if fd is not None:
            os.close(fd)
        if output_events is not None:
            output_events.close(timeout=1)


if __name__ == "__main__":
    sys.exit(main())
