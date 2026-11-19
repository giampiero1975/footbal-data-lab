"""Synthetic NDJSON only. No networking, model, application or subprocess API."""
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import time


def deny_external(event, args):
    if event.startswith(("socket.", "subprocess.", "os.exec", "os.spawn", "os.system")):
        raise PermissionError("E_SYNTHETIC_EXTERNAL_OPERATION")


def main():
    sys.addaudithook(deny_external)
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    def emit(event, **data):
        raw = (json.dumps(dict(event=event, monotonic=time.monotonic(),
                utc_ns=time.time_ns(), **data), sort_keys=True)+"\n").encode()
        while raw:
            raw = raw[os.write(1, raw):]
    emit("ready", payload_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         pid=os.getpid(), pgid=os.getpgrp(), attempt_id=sys.argv[1],
         network_denied=True, term_policy="SIG_IGN")
    if sys.stdin.buffer.readline() != b"GO\n":
        return 40
    sequence = 0
    while True:
        emit("sample", synthetic_sequence=sequence, text="synthetic; no model output")
        sequence += 1
        time.sleep(0.25)


if __name__ == "__main__":
    raise SystemExit(main())
