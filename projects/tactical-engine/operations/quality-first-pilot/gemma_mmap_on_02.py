"""Authorized single Gemma mmap attempt02. Delegates the existing transport.

prepare is file-only. execute is exclusive, committed and published first.
No retry, six-slot loop, repair, fallback, service changes or model download.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time
import paired_pilot_01 as pilot
import pilot_supervision_01 as core

HERE=Path(__file__).resolve().parent
PROJECT=pilot.PROJECT
PREP=PROJECT/'docs/gemma-mmap-on-02-preparation'
LEDGER=PROJECT/'evaluation/gemma_mmap_on_02'
FROZEN=PROJECT/'docs/gemma26-mmap-post-gate02-readiness-01/payload.frozen.json'
EXPECTED='7bc057b52a120ebbc5415ebd22da236f66fd1240421f4b114fcde629a6de97ce'
REMOTE='/home/football/.local/share/football-data-lab/runtime-evidence/gemma-mmap-on-02-call-01'
SSH=['ssh','-F',r'C:\Users\giamp\.ssh\config','-T','-o','BatchMode=yes',
     '-o','ConnectTimeout=10','-o','StrictHostKeyChecking=yes','-o','UpdateHostKeys=no',
     '-o','HostKeyAlgorithms=ssh-ed25519','-o','KexAlgorithms=curve25519-sha256','football-vps']
CODE=('gemma_mmap_on_02.py','paired_pilot_01.py','paired_pilot_remote_01.py','pilot_supervision_01.py')

# Executed solely in a separate diagnostic SSH process, never in the model worker.
DIAGNOSTIC=r'''
import os,stat,pathlib,hashlib,time,sys
def snapshot(m,binding):
    services=m.service_states(binding['services'])
    data={'version':m.get('/api/version'),'tags':m.get('/api/tags'),'ps':m.get('/api/ps'),
          'resources':m.resources(),'services':services,'runners':m.runner_processes(),
          'concurrent':m.concurrent_processes(),'monotonic':time.monotonic(),'utc_ns':time.time_ns(),
          'python':sys.version}
    parent=pathlib.Path('/home/football/.local/share/football-data-lab')
    destination=pathlib.Path(REMOTE)
    v=os.statvfs(parent);data['disk_available_bytes']=v.f_bavail*v.f_frsize
    data['destination_exists']=os.path.lexists(destination)
    data['critical_symlinks']=[str(p) for p in [destination,*destination.parents] if p.is_symlink()]
    info=os.lstat(m.LOCK)
    data['lock']={'dev':info.st_dev,'ino':info.st_ino,'uid':info.st_uid,'mode':info.st_mode,
                  'regular':stat.S_ISREG(info.st_mode),'symlink':stat.S_ISLNK(info.st_mode)}
    data['lock_path_symlinks']=[str(p) for p in [pathlib.Path(m.LOCK),*pathlib.Path(m.LOCK).parents] if p.is_symlink()]
    data['uid']=os.getuid()
    # Observe known ephemeral supervisors without copying their large argv.
    ancestors=set();cursor=os.getpid()
    while cursor>0 and cursor not in ancestors:
        ancestors.add(cursor)
        try:cursor=int(next(x.split()[1] for x in pathlib.Path('/proc',str(cursor),'status').read_text().splitlines() if x.startswith('PPid:')))
        except (OSError,ValueError,StopIteration):break
    data['ephemeral_supervisors']=[]
    for p in pathlib.Path('/proc').iterdir():
        if not p.name.isdigit() or int(p.name) in ancestors:continue
        try:
            raw=(p/'cmdline').read_bytes()
            if b"types.ModuleType('pilot_supervision_01')" in raw or b'controller-remote-gate-' in raw:
                data['ephemeral_supervisors'].append({'pid':int(p.name),'argv_sha256':hashlib.sha256(raw).hexdigest()})
        except OSError:pass
    return data
'''


def sha(raw):return hashlib.sha256(raw).hexdigest()
def save(path,value):core.exclusive(path,value)
def read(path):return json.loads(Path(path).read_bytes())


def prepare():
    assert sha(FROZEN.read_bytes())==EXPECTED
    assert not LEDGER.exists()
    PREP.mkdir(exist_ok=False)
    (PREP/'.gitattributes').write_bytes(b'* -text\n')
    old=read(PROJECT/'docs/quality-first-pilot-authorized-readiness-01/execution_binding_03.json')
    binding=dict(old,models={'gemma':old['models']['gemma']},
                 custody={'remote_write_authorized':True,'attempt_id':'gemma-mmap-on-02'})
    save(PREP/'binding.json',binding)
    auth=Path(r'C:\Users\giamp\.codex\attachments\8437fa90-5da2-451f-ba4d-1aa895cbfa94\Testo incollato.txt')
    save(PREP/'manifest.json',{'activity':pilot.ACTIVITY,'attempt_id':'gemma-mmap-on-02',
        'baseline':'98211a31a944d61fbf16626a1f9f3de486bf7fe7','authorized':True,'max_POST':1,
        'authorization_source_sha256':sha(auth.read_bytes()),'payload_sha256':EXPECTED,
        'binding_sha256':sha((PREP/'binding.json').read_bytes()),
        'code_sha256':{name:sha((HERE/name).read_bytes()) for name in CODE},
        'limits':{'absolute_seconds':900,'grace_seconds':15,'RAM_minimum_bytes':4000000000},
        'difference':'Same historical mmap payload, corrected independent supervision/custody after Gate02; old final absent.',
        'retry':0,'repair':0,'fallback':0,'promotion_authorized':False})
    print('Prepared only; no SSH or POST.')


def capture(label,argv,data=None):
    save(LEDGER/(label+'-invocation.json'),{'argv':argv,'stdin_sha256':sha(data) if data else None,**core.stamp()})
    try:r=subprocess.run(argv,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25,
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    except subprocess.TimeoutExpired as error:
        (LEDGER/(label+'.stdout.raw')).write_bytes(error.stdout or b'')
        (LEDGER/(label+'.stderr.raw')).write_bytes(error.stderr or b'')
        raise RuntimeError('E_READONLY_TIMEOUT') from error
    (LEDGER/(label+'.stdout.raw')).write_bytes(r.stdout)
    (LEDGER/(label+'.stderr.raw')).write_bytes(r.stderr)
    save(LEDGER/(label+'-exit.json'),{'returncode':r.returncode,**core.stamp()})
    if r.returncode:raise RuntimeError('E_READONLY_SSH: '+label)
    return json.loads(r.stdout)


def diagnostic(label,binding):
    package={'core':base64.b64encode((HERE/'pilot_supervision_01.py').read_bytes()).decode(),
        'worker':base64.b64encode((HERE/'paired_pilot_remote_01.py').read_bytes()).decode(),
        'diagnostic':DIAGNOSTIC,'binding':binding,'remote':REMOTE}
    bootstrap=("import sys,json,base64,types;p=json.loads(sys.stdin.buffer.readline());"
        "c=types.ModuleType('pilot_supervision_01');sys.modules[c.__name__]=c;"
        "exec(base64.b64decode(p['core']),c.__dict__);"
        "m=types.ModuleType('readonly_worker');exec(base64.b64decode(p['worker']),m.__dict__);"
        "g={'REMOTE':p['remote']};exec(p['diagnostic'],g);"
        "print(json.dumps(g['snapshot'](m,p['binding'])))")
    return capture(label,SSH+['/usr/bin/python3 -B -I -c '+shlex.quote(bootstrap)],core.encoded(package)+b'\n')


def preflight_ok(state,binding):
    model=binding['models']['gemma']
    matches=[x for x in state['tags']['models'] if x.get('name')==model['tag']]
    return (state['version']['version']==binding['version'] and len(matches)==1
        and matches[0]['digest'].removeprefix('sha256:')==model['digest']
        and matches[0]['details']['quantization_level']=='Q4_K_M'
        and not state['ps'].get('models') and not state['runners'] and not state['concurrent']
        and not state['ephemeral_supervisors'] and not state['destination_exists']
        and not state['critical_symlinks'] and not state['lock_path_symlinks']
        and state['lock']['regular'] and not state['lock']['symlink'] and state['lock']['uid']==state['uid']
        and state['resources']['available_bytes']>=4000000000 and state['disk_available_bytes']>=100*1024*1024)


def execute():
    if pilot.git('branch','--show-current').decode().strip()!='codex/tactical-state-contract-v1' or pilot.git('status','--porcelain').strip():
        raise RuntimeError('E_LOCAL_GIT')
    head=pilot.git('rev-parse','HEAD').decode().strip()
    if pilot.git('ls-remote','origin','refs/heads/codex/tactical-state-contract-v1').decode().split()[0]!=head:
        raise RuntimeError('E_NOT_PUBLISHED')
    manifest=read(PREP/'manifest.json');binding=read(PREP/'binding.json')
    assert manifest['authorized'] is True and manifest['max_POST']==1
    assert sha(FROZEN.read_bytes())==EXPECTED==manifest['payload_sha256']
    assert sha((PREP/'binding.json').read_bytes())==manifest['binding_sha256']
    for name,digest in manifest['code_sha256'].items():assert sha((HERE/name).read_bytes())==digest
    known=subprocess.check_output(['ssh-keygen','-F','163.5.26.155','-f',r'C:\Users\giamp\.ssh\known_hosts'])
    fingerprint=subprocess.check_output(['ssh-keygen','-lf','-'],input=known).decode()
    if 'SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks' not in fingerprint:raise RuntimeError('E_HOST_KEY')
    LEDGER.mkdir(exist_ok=False)
    (LEDGER/'.gitattributes').write_bytes(b'* -text\n')
    save(LEDGER/'activity-created.json',{'HEAD':head,'attempt_id':'gemma-mmap-on-02','max_POST':1,
         'manifest_sha256':sha((PREP/'manifest.json').read_bytes()),**core.stamp()})
    error=None;invoked=False;call_start=None
    try:
        before=diagnostic('preflight',binding);save(LEDGER/'preflight.json',before)
        if not preflight_ok(before,binding):raise RuntimeError('E_PREFLIGHT')
        call={'ordinal':1,'case':'V10-02','candidate':'gemma','payload':read(FROZEN),'payload_sha256':EXPECTED}
        directory=LEDGER/'call-01';directory.mkdir(exist_ok=False);save(directory/'request.json',call)
        call_start=time.monotonic()
        save(LEDGER/'invocation-reserved.json',{'max_calls':1,**core.stamp()})
        invoked=True
        final=pilot.one_remote(call,binding,directory,call_start+900)
        save(LEDGER/'worker-result.json',final)
    except BaseException as exc:
        error=repr(exc);save(LEDGER/'execution-error.json',{'error':error,**core.stamp()})
    finally:
        if invoked:
            # Read-only collection, never a second execution or POST. After a
            # local deadline, allow the independently bounded remote cleanup.
            if error and call_start and time.monotonic()-call_start>=900:
                time.sleep(max(0,call_start+935-time.monotonic()))
            try:
                request=pilot.remote_recovery_command('gemma-mmap-on-02-call-01')
                bundle=capture('remote-recovery',request['argv'],request['stdin'])
                core.import_custody(bundle,LEDGER/'remote-custody')
                save(LEDGER/'custody-recovered.json',{'verified':True,**core.stamp()})
            except BaseException as exc:
                save(LEDGER/'recovery-error.json',{'error':repr(exc),**core.stamp()})
        try:
            after=diagnostic('post-stop',binding);save(LEDGER/'post-state.json',after)
        except BaseException as exc:save(LEDGER/'post-state-error.json',{'error':repr(exc),**core.stamp()})
        save(LEDGER/'STOP.json',{'execution_error':error,'no_further_calls':True,
            'status':'ESEGUITO' if invoked else 'BLOCCATO','assessment_pending':True,**core.stamp()})
    print(json.dumps({'execution_returned':True,'error':error,'invoked_once':invoked}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=('prepare','execute'));args=parser.parse_args()
    if args.mode=='prepare':prepare()
    else:execute()
