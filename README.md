# CI Master Control — Community

> **Development scaffold. Not yet a beta release.** Free, open-source local-first CI monitoring and failure-analysis platform in development.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

CI Master Control aims to provide multi-repository CI monitoring, historical pipeline investigation, safe failure diagnosis, and **human-approved repairs**. No CI changes, spending, merges or deployments should happen without an explicit human decision.

## Current capabilities

This public repository contains a self-hosted synthetic preview, an example project inventory, and an **experimental opt-in read-only CircleCI monitoring panel**. When configured, the backend reads recent pipeline and workflow statuses from CircleCI. It does not generate repairs, run pipelines, or ship installable releases. Real-provider integration remains unverified. It does not contain private repository inventory, credentials, or the existing private controller's source history.

### Run locally

Requires Python 3.10+; no third-party dependencies.

```bash
python3 scripts/demo_server.py
```

Open http://127.0.0.1:8787/ from the same machine. The preview binds to localhost. To choose a port: `CI_COMMUNITY_PREVIEW_PORT=8790 python3 scripts/demo_server.py`.

### Optional live monitoring (experimental)

The dashboard starts with live monitoring **disabled**. To opt in, supply a server-side CircleCI API token and an explicit comma-separated list of repositories you own or are authorized to monitor:

```bash
# Set CIRCLECI_TOKEN using your local secret manager, not a committed file.
CI_COMMUNITY_REPOS=your-org/your-repo python3 scripts/demo_server.py
```

The server requires `CIRCLECI_TOKEN` in its environment before enabling live requests. Do not put a token in the browser, Git commits, screenshots, or shell history. The dashboard remains bound to `127.0.0.1`. It currently supports the GitHub-backed CircleCI project slug format only, and does not validate real provider behavior yet. See [read-only integration notes](docs/CIRCLECI_READONLY.md).

### Tests

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
```

## Editions and development

- **Community** (this public repository): essential monitoring, safe diagnostics, manual approval, and security by default. See [Roadmap](docs/ROADMAP.md).
- **Pro** (future private edition): optional advanced analysis, additional integrations, teamwork and audit capabilities. Any synchronization will flow **Community → Pro**, never Pro → Community.
- **Private operations:** The pre-existing private control plane is separate and never automatically copied into this repository.

## Security and privacy

Never commit tokens, private CI logs, real customer configuration, local path inventories, or sensitive project information. All input from external CI logs is untrusted. Until authentication, isolation and permissions are audited, do not expose the preview on public interfaces or forward its port publicly. See [Security policy](SECURITY.md).

## License

Apache License 2.0. See [LICENSE](LICENSE). This license covers code published in this repository, not unrelated private code or third-party work.

Contributions are welcome once the contribution guidelines and real provider adapters are developed. Current status is an **early development scaffold**, not a production release.
