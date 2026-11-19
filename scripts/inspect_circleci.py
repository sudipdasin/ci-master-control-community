#!/usr/bin/env python3
"""Explicitly invoked read-only CLI for user-owned CircleCI pipeline statuses."""
import argparse
import json
import os
import sys
from readonly_circleci import ProviderError, Reader


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read recent CircleCI statuses; never triggers CI")
    parser.add_argument("repository", help="GitHub owner/repo shown in your CircleCI project")
    parser.add_argument("--branch", default="main", help="Branch to inspect (default: main)")
    args = parser.parse_args(argv)
    token = os.environ.get("CIRCLECI_TOKEN", "")
    if not token:
        print("CIRCLECI_TOKEN must be set locally; no request made.", file=sys.stderr)
        return 2
    try:
        report = Reader(token).latest(args.repository, branch=args.branch)
    except ProviderError as exc:
        print(f"CircleCI read failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
