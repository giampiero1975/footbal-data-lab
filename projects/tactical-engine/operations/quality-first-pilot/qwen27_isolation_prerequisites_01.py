"""Provision only the dedicated account and state directory on the known VPS."""

import grp
import hashlib
import json
import os
from pathlib import Path
import pwd
import shlex
import stat
import subprocess
import sys


NAME = 'football-qwen27'
STATE = Path('/var/lib/football-qwen27-isolation')
HOME = Path('/nonexistent')
SHELL = '/usr/sbin/nologin'
SHADOW = Path('/etc/shadow')
USERADD = ['/usr/sbin/useradd', '--system', '--user-group', '--no-create-home',
           '--no-log-init', '--home-dir', str(HOME), '--shell', SHELL, NAME]
FIELDS = ('Id', 'ActiveState', 'SubState', 'MainPID', 'InvocationID',
          'ControlGroup', 'ActiveEnterTimestampMonotonic', 'FragmentPath', 'DropInPaths')


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def lookup(reader, name):
    try:
        return reader(name)
    except KeyError:
        return None


def path_state(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    return {'uid': info.st_uid, 'gid': info.st_gid, 'mode': f'{stat.S_IMODE(info.st_mode):04o}',
            'directory': stat.S_ISDIR(info.st_mode), 'symlink': stat.S_ISLNK(info.st_mode)}


def resources():
    user = lookup(pwd.getpwnam, NAME)
    group = lookup(grp.getgrnam, NAME)
    record = {'account': None, 'group': None, 'directory': path_state(STATE)}
    if group is not None:
        record['group'] = {'name': NAME, 'gid': group.gr_gid, 'explicit_members': group.gr_mem}
    if user is not None:
        record['account'] = {'name': NAME, 'uid': user.pw_uid, 'gid': user.pw_gid,
                             'home': user.pw_dir, 'shell': user.pw_shell,
                             'groups': sorted(os.getgrouplist(NAME, user.pw_gid))}
    if record['directory'] and record['directory']['directory']:
        record['marker_present'] = os.path.lexists(STATE / 'open.json')
    return record


def verify_directory(info):
    require(info == {'uid': 0, 'gid': 0, 'mode': '0755', 'directory': True, 'symlink': False},
            'E_STATE_DIRECTORY_IDENTITY')
    require(not any(key.startswith('system.posix_acl_') for key in os.listxattr(STATE)),
            'E_STATE_DIRECTORY_ACL')
    require(not any(STATE.iterdir()), 'E_STATE_DIRECTORY_NOT_EMPTY')


def verify_account(account, group):
    require(group is not None and account is not None and group['gid'] == account['gid']
            and group['gid'] != 0 and not group['explicit_members'], 'E_ACCOUNT_PRIMARY_GROUP')
    excluded = {0, pwd.getpwnam('football').pw_uid, pwd.getpwnam('ollama').pw_uid}
    require(account['uid'] not in excluded and account['shell'] == SHELL
            and account['home'] == str(HOME) and account['groups'] == [group['gid']],
            'E_SERVICE_ACCOUNT_IDENTITY')
    for line in SHADOW.read_text().splitlines():
        fields = line.split(':', 2)
        if fields[0] == NAME:
            require(fields[1].startswith(('!', '*')), 'E_SERVICE_ACCOUNT_PASSWORD_UNLOCKED')
            return
    raise RuntimeError('E_SERVICE_ACCOUNT_SHADOW_ENTRY')


def provision(source):
    require(os.geteuid() == os.getegid() == 0, 'E_EXISTING_ROOT_AUTHORIZATION_REQUIRED')
    before = resources()
    require(not os.path.lexists(HOME) and os.access(SHELL, os.X_OK), 'E_NOLOGIN_OR_HOME_PRECONDITION')
    for parent in STATE.parents:
        info = parent.lstat()
        require(stat.S_ISDIR(info.st_mode) and info.st_uid == 0 and not info.st_mode & 0o022,
                'E_STATE_DIRECTORY_ANCESTOR')
    require('system.posix_acl_default' not in os.listxattr(STATE.parent), 'E_STATE_PARENT_DEFAULT_ACL')
    if before['directory'] is not None:
        verify_directory(before['directory'])
    if before['account'] is None:
        require(before['group'] is None, 'E_EXISTING_GROUP_WITHOUT_ACCOUNT')
        subprocess.run(USERADD, check=True, stdin=subprocess.DEVNULL, timeout=10)
    current = resources()
    verify_account(current['account'], current['group'])
    if before['directory'] is None:
        os.umask(0o022)
        STATE.mkdir(mode=0o755)
    after = resources()
    verify_directory(after['directory'])
    after['account']['password_locked'] = True
    print(json.dumps({'source_sha256': hashlib.sha256(source).hexdigest(), 'euid': os.geteuid(),
                      'before': before, 'after': after, 'account_created': before['account'] is None,
                      'directory_created': before['directory'] is None}, sort_keys=True))


def production():
    services = {}
    for name, scope in (('ollama.service', ()), ('football-rag-api.service', ('--user',))):
        result = subprocess.run(['/usr/bin/systemctl', *scope, 'show', name,
                                 *(f'--property={field}' for field in FIELDS)],
                                check=True, capture_output=True, text=True, timeout=5)
        values = dict(item.split('=', 1) for item in result.stdout.splitlines() if '=' in item)
        require(values['Id'] == name and values['ActiveState'] == 'active'
                and values['SubState'] == 'running' and int(values['MainPID']) > 0
                and bool(values['InvocationID']), 'E_REQUIRED_SERVICE')
        paths = [values['FragmentPath'], *shlex.split(values['DropInPaths'])]
        values['unit_files_sha256'] = {path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
                                       for path in paths}
        services[name] = values
    return services


def main(source):
    require(pwd.getpwuid(os.geteuid()).pw_name == 'football', 'E_SSH_PRINCIPAL')
    report = {'source_sha256': hashlib.sha256(source).hexdigest(), 'before': resources(),
              'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
              'services_before': production()}
    loader = ("import sys; src=sys.stdin.buffer.read(); scope={'__name__':'provision'}; "
              "exec(compile(src,'<provision>','exec'),scope); scope['provision'](src)")
    code = 1
    try:
        result = subprocess.run(['/usr/bin/sudo', '-n', '--', '/usr/bin/python3', '-I', '-B', '-c', loader],
                                input=source, capture_output=True, timeout=25)
        report['privileged_exit'] = result.returncode
        if result.stderr:
            report['privileged_stderr'] = result.stderr.decode(errors='replace').strip()
        if result.returncode == 0:
            report['provisioning'] = json.loads(result.stdout)
            require(report['provisioning']['source_sha256'] == report['source_sha256'], 'E_SOURCE_HASH')
            code = 0
    finally:
        report['after'] = resources()
        report['services_after'] = production()
        report['services_unchanged'] = report['services_before'] == report['services_after']
        report['ssh_principal_directory_access'] = {'read_and_traverse': os.access(STATE, os.R_OK | os.X_OK),
                                                     'write': os.access(STATE, os.W_OK)}
        print(json.dumps(report, sort_keys=True))
    access = report['ssh_principal_directory_access']
    return code or (0 if report['services_unchanged'] and access['read_and_traverse'] and not access['write'] else 41)


if __name__ == '__main__':
    sys.exit('Invoke with the pinned stdin loader.')
