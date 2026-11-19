# Edition synchronization and privacy boundaries

## Repositories

- Public source of truth for Community: `sudipdasin/ci-master-control-community`
- Private operational dashboard: `sudipdasin/CI-Master-Control` — **not** an upstream for public publication
- Future private commercial repository: `sudipdasin/ci-master-control-pro` (not yet created)

## One-way flow

```text
Public Community ── reviewed upstream changes ──▶ Private Pro
        ▲                                      │
        └────────────── NEVER ◀────────────────┘
```

There is **no automatic cross-repository push or replication** in this initial stage. Such automation must first have a dedicated least-privilege credential, immutable upstream source revision, explicit review before merges, no access to Pro secrets from Community workflows, and safety tests against accidental disclosure.

## Manual sync procedure for future Pro repository

1. Fetch the public Community repository as a read-only Git remote in a private Pro workspace.
2. Review upstream changes and provenance, including licenses and dependencies.
3. Apply approved Community commits to an isolated Pro integration branch.
4. Run private Pro tests in the private environment and inspect the resulting diff.
5. Open a private review PR; require human approval before merging.
6. Never open a Pro-to-Community PR containing private modules or proprietary resources.

## Release controls

The existing private operational history, configuration and backup directories must never be cloned into the public repository. Publish Community releases only from clean Community history after test evidence and privacy checks. Public development contributions may be freely reviewed without initiating paid CI workflows.
