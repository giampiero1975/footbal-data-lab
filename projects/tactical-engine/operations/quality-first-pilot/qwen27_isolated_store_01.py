"""Publish a dedicated Qwen27 model store from the existing local blobs."""

import base64
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import zlib


REMOTE = r"""
import grp
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

expected = 'aaee06c39dcf2437cde036998d960e1fc1494b8191be7cc9657d01e509097813'
catalog_hash = 'b45285c1cc1fafaf0272e840a7b799cb11e1b4597c2dc47a2dc58a61942f408c'
source = Path('/usr/share/ollama/.ollama/models')
state = Path('/var/lib/football-qwen27-isolation')
relative = Path('manifests/registry.ollama.ai/library/qwen3.8/27b')
destination = state / 'models-qwen27'


def require(condition, error):
    if not condition:
        raise RuntimeError(error)


def services():
    values = {}
    for name, manager in (
        ('ollama.service', []),
        ('football-rag-api.service', ['--user', '--machine=football@.host']),
    ):
        output = subprocess.check_output(['/usr/bin/systemctl', *manager, 'show', name,
                                          '-p', 'ActiveState', '-p', 'MainPID',
                                          '-p', 'InvocationID'], text=True, timeout=3)
        values[name] = dict(line.split('=', 1) for line in output.splitlines())
        require(values[name].get('ActiveState') == 'active'
                and values[name].get('MainPID', '0') != '0'
                and values[name].get('InvocationID'), 'E_PRODUCTION_SERVICE')
    return values


def access(user, path, flag):
    return subprocess.run(
        ['/usr/bin/setpriv', f'--reuid={user.pw_uid}', f'--regid={user.pw_gid}',
         '--init-groups', '--no-new-privs', '/usr/bin/test', flag, str(path)],
        stdin=subprocess.DEVNULL, timeout=2).returncode == 0


def small_file(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'E_METADATA_FILE')
    with path.open('rb') as stream:
        raw = stream.read(65537)
    require(len(raw) <= 65536, 'E_METADATA_SIZE')
    return raw


def install():
    require(os.geteuid() == 0, 'E_ROOT')
    st = state.lstat()
    require(stat.S_ISDIR(st.st_mode) and st.st_uid == st.st_gid == 0
            and stat.S_IMODE(st.st_mode) == 0o755, 'E_STATE_DIRECTORY')
    require(not os.path.lexists(destination) and not os.path.lexists(state / 'open.json'),
            'E_ALREADY_PREPARED_OR_OPEN')
    user = pwd.getpwnam('football-qwen27')
    require((user.pw_uid, user.pw_gid) == (997, 987)
            and [entry.pw_name for entry in pwd.getpwall() if entry.pw_gid == user.pw_gid]
            == [user.pw_name] and not grp.getgrgid(user.pw_gid).gr_mem
            and os.getgrouplist(user.pw_name, user.pw_gid) == [user.pw_gid],
            'E_ISOLATED_IDENTITY')

    catalog_raw = small_file(source / relative)
    require(hashlib.sha256(catalog_raw).hexdigest() == catalog_hash, 'E_CATALOG_CHANGED')
    catalog = json.loads(catalog_raw)
    manifest_blob = source / 'blobs' / ('sha256-' + expected)
    manifest_raw = small_file(manifest_blob)
    require(hashlib.sha256(manifest_raw).hexdigest() == expected, 'E_CANONICAL_MANIFEST')
    require(any(item['digest'] == 'sha256:' + expected and item['size'] == len(manifest_raw)
                and item['mediaType'] == 'application/vnd.docker.distribution.manifest.v2+json'
                for item in catalog['layers']), 'E_CANONICAL_REFERENCE')
    manifest = json.loads(manifest_raw)
    referenced = [catalog['config'], *catalog['layers']]
    objects = []
    for item in [manifest['config'], *manifest['layers']]:
        digest = item['digest']
        require(re.fullmatch(r'sha256:[a-f0-9]{64}', digest)
                and any(all(entry[key] == item[key] for key in ('digest', 'size', 'mediaType'))
                        for entry in referenced), 'E_COMPONENT_BINDING')
        blob = source / 'blobs' / digest.replace(':', '-')
        blob_stat = blob.lstat()
        require(stat.S_ISREG(blob_stat.st_mode) and blob_stat.st_size == item['size']
                and blob_stat.st_dev == st.st_dev, 'E_SOURCE_BLOB')
        objects.append((blob, blob_stat))

    before = services()
    pending = Path(tempfile.mkdtemp(prefix='.qwen27-models-', dir=state))
    published = False
    try:
        (pending / 'blobs').mkdir()
        (pending / relative).parent.mkdir(parents=True)
        for directory in [p for p in pending.rglob('*') if p.is_dir()]:
            directory.chmod(0o755)
        for blob, blob_stat in objects:
            link = pending / 'blobs' / blob.name
            os.link(blob, link, follow_symlinks=False)
            linked = link.lstat()
            require((linked.st_dev, linked.st_ino, linked.st_size)
                    == (blob_stat.st_dev, blob_stat.st_ino, blob_stat.st_size),
                    'E_LINK_IDENTITY')
        (pending / relative).write_bytes(manifest_raw)
        (pending / relative).chmod(0o644)
        os.chown(pending, 0, user.pw_gid)
        pending.chmod(0o750)
        for path in [pending / relative, *(pending / 'blobs' / blob.name for blob, _ in objects)]:
            require(access(user, path, '-r') and not access(user, path, '-w'), 'E_ACCESS')
        require(not access(user, pending, '-w') and not access(user, pending / 'blobs', '-w'),
                'E_DIRECTORY_ACCESS')
        require(not access(user, source / relative, '-r') and not access(user, source, '-x'),
                'E_ORIGINAL_STORE_EXPOSURE')
        after = services()
        require(before == after, 'E_SERVICE_IDENTITY_CHANGED')
        require(not os.path.lexists(destination) and not os.path.lexists(state / 'open.json'),
                'E_ALREADY_PREPARED_OR_OPEN')
        pending.rename(destination)
        published = True
        require(access(user, destination / relative, '-r'), 'E_FINAL_ACCESS')
        print(json.dumps({'store': str(destination), 'uid': user.pw_uid, 'gid': user.pw_gid,
                          'root_mode': '0750', 'digest': expected,
                          'catalog_digest': catalog_hash, 'read_only_components': len(objects),
                          'services_before': before, 'services_after': after,
                          'original_store_access': False, 'model_loaded': False}, sort_keys=True))
    except BaseException:
        shutil.rmtree(destination if published else pending)
        raise


install()
"""


