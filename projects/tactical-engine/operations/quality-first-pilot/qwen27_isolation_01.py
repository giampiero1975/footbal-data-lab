"""Linux entry point for a separately authorized, detached Qwen27 attempt."""

import hashlib
import json
import os
from pathlib import Path
import re
import socket
import stat
import subprocess
import sys
import threading
import time


STATE = Path('/var/lib/football-qwen27-isolation')
CGROUP = Path('/sys/fs/cgroup')
SYSTEMCTL = '/usr/bin/systemctl'
SYSTEMD_RUN = '/usr/bin/systemd-run'
TAG = 'qwen3.8:27b'
DIGEST = 'aaee06c39dcf2437cde036998d960e1fc1494b8191be7cc9657d01e509097813'
PAYLOAD_HASH = '331530c85dac2e0030e5c8d3489cee9c4ea0ee5e53486667e95b00096304451e'
NS = 1_000_000_000
GRACE = 15 * NS
BUDGET = 900 * NS
SERVICES = ('ollama.service', 'football-rag-api.service')
DAEMON_USER = 'football-qwen27'


def json_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_record(path, data, *, readable=False):
    # A partial file is ambiguous and deliberately prevents automatic reopening.
    with path.open('xb') as handle:
        handle.write(json_bytes(data) + b'\n')
        handle.flush()
        if readable:
            os.chmod(path, 0o444)
        os.fsync(handle.fileno())
    sync_dir(path.parent)


class AttemptStore:
    """All mutations run under the existing pilot lock, held by the supervisor."""

    def __init__(self, root):
        self.root = root
        self.marker = root / 'open.json'

    def reserve(self, binding):
        attempt = binding['attempt_id']
        require(re.fullmatch(r'qwen27-mmap-on-[0-9]{2,8}', attempt), 'E_ATTEMPT_ID')
        require(not os.path.lexists(self.marker), 'E_ISOLATED_ATTEMPT_OPEN')
        directory = self.root / attempt
        directory.mkdir(mode=0o700)
        sync_dir(self.root)
        write_record(self.marker, binding, readable=True)
        return directory

    def finish(self, directory, binding, receipt):
        write_record(directory / 'stop-receipt.json', receipt)
        if receipt['quiet'] is True:
            require(json.loads(self.marker.read_bytes()) == binding, 'E_ATTEMPT_MARKER_CHANGED')
            self.marker.unlink()
            sync_dir(self.root)


def read_cgroup_events(data):
    values = [line.split() for line in data.splitlines() if line.startswith('populated ')]
    require(values in ([['populated', '0']], [['populated', '1']]), 'E_CGROUP_EVENTS')
    return values[0][1] == '1'


def escalation_at(stop_ns, deadline_ns):
    return min(stop_ns, deadline_ns) + GRACE


def validate_request(plan):
    attempt, request = plan['attempt_id'], plan['request']
    require(re.fullmatch(r'qwen27-mmap-on-[0-9]{2,8}', attempt), 'E_ATTEMPT_ID')
    require(plan['authorized'] is True and plan['max_posts'] == 1
            and plan['kill_authorized'] is True, 'E_SEPARATE_AUTHORIZATION')
    call, binding = request['call'], request['binding']
    payload = call['payload']
    require(set(request) == {'call', 'binding'} and call['candidate'] == 'qwen'
            and call['case'] == 'V10-02' and call['ordinal'] == 2
            and payload['model'] == TAG and payload['options']['use_mmap'] is True
            and call['payload_sha256'] == PAYLOAD_HASH
            and hashlib.sha256(json_bytes(payload)).hexdigest() == PAYLOAD_HASH,
            'E_QWEN_PAYLOAD')
    require(binding['version'] == '0.40.5' and set(binding['models']) == {'qwen'}
            and binding['models']['qwen']['tag'] == TAG
            and binding['models']['qwen']['digest'] == DIGEST, 'E_MODEL_BINDING')
    return attempt, request


def trusted_path(path):
    require(path.is_absolute() and path == path.resolve(strict=True), 'E_UNTRUSTED_PATH')
    for part in (path, *path.parents):
        info = part.stat()
        require(info.st_uid == 0 and not info.st_mode & 0o022, 'E_UNTRUSTED_OWNER')


def invocation(value):
    return bool(re.fullmatch(r'[0-9a-f]{32}', value) and int(value, 16))


