# CI Master Control — Community

[![Latest release](https://img.shields.io/badge/Download-Latest%20Release-orange)](https://github.com/sudipdasin/ci-master-control-community/releases)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

> **Public alpha v0.1.0-alpha.3 is available.** Experimental local-first CI monitoring preview; not production-ready.

<!-- LATEST-RELEASE:START -->
## Latest published release: v0.1.0-alpha.3
**[Release notes and downloads](https://github.com/sudipdasin/ci-master-control-community/releases/tag/v0.1.0-alpha.3)** · Prerelease

| Asset | Download |
| --- | --- |
| `ci-master-control-community-v0.1.0-alpha.3-linux-source.zip` | [Download](https://github.com/sudipdasin/ci-master-control-community/releases/download/v0.1.0-alpha.3/ci-master-control-community-v0.1.0-alpha.3-linux-source.zip) |
| `ci-master-control-community_0.1.0-alpha.3_all.deb` | [Download](https://github.com/sudipdasin/ci-master-control-community/releases/download/v0.1.0-alpha.3/ci-master-control-community_0.1.0-alpha.3_all.deb) |
<!-- LATEST-RELEASE:END -->

Python 3.10+ is required. The application is an experimental localhost-only preview, not a standalone native binary. Do not expose port 8787 publicly.

### Install the Debian package

```sh
sudo apt install ./ci-master-control-community_0.1.0-alpha.3_all.deb
ci-master-control-community
```

### Install from the source ZIP

Extract the ZIP, enter its top-level directory, then run:

```sh
sh install.sh
python3 "$HOME/.local/share/ci-master-control-community/scripts/demo_server.py"
```

Open **http://127.0.0.1:8787/** on the same machine. Synthetic sample data is displayed by default.

[Read the alpha release guide](docs/ALPHA_RELEASE.md).

## What works in the alpha

- Localhost-only preview dashboard with synthetic sample projects.
- Optional **read-only CircleCI monitoring** for explicitly authorized repositories.
- Recent pipeline/workflow statuses and historical failure detection.
- Read-only CLI inspector; no automatic repairs, CI reruns, merges, or deployments.
- Local installation and non-destructive uninstall helper.

**Verification:** Alpha 3 passed its GitHub Actions source validation, Python tests, ZIP installation smoke test, extracted Debian dashboard health/inventory checks, and release asset publication. The overall workflow ended in failure at the separate post-release homepage synchronization step; the publication and package checks succeeded. Full system-wide installation and multi-distribution VM compatibility remain unverified.

### Optional live monitoring (experimental)

The dashboard starts with live monitoring **disabled**. Supply a server-side CircleCI API token via a local secret manager and an allowlist of repositories you own or are authorized to monitor:

```sh
# Set CIRCLECI_TOKEN securely in the environment first.
CI_COMMUNITY_REPOS=your-org/your-repo python3 scripts/demo_server.py
```

Do not place tokens in source control, browser URLs, screenshots, or shell history. The server stays on `127.0.0.1`. See [read-only integration notes](docs/CIRCLECI_READONLY.md).

### Tests

```sh
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
```

## Editions and development

- **Community** (this public repository): free Apache-2.0 monitoring, safe diagnostics and human approval. See [roadmap](docs/ROADMAP.md).
- **Pro** (future private edition): optional advanced analysis and integrations. Synchronization, when implemented, flows **Community → Pro** only.
- **Private operations:** Existing private controller repositories, their history, credentials and inventories are not included.

## Security and privacy

Never commit credentials, private CI logs, real customer configuration or sensitive project information. External CI responses are untrusted. **Do not expose this alpha server on a public interface or through a public port forward**; it has no internet-facing authentication. See [security policy](SECURITY.md).

## Contributing and license

Licensed under the [Apache License 2.0](LICENSE). [Contributions](CONTRIBUTING.md) and bug reports are welcome. The current release is an **early alpha**, not a production or beta release.
