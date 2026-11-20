"""Bounded custody/control shared by the existing pilot and local fixtures.

No network, application import or process launch at import time. Remote use
requires a separately authorized binding. A missing terminal is never a PASS.
"""
import base64
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import queue
import signal
import subprocess
import threading
import time

TIMEOUT = 900
GRACE = 15
CAPACITY = 64
MAX_BYTES = 64 * 1024 * 1024


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode()


def stamp(clock=time.monotonic, wall=time.time_ns):
    return {"monotonic": clock(), "utc_ns": wall()}


def exclusive(path, value):
    with Path(path).open("xb") as f:
        f.write(encoded(value) + b"\n")
        f.flush()
        os.fsync(f.fileno())


def _write_once(path, data, gate):
    if gate is not None:
        gate.wait()
    with Path(path).open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def durable_file(path, data, timeout=GRACE, fixture_gate=None):
    """Bounded exclusive mirrors/GO files; a hung fsync cannot hang its caller."""
    # This helper is also called after relay/control threads have started.
    # Spawn an independent interpreter, including for stdin-injected modules
    # that cannot be imported by name in a spawned Linux child.
    ctx = mp.get_context("spawn")
    code = ("import os\nif gate is not None: gate.wait()\n"
            "with open(path, 'xb') as f:\n"
            " f.write(data)\n f.flush()\n os.fsync(f.fileno())\n")
    child = ctx.Process(target=exec, args=(code, {
        "path": str(path), "data": data, "gate": fixture_gate}))
    child.start()
    child.join(timeout)
    if child.is_alive():
        child.terminate()
        child.join(0.5)
        if child.is_alive():
            child.kill()
            child.join(0.5)
        raise TimeoutError("E_CUSTODY_WRITE_DEADLINE")
    if child.exitcode != 0:
        raise OSError("E_CUSTODY_WRITE_EXIT: " + str(child.exitcode))


def _journal_writer(directory, inbox, acks, gate, stall_at, fail_at, close_fds=()):
    """Only this killable process can block in write/fsync. Fault args are fixtures."""
    root = Path(directory)
    files = []
    try:
        for fd in close_fds:
            os.close(fd)
        journal = (root / "journal.ndjson").open("xb")
        out = (root / "stdout.raw").open("xb")
        err = (root / "stderr.raw").open("xb")
        files = [journal, out, err]
        previous = "0" * 64
        size = 0
        seq = 0
        while True:
            item = inbox.get()
            if stall_at is not None and seq >= stall_at:
                gate.wait()  # A local controlled fixture, never enabled in remote_entry.
            if fail_at is not None and seq >= fail_at:
                raise OSError("fixture sink failure")
            if item["kind"] in ("stdout", "stderr"):
                raw = base64.b64decode(item["bytes_base64"], validate=True)
                (out if item["kind"] == "stdout" else err).write(raw)
            payload = dict(item, sequence=seq, previous_sha256=previous)
            previous = hashlib.sha256(encoded(payload)).hexdigest()
            line = encoded(dict(payload, sha256=previous)) + b"\n"
            size += len(line)
            if size > MAX_BYTES or seq >= 10000:
                raise OSError("E_CUSTODY_LIMIT")
            journal.write(line)
            for f in files:
                f.flush()
                os.fsync(f.fileno())
            if item["kind"] in ("reserve_before_GO", "terminal") or seq % 64 == 0:
                exclusive(root / ("checkpoint-%06d.json" % seq),
                          {"sequence": seq, "sha256": previous, "journal_bytes": size})
            if item["kind"] == "terminal":
                terminal = dict(item["data"], sequence=seq, journal_chain_sha256=previous)
                for name in ("stdout.raw", "stderr.raw", "journal.ndjson"):
                    terminal[name + "_sha256"] = hashlib.sha256((root / name).read_bytes()).hexdigest()
                exclusive(root / "terminal.json", terminal)
            acks.put({"sequence": seq, "kind": item["kind"], "sha256": previous})
            seq += 1
            if item["kind"] == "terminal":
                return
    except BaseException as error:
        acks.put({"writer_error": repr(error)})
    finally:
        for f in files:
            f.close()


