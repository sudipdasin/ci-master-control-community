#!/usr/bin/env python3
"""Deterministic, versioned Community source-installer ZIP builder."""
from pathlib import Path
import argparse
import zipfile

FILES = (
    "VERSION", "LICENSE", "README.md", "CHANGELOG.md", "SECURITY.md",
    "install.sh", "uninstall.sh", "config/projects.example.json",
    "scripts/demo_server.py", "scripts/readonly_circleci.py",
    "scripts/inspect_circleci.py", "docs/ALPHA_RELEASE.md",
    "docs/CIRCLECI_READONLY.md",
)

def build(root: Path, destination: Path) -> Path:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not version or any(c not in "0123456789abcdefghijklmnopqrstuvwxyz.-" for c in version):
        raise ValueError("Invalid VERSION")
    package = f"ci-master-control-community-v{version}"
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / f"{package}-linux-source.zip"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for rel in FILES:
            source = root / rel
            if not source.is_file() or source.is_symlink():
                raise FileNotFoundError(f"Missing or unsafe package input: {rel}")
            info = zipfile.ZipInfo(f"{package}/{rel}", date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o644 << 16)
            z.writestr(info, source.read_bytes())
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output", type=Path, default=Path("dist"))
    args = parser.parse_args()
    print(build(args.root.resolve(), args.output.resolve()))
