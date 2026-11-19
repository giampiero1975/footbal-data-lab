'Optional observer on the shared monotonic budget; never a model caller.'
import base64
import json
from pathlib import Path
import shlex
import threading
import time
import pilot_supervision_01 as supervision

REMOTE = r'''
import json,os,pathlib,signal,sys,threading,time
import pilot_supervision_01 as supervision
stop=threading.Event();started=time.monotonic();wall_started=time.time_ns()
errors=[];denied=set();clock_budget=min(900,float(BUDGET_SECONDS))
events=supervision.NonBlockingEmitter(lambda v:os.write(1,supervision.encoded(v)+b"\n"),
    lambda reason:(errors.append(reason),stop.set()))
def emit(event,**fields):
    return events.emit(dict(event=event,**supervision.stamp(),**fields))
def read(path):
    try:return pathlib.Path(path).read_text()
    except Exception as error:return {"error":repr(error)}
def stop_reader():
    try:sys.stdin.buffer.readline()
    finally:stop.set()
threading.Thread(target=stop_reader,daemon=True).start()
signal.signal(signal.SIGTERM,lambda *_:stop.set())
emit("observer_started",pid=os.getpid(),budget_seconds=clock_budget)
try:
    while not stop.is_set() and time.monotonic()-started<clock_budget:
        cgroup={n:read("/sys/fs/cgroup/system.slice/ollama.service/"+n)
                for n in ("memory.stat","memory.current","memory.swap.current")}
        runners=[]
        for path in pathlib.Path("/proc").iterdir():
            if not path.name.isdigit():continue
            try:
                if (path/"comm").read_text().strip()!="llama-server":continue
                item={"pid":path.name,"status":read(path/"status")}
                if path.name not in denied:
                    maps=read(path/"maps")
                    if isinstance(maps,dict):
                        denied.add(path.name);item["maps_access"]=maps
                    else:
                        item["model_file_mappings"]=[x for x in maps.splitlines()
                            if "/.ollama/models/blobs/" in x]
                    item["smaps_rollup"]=read(path/"smaps_rollup")
                runners.append(item)
            except OSError:pass
        if not emit("observation",cgroup=cgroup,runners=runners):break
        stop.wait(min(2,max(0,clock_budget-(time.monotonic()-started))))
except BaseException as error:
    errors.append(repr(error))
finally:
    emit("observer_finished",duration_seconds=time.monotonic()-started,
         error=errors[0] if errors else None,budget_expired=time.monotonic()-started>=clock_budget)
    drained=events.close(timeout=1)
sys.exit(0 if not errors and drained else 42)
'''

def start(directory, deadline=None):
    if deadline is None or deadline <= time.monotonic():
        raise ValueError("E_OBSERVER_SHARED_BUDGET_REQUIRED")
    core = Path(supervision.__file__).read_bytes()
    package = {"core":base64.b64encode(core).decode(),
               "observer":base64.b64encode(REMOTE.encode()).decode(),
               "remaining":min(900,deadline-time.monotonic())}
    bootstrap = ("import sys,json,types,base64;p=json.loads(sys.stdin.buffer.readline());"
                 "m=types.ModuleType('pilot_supervision_01');sys.modules[m.__name__]=m;"
                 "exec(base64.b64decode(p['core']),m.__dict__);"
                 "exec(base64.b64decode(p['observer']),{'BUDGET_SECONDS':p['remaining']})")
    argv=["ssh","-F",r"C:\Users\giamp\.ssh\config","-T","-o","BatchMode=yes",
          "-o","StrictHostKeyChecking=yes","-o","UpdateHostKeys=no",
          "-o","HostKeyAlgorithms=ssh-ed25519","-o","KexAlgorithms=curve25519-sha256",
          "football-vps","/usr/bin/python3 -B -I -c "+shlex.quote(bootstrap)]
    supervisor=supervision.Supervisor(Path(directory)/"observer-custody",argv,
        attempt_id="optional-observer",expected_payload="observer",
        initial=supervision.encoded(package)+b"\n",timeout=package["remaining"])
    watch={"supervisor":supervisor,"result":None,"error":None}
    def run():
        try:watch["result"]=supervisor.run()
        except BaseException as error:watch["error"]=repr(error)
    thread=threading.Thread(target=run,daemon=True)
    watch["thread"]=thread;thread.start()
    return watch

def finish(watch,directory):
    watch["supervisor"].cancel("E_OBSERVER_STOP_REQUESTED")
    watch["thread"].join(timeout=supervision.GRACE+2)
    outcome={"optional":True,"primary_result_unchanged":True,"result":watch["result"],
             "error":watch["error"],"controller_thread_alive":watch["thread"].is_alive(),
             **supervision.stamp()}
    supervision.durable_file(Path(directory)/"observer-exit.json",supervision.encoded(outcome)+b"\n")