def recover(directory):
    """Read-only verification, including late/failure terminals; never sends GO."""
    root = Path(directory)
    previous = "0" * 64
    records = []
    for seq, line in enumerate((root / "journal.ndjson").read_bytes().splitlines()):
        record = json.loads(line)
        digest = record.pop("sha256")
        if (record["sequence"] != seq or record["previous_sha256"] != previous
                or hashlib.sha256(encoded(record)).hexdigest() != digest):
            raise ValueError("E_JOURNAL_INTEGRITY")
        previous = digest
        records.append(dict(record, sha256=digest))
    terminal = json.loads((root / "terminal.json").read_bytes())
    if (not records or records[-1]["kind"] != "terminal"
            or terminal["sequence"] != records[-1]["sequence"]
            or terminal["journal_chain_sha256"] != previous
            or any(terminal.get(key) != value for key, value in records[-1]["data"].items())):
        raise ValueError("E_TERMINAL_INTEGRITY")
    for checkpoint in root.glob("checkpoint-*.json"):
        value = json.loads(checkpoint.read_bytes())
        seq = value["sequence"]
        if (not isinstance(seq, int) or not 0 <= seq < len(records)
                or records[seq]["sha256"] != value["sha256"]
                or checkpoint.name != "checkpoint-%06d.json" % seq):
            raise ValueError("E_CHECKPOINT_INTEGRITY")
    for name in ("stdout.raw", "stderr.raw", "journal.ndjson"):
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != terminal[name + "_sha256"]:
            raise ValueError("E_RAW_INTEGRITY")
    for kind, name in (("stdout", "stdout.raw"), ("stderr", "stderr.raw")):
        raw = b"".join(base64.b64decode(x["bytes_base64"]) for x in records if x["kind"] == kind)
        if raw != (root / name).read_bytes():
            raise ValueError("E_RAW_SEQUENCE")
    return {"terminal": terminal, "records": records}


def export_custody(directory):
    """Read-only snapshot of a completed, verified attempt; no worker or GO."""
    root = Path(directory)
    if root.resolve() != root.absolute():
        raise ValueError("E_RECOVERY_SYMLINK_PATH")
    verified = recover(root)
    names = ["journal.ndjson", "stdout.raw", "stderr.raw", "terminal.json"]
    names += sorted(p.name for p in root.glob("checkpoint-*.json"))
    files = {}
    total = 0
    for name in names:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError("E_RECOVERY_FILE_TYPE")
        raw = path.read_bytes()
        total += len(raw)
        if total > MAX_BYTES * 2:
            raise ValueError("E_RECOVERY_LIMIT")
        files[name] = {"sha256": hashlib.sha256(raw).hexdigest(),
                       "bytes_base64": base64.b64encode(raw).decode()}
    # Detect a changed journal during collection. A missing terminal is an error.
    if recover(root) != verified:
        raise ValueError("E_RECOVERY_CHANGED")
    return {"format": "pilot-custody-01", "files": files}


def import_custody(bundle, directory):
    """Exclusive local copy, followed by full chain/raw verification."""
    import re
    if bundle.get("format") != "pilot-custody-01":
        raise ValueError("E_RECOVERY_FORMAT")
    decoded = {}
    total = 0
    for name, item in bundle["files"].items():
        if not re.fullmatch(r"(?:journal\.ndjson|stdout\.raw|stderr\.raw|terminal\.json|checkpoint-[0-9]{6}\.json)", name):
            raise ValueError("E_RECOVERY_NAME")
        raw = base64.b64decode(item["bytes_base64"], validate=True)
        total += len(raw)
        if total > MAX_BYTES * 2 or hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError("E_RECOVERY_HASH_OR_LIMIT")
        decoded[name] = raw
    root = Path(directory)
    root.mkdir(mode=0o700, exist_ok=False)
    for name, raw in decoded.items():
        durable_file(root / name, raw)
    return recover(root)


class NonBlockingEmitter:
    """Optional/worker output cannot hold the safety thread's lock."""
    def __init__(self, sink, on_failure, capacity=CAPACITY):
        self.queue = queue.Queue(capacity)
        self.sink = sink
        self.on_failure = on_failure
        self.closed = threading.Event()
        self.error = None
        self.thread = threading.Thread(target=self._write, daemon=True)
        self.thread.start()

    def _fail(self, reason):
        if self.error is None:
            self.error = reason
            self.on_failure(reason)  # Cancel first; no logging in this callback.

    def _write(self):
        try:
            while not self.closed.is_set() or not self.queue.empty():
                try:
                    item = self.queue.get(timeout=0.02)
                except queue.Empty:
                    continue
                self.sink(item)
        except BaseException as error:
            self._fail("E_EVENT_SINK: " + repr(error))

    def emit(self, item):
        if self.error or self.closed.is_set():
            return False
        try:
            self.queue.put_nowait(item)
            return True
        except queue.Full:
            self._fail("E_EVENT_BACKPRESSURE")
            return False

    def close(self, timeout=1):
        self.closed.set()
        self.thread.join(timeout)
        return not self.thread.is_alive() and self.error is None


