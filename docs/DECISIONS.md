# Decision Log

**Status:** Living document.  
**Purpose:** Single source of truth for open and resolved product, provider, platform, API, and development-workflow decisions.  
**Rule:** Resolve a decision before implementing work that depends on it. Record the date, owner, rationale, consequences, and affected requirements/tasks.

Status values: `open`, `proposed`, `accepted`, `superseded`.

Decision IDs are stable from tracker activation (D-026) onward. Before tracker activation, on 2026-11-05, the product owner directed a one-time renumbering so decision and backlog IDs are dense and ASCII-ordered from the start; the mapping is recorded in the tracker decision (D-026). After activation, new decisions receive new IDs rather than renumbering existing entries.

## Open decisions

Phase-0 provider and hub decisions are accepted (D-001, D-002, 2026-11-05); see Resolved decisions.

### Product and provider

| ID | Decision | Status | Owner | Affects |
|---|---|---|---|---|
| D-003 | Exact supported flexible-date and flexible-destination constraints | open | product owner | FR-004, FR-005, T-015, T-016 |
| D-004 | Collection intervals, quota allocation, adaptive-monitoring policy, and tracking-mode rollout | open | product owner | FR-011–FR-013, T-008, T-016 |
| D-005 | Minimum sample size, coverage, and staleness thresholds for statistics and recommendations | open | product owner | FR-018, FR-021, FR-023, T-011, T-013 |
| D-006 | Exact deal-score formula, weights, evidence payload, and versioning policy | open | product owner | FR-020–FR-022, T-012, T-013 |
| D-007 | Public data display, caching, provider attribution, and redistribution policy | open | product owner | FR-001, FR-006, NFR-002 |
| D-008 | Exchange-rate snapshot strategy for historical display-currency comparisons | open | product owner | FR-034–FR-036, T-010, T-019 |
| D-009 | MVP scope/timeline trade-off if the 4–6 week target is constrained | open | product owner | ROADMAP, all phases |

### Platform and data

*D-010–D-013 must be resolved before T-001 (repository setup).*

| ID | Decision | Status | Owner | Affects |
|---|---|---|---|---|
| D-010 | Authentication mechanism, account lifecycle, session/token strategy | open | product owner | FR-008–FR-010, NFR-006, T-017 |
| D-011 | Exchange-rate provider and refresh policy | open | product owner | FR-035–FR-036, T-019 |
| D-012 | Email delivery provider | open | product owner | FR-028, T-021 |
| D-013 | Hosting/deployment target and operational budget | open | product owner | NFR-010, T-002, T-027 |
| D-014 | Data retention, PII classification, deletion/export policy, and provider-payload retention | open | product owner | NFR-002, NFR-005, NFR-006, NFR-013 |
| D-015 | Database schema, itinerary matching algorithm, tolerances, and matching-policy versioning | open | product owner + engineer | FR-016, FR-017, BR-002, BR-003, T-003 |
| D-016 | API paths, request/response schemas, pagination, error envelope, and ownership boundaries | open | product owner + engineer | API design, T-004, T-010, T-014–T-023 |
| D-017 | API versioning and deprecation policy | open | product owner + engineer | API design, T-010 |
| D-018 | OpenAPI generation source, shared client/types, and contract-test strategy | open | engineer | API design, T-004, T-010 |
| D-019 | Assistant streaming protocol and message/evidence format | open | product owner + engineer | FR-029–FR-033, T-022, T-023 |
| D-020 | Accessibility target for core flows (for example WCAG 2.1 AA) | open | product owner | NFR-012, T-014–T-019, T-024 |
| D-021 | Performance budgets for search, analytics, assistant, and worker jobs | open | product owner + engineer | NFR-011, T-014–T-023 |
| D-022 | UI design tokens and component library | open | product owner | Design system, T-014–T-019 |

### Development workflow

| ID | Decision | Status | Owner | Affects |
|---|---|---|---|---|
| D-023 | Default model/tier per development-agent role and escalation budget | open | product owner | WORKFLOW.md (pre-implementation gate) |
| D-024 | 9Router deployment mode, provider/model shortlist, fallback, logging, and retention | open | product owner | WORKFLOW.md (pre-implementation gate) |

*D-025 is resolved (2026-11-05, worktree/branch-per-issue runtime) and D-026 is accepted (GitHub Issues tracker); see Resolved decisions. D-023/D-024 remain open and must be resolved before implementation starts (pre-T-001).*

## Resolved decisions

Accepted decisions in ID order. Open work continues in the sections above.

### D-001 — MVP flight-data source: SerpApi Google Flights

- **Status:** accepted
- **Date:** 2026-11-05
- **Owner:** product owner
- **Context:** Phase-0 provider evaluation. Research (Nov 2026): Amadeus Self-Service was decommissioned on 2026-07-17 and is now Enterprise-only (negotiated contract, accreditation); Kiwi Tequila is invite-only; Skyscanner's official partnership is gated on large-MAU approval; Duffel is booking-oriented with commercial KYC activation; Travelpayouts exposes free cached/aggregated data with weak itinerary-level detail. The product's growth goal needs complete itinerary price data at MVP and at scale.
- **Decision:** Use SerpApi's `google_flights` engine as the MVP fare source, behind the provider-neutral adapter (NFR-001), replaceable or supplement-able without changing domain services.
- **Facts recorded (2026-11):** Free plan 250 searches/month at 50/hr; Starter $25/mo 1,000/mo; Developer $75/mo 5,000/mo; Production $150/mo 15,000/mo including U.S. Legal Shield; month-to-month. Only successful searches bill, and duplicate requests within a ~1-hour window are served from cache without charge. SerpApi deletes its copy of search data after 31 days, so customer-side retention is the intended model for this product's observations.
- **Consequences:**
  - D-004 collection intervals and quota budgets must be set against the active plan tier, including hourly throughput caps (~20% of plan volume) and cache behavior.
  - Google Flights results contain itinerary and price detail but not uniform fare-family/baggage data; missing attributes remain `unknown` (BR-004).
  - Observations keep provider attribution; guaranteed-bookability claims remain prohibited.
  - T-005 spot-checks redistribution/resale-terms implications, Indonesia coverage quality for the configured hubs, and outbound-link bookability.
