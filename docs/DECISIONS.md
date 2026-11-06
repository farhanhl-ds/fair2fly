# Decision Log

**Status:** Living document.  
**Purpose:** Single source of truth for open and resolved product, provider, platform, API, and development-workflow decisions.  
**Rule:** Resolve a decision before implementing work that depends on it. **Gating rule:** a decision blocks only the tasks in its *Affects* column, never the whole backlog. Record the date, owner, rationale, consequences, and affected requirements/tasks.

Status values: `open`, `proposed`, `accepted`, `deferred`, `superseded`. `deferred` means intentionally postponed: it blocks no task and is revisited when needed.

Decision IDs are stable from tracker activation (D-026) onward. After activation, new decisions receive new IDs rather than renumbering existing entries.

## Decision index

Every decision appears in the tables below with its status. Accepted decisions (D-001, D-002, D-025, D-026) keep their full record, with rationale and consequences, under Resolved decisions.

### Product and provider

| ID | Decision | Status | Owner | Affects |
|---|---|---|---|---|
| D-001 | MVP flight-data source: SerpApi Google Flights behind the provider adapter | accepted | product owner | FR-002, FR-004, FR-005, FR-006, FR-012–FR-013, FR-017, NFR-001–NFR-002, D-004, D-007, T-005–T-006, T-009 |
| D-002 | Initial airport hub list (CGK, DPS, SUB, KNO, JOG, UPG, BDO) and OurAirports reference data | accepted | product owner | FR-005, FR-009, D-003, T-004, T-006 |
| D-003 | Exact supported flexible-date and flexible-destination constraints | open | product owner | FR-004, FR-005, T-016, T-017 |
| D-004 | Collection intervals, quota allocation, adaptive-monitoring policy, and tracking-mode rollout | open | product owner | FR-011–FR-013, T-009, T-017 |
| D-005 | Minimum sample size, coverage, and staleness thresholds for statistics and recommendations | open | product owner | FR-018, FR-021, FR-023, T-012, T-014 |
| D-006 | Exact deal-score formula, weights, evidence payload, and versioning policy | open | product owner | FR-020–FR-022, T-013, T-014 |
| D-007 | Public data display, caching, provider attribution, and redistribution policy | open | product owner | FR-001, FR-006, NFR-002 |
| D-008 | Exchange-rate snapshot strategy for historical display-currency comparisons | open | product owner | FR-034–FR-036, T-011, T-020 |
| D-009 | MVP scope/timeline trade-off if the 4–6 week target is constrained | open | product owner | ROADMAP, all milestones |

D-004, D-007, and D-015 are informed by the T-003 spike. Keep them open until its findings are recorded.

### Platform and data

*No platform decision gates T-001. Resolve each one before the first task in its Affects column starts. Planning order: D-013 before T-002, D-010 before T-018, D-011 before T-020, D-012 before T-022.*

| ID | Decision | Status | Owner | Affects |
|---|---|---|---|---|
| D-010 | Authentication mechanism, account lifecycle, session/token strategy | open | product owner | FR-008–FR-010, NFR-006, T-018 |
| D-011 | Exchange-rate provider and refresh policy | open | product owner | FR-035–FR-036, T-020 |
| D-012 | Email delivery provider | open | product owner | FR-028, T-022 |
| D-013 | Hosting/deployment target and operational budget | open | product owner | NFR-010, T-002, T-028 |
| D-014 | Data retention, PII classification, deletion/export policy, and provider-payload retention | open | product owner | NFR-002, NFR-005, NFR-006, NFR-013 |
| D-015 | Database schema, itinerary matching algorithm, tolerances, and matching-policy versioning | open | product owner + engineer | FR-016, FR-017, BR-002, BR-003, T-004 |
| D-016 | API paths, request/response schemas, pagination, error envelope, and ownership boundaries | open | product owner + engineer | API design, T-005, T-011, T-015–T-024 |
| D-017 | API versioning and deprecation policy | open | product owner + engineer | API design, T-011 |
| D-018 | OpenAPI generation source, shared client/types, and contract-test strategy | open | engineer | API design, T-005, T-011 |
| D-019 | Assistant streaming protocol and message/evidence format | open | product owner + engineer | FR-029–FR-033, T-023, T-024 |
| D-020 | Accessibility target for core flows (for example WCAG 2.1 AA) | open | product owner | NFR-012, T-015–T-020, T-025 |
| D-021 | Performance budgets for search, analytics, assistant, and worker jobs | open | product owner + engineer | NFR-011, T-015–T-024 |
| D-022 | UI design tokens and component library | open | product owner | Design system, T-015–T-020 |

