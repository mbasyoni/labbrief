"""Public-candidate boundaries with fake providers and ephemeral loopback HTTP."""
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import app
import test_app


class PublicSurfaceTests(unittest.TestCase):
    setUp = test_app.HTTPTests.setUp
    tearDown = test_app.HTTPTests.tearDown
    call = test_app.HTTPTests.call
    headers = test_app.HTTPTests.headers

    def test_removed_get_assets_and_private_routes_return_404_without_session(self):
        paths = ['/setup', '/setup.js', '/api/private-sandbox-setup/claim',
                 '/api/private-sandbox-setup/configure', '/api/private-sandbox-setup/clear',
                 '/api/private-continuation/status', '/api/private-continuation/import',
                 '/api/private-continuation/reconcile', '/api/private-continuation/replay']
        for path in paths:
            with self.subTest(path=path):
                code, headers, body = self.call('GET', path)
                self.assertEqual(code, 404)
                self.assertNotIn('Set-Cookie', headers)
                self.assertEqual(json.loads(body), {'error': 'Not found.'})

    def test_removed_post_routes_return_404_before_body_or_session_processing(self):
        paths = ['/api/private-sandbox-setup/claim', '/api/private-sandbox-setup/configure',
                 '/api/private-sandbox-setup/clear', '/api/private-continuation/import',
                 '/api/private-continuation/reconcile', '/api/private-continuation/replay']
        for path in paths:
            for headers in ({}, self.headers()):
                with self.subTest(path=path, session=bool(headers)):
                    self.assertEqual(self.call('POST', path, {}, headers)[0], 404)
        self.assertEqual(self.application.service.paypal.creates, 0)
        self.assertEqual(self.application.service.paypal.captures, 0)
        self.assertEqual(self.application.service.paypal.gets, 0)

    def test_session_metadata_contains_only_normal_mode_fields(self):
        code, _, body = self.call('GET', '/api/session', headers={'Cookie': self.cookie})
        self.assertEqual(code, 200)
        self.assertEqual(set(json.loads(body)), {'csrf', 'catalog', 'ai_ready', 'ai_description', 'paypal_ready', 'sandbox'})

    def test_setup_environment_cannot_arm_private_interfaces(self):
        with patch.dict(os.environ, {'LABBRIEF_ENABLE_SETUP': '1'}):
            self.assertEqual(self.call('GET', '/setup')[0], 404)
            self.assertEqual(self.call('POST', '/api/private-sandbox-setup/claim', {}, self.headers())[0], 404)
            self.assertFalse(hasattr(self.application, 'setup_token'))
            self.assertFalse(hasattr(self.application, 'setup_action'))
            self.assertFalse(hasattr(self.application.service, 'private_providers'))


class PublicSourceTests(unittest.TestCase):
    def test_private_construction_and_methods_are_removed(self):
        self.assertEqual(tuple(inspect.signature(app.App).parameters), ('service', 'origin'))
        self.assertEqual(tuple(inspect.signature(app.Service).parameters), ('store', 'ai', 'paypal'))
        for name in ('CONTINUATION_HASHES', 'CONTINUATION_RETENTION_SECONDS', 'load_continuation', 'UnconfiguredPrivateProvider'):
            self.assertFalse(hasattr(app, name))
        self.assertFalse(hasattr(app.PayPalSandbox, 'replay_original'))

    def test_removed_cli_flags_fail_before_startup(self):
        flags = ['--enable-sandbox-setup', '--resume-handoff', '--allow-existing-continuation-resume',
                 '--allow-existing-provider-resume', '--resume-provider-order-id']
        for flag in flags:
            with self.subTest(flag=flag):
                result = subprocess.run([sys.executable, str(app.ROOT / 'app.py'), flag], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn('unrecognized arguments', result.stderr)
                self.assertEqual(result.stdout, '')
        help_result = subprocess.run([sys.executable, str(app.ROOT / 'app.py'), '--help'], capture_output=True, text=True)
        self.assertEqual(help_result.returncode, 0)
        for flag in flags: self.assertNotIn(flag, help_result.stdout)

    def test_private_assets_tools_and_operation_fixtures_are_not_shipped(self):
        for name in ('private_mac_launcher.py', 'durable_mac.py', 'preview_launcher.py',
                     'portable_handoff', 'static/setup.html', 'static/setup.js',
                     'tests/test_continuation.py', 'tests/test_private_setup.py'):
            with self.subTest(name=name): self.assertFalse((app.ROOT / name).exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
