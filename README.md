# fair2fly

fair2fly is a flight price intelligence platform: a spec-driven project for discovering flight deals, collecting persistent flight-price observations, and helping travelers make evidence-based booking decisions.

## Start here

**For humans**

1. [`docs/PRD.md`](docs/PRD.md) — product scope, users, and requirements.
2. [`docs/SRS.md`](docs/SRS.md) — testable requirements, invariants, and verification layers.
3. [`docs/TECHNICAL_DESIGN.md`](docs/TECHNICAL_DESIGN.md) — architecture, data concepts, and technical decisions.
4. [`docs/ROADMAP.md`](docs/ROADMAP.md) — milestones and exit criteria.
5. [`docs/DECISIONS.md`](docs/DECISIONS.md) — open and resolved decisions.

**For agents**

1. [`AGENTS.md`](AGENTS.md) — repository-wide rules and boundaries.
2. [`docs/WORKFLOW.md`](docs/WORKFLOW.md) — roles, loop limits, routing, and handoffs.
3. GitHub Issues (D-026): canonical tracker. Packet format: [`docs/TASK_TEMPLATE.md`](docs/TASK_TEMPLATE.md).

## Getting started

### Prerequisites

- Linux, macOS, or WSL
- [uv](https://docs.astral.sh/uv/) 0.13.7 (it can provide Python 3.14)
- Node.js 26.13.0 with npm 11.20.0 (see `frontend/.nvmrc`)
- GNU Make 4.4.1

### Setup

```sh
cp .env.example .env
make install
make dev
```

The API listens on `http://localhost:${API_PORT}/health` and the web app on
`http://localhost:${WEB_PORT}`. The defaults are 8000 and 3000; change the ports
in `.env`. `.env` is ignored by git, so each git worktree can use different
ports and run at the same time.

### Commands

| Command | Purpose |
|---|---|
| `make install` | Install backend and frontend dependencies from the committed lockfiles |
| `make dev` | Run the FastAPI API and Next.js app in development mode |
| `make test` | Run backend and frontend tests |
| `make lint` | Run Ruff, ESLint, and Prettier checks |
| `make typecheck` | Run mypy and `tsc --noEmit` |

The database migration command is added by T-004 (issue #4) and the end-to-end
test command by T-025 (issue #25).

### Pinned versions

| Tool | Version |
|---|---|
| Python | 3.14 (`backend/pyproject.toml`) |
| uv | 0.13.7 |
| FastAPI | 0.162.0 |
| Uvicorn | 0.54.0 |
| Ruff | 0.17.4 |
| mypy | 2.4.1 |
| pytest | 9.2.0 |
| Node.js | 26.13.0 (`frontend/.nvmrc`) |
| Next.js | 16.4.5 |
| React | 19.3.1 |
| TypeScript | 5.9.3 (latest supported by the Next.js ESLint toolchain) |
| ESLint | 9.39.5 |
| Prettier | 3.9.10 |
| Vitest | 5.1.0 |

## Continuous integration

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) defines the `ci` workflow
and its single `ci` job. It runs on every pull request that is opened, reopened,
or updated, and on every push to `main`. The job calls the same root `Makefile`
entry points as a local checkout — `make install`, `make lint`,
`make typecheck`, and `make test` — so CI and local runs cannot disagree.

After this workflow merges, the product owner must protect `main` in the
repository settings: require a pull request, require the `ci` status check,
require the branch to be up to date before merging, and allow only the owner to
merge.

## Documentation map

| File | Purpose |
|---|---|
| `AGENTS.md` | Agent constitution: source of truth, rules, boundaries, definition of done |
| `docs/PRD.md` | Product requirements, users, scope, risks, and success measures |
| `docs/SRS.md` | Functional/non-functional requirements, business rules, and testing invariants |
| `docs/TECHNICAL_DESIGN.md` | Architecture, components, data concepts, security, and deployment |
| `docs/ROADMAP.md` | Milestones, sequencing, exit criteria, and scope control |
| `docs/archive/TASKS.md` | Archived seed backlog; GitHub Issues is the canonical tracker (D-026) |
| `docs/TASK_TEMPLATE.md` | Standard task packet with acceptance criteria and evidence |
| `docs/DECISIONS.md` | Single decision log for open and resolved choices |
| `docs/WORKFLOW.md` | Development-time agent graph, loops, routing, and model policy |

## Status and decision policy

This is an initial specification baseline. Items marked **Open decision**, **Proposed**, or **To validate** must be resolved before the affected implementation begins. Resolve and record decisions in [`docs/DECISIONS.md`](docs/DECISIONS.md). Do not turn assumptions into facts without recording the decision.

## Status snapshot (2026-11-06)

- The repository has a runnable FastAPI and Next.js skeleton with install, development, test, lint, and type-check commands; product features are not implemented yet.
- Decision state, including accepted Milestone 0 outcomes and everything still open, lives only in [`docs/DECISIONS.md`](docs/DECISIONS.md). A decision gates only the tasks in its *Affects* column.
- Platform decisions (D-010-D-013) are resolved just before the first task each one affects. Agent model routing (D-023/D-024) is deferred and gates nothing.

## Product principle

The platform's differentiator is its persistent, structured flight-price history, not one-time flight search. Analytics and AI recommendations must be grounded in observed data and communicate uncertainty.
