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

## Status snapshot (2026-11-05)

- The repository is initialized on `main` with specifications only; there is no application code yet.
- Decision state, including accepted Milestone 0 outcomes and everything still open, lives only in [`docs/DECISIONS.md`](docs/DECISIONS.md). A decision gates only the tasks in its *Affects* column.
- Platform decisions (D-010-D-013) are resolved just before the first task each one affects. Agent model routing (D-023/D-024) is deferred and gates nothing.

## Product principle

The platform's differentiator is its persistent, structured flight-price history, not one-time flight search. Analytics and AI recommendations must be grounded in observed data and communicate uncertainty.
