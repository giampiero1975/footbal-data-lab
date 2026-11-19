
import datetime,http.client,json,os,pathlib,shlex,shutil,subprocess
r={"activity":"RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01","scope":"read-only hardware/parameter audit","utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"generative_posts":0,"models_loaded_by_audit":0,"lock_acquired":False}
def run(argv):
 try:
  q=subprocess.run(argv,capture_output=True,text=True,timeout=10)
  return {"argv":argv,"exit":q.returncode,"stdout":q.stdout,"stderr":q.stderr}
 except Exception as e:return {"argv":argv,"error":repr(e)}
def read(path):
 try:
  with open(path) as f:return f.read(524288)
 except Exception as e:return {"error":repr(e)}
def get(path):
 assert path in ("/api/version","/api/tags","/api/ps")
 c=http.client.HTTPConnection("127.0.0.1",11434,timeout=10)
 try:
  c.request("GET",path);q=c.getresponse();b=q.read(2000000)
  return {"status":q.status,"json":json.loads(b)}
 except Exception as e:return {"error":repr(e)}
 finally:c.close()
r["version"]=get("/api/version");r["tags"]=get("/api/tags");r["loaded_before"]=get("/api/ps")
r["cpu"]=run(["lscpu","-J"]);r["uname"]=run(["uname","-a"])
r["virtualization"]=run(["systemd-detect-virt"])
r["meminfo"]=read("/proc/meminfo");r["swaps"]=read("/proc/swaps")
r["swap_metadata"]=run(["swapon","--show","--bytes","--json"])
r["disks"]=run(["lsblk","--json","--bytes","--output","NAME,TYPE,SIZE,ROTA,TRAN,MODEL,FSTYPE,MOUNTPOINTS"])
r["filesystem"]={str(p):dict(zip(("total","used","free"),shutil.disk_usage(p))) for p in ("/home/football","/usr/share/ollama/.ollama/models")}
r["top_rss"]=run(["ps","-eo","pid=,ppid=,comm=,rss=,etimes=","--sort=-rss"])
if "stdout" in r["top_rss"]:r["top_rss"]["stdout"]="\n".join(r["top_rss"]["stdout"].splitlines()[:20])
r["mountinfo_cgroup"]=[x for x in open("/proc/self/mountinfo") if "cgroup" in x]
r["self_cgroup"]=read("/proc/self/cgroup")
allowed={"OLLAMA_NUM_PARALLEL","OLLAMA_MAX_LOADED_MODELS","OLLAMA_KV_CACHE_TYPE","OLLAMA_FLASH_ATTENTION","OLLAMA_CONTEXT_LENGTH","OLLAMA_KEEP_ALIVE","OLLAMA_MAX_QUEUE","OLLAMA_LLM_LIBRARY","OLLAMA_GPU_OVERHEAD","OLLAMA_NOHISTORY"}
r["services"]=[]
for scope,unit in (("system","ollama.service"),("user","football-rag-api.service")):
 prefix=["systemctl"]+(["--user"] if scope=="user" else [])
 props=run(prefix+["show",unit,"--property=MainPID,MemoryCurrent,MemoryMax,ActiveState,ControlGroup,TasksCurrent"])
 item={"scope":scope,"unit":unit,"properties":props}
 fields=dict(x.split("=",1) for x in props.get("stdout","").splitlines() if "=" in x)
 pid=fields.get("MainPID","0")
 if pid.isdigit() and int(pid)>0:
  item["proc_status"]=read("/proc/"+pid+"/status")
  item["smaps_rollup"]=read("/proc/"+pid+"/smaps_rollup")
  item["cgroup"]=read("/proc/"+pid+"/cgroup")
  try:
   b=pathlib.Path("/proc/"+pid+"/environ").read_bytes()
   item["environment_allowlist"]={k:v for x in b.decode().split("\0") if "=" in x for k,v in [x.split("=",1)] if k in allowed}
  except Exception as ex:item["environment_allowlist"]={"error":repr(ex)}
 env=run(prefix+["show",unit,"--property=Environment","--value"])
 # Never persist the full environment: only explicitly relevant non-secret controls.
 if env.get("exit")==0:
  item["systemd_environment_allowlist"]={k:v for x in shlex.split(env["stdout"]) if "=" in x for k,v in [x.split("=",1)] if k in allowed}
 else:item["systemd_environment_allowlist"]={"error":env.get("stderr",env.get("error"))}
 group=fields.get("ControlGroup","")
 item["cgroup_limits"]={}
 paths=[pathlib.Path("/sys/fs/cgroup")]
 if group.startswith("/"):
  target=pathlib.Path("/sys/fs/cgroup")/group.strip("/")
  paths.extend([x for x in reversed([target]+list(target.parents)) if str(x).startswith("/sys/fs/cgroup/")])
 for base in paths:
  item["cgroup_limits"][str(base)]={n:read(base/n) for n in ("memory.max","memory.current","memory.swap.max","cpu.max") if (base/n).exists()}
 r["services"].append(item)
r["gpu_pci"]=[]
for device in pathlib.Path("/sys/bus/pci/devices").glob("*"):
 try:
  kind=(device/"class").read_text().strip()
  if kind.startswith("0x03"):
   r["gpu_pci"].append({"device":device.name,"class":kind,"vendor":read(device/"vendor"),"id":read(device/"device"),"driver":str((device/"driver").resolve()) if (device/"driver").exists() else None})
 except OSError:pass
r["gpu_nodes"]=[str(x) for x in pathlib.Path("/dev").glob("nvidia*")]+(["/dev/dri"] if pathlib.Path("/dev/dri").exists() else [])
r["swap_counters"]=[x for x in open("/proc/vmstat") if x.startswith(("pswpin ","pswpout "))]
r["loaded_after"]=get("/api/ps")
r["utc_end"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
print(json.dumps(r))
