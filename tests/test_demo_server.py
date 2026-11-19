"""Unit and live HTTP tests for the Community development scaffold."""
import json
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import demo_server


class CommunityPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), demo_server.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_synthetic_data(self):
        data = demo_server.inventory()
        self.assertEqual(len(data["projects"]), 2)
        self.assertTrue(all(p["repository"].startswith("example/") for p in data["projects"]))

    def test_local_only(self):
        self.assertEqual(demo_server.HOST, "127.0.0.1")

    def test_health_endpoint(self):
        with urlopen(self.url + "/health") as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read())["mode"], "synthetic-preview")

    def test_inventory_endpoint_and_headers(self):
        with urlopen(self.url + "/api/inventory") as response:
            self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
            self.assertEqual(len(json.loads(response.read())["projects"]), 2)

    def test_home_explicitly_declares_synthetic_data(self):
        with urlopen(self.url) as response:
            page = response.read().decode()
            self.assertIn("No CI provider connected", page)
            self.assertIn("human approval", page)

    def test_writes_not_allowed(self):
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            with self.subTest(method=method), self.assertRaises(HTTPError) as caught:
                urlopen(Request(self.url + "/api/inventory", data=b"{}", method=method))
            self.assertEqual(caught.exception.code, 405)

    def test_missing_endpoint_is_404(self):
        with self.assertRaises(HTTPError) as caught:
            urlopen(self.url + "/unknown")
        self.assertEqual(caught.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
