"""Synthetic local child ONLY. No network, SSH, models, or application imports."""
import base64
import json
import os
from pathlib import Path
import signal
import sys
import time


def main():
    mode, spool_name = sys.argv[1:3]
    spool = Path(spool_name).open("xb")
    def emit(value, fragmented=False):
        raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()+b"\n"
        spool.write(raw)
        spool.flush()
        os.fsync(spool.fileno())
        if fragmented:
            os.write(1, raw[:3])
            time.sleep(0.005)
            os.write(1, raw[3:])
        else:
            os.write(1, raw)
    if mode == "observer":
        emit({"event":"observation","synthetic":True}, True)
        emit({"event":"observer_finished","error":"fixture optional failure"})
        return
    if sys.stdin.buffer.readline() != b"REQUEST\n":
        raise ValueError("fixture initial request")
    emit({"event":"ready","payload_sha256":"fixture"}, True)
    if sys.stdin.buffer.readline() != b"GO\n":
        raise ValueError("fixture missing GO")
    if mode == "eof":
        return
    if mode == "normal" or mode == "late":
        body = b'{"message":{"content":"synthetic answer"},"done":true}\n'
        emit({"event":"wire","index":0,"bytes_base64":base64.b64encode(body).decode()}, True)
        emit({"event":"finished","ok":True,"content":"synthetic answer"}, True)
        return
    if mode == "ignore-term" and os.name == "posix":
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    n = 0
    while True:
        if mode == "continuous":
            emit({"event":"sample","synthetic":True,"ordinal":n})
            n += 1
        time.sleep(0.01)


if __name__ == "__main__":
    main()
