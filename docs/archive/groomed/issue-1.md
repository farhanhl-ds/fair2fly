# T-001: Initialize repository and local development environment

**References:** [Technical design §2 and §12](https://github.com/farhanhl-ds/fair2fly/blob/main/docs/TECHNICAL_DESIGN.md), [AGENTS.md "Commands"](https://github.com/farhanhl-ds/fair2fly/blob/main/AGENTS.md); NFR-005, NFR-008, NFR-010  
**Depends on:** none

## Goal

Give the project a runnable, lintable, testable skeleton with one documented command per action, so every later task, and every agent working in its own worktree, starts from the same exact commands. `AGENTS.md` currently has no commands and QA has nothing to run.

## Acceptance criteria

- **AC-1:** Given a clean clone and the documented prerequisites, when the documented install command is run, then backend and frontend dependencies install with no other manual step.
- **AC-2:** Given installed dependencies, when the documented dev command is run, then `GET /health` on the API returns HTTP 200 and the Next.js page loads, each on a port taken from an environment variable with a default from `.env.example`. Two git worktrees can run this at once with different ports.
- **AC-3:** When the documented test command is run, then backend and frontend each run at least one passing test, and the command exits non-zero if any test fails.
- **AC-4:** When the documented lint command is run, then lint and format checks run for backend and frontend, and the command exits non-zero on a violation.
- **AC-5:** When the documented type-check command is run, then Python and TypeScript type checks run, and the command exits non-zero on a type error.
- **AC-6:** Given the repository, then `.env.example` lists every setting the code reads with no real values; `.env`, virtual environments, `node_modules`, and caches are ignored; and `git ls-files` shows no secret, local artifact, or absolute path.
- **AC-7:** Given `AGENTS.md` and `README.md`, then `AGENTS.md` lists the exact install, dev, test, lint, and type-check commands and states that the migration command is added by #4 and the end-to-end command by #25 (no guessed commands), and `README.md` has a Getting started section with prerequisites and the pinned tool versions.

## Out of scope

- Docker Compose, PostgreSQL, Redis, Celery: #2 (T-002).
- Database schema, migrations, migration command: #4 (T-004).
- End-to-end test tooling and command: #25 (T-025).
- Structured logging and metrics: #10 (T-010).
- CI workflow (GitHub Actions running lint, type-check, and tests): #30 (T-030).
- Any product feature, provider code, or domain model.

## Edge and failure cases

- Each of test, lint, and type-check must fail non-zero on a deliberate violation. QA verifies by breaking one test, one lint rule, and one type, then restoring them.
- An empty test suite must not pass silently (pytest exits non-zero when it collects nothing; configure the frontend runner the same way).
- A missing `.env` gives defaults or a clear error, not a stack trace.
- A port already in use fails with a readable message.

## Implementation notes

Decisions made while grooming, because later issues depend on them:

1. **Monorepo layout:** `backend/` and `frontend/` at the root. It matches the modular monolith in the technical design and maps onto the services in #2.
2. **Single entry point:** a root `Makefile` with `install`, `dev`, `test`, `lint`, `typecheck`, delegating to each side. One set of commands for engineers, QA, and `AGENTS.md`. Assumes Linux, macOS, or WSL.
3. **Backend tooling:** `uv` (lockfile committed), `ruff` for lint and format, `mypy` for types, `pytest`. Python version pinned in `pyproject.toml`.
4. **Frontend tooling:** `npm` with a committed lockfile, ESLint and Prettier, `tsc --noEmit`, Vitest. Node version pinned (`.nvmrc` or `engines`).
5. **Skeletons belong here:** the roadmap lists the FastAPI and Next.js skeletons in Week 1, no other task creates them, and #2 expects them. Keep them minimal: one health endpoint, one page, one test each.
6. **Ports from environment:** `API_PORT` and `WEB_PORT`, defaults in `.env.example`, so parallel worktrees do not collide.
7. **Versions:** pin the latest stable versions supported by FastAPI and Next.js at the time of work, and record them in `README.md`.
8. **Project name:** `fair2fly` in `pyproject.toml`, `package.json`, and the README title.
9. **AGENTS.md conflict:** it says T-001 must add the migration and end-to-end commands, which cannot exist before #4 and #25. AC-7 resolves this, and the engineer updates that sentence in this task.

## Must not change (optional)

- The specifications under `docs/`, and all rules in `AGENTS.md` other than the Commands section.

## Security and data impact (optional)

- Public repository: nothing sensitive in any file or commit. `.env.example` has names only.

---

This body is the spec written by the PM. Engineer and QA do not edit it; they post their evidence as issue comments (formats in `team/engineer.md` and `team/qa.md`). Status lives in labels, not here.
