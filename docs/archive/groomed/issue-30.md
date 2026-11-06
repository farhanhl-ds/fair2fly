# T-030: Add CI workflow running lint, type-check, and tests

**References:** [WORKFLOW.md "Before merging"](https://github.com/farhanhl-ds/fair2fly/blob/main/docs/WORKFLOW.md), [AGENTS.md "Commands"](https://github.com/farhanhl-ds/fair2fly/blob/main/AGENTS.md); NFR-008  
**Depends on:** #1

## Goal

Run the project's documented checks automatically on every pull request and on `main`, so a green result on the merged code does not depend on anyone remembering to run them. This is also where "re-test after `main` moved" happens, since QA's verdict only covers the commit it saw.

## Acceptance criteria

- **AC-1:** Given a pull request is opened or updated, then a workflow named `ci` runs install, lint, type-check, and test using the `make` targets documented in `AGENTS.md`, and the check fails if any of them exits non-zero.
- **AC-2:** Given a push to `main`, then the same workflow runs.
- **AC-3:** The workflow contains no check logic of its own: it only calls the documented commands, so CI and a local run cannot disagree.
- **AC-4:** The workflow uses the tool versions pinned in #1 rather than "latest", pins every third-party action to a version tag or commit SHA, sets `permissions: contents: read`, and uses no secrets.
- **AC-5:** The check name (`ci`) is documented in `README.md`, so the product owner can mark it required on `main`.

## Out of scope

- Services such as PostgreSQL and Redis in CI: added by the task that introduces tests needing them (#2 onward).
- Deployment or release workflows: #28 (T-028).
- Coverage thresholds, dependency-update bots, and matrix builds across versions.
- Branch protection settings: a repository setting the product owner applies (see Implementation notes).

## Edge and failure cases

- A cache must never turn a failing run green; the workflow starts from a clean checkout and may restore only dependency caches keyed on the lockfiles.
- A hung test must fail the run: set a job timeout (for example 15 minutes) so it cannot wait forever.
- A newer push to the same pull request cancels the superseded run (concurrency group).
- A missing `.env` must not break CI; the workflow relies on the defaults #1 established.

## Implementation notes

1. **One job:** `ci`, running `make install lint typecheck test`. It matches the single entry point chosen in #1. Split into parallel jobs only if the run becomes slow.
2. **File:** `.github/workflows/ci.yml`. Triggers: `pull_request` and `push` to `main`.
3. **Product owner step after this merges (not code):** in the repository settings, protect `main` so changes need a pull request, require the `ci` check, require the branch to be up to date before merging, and allow only the owner to merge. That makes the Before merging rule in `docs/WORKFLOW.md` enforced by GitHub, not by a prompt.

## Security and data impact (optional)

- Public repository: no secrets in the workflow, read-only token permissions.

---

This body is the spec written by the PM. Engineer and QA do not edit it; they post their evidence as issue comments (formats in `team/engineer.md` and `team/qa.md`). Status lives in labels, not here.
