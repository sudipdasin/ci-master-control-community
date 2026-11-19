# Security policy

**Status:** Early development scaffold, not approved for internet-facing production use.

Please report vulnerabilities privately using GitHub's **Report a vulnerability** feature when enabled, or contact the repository maintainer through a private channel. Do not put real credentials, private logs or exploit data in public issues.

- No credentials are needed for the synthetic preview.
- The preview listens only on `127.0.0.1`, uses no external CI APIs and rejects write methods.
- Do not expose the preview using a public reverse proxy, public Codespaces forwarded port or other internet-facing endpoint.
- Future CI tokens must be least-privilege and server-side; user-provided logs must be treated as untrusted.
- Repairs and credit-consuming CI work require explicit human approval; merging/deployment remain manual.
