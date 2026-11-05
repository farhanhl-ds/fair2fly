# Implementation Backlog

**Status:** Working backlog seed. GitHub Issues (D-026) becomes canonical on tracker activation; issue status lives in labels and open/closed state — never duplicated here.  
**Source of truth:** This file until the repository is connected; GitHub Issues (D-026) thereafter.  
**Roadmap:** [`ROADMAP.md`](ROADMAP.md) for milestone sequencing.

## Backlog conventions

- Every implementation task needs a task packet, acceptance criteria, dependencies, requirement references, and test expectations.
- Do not start a task until its dependencies are complete and dependent decisions in [`DECISIONS.md`](DECISIONS.md) are resolved.
- Keep tasks small enough to implement, verify, and review in one focused work session where practical.
- The PM may refine tasks but must not silently change product scope.
- QA independently verifies non-trivial tasks.
- Record evidence on the issue (or in the completion report until tracker activation) when complete.
- One task (T-xxx) maps to one GitHub issue. Seeded issue bodies are lightweight (goal, refs, deps, exit criteria, type label); [`TASK_TEMPLATE.md`](TASK_TEMPLATE.md) grooming happens only when the task becomes Ready.
- Labels: phase (`phase-1`…`phase-6`), type (`decision`, `scaffold`, `backend`, `frontend`, `hardening`), status (`proposed`, `ready`, `in-progress`, `in-qa`, `blocked`). Completion is the closed state.
- IDs are dense and sequential: tasks T-001–T-028 align with the roadmap weeks; decisions D-001–D-026 group by theme (product/provider, platform/data, workflow). Decision work lives in [`DECISIONS.md`](DECISIONS.md), not in the backlog. A `decision`-labeled issue is reserved for decisions the product owner later chooses to track explicitly.

## Phase 0 — Feasibility and decisions (closed)

Phase 0 produced decisions only; decision work does not enter the backlog or the tracker (D-026). Outcomes, with rationale and evidence, are recorded in [`DECISIONS.md`](DECISIONS.md):

- **D-001** (2026-11-05) — MVP fare source: Google Flights data via SerpApi, behind a replaceable adapter (NFR-001).
- **D-002** (2026-11-05) — MVP hub set: CGK, DPS, SUB, KNO, JOG, UPG, BDO; OurAirports reference data.
- **D-025** (2026-11-05) — worktree/branch-per-issue agent runtime (development workflow).

Open decision gates before implementation starts:

- **D-010–D-013** — authentication, exchange-rate source, email delivery, and hosting (required before T-001).
- **D-023/D-024** — development-agent model routing and 9Router configuration (required before engineering sessions run).

## Phase 1 — Foundation (Week 1)

- [ ] **T-001 — Initialize repository and local development environment**  
  Set up project structure, lint/format configuration, environment template, and developer commands.  
  **Refs:** NFR-008, NFR-010. **Deps:** decision gates D-010–D-013 (see Phase 0).  
  **Exit:** Reproducible setup; exact commands added to `AGENTS.md`.

- [ ] **T-002 — Create Docker Compose foundation**  
  Bring up Next.js, FastAPI, PostgreSQL, Redis, worker, and scheduler with health checks.  
  **Refs:** NFR-010. **Deps:** T-001.  
  **Exit:** Services start locally with documented environment variables.

- [ ] **T-003 — Define initial domain model and migrations**  
  Model users, airports, routes/itineraries, fare products, observations, tracking requests, and source metadata.  
  **Refs:** FR-016–FR-017, BR-001–BR-003. **Deps:** T-002.  
  **Exit:** Versioned migrations and a data-model document; D-015 updated.

- [ ] **T-004 — Define provider adapter contract**  
  Establish provider-neutral request/response types, errors, quota metadata, and normalization boundary.  
  **Refs:** FR-017, NFR-001. **Deps:** T-003 (provider decision D-001 already accepted).  
  **Exit:** Contract documented and covered by focused tests.

- [ ] **T-005 — Implement provider integration spike**  
  Retrieve a supported search and normalize at least one offer without leaking provider-specific fields into domain services.  
  **Refs:** FR-006, FR-017, NFR-001. **Deps:** T-004.  
  **Exit:** Normalized offer available in development with sanitized fixture tests.

## Phase 2 — Collection and persistence (Week 2)

- [ ] **T-006 — Persist normalized offers and immutable observations**  
  Ensure repeated collection appends timestamped observations and preserves original fare/currency.  
  **Refs:** FR-014–FR-017, BR-001–BR-008. **Deps:** T-003, T-005.  
  **Exit:** Repeated collection creates new observations without overwriting history.

- [ ] **T-007 — Implement tracking-request CRUD**  
  Support create, list, update, pause, and delete with ownership checks.  
  **Refs:** FR-010–FR-011, NFR-006. **Deps:** T-003.  
  **Exit:** Authorization and validation tests pass.

- [ ] **T-008 — Implement scheduled collection worker**  
  Add scheduling, quota budgets, retries, backoff, idempotency, and structured logs.  
  **Refs:** FR-012–FR-013, NFR-002–NFR-003. **Deps:** T-005–T-007.  
  **Exit:** Jobs are retry-safe and do not duplicate observations.

- [ ] **T-009 — Add collection observability**  
  Track provider success/failure, latency, quota consumption, freshness, and worker retry outcomes.  
  **Refs:** NFR-007. **Deps:** T-008.  
  **Exit:** Metrics/logs available for provider and worker health.

## Phase 3 — Price intelligence (Week 3)

- [ ] **T-010 — Implement historical query services**  
  Query observations by route and itinerary with explicit windows and comparability constraints.  
  **Refs:** FR-018–FR-019, BR-005. **Deps:** T-006.  
  **Exit:** Queries return comparable observations with explicit windows.

