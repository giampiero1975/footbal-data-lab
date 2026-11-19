"""Exactly the nine diagnostic fixtures. Only local synthetic children/sinks."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import pilot_supervision_01 as core

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
OUT = PROJECT / "docs/controller-correction-local-01"
PLAN = PROJECT / "docs/gemma-mmap-timeout-diagnosis-01/proposed-validation-plan.json"


class Clock:
    def __init__(self):
        self.value = 0.0
        self.wall = 1000000000000
    def __call__(self):
        return self.value
    def utc(self):
        return self.wall
    def advance(self, value):
        self.value = max(self.value, value)


class Hook:
    def __init__(self, callback):
        self.callback = callback
    def emit(self, event):
        self.callback(event)
        return True


def check(value, message):
    if not value:
        raise AssertionError(message)


def clean(result):
    check(not result["cleanup"]["child_alive"], "uncontrolled fixture child")
    check(not result["cleanup"]["writer_alive"], "uncontrolled custody process")


def run_case(number, directory):
    processes = []
    def attempt(mode="normal", **kw):
        folder = directory / ("attempt-%02d" % len(processes))
        command = [sys.executable, "-B", str(HERE/"controller_fixture_worker_01.py"),
                   mode, str(directory/("independent-%02d.raw" % len(processes)))]
        instance = core.Supervisor(folder, command, attempt_id="fixture-%d" % number,
            expected_payload="fixture", initial=b"REQUEST\n" if mode!="observer" else b"", **kw)
        processes.append(instance)
        result = instance.run()
        clean(result)
        return result, folder

    if number == 1:
        result, folder = attempt()
        recovered = core.recover(folder)
        check(result["ok"] and result["custody_terminal_verified"], "normal completion")
        check((folder/"stdout.raw").read_bytes() == (directory/"independent-00.raw").read_bytes(),
              "fragmented stream byte integrity")
        check(sum(x["kind"]=="reserve_before_GO" for x in recovered["records"])==1,
              "one durable reservation")
        return result
    if number == 2:
        clock = Clock()
        def jump(e):
            if e.get("event")=="sample":
                clock.advance(901)
        result, folder = attempt("continuous", clock=clock, wall=clock.utc, relay=Hook(jump))
        check(result["reason"]=="E_CONTROLLER_DEADLINE" and not result["ok"], "absolute deadline")
        core.recover(folder)
        return result
    if number == 3:
        blocked, release = threading.Event(), threading.Event()
        def sink(_):
            blocked.set()
            release.wait(3)
        emitter = core.NonBlockingEmitter(sink, lambda _:None)
        instance_box = {}
        def resources():
            if blocked.is_set():
                core.guard_then_emit("E_MEMORY_RESERVE", instance_box["s"].cancel,
                                     emitter.emit, {"event":"abort"})
            return None
        command = [sys.executable,"-B",str(HERE/"controller_fixture_worker_01.py"),
                   "quiet",str(directory/"independent-00.raw")]
        instance = core.Supervisor(directory/"attempt-00",command,attempt_id="fixture-3",
            expected_payload="fixture",initial=b"REQUEST\n",relay=emitter,resource_reason=resources)
        instance_box["s"] = instance
        try:
            result = instance.run()
            clean(result)
            check(blocked.is_set() and not release.is_set(), "sink still blocked at safety stop")
            check(result["reason"]=="E_MEMORY_RESERVE", "guard independent of logging")
        finally:
            release.set()
            check(emitter.close(), "blocked fixture emitter cleaned")
        return result
    if number == 4:
        outcomes = []
        for fail in (False, True):
            clock = Clock()
            def jump(e):
                if e.get("event")=="ready":
                    threading.Timer(0.1, lambda:clock.advance(901)).start()
                    threading.Timer(0.3, lambda:clock.advance(917)).start()
            ctx = core.mp.get_context("spawn" if os.name=="nt" else "fork")
            gate = ctx.Event()
            opts = {"writer_fail_at":4} if fail else {"writer_gate":gate,"writer_stall_at":4}
            result, folder = attempt("quiet",clock=clock,wall=clock.utc,relay=Hook(jump),**opts)
            check(not result["ok"], "sink fault cannot PASS")
            check(result["reason"] in ("E_CONTROLLER_DEADLINE","E_CUSTODY_IO","E_CUSTODY_WRITER_EXIT"),
                  "sink/timeout classified")
            check((folder/"stdout.raw").read_bytes()==(directory/("independent-%02d.raw" % (len(processes)-1))).read_bytes(),
                  "independent raw retained")
            outcomes.append(result)
        return {"variants":outcomes}
    if number == 5:
        clock = Clock()
        result, folder = attempt("late",clock=clock,wall=clock.utc,
            relay=Hook(lambda e:clock.advance(901) if e.get("event")=="finished" else None))
        check(not result["ok"] and result["reason"]=="E_CONTROLLER_DEADLINE", "late done not promoted")
        check(result["terminal_event"] is not None, "late terminal retained")
        core.recover(folder)
        return result
    if number == 6:
        gate, entered = threading.Event(), threading.Event()
        emitter = core.NonBlockingEmitter(lambda _:(entered.set(),gate.wait(3)),lambda _:None)
        try:
            result, folder = attempt(relay=emitter)
            check(entered.is_set(), "fake local consumer paused")
            recovered = core.recover(folder)
            check(result["ok"] and recovered["terminal"]["GO_sent"], "custody independent of relay")
            check((folder/"stdout.raw").read_bytes()==(directory/"independent-00.raw").read_bytes(),
                  "read-only recovery integrity")
            check(sum(x["kind"]=="GO_sent" for x in recovered["records"])==1,"no second request")
            bundle = core.export_custody(folder)
            copied = core.import_custody(bundle, directory/"recovered-copy")
            check(copied == recovered, "export/import preserves full verified journal")
            # A terminal with altered semantics must fail even if its file hash
            # is recomputed: the terminal data is bound to the journal chain.
            changed = json.loads(core.encoded(bundle))
            terminal = json.loads(core.base64.b64decode(changed["files"]["terminal.json"]["bytes_base64"]))
            terminal["reason"] = "fixture forged outcome"
            raw = core.encoded(terminal)+b"\n"
            changed["files"]["terminal.json"] = {"bytes_base64":core.base64.b64encode(raw).decode(),
                                                   "sha256":hashlib.sha256(raw).hexdigest()}
            try:
                core.import_custody(changed,directory/"rejected-copy")
            except ValueError as error:
                check(str(error)=="E_TERMINAL_INTEGRITY", "typed terminal integrity rejection")
            else:
                raise AssertionError("altered terminal accepted")
            import paired_pilot_01 as controller
            prepared = controller.remote_recovery_command("fixture-6")
            check(prepared["executed"] is False and "StrictHostKeyChecking=yes" in prepared["argv"],
                  "recovery command prepared only with strict host key")
        finally:
            gate.set();check(emitter.close(),"paused fixture relay cleaned")
        eof, _ = attempt("eof")
        check(eof["reason"]=="E_TRANSPORT_EOF", "transport loss not attributed to model")
        return {"recovered":result,"transport_EOF":eof}
    if number == 7:
        clock = Clock()
        def jump(e):
            if e.get("event")=="ready":
                threading.Timer(0.1,lambda:clock.advance(901)).start()
                threading.Timer(0.3,lambda:clock.advance(917)).start()
        def ignored_term(_):
            pass  # Explicit Windows-compatible simulation of an ignored TERM, not an OS signal claim.
        result, folder = attempt("ignore-term",clock=clock,wall=clock.utc,
                                 relay=Hook(jump),term_sender=ignored_term)
        check(result["forced_kill"] and [x["action"] for x in result["actions"]]==["TERM","KILL"],
              "TERM then KILL recorded")
        check(result["returncode"] is not None,"return code retained")
        core.recover(folder)
        result["TERM_fixture_semantics"]="injected ignored TERM; native Linux signals not tested"
        return result
    if number == 8:
        clock = Clock()
        def adjust(_):
            clock.wall += 999999999999999
        result, folder = attempt("observer",clock=clock,wall=clock.utc,relay=Hook(adjust))
        check(result["reason"]=="E_MODEL_OR_REMOTE_RESULT", "optional error retained")
        check(result["ended_monotonic"]==0,"wall step did not change monotonic budget")
        check(result["terminal_event"]["event"]=="observer_finished", "observer terminal typed")
        import gemma_mmap_observation_01 as observation
        core.exclusive(directory/"STOP.json", {"reason":"original generative reason"})
        before = (directory/"STOP.json").read_bytes()
        inactive = core.Supervisor(directory/"never-started",[],attempt_id="observer-fixture",
                                   expected_payload="unused")
        thread = threading.Thread(target=lambda:None)
        thread.start();thread.join()
        observation.finish({"supervisor":inactive,"thread":thread,"result":result,"error":None},directory)
        check((directory/"STOP.json").read_bytes()==before,"observer cannot overwrite primary stop")
        optional=json.loads((directory/"observer-exit.json").read_bytes())
        check(optional["primary_result_unchanged"] and not optional["controller_thread_alive"],
              "observer termination structured and bounded")
        core.recover(folder)
        return result
    if number == 9:
        source = (HERE/"paired_pilot_remote_01.py").read_text(encoding="utf-8")
        function = next(x for x in ast.parse(source).body if isinstance(x,ast.FunctionDef)
                        and x.name=="pressure_step")
        scope = {}
        exec(compile(ast.Module(body=[function],type_ignores=[]),"unchanged_pressure_step","exec"),scope)
        step = scope["pressure_step"]
        a={"available_bytes":5500000000,"swap_in":0,"swap_out":0}
        check(step(a,dict(a,swap_in=2),1,0,4096)[1] is None,"two isolated pages allowed")
        actions=[]
        blocked, release = threading.Event(), threading.Event()
        emitter = core.NonBlockingEmitter(lambda _:(blocked.set(),release.wait(3)),
                                         lambda e:actions.append(e))
        try:
            emitter.emit({"event":"start"})
            check(blocked.wait(1),"counter fixture sink blocked")
            reason=step(a,dict(a,available_bytes=3999999999),1,0,4096)[1]
            core.guard_then_emit(reason,lambda e:actions.append(e),emitter.emit,{"event":"sample"})
            check(actions==["E_MEMORY_RESERVE"],"exact memory threshold before emission")
            duration=0
            for i in range(5):
                old=dict(a,swap_out=i*16384);new=dict(a,swap_out=(i+1)*16384)
                duration,reason,_=step(old,new,1,duration,4096)
            check(reason=="E_PERSISTENT_PAGING" and duration==5,"unchanged paging5s/64MiB")
        finally:
            release.set()
            check(emitter.close(),"counter fixture emitter cleaned")
        return {"thresholds_unchanged":True,"new_scope":"guard/sink decoupling only"}
    raise ValueError(number)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--case",type=int,choices=range(1,10))
    args=parser.parse_args()
    OUT.mkdir(exist_ok=True)
    (OUT/".gitattributes").write_bytes(b"* -text\n")
    plan=json.loads(PLAN.read_bytes())
    for n in ([args.case] if args.case else range(1,10)):
        runs=len(list(OUT.glob("case-%02d-run-*" % n)))+1
        directory=OUT/("case-%02d-run-%02d" % (n,runs));directory.mkdir(exist_ok=False)
        record={"case":n,"name":plan["cases"][n-1]["name"],"scope":"local synthetic only",
                "code_sha256":{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                  for name in ("pilot_supervision_01.py","controller_local_fixtures_01.py",
                               "controller_fixture_worker_01.py","paired_pilot_remote_01.py")},
                "post_calls":0,"SSH":0,"models_loaded":0}
        try:
            record["evidence"]=run_case(n,directory)
            record["result"]="PASS"
        except BaseException as error:
            record.update(result="FAIL",error=repr(error))
        (directory/"result.json").write_bytes((json.dumps(record,indent=2)+"\n").encode())
        print(json.dumps({"case":n,"result":record["result"],"error":record.get("error")}),flush=True)
        if record["result"]!="PASS":
            raise SystemExit(1)


if __name__=="__main__":
    main()
