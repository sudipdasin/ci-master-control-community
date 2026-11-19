# CI Master Control Community v0.1.0-alpha.1

**Audience:** developers and early testers on a local Linux machine. **Status:** experimental, read-only, not production-ready.

## Installation

Download the source archive from the repository or clone it. Requires Python 3.10+ and POSIX shell.

```sh
sh install.sh
python3 "$HOME/.local/share/ci-master-control-community/scripts/demo_server.py"
```

Open http://127.0.0.1:8787/ locally. This starts with synthetic sample data.

## Opt-in CircleCI read-only status

Provide `CIRCLECI_TOKEN` through a local secret manager and `CI_COMMUNITY_REPOS` as a comma-separated list of `owner/repo` values, then start the server. No CI build, rerun, PR or merge is triggered.

## Verification

```sh
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
```

No real CircleCI integration tests or virtual-machine compatibility tests have yet been verified. This release candidate must not be described as fully validated.

## Uninstall

```sh
sh uninstall.sh
```

The uninstall helper prints the install directory for manual removal; it does not delete files automatically.

## Safety

The HTTP server listens only on 127.0.0.1 and has no public-network authentication. Do not forward its port publicly or use a public reverse proxy. Never paste a CI token into GitHub issues or commit it to the repository. Read-only monitoring is the only live integration in this alpha.

## Release gates

A GitHub Release/tag has **not** been published by merely adding these files. A release should be published only after checks, security review and appropriate human release approval.
