# CI Master Control Community v0.1.0-alpha.2

**Status:** experimental Linux source-installer alpha, not production-ready.

## Download and install

Download the versioned ZIP from the GitHub Releases page, extract it, open a terminal in the extracted directory, then:

```sh
sh install.sh
python3 "$HOME/.local/share/ci-master-control-community/scripts/demo_server.py"
```

Visit http://127.0.0.1:8787/ locally. Python 3.10+ is required. No third-party Python dependencies are required.

## Security boundaries

Synthetic project data is shown by default. Live CircleCI monitoring is opt-in, read-only, and requires `CIRCLECI_TOKEN` in the server environment and an explicit `CI_COMMUNITY_REPOS` allowlist. Never commit tokens. The server binds only to localhost and must not be exposed publicly.

## Verification

```sh
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py --output dist
```

The release workflow also extracts the ZIP and smoke-tests its installation before publishing. These alpha.2 checks must be observed passing before declaring the new release validated.

## Uninstall

`sh uninstall.sh` prints the install path for manual review and removal; it does not automatically delete files.

## Limitations

Not a standalone executable, DEB, RPM, or AppImage. No public network authentication, automatic repairs, CI reruns, merges, or deployments. Real CircleCI integration and multi-distribution VM testing remain pending.
