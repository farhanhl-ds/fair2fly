# Development Roadmap

**Status:** Planning baseline.  
**Target:** 4–6 weeks.  
**Task backlog:** GitHub Issues (D-026). Issue titles carry the T-xxx IDs used in this roadmap.

## Milestone 0 — Feasibility and product decisions

Scope: select the MVP flight-data provider, confirm the initial airport hubs, record provider risks and limitations, and settle platform and agent-workflow choices. Status and outcomes live only in [`DECISIONS.md`](DECISIONS.md).

**Exit criteria:** One provider selected for the MVP; permitted collection and storage behavior understood; initial airport list agreed. Platform decisions (D-010-D-013) are resolved before the first task each one affects, per the gating rule in `DECISIONS.md`.

## Week 1 — Foundation (T-001–T-006)
- Repository structure and development environment.
- Docker Compose for application, PostgreSQL, and Redis.
- FastAPI skeleton and Next.js skeleton.
- Time-boxed provider spike (T-003): quota cost, offer-ID stability, coverage, and terms.
- Initial domain model and migrations, designed after the spike findings.
- Provider adapter interface and one provider integration.

**Exit criteria:** A supported search can retrieve and normalize a provider offer in a development environment.

## Week 2 — Collection and persistence (T-007–T-010)
- Persist normalized offers and immutable price observations.
- Implement Celery worker and scheduled collection.
- Add idempotency, retries, quota handling, and structured logs.
- Create tracking-request CRUD.

**Exit criteria:** A tracking request can produce multiple timestamped observations without overwriting history.

## Week 3 — Price intelligence (T-011–T-014)
- Historical query services.
- Statistical summaries and price charts.
- Rule-based deal scoring with versioning.
- Data coverage and confidence rules.
- Initial recommendation explanation.

**Exit criteria:** A user can inspect historical observations and see an evidence-backed statistical assessment.

## Week 4 — User-facing application (T-015–T-020)
- Public Explore homepage.
- Search and flexible discovery flow within provider capabilities.
- Deal and market insight pages.
- Authentication and user preferences.
- Personal watchlist and tracking workspace.

**Exit criteria:** A visitor can discover deals; a registered user can save and manage tracking requests.

## Week 5 — Notifications and AI (T-021–T-024)
- Telegram alert delivery and cooldowns.
- Email notifications.
- AI assistant with approved tool calling.
- Search, history, deal-analysis, and tracking tools.
- AI response grounding and tool authorization tests.

**Exit criteria:** The assistant can answer using backend data and a user can receive a meaningful alert.

## Week 6 — Hardening and deployment (T-025–T-029)
- Unit, integration, and end-to-end tests.
- Provider failure and quota-exhaustion tests.
- Security and access-control review.
- Deployment, health checks, and monitoring.
- README, architecture documentation, demo scenario, and project presentation.

**Exit criteria:** Deployed MVP with reproducible setup, documented limitations, and demonstrable end-to-end user journey.

## Scope-control rule

If time is constrained, prioritize:
1. Reliable provider integration and observation history.
2. Historical analytics and explainable scoring.
3. Search, tracking, and dashboard.
4. Notifications.
5. AI assistant polish.

Do not sacrifice data correctness to add advanced agent behavior.
