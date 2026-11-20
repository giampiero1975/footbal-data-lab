"""Run once on Linux with an inert daemon and the actual isolation primitives."""
import base64
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import sys
import time
import zlib


ATTEMPT = 'qwen27-mmap-on-26112002'
PREFIX = 'football-' + ATTEMPT
SUPERVISOR = PREFIX + '-supervisor.service'
TARGET = PREFIX + '-ollama.service'
WATCHDOGS = [f'{PREFIX}-deadline-{action}.{kind}'
             for action in ('term', 'kill') for kind in ('timer', 'service')]
ROOT = Path('/run/football-qwen27-linux-gate-02')
MODEL_STORE = Path('/var/lib/football-qwen27-isolation/models-qwen27')
NS = 1_000_000_000
BUDGET = 8 * NS
GRACE = 2 * NS
PYTHON = '/usr/bin/python3'

PAYLOAD = """
import os, signal, socket, sys, time
from pathlib import Path
observed = Path(sys.argv[1])
def term(*_):
    with (observed / 'term').open('x') as handle:
        handle.write(str(time.monotonic_ns()))
signal.signal(signal.SIGTERM, term)
(observed / 'ready').write_text(str(os.getpid()) + ':' + ','.join(n for _, n in socket.if_nameindex()))
while True:
    time.sleep(1)
"""


def wait_for(check, until):
    while time.monotonic_ns() < until:
        result = check()
        if result:
            return result
        time.sleep(0.025)
    raise RuntimeError('E_GATE_OBSERVATION_TIMEOUT')


