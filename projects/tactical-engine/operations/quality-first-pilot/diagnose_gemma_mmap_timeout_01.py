"""Offline documentary diagnosis. Never imports or executes controller/worker/observer."""
import ast
import base64
import collections
import datetime
import hashlib
import json
from pathlib import Path
import statistics
import zipfile

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
LEDGER=PROJECT/"evaluation/gemma_mmap_on_01"
OUT=PROJECT/"docs/gemma-mmap-timeout-diagnosis-01"
BASE="aa15ed26d9c29ddb05eb950010e36cc065b9837e"

def read(file):return json.loads(file.read_bytes())
def digest(b):return hashlib.sha256(b).hexdigest()
def utc(ns):return datetime.datetime.fromtimestamp(ns/1000000000,datetime.timezone.utc).isoformat()
def sequence(items,origin):
    t=[x["monotonic"] for x in items]
    gaps=[b-a for a,b in zip(t,t[1:])]
    return {"count":len(items),"first_monotonic":t[0],"last_monotonic":t[-1],
        "first_relative_to_post":t[0]-origin,"last_relative_to_post":t[-1]-origin,
        "prefix_duration":t[-1]-t[0],"max_internal_gap":max(gaps) if gaps else None,
        "median_internal_gap":statistics.median(gaps) if gaps else None}

