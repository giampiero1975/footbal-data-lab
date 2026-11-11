"""Download only the two approved, digest-pinned pilot models. Never generates.

User authorization: downloads and max six generations, STOP at existing gates;
selected VPS 163.5.26.155 explicitly confirmed despite corrected resource data.
This program performs zero /api/chat calls and never invokes the pilot worker.
"""
import base64
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
EVIDENCE=ROOT/'projects/tactical-engine/docs/quality-first-pilot-authorized-readiness-01'
OUT=EVIDENCE/'downloads'
REMOTE=r"""
import http.client,json,pathlib,shutil,sys,time
plan=json.loads(sys.stdin.buffer.readline())
def emit(kind,**fields): print(json.dumps(dict(event=kind,utc_ns=time.time_ns(),**fields)),flush=True)
def request(method,path,body=None):
    if (method,path) not in [('GET','/api/tags'),('GET','/api/ps'),('POST','/api/pull'),('POST','/api/show')]:
        raise RuntimeError('E_ENDPOINT')
    c=http.client.HTTPConnection('127.0.0.1',11434,timeout=600)
    c.request(method,path,body=None if body is None else json.dumps(body).encode(),headers={} if body is None else {'Content-Type':'application/json'})
    return c,c.getresponse()
def get(path):
    c,r=request('GET',path)
    try:
        if r.status!=200: raise RuntimeError('E_GET_HTTP')
        return json.loads(r.read())
    finally: c.close()
def available():
    for line in pathlib.Path('/proc/meminfo').read_text().splitlines():
        if line.startswith('MemAvailable:'): return int(line.split()[1])*1024
    raise RuntimeError('E_MEMORY_NOT_READABLE')
try:
    before=get('/api/tags'); loaded=get('/api/ps'); free=shutil.disk_usage('/home/football').free
    existing={m['name']:m for m in before['models']}
    new=sum(m['maximum_new_bytes'] for m in plan['models'] if m['tag'] not in existing)
    emit('before',tags=before,loaded=loaded,free_disk_bytes=free,maximum_download_bytes=new,available_memory_bytes=available())
    if loaded.get('models')!=[]: raise RuntimeError('E_CONCURRENT_MODEL')
    if free-new<plan['minimum_free_disk_bytes']: raise RuntimeError('E_DISK_RESERVE_BEFORE_DOWNLOAD')
    if available()<plan['minimum_available_memory_bytes']: raise RuntimeError('E_MEMORY_BEFORE_DOWNLOAD')
    for model in plan['models']:
        tag=model['tag']
        if tag in existing:
            if existing[tag]['digest'].removeprefix('sha256:')!=model['digest']: raise RuntimeError('E_EXISTING_DIVERGENT_TAG')
            emit('already_present',model=tag)
        else:
            c,r=request('POST','/api/pull',{'model':tag,'stream':True})
            if r.status!=200: raise RuntimeError('E_PULL_HTTP_'+str(r.status))
            success=False; began=time.monotonic(); checked=0
            try:
                while True:
                    line=r.readline()
                    if not line: break
                    item=json.loads(line); emit('pull',model=tag,data=item)
                    if item.get('error'): raise RuntimeError('E_PULL_'+item['error'])
                    if item.get('status')=='success': success=True
                    now=time.monotonic()
                    if now-checked>=1:
                        disk=shutil.disk_usage('/home/football').free; mem=available()
                        if disk<plan['minimum_free_disk_bytes'] or mem<plan['minimum_available_memory_bytes']:
                            raise RuntimeError('E_RESOURCE_DURING_DOWNLOAD')
                        if now-began>1800: raise RuntimeError('E_DOWNLOAD_DEADLINE')
                        checked=now
            finally: c.close()
            if not success: raise RuntimeError('E_PULL_INCOMPLETE')
        tags=get('/api/tags'); entries=[m for m in tags['models'] if m['name']==tag]
        if len(entries)!=1 or entries[0]['digest'].removeprefix('sha256:')!=model['digest']:
            raise RuntimeError('E_DOWNLOADED_DIGEST')
        if entries[0].get('details',{}).get('quantization_level')!='Q4_K_M': raise RuntimeError('E_QUANTIZATION')
        emit('verified_model',model=entries[0])
        c,r=request('POST','/api/show',{'model':tag,'verbose':False})
        try:
            raw=r.read()
            if r.status!=200: raise RuntimeError('E_SHOW_HTTP')
            emit('show',model=tag,data=json.loads(raw))
        finally: c.close()
    emit('after',tags=get('/api/tags'),loaded=get('/api/ps'),free_disk_bytes=shutil.disk_usage('/home/football').free,
         available_memory_bytes=available(),generative_posts=0)
except Exception as e:
    emit('STOP',error=repr(e),generative_posts=0,download_cancellation_not_assumed=True)
    sys.exit(40)
"""

def main():
    plan=json.loads((EVIDENCE/'download-plan.json').read_text())
    OUT.mkdir(exist_ok=False)
    program='import base64;exec(base64.b64decode('+repr(base64.b64encode(REMOTE.encode()).decode())+'))'
    command='/usr/bin/python3 -B -I -c '+shlex.quote(program)
    argv=['ssh','-F',r'C:\Users\giamp\.ssh\config','-T','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',
          '-o','UpdateHostKeys=no','-o','HostKeyAlgorithms=ssh-ed25519','-o','KexAlgorithms=curve25519-sha256','football-vps',command]
    (OUT/'invocation.json').write_bytes((json.dumps({'argv':argv,'plan_sha256':hashlib.sha256((EVIDENCE/'download-plan.json').read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'generative_posts':0},indent=2)+'\n').encode())
    last=0
    with (OUT/'stdout.jsonl').open('xb') as raw,(OUT/'stderr.txt').open('xb') as err:
        process=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err)
        process.stdin.write(json.dumps(plan).encode()+b'\n'); process.stdin.close()
        for line in process.stdout:
            raw.write(line); raw.flush()
            event=json.loads(line)
            if event['event']!='pull' or time.monotonic()-last>=15:
                if event['event']=='pull':
                    item=event['data']; print(json.dumps({'event':'download_progress','model':event['model'],**item}),flush=True)
                else: print(json.dumps({'event':event['event'],'model':event.get('model',{}).get('name') if isinstance(event.get('model'),dict) else event.get('model'),'error':event.get('error')}),flush=True)
                last=time.monotonic()
        code=process.wait()
    (OUT/'exit-code.json').write_bytes((json.dumps({'ssh_exit':code,'generative_posts':0})+'\n').encode())
    if code: raise SystemExit(code)

if __name__=='__main__': main()
