import json
import sys
import unittest
from io import BytesIO
from pathlib import Path
from urllib.request import Request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from readonly_circleci import NoRedirect, ProviderError, Reader

P1 = "00000000-0000-4000-8000-000000000001"
P2 = "00000000-0000-4000-8000-000000000002"


class Response:
    status = 200
    def __init__(self, data):
        self.stream = BytesIO(json.dumps(data).encode())
    def __enter__(self):
        return self
    def __exit__(self, *_):
        self.stream.close()
    def read(self, n):
        return self.stream.read(n)


class Opener:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []
    def open(self, request, timeout=None):
        assert isinstance(request, Request)
        self.requests.append(request)
        return Response(self.responses.pop(0))


class ReadonlyCircleCITests(unittest.TestCase):
    def test_missing_token_fails_closed(self):
        with self.assertRaisesRegex(ProviderError, "token not configured"):
            Reader("").latest("example/repo")

    def test_slugs_reject_injection(self):
        for slug in ("../evil", "x/y?run=true", "x/y/../../../bad", "x/y#extra", "x%2Fy", "x/y z"):
            with self.subTest(slug=slug), self.assertRaises(ProviderError):
                Reader("local-test").latest(slug)

    def test_readonly_calls_and_historical_failure_detection(self):
        opener = Opener([{"items": [{"id": P2, "number": 13}, {"id": P1, "number": 12}]},
                         {"items": []}, {"items": [{"status": "failed"}]}])
        now = [1]
        reader = Reader("local-test", opener=opener, clock=lambda: now[0])
        result = reader.latest("example/repo")
        self.assertEqual(result["latest"]["number"], 13)
        self.assertTrue(result["historical_failure"])
        self.assertEqual(result["recent_failure"]["number"], 12)
        self.assertEqual(len(opener.requests), 3)
        self.assertTrue(all(r.get_method() == "GET" for r in opener.requests))
        self.assertTrue(all(r.full_url.startswith("https://circleci.com/api/v2/") for r in opener.requests))
        self.assertEqual(reader.latest("example/repo"), result)
        self.assertEqual(len(opener.requests), 3)  # cached, no additional calls
        now[0] = 32
        with self.assertRaises(IndexError):  # expires cache and attempts fresh read
            reader.latest("example/repo")

    def test_redirects_rejected(self):
        with self.assertRaises(ProviderError):
            NoRedirect().redirect_request(Request("https://circleci.com/api/v2/test"), None, 302, "moved", {}, "https://evil.example")

    def test_unexpected_pipeline_id_rejected(self):
        opener = Opener([{"items": [{"id": "../../bad"}]}])
        with self.assertRaises(ProviderError):
            Reader("local-test", opener=opener).latest("example/repo")

    def test_response_token_not_embedded_in_report(self):
        opener = Opener([{"items": []}])
        result = Reader("sensitive-test-token", opener=opener).latest("example/repo")
        self.assertNotIn("sensitive-test-token", json.dumps(result))
