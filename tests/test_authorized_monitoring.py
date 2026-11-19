"""HTTP-level integration tests for authorized read-only provider status."""
import json
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import demo_server
from readonly_circleci import ProviderError


class FakeReader:
    def __init__(self):
        self.calls = []
    def latest(self, repo):
        self.calls.append(repo)
        return {"repository": repo, "latest": {"number": 9, "statuses": []},
                "recent_failure": {"number": 8}, "historical_failure": True}


class AuthorizedMonitoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), demo_server.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = "http://127.0.0.1:" + str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_only_configured_repo_is_read(self):
        reader = FakeReader()
        with patch.object(demo_server, "TOKEN", "test-token"), patch.object(demo_server, "ALLOWED_REPOS", ("example/allowed",)), patch.object(demo_server, "READER", reader):
            with urlopen(self.url + "/api/live/config") as response:
                config = json.loads(response.read())
                self.assertEqual(config["repositories"], ["example/allowed"])
                self.assertNotIn("test-token", json.dumps(config))
            with self.assertRaises(HTTPError) as denied:
                urlopen(self.url + "/api/live?repo=example/other")
            self.assertEqual(denied.exception.code, 403)
            self.assertEqual(reader.calls, [])
            with urlopen(self.url + "/api/live?repo=example/allowed") as response:
                report = json.loads(response.read())
                self.assertTrue(report["historical_failure"])
                self.assertEqual(reader.calls, ["example/allowed"])

    def test_provider_error_does_not_leak_details(self):
        class ErrorReader:
            def latest(self, repo):
                raise ProviderError("private provider details test-token")
        with patch.object(demo_server, "TOKEN", "test-token"), patch.object(demo_server, "ALLOWED_REPOS", ("example/allowed",)), patch.object(demo_server, "READER", ErrorReader()):
            with self.assertRaises(HTTPError) as denied:
                urlopen(self.url + "/api/live?repo=example/allowed")
            self.assertEqual(denied.exception.code, 502)
            self.assertNotIn("test-token", denied.exception.read().decode())
