"""Authorized diagnostic only. No worker import, generation, lock acquisition or writes remotely.

New phase of RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01; does not repeat 32 static checks.
GET whitelist plus /api/show only for installed selected tags. CLI help only.
"""
import base64
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = ROOT / "projects/tactical-engine/docs/quality-first-pilot-remote-preflight-01"
EXPECTED_HOST_KEY = "SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks"
SSH_CONFIG = r"C:\Users\giamp\.ssh\config"
KNOWN_HOSTS = r"C:\Users\giamp\.ssh\known_hosts"
REMOTE = r"""
import base64,datetime,http.client,json,os,pathlib,pwd,re,shutil,stat,subprocess
result={'activity':'RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01','phase':'diagnostic read-only preflight',
        'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'uid':os.getuid(),
        'user':pwd.getpwuid(os.getuid()).pw_name,'requests':[], 'generative_posts':0,'lock_acquired':False}
if result['user']!='football': raise RuntimeError('E_REMOTE_USER')
def run(argv):
    try:
        p=subprocess.run(argv,capture_output=True,text=True,timeout=10)
        return {'argv':argv,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    except Exception as e: return {'argv':argv,'error':repr(e)}
def api(method,path,body=None):
    if (method,path) not in [('GET','/api/version'),('GET','/api/tags'),('GET','/api/ps'),('POST','/api/show')]:
        raise RuntimeError('E_ENDPOINT_NOT_AUTHORIZED')
    conn=http.client.HTTPConnection('127.0.0.1',11434,timeout=10)
    record={'method':method,'path':path,'body':body}
    try:
        payload=None if body is None else json.dumps(body).encode()
        conn.request(method,path,body=payload,headers={} if body is None else {'Content-Type':'application/json'})
        res=conn.getresponse(); raw=res.read(4000001)
        record.update(status=res.status,headers=res.getheaders(),raw_base64=base64.b64encode(raw).decode(),bytes=len(raw))
        if len(raw)>4000000: raise RuntimeError('E_DIAGNOSTIC_SIZE')
        record['json']=json.loads(raw)
    except Exception as e: record['error']=repr(e)
    finally:
        conn.close(); result['requests'].append(record)
    return record.get('json') if record.get('status')==200 and not record.get('error') else None

def metadata(path):
    try:
        x=os.lstat(path)
        return {'path':path,'exists':True,'uid':x.st_uid,'gid':x.st_gid,'mode':oct(stat.S_IMODE(x.st_mode)),
                'regular':stat.S_ISREG(x.st_mode),'directory':stat.S_ISDIR(x.st_mode),
                'symlink':stat.S_ISLNK(x.st_mode),'size':x.st_size,'inode':x.st_ino,'dev':x.st_dev,'mtime_ns':x.st_mtime_ns}
    except FileNotFoundError: return {'path':path,'exists':False}
    except Exception as e: return {'path':path,'error':repr(e)}
def readfile(path):
    try: return pathlib.Path(path).read_text()
    except Exception as e: return {'error':repr(e)}

result['version']=api('GET','/api/version')
result['tags']=api('GET','/api/tags')
result['loaded_before']=api('GET','/api/ps')
installed={x.get('name') for x in (result['tags'] or {}).get('models',[])}
result['selected']={}
for name in ['gemma4:26b','qwen3.8:27b']:
    entry={'installed_exact_tag':name in installed}
    if name in installed: entry['show']=api('POST','/api/show',{'model':name,'verbose':False})
    result['selected'][name]=entry

ollama=shutil.which('ollama')
result['ollama_executable']=ollama
result['official_cli_help']=run([ollama,'--help']) if ollama else {'unavailable':True}
result['official_show_help']=run([ollama,'show','--help']) if ollama else {'unavailable':True}
result['tokenizer_commands_on_PATH']={name:shutil.which(name) for name in
    ['llama-tokenize','llama-cli','llama-server','ollama-tokenize']}
# Bounded names in established installation roots, no recursive host/source scan.
result['installed_interface_roots']={}
for name in ['/usr/local/lib/ollama','/usr/lib/ollama','/usr/share/doc/ollama']:
    root=pathlib.Path(name)
    try: result['installed_interface_roots'][name]=sorted(x.name for x in root.iterdir())[:100]
    except FileNotFoundError: result['installed_interface_roots'][name]=None
    except Exception as e: result['installed_interface_roots'][name]={'error':repr(e)}

result['meminfo']=readfile('/proc/meminfo')
vm=readfile('/proc/vmstat')
result['swap_counters']=[x for x in vm.splitlines() if x.startswith(('pswpin ','pswpout '))] if isinstance(vm,str) else vm
result['services']=[run(['systemctl','--user','is-active','football-rag-api.service']),run(['systemctl','is-active','ollama.service'])]
result['disk']={}
for path in ['/home/football','/opt/football-data-lab']:
    try: result['disk'][path]=dict(zip(['total','used','free'],shutil.disk_usage(path)))
    except Exception as e: result['disk'][path]={'error':repr(e)}
lock='/home/football/.local/share/football-data-lab/runtime-locks/spatial-v2-extraction-locator.lock'
result['lock_before']=metadata(lock)
result['lock_path_components']=[]
cur='/'
for part in lock.strip('/').split('/'):
    cur=os.path.join(cur,part); result['lock_path_components'].append(metadata(cur))
result['kernel_lock_records']=[]
if result['lock_before'].get('exists'):
    device=result['lock_before']['dev']; inode=result['lock_before']['inode']
    for line in pathlib.Path('/proc/locks').read_text().splitlines():
        for field in line.split():
            match=re.fullmatch(r'([0-9a-fA-F]+):([0-9a-fA-F]+):(\d+)',field)
            if match and (int(match[1],16),int(match[2],16),int(match[3]))==(os.major(device),os.minor(device),inode):
                result['kernel_lock_records'].append(line)
result['known_remote_pilot_path']=metadata('/opt/football-data-lab/projects/tactical-engine/evaluation/quality_first_paired_pilot_01')
result['observable_processes']=[]
for proc in pathlib.Path('/proc').iterdir():
    if not proc.name.isdigit(): continue
    try:
        comm=(proc/'comm').read_text().strip()
        args=(proc/'cmdline').read_bytes().split(b'\0')
        names=[os.path.basename(a.decode(errors='replace')) for a in args if a.endswith(b'.py')]
        if any(x in comm.lower() for x in ['ollama','llama','runner']) or any(x in names for x in
            ['paired_pilot_01.py','official_api_single_case_01.py','smoke_test_rag_v5_e2e.py','run_rag_v5_query.py']):
            result['observable_processes'].append({'pid':int(proc.name),'comm':comm,'script_basenames':names})
    except (FileNotFoundError,PermissionError,ProcessLookupError): pass
result['loaded_after']=api('GET','/api/ps')
result['lock_after']=metadata(lock)
result['lock_metadata_preserved']=result['lock_before']==result['lock_after']
result['utc_end']=datetime.datetime.now(datetime.timezone.utc).isoformat()
print(json.dumps(result,ensure_ascii=False,indent=2))
"""

