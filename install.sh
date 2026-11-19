#!/bin/sh
set -eu
# Installs only to a user-owned local directory; never modifies system services.
PREFIX="${1:-$HOME/.local/share/ci-master-control-community}"
case "$PREFIX" in
  /*) ;;
  *) echo "Install path must be absolute" >&2; exit 2 ;;
esac
if [ -e "$PREFIX" ]; then
  echo "Destination already exists; refusing overwrite: $PREFIX" >&2
  exit 2
fi
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required" >&2; exit 2; }
mkdir -p "$PREFIX/scripts" "$PREFIX/config"
cp scripts/demo_server.py scripts/readonly_circleci.py scripts/inspect_circleci.py "$PREFIX/scripts/"
cp config/projects.example.json "$PREFIX/config/"
cp VERSION LICENSE README.md "$PREFIX/"
printf 'Installed to %s\nRun: python3 "%s/scripts/demo_server.py"\n' "$PREFIX" "$PREFIX"
