#!/bin/sh
set -eu
# Explicit path, no wildcard deletion or privileged operations.
PREFIX="${1:-$HOME/.local/share/ci-master-control-community}"
case "$PREFIX" in
  /*) ;;
  *) echo "Install path must be absolute" >&2; exit 2 ;;
esac
if [ ! -f "$PREFIX/VERSION" ] || [ ! -f "$PREFIX/scripts/demo_server.py" ]; then
  echo "Not a recognizable CI Master Control Community installation; refusing removal" >&2
  exit 2
fi
echo "To uninstall, manually review and remove this directory: $PREFIX"
echo "No files were deleted automatically."
