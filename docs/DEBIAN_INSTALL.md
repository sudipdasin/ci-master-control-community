# Debian / Ubuntu Community alpha package

The `.deb` package is an **experimental architecture-independent Python application**, not a native compiled binary. It installs a launcher named `ci-master-control-community` and read-only dashboard files under `/usr/share/ci-master-control-community`.

Install the downloaded package on Debian/Ubuntu with:

```sh
sudo apt install ./ci-master-control-community_0.1.0-alpha.2_all.deb
ci-master-control-community
```

Open http://127.0.0.1:8787/ on the same machine.

Remove using `sudo apt remove ci-master-control-community`.

**Security:** The app does not install a system service, does not start automatically, and binds only to localhost. Do not forward the port publicly. The CircleCI integration remains opt-in and read-only. Python 3.10+ is required.

The package is built and inspected with `dpkg-deb` in CI. Actual interactive installation on several Linux distributions remains a separate release-validation task.