- [ ] **T-011 — Implement statistical summaries**  
  Calculate supported statistics and suppress or qualify insufficient samples.  
  **Refs:** FR-018, FR-021, FR-023, BR-005–BR-006. **Deps:** T-010.  
  **Exit:** Insufficient/stale data produces an explicit qualified state.

- [ ] **T-012 — Implement versioned deal score**  
  Create deterministic rules with evidence payload and test cases.  
  **Refs:** FR-020–FR-021, BR-006. **Deps:** T-011.  
  **Exit:** Formula version and evidence are recorded; tests cover boundaries.

- [ ] **T-013 — Implement recommendation evidence contract**  
  Return recommendation, rationale, sample size, observation window, freshness, and confidence/coverage context.  
  **Refs:** FR-021–FR-023, BR-005–BR-006. **Deps:** T-012.  
  **Exit:** Every recommendation includes supporting evidence and uncertainty.

## Phase 4 — User-facing application (Week 4)

- [ ] **T-014 — Build public Explore homepage**  
  Show public deals/insights and make search discoverable.  
  **Refs:** FR-001, FR-006. **Deps:** T-011, T-013.  
  **Exit:** Public visitors understand the product without registering.

- [ ] **T-015 — Build route and itinerary search UI**  
  Support one-way/round-trip economy and fixed/flexible dates within provider capabilities.  
  **Refs:** FR-002–FR-004, FR-006–FR-007. **Deps:** T-005, T-014.  
  **Exit:** Search criteria, results, and provider context are visible and testable.

- [ ] **T-016 — Build flexible destination discovery**  
  Support origin, budget, date window, trip duration, and destination constraints within quota limits.  
  **Refs:** FR-005, FR-013, NFR-002. **Deps:** T-015, T-008.  
  **Exit:** Discovery respects quota limits and shows explicit empty/error states.

- [ ] **T-017 — Implement authentication and user preferences**  
  Add saved preferences, default display currency, and preferred origins.  
  **Refs:** FR-008–FR-009, NFR-006. **Deps:** T-003, T-014.  
  **Exit:** Ownership checks and preference persistence tests pass.

- [ ] **T-018 — Build tracking/watchlist workspace**  
  Show tracking requests, status, latest observation, and history.  
  **Refs:** FR-010–FR-011, FR-019. **Deps:** T-007, T-017.  
  **Exit:** Users can manage and inspect their own tracking requests.

- [ ] **T-019 — Build price history and deal detail views**  
  Display comparable historical observations, statistics, and recommendation evidence.  
  **Refs:** FR-019, FR-021–FR-023. **Deps:** T-013, T-017–T-018.  
  **Exit:** Charts and detail views show window, sample size, freshness, and evidence.

## Phase 5 — Notifications and AI assistant (Week 5)

- [ ] **T-020 — Implement Telegram notifications**  
  Support threshold and intelligence triggers, cooldown, deduplication, and trigger explanation.  
  **Refs:** FR-024–FR-028, NFR-003, NFR-007. **Deps:** T-013, T-018.  
  **Exit:** Alert fires once per qualifying event within its cooldown window.

- [ ] **T-021 — Implement email notifications**  
  Reuse notification event semantics and preference controls.  
  **Refs:** FR-028, NFR-003. **Deps:** T-020.  
  **Exit:** Email delivery uses the same deduplication and explanation contract.

- [ ] **T-022 — Implement approved AI assistant tools**  
  Add search, discovery, price history, deal analysis, and tracking operations with authorization.  
  **Refs:** FR-029–FR-033, NFR-006. **Deps:** T-013, T-018.  
  **Exit:** Tools call deterministic services and cannot bypass service-layer authorization.

- [ ] **T-023 — Build grounded assistant experience**  
  Ensure answers cite tool-returned evidence in the UI and do not fabricate unsupported values.  
  **Refs:** FR-030–FR-033. **Deps:** T-022.  
  **Exit:** Every factual fare/statistics claim is traceable to a tool result.

## Phase 6 — Hardening and release (Week 6)

- [ ] **T-024 — Add end-to-end user journey tests**  
  Cover discovery → account → tracking → observation → analytics → notification → assistant.  
  **Refs:** FR-001–FR-036, NFR-008. **Deps:** T-014–T-023.  
  **Exit:** Critical journey passes with controlled fixtures/stubs.

- [ ] **T-025 — Test provider failure and quota exhaustion**  
  Verify graceful degradation and historical data integrity.  
  **Refs:** NFR-002–NFR-003, NFR-007, BR-001. **Deps:** T-008–T-009.  
  **Exit:** Failures are visible and do not corrupt stored history.

- [ ] **T-026 — Security and authorization review**  
  Review secrets, user data access, assistant tools, rate limits, logs, and prompt-injection boundaries.  
  **Refs:** NFR-005–NFR-007, FR-033. **Deps:** T-017, T-022.  
  **Exit:** No unresolved critical/high-severity findings.

- [ ] **T-027 — Deploy MVP and configure monitoring**  
  Add health checks, error reporting, backup strategy, and deployment instructions.  
  **Refs:** NFR-007, NFR-010. **Deps:** T-002, T-024–T-026.  
  **Exit:** Deployed environment is observable and reproducible.

- [ ] **T-028 — Finalize documentation and demo scenario**  
  Document setup, limitations, architecture, API, test commands, and a reproducible demo.  
  **Refs:** all. **Deps:** T-027.  
  **Exit:** A new contributor can run the system and follow the demo.

## Prioritization rule

If time is constrained, prioritize:

1. Reliable provider integration and observation history.
2. Historical analytics and explainable scoring.
3. Search, tracking, and dashboard.
4. Notifications.
5. AI assistant polish.

Do not sacrifice data correctness to add advanced agent behavior.
