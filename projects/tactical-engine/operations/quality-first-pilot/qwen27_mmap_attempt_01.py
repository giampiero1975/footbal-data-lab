"""One authorized V10-02 mmap attempt; the detached Linux supervisor owns GO."""
import base64
import copy
import hashlib
import json
import lzma
from pathlib import Path
import shlex
import subprocess
import sys

import qwen27_isolation_01 as isolation


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATTEMPT = 'qwen27-mmap-on-26112004'
SOURCES = ('qwen27_isolation_01.py', 'pilot_supervision_01.py', 'paired_pilot_remote_01.py')
LEDGER = PROJECT / 'evaluation/quality_first_qwen27_mmap_on_01'
REFERENCE = PROJECT / 'docs/quality-first-pilot-authorized-readiness-01/execution_binding_03.json'

REMOTE = r"""
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import stat
import subprocess
import sys
import tempfile

def provision_catalog(store, scope):
    require = scope['require']
    production = Path('/usr/share/ollama/.ollama/models')
    v2 = Path('manifests-v2/ollama.com/library/qwen3.8/27b')
    variant = scope['DIGEST']
    catalog = 'e118e4d12a705129abfcd3076c3a420108987e7150c037a92515d3e0091e0eb1'
    root = store / 'manifests-v2'
    scope['trusted_path'](store)
    scope['trusted_path'](store / 'blobs')
    require(not os.path.lexists(root), 'E_V2_CATALOG_ALREADY_PRESENT')

    def verified(path, digest):
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size <= 65536, 'E_V2_CATALOG_FILE')
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == digest, 'E_V2_CATALOG_DIGEST')
        return raw

    source_index = production / v2
    catalog_blob = 'sha256-' + catalog
    require(source_index.is_symlink()
            and source_index.resolve(strict=True) == production / 'blobs' / catalog_blob,
            'E_V2_CATALOG_LINK')
    index = verified(production / 'blobs' / catalog_blob, catalog)
    require([item.get('digest') for item in json.loads(index)['manifests']
             if item.get('runner') == 'llamacpp' and item.get('format') == 'gguf']
            == ['sha256:' + variant], 'E_V2_GGUF_VARIANT')
    objects = {}
    for digest in (variant, catalog):
        name = 'sha256-' + digest
        objects[name] = verified(production / 'blobs' / name, digest)
        require(not os.path.lexists(store / 'blobs' / name), 'E_V2_METADATA_ALREADY_PRESENT')

    staged = Path(tempfile.mkdtemp(prefix='.manifests-v2-', dir=store))
    written = []
    try:
        leaf = staged.joinpath(*v2.parts[1:])
        leaf.parent.mkdir(parents=True)
        for directory in staged.rglob('*'):
            if directory.is_dir():
                directory.chmod(0o755)
        for name, raw in objects.items():
            path = store / 'blobs' / name
            with path.open('xb') as handle:
                written.append(path)
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
            path.chmod(0o644)
        leaf.symlink_to(os.path.relpath(store / 'blobs' / catalog_blob, leaf.parent))
        require(leaf.resolve(strict=True) == store / 'blobs' / catalog_blob,
                'E_V2_ISOLATED_LINK')
        staged.chmod(0o755)
        staged.rename(root)
    except Exception:
        for path in written:
            path.unlink()
        shutil.rmtree(staged)
        raise
    scope['sync_dir'](store / 'blobs')
    scope['sync_dir'](store)
    return {'path': str(store / v2), 'sha256': catalog, 'gguf_manifest_sha256': variant}

def collect(plan, code):
    scope = {'__name__': 'preflight'}
    exec(compile(code['qwen27_isolation_01.py'], '<isolation>', 'exec'), scope)
    state = scope['STATE']
    attempt, _ = scope['validate_request'](plan)
    prefix = 'football-' + attempt
    supervisor = prefix + '-supervisor.service'
    directory = state / attempt
    launcher = state / ('launcher-' + attempt)
    require = scope['require']
    data = {'attempt_id': attempt, 'sha256': sha, 'payload_sha256': scope['PAYLOAD_HASH'],
            'authorized_posts': 1, 'invoked': False}
    try:
        scope['trusted_path'](state)
        require(not any(os.path.lexists(p) for p in (state / 'open.json', directory, launcher)),
                'E_ATTEMPT_ALREADY_PRESENT')
        units = [supervisor, prefix + '-ollama.service']
        units += [prefix + '-deadline-' + action + '.' + kind
                  for action in ('term', 'kill') for kind in ('timer', 'service')]
        require(all(scope['unit_info'](name).get('LoadState') == 'not-found' for name in units),
                'E_UNIT_COLLISION')
        require(Path('/sys/fs/cgroup/system.slice/cgroup.kill').is_file()
                and Path('/sys/fs/cgroup/cgroup.controllers').is_file(), 'E_CGROUP_V2')

        def services():
            summary = {}
            for service, manager in (
                ('ollama.service', []),
                ('football-rag-api.service', ['--user', '--machine=football@.host']),
            ):
                text = subprocess.check_output(
                    ['/usr/bin/systemctl', *manager, 'show', service, '-p', 'ActiveState',
                     '-p', 'MainPID', '-p', 'InvocationID'], text=True, timeout=3)
                item = dict(line.split('=', 1) for line in text.splitlines())
                require(item['ActiveState'] == 'active' and int(item['MainPID']) > 0
                        and scope['invocation'](item['InvocationID']), 'E_PRODUCTION_SERVICE')
                summary[service] = item
            return summary

        data['services_before'] = services()
        mem = next(line for line in Path('/proc/meminfo').read_text().splitlines()
                   if line.startswith('MemAvailable:'))
        data['available_before_bytes'] = int(mem.split()[1]) * 1024
        require(data['available_before_bytes'] >= 4000000000, 'E_MEMORY_BEFORE_START')
        daemon = pwd.getpwnam(scope['DAEMON_USER'])
        require(daemon.pw_uid == 997 and daemon.pw_gid == 987, 'E_DAEMON_IDENTITY')
        model_store = Path(plan['model_store'])
        scope['check_model_access'](model_store, daemon)
        if plan.get('provision_catalog_v2') is True:
            require(attempt == 'qwen27-mmap-on-26112006'
                    and model_store == state / 'models-qwen27', 'E_CATALOG_SCOPE')
            data['catalog_v2'] = provision_catalog(model_store, scope)
        pid = int(data['services_before']['ollama.service']['MainPID'])
        binary = Path(f'/proc/{pid}/exe').resolve(strict=True)
        scope['trusted_path'](binary)
        require(binary.name == 'ollama' and re.fullmatch(r'/[A-Za-z0-9_./-]+', str(binary)),
                'E_OLLAMA_BINARY')
        plan.update(ollama_binary=str(binary), ollama_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
        data['ollama_binary'] = plan['ollama_binary']
        data['ollama_sha256'] = plan['ollama_sha256']
        launcher.mkdir(mode=0o755)
        for name, source in code.items():
            path = launcher / name
            with path.open('xb') as handle:
                handle.write(source)
                handle.flush()
                os.fsync(handle.fileno())
            path.chmod(0o644)
        authorization = launcher / 'authorization.json'
        scope['write_record'](authorization, plan)
        authorization.chmod(0o600)
        scope['sync_dir'](state)
        scope['load_plan'](authorization)
        data['invoked'] = True
        result = subprocess.run([scope['SYSTEMD_RUN'], '--quiet', '--wait', '--collect',
                                 f'--unit={supervisor}', '--slice=system.slice', '--service-type=exec',
                                 '--property=PrivateNetwork=yes', '--property=Restart=no',
                                 '--property=RuntimeMaxSec=950s', '--', '/usr/bin/python3', '-I', '-B',
                                 str(launcher / 'qwen27_isolation_01.py'), str(authorization)],
                                capture_output=True, text=True, timeout=970)
        data['supervisor_exit'] = result.returncode
        data['transport_message'] = result.stderr[-3000:]
        data['services_after'] = services()
        data['services_unchanged'] = data['services_before'] == data['services_after']
        receipt_path = directory / 'stop-receipt.json'
        data['marker_open'] = os.path.lexists(state / 'open.json')
        if receipt_path.is_file():
            data['receipt'] = json.loads(receipt_path.read_bytes())
        custody = directory / 'custody'
        terminal_path = custody / 'terminal.json'
        if terminal_path.is_file():
            sys.path.insert(0, str(launcher))
            from pilot_supervision_01 import recover
            recovered = recover(custody)
            terminal = recovered['terminal']
            events = [json.loads(line) for line in (custody / 'stdout.raw').read_bytes().splitlines()]
            data['custody'] = {'verified': True, 'GO_sent': terminal['GO_sent'],
                               'reason': terminal.get('reason'),
                               'post_started_events': sum(event['event'] == 'post_started' for event in events),
                               'terminal_event': terminal.get('terminal_event') or {},
                               'journal_chain_sha256': terminal['journal_chain_sha256'],
                               'journal_sha256': terminal['journal.ndjson_sha256']}
            data['custody']['terminal_event'].pop('thinking', None)
            metadata = data['custody']['terminal_event'].get('final_metadata')
            if metadata and 'message' in metadata:
                metadata.pop('message')
            pressure = [row['data'] for row in recovered['records']
                        if isinstance(row.get('data'), dict)
                        and row['data'].get('event') == 'isolated_pressure']
            if pressure:
                data['min_available_bytes'] = min(x['available_bytes'] for x in pressure)
        if result.returncode or not data.get('receipt'):
            journal = subprocess.run(['/usr/bin/journalctl', '--no-pager', '-o', 'cat',
                                      '-u', supervisor, '-u', prefix + '-ollama.service', '-n', '24'],
                                     capture_output=True, text=True, timeout=4)
            data['diagnostic_tail'] = journal.stdout[-8500:]
    except Exception as exc:
        data['error'] = f'{type(exc).__name__}: {exc}'
    data['eligible'] = (data.get('supervisor_exit') == 0 and data.get('services_unchanged') is True
                        and data.get('marker_open') is False and 'error' not in data
                        and data.get('receipt', {}).get('status') == 'ESEGUITO'
                        and data.get('receipt', {}).get('quiet') is True
                        and data.get('custody', {}).get('post_started_events') == 1
                        and data.get('custody', {}).get('terminal_event', {}).get('ok') is True)
    return data

def main(encoded):
    envelope = json.loads(encoded)
    code = {name: data.encode() for name, data in envelope['code'].items()}
    global sha
    sha = {name: hashlib.sha256(data).hexdigest() for name, data in code.items()}
    if sha != envelope['sha256'] or set(code) != {'qwen27_isolation_01.py', 'pilot_supervision_01.py',
                                                  'paired_pilot_remote_01.py'}:
        raise RuntimeError('E_SOURCE_IDENTITY')
    result = collect(envelope['plan'], code)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['eligible'] else 41
"""