def main():
    home = Path.home() / '.ssh'
    known = subprocess.check_output(['ssh-keygen', '-F', '163.5.26.155',
                                     '-f', str(home / 'known_hosts')])
    fingerprints = subprocess.check_output(['ssh-keygen', '-lf', '-'], input=known).decode()
    if 'SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks' not in fingerprints:
        raise RuntimeError('E_HOST_KEY')
    root = Path(__file__).resolve().parents[2]
    artifact = root / 'docs/qwen27-isolation-model-access-01/isolated-store.json'
    if artifact.exists():
        raise RuntimeError('E_LOCAL_RESULT_EXISTS')
    password = sys.stdin.buffer.readline(1024).rstrip(bytes([13, 10]))
    if not password or len(password) >= 1023:
        raise RuntimeError('E_CREDENTIAL_INPUT')
    loader = 'import base64,sys,zlib;exec(compile(zlib.decompress(base64.b64decode(sys.argv[1],validate=True)), "<qwen-store>", "exec"))'
    encoded = base64.b64encode(zlib.compress(REMOTE.encode())).decode()
    command = shlex.join(['/usr/bin/sudo', '-S', '-p', '', '--', '/usr/bin/python3',
                         '-I', '-B', '-c', loader, encoded])
    result = subprocess.run(
        ['ssh', '-F', str(home / 'config'), '-T', '-o', 'BatchMode=yes',
         '-o', 'ConnectTimeout=10', '-o', 'StrictHostKeyChecking=yes',
         '-o', 'UpdateHostKeys=no', '-o', 'HostKeyAlgorithms=ssh-ed25519',
         '-o', 'KexAlgorithms=curve25519-sha256', 'football-vps', command],
        input=password + bytes([10]), capture_output=True, timeout=45)
    del password
    if result.returncode:
        detail = re.search(r'RuntimeError: (E_[A-Z_]+)', result.stderr.decode(errors='replace'))
        raise RuntimeError(detail.group(1) if detail else f'E_REMOTE_EXIT_{result.returncode}')
    record = json.loads(result.stdout)
    record['commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    record['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with artifact.open('x', encoding='utf-8', newline='\n') as output:
        json.dump(record, output, indent=2, sort_keys=True)
        output.write('\n')
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
