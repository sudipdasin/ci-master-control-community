# Changelog

## 0.1.0-alpha.3 — 2026-11-19 (release candidate)

- Fix Debian packaging by including the synthetic sample project inventory.
- Resolve the inventory path correctly when running from an extracted or installed Debian package.
- Add packaging regression assertions for the extracted inventory.
- Require live HTTP health and inventory smoke tests of the extracted Debian payload before publication.
- Maintain immutable release tags and preserve Alpha 2 for rollback.

**Release gate:** Alpha 3 must pass its own GitHub Actions test/build/package workflow before any assets are published. Pro verification remains independent and is not implied by a Community release.

## 0.1.0-alpha.2 — 2026-11-19 (candidate)

- Reproducible versioned Linux source-installer ZIP builder with automated archive tests.
- Publishing workflow validates source, unit tests, and extracted-package installation before creating the versioned GitHub pre-release and attaching its ZIP asset.
- Preserves immutable tags and avoids overwriting published release versions.
- Continues localhost-only dashboard and opt-in read-only CircleCI integration.

**Validation pending:** Codespace/VM tests of alpha.2 branch and GitHub workflow run. Real CircleCI provider integration remains unverified.

## 0.1.0-alpha.1 — 2026-11-19

First Community alpha preview: localhost dashboard, synthetic example projects, optional server-side read-only CircleCI pipeline monitoring, historical failure flag, CLI inspector, and HTTP security smoke tests.
