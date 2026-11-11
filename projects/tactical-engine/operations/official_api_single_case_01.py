"""One authorized q3_04 call. No retries. Run once; existing evidence dir stops.

Delta justification: remediation A/R1 schema/handoff were not used in runtime-04.
Static review only before execution; this is not a historical test suite.
Remote code is stdin/argv-only, holds an existing read-only lock FD, and is
supervised by GNU timeout as a process group (450s TERM, 15s KILL).
"""
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

ACTIVITY = "RD-RAG-V5-REMEDIATION-A-OFFICIAL-API-SINGLE-CASE-01"
ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "projects/tactical-engine"
OUT = PROJECT / "evaluation/remediation_a_official_api_single_case_01"
BASE = "2b235a6db692bab0ed097482e9fac8cc04a0ca15"
APP_BASE = "cec94e57ce11903460bc9314de2c699aa83b0193"
MODEL_DIGEST = "56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90"

REMOTE = r'''
import base64,datetime,fcntl,hashlib,json,os,stat,subprocess,sys,time,urllib.request
def emit(kind, **fields):
    print(json.dumps(dict(event=kind,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**fields)),flush=True)
def get(path):
    with urllib.request.urlopen('http://127.0.0.1:11434'+path,timeout=10) as response:
        return json.load(response)
try:
    payload_line=sys.stdin.buffer.readline()
    payload=json.loads(payload_line)
    body=json.dumps(payload,ensure_ascii=False).encode('utf-8')
    parent=os.getppid()
    with open('/proc/%d/cmdline'%parent,'rb') as f: supervisor=f.read().split(b'\0')
    # Parent executable and process group bind the deadline to this remote process.
    supervisor=[x.decode() for x in supervisor if x]
    if os.path.basename(supervisor[0])!='timeout' or supervisor[1:4]!=['--signal=TERM','--kill-after=15s','450s']:
        raise RuntimeError('E_SUPERVISOR_ARGV')
    if os.getpgrp()!=parent or os.getpgid(parent)!=parent:
        raise RuntimeError('E_SUPERVISOR_GROUP')
    lock='/home/football/.local/share/football-data-lab/runtime-locks/spatial-v2-extraction-locator.lock'
    current='/'
    for part in lock.strip('/').split('/'):
        current=os.path.join(current,part)
        if stat.S_ISLNK(os.lstat(current).st_mode): raise RuntimeError('E_LOCK_SYMLINK')
    fd=os.open(lock,os.O_RDONLY|os.O_NOFOLLOW)
    info=os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_uid!=os.getuid(): raise RuntimeError('E_LOCK_IDENTITY')
    fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    lock_before=dict(dev=info.st_dev,ino=info.st_ino,uid=info.st_uid,mode=stat.S_IMODE(info.st_mode),size=info.st_size,mtime_ns=info.st_mtime_ns)
    version=get('/api/version'); tags=get('/api/tags'); loaded=get('/api/ps')
    if version.get('version')!='0.40.5': raise RuntimeError('E_VERSION_IDENTITY')
    expected='56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90'
    models=[x for x in tags.get('models',[]) if x.get('name')=='qwen3.5:9b']
    if len(models)!=1 or models[0].get('digest','').removeprefix('sha256:')!=expected:
        raise RuntimeError('E_MODEL_IDENTITY')
    if loaded.get('models')!=[]: raise RuntimeError('E_MODEL_ALREADY_LOADED')
    ps=subprocess.run(['ps','-eo','pid=,ppid=,pgid=,args='],capture_output=True,text=True,check=True)
    concurrent=[]
    for line in ps.stdout.splitlines():
        fields=line.strip().split(None,3)
        if len(fields)<4 or int(fields[2])==os.getpgrp(): continue
        if any(x in fields[3] for x in ['spatial-v2-extraction-locator','official_api_single_case','shadow_nli_spatial_relations_v2_inference']): concurrent.append(line)
    if concurrent: raise RuntimeError('E_CONCURRENT_RUNTIME: '+repr(concurrent))
    emit('ready',version=version,model=models[0],ps=loaded,concurrent=concurrent,
         lock=lock_before,supervisor_argv=supervisor[:4],supervisor_pid=parent,
         remote_pid=os.getpid(),pgid=os.getpgrp(),payload_sha256=hashlib.sha256(body).hexdigest())
    if sys.stdin.buffer.readline()!=b'GO\n': raise RuntimeError('E_NO_LOCAL_COMMIT_TO_SEND')
except Exception as error:
    emit('blocked',error=repr(error)); sys.exit(40)

# Exactly one transport invocation. No redirect handler or retry path.
import http.client
connection=http.client.HTTPConnection('127.0.0.1',11434,timeout=360)
started=time.monotonic()
try:
    emit('post_started',transport_calls=1)
    connection.request('POST','/api/chat',body=body,headers={'Content-Type':'application/json'})
    response=connection.getresponse()
    emit('http_headers',http_status=response.status,headers=response.getheaders())
    chunks=[]
    while True:
        chunk=response.read1(4096)
        if not chunk: break
        chunks.append(chunk)
        emit('http_chunk',body_base64=base64.b64encode(chunk).decode(),bytes=len(chunk))
    raw=b''.join(chunks)
    emit('http_response',http_status=response.status,headers=response.getheaders(),
         body_base64=base64.b64encode(raw).decode(),body_sha256=hashlib.sha256(raw).hexdigest(),
         bytes=len(raw),elapsed_seconds=time.monotonic()-started)
except Exception as error:
    emit('transport_error',error=repr(error),elapsed_seconds=time.monotonic()-started)
finally:
    connection.close()
    after=os.fstat(fd)
    lock_after=dict(dev=after.st_dev,ino=after.st_ino,uid=after.st_uid,mode=stat.S_IMODE(after.st_mode),size=after.st_size,mtime_ns=after.st_mtime_ns)
    emit('finished',lock_after=lock_after,lock_metadata_preserved=lock_after==lock_before)
    os.close(fd)
'''


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def save_bytes(name, data):
    with (OUT / name).open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def save(name, data):
    save_bytes(name, (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode())


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def main():
    if OUT.exists():
        raise SystemExit('STOP: evidence directory exists; never repeat this activity')
    if git('branch', '--show-current').decode().strip() != 'codex/tactical-state-contract-v1':
        raise SystemExit('STOP: branch mismatch')
    if git('status', '--porcelain').strip():
        raise SystemExit('STOP: working tree not clean')
    head = git('rev-parse', 'HEAD').decode().strip()
    git('merge-base', '--is-ancestor', BASE, head)
    app_paths = sorted((PROJECT / 'scripts').glob('*.py'))
    identities = {}
    # The complete Python application directory remains at the decision baseline.
    for path in app_paths:
        relative = path.relative_to(ROOT).as_posix()
        original = git('show', APP_BASE + ':' + relative)
        if path.read_bytes() != original:
            raise SystemExit('STOP: application divergence ' + relative)
        identities[relative] = dict(sha256=hashlib.sha256(original).hexdigest(),
                                    blob=git('rev-parse', head + ':' + relative).decode().strip())
    OUT.mkdir()
    save('identity.json', dict(activity=ACTIVITY,head=head,application_base=APP_BASE,
         application_files=identities,driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         driver_blob=git('rev-parse',head+':'+Path(__file__).relative_to(ROOT).as_posix()).decode().strip(),
         remote_program_sha256=hashlib.sha256(REMOTE.encode()).hexdigest(),utc=utc()))
    save_bytes('remote-program.txt', REMOTE.encode())
    input_path = PROJECT / 'evaluation/runtime04_execution_01/artifacts/input.json'
    original_input = input_path.read_bytes()
    assert original_input == git('show', APP_BASE + ':' + input_path.relative_to(ROOT).as_posix())
    case = json.loads(original_input)
    save_bytes('input.json', original_input)
    save('ledger-created.json',dict(activity=ACTIVITY,utc=utc(),post_count=0,
                                  no_retry=True,case_id=case['case_id']))
    sys.path.insert(0, str(PROJECT / 'scripts'))
    import shadow_nli_spatial_relations_v2_inference as caller
    import v5_tactical_semantic_support_s2_spatial_v2_extraction as extraction
    state = dict(transport_calls=0,post_started_events=0,commit_to_send=False,
                 http_status=None,ssh_exit=None,blocked=None)
    raw_response = None

    def transport(url, payload, timeout):
        nonlocal raw_response
        assert state['transport_calls'] == 0
        state['transport_calls'] = 1
        assert url == 'http://127.0.0.1:11434' and timeout == 360
        assert payload['model'] == 'qwen3.5:9b'
        assert payload['options'] == dict(temperature=0,num_predict=2048,num_ctx=4096)
        assert payload['think'] is False and payload['stream'] is False
        assert payload['format'] == extraction.EXTRACTION_SCHEMA
        assert len(payload['messages']) == 2 and all('gold' not in m['content'].lower() for m in payload['messages'])
        body=json.dumps(payload,ensure_ascii=False).encode()
        save_bytes('request_payload.json',body)
        save('schema.json',payload['format'])
        program=base64.b64encode(REMOTE.encode()).decode()
        remote_command="timeout --signal=TERM --kill-after=15s 450s /usr/bin/python3 -B -I -c " + shlex.quote("import base64;exec(base64.b64decode('"+program+"'))")
        argv=['ssh','-T','-o','BatchMode=yes','-o','ConnectTimeout=10','-o','StrictHostKeyChecking=yes',
              '-o','UpdateHostKeys=no','-o','KexAlgorithms=curve25519-sha256',
              '-o','HostKeyAlgorithms=ssh-ed25519','football-vps',remote_command]
        save('invocation.json',dict(argv=argv,http_timeout=360,supervisor=450,kill_after=15))
        events=[]
        with (OUT/'ssh-stdout.jsonl').open('xb') as stdout, (OUT/'ssh-stderr.txt').open('xb') as stderr:
            process=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=stderr)
            process.stdin.write(body+b'\n');process.stdin.flush()
            for line in process.stdout:
                stdout.write(line);stdout.flush();os.fsync(stdout.fileno())
                event=json.loads(line);events.append(event)
                print(json.dumps({k:v for k,v in event.items() if k not in ['body_base64','headers','model']}),flush=True)
                if event['event']=='ready':
                    assert not state['commit_to_send']
                    assert event['payload_sha256']==hashlib.sha256(body).hexdigest()
                    save('ledger-commit-to-send.json',dict(utc=utc(),activity=ACTIVITY,
                         send_authorized_once=True,post_count_if_interrupted='unknown_0_or_1',
                         payload_sha256=event['payload_sha256'],remote_ready=event))
                    state['commit_to_send']=True
                    process.stdin.write(b'GO\n');process.stdin.flush();process.stdin.close()
                elif event['event']=='http_headers':
                    save('http-headers.json',event)
                    save_bytes('response-body.bin',b'')
                elif event['event']=='http_chunk':
                    with (OUT/'response-body.bin').open('ab') as body_file:
                        body_file.write(base64.b64decode(event['body_base64'],validate=True))
                        body_file.flush();os.fsync(body_file.fileno())
                elif event['event']=='post_started':
                    state['post_started_events']+=1
                    save('ledger-post-started.json',event)
                elif event['event']=='blocked': state['blocked']=event['error']
                elif event['event']=='http_response':
                    state['http_status']=event['http_status']
                    raw=base64.b64decode(event['body_base64'],validate=True)
                    assert hashlib.sha256(raw).hexdigest()==event['body_sha256']
                    save_bytes('raw_response.json',raw)
                    if event['http_status']==200:raw_response=json.loads(raw)
            state['ssh_exit']=process.wait()
        save('remote-events.json',events)
        if raw_response is None:
            raise ConnectionError('No complete successful HTTP response; no retry')
        return raw_response

    try:
        result=caller.judge_pair(case['claim'],case['evidence'],transport=transport,
             extraction_locator=True,q3_04_timeout_360=True,max_tokens=2048)
        save('result.json',result)
        parsed=None
        if raw_response and isinstance(raw_response.get('message',{}).get('content'),str):
            try:parsed=json.loads(raw_response['message']['content'])
            except ValueError:pass
        if parsed is not None:save('extraction.json',parsed)
        shape=extraction.extraction_shape_errors(parsed) if parsed is not None else None
        witness=result.get('witness');validation=result.get('validation')
        observed=witness.get('label') if result.get('evaluation_status')=='evaluated' and witness else None
        summary=dict(activity=ACTIVITY,utc=utc(),**state,
            completed_generations=int(bool(raw_response and raw_response.get('done') is True and raw_response.get('done_reason')=='stop')),
            done_reason=raw_response.get('done_reason') if raw_response else None,
            prompt_eval_count=raw_response.get('prompt_eval_count') if raw_response else None,
            eval_count=raw_response.get('eval_count') if raw_response else None,
            shape_errors=shape,reason_codes=result.get('reason_codes'),details=result.get('details'),
            witness_present=witness is not None,validation_present=validation is not None,
            proposed_label=parsed.get('label') if isinstance(parsed,dict) else None,
            observed_label=observed,gold_label=case['gold_label'],
            semantic_match=(observed==case['gold_label']) if observed else None,
            promotion_authorized=False)
        save('summary.json',summary)
        print(json.dumps(summary),flush=True)
    except Exception as error:
        save('local-error.json',dict(error=repr(error),utc=utc(),**state))
        raise
    finally:
        inventory=[dict(path=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(OUT.iterdir()) if p.is_file()]
        save('manifest.json',dict(activity=ACTIVITY,utc=utc(),files=inventory))


if __name__ == '__main__':
    sys.dont_write_bytecode=True
    main()
