# Experimental read-only CircleCI adapter

The optional CLI can inspect up to four recent pipeline histories and their workflows for a GitHub-backed CircleCI project. It does **not** start pipelines, rerun jobs, modify GitHub repositories or create repair PRs. The dashboard still displays only synthetic data; the adapter has **not** yet been integrated into the dashboard.

## Safe local use

1. Create or obtain an appropriate CircleCI **personal/API v2-compatible token** with the narrowest supported read scope. Check the latest CircleCI guidance: API v2 does not accept legacy project API tokens; some manually created personal tokens may grant broad privileges. Protect and rotate tokens accordingly.
2. Store the token privately outside the Git repository. Do not paste it in issues, chat, logs or command history. Set it in your local process environment using your preferred secret manager.
3. Run:

```bash
python3 scripts/inspect_circleci.py YOUR_ORG/YOUR_REPOSITORY --branch main
```

The result distinguishes the **latest pipeline** from a **historical failure** in an older pipeline, even if the latest pipeline has no workflows. CircleCI itself may return pipelines in unexpected order; this early adapter assumes the provider's standard most-recent-first response and is **experimental**.

## Safeguards

- GET-only fixed CircleCI API host and endpoints; no redirects.
- Repository slug, branch and pipeline UUID validation.
- 8-second per-request timeout, 256 KiB maximum response, maximum 4 inspected pipelines per call.
- 30-second in-process result cache.
- No raw provider error bodies or tokens returned in the JSON report.
- Mocked tests available via `python3 -m unittest discover -s tests -v`.

**Limitations:** Not validated with a real CircleCI account in this environment. Does not support GitHub App/new `circleci/<org-id>/<project-id>` project slugs, pagination, federated authentication, advanced provenance checks or long-term storage yet. Do not use it as an authoritative operational security or release gate.
