"""One differential bootstrap check; synthetic local processes only.

Positive custody, failed-custody negative branch, and active-thread rejection
are dependencies of the same startup check, not a replay of historical fixtures.
"""
import argparse
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import sys
import threading
import time
import pilot_supervision_01 as core

HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'docs/writer-bootstrap-order-local-01'


def child(marker):
    Path(marker).write_bytes(b'synthetic child launched\n')
    print(json.dumps({'event':'ready','payload_sha256':'bootstrap-check-01'}),flush=True)
    if sys.stdin.buffer.readline()!=b'GO\n':return 40
    print(json.dumps({'event':'finished','ok':True,'synthetic':True}),flush=True)
    return 0


def check():
    OUT.mkdir(exist_ok=True)
    (OUT/'.gitattributes').write_bytes(b'* -text\n')
    run=OUT/'run-01';run.mkdir(exist_ok=False)
    authorized=threading.Event();reader_started=threading.Event();receipts=[];seen=[]
    fd_read,fd_write=os.pipe()
    reader=None;emitter=None
    marker=run/'child-started.txt'
    command=[sys.executable,'-B',str(Path(__file__).resolve()),'--child',str(marker)]
    instance=core.Supervisor(run/'custody',command,attempt_id='bootstrap-local-01',
        expected_payload='bootstrap-check-01',timeout=10,authorize=authorized.is_set)

    def custody_ready(supervisor,ack):
        nonlocal reader,emitter
        assert not reader_started.is_set() and not marker.exists()
        record=json.loads((supervisor.root/'journal.ndjson').read_bytes().splitlines()[0])
        checkpoint=json.loads((supervisor.root/'checkpoint-000000.json').read_bytes())
        assert record['kind']=='custody_ready' and record['sha256']==ack['sha256']==checkpoint['sha256']
        receipts.append(dict(ack,reader_started_before_ack=False))
        def stdin_reader():
            reader_started.set()
            with os.fdopen(fd_read,'rb') as f:
                if f.readline()==b'LOCAL_AUTHORIZATION\n':authorized.set()
        reader=threading.Thread(target=stdin_reader);reader.start()
        assert reader_started.wait(1)
        # Same one-shot bootstrap used for post-cleanup remote receipts:
        # it must not fork the interpreter with this blocked reader active.
        core.durable_file(run/'threaded-receipt.json',core.encoded(ack)+b'\n')
        assert json.loads((run/'threaded-receipt.json').read_bytes())==ack
        def relay(event):
            seen.append(event)
            if event.get('event')=='ready':
                # READY is relayed only after its journal record is fsynced/acked.
                lines=(supervisor.root/'journal.ndjson').read_bytes().splitlines()
                assert any(json.loads(x).get('data',{}).get('event')=='ready' for x in lines)
                os.write(fd_write,b'LOCAL_AUTHORIZATION\n')
        emitter=core.NonBlockingEmitter(relay,supervisor.cancel)
        supervisor.relay=emitter

    instance.on_custody_ready=custody_ready
    try:
        positive=instance.run()
        assert positive['ok'] and positive['GO_sent'] and positive['custody_terminal_verified']
        recovered=core.recover(instance.root)
        records=recovered['records'];kinds=[x['kind'] for x in records]
        assert kinds[0]=='custody_ready' and kinds[-1]=='terminal'
        assert kinds.count('reserve_before_GO')==kinds.count('GO_sent')==1
        assert kinds.index('reserve_before_GO')<kinds.index('GO_sent')
        assert any(x.get('event')=='ready' for x in seen)
        assert list(instance.root.glob('checkpoint-*.json'))
        assert not positive['cleanup']['child_alive'] and not positive['cleanup']['writer_alive']
    finally:
        os.close(fd_write)
        if reader:reader.join(timeout=1)
        if emitter:assert emitter.close()
    assert reader and not reader.is_alive()

    # Same bootstrap, writer fails before ack0: no callback, no child, no GO.
    callback=[]
    negative_marker=run/'forbidden-child.txt'
    failed=core.Supervisor(run/'unready-custody',command[:-1]+[str(negative_marker)],
        attempt_id='bootstrap-local-unready',expected_payload='bootstrap-check-01',
        writer_fail_at=0,on_custody_ready=lambda *_:callback.append(True),timeout=10)
    try:
        failed.run()
    except RuntimeError as error:
        negative_error=str(error)
        assert negative_error.startswith(('E_CUSTODY_BOOTSTRAP_IO','E_CUSTODY_BOOTSTRAP_EXIT'))
    else:raise AssertionError('unready writer accepted')
    assert not callback and not negative_marker.exists()
    assert not (failed.root/'terminal.json').exists()

    # Guard is portable Python logic; native fork is exercised only on Linux.
    release=threading.Event();active=threading.Event()
    def already_running():active.set();release.wait(2)
    background=threading.Thread(target=already_running);background.start();assert active.wait(1)
    try:
        try:core.require_single_threaded_fork()
        except RuntimeError as error:assert str(error)=='E_CUSTODY_FORK_THREADS'
        else:raise AssertionError('active thread not rejected')
        if os.name=='posix':
            forbidden=core.Supervisor(run/'forbidden-fork',command,
                attempt_id='forbidden',expected_payload='bootstrap-check-01')
            try:forbidden.run()
            except RuntimeError as error:assert str(error)=='E_CUSTODY_FORK_THREADS'
            else:raise AssertionError('fork with active thread accepted')
            assert not forbidden.root.exists()
    finally:
        release.set();background.join(timeout=1)
    assert not background.is_alive() and not mp.active_children()
    evidence={'result':'PASS','scope':'one local bootstrap differential check',
        'platform':sys.platform,'python':sys.version,'Linux_native_tested':sys.platform.startswith('linux'),
        'custody_receipts':receipts,'positive':positive,'unready_error':negative_error,
        'unready_child_launched':False,'unready_GO_sent':False,'active_thread_guard':'PASS',
        'residual_children':[],'SSH':0,'POST':0,'models':0,
        'code_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                       for name in ('pilot_supervision_01.py',Path(__file__).name)}}
    core.exclusive(run/'result.json',evidence)
    print(json.dumps({'result':'PASS','platform':sys.platform,'Linux_native_tested':evidence['Linux_native_tested']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--child');args=parser.parse_args()
    if args.child:raise SystemExit(child(args.child))
    check()