def plan(attempt=ATTEMPT, *, provision_catalog_v2=False):
    manifest = json.loads((HERE / 'prepared/pilot_manifest_01.json').read_bytes())
    frozen = next(c for c in manifest['calls'] if c['candidate'] == 'qwen' and c['case'] == 'V10-02')
    historical = PROJECT / 'evaluation/quality_first_qwen27_single_case_01/call-02/request.json'
    if json.loads(historical.read_bytes())['payload'] != frozen['payload']:
        raise RuntimeError('E_HISTORIC_PAYLOAD')
    call = copy.deepcopy(frozen)
    call['payload']['options']['use_mmap'] = True
    call['payload_sha256'] = hashlib.sha256(isolation.json_bytes(call['payload'])).hexdigest()
    binding = json.loads(REFERENCE.read_bytes())
    binding['models'] = {'qwen': binding['models']['qwen']}
    request = {'call': call, 'binding': binding}
    value = {'attempt_id': attempt, 'request': request, 'authorized': True, 'max_posts': 1,
             'kill_authorized': True, 'model_store': '/var/lib/football-qwen27-isolation/models-qwen27'}
    if provision_catalog_v2:
        value['provision_catalog_v2'] = True
    isolation.validate_request(value)
    return value


def command(value):
    sources = {name: (HERE / name).read_bytes() for name in SOURCES}
    envelope = {'plan': value, 'code': {n: b.decode() for n, b in sources.items()},
                'sha256': {n: hashlib.sha256(b).hexdigest() for n, b in sources.items()}}
    def encode(data):
        return base64.b64encode(lzma.compress(data)).decode()
    loader = ('import base64,lzma,sys;'
              'src=lzma.decompress(base64.b64decode(sys.argv[1],validate=True));'
              'p=lzma.decompress(base64.b64decode(sys.stdin.buffer.readline(131072).strip(),validate=True));'
              'g={"__name__":"authorization"};exec(compile(src,"<authorization>","exec"),g);'
              'sys.exit(g["main"](p))')
    remote = shlex.join(['/usr/bin/sudo', '-k', '-S', '-p', '', '--', '/usr/bin/python3', '-I', '-B',
                         '-c', loader, encode(REMOTE.encode())])
    body = encode(isolation.json_bytes(envelope)).encode() + bytes([10])
    if len(body) >= 131072:
        raise RuntimeError('E_TRANSPORT_BODY_SIZE')
    return remote, body, envelope['sha256']


