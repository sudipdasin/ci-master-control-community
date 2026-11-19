"""Safe, minimal CircleCI API v2 reader. NEVER sends non-GET requests."""
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}/[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$")
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
MAX_RESPONSE = 256 * 1024
API_BASE = "https://circleci.com/api/v2"


class ProviderError(Exception):
    """Public generic failure; do not leak tokens or provider response payloads."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise ProviderError("CircleCI returned a redirect, which is not permitted")


class Reader:
    def __init__(self, token, opener=None, clock=time.monotonic):
        self._token = token
        self._opener = opener or urllib.request.build_opener(NoRedirect())
        self._clock = clock
        self._cache = {}

    def _get(self, endpoint):
        if not self._token:
            raise ProviderError("CircleCI token not configured")
        if not endpoint.startswith("/") or endpoint.startswith("//") or ".." in endpoint or "\\" in endpoint:
            raise ProviderError("Invalid CircleCI endpoint")
        request = urllib.request.Request(
            API_BASE + endpoint,
            headers={"Circle-Token": self._token, "Accept": "application/json"},
            method="GET",
        )
        try:
            with self._opener.open(request, timeout=8) as response:
                if response.status != 200:
                    raise ProviderError("CircleCI read request failed")
                body = response.read(MAX_RESPONSE + 1)
                if len(body) > MAX_RESPONSE:
                    raise ProviderError("CircleCI response exceeds safety limit")
                result = json.loads(body)
                if not isinstance(result, dict):
                    raise ProviderError("Unexpected CircleCI response")
                return result
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
            raise ProviderError("CircleCI read request unavailable") from None

    def latest(self, slug, branch="main", max_pipelines=4):
        if not SLUG_RE.fullmatch(slug):
            raise ProviderError("Invalid repository slug")
        if not isinstance(branch, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.\\-/]{0,79}", branch) or ".." in branch:
            raise ProviderError("Invalid branch")
        max_pipelines = min(4, max(1, int(max_pipelines)))
        cache_key = (slug, branch, max_pipelines)
        cached = self._cache.get(cache_key)
        if cached and self._clock() - cached[0] < 30:
            return cached[1]
        escaped_branch = urllib.parse.quote(branch, safe="")
        raw = self._get(f"/project/gh/{slug}/pipeline?branch={escaped_branch}")
        pipelines = raw.get("items", [])
        if not isinstance(pipelines, list):
            raise ProviderError("Invalid pipeline list")
        pipelines = pipelines[:max_pipelines]
        results = []
        for pipeline in pipelines:
            if not isinstance(pipeline, dict) or not UUID_RE.fullmatch(str(pipeline.get("id", ""))):
                raise ProviderError("Unexpected pipeline identifier")
            workflow_response = self._get(f"/pipeline/{pipeline['id']}/workflow")
            workflows = workflow_response.get("items", [])
            if not isinstance(workflows, list):
                raise ProviderError("Invalid workflow list")
            states = [w.get("status", "unknown") for w in workflows[:20] if isinstance(w, dict)]
            results.append({"pipeline_id": pipeline["id"], "number": pipeline.get("number"),
                            "created_at": pipeline.get("created_at"), "statuses": states})
        latest = results[0] if results else None
        recent_failure = next((p for p in results if any(s in ("failed", "failing", "error") for s in p["statuses"])), None)
        report = {"repository": slug, "branch": branch, "latest": latest,
                  "recent_failure": recent_failure,
                  "historical_failure": bool(recent_failure and latest and recent_failure["pipeline_id"] != latest["pipeline_id"]),
                  "pipelines_checked": len(results)}
        self._cache[cache_key] = (self._clock(), report)
        return report
