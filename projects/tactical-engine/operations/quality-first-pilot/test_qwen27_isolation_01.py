"""Differential fixtures for the new lease, target, and watchdog contracts.

Gate02 already covers custody bootstrap, durability and SSH EOF. These tests
address persistent attempt admission and stop pipe lifetime, which Gate02 never
exercised. They use local files and fake systemd/target objects only.
"""

import ast
import json
import os
from pathlib import Path
import queue
import tempfile
import time
import unittest
from unittest.mock import patch

import pilot_supervision_01 as core
import qwen27_isolation_01 as isolated


HERE = Path(__file__).resolve().parent


class AttemptTests(unittest.TestCase):
    def test_ambiguous_receipt_preserves_interdiction_across_new_store(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(isolated, 'sync_dir'), patch.object(os, 'chmod'):
            root = Path(tmp)
            binding = {'attempt_id': 'qwen27-mmap-on-01', 'boot_id': 'first-boot'}
            store = isolated.AttemptStore(root)
            directory = store.reserve(binding)
            store.finish(directory, binding, {'quiet': False, 'status': 'BLOCCATO'})
            self.assertEqual(json.loads(store.marker.read_bytes()), binding)
            with self.assertRaisesRegex(RuntimeError, 'E_ISOLATED_ATTEMPT_OPEN'):
                isolated.AttemptStore(root).reserve({'attempt_id': 'qwen27-mmap-on-02', 'boot_id': 'other'})

    def test_quiet_receipt_releases_marker_but_keeps_attempt_consumed(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(isolated, 'sync_dir'), patch.object(os, 'chmod'):
            root = Path(tmp)
            store = isolated.AttemptStore(root)
            binding = {'attempt_id': 'qwen27-mmap-on-01'}
            directory = store.reserve(binding)
            store.finish(directory, binding, {'quiet': True, 'status': 'BLOCCATO'})
            self.assertFalse(store.marker.exists())
            self.assertTrue((directory / 'stop-receipt.json').is_file())
            with self.assertRaises(FileExistsError):
                store.reserve(binding)
            self.assertTrue(store.reserve({'attempt_id': 'qwen27-mmap-on-02'}).is_dir())

    def test_mismatched_marker_is_never_removed(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(isolated, 'sync_dir'), patch.object(os, 'chmod'):
            store = isolated.AttemptStore(Path(tmp))
            binding = {'attempt_id': 'qwen27-mmap-on-01', 'boot_id': 'current'}
            directory = store.reserve(binding)
            store.marker.write_text('{"attempt_id":"qwen27-mmap-on-02"}')
            with self.assertRaisesRegex(RuntimeError, 'E_ATTEMPT_MARKER_CHANGED'):
                store.finish(directory, binding, {'quiet': True})
            self.assertTrue(store.marker.exists())

    def test_only_frozen_qwen_request_and_separate_authorization_are_accepted(self):
        project = HERE.parents[1]
        historical = project / 'evaluation/quality_first_qwen27_single_case_01/call-02/request.json'
        call = json.loads(historical.read_bytes())
        call['payload']['options']['use_mmap'] = True
        call['payload_sha256'] = isolated.PAYLOAD_HASH
        binding = {'version': '0.40.5', 'models': {'qwen': {'tag': isolated.TAG, 'digest': isolated.DIGEST}}}
        plan = {'attempt_id': 'qwen27-mmap-on-01', 'request': {'call': call, 'binding': binding},
                'authorized': True, 'max_posts': 1, 'kill_authorized': True}
        self.assertEqual(isolated.validate_request(plan)[0], plan['attempt_id'])
        with self.assertRaisesRegex(RuntimeError, 'E_SEPARATE_AUTHORIZATION'):
            isolated.validate_request(dict(plan, kill_authorized=False))
        call['payload']['options']['seed'] += 1
        with self.assertRaisesRegex(RuntimeError, 'E_QWEN_PAYLOAD'):
            isolated.validate_request(plan)


class ControlTests(unittest.TestCase):
    def test_grace_stays_anchored_after_late_trigger(self):
        s = isolated.NS
        self.assertEqual(isolated.escalation_at(100 * s, 900 * s), 115 * s)
        self.assertEqual(isolated.escalation_at(902 * s, 900 * s), 915 * s)

    def test_cgroup_requires_an_unambiguous_population_value(self):
        self.assertFalse(isolated.read_cgroup_events('populated 0\nfrozen 0\n'))
        self.assertTrue(isolated.read_cgroup_events('populated 1\n'))
        for value in ('', 'populated 0\npopulated 1', 'populated 2'):
            with self.subTest(value=value), self.assertRaisesRegex(RuntimeError, 'E_CGROUP_EVENTS'):
                isolated.read_cgroup_events(value)

    def test_writer_does_not_keep_the_stop_pipe_alive(self):
        with tempfile.TemporaryDirectory() as tmp:
            rd, wr = os.pipe()
            try:
                inbox, acks = queue.Queue(), queue.Queue()
                inbox.put({'kind': 'terminal', 'data': {}})
                core._journal_writer(tmp, inbox, acks, None, None, None, (wr,))
                self.assertEqual(acks.get_nowait()['kind'], 'terminal')
                with self.assertRaises(OSError):
                    os.fstat(wr)
                self.assertEqual(os.read(rd, 1), b'')
            finally:
                os.close(rd)

    def test_due_escalation_cannot_wait_for_manager_term_call(self):
        rd, wr = os.pipe()
        try:
            deadline = time.monotonic_ns() - isolated.GRACE - isolated.NS
            control = isolated.StopControl(deadline, wr)
            actions = []

            class Target:
                def term(self):
                    if os.read(rd, 1) != b'':
                        raise RuntimeError('expected cooperative EOF')
                    actions.append('term_requested')
                    raise TimeoutError('synthetic manager timeout')

                def populated(self):
                    return True

                def kill(self):
                    actions.append('anchored_kill')

            control.watch(Target(), lambda: self.fail('sampling after expired deadline'), None, lambda _: None)
            self.assertFalse(control.allow_go())
            self.assertIn('term_requested', actions)
            self.assertIn('anchored_kill', actions)
            self.assertEqual(control.trigger['reason'], 'E_DEADLINE')
            self.assertTrue(any(action.get('written') for action in control.actions))
        finally:
            os.close(rd)

    def test_reserve_violation_closes_gate_before_sample_is_collected(self):
        rd, wr = os.pipe()
        try:
            control = isolated.StopControl(time.monotonic_ns() + isolated.BUDGET, wr)

            class Target:
                def populated(self):
                    return False

                def members(self):
                    return []

                def term(self):
                    raise ProcessLookupError('synthetic exited target')

            def note(_sample):
                self.assertIsNotNone(control.trigger)
                self.assertFalse(control.allow_go())

            control.watch(Target(), lambda: {'available_bytes': 3_999_999_999}, None, note)
            self.assertEqual(control.trigger['reason'], 'E_MEMORY_RESERVE')
            self.assertIsNotNone(control.empty_ns)
            self.assertEqual(os.read(rd, 1), b'')
        finally:
            os.close(rd)

    def test_term_refuses_same_unit_name_with_a_different_invocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = isolated.Target.__new__(isolated.Target)
            target.unit = 'football-qwen27-mmap-on-01-ollama.service'
            target.path = Path(tmp) / 'fake-cgroup'
            target.path.touch()
            target.invocation = 'a' * 32
            target.fd = os.open(target.path, os.O_RDONLY)
            try:
                changed = {'Id': target.unit, 'ControlGroup': '/system.slice/' + target.unit,
                           'InvocationID': 'b' * 32}
                with patch.object(isolated, 'unit_info', return_value=changed), patch.object(isolated.subprocess, 'Popen') as popen:
                    with self.assertRaisesRegex(RuntimeError, 'E_TARGET_REBOUND'):
                        target.term()
                popen.assert_not_called()
            finally:
                os.close(target.fd)

    def test_unit_plan_is_confined_and_reuses_single_post_site(self):
        target = 'football-qwen27-mmap-on-01-ollama.service'
        sup = 'football-qwen27-mmap-on-01-supervisor.service'
        args = isolated.daemon_arguments(target, sup, 27, '/usr/bin/ollama', '/var/lib/models')
        for option in ('--unit=' + target, '--property=Restart=no', '--property=BindsTo=' + sup,
                       '--property=TimeoutStopSec=15s', '--property=NetworkNamespacePath=/proc/27/ns/net',
                       '--property=KillMode=control-group', '--property=ProtectControlGroups=yes',
                       '--property=User=football-qwen27', '--property=Delegate=no',
                       '--property=ReadOnlyPaths=/var/lib/models', '--setenv=OLLAMA_HOST=127.0.0.1:11434'):
            self.assertIn(option, args)
        with patch.object(isolated, 'run_unit') as run, patch.object(isolated, 'unit_info',
                                                                   return_value={'ActiveState': 'active'}):
            isolated.start_watchdog('football-qwen27-mmap-on-01', Path('/binding.json'), 900 * isolated.NS)
        self.assertEqual([call.args[0][1] for call in run.call_args_list],
                         ['--on-boot=900000000us', '--on-boot=915000000us'])
        posts = []
        for name in ('paired_pilot_remote_01.py', 'qwen27_isolation_01.py'):
            tree = ast.parse((HERE / name).read_bytes())
            posts += [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                      and isinstance(node.func, ast.Attribute) and node.func.attr == 'request'
                      and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == 'POST']
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].args[1].value, '/api/chat')


if __name__ == '__main__':
    unittest.main()