def main():
    OUT.mkdir(exist_ok=False)
    (OUT/".gitattributes").write_bytes(b"* -text\n")
    used=[]
    def record(path):
        b=path.read_bytes();used.append({"path":path.relative_to(PROJECT).as_posix(),"bytes":len(b),"sha256":digest(b)})
        return b
    for row in read(LEDGER/"inventory.json")["files"]:
        b=record(LEDGER/row["path"])
        if len(b)!=row["bytes"] or digest(b)!=row["sha256"]:raise ValueError("Original custody mismatch")
    ev=[json.loads(x) for x in (LEDGER/"call-01/stdout.raw").read_bytes().splitlines()]
    obs=[json.loads(x) for x in (LEDGER/"observer.stdout.jsonl").read_bytes().splitlines()]
    origin=next(x["monotonic"] for x in ev if x["event"]=="post_started")
    wires=[x for x in ev if x["event"]=="wire"]
    with zipfile.ZipFile(LEDGER/"wire-originals.zip") as archive:
        rows=read(LEDGER/"wire-inventory.json")["chunks"]
        for row,event in zip(rows,wires):
            b=archive.read(row["path"])
            if digest(b)!=row["sha256"] or b!=base64.b64decode(event["bytes_base64"]):raise ValueError("Wire mismatch")
        info=archive.infolist()
        zip_times={"first":info[0].date_time,"last":info[-1].date_time,"timezone_recorded":False,"precision_seconds":2}
    created=read(LEDGER/"activity-created.json");go=read(LEDGER/"call-01/reserved-before-GO.json");stop=read(LEDGER/"STOP.json")
    diagnostic=read(LEDGER/"post-stop-diagnostic.stdout.json");invocation=read(LEDGER/"post-stop-diagnostic-invocation.json")
    headers=next(x for x in ev if x["event"]=="http")
    timeline={"local_activity_created":{"utc_ns":created["utc_ns"],"utc":utc(created["utc_ns"])},
        "local_GO_reserved":{"utc_ns":go["utc_ns"],"utc":utc(go["utc_ns"])},
        "local_STOP_persisted":{"utc_ns":stop["utc_ns"],"utc":utc(stop["utc_ns"])},
        "local_wall_GO_to_STOP_seconds":(stop["utc_ns"]-go["utc_ns"])/1e9,
        "local_monotonic_start_deadline_detection_cleanup_timestamps":"not recorded",
        "remote_HTTP_headers":headers,
        "remote_sequences":{key:sequence(items,origin) for key,items in (
            ("all_events",ev),("samples",[x for x in ev if x["event"]=="sample"]),
            ("wire",wires),("observer",obs))},
        "remote_post_started_monotonic":origin,
        "ZIP_original_write_dates":zip_times,
        "post_diagnostic":{"remote_utc":utc(diagnostic["utc_ns"]),"remote_monotonic":diagnostic["monotonic"],
            "local_start_utc":utc(invocation["local_start_ns"]),"local_end_utc":utc(invocation["local_end_ns"]),
            "remote_wall_stamp_minus_local_end_seconds":(diagnostic["utc_ns"]-invocation["local_end_ns"])/1e9,
            "last_raw_to_post_diagnostic_remote_seconds":diagnostic["monotonic"]-ev[-1]["monotonic"]},
        "event_counts":dict(collections.Counter(x["event"] for x in ev)),
        "observer_counts":dict(collections.Counter(x["event"] for x in obs)),
        "observer_exit":read(LEDGER/"observer-exit.json"),
        "generator_SSH_exit_code":"not persisted",
        "terminal_remote_event":"absent; neither finished nor error/abort/EOF envelope",
        "interpretation":"Remote intervals and local wall intervals must not be treated as a common monotonic clock; STOP is saved after one_remote finally cleanup."}
    anchors={'paired_pilot_01.py': ['process = subprocess.Popen', 'def collect():', 'os.fsync(stdout.fileno())', 'events.put(line)', 'deadline = min(', 'process.stdin.write(encoded(request)', 'remaining = deadline - time.monotonic()', 'E_DEADLINE_AMBIGUOUS', 'line = events.get(', 'write_new(directory / (', 'process.kill()', 'thread.join(timeout=2)', 'os.fsync(stderr.fileno())'], 'paired_pilot_remote_01.py': ['def emit(', 'with output_lock:', 'print(json.dumps(', 'E_REMOTE_SUPERVISOR', 'if sys.stdin.buffer.readline()', 'HTTPConnection(', 'def sample():', 'emit("sample"', 'if reason or now - began >= 900:', 'emit("abort"', 'connection.sock.shutdown', 'line = response.readline()', 'finally:'], 'gemma_mmap_on_01.py': ['watch=observation.start', 'pilot.one_remote(', 'except BaseException as error:', 'pilot.save(LEDGER/"STOP.json"', 'if watch is not None:observation.finish'], 'gemma_mmap_observation_01.py': ['while not stop.is_set() and time.time()-start<900:', 'seen.add(pid)', 'item["smaps_rollup"]', 'emit("observation"', 'journalctl', 'observer_finished', 'def finish(', 'process.wait(timeout=8)', 'process.kill();process.wait()', 'observer-exit.json']}
    findings=[]
    for file,needles in anchors.items():
        path=HERE/file;raw=record(path);lines=raw.decode().splitlines();ast.parse(raw.decode())
        findings.append({"file":path.relative_to(PROJECT).as_posix(),"sha256":digest(raw),"anchors":[{"text":needle,"lines":[i+1 for i,l in enumerate(lines) if needle in l]} for needle in needles]})
    for file in ("todo.md","docs/experiment-register.md","docs/rag-v5-gemma-mmap-on-01.md"):
        record(PROJECT/file)
    facts={"activity":"RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01","baseline":BASE,"scope":"offline static analysis and original artifact parsing only; no runtime simulations executed", "timeline":timeline,"source_anchors":findings,
        "proven_trigger":"The sole E_DEADLINE_AMBIGUOUS branch tests remaining<=0 in the local controller.",
        "unresolved_root_cause":"No arrival timestamps, local monotonic detection/cleanup phases or remote durable terminal exist to select a causal mechanism for the unobserved interval.",
        "structural_defects":["local deadline polled only between potentially unbounded I/O/cleanup operations","remote safety monitor emits through shared blocking stdout before guard/cancellation","no remote durable evidence or terminal independent from SSH stdout","reader exceptions/SSH exit/signal/forced kill and cleanup timing not durably distinguished","observer wall clock and transport share failure modes; final-only journal/maps sampled once per PID"],
        "new_model_calls":0,"new_SSH_connections":0,"controller_changes":False,"hypotheses_not_demonstrated":["PC suspend/resume","transport interruption","local filesystem stall","CPU scheduling or process pause","wall-clock adjustment","model completion or failure after final received event"]}
    (OUT/"facts.json").write_bytes((json.dumps(facts,ensure_ascii=False,indent=2)+"\n").encode())
    (OUT/"input-inventory.json").write_bytes((json.dumps({"files":used},indent=2)+"\n").encode())
    print(json.dumps({"original_integrity":"PASS","local_wall_GO_STOP":timeline["local_wall_GO_to_STOP_seconds"],"last_sample_relative":timeline["remote_sequences"]["samples"]["last_relative_to_post"],"last_wire_relative":timeline["remote_sequences"]["wire"]["last_relative_to_post"],"model_calls":0,"SSH":0}))

if __name__=="__main__":main()
