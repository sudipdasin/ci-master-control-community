# CI Master Control Community v0.1.0-alpha.3

**Status:** experimental Linux Community alpha, not production-ready.

## Downloads

- [Debian / Ubuntu .deb installer](https://github.com/sudipdasin/ci-master-control-community/releases/download/v0.1.0-alpha.3/ci-master-control-community_0.1.0-alpha.3_all.deb)
- [Linux source ZIP](https://github.com/sudipdasin/ci-master-control-community/releases/download/v0.1.0-alpha.3/ci-master-control-community-v0.1.0-alpha.3-linux-source.zip)
- [Release notes](https://github.com/sudipdasin/ci-master-control-community/releases/tag/v0.1.0-alpha.3)

## Debian / Ubuntu install

```sh
sudo apt install ./ci-master-control-community_0.1.0-alpha.3_all.deb
ci-master-control-community
```

Open http://127.0.0.1:8787/ locally. Remove the package with `sudo apt remove ci-master-control-community`.

## Source ZIP install

Extract the ZIP, enter the extracted directory, then:

```sh
sh install.sh
python3 "$HOME/.local/share/ci-master-control-community/scripts/demo_server.py"
```

Python 3.10+ is required. No third-party Python dependencies are required.

## Security boundaries

Synthetic project data is shown by default. Live CircleCI monitoring is opt-in, read-only, and requires `CIRCLECI_TOKEN` in the server environment and an explicit `CI_COMMUNITY_REPOS` allowlist. Never commit tokens. The server binds only to localhost and must not be exposed publicly.

## Verification

The release workflow must pass Python regression tests, source-ZIP installation smoke tests, and an extracted Debian package runtime smoke test covering `/health` and `/api/inventory` before publication. Results for Alpha 3 must be verified from its own GitHub Actions run; earlier Alpha 2 results do not count as Alpha 3 validation. Full system-wide package installation and multi-distribution VM validation remain unverified.

```sh
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py --output dist
python3 scripts/build_deb.py --output dist
```

## Fixes since Alpha 2

- Include the synthetic inventory in the Debian installer and resolve it from the installed layout.
- Add regression assertions for the extracted inventory file.
- Gate publishing on the packaged dashboard responding successfully to health and inventory endpoints.

## Limitations

Not a standalone native executable, RPM, or AppImage. No public-network authentication, automatic repairs, CI reruns, merges, or deployments. Real CircleCI integration and multi-distribution VM testing remain pending.
