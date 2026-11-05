# Flight Price Intelligence Platform

A spec-driven project for discovering flight deals, collecting persistent flight-price observations, and helping travelers make evidence-based booking decisions.

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
3. GitHub Issues (D-026) once the repository is connected — canonical tracker. Until then: [`docs/TASKS.md`](docs/TASKS.md) seed backlog and [`docs/TASK_TEMPLATE.md`](docs/TASK_TEMPLATE.md) packet format.

## Documentation map

| File | Purpose |
|---|---|
| `AGENTS.md` | Agent constitution: source of truth, rules, boundaries, definition of done |
| `docs/PRD.md` | Product requirements, users, scope, risks, and success measures |
| `docs/SRS.md` | Functional/non-functional requirements, business rules, and testing invariants |
| `docs/TECHNICAL_DESIGN.md` | Architecture, components, data concepts, security, and deployment |
| `docs/ROADMAP.md` | Milestones, weekly sequencing, exit criteria, and scope control |
| `docs/TASKS.md` | Backlog seed with IDs, references, and dependencies (canonical tracker: GitHub Issues, D-026) |
| `docs/TASK_TEMPLATE.md` | Standard task packet with acceptance criteria and evidence |
| `docs/DECISIONS.md` | Single decision log for open and resolved choices |
| `docs/WORKFLOW.md` | Development-time agent graph, loops, routing, and model policy |

## Status and decision policy

This is an initial specification baseline. Items marked **Open decision**, **Proposed**, or **To validate** must be resolved before the affected implementation begins. Resolve and record decisions in [`docs/DECISIONS.md`](docs/DECISIONS.md). Do not turn assumptions into facts without recording the decision.

## Status snapshot (2026-11-05)

- Phase 0 complete where it matters: flight-data provider **D-001** (Google Flights data via SerpApi) and airport hubs **D-002** (CGK, DPS, SUB, KNO, JOG, UPG, BDO) are accepted.
- Development-workflow decisions accepted: **D-025** (worktree/branch-per-issue agent runtime) and **D-026** (GitHub Issues becomes the canonical tracker on repository connection).
- Repository is initialized on `main` with specs only; no application code yet.
- Next: resolve **D-010–D-013** (auth, exchange rates, email, hosting) and **D-023/D-024** (model routing) — both required before **T-001** — then Week-1 foundation work starts.
- All accepted reasoning and the full historical record of every decision live in [`docs/DECISIONS.md`](docs/DECISIONS.md) (single decision log).

## Product principle

The platform's differentiator is its persistent, structured flight-price history, not one-time flight search. Analytics and AI recommendations must be grounded in observed data and communicate uncertainty.