def write(path, data):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write('\n')


def main(attempt=ATTEMPT, ledger=LEDGER, *, provision_catalog_v2=False):
    value = plan(attempt, provision_catalog_v2=provision_catalog_v2)
    remote, body, hashes = command(value)
    home = Path.home() / '.ssh'
    known = subprocess.check_output(['ssh-keygen', '-F', '163.5.26.155', '-f', str(home / 'known_hosts')])
    host = subprocess.check_output(['ssh-keygen', '-lf', '-'], input=known).decode()
    if 'SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks' not in host:
        raise RuntimeError('E_HOST_KEY')
    password = sys.stdin.buffer.readline(1024).rstrip(bytes([13, 10]))
    if not password or len(password) >= 1023:
        raise RuntimeError('E_CREDENTIAL_INPUT')
    ledger.mkdir()
    write(ledger / 'authorization.json', value)
    write(ledger / 'invocation.json', {'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                                                                       text=True).strip(),
                                      'sha256': hashes, 'max_ssh_invocations': 1})
    args = ['ssh', '-F', str(home / 'config'), '-T', '-o', 'BatchMode=yes',
            '-o', 'ConnectTimeout=10', '-o', 'StrictHostKeyChecking=yes',
            '-o', 'UpdateHostKeys=no', '-o', 'HostKeyAlgorithms=ssh-ed25519',
            '-o', 'KexAlgorithms=curve25519-sha256', 'football-vps', remote]
    print('Starting the authorized, single Qwen27 mmap attempt.', flush=True)
    try:
        result = subprocess.run(args, input=password + bytes([10]) + body, capture_output=True, timeout=990)
        evidence = json.loads(result.stdout) if result.stdout else {'error': 'E_REMOTE_NO_REPORT'}
        evidence['ssh_exit'] = result.returncode
        if 'sha256' in evidence and evidence['sha256'] != hashes:
            raise RuntimeError('E_SOURCE_IDENTITY')
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as error:
        evidence = {'error': f'{type(error).__name__}: {error}', 'attempt_status_ambiguous': True}
    finally:
        del password
    write(ledger / 'result.json', evidence)
    answer = evidence.get('custody', {}).get('terminal_event', {}).get('content', '')
    if evidence.get('eligible') and answer.strip():
        with (ledger / 'response.md').open('x', encoding='utf-8', newline='\n') as output:
            output.write(answer.rstrip() + '\n')
    summary = {k: evidence.get(k) for k in ('eligible', 'invoked', 'marker_open', 'error',
                                          'supervisor_exit', 'ssh_exit', 'min_available_bytes')}
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if evidence.get('eligible') else 41


if __name__ == '__main__':
    sys.exit(main())
