"""Read-only Linux gate preflight. Execute once over the known SSH principal.

Gate02 verified a user-owned synthetic child and custody. This inspection is
different: it checks prerequisites for system-manager units, private network
namespaces, cgroup-scoped STOP and an interdiction marker after supervisor exit.
It does not open a network socket or create any remote file, unit, or process
in a synthetic cgroup. sudo is used only to list existing policy, when present.
"""

import hashlib
import json
import os
from pathlib import Path
import pwd
import shutil
import stat
import subprocess
import sys
import time


GATE = 'qwen27-isolation-linux-gate-20261120-01'
UNITS = [f'football-{GATE}-{role}.{kind}' for role, kind in (
    ('supervisor', 'service'), ('target', 'service'), ('sentinel', 'service'),
    ('deadline-term', 'timer'), ('deadline-term', 'service'),
    ('deadline-kill', 'timer'), ('deadline-kill', 'service'),
)]
STATE = Path('/var/lib/football-qwen27-isolation')
CGROUP = Path('/sys/fs/cgroup')
LOCK = Path('/home/football/.local/share/football-data-lab/runtime-locks/spatial-v2-extraction-locator.lock')
SERVICE_FIELDS = ('Id', 'LoadState', 'ActiveState', 'SubState', 'MainPID', 'InvocationID',
                  'ControlGroup', 'ActiveEnterTimestampMonotonic')


def run(*argv):
    try:
        result = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                timeout=5, env=dict(os.environ, LC_ALL='C', SYSTEMD_PAGER='cat'))
    except (OSError, subprocess.TimeoutExpired) as error:
        return {'exit': None, 'error': str(error)}
    return {'exit': result.returncode, 'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()}


def unit(name, user=False):
    scope = ('--user',) if user else ()
    result = run('/usr/bin/systemctl', *scope, 'show', name,
                 *(f'--property={field}' for field in SERVICE_FIELDS))
    return {**result, 'properties': dict(line.split('=', 1) for line in
                                       result.get('stdout', '').splitlines() if '=' in line)}


def production():
    return {'ollama': unit('ollama.service'), 'rag': unit('football-rag-api.service', user=True)}


def probe_path(path):
    try:
        info = path.lstat()
    except OSError as error:
        return {'exists': False if isinstance(error, FileNotFoundError) else None, 'errno': error.errno}
    return {'exists': True, 'uid': info.st_uid, 'gid': info.st_gid,
            'mode': oct(stat.S_IMODE(info.st_mode)), 'inode': info.st_ino,
            'regular': stat.S_ISREG(info.st_mode), 'directory': stat.S_ISDIR(info.st_mode),
            'symlink': stat.S_ISLNK(info.st_mode), 'writable_by_ssh_principal': os.access(path, os.W_OK)}


def text(path):
    try:
        return Path(path).read_text().strip()
    except OSError as error:
        return {'errno': error.errno}


def account(name):
    try:
        data = pwd.getpwnam(name)
    except KeyError:
        return {'exists': False}
    return {'exists': True, 'uid': data.pw_uid, 'gid': data.pw_gid}


def link(path):
    try:
        return os.readlink(path)
    except OSError as error:
        return {'errno': error.errno}


def main(source):
    before = production()
    login = pwd.getpwuid(os.geteuid()).pw_name
    own_cgroup = text('/proc/self/cgroup')
    own_slice = CGROUP / own_cgroup[3:].lstrip('/') if isinstance(own_cgroup, str) and own_cgroup.startswith('0::') else None
    systemd_run = run('/usr/bin/systemd-run', '--help')
    systemd_help = systemd_run.pop('stdout', '')
    flags = ('--unit=', '--slice=', '--property=', '--service-type=', '--on-boot=', '--timer-property=')
    planned_unit = UNITS[0]
    args = ('--action-id', 'org.freedesktop.systemd1.manage-units', '--process', str(os.getpid()),
            '--detail', 'unit', planned_unit, '--detail', 'verb', 'start')
    result = {'gate': GATE, 'source_sha256': hashlib.sha256(source).hexdigest(),
              'timestamp_monotonic_ns': time.monotonic_ns(), 'kernel': os.uname().release,
              'python': sys.version.split()[0], 'login': login, 'euid': os.geteuid(), 'egid': os.getegid(),
              'pid1': text('/proc/1/comm'), 'boot_id': text('/proc/sys/kernel/random/boot_id'),
              'systemd_version': run('/usr/bin/systemctl', '--version'),
              'systemd_run_cli': {**systemd_run, 'flags': {flag: flag in systemd_help for flag in flags}},
              'systemd_start_policy': run('/usr/bin/pkcheck', *args) if shutil.which('pkcheck') else None,
              'sudo_systemd_run_policy': run('/usr/bin/sudo', '-n', '-l', '--', '/usr/bin/systemd-run')
              if shutil.which('sudo') else None,
              'sudo_root_python_policy': run('/usr/bin/sudo', '-n', '-l', '--', '/usr/bin/python3')
              if shutil.which('sudo') else None,
              'cgroup_fs': run('/usr/bin/stat', '-f', '-c', '%T', str(CGROUP)),
              'cgroup_controllers': text(CGROUP / 'cgroup.controllers'), 'ssh_cgroup': own_cgroup,
              'system_slice_kill': probe_path(CGROUP / 'system.slice/cgroup.kill'),
              'ssh_cgroup_kill': probe_path(own_slice / 'cgroup.kill') if own_slice else None,
              'network_namespace': {'ssh': link('/proc/self/ns/net'), 'pid1': link('/proc/1/ns/net'),
                                    'max_net_namespaces': text('/proc/sys/user/max_net_namespaces'),
                                    'nsenter_present': bool(shutil.which('nsenter'))},
              'accounts': {name: account(name) for name in ('football', 'ollama', 'football-qwen27')},
              'lock': probe_path(LOCK), 'state_root': probe_path(STATE), 'open_marker': probe_path(STATE / 'open.json'),
              'gate_units': {name: unit(name)['properties'] for name in UNITS}, 'services_before': before}
    result['services_after'] = production()
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))


if __name__ == '__main__':
    sys.exit('Invoke via the pinned stdin loader so the observed source is hashed.')
