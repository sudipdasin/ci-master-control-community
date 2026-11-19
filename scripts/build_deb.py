#!/usr/bin/env python3
"""Build a no-root, architecture-independent Debian alpha package."""
import argparse
import pathlib
import re
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKAGE = "ci-master-control-community"
FILES = ["demo_server.py", "readonly_circleci.py", "inspect_circleci.py"]

def build(root: pathlib.Path, output: pathlib.Path) -> pathlib.Path:
    version = (root / "VERSION").read_text().strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+-alpha\.[0-9]+", version):
        raise ValueError("Invalid alpha version")
    if not shutil.which("dpkg-deb"):
        raise RuntimeError("dpkg-deb is required (Debian/Ubuntu build host)")
    output.mkdir(parents=True, exist_ok=True)
    artifact = output / f"{PACKAGE}_{version}_all.deb"
    with tempfile.TemporaryDirectory(prefix="cmc-deb-") as temp:
        stage = pathlib.Path(temp)
        control = stage / "DEBIAN"
        control.mkdir(mode=0o755)
        control.chmod(0o755)
        (control / "control").write_text(
            f"Package: {PACKAGE}\nVersion: {version}\nSection: utils\n"
            "Priority: optional\nArchitecture: all\nDepends: python3 (>= 3.10)\n"
            "Maintainer: CI Master Control Community contributors\n"
            "Description: Experimental localhost-only CI monitoring dashboard\n"
            " Read-only Community alpha; not for public-network deployment.\n"
        )
        app = stage / "usr/share" / PACKAGE
        app.mkdir(parents=True)
        app.chmod(0o755)
        for name in FILES:
            shutil.copyfile(root / "scripts" / name, app / name)
        docs = stage / "usr/share/doc" / PACKAGE
        docs.mkdir(parents=True)
        docs.chmod(0o755)
        for name in ["README.md", "LICENSE", "CHANGELOG.md"]:
            shutil.copyfile(root / name, docs / name)
        binpath = stage / "usr/bin" / PACKAGE
        binpath.parent.mkdir(parents=True)
        binpath.parent.chmod(0o755)
        binpath.write_text(
            "#!/bin/sh\nexec /usr/bin/python3 "
            "/usr/share/ci-master-control-community/demo_server.py \"$@\"\n"
        )
        binpath.chmod(0o755)
        (control / "control").chmod(0o644)
        for directory in [stage, stage / "usr", stage / "usr/share", stage / "usr/share/doc"]:
            directory.chmod(0o755)
        subprocess.run(["dpkg-deb", "--build", "--root-owner-group", str(stage), str(artifact)], check=True)
    return artifact

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("dist"))
    args = parser.parse_args()
    print(build(ROOT, args.output.resolve()))