def main():
    # Reconcile config/public host identity before the sole diagnostic SSH session.
    conf=subprocess.check_output(['ssh','-F',SSH_CONFIG,'-G','football-vps'],text=True)
    fields={}
    for line in conf.splitlines():
        key,_,value=line.partition(' ')
        if key in ['hostname','user','port','identityfile','identitiesonly','stricthostkeychecking']:
            fields.setdefault(key,[]).append(value)
    if (fields.get('hostname')!=['163.5.26.155'] or fields.get('user')!=['football']
            or fields.get('port')!=['22'] or fields.get('identitiesonly')!=['yes']
            or fields.get('identityfile')!=['~/.ssh/codex-football-vps-ed25519-v3']):
        raise RuntimeError('E_AUTHORIZED_ALIAS')
    known=subprocess.check_output(['ssh-keygen','-F','163.5.26.155','-f',KNOWN_HOSTS],text=True)
    verified=False
    for line in known.splitlines():
        if not line or line.startswith('#'): continue
        parts=line.split()
        if parts[1]=='ssh-ed25519':
            fp='SHA256:'+base64.b64encode(hashlib.sha256(base64.b64decode(parts[2])).digest()).decode().rstrip('=')
            verified=verified or fp==EXPECTED_HOST_KEY
    if not verified: raise RuntimeError('E_HOST_KEY')
    OUT.mkdir(exist_ok=False)
    argv=['ssh','-F',SSH_CONFIG,'-T','-o','BatchMode=yes','-o','ConnectTimeout=10',
          '-o','StrictHostKeyChecking=yes','-o','UpdateHostKeys=no',
          '-o','KexAlgorithms=curve25519-sha256','-o','HostKeyAlgorithms=ssh-ed25519',
          'football-vps','/usr/bin/python3 -B -I -']
    invocation={'activity':'RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01','phase':'read-only diagnostic',
                'argv':argv,'config':fields,'verified_host_key':EXPECTED_HOST_KEY,
                'program_sha256':hashlib.sha256(REMOTE.encode()).hexdigest(),
                'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'local_execution_ledger_exists':(ROOT/'projects/tactical-engine/evaluation/quality_first_paired_pilot_01').exists(),
                'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (OUT/'invocation.json').write_text(json.dumps(invocation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'stdout.json').open('xb') as stdout,(OUT/'stderr.txt').open('xb') as stderr:
        result=subprocess.run(argv,input=REMOTE.encode(),stdout=stdout,stderr=stderr,timeout=120)
    (OUT/'exit-code.json').write_text(json.dumps({'ssh_exit':result.returncode})+'\n',encoding='utf-8')
    print(json.dumps({'ssh_exit':result.returncode,'evidence_directory':str(OUT)}))

if __name__=='__main__': main()
