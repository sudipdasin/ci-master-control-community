# Roadmap — Community first, hybrid control

## Stage 0: Safe public foundation (current)
- New public repository with independent history and real Apache-2.0 license
- Synthetic localhost-only server, example data, tests, security policy and contribution guidance
- No private repository inventory, secrets or Pro source

## Stage 1: Useful Community alpha
- User-managed multi-repository inventory and read-only CircleCI adapter
- Read-only pipeline history and failure discovery, explicitly label stale historical failures
- Credentials only on the backend; strong redaction, host allowlist, bounded requests and caching
- Accessible dashboard, actionable errors and portable local installation
- Separate approval request and immutable patch fingerprint; no auto-merge or auto-rerun

## Stage 2: Beta verification
- Threat model for untrusted CI logs, authenticated APIs and local/forwarded deployments
- Integration tests against appropriate real provider environments without unsolicited paid runs
- Compatibility testing on Linux; packaged install/update/uninstall and rollback
- Release notes, dependency notices, build attestations and complete test evidence

## Stage 3: Private Pro foundation
- Separate private repository and clean licensed upstream import
- One-way Community → Pro change intake through reviewed pull requests
- Private proprietary modules, license separation and dedicated pipelines
- AI-assisted diagnosis and team approval workflows only after security review

## Release policy
No automatic source changes, CI reruns, merges, deployments, releases or spending. Each consequential action needs informed human approval. No general-public beta claim until its gates are verified.