- **Affects:** FR-002, FR-004, FR-005, FR-006, FR-012–FR-013, FR-017, NFR-001–NFR-002, D-004, D-007, T-004–T-005, T-008; PRD §5, §14, §18.

### D-002 — Initial airport hub list and reference-data source

- **Status:** accepted
- **Date:** 2026-11-05
- **Owner:** product owner
- **Context:** Phase 0 required a starter, demand-based set of Indonesian departure hubs that stays configurable and expandable.
- **Decision:** MVP hub set: CGK, DPS, SUB, KNO, JOG, UPG, BDO. Airport reference data is seeded from the OurAirports dataset (community-maintained, public domain). The list lives in seed/configuration data, so expansion does not require a PRD change.
- **Consequences:**
  - Yogyakarta commercial traffic now largely operates from YIA (Yogyakarta International, Kulon Progo); the seed step maps the Yogyakarta hub to YIA and retains JOG as a legacy alias.
  - BDO has thin scheduled service; verify during seed/coverage validation and extend the hub to Kertajati (KJT) via configuration only if material traffic exists.
  - Both verifications land in T-003 seed work and the T-005 live spot-check; they do not reopen this decision.
- **Affects:** FR-005, FR-009, D-003, T-003 seed data, T-005 coverage check; PRD §5.

### D-025 — Agent runtime: worktree/branch-per-issue model

- **Status:** accepted
- **Date:** 2026-11-05
- **Owner:** product owner + engineer
- **Context:** D-025 asked for the development-agent runtime format. The `team/` role prompts already assume Git worktrees, per-issue branches, and QA verdicts posted on issues.
- **Decision:** Adopt the worktree/branch-per-issue orchestration model: the orchestrator provisions a dedicated worktree, branch `issue-<n>`, and environment/database per engineer/QA session; engineers implement, commit, and push only their own branch; they never merge, rebase main, or touch another branch (the orchestrator rebases; no force-pushes); QA verifies a single dedicated worktree and posts PASS/FAIL verdicts with evidence as issue comments; destructive commands require explicit human approval.
- **Consequences:** `WORKFLOW.md` §10 records the model; `team/pm.md` and `team/qa.md` are aligned in this documentation pass (template path, project-appropriate checks). Model routing specifics remain D-023/D-024.
- **Affects:** WORKFLOW.md §10, `team/*` role prompts, D-023, D-024.

### D-026 — GitHub Issues as the canonical implementation tracker

- **Status:** accepted
- **Date:** 2026-11-05
- **Owner:** product owner
- **Context:** The backlog needed shared, reviewable tracking beyond markdown checklists; `docs/TASKS.md` had reserved canonical status for "GitHub Issues once explicitly adopted".
- **Decision:**
  - GitHub Issues is the canonical implementation tracker from tracker activation; until the repository is connected, `docs/TASKS.md` remains the working source of truth.
  - Mapping: one task (T-xxx) → one issue. Seeded issues carry lightweight bodies drawn from `TASKS.md` (goal, refs, deps, exit criteria, type label). `team/pm.md` grooms a body into a full packet from `docs/TASK_TEMPLATE.md` only when the task becomes Ready.
  - Labels: phase (`phase-1`…`phase-6`), type (`decision`, `scaffold`, `backend`, `frontend`, `hardening`), status (`proposed`, `ready`, `in-progress`, `in-qa`, `blocked`); completion is the closed state. Docs never duplicate issue status.
  - `decision`-type tasks close upon an accepted decision entry in `docs/DECISIONS.md` (evidence = the decision record).
  - Phase-0 decision work never becomes issues; decisions close within `DECISIONS.md`, and issue seeding covers the full implementation backlog (T-001–T-028). IDs were renumbered once, pre-activation, at the product owner's direction (2026-11-05): old T-005–T-032 became T-001–T-028, and decision IDs were regrouped theme-contiguously (product D-001–D-009, platform D-010–D-022, workflow D-023–D-026). IDs are stable from tracker activation onward.
  - Cross-referencing: branches are named `issue-<n>`; PRs link issues; QA verdicts and completion evidence are issue comments.
- **Consequences:** `AGENTS.md`, `README.md`, `ROADMAP.md`, `TASKS.md`, and `WORKFLOW.md` are updated in this documentation pass. Tracker activation remains a follow-up: install/authenticate `gh`, create the remote repository, enable Issues, configure labels, and seed the backlog.
- **Affects:** TASKS.md, WORKFLOW.md, AGENTS.md, README.md, ROADMAP.md, `team/*`.

## Superseded decisions

Record superseded decisions here with a link to the replacement. Do not delete historical decisions.