def unit_info(unit):
    fields = ('Id', 'InvocationID', 'ControlGroup', 'MainPID', 'LoadState', 'ActiveState',
              'Restart', 'BindsTo', 'KillMode', 'PrivateNetwork')
    result = subprocess.run([SYSTEMCTL, 'show', unit, *(f'--property={field}' for field in fields)],
                            capture_output=True, text=True, timeout=2)
    info = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    if info.get('Id') != unit or info.get('LoadState') != 'not-found':
        result.check_returncode()
    return info


def namespace(pid):
    info = os.stat(f'/proc/{pid}/ns/net')
    return [info.st_dev, info.st_ino]


def process_identity(pid):
    fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
    return {'pid': pid, 'parent_pid': int(fields[1]), 'start_ticks': int(fields[19]),
            'cgroup': Path(f'/proc/{pid}/cgroup').read_text().strip()}


def same_cgroup(info, unit):
    return (info.get('Id') == unit and info.get('ControlGroup') == '/system.slice/' + unit
            and invocation(info.get('InvocationID', '')))


class Target:
    """Open descriptors anchor escalation to the originally bound cgroup inode."""

    def __init__(self, unit, info, supervisor_unit, net):
        require(same_cgroup(info, unit) and info['ActiveState'] == 'active'
                and info['Restart'] == 'no' and info['KillMode'] == 'control-group'
                and supervisor_unit in info['BindsTo'].split(), 'E_TARGET_UNIT')
        self.unit = unit
        self.invocation = info['InvocationID']
        self.path = CGROUP / info['ControlGroup'].lstrip('/')
        self.fd = os.open(self.path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        self.files = {}
        try:
            for name, mode in (('cgroup.events', os.O_RDONLY), ('cgroup.procs', os.O_RDONLY),
                               ('cgroup.kill', os.O_WRONLY)):
                self.files[name] = os.open(name, mode | os.O_NOFOLLOW, dir_fd=self.fd)
            info_stat = os.fstat(self.fd)
            self.inode = [info_stat.st_dev, info_stat.st_ino]
            pid = int(info['MainPID'])
            require(pid > 1, 'E_TARGET_MAINPID')
            self.process = process_identity(pid)
            require(pid in self.members() and namespace(pid) == net
                    and self.process['cgroup'] == '0::' + info['ControlGroup'], 'E_TARGET_MEMBERSHIP')
        except BaseException:
            self.close()
            raise

    def close(self):
        for fd in self.files.values():
            os.close(fd)
        os.close(self.fd)

    def members(self):
        return [int(line) for line in os.pread(self.files['cgroup.procs'], 16384, 0).splitlines()]

    def populated(self):
        value = os.pread(self.files['cgroup.events'], 4096, 0).decode()
        return read_cgroup_events(value)

    def term(self):
        require(os.path.samestat(self.path.stat(), os.fstat(self.fd)), 'E_TARGET_REPLACED')
        info = unit_info(self.unit)
        require(same_cgroup(info, self.unit) and self.invocation == info['InvocationID'],
                'E_TARGET_REBOUND')
        return subprocess.Popen([SYSTEMCTL, '--no-block', 'stop', self.unit],
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)

    def kill(self):
        require(os.write(self.files['cgroup.kill'], b'1') == 1, 'E_CGROUP_KILL_WRITE')

    def proof(self):
        # Once systemd removes the directory, the open descriptors may be offline.
        # Require manager corroboration for the reserved unit in that case.
        info = unit_info(self.unit)
        inactive = info.get('ActiveState') in ('inactive', 'failed')
        same_or_gone = info.get('InvocationID', '') in ('', self.invocation)
        if not (inactive and same_or_gone and info.get('Id') == self.unit):
            return None
        try:
            current = self.path.stat()
        except FileNotFoundError:
            return {'unit': info, 'cgroup_removed': True, 'anchored_inode': self.inode}
        if os.path.samestat(current, os.fstat(self.fd)) and not self.populated() and not self.members():
            return {'unit': info, 'populated': 0, 'members': [], 'anchored_inode': self.inode}
        return None


def service_snapshot():
    # Filesystem system/user buses. No requests against the production HTTP API.
    commands = ([SYSTEMCTL, 'is-active', SERVICES[0]],
                [SYSTEMCTL, '--user', '--machine=football@.host', 'is-active', SERVICES[1]])
    snapshot = {}
    for name, command in zip(SERVICES, commands):
        result = subprocess.run(command, capture_output=True, text=True, timeout=2)
        snapshot[name] = {'exit': result.returncode, 'state': result.stdout.strip()}
    return snapshot


def services_active(snapshot):
    return set(snapshot) == set(SERVICES) and all(
        item == {'exit': 0, 'state': 'active'} for item in snapshot.values())


class StopControl:
    def __init__(self, deadline, stop_writer):
        self.deadline = deadline
        self.writer = stop_writer
        self.trigger = None
        self.lock = threading.Lock()
        self.ready = threading.Event()
        self.actions = []
        self.sample = None
        self.empty_ns = None

    def stop(self, reason):
        with self.lock:
            if self.trigger is None:
                self.trigger = {'reason': reason, 'monotonic_ns': time.monotonic_ns()}
                os.close(self.writer)  # EOF first, independent of custody and systemctl.

    def allow_go(self):
        return self.ready.is_set() and self.trigger is None and time.monotonic_ns() < self.deadline

    def watch(self, target, read_resources, pressure_step, note):
        previous = None
        persistent = 0.0
        next_sample = 0
        attempted_term = False
        term = None
        while True:
            now = time.monotonic_ns()
            if now >= self.deadline:
                self.stop('E_DEADLINE')
            if self.trigger is not None:
                limit = escalation_at(self.trigger['monotonic_ns'], self.deadline)
                if not attempted_term:
                    # Manager identity checks may block briefly. Keep escalation on this thread.
                    attempted_term = True
                    term = threading.Thread(target=self.request_term, args=(target,), daemon=True)
                    term.start()
                try:
                    if not target.populated():
                        self.empty_ns = time.monotonic_ns()
                        break
                except (OSError, RuntimeError):
                    pass  # Disappearance is corroborated during final classification.
                if now >= limit:
                    action = {'action': 'KILL', 'monotonic_ns': time.monotonic_ns(), 'limit_ns': limit}
                    try:
                        target.kill()
                        action['written'] = True
                    except (OSError, RuntimeError) as error:
                        action['error'] = repr(error)
                    self.actions.append(action)
                    break
            if now >= next_sample:
                try:
                    value = read_resources()
                    reason = 'E_MEMORY_RESERVE' if value['available_bytes'] < 4000000000 else None
                    if previous is not None:
                        persistent, pressure_reason, rate = pressure_step(
                            previous, value, (now - next_sample + NS) / NS,
                            persistent, os.sysconf('SC_PAGE_SIZE'))
                        reason = reason or pressure_reason
                        value['paging_bytes_per_second'] = rate
                        value['paging_persistent_seconds'] = persistent
                    self.sample = dict(value, monotonic_ns=now)
                    if reason:
                        self.stop(reason)
                    try:
                        self.sample['members'] = target.members()
                    except OSError:
                        self.sample['members'] = None
                    note({'event': 'isolated_pressure', **self.sample})
                    previous = value
                    self.ready.set()
                except Exception as error:
                    self.stop('E_RESOURCE_COUNTER')
                    self.actions.append({'action': 'RESOURCE_ERROR', 'error': repr(error),
                                         'monotonic_ns': time.monotonic_ns()})
                next_sample = now + NS
            delay = min(0.02, max(0, (limit - time.monotonic_ns()) / NS)) if attempted_term else 0.02
            time.sleep(delay)
        if term is not None:
            term.join(timeout=2.5)

    def request_term(self, target):
        action = {'action': 'TERM', 'monotonic_ns': time.monotonic_ns()}
        try:
            command = target.term()
            action['dispatched_monotonic_ns'] = time.monotonic_ns()
            action['exit'] = command.wait(timeout=2)
        except (OSError, RuntimeError, subprocess.SubprocessError) as error:
            action['error'] = repr(error)
        self.actions.append(action)


def run_unit(arguments):
    subprocess.run([SYSTEMD_RUN, '--quiet', *arguments], check=True,
                   stdin=subprocess.DEVNULL, timeout=8)


def daemon_arguments(unit, supervisor, pid, ollama, model_store):
    scratch = unit.removesuffix('.service')
    return [f'--unit={unit}', '--slice=system.slice', '--service-type=exec',
            f'--property=User={DAEMON_USER}', '--property=Restart=no',
            f'--property=BindsTo={supervisor}', f'--property=After={supervisor}',
            f'--property=NetworkNamespacePath=/proc/{pid}/ns/net',
            '--property=KillMode=control-group', '--property=TimeoutStopSec=15s',
            '--property=SendSIGKILL=yes', '--property=NoNewPrivileges=yes',
            '--property=CapabilityBoundingSet=', '--property=ProtectControlGroups=yes',
            '--property=Delegate=no',
            '--property=RestrictNamespaces=yes', '--property=ProtectSystem=strict',
            '--property=PrivateTmp=yes', '--property=UMask=0077',
            f'--property=RuntimeDirectory={scratch}', '--property=RuntimeDirectoryMode=0700',
            f'--property=ReadOnlyPaths={model_store}', f'--setenv=OLLAMA_MODELS={model_store}',
            f'--setenv=HOME=/run/{scratch}', '--setenv=OLLAMA_HOST=127.0.0.1:11434',
            '--setenv=OLLAMA_NO_CLOUD=1', '--', str(ollama), 'serve']


def start_watchdog(prefix, binding_path, deadline):
    # PID 1 owns this timer. The target name is reserved once and never reused.
    for action, when in (('term', deadline), ('kill', deadline + GRACE)):
        unit = f'{prefix}-deadline-{action}'
        run_unit([f'--unit={unit}', f'--on-boot={when // 1000}us',
                  '--timer-property=AccuracySec=1us', '--timer-property=RandomizedDelaySec=0',
                  '--timer-property=WakeSystem=no', '--timer-property=RemainAfterElapse=no',
                  '--', '/usr/bin/python3', '-I', '-B', str(Path(__file__).absolute()),
                  '--deadline', action, str(binding_path)])
        require(unit_info(unit + '.timer').get('ActiveState') == 'active', 'E_DEADLINE_TIMER')


def deadline_stop(path, action):
    require(sys.platform == 'linux' and os.getuid() == 0, 'E_LINUX_SYSTEM_MANAGER_REQUIRED')
    trusted_path(Path(__file__).absolute())
    trusted_path(STATE)
    try:
        trusted_path(path)
    except FileNotFoundError:
        return  # No READY was possible without this durable binding.
    binding = json.loads(path.read_bytes())
    attempt = binding['attempt_id']
    require(re.fullmatch(r'qwen27-mmap-on-[0-9]{2,8}', attempt)
            and path == STATE / attempt / 'binding.json', 'E_ATTEMPT_ID')
    marker_path = STATE / 'open.json'
    try:
        marker = json.loads(marker_path.read_bytes())
    except FileNotFoundError:
        return  # Already settled with a durable receipt.
    if marker.get('attempt_id') != attempt:
        return
    require(all(binding.get(field) == value for field, value in marker.items())
            and Path('/proc/sys/kernel/random/boot_id').read_text().strip() == binding['boot_id'],
            'E_WATCHDOG_BINDING')
    # OnBootSec is configured to microsecond precision. Never start the deadline early.
    when = binding['deadline_ns'] + (GRACE if action == 'kill' else 0)
    remaining = when - time.monotonic_ns()
    if remaining > 0:
        require(remaining <= NS, 'E_WATCHDOG_BEFORE_DEADLINE')
        time.sleep(remaining / NS)
    unit = 'football-' + attempt + '-ollama.service'
    require(unit == binding['target_unit'], 'E_TARGET_UNIT')
    info = unit_info(unit)
    if info.get('ActiveState') in ('inactive', 'failed'):
        return
    if action == 'term' and info.get('ActiveState') == 'deactivating':
        return
    require(same_cgroup(info, unit) and info['InvocationID'] == binding['target_invocation'],
            'E_TARGET_REBOUND')
    group = CGROUP / info['ControlGroup'].lstrip('/')
    group_fd = os.open(group, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        group_stat = os.fstat(group_fd)
        require(str(group) == binding['target_cgroup'] and
                [group_stat.st_dev, group_stat.st_ino] == binding['target_cgroup_inode'],
                'E_TARGET_REPLACED')
        evidence = {'attempt_id': attempt, 'action': action.upper(),
                    'monotonic_ns': time.monotonic_ns(), 'limit_ns': when}
        try:
            if action == 'kill':
                fd = os.open('cgroup.kill', os.O_WRONLY | os.O_NOFOLLOW, dir_fd=group_fd)
                try:
                    require(os.write(fd, b'1') == 1, 'E_CGROUP_KILL_WRITE')
                    evidence['written'] = True
                finally:
                    os.close(fd)
            else:
                subprocess.run([SYSTEMCTL, '--no-block', 'stop', unit], check=True, timeout=2)
                evidence['queued'] = True
        except (OSError, RuntimeError, subprocess.SubprocessError) as error:
            evidence['error'] = repr(error)
            raise
        finally:
            write_record(path.parent / f'deadline-{action}.json', evidence)
    finally:
        os.close(group_fd)


def load_plan(path):
    trusted_path(path)
    plan = json.loads(path.read_bytes())
    attempt, request = validate_request(plan)
    ollama, model_store = Path(plan['ollama_binary']), Path(plan['model_store'])
    for value in (ollama, model_store):
        require(value.is_absolute() and value.resolve(strict=True) == value
                and re.fullmatch(r'/[A-Za-z0-9_./-]+', str(value)), 'E_RUNTIME_PATH')
    trusted_path(ollama)
    require(hashlib.sha256(ollama.read_bytes()).hexdigest() == plan['ollama_sha256'],
            'E_OLLAMA_BINARY')
    require(model_store.is_dir() and (model_store / 'blobs').is_dir()
            and (model_store / 'manifests').is_dir(), 'E_MODEL_STORE')
    return attempt, request, ollama, model_store, plan['ollama_sha256']


def check_model_access(store, account):
    manifest_path = store / 'manifests/registry.ollama.ai/library/qwen3.8/27b'
    require(not manifest_path.is_symlink() and manifest_path.is_file(), 'E_MODEL_MANIFEST_PATH')
    raw = manifest_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == DIGEST, 'E_MODEL_MANIFEST_DIGEST')
    manifest = json.loads(raw)
    for item in [manifest['config'], *manifest['layers']]:
        digest = item['digest']
        require(re.fullmatch(r'sha256:[0-9a-f]{64}', digest), 'E_MODEL_BLOB_DIGEST')
        blob = store / 'blobs' / digest.replace(':', '-')
        require(not blob.is_symlink() and blob.is_file() and blob.stat().st_size == item['size'],
                'E_MODEL_BLOB_IDENTITY')
        check_read_as(account, blob)
    check_read_as(account, manifest_path)


def check_read_as(account, path):
    subprocess.run(['/usr/bin/setpriv', f'--reuid={account.pw_uid}', f'--regid={account.pw_gid}',
                    '--init-groups', '--no-new-privs', '/usr/bin/test', '-r', str(path)],
                   check=True, stdin=subprocess.DEVNULL, timeout=2)


def pressure_inputs(counters):
    mem, swap = counters('/proc/meminfo'), counters('/proc/vmstat')
    return {'available_bytes': mem['MemAvailable'], 'swap_in': swap['pswpin'],
            'swap_out': swap['pswpout'], 'swap_used_bytes': mem['SwapTotal'] - mem['SwapFree']}


def run(path):
    require(sys.platform == 'linux' and os.getuid() == 0, 'E_LINUX_SYSTEM_MANAGER_REQUIRED')
    import fcntl
    import pwd

    here = Path(__file__).absolute().parent
    source_hashes = {}
    for name in (Path(__file__).name, 'pilot_supervision_01.py', 'paired_pilot_remote_01.py'):
        trusted_path(here / name)
        source_hashes[name] = hashlib.sha256((here / name).read_bytes()).hexdigest()
    os.umask(0o077)
    sys.path.insert(0, str(here))
    import pilot_supervision_01 as core
    import paired_pilot_remote_01 as worker

    attempt, request, ollama, model_store, ollama_hash = load_plan(path)
    daemon = pwd.getpwnam(DAEMON_USER)
    user = pwd.getpwnam('football')
    require(daemon.pw_uid not in (0, user.pw_uid, pwd.getpwnam('ollama').pw_uid), 'E_DAEMON_UID')
    check_model_access(model_store, daemon)
    prefix = 'football-' + attempt
    supervisor_unit, target_unit = prefix + '-supervisor.service', prefix + '-ollama.service'
    manager = unit_info(supervisor_unit)
    pid = os.getpid()
    net = namespace(pid)
    identity = process_identity(pid)
    require(same_cgroup(manager, supervisor_unit) and int(manager['MainPID']) == pid
            and manager['PrivateNetwork'] == 'yes' and manager['Restart'] == 'no'
            and identity['cgroup'] == '0::' + manager['ControlGroup']
            and net != namespace(1) and {name for _, name in socket.if_nameindex()} == {'lo'}
            and (CGROUP / 'cgroup.controllers').is_file(), 'E_SUPERVISOR_CONFINEMENT')
    require(unit_info(target_unit).get('LoadState') == 'not-found', 'E_TARGET_ALREADY_EXISTS')
    initial_services = service_snapshot()
    require(services_active(initial_services), 'E_REQUIRED_SERVICE')
    read_resources = lambda: pressure_inputs(worker.counters)
    require(read_resources()['available_bytes'] >= 4000000000, 'E_MEMORY_BEFORE_START')
    trusted_path(STATE)
    require(STATE.is_dir() and STATE.stat().st_mode & 0o005 == 0o005, 'E_ATTEMPT_STORE_MODE')
    require(Path(worker.LOCK).resolve(strict=True) == Path(worker.LOCK), 'E_LOCK_SYMLINK')
    uid, gid = user.pw_uid, user.pw_gid
    stop_read, stop_write = os.pipe()
    lock_fd = os.open(worker.LOCK, os.O_RDONLY | os.O_NOFOLLOW)
    target = None
    watcher = None
    services_thread = None
    probe_done = threading.Event()
    control = None
    result = None
    receipt = None
    try:
        lock_stat = os.fstat(lock_fd)
        require(stat.S_ISREG(lock_stat.st_mode) and lock_stat.st_uid == uid, 'E_LOCK_IDENTITY')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        started = time.monotonic_ns()
        deadline = started + BUDGET
        control = StopControl(deadline, stop_write)
        marker = {'attempt_id': attempt, 'boot_id': boot, 'payload_sha256': PAYLOAD_HASH,
                  'model_digest': DIGEST, 'target_unit': target_unit, 'deadline_ns': deadline,
                  'started_ns': started, 'network_namespace': net, 'supervisor': identity,
                  'supervisor_unit': supervisor_unit, 'supervisor_invocation': manager['InvocationID'],
                  'lock': [lock_stat.st_dev, lock_stat.st_ino], 'services_before': initial_services,
                  'source_sha256': source_hashes}
        store = AttemptStore(STATE)
        directory = store.reserve(marker)

        def launch(instance, _ack):
            nonlocal target, watcher, services_thread
            start_watchdog(prefix, directory / 'binding.json', deadline)
            require(time.monotonic_ns() < deadline, 'E_DEADLINE_BEFORE_DAEMON')
            run_unit(daemon_arguments(target_unit, supervisor_unit, pid, ollama, model_store))
            target = Target(target_unit, unit_info(target_unit), supervisor_unit, net)
            watcher = threading.Thread(target=control.watch,
                                       args=(target, read_resources, worker.pressure_step, instance.note), daemon=True)
            watcher.start()
            binding = {**marker, 'target_invocation': target.invocation, 'target_cgroup': str(target.path),
                       'target_cgroup_inode': target.inode, 'target_main': target.process,
                       'ollama_binary_sha256': ollama_hash}
            write_record(directory / 'binding.json', binding)
            instance.note({'event': 'isolated_binding', **binding})

            # Type=exec confirms execve, which can precede Ollama binding its socket.
            listener_deadline = min(deadline, time.monotonic_ns() + 10 * NS)
            while True:
                require(control.trigger is None and time.monotonic_ns() < listener_deadline,
                        'E_ISOLATED_LISTENER')
                try:
                    with socket.create_connection(('127.0.0.1', 11434), timeout=0.2):
                        break
                except ConnectionRefusedError:
                    time.sleep(0.05)
            require(namespace(int(unit_info(target_unit)['MainPID'])) == net,
                    'E_ISOLATED_LISTENER_NAMESPACE')

            def probe_services():
                while not probe_done.wait(5):
                    try:
                        snapshot = service_snapshot()
                        instance.note({'event': 'isolated_services', 'services': snapshot})
                        if services_active(snapshot):
                            continue
                    except (OSError, subprocess.SubprocessError) as error:
                        instance.note({'event': 'isolated_services_error', 'error': repr(error)})
                    control.stop('E_REQUIRED_SERVICE')
                    instance.cancel('E_REQUIRED_SERVICE')
                    return

            services_thread = threading.Thread(target=probe_services, daemon=True)
            services_thread.start()

        isolated_request = {**request, 'isolation': {'supervisor_pid': pid, 'network_namespace': net,
                            'lock_fd': lock_fd, 'stop_fd': stop_read, 'deadline_ns': deadline,
                            'attempt_id': attempt}}
        worker_entry = f'import sys;sys.path.insert(0,{str(here)!r});from paired_pilot_remote_01 import main;sys.exit(main())'
        command = ['/usr/bin/setpriv', f'--reuid={uid}', f'--regid={gid}', '--init-groups',
                   '--no-new-privs', '/usr/bin/python3', '-I', '-B', '-c', worker_entry]
        supervisor = core.Supervisor(directory / 'custody', command, attempt_id=attempt,
                                     expected_payload=PAYLOAD_HASH, initial=core.encoded(isolated_request) + b'\n',
                                     pass_fds=(lock_fd, stop_read), absolute_deadline=deadline / NS,
                                     authorize=control.allow_go, on_custody_ready=launch,
                                     on_stop=control.stop,
                                     writer_close_fds=(lock_fd, stop_read, stop_write))
        failure = None
        try:
            result = supervisor.run()
        except Exception as error:
            failure = repr(error)
        finally:
            completed = bool(result and result['ok'] and result['terminal_event'].get('ok') is True)
            control.stop('WORKER_FINISHED' if completed else 'E_WORKER_OR_CUSTODY')
            if watcher:
                watcher.join(timeout=18)
            probe_done.set()
            if services_thread:
                services_thread.join(timeout=5)

        proof = None
        diagnostics = {}
        if watcher and not watcher.is_alive():
            try:
                proof = target.proof()
                diagnostics = {'memory': read_resources(), 'services': service_snapshot()}
            except (OSError, RuntimeError, subprocess.SubprocessError) as error:
                diagnostics['error'] = repr(error)
        recovery_ok = (diagnostics.get('memory', {}).get('available_bytes', 0) >= 4000000000
                       and services_active(diagnostics.get('services', {})))
        boot_unchanged = Path('/proc/sys/kernel/random/boot_id').read_text().strip() == boot
        worker_reaped = bool(result and result['cleanup']['child_alive'] is False
                             and result['cleanup']['writer_alive'] is False)
        custody_verified = bool(result and result['custody_terminal_verified'])
        lock_unchanged = os.path.samestat(os.lstat(worker.LOCK), lock_stat)
        quiet = bool(proof and worker_reaped and recovery_ok and boot_unchanged
                     and custody_verified and lock_unchanged)
        receipt = {'attempt_id': attempt, 'binding': marker, 'trigger': control.trigger,
                   'actions': control.actions, 'empty_monotonic_ns': control.empty_ns,
                   'last_sample': control.sample, 'cgroup_proof': proof, 'diagnostics': diagnostics,
                   'quiet': quiet, 'worker_finished_naturally': completed,
                   'custody_terminal_verified': custody_verified,
                   'remote_cancellation_verified': False, 'failure': failure,
                   'recorded_monotonic_ns': time.monotonic_ns()}
        eligible = (quiet and completed and control.trigger['reason'] == 'WORKER_FINISHED'
                    and receipt['custody_terminal_verified'] and not any(a['action'] == 'KILL' for a in control.actions)
                    and control.empty_ns is not None
                    and control.empty_ns <= escalation_at(control.trigger['monotonic_ns'], deadline))
        receipt['status'] = 'ESEGUITO' if eligible else 'BLOCCATO'
        store.finish(directory, marker, receipt)
        return 0 if eligible else 41
    finally:
        if control is None:
            os.close(stop_write)
        else:
            control.stop('E_SUPERVISOR_EXIT')
        if target and (watcher is None or not watcher.is_alive()):
            target.close()
        os.close(stop_read)
        os.close(lock_fd)


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--deadline' and sys.argv[2] in ('term', 'kill'):
        deadline_stop(Path(sys.argv[3]), sys.argv[2])
    elif len(sys.argv) == 2:
        sys.exit(run(Path(sys.argv[1])))
    else:
        sys.exit('Usage: qwen27_isolation_01.py /absolute/root-owned/authorization.json')
