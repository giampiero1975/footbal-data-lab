"""Local one-shot coordinator for the explicitly authorized synthetic gate.

Never imports the model worker, sends POST, touches a RAG lock or retries run.
Requires this code to be committed, published, and the working tree clean.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import queue
import shlex
import subprocess
import sys
import threading
import time
import pilot_supervision_01 as core

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
PROJECT=REPO/'projects/tactical-engine'
OUT=PROJECT/'evaluation/controller_remote_gate_02'
ATTEMPT='controller-remote-gate-20261119-02'
REMOTE='/home/football/.local/share/football-data-lab/'+ATTEMPT
FILES=('remote_supervision_gate_01.py','remote_gate_synthetic_01.py','pilot_supervision_01.py')
HOST_KEY='SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks'
SSH=['ssh','-F',r'C:\Users\giamp\.ssh\config','-T','-o','BatchMode=yes',
     '-o','ConnectTimeout=10','-o','StrictHostKeyChecking=yes','-o','UpdateHostKeys=no',
     '-o','HostKeyAlgorithms=ssh-ed25519','-o','KexAlgorithms=curve25519-sha256','football-vps']


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(name,value):
    core.exclusive(OUT/name,value)


def git(*args):
    return subprocess.check_output(['git','-C',str(REPO),*args]).decode().strip()


def rpc(operation,package=None):
    # Source in stdin: short argv, no installed application import.
    request={'source':base64.b64encode((HERE/'remote_supervision_gate_01.py').read_bytes()).decode(),
             'operation':operation,'package':package}
    bootstrap=("import sys,json,base64,types;p=json.loads(sys.stdin.buffer.readline());"
        "m=types.ModuleType('gate');exec(base64.b64decode(p['source']),m.__dict__);"
        "r=m.preflight() if p['operation']=='preflight' else m.install(p['package']);"
        "print(m.encoded(r).decode())")
    return capture(operation,SSH+['/usr/bin/python3 -B -I -c '+shlex.quote(bootstrap)],
                   core.encoded(request)+b'\n')


def capture(label,argv,request=None):
    save(label+'-invocation.json',{'argv':argv,'request_sha256':sha(request) if request else None,
                                **core.stamp()})
    try:
        r=subprocess.run(argv,input=request,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25,
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    except subprocess.TimeoutExpired as error:
        (OUT/(label+'.stdout.raw')).write_bytes(error.stdout or b'')
        (OUT/(label+'.stderr.raw')).write_bytes(error.stderr or b'')
        raise RuntimeError('E_DIAGNOSTIC_TRANSPORT_TIMEOUT') from error
    (OUT/(label+'.stdout.raw')).write_bytes(r.stdout)
    (OUT/(label+'.stderr.raw')).write_bytes(r.stderr)
    save(label+'-exit.json',{'returncode':r.returncode,**core.stamp()})
    if r.returncode!=0:raise RuntimeError('E_'+label.upper()+'_SSH')
    return json.loads(r.stdout)


def cut_transport():
    argv=SSH+['exec /usr/bin/python3 -B -I '+shlex.quote(REMOTE+'/remote_supervision_gate_01.py')+' run']
    save('run-reserved.json',{'attempt_id':ATTEMPT,'max_executions':1,'argv':argv,
                            'post_limit':0,**core.stamp()})
    child=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                           bufsize=0,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    save('ssh-started.json',{'pid':child.pid,**core.stamp()})
    inbox=queue.Queue(64)
    def reader(stream,channel):
        while True:
            raw=stream.readline()
            inbox.put((channel,raw,core.stamp()))
            if not raw:return
    threads=[]
    for channel,stream in (('stdout',child.stdout),('stderr',child.stderr)):
        t=threading.Thread(target=reader,args=(stream,channel),daemon=True);t.start();threads.append(t)
    raw={'stdout':bytearray(),'stderr':bytearray()}
    go=False;cut=None;ready_time=None
    stop_at=time.monotonic()+25
    try:
        while time.monotonic()<stop_at:
            try:channel,line,received=inbox.get(timeout=0.1)
            except queue.Empty:
                if child.poll() is not None:raise RuntimeError('E_EARLY_SSH_EXIT')
                continue
            raw[channel].extend(line)
            if channel!='stdout' or not line:continue
            event=json.loads(line)
            if event.get('event')=='ready':
                if go:raise RuntimeError('E_DUPLICATE_READY')
                if event.get('payload_sha256')!=sha((HERE/'remote_gate_synthetic_01.py').read_bytes()):
                    raise RuntimeError('E_READY_IDENTITY')
                # Persist reservation before authorizing the one synthetic child.
                save('GO-reserved.json',{'event':event,'received':received,'max_go':1})
                child.stdin.write(b'GO\n');child.stdin.flush();go=True
                ready_time=time.monotonic()
                save('GO-sent.json',core.stamp())
            elif event.get('event')=='transport_cut_ready':
                cut=dict(event=event,received=received,local=core.stamp())
                save('transport-cut.json',cut)
                child.terminate()  # Only this SSH client; never a remote daemon.
                break
        if cut is None:raise RuntimeError('E_NO_CUT_BARRIER')
    finally:
        if child.poll() is None:child.terminate()
        try:child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            child.kill();child.wait(timeout=2)
        for t in threads:t.join(timeout=0.5)
        while not inbox.empty():
            channel,line,_=inbox.get_nowait();raw[channel].extend(line)
        for channel,value in raw.items():(OUT/('run.'+channel+'.raw')).write_bytes(value)
        save('ssh-exit.json',{'pid':child.pid,'returncode':child.returncode,
                            'intentionally_cut':cut is not None,**core.stamp()})
    # One finite wait, no execution retry. The remote budget is 12+15s.
    remaining=max(0,ready_time+32-time.monotonic())
    time.sleep(remaining)


def analyze(exported):
    recovered=core.import_custody(exported['custody'],OUT/'recovered-custody')
    extras={}
    for name,item in exported['extras'].items():
        if name not in ('code-manifest.json','session-started.json','supervisor-result.json'):
            raise RuntimeError('E_EXTRA_NAME')
        raw=base64.b64decode(item['base64'],validate=True)
        if sha(raw)!=item['sha256']:raise RuntimeError('E_EXTRA_HASH')
        (OUT/('remote-'+name)).write_bytes(raw);extras[name]=json.loads(raw)
    result=extras['supervisor-result.json'];records=recovered['records']
    events=[x['data'] for x in records if x['kind']=='event']
    external=[x['data'] for x in records if x['kind']=='external']
    eof=[x for x in external if x.get('event')=='transport_EOF']
    samples=[x for x in events if x.get('event')=='sample']
    actions=result['actions'];state=exported['state_after']
    bootstrap=[x for x in external if x.get('event')=='custody_ack_before_threads']
    threads=[x for x in external if x.get('event')=='reader_relay_started']
    ready=[x for x in records if x['kind']=='event' and x['data'].get('event')=='ready']
    reserved=[x for x in records if x['kind']=='reserve_before_GO']
    gos=[x for x in records if x['kind']=='GO_sent']
    cut=json.loads((OUT/'transport-cut.json').read_bytes())['event']
    cut_sample=[x for x in records if x['kind']=='event' and x['data'].get('event')=='sample'
                and x['data'].get('synthetic_sequence')==cut.get('durable_sample_sequence')
                and x['data'].get('monotonic')==cut.get('sample_monotonic')]
    checks={
        'writer_initialized':records[0]['kind']=='custody_ready' and records[0]['sequence']==0,
        'custody_before_reader_relay':bool(len(bootstrap)==len(threads)==1
            and bootstrap[0]['ack']['sha256']==records[0]['sha256']
            and records[0]['monotonic']<=bootstrap[0]['monotonic']<=threads[0]['monotonic']
            and bootstrap[0]['relay_initialized'] is False),
        'durable_READY_reservation_GO':bool(len(ready)==len(reserved)==len(gos)==1
            and ready[0]['sequence']<reserved[0]['sequence']<gos[0]['sequence']),
        'cut_barrier_links_durable_sample':len(cut_sample)==1,
        'single_GO':sum(x['kind']=='GO_sent' for x in records)==1,
        'real_transport_EOF':len(eof)==1,
        'samples_contiguous':[x['synthetic_sequence'] for x in samples]==list(range(len(samples))),
        'journal_continues_after_EOF':bool(eof and any(x['monotonic']>eof[0]['monotonic']+1 for x in samples)),
        'relay_blocked_during_control':result['relay_deliberately_blocked'] and not result['relay_close_completed'],
        'absolute_deadline':actions and 0<=actions[0]['monotonic']-result['deadline_monotonic']<=0.5,
        'TERM_KILL':[x['action'] for x in actions]==['TERM','KILL'],
        'grace_15s':len(actions)==2 and 15<=actions[1]['monotonic']-actions[0]['monotonic']<=15.5,
        'native_SIGKILL_exit':result['returncode']==-9 and result['forced_kill'],
        'bounded_cleanup':result['cleanup']['monotonic']<=result['deadline_monotonic']+18,
        'custody_terminal':result['custody_terminal_verified'],
        'children_reaped':not result['cleanup']['child_alive'] and not result['cleanup']['writer_alive'],
        'no_synthetic_remaining':not state['synthetic_processes'],
        'services_preserved':all(x['state']=='active' and x['returncode']==0 for x in state['services']),
        'no_resident_or_runners':state['api_ps'].get('models')==[] and not state['runner_processes'],
        'no_concurrent_tests':not state['concurrent_tests'],
        'ollama_cancel_not_claimed':result['ollama_cancellation_verified'] is False,
    }
    return {'checks':checks,'all_pass':all(checks.values()),'sample_count':len(samples),
            'journal_records':len(records),'chain_sha256':recovered['terminal']['journal_chain_sha256'],
            'custody_bootstrap_evidence':bootstrap,'thread_start_evidence':threads,
            'cut_barrier_journal_sequence':cut_sample[0]['sequence'] if cut_sample else None,
            'supervisor':result,'post_state':state,'post_calls':0,'models_loaded':0}


def execute():
    if git('branch','--show-current')!='codex/tactical-state-contract-v1' or git('status','--porcelain'):
        raise RuntimeError('E_LOCAL_GIT')
    head=git('rev-parse','HEAD')
    if git('ls-remote','origin','refs/heads/codex/tactical-state-contract-v1').split()[0]!=head:
        raise RuntimeError('E_NOT_PUBLISHED')
    known=subprocess.check_output(['ssh-keygen','-F','163.5.26.155','-f',r'C:\Users\giamp\.ssh\known_hosts'])
    fingerprint=subprocess.check_output(['ssh-keygen','-lf','-'],input=known).decode()
    if HOST_KEY not in fingerprint:raise RuntimeError('E_HOST_KEY')
    OUT.mkdir(exist_ok=False)
    (OUT/'.gitattributes').write_bytes(b'* -text\n')
    files={name:{'base64':base64.b64encode((HERE/name).read_bytes()).decode(),
                 'sha256':sha((HERE/name).read_bytes())} for name in FILES}
    save('activity-created.json',{'attempt_id':ATTEMPT,'technical_commit':head,
        'activity':'RD-RAG-V5-QUALITY-FIRST-PAIRED-PILOT-01','code':{n:v['sha256'] for n,v in files.items()},
        'host_fingerprint':HOST_KEY,'post_limit':0,'max_remote_executions':1,**core.stamp()})
    try:
        preflight=rpc('preflight');save('preflight.json',preflight)
        if not preflight['ok']:raise RuntimeError('E_PREFLIGHT')
        installed=rpc('install',{'files':files,'technical_commit':head});save('installed.json',installed)
        for name,item in installed['files'].items():
            if item['sha256']!=files[name]['sha256']:raise RuntimeError('E_TRANSFER_IDENTITY')
        cut_transport()
        exported=capture('recovery',SSH+['exec /usr/bin/python3 -B -I '+
            shlex.quote(REMOTE+'/remote_supervision_gate_01.py')+' export'])
        result=analyze(exported);save('result.json',result)
        save('STOP.json',{'status':'VALIDATO' if result['all_pass'] else 'BLOCCATO',
                         'scope':'remote synthetic only','post_calls':0,**core.stamp()})
        print(json.dumps({'all_pass':result['all_pass'],'checks':result['checks']}),flush=True)
    except BaseException as error:
        save('STOP.json',{'status':'BLOCCATO','error':repr(error),'post_calls':0,**core.stamp()})
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    if not args.execute:raise SystemExit('Explicit --execute required; no dry-run execution.')
    execute()
