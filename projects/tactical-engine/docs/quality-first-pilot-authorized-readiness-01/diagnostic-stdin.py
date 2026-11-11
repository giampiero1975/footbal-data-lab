import json,os,pathlib,subprocess,urllib.request
r={"activity":"RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01","phase":"conditional execution readiness","generative_posts":0}
def run(args):
 p=subprocess.run(args,capture_output=True,text=True,timeout=15)
 return {"argv":args,"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
r["cpu"]=run(["nproc"])
r["disks"]=run(["lsblk","-b","-ndo","NAME,SIZE,TYPE"])
r["virtualization"]=run(["systemd-detect-virt"])
r["cgroup_memory_max"]=pathlib.Path("/sys/fs/cgroup/memory.max").read_text() if pathlib.Path("/sys/fs/cgroup/memory.max").exists() else None
r["existing_server_help"]=run(["/usr/local/lib/ollama/llama-server","--help"])
print(json.dumps(r,indent=2))