def guard_then_emit(reason, cancel, emit, value):
    """The ordering is the safety contract; emit itself must be nonblocking."""
    if reason:
        cancel(reason)
    return emit(value)


def require_single_threaded_fork():
    """Reject known unsafe bootstrap rather than fork a threaded interpreter."""
    if (threading.current_thread() is not threading.main_thread()
            or len(threading.enumerate()) != 1):
        raise RuntimeError("E_CUSTODY_FORK_THREADS")


class Supervisor:
    """Deadline loop does no filesystem/stream write or fsync while a child runs.

    Reader/sender threads have bounded queues. Custody is a separate killable
    process. Only the local fixtures override clocks, sink faults or TERM.
    """
    def __init__(self, directory, command, *, attempt_id, expected_payload,
                 initial=b"", timeout=TIMEOUT, grace=GRACE, clock=time.monotonic,
                 wall=time.time_ns, authorize=None, relay=None, resource_reason=None,
                 writer_gate=None, writer_stall_at=None, writer_fail_at=None,
                 term_sender=None, on_custody_ready=None, pass_fds=(),
                 absolute_deadline=None, on_stop=None, writer_close_fds=()):
        self.root = Path(directory)
        self.command = command
        self.attempt_id = attempt_id
        self.expected_payload = expected_payload
        self.initial = initial
        self.timeout, self.grace = timeout, grace
        self.clock, self.wall = clock, wall
        self.authorize = authorize or (lambda: True)
        self.relay = relay
        self.resource_reason = resource_reason
        self.term_sender = term_sender
        self.on_custody_ready = on_custody_ready
        self.pass_fds = pass_fds
        self.absolute_deadline = absolute_deadline
        self.on_stop = on_stop
        self.writer_close_fds = writer_close_fds
        self.ctx = mp.get_context("spawn" if os.name == "nt" else "fork")
        self.writer_gate = writer_gate or self.ctx.Event()
        if writer_gate is None:
            self.writer_gate.set()
        self.stall_at, self.fail_at = writer_stall_at, writer_fail_at
        self.cancellations = queue.Queue(1)
        self.notes = queue.Queue(CAPACITY)

    def cancel(self, reason):
        try:
            self.cancellations.put_nowait(reason)
        except queue.Full:
            pass

    def note(self, value):
        try:
            self.notes.put_nowait(value)
        except queue.Full:
            self.cancel("E_CONTROL_BACKPRESSURE")

    def run(self):
        if self.ctx.get_start_method() == "fork":
            require_single_threaded_fork()
        self.root.mkdir(mode=0o700, exist_ok=False)
        if self.root.is_symlink():
            raise ValueError("E_CUSTODY_SYMLINK")
        incoming = queue.Queue(CAPACITY)
        outgoing = queue.Queue(2)
        failure = queue.Queue(1)
        inbox, acks = self.ctx.Queue(CAPACITY), self.ctx.Queue(CAPACITY * 2)
        writer = self.ctx.Process(target=_journal_writer, args=(str(self.root), inbox, acks,
                                  self.writer_gate, self.stall_at, self.fail_at,
                                  self.writer_close_fds), daemon=True)
        writer.start()
        started = self.clock()
        deadline = started + self.timeout
        if self.absolute_deadline is not None:
            deadline = min(deadline, self.absolute_deadline)
        actions = []
        reason = None
        child = None
        readers = []
        sender = None
        sent = False
        ready = None
        reserve_sequence = None
        committed = -1
        submitted = 0
        pending_events = {}
        terminal_event = None
        eof = set()
        partial = b""
        kill_at = None
        forced = False
        writer_error = None
        ended = None
        result = None

        def fault(value):
            try:
                failure.put_nowait(value)
            except queue.Full:
                pass

        def record(kind, **data):
            nonlocal submitted
            item = dict(kind=kind, attempt_id=self.attempt_id,
                        **stamp(self.clock, self.wall), **data)
            try:
                inbox.put_nowait(item)
            except queue.Full:
                fault("E_CUSTODY_BACKPRESSURE")
                return None
            seq = submitted
            submitted += 1
            return seq

        def reader(stream, channel):
            try:
                while True:
                    b = os.read(stream.fileno(), 4096)
                    value = (channel, b, stamp(self.clock, self.wall))
                    incoming.put(value, timeout=0.05)
                    if not b:
                        return
            except BaseException as error:
                fault("E_READER: " + repr(error))

        def send():
            try:
                while True:
                    value = outgoing.get()
                    if value is None:
                        return
                    child.stdin.write(value)
                    child.stdin.flush()
            except BaseException as error:
                fault("E_STDIN_TRANSPORT: " + repr(error))

        def terminate(value):
            nonlocal reason, kill_at
            if reason is not None:
                return
            reason = value
            kill_at = self.clock() + self.grace
            if self.on_stop:
                self.on_stop(value)
            action = dict(action="TERM", cause=value, **stamp(self.clock, self.wall))
            if child is not None and child.poll() is None:
                try:
                    if self.term_sender:
                        self.term_sender(child)
                        action["delivery"] = "injected_fixture"
                    elif os.name == "posix":
                        os.killpg(child.pid, signal.SIGTERM)
                        action["delivery"] = "POSIX_process_group"
                    else:
                        child.terminate()
                        action["delivery"] = "Windows_TerminateProcess_child"
                except OSError as error:
                    action["error"] = repr(error)
            actions.append(action)
            record("control", data=action)

        try:
            # No child, relay or stdin thread before sequence0 and its
            # checkpoint have been fsynced by the writer and acknowledged.
            bootstrap_sequence = record("custody_ready", data={"writer_pid": writer.pid})
            bootstrap_until = time.monotonic() + min(self.grace, self.timeout)
            while True:
                if self.clock() >= deadline or time.monotonic() >= bootstrap_until:
                    raise RuntimeError("E_CUSTODY_BOOTSTRAP_TIMEOUT")
                try:
                    ack = acks.get(timeout=0.005)
                except queue.Empty:
                    if writer.exitcode is not None:
                        raise RuntimeError("E_CUSTODY_BOOTSTRAP_EXIT")
                    continue
                if "writer_error" in ack:
                    raise RuntimeError("E_CUSTODY_BOOTSTRAP_IO: " + ack["writer_error"])
                if (ack.get("kind") != "custody_ready" or ack.get("sequence") != bootstrap_sequence
                        or not isinstance(ack.get("sha256"), str) or len(ack["sha256"]) != 64):
                    raise RuntimeError("E_CUSTODY_BOOTSTRAP_ACK")
                committed = ack["sequence"]
                break
            if self.on_custody_ready:
                self.on_custody_ready(self, dict(ack))
            flags = {"start_new_session": True} if os.name == "posix" else {
                "creationflags": subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP}
            if self.pass_fds:
                flags["pass_fds"] = self.pass_fds
            child = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, bufsize=0, **flags)
            record("launch", data={"pid": child.pid,
                   "pgid": child.pid if os.name == "posix" else None,
                   "process_group_semantics": "POSIX_session" if os.name == "posix" else "Windows_child",
                   "deadline_monotonic": deadline,
                   "clock_info": vars(time.get_clock_info("monotonic"))})
            for channel, stream in (("stdout", child.stdout), ("stderr", child.stderr)):
                t = threading.Thread(target=reader, args=(stream, channel), daemon=True)
                t.start()
                readers.append(t)
            sender = threading.Thread(target=send, daemon=True)
            sender.start()
            if self.initial:
                outgoing.put_nowait(self.initial)
            while True:
                now = self.clock()
                if now >= deadline and reason is None:
                    terminate("E_CONTROLLER_DEADLINE")
                try:
                    terminate(failure.get_nowait())
                except queue.Empty:
                    pass
                try:
                    terminate(self.cancellations.get_nowait())
                except queue.Empty:
                    pass
                for _ in range(CAPACITY):
                    try:
                        record("external", data=self.notes.get_nowait())
                    except queue.Empty:
                        break
                if self.resource_reason and reason is None:
                    value = self.resource_reason()
                    if value:
                        terminate(value)
                for _ in range(CAPACITY):
                    try:
                        ack = acks.get_nowait()
                    except queue.Empty:
                        break
                    if "writer_error" in ack:
                        writer_error = ack["writer_error"]
                        terminate("E_CUSTODY_IO")
                        continue
                    committed = ack["sequence"]
                    event = pending_events.pop(committed, None)
                    if event is not None:
                        if self.relay:
                            self.relay.emit(event)
                        if event.get("event") == "ready":
                            ready = event
                for _ in range(CAPACITY):
                    try:
                        channel, b, received = incoming.get_nowait()
                    except queue.Empty:
                        break
                    if not b:
                        eof.add(channel)
                        record("EOF", data={"channel": channel, "received": received})
                        continue
                    seq = record(channel, bytes_base64=base64.b64encode(b).decode(),
                                 received=received)
                    if channel == "stdout":
                        partial += b
                        if len(partial) > 1048576:
                            terminate("E_FRAME_LIMIT")
                        while b"\n" in partial:
                            line, partial = partial.split(b"\n", 1)
                            try:
                                event = json.loads(line)
                            except ValueError:
                                terminate("E_TRANSPORT_PROTOCOL")
                                continue
                            # Preserve every event, not one event per read block.
                            event_seq = record("event", data=event, received=received)
                            if event_seq is not None:
                                pending_events[event_seq] = event
                            kind = event.get("event")
                            if kind in ("finished", "observer_finished"):
                                terminal_event = dict(event, received=received)
                                if kind == "observer_finished":
                                    terminal_event["ok"] = event.get("error") is None
                            elif kind in ("abort", "error", "blocked"):
                                terminate("E_REMOTE_CONTROL: " + str(event.get("error", kind)))
                # A callback/arrival may advance the clock while draining: recheck
                # before GO and before accepting terminal completion.
                if self.clock() >= deadline and reason is None:
                    terminate("E_CONTROLLER_DEADLINE")
                if ready is not None and reserve_sequence is None and reason is None:
                    if ready.get("payload_sha256") != self.expected_payload:
                        terminate("E_HANDSHAKE_IDENTITY")
                    else:
                        reserve_sequence = record("reserve_before_GO", data={
                            "payload_sha256": self.expected_payload, "max_posts": 1})
                if (reserve_sequence is not None and committed >= reserve_sequence
                        and not sent and reason is None and self.authorize()):
                    outgoing.put_nowait(b"GO\n")
                    sent = True
                    record("GO_sent", data={"reservation_sequence": reserve_sequence})
                rc = child.poll()
                if reason is not None and rc is None and self.clock() >= kill_at and not forced:
                    forced = True
                    try:
                        if os.name == "posix":
                            os.killpg(child.pid, signal.SIGKILL)
                        else:
                            child.kill()
                    except OSError:
                        pass
                    actions.append(dict(action="KILL", **stamp(self.clock, self.wall)))
                custody_drained = committed >= submitted - 1
                if (rc is not None and eof == {"stdout", "stderr"}
                        and (custody_drained or (reason and (
                            writer_error or writer.exitcode is not None or now >= kill_at)))):
                    if not reason:
                        if partial:
                            reason = "E_PARTIAL_FRAME"
                        elif not terminal_event:
                            reason = "E_TRANSPORT_EOF"
                        elif rc != 0:
                            reason = "E_REMOTE_EXIT"
                        elif (terminal_event.get("ok") is not True and not (
                                terminal_event.get("outcome") == "http_rejection"
                                and terminal_event.get("safe_to_continue") is True)):
                            reason = "E_MODEL_OR_REMOTE_RESULT"
                    ended = self.clock()
                    break
                if reason and self.clock() > kill_at + 0.5:
                    ended = self.clock()
                    break
                if writer.exitcode is not None and reason is None:
                    terminate("E_CUSTODY_WRITER_EXIT")
                time.sleep(0.005)
            if child.poll() is None:
                try:
                    child.wait(timeout=0.2)
                except subprocess.TimeoutExpired:
                    pass
            result = {"attempt_id": self.attempt_id, "reason": reason,
                      "ok": reason is None and terminal_event is not None,
                      "pid": child.pid, "pgid": child.pid if os.name == "posix" else None,
                      "returncode": child.poll(), "actions": actions, "forced_kill": forced,
                      "started_monotonic": started, "deadline_monotonic": deadline,
                      "ended_monotonic": ended, "GO_sent": sent,
                      "terminal_event": terminal_event,
                      "remote_cancellation_verified": bool(terminal_event and
                          terminal_event.get("remote_cancellation_verified") is True),
                      "promotion_authorized": False, "writer_error": writer_error,
                      "custody_ready": dict(sequence=bootstrap_sequence, writer_pid=writer.pid),
                      **stamp(self.clock, self.wall)}
            if child.poll() is not None:
                for thread in readers:
                    thread.join(timeout=0.1)
            result["reader_threads_alive_at_terminal"] = [x.is_alive() for x in readers]
            terminal_sequence = record("terminal", data=result)
            custody_until = time.monotonic() + min(self.grace, 1.0)
            durable = False
            while time.monotonic() < custody_until:
                try:
                    ack = acks.get_nowait()
                    if ack.get("sequence") == terminal_sequence and ack.get("kind") == "terminal":
                        durable = True
                        break
                except queue.Empty:
                    pass
                time.sleep(0.005)
            result["custody_terminal_verified"] = durable
            if not durable:
                result["ok"] = False
                result["reason"] = result["reason"] or "E_CUSTODY_INCOMPLETE"
            return result
        finally:
            if child is not None:
                if child.poll() is None:
                    if os.name == "posix":
                        try:
                            os.killpg(child.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    else:
                        child.kill()
                try:
                    child.wait(timeout=0.5)
                except subprocess.TimeoutExpired:
                    pass
                try:
                    outgoing.put_nowait(None)
                except queue.Full:
                    pass
                for t in readers + ([sender] if sender else []):
                    t.join(timeout=0.1)
            writer.join(timeout=0.2)
            if writer.is_alive():
                writer.terminate()
                writer.join(timeout=0.5)
                if writer.is_alive():
                    writer.kill()
                    writer.join(timeout=0.5)
            if result is not None:
                result["cleanup"] = dict(child_alive=child is not None and child.poll() is None,
                    child_returncode=child.poll() if child else None,
                    writer_pid=writer.pid, writer_exitcode=writer.exitcode,
                    writer_alive=writer.is_alive(), **stamp(self.clock, self.wall))
            inbox.cancel_join_thread()
            acks.cancel_join_thread()
            inbox.close()
            acks.close()


def remote_entry(package, core_source, worker_source):
    """Prepared only: authorized ephemeral supervisor and private remote ledger.

    Ignores SSH HUP and stops relaying on broken transport while custody and
    the fixed deadline continue. No service installation or model retry.
    """
    import pwd
    import re
    import sys
    if os.name != "posix" or pwd.getpwuid(os.getuid()).pw_name != "football":
        raise ValueError("E_REMOTE_IDENTITY")
    custody = package["custody"]
    attempt = custody["attempt_id"]
    if (custody.get("remote_write_authorized") is not True
            or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,100}", attempt)):
        raise ValueError("E_REMOTE_CUSTODY_AUTHORIZATION")
    parent = Path("/home/football/.local/share/football-data-lab/runtime-evidence")
    current = Path("/")
    for part in parent.parts[1:]:
        current /= part
        if current.exists() and current.is_symlink():
            raise ValueError("E_REMOTE_CUSTODY_SYMLINK")
    os.umask(0o077)
    parent.mkdir(mode=0o700, exist_ok=True)
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    authorized = threading.Event()
    relay = None
    injected = ("import sys,types,base64; m=types.ModuleType('pilot_supervision_01');"
                "sys.modules[m.__name__]=m;exec(base64.b64decode(%r),m.__dict__);"
                "exec(base64.b64decode(%r),{'__name__':'__main__'})" % (
                    base64.b64encode(core_source).decode(),
                    base64.b64encode(worker_source).decode()))
    command = ["timeout", "--signal=TERM", "--kill-after=15s", "900s",
               sys.executable, "-B", "-I", "-c", injected]
    request = package["request"]
    supervisor = Supervisor(parent / attempt, command, attempt_id=attempt,
        expected_payload=request["call"]["payload_sha256"],
        initial=encoded(request) + b"\n", authorize=authorized.is_set)

    def input_control():
        while True:
            line = sys.stdin.buffer.readline()
            if line == b"GO\n":
                if authorized.is_set():
                    supervisor.cancel("E_DUPLICATE_GO")
                else:
                    authorized.set()
            elif line == b"ABORT\n":
                supervisor.cancel("E_CLIENT_ABORT")
            elif not line:
                supervisor.note({"event": "transport_EOF", **stamp()})
                if not authorized.is_set():
                    supervisor.cancel("E_NO_DURABLE_GO")
                return
            else:
                supervisor.cancel("E_CONTROL_PROTOCOL")
    def custody_started(instance, ack):
        nonlocal relay
        relay = NonBlockingEmitter(lambda e: os.write(1, encoded(e) + b"\n"), lambda _: None)
        instance.relay = relay
        threading.Thread(target=input_control, daemon=True).start()
    supervisor.on_custody_ready = custody_started
    result = supervisor.run()
    relay.emit({"event": "supervisor_terminal", "result": result})
    relay.close(timeout=0.2)
    return 0 if result["ok"] else 41
