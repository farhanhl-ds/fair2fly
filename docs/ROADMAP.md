# Development Roadmap

**Status:** Planning baseline; provider and hub selections accepted (D-001, D-002).  
**Target:** 4–6 weeks.  
**Task backlog:** GitHub Issues (D-026) once the repository is connected; [`TASKS.md`](TASKS.md) is the current seed.

## Milestone 0 — Feasibility and product decisions (closed decisions: D-001, D-002, D-023)

- [x] Compare flight API providers for Indonesian coverage, price/fare fields, quotas, terms, retention, and cost — D-001 accepted 2026-11-05.
- [x] Confirm initial airport hubs — D-002 accepted 2026-11-05 (CGK, DPS, SUB, KNO, JOG, UPG, BDO).
- [x] Record risks and provider limitations for the MVP — captured in D-001; live terms/coverage verification happens at T-009.
- [ ] Confirm authentication, currency-rate, email, and deployment choices (D-008–D-011).
- [ ] Validate development-agent model routing (D-021–D-022; the runtime model itself is resolved in D-023).

**Exit criteria:** One provider selected for MVP; permitted collection/storage behavior understood; initial airport list agreed; platform-service choices (D-008–D-011) and agent model routing (D-021/D-022) resolved before Week 1.

## Week 1 — Foundation (T-005–T-009)
- Repository structure and development environment.
- Docker Compose for application, PostgreSQL, and Redis.
- FastAPI skeleton and Next.js skeleton.
- Initial domain model and migrations.
- Provider adapter interface and one provider integration spike.

**Exit criteria:** A supported search can retrieve and normalize a provider offer in a development environment.

## Week 2 — Collection and persistence (T-010–T-013)
- Persist normalized offers and immutable price observations.
- Implement Celery worker and scheduled collection.
- Add idempotency, retries, quota handling, and structured logs.
- Create tracking-request CRUD.

**Exit criteria:** A tracking request can produce multiple timestamped observations without overwriting history.

## Week 3 — Price intelligence (T-014–T-017)
- Historical query services.
- Statistical summaries and price charts.
- Rule-based deal scoring with versioning.
- Data coverage and confidence rules.
- Initial recommendation explanation.

**Exit criteria:** A user can inspect historical observations and see an evidence-backed statistical assessment.

## Week 4 — User-facing application (T-018–T-023)
- Public Explore homepage.
- Search and flexible discovery flow within provider capabilities.
- Deal and market insight pages.
- Authentication and user preferences.
- Personal watchlist and tracking workspace.

**Exit criteria:** A visitor can discover deals; a registered user can save and manage tracking requests.

## Week 5 — Notifications and AI (T-024–T-027)
- Telegram alert delivery and cooldowns.
- Email notifications.
- AI assistant with approved tool calling.
- Search, history, deal-analysis, and tracking tools.
- AI response grounding and tool authorization tests.

**Exit criteria:** The assistant can answer using backend data and a user can receive a meaningful alert.

## Week 6 — Hardening and deployment (T-028–T-032)
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
