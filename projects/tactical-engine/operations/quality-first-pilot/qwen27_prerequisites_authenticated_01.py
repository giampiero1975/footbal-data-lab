"""Run the existing, two-resource provisioning payload with one sudo authentication."""

import base64
import getpass
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time
import warnings


FINGERPRINT = 'SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks'
REF = 'refs/heads/codex/tactical-state-contract-v1'
PROVISION_SHA256 = 'ee6dfcf2878da5f908877ae1917be39ed23d9da131cbe403ef09f7854048af69'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def remote():
    source = base64.b64decode(sys.argv[1], validate=True)
    if sha(source) != PROVISION_SHA256:
        raise RuntimeError('E_PROVISION_SOURCE')
    scope = {'__name__': 'provision_source'}
    exec(compile(source, '<published-provision-source>', 'exec'), scope)
    if scope['pwd'].getpwuid(os.geteuid()).pw_name != 'football':
        raise RuntimeError('E_SSH_PRINCIPAL')
    report = {'source_sha256': sha(source), 'before': scope['resources'](),
              'services_before': scope['production'](),
              'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
    root_code = ("import sys,base64;src=base64.b64decode(sys.argv[1],validate=True);"
                 "scope={'__name__':'provision'};exec(compile(src,'<provision>','exec'),scope);"
                 "scope['provision'](src)")
    code = 41
    try:
        password_line = sys.stdin.buffer.readline(1024)
        if not (1 < len(password_line) < 1024 and password_line.endswith(b'\n')):
            raise RuntimeError('E_SINGLE_AUTHENTICATION_INPUT')
        result = subprocess.run(['/usr/bin/sudo', '-S', '-p', '', '--', '/usr/bin/python3',
                                 '-I', '-B', '-c', root_code, sys.argv[1]], input=password_line,
                                capture_output=True, timeout=25)
        report['privileged_exit'] = result.returncode
        if result.returncode == 0:
            report['provisioning'] = json.loads(result.stdout)
            if report['provisioning']['source_sha256'] != sha(source):
                raise RuntimeError('E_PRIVILEGED_SOURCE_HASH')
            code = 0
        else:
            # Preserve a diagnostic category without recording authentication output.
            report['failure'] = 'E_SUDO_OR_PROVISIONING_FAILED'
    finally:
        report['after'] = scope['resources']()
        report['services_after'] = scope['production']()
        report['services_unchanged'] = report['services_before'] == report['services_after']
        state = scope['STATE']
        report['ssh_principal_directory_access'] = {'read_and_traverse': os.access(state, os.R_OK | os.X_OK),
                                                     'write': os.access(state, os.W_OK)}
        print(json.dumps(report, sort_keys=True))
    access = report['ssh_principal_directory_access']
    return code or (0 if report['services_unchanged'] and access['read_and_traverse'] and not access['write'] else 41)


def local():
    here = Path(__file__).resolve()
    project = here.parents[2]
    source = here.with_name('qwen27_isolation_prerequisites_01.py').read_bytes()
    if sha(source) != PROVISION_SHA256:
        raise RuntimeError('E_PROVISION_SOURCE')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    published = subprocess.check_output(['git', 'ls-remote', 'origin', REF], text=True).split()
    if published != [head, REF] or subprocess.check_output(['git', 'status', '--porcelain']):
        raise RuntimeError('E_LOCAL_GIT')
    home = Path(os.environ['USERPROFILE']) / '.ssh'
    known = subprocess.check_output(['ssh-keygen', '-F', '163.5.26.155', '-f', str(home / 'known_hosts')])
    if FINGERPRINT not in subprocess.check_output(['ssh-keygen', '-lf', '-'], input=known).decode():
        raise RuntimeError('E_HOST_KEY')
    ssh = ['ssh', '-F', str(home / 'config'), '-T', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10',
           '-o', 'StrictHostKeyChecking=yes', '-o', 'UpdateHostKeys=no', '-o', 'HostKeyAlgorithms=ssh-ed25519',
           '-o', 'KexAlgorithms=curve25519-sha256', 'football-vps']
    own_source = here.read_bytes()
    loader = ("import base64,sys;scope={'__name__':'published_authenticated_runner'};"
              "exec(compile(base64.b64decode(sys.argv[2],validate=True),'<authenticated-runner>','exec'),scope);"
              "sys.exit(scope['remote']())")
    command = shlex.join(['/usr/bin/python3', '-I', '-B', '-c', loader,
                          base64.b64encode(source).decode(), base64.b64encode(own_source).decode()])
    folder = project / 'docs/qwen27-isolation-prerequisites-authenticated-01'
    folder.mkdir()
    (folder / '.gitattributes').write_bytes(b'* -text\n')
    invocation = {'technical_commit': head, 'runner_sha256': sha(own_source),
                  'provision_sha256': sha(source), 'host_fingerprint': FINGERPRINT,
                  'remote_command_sha256': sha(command.encode()), 'max_ssh_invocations': 1}
    (folder / 'invocation.json').write_bytes((json.dumps(invocation, indent=2) + '\n').encode())
    with warnings.catch_warnings():
        warnings.simplefilter('error', getpass.GetPassWarning)
        password = getpass.getpass('Sudo authentication for football-vps (hidden): ')
    if not password or '\r' in password or '\n' in password or len(password.encode()) >= 1023:
        raise RuntimeError('E_SINGLE_AUTHENTICATION_INPUT')
    result = subprocess.run(ssh + [command], input=password.encode() + b'\n', capture_output=True, timeout=55)
    del password
    # Only parse and retain the intended JSON schema. SSH stderr is intentionally omitted.
    if result.stdout:
        record = json.loads(result.stdout)
        if record.get('source_sha256') != sha(source):
            raise RuntimeError('E_PROVISION_SOURCE')
        (folder / 'stdout.json').write_bytes(result.stdout)
        print(json.dumps(record, sort_keys=True))
    (folder / 'exit.json').write_bytes((json.dumps({'exit': result.returncode, 'ended_utc_ns': time.time_ns()}) + '\n').encode())
    return result.returncode


if __name__ == '__main__':
    sys.exit(local())
