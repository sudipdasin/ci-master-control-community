"""HTTP integration tests for optional live monitoring. No real CircleCI calls."""
import json
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import demo_server
from test_demo_server import CommunityPreviewTests


class LiveDashboardTests(CommunityPreviewTests):
    def test_config_does_not_expose_token(self):
        with urlopen(self.url + "/api/live/config") as response:
            data = json.loads(response.read())
            self.assertFalse(data["enabled"])
            self.assertNotIn("token", data)
            self.assertEqual(data["repositories"], [])

    def test_live_disabled_without_opt_in(self):
        with self.assertRaises(HTTPError) as caught:
            urlopen(self.url + "/api/live?repo=example/demo-app")
        self.assertEqual(caught.exception.code, 503)

    def test_dashboard_has_opt_in_panel(self):
        with urlopen(self.url) as response:
            html = response.read().decode()
            self.assertIn("Opt-in live CircleCI monitoring", html)
            self.assertIn("/api/live/config", html)

    def test_reject_invalid_allowlist_at_startup(self):
        self.assertFalse(demo_server.ALLOWED_REPOS)
        self.assertEqual(demo_server.HOST, "127.0.0.1")
