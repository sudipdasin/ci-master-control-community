# CI Master Control — Community

[![Alpha release](https://img.shields.io/badge/Download-v0.1.0--alpha.1-orange)](https://github.com/sudipdasin/ci-master-control-community/releases/tag/v0.1.0-alpha.1)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

> **Public alpha v0.1.0-alpha.1 is available.** Experimental local-first CI monitoring preview; not production-ready.

## Download the Community alpha

**[⬇ Download v0.1.0-alpha.1 (ZIP)](https://github.com/sudipdasin/ci-master-control-community/archive/refs/tags/v0.1.0-alpha.1.zip)** · **[TAR.GZ](https://github.com/sudipdasin/ci-master-control-community/archive/refs/tags/v0.1.0-alpha.1.tar.gz)** · **[Release page and notes](https://github.com/sudipdasin/ci-master-control-community/releases/tag/v0.1.0-alpha.1)**

These are downloadable **source distributions** for Linux testers, not standalone executable binaries. Python 3.10+ is required. The release includes a local user-space installer and uninstall helper.

### Install and run

Download and extract the ZIP/TAR.GZ, open a terminal in the extracted directory, then:

```sh
sh install.sh
python3 "$HOME/.local/share/ci-master-control-community/scripts/demo_server.py"
```

Open **http://127.0.0.1:8787/** locally. The preview is bound to localhost and starts with synthetic sample data.

[Read the alpha release guide](docs/ALPHA_RELEASE.md) · [Report bugs](https://github.com/sudipdasin/ci-master-control-community/issues/new)

## What works in the alpha

- Localhost-only preview dashboard with synthetic sample projects.
- Optional **read-only CircleCI monitoring** for explicitly authorized repositories.
- Recent pipeline/workflow statuses and historical failure detection.
- Read-only CLI inspector; no automatic repairs, CI reruns, merges, or deployments.
- Local installation and non-destructive uninstall helper.

**Verification:** 33 Python tests passed in GitHub Codespaces on the release branch, along with compilation and isolated installation checks. Real CircleCI integration and multi-distribution VM compatibility are not yet verified.

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