### Development workflow

| ID | Decision | Status | Owner | Affects |
|---|---|---|---|---|
| D-023 | Default model/tier per development-agent role and escalation budget | deferred | product owner | WORKFLOW.md §9 (not a gate; revisit when model routing is needed) |
| D-024 | 9Router deployment mode, provider/model shortlist, fallback, logging, and retention | deferred | product owner | WORKFLOW.md §9 (not a gate; revisit when model routing is needed) |
| D-025 | Agent runtime: worktree/branch-per-issue model | accepted | product owner + engineer | WORKFLOW.md §10, `team/*` role prompts, D-023, D-024 |
| D-026 | GitHub Issues as the canonical implementation tracker | accepted | product owner | docs/archive/TASKS.md, WORKFLOW.md, AGENTS.md, README.md, ROADMAP.md, `team/*` |

*D-023/D-024 are deferred: development agents use the default model until routing becomes necessary.*

## Resolved decisions

Accepted decisions in ID order, with full rationale and consequences. Status of every decision is in the index above.

### D-001 — MVP flight-data source: SerpApi Google Flights

- **Status:** accepted
- **Date:** 2026-11-05
- **Owner:** product owner
- **Context:** Milestone 0 provider evaluation. Research (Nov 2026): Amadeus Self-Service was decommissioned on 2026-07-17 and is now Enterprise-only (negotiated contract, accreditation); Kiwi Tequila is invite-only; Skyscanner's official partnership is gated on large-MAU approval; Duffel is booking-oriented with commercial KYC activation; Travelpayouts exposes free cached/aggregated data with weak itinerary-level detail. The product's growth goal needs complete itinerary price data at MVP and at scale.
- **Decision:** Use SerpApi's `google_flights` engine as the MVP fare source, behind the provider-neutral adapter (NFR-001), replaceable or supplement-able without changing domain services.
- **Facts recorded (2026-11):** Free plan 250 searches/month at 50/hr; Starter $25/mo 1,000/mo; Developer $75/mo 5,000/mo; Production $150/mo 15,000/mo including U.S. Legal Shield; month-to-month. Only successful searches bill, and duplicate requests within a ~1-hour window are served from cache without charge. SerpApi deletes its copy of search data after 31 days, so customer-side retention is the intended model for this product's observations.
- **Consequences:**
  - D-004 collection intervals and quota budgets must be set against the active plan tier, including hourly throughput caps (~20% of plan volume) and cache behavior.
  - Google Flights results contain itinerary and price detail but not uniform fare-family/baggage data; missing attributes remain `unknown` (BR-004).
  - Observations keep provider attribution; guaranteed-bookability claims remain prohibited.
  - The T-003 spike validates redistribution/resale-terms implications, Indonesia coverage quality for the configured hubs, and outbound-link bookability before the domain model is designed; T-006 reconfirms them against the live adapter.
- **Affects:** FR-002, FR-004, FR-005, FR-006, FR-012–FR-013, FR-017, NFR-001–NFR-002, D-004, D-007, T-005–T-006, T-009; PRD §5, §14, §18.

### D-002 — Initial airport hub list and reference-data source

