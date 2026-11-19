"""Read-only side observer, no API calls, no model or library loading."""
import base64
import json
from pathlib import Path
import shlex
import subprocess
import os

REMOTE=r'''
import json,os,pathlib,subprocess,sys,threading,time,re
stop=threading.Event();start=time.time();seen=set()
def emit(event,**kw):print(json.dumps(dict(event=event,monotonic=time.monotonic(),**kw)),flush=True)
def read(path):
 try:return pathlib.Path(path).read_text()
 except Exception as e:return {"error":repr(e)}
def stop_reader():
 sys.stdin.buffer.readline();stop.set()
threading.Thread(target=stop_reader,daemon=True).start()
allowed={"--model","--load-mode","-lm","-c","--ctx-size","-np","--parallel","--cache-type-k","--cache-type-v","--spec-draft-n-max","--spec-type","--flash-attn","-fa","-b","-ub","-t"}
emit("observer_started",pid=os.getpid(),read_only=True)
while not stop.is_set() and time.time()-start<900:
 cg={}
 for name in ("memory.stat","memory.current","memory.swap.current"):
  cg[name]=read("/sys/fs/cgroup/system.slice/ollama.service/"+name)
 runners=[]
 for x in pathlib.Path("/proc").iterdir():
  if not x.name.isdigit():continue
  try:
   if (x/"comm").read_text().strip()!="llama-server":continue
   pid=x.name;item={"pid":pid,"status":read(x/"status")}
   if pid not in seen:
    seen.add(pid)
    try:
     args=(x/"cmdline").read_bytes().decode().split("\0")
     item["selected_launch_options"]=[{"flag":a,"value":args[i+1] if i+1<len(args) else None} for i,a in enumerate(args) if a in allowed]
    except Exception as ex:item["selected_launch_options"]={"error":repr(ex)}
    item["smaps_rollup"]=read(x/"smaps_rollup")
    maps=read(x/"maps")
    item["model_file_mappings"]=[a for a in maps.splitlines() if "/.ollama/models/blobs/" in a] if isinstance(maps,str) else maps
   runners.append(item)
  except OSError:pass
 emit("observation",cgroup=cg,runners=runners)
 stop.wait(2)
try:
 q=subprocess.run(["journalctl","-u","ollama.service","--since","@"+str(int(start)),"--no-pager","-o","json","-n","1500"],capture_output=True,text=True,timeout=5)
 logs=[]
 for line in q.stdout.splitlines():
  try:row=json.loads(line)
  except ValueError:continue
  msg=row.get("MESSAGE","")
  if any(t in msg for t in ("CPU_Mapped","load-mode","load_mode","mmap","model weights","KV buffer","compute buffer","starting llama-server","model buffer")):
   msg=re.sub(r"(--api-key[= ]+)\S+",r"\1[redacted]",msg)
   logs.append({"realtime_timestamp":row.get("__REALTIME_TIMESTAMP"),"message":msg[:5000]})
 emit("journal_selection",exit=q.returncode,stderr=q.stderr,lines=logs)
except Exception as ex:emit("journal_selection",error=repr(ex))
emit("observer_finished",duration_seconds=time.time()-start)
'''

def start(directory):
    command="timeout --signal=TERM --kill-after=15s 900s /usr/bin/python3 -B -I -c "+shlex.quote("import base64;exec(base64.b64decode("+repr(base64.b64encode(REMOTE.encode()).decode())+"))")
    argv=["ssh","-F",r"C:\Users\giamp\.ssh\config","-T","-o","BatchMode=yes","-o","StrictHostKeyChecking=yes","-o","UpdateHostKeys=no","-o","HostKeyAlgorithms=ssh-ed25519","-o","KexAlgorithms=curve25519-sha256","football-vps",command]
    (directory/"observer-invocation.json").write_bytes((json.dumps({"argv":argv,"scope":"read-only optional measurements; generator unchanged"},indent=2)+"\n").encode())
    out=(directory/"observer.stdout.jsonl").open("xb");err=(directory/"observer.stderr.raw").open("xb")
    process=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=out,stderr=err)
    return process,out,err

def finish(watch,directory):
    process,out,err=watch
    try:
        process.stdin.write(b"STOP\n");process.stdin.flush();process.stdin.close()
    except (OSError,ValueError):pass
    try:process.wait(timeout=8)
    except subprocess.TimeoutExpired:
        process.kill();process.wait()
    for f in (out,err):f.flush();os.fsync(f.fileno());f.close()
    (directory/"observer-exit.json").write_bytes((json.dumps({"exit":process.returncode,"generator_not_controlled_by_observer":True})+"\n").encode())