def remote(source):
    import pwd

    evidence = {'attempt': ATTEMPT, 'deadline_seconds': 8, 'grace_seconds': 2,
                'operational_deadline_seconds': 900, 'operational_grace_seconds': 15,
                'source_sha256': hashlib.sha256(source).hexdigest(), 'posts': 0,
                'models_loaded': 0, 'events': {}}
    event = evidence['events']
    scope = {'__name__': 'preflight', '__file__': str(ROOT / 'qwen27_isolation_01.py')}
    exec(compile(source, scope['__file__'], 'exec'), scope)
    info, require = scope['unit_info'], scope['require']
    before = scope['service_snapshot']()
    evidence['services_before'] = before
    evidence['systemd'] = subprocess.check_output(['/usr/bin/systemctl', '--version'], text=True).splitlines()[0]
    evidence['kernel'] = os.uname().release
    account = pwd.getpwnam(scope['DAEMON_USER'])
    require(account.pw_uid == 997 and scope['services_active'](before), 'E_PREFLIGHT_SERVICES')
    require(Path('/sys/fs/cgroup/cgroup.controllers').is_file()
            and Path('/sys/fs/cgroup/system.slice/cgroup.kill').is_file(), 'E_CGROUP_V2')
    require(not os.path.lexists(scope['STATE'] / 'open.json'), 'E_OPERATIONAL_ATTEMPT_OPEN')
    scope['check_model_access'](MODEL_STORE, account)
    names = [TARGET, SUPERVISOR, *WATCHDOGS]
    require(all(info(unit).get('LoadState') == 'not-found' for unit in names), 'E_UNIT_COLLISION')
    ROOT.mkdir(mode=0o755)
    sentinel = target = None
    try:
        # Only the fixture path and grace differ in the copied operational module.
        fixture_source = source.replace(
            b"STATE = Path('/var/lib/football-qwen27-isolation')",
            f"STATE = Path({str(ROOT)!r})".encode(), 1).replace(
            b'GRACE = 15 * NS', b'GRACE = 2 * NS', 1)
        require(fixture_source != source and scope['GRACE'] == 15 * NS, 'E_FIXTURE_SUBSTITUTION')
        fixture_file = Path(scope['__file__'])
        fixture_file.write_bytes(fixture_source)
        evidence['watchdog_fixture_sha256'] = hashlib.sha256(fixture_source).hexdigest()
        exec(compile(fixture_source, str(fixture_file), 'exec'), scope)
        require(scope['STATE'] == ROOT and scope['GRACE'] == GRACE
                and scope['BUDGET'] == 900 * NS, 'E_FIXTURE_CONFIGURATION')
        observed = ROOT / 'observed'
        observed.mkdir(mode=0o700)
        os.chown(observed, account.pw_uid, account.pw_gid)
        sentinel = subprocess.Popen(['/usr/bin/sleep', '45'], stdin=subprocess.DEVNULL)
        evidence['sentinel_before'] = scope['process_identity'](sentinel.pid)
        evidence['sentinel_namespace'] = scope['namespace'](sentinel.pid)

        scope['run_unit']([f'--unit={SUPERVISOR}', '--slice=system.slice', '--service-type=exec',
                           '--property=PrivateNetwork=yes', '--property=Restart=no',
                           '--', '/usr/bin/sleep', '45'])
        supervisor = info(SUPERVISOR)
        pid = int(supervisor['MainPID'])
        net = scope['namespace'](pid)
        require(scope['same_cgroup'](supervisor, SUPERVISOR)
                and supervisor['PrivateNetwork'] == 'yes'
                and net != scope['namespace'](1)
                and net != evidence['sentinel_namespace'], 'E_SUPERVISOR_NAMESPACE')
        evidence['supervisor'] = supervisor
        evidence['namespace'] = net
        args = scope['daemon_arguments'](TARGET, SUPERVISOR, pid, PYTHON, MODEL_STORE)
        args.insert(args.index('--'), f'--property=ReadWritePaths={observed}')
        args = args[:-1]  # Replace the Ollama serve argument with the synthetic body.
        scope['run_unit']([*args, '-I', '-B', '-c', PAYLOAD, str(observed)])
        ready = observed / 'ready'
        wait_for(lambda: ready.exists() and ready.stat().st_size, time.monotonic_ns() + 2 * NS)
        target = scope['Target'](TARGET, info(TARGET), SUPERVISOR, net)
        require(ready.read_text() == f"{target.process['pid']}:lo", 'E_SYNTHETIC_NAMESPACE')
        require(evidence['sentinel_before']['cgroup'] != target.process['cgroup'], 'E_SENTINEL_CGROUP')
        deadline = time.monotonic_ns() + BUDGET
        marker = {'attempt_id': ATTEMPT, 'deadline_ns': deadline, 'target_unit': TARGET,
                  'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
        store = scope['AttemptStore'](ROOT)
        directory = store.reserve(marker)
        binding_path = directory / 'binding.json'
        binding = {**marker, 'target_invocation': target.invocation,
                   'target_cgroup': str(target.path), 'target_cgroup_inode': target.inode,
                   'target_main': target.process}
        scope['write_record'](binding_path, binding)
        evidence['binding'] = binding
        scope['start_watchdog'](PREFIX, binding_path, deadline)

        term_path = observed / 'term'
        wait_for(lambda: term_path.exists() and term_path.stat().st_size, deadline + GRACE)
        event['term_at_ns'] = int(term_path.read_text())
        require(deadline <= event['term_at_ns'] < deadline + GRACE, 'E_TERM_TIMING')
        event['supervisor_interrupted_at_ns'] = time.monotonic_ns()
        supervisor_fd = os.pidfd_open(pid)
        try:
            require(info(SUPERVISOR)['InvocationID'] == supervisor['InvocationID']
                    and int(info(SUPERVISOR)['MainPID']) == pid, 'E_SUPERVISOR_IDENTITY')
            signal.pidfd_send_signal(supervisor_fd, signal.SIGKILL)
        finally:
            os.close(supervisor_fd)
        wait_for(lambda: info(SUPERVISOR).get('ActiveState') in ('inactive', 'failed'),
                 deadline + GRACE)
        require(json.loads(store.marker.read_bytes()) == marker, 'E_MARKER_LOST')
        try:
            store.reserve({'attempt_id': 'qwen27-mmap-on-26112003'})
        except RuntimeError as error:
            require(str(error) == 'E_ISOLATED_ATTEMPT_OPEN', 'E_BARRIER')
        else:
            raise RuntimeError('E_BARRIER_REFUSED_TO_BLOCK')
        evidence['barrier_blocked_with_supervisor_gone'] = True

        kill_path = directory / 'deadline-kill.json'
        wait_for(lambda: kill_path.exists() and kill_path.stat().st_size, deadline + GRACE + 3 * NS)
        kill = json.loads(kill_path.read_bytes())
        term = json.loads((directory / 'deadline-term.json').read_bytes())
        require(term.get('queued') is True and kill.get('written') is True
                and deadline + GRACE <= kill['monotonic_ns'] <= deadline + GRACE + 3 * NS,
                'E_WATCHDOG_EVIDENCE')
        event['term_watchdog'] = term
        event['kill_watchdog'] = kill
        quiet = wait_for(target.proof, deadline + GRACE + 5 * NS)
        event['quiet_at_ns'] = time.monotonic_ns()
        evidence['quiet'] = quiet
        require(sentinel.poll() is None
                and scope['process_identity'](sentinel.pid) == evidence['sentinel_before'],
                'E_SENTINEL_CHANGED')
        evidence['sentinel_survived'] = True
        store.finish(directory, marker, {'quiet': True, 'proof': quiet})
        require(not os.path.lexists(store.marker), 'E_BARRIER_NOT_SETTLED')
        evidence['barrier_cleared_after_quiet'] = True
    except Exception as error:
        evidence['error'] = f'{type(error).__name__}: {error}'
    finally:
        if target is not None:
            target.close()
        if sentinel is not None:
            sentinel.terminate()
            sentinel.wait(timeout=3)
        systemctl = scope['SYSTEMCTL']
        subprocess.run([systemctl, 'stop', *WATCHDOGS, TARGET, SUPERVISOR],
                       capture_output=True, timeout=19)
        subprocess.run([systemctl, 'reset-failed', *WATCHDOGS, TARGET, SUPERVISOR],
                       capture_output=True, timeout=3)
        evidence['units_remaining'] = [name for name in names if info(name).get('LoadState') != 'not-found']
        for entry in ROOT.rglob('*.json'):
            evidence.setdefault('remote_inventory', {})[str(entry.relative_to(ROOT))] = hashlib.sha256(entry.read_bytes()).hexdigest()
        shutil.rmtree(ROOT)
        evidence['scratch_removed'] = not ROOT.exists()
        evidence['services_after'] = scope['service_snapshot']()
        evidence['services_unchanged'] = evidence['services_after'] == before
        evidence['validated'] = ('error' not in evidence and not evidence['units_remaining']
                                 and evidence['scratch_removed'] and evidence['services_unchanged'])
        print(json.dumps(evidence, sort_keys=True))
    return 0 if evidence['validated'] else 41


def main():
    script = Path(__file__).resolve()
    source = script.with_name('qwen27_isolation_01.py').read_bytes()
    root = script.parents[2]
    result_path = root / 'docs/qwen27-isolation-linux-gate-02.json'
    if result_path.exists():
        raise RuntimeError('E_GATE_ALREADY_RUN')
    home = Path.home() / '.ssh'
    hosts = subprocess.check_output(['ssh-keygen', '-F', '163.5.26.155', '-f', str(home / 'known_hosts')])
    fingerprint = subprocess.check_output(['ssh-keygen', '-lf', '-'], input=hosts).decode()
    if 'SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks' not in fingerprint:
        raise RuntimeError('E_HOST_KEY')
    password = sys.stdin.buffer.readline(1024).rstrip(bytes([13, 10]))
    if not password or len(password) >= 1023:
        raise RuntimeError('E_CREDENTIAL_INPUT')
    def pack(raw):
        return base64.b64encode(zlib.compress(raw)).decode()
    loader = ('import sys,base64,zlib;'
              'a,b=(zlib.decompress(base64.b64decode(v,validate=True)) for v in sys.argv[1:]);'
              'g={"__name__":"gate"};exec(compile(a,"<gate>","exec"),g);sys.exit(g["remote"](b))')
    command = shlex.join(['/usr/bin/sudo', '-S', '-p', '', '--', PYTHON, '-I', '-B', '-c',
                         loader, pack(script.read_bytes()), pack(source)])
    ssh = ['ssh', '-F', str(home / 'config'), '-T', '-o', 'BatchMode=yes', '-o',
           'ConnectTimeout=10', '-o', 'StrictHostKeyChecking=yes', '-o', 'UpdateHostKeys=no',
           '-o', 'HostKeyAlgorithms=ssh-ed25519', '-o', 'KexAlgorithms=curve25519-sha256',
           'football-vps', command]
    result = subprocess.run(ssh, input=password + bytes([10]), capture_output=True, timeout=55)
    del password
    evidence = json.loads(result.stdout) if result.stdout else {
        'attempt': ATTEMPT, 'validated': False, 'error': result.stderr.decode(errors='replace')}
    evidence['exit_code'] = result.returncode
    evidence['git_commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    evidence['gate_source_sha256'] = hashlib.sha256(script.read_bytes()).hexdigest()
    with result_path.open('x', encoding='utf-8', newline='\n') as article:
        json.dump(evidence, article, indent=2, sort_keys=True)
        article.write('\n')
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