- **Status:** accepted
- **Date:** 2026-11-05
- **Owner:** product owner
- **Context:** Milestone 0 required a starter, demand-based set of Indonesian departure hubs that stays configurable and expandable.
- **Decision:** MVP hub set: CGK, DPS, SUB, KNO, JOG, UPG, BDO. Airport reference data is seeded from the OurAirports dataset (community-maintained, public domain). The list lives in seed/configuration data, so expansion does not require a PRD change.
- **Consequences:**
  - Yogyakarta commercial traffic now largely operates from YIA (Yogyakarta International, Kulon Progo); the seed step maps the Yogyakarta hub to YIA and retains JOG as a legacy alias.
  - BDO has thin scheduled service; verify during seed/coverage validation and extend the hub to Kertajati (KJT) via configuration only if material traffic exists.
  - Both verifications land in T-004 seed work and the T-003 spike; they do not reopen this decision.
- **Affects:** FR-005, FR-009, D-003, T-004 seed data, T-006 coverage check; PRD §5.

### D-025 — Agent runtime: worktree/branch-per-issue model

- **Status:** accepted
- **Date:** 2026-11-05
- **Owner:** product owner + engineer
- **Context:** D-025 asked for the development-agent runtime format. The `team/` role prompts already assume Git worktrees, per-issue branches, and QA verdicts posted on issues.
- **Decision:** Adopt the worktree/branch-per-issue orchestration model: the orchestrator creates a dedicated worktree, branch `issue-<n>`, and environment/database per task and runs each role in a separate session with fresh context; engineers commit and push only their own branch; QA verifies a detached worktree at the pushed commit and posts PASS/FAIL verdicts with evidence as issue comments; nobody rebases, merges, or force-pushes, and destructive commands require explicit human approval; the orchestrator opens the pull request (`Closes #n`) and the product owner merges it as final acceptance. Role prompts stay tool-agnostic in `team/`; tool-specific wrappers only point to them.
- **Consequences:** `WORKFLOW.md` §10 records the model and the permissions per role; `team/pm.md` and `team/qa.md` are aligned in this documentation pass (template path, project-appropriate checks). Model routing specifics remain D-023/D-024.
- **Affects:** WORKFLOW.md §10, `team/*` role prompts, D-023, D-024.

### D-026 — GitHub Issues as the canonical implementation tracker

- **Status:** accepted
- **Date:** 2026-11-05
- **Owner:** product owner
- **Context:** The backlog needed shared, reviewable tracking beyond markdown checklists; the markdown backlog had reserved canonical status for "GitHub Issues once explicitly adopted".
- **Decision:**
  - GitHub Issues is the canonical implementation tracker. The initial seed backlog is archived at `docs/archive/TASKS.md` and is not maintained.
  - Mapping: one task (T-xxx) → one issue. Seeded issues carry lightweight bodies drawn from the archived seed backlog (`docs/archive/TASKS.md`) (goal, refs, deps, exit criteria, type label). `team/pm.md` grooms a body into a full packet from `docs/TASK_TEMPLATE.md` only when the task becomes Ready.
  - Milestone: each task is assigned to the GitHub milestone for its ROADMAP section (Milestone 1 to 6). Labels: type (`decision`, `scaffold`, `spike`, `backend`, `frontend`, `hardening`), status (`proposed`, `ready`, `in-progress`, `in-qa`, `blocked`), scope (`post-mvp`, for work moved out of a groomed task); completion is the closed state. Docs never duplicate issue status.
  - `decision`-type tasks close upon an accepted decision entry in `docs/DECISIONS.md` (evidence = the decision record).
  - Milestone 0 decision work never becomes issues; decisions close within `DECISIONS.md`, and issue seeding covers the full implementation backlog (T-001–T-029). IDs are stable from tracker activation onward.
  - Cross-referencing: branches are named `issue-<n>`; PRs link issues; QA verdicts and completion evidence are issue comments.
- **Consequences:** `AGENTS.md`, `README.md`, `ROADMAP.md`, and `WORKFLOW.md` point to the tracker instead of a backlog file. Activation steps: authenticate `gh`, create the remote repository, create the labels, and seed one issue per task in T-xxx order so issue numbers match task numbers.
- **Affects:** docs/archive/TASKS.md, WORKFLOW.md, AGENTS.md, README.md, ROADMAP.md, `team/*`.

## Superseded decisions

Record superseded decisions here with a link to the replacement. Do not delete historical decisions.
