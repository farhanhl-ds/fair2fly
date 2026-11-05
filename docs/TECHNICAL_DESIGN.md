# Technical Design (Initial Baseline)

**Status:** Proposed implementation baseline; provider selected (D-001); schema not finalized.  
**Last updated:** 2026-11-05  
**Open decisions:** [`DECISIONS.md`](DECISIONS.md)  
**Related:** [`PRD.md`](PRD.md), [`SRS.md`](SRS.md), [`ROADMAP.md`](ROADMAP.md), [`WORKFLOW.md`](WORKFLOW.md)

## 1. Design principles

1. Historical price observations are a first-class product asset.
2. Preserve raw source context and normalize into a stable internal model.
3. Separate deterministic business logic from LLM interaction.
4. Make provider integration replaceable.
5. Respect API terms, quotas, caching, and data-retention rules.
6. Avoid premature microservices and multi-agent complexity.

## 2. Proposed stack

- Frontend: Next.js
- Backend API: FastAPI
- Primary database: PostgreSQL
- Background processing: Celery + Redis
- AI: LLM API with tool calling
- Packaging/deployment: Docker

TimescaleDB, a separate analytics warehouse, or additional orchestration infrastructure are not MVP requirements. Revisit only when workload justifies them.

## 3. Logical components

### Web application
- Public Explore homepage.
- Flight search and results.
- Deal and market insight pages.
- Authenticated dashboard and watchlist.
- Tracking configuration.
- AI assistant interface.

### FastAPI application
- Authentication/authorization integration.
- Search and discovery endpoints.
- Tracking-request management.
- Historical analytics endpoints.
- Deal-scoring service.
- Notification preferences.
- AI tool endpoints/services.

### Provider adapter
- Provider-specific request/response handling.
- Quota and rate-limit handling.
- Normalization into internal flight-offer structures.
- Provider attribution and error reporting.

### Background workers
- Scheduled price collection.
- Adaptive monitoring policy.
- Observation deduplication/idempotency.
- Analytics refresh.
- Alert evaluation and delivery.

### AI tool layer
Initial tools may include:
- `search_flights`
- `discover_destinations`
- `get_route_price_history`
- `get_itinerary_price_history`
- `analyze_deal`
- `create_tracking_request`
- `list_tracking_requests`
- `update_tracking_request`

Tool names are illustrative. Define exact schemas and authorization behavior during API design. AI tools must call deterministic application services rather than query providers or mutate data without authorization checks.

### Development-time agent workflow

Development-time roles (orchestrator, PM, engineer, QA, documentation) are described in [`WORKFLOW.md`](WORKFLOW.md). They are development-time only and do not imply autonomous multi-agent behavior in the deployed flight product. The product AI assistant remains a single tool-calling agent for the MVP.

## 4. Data concepts

These are conceptual entities, not a finalized schema:

- **User:** account identity and preferences.
- **Airport:** IATA/ICAO codes, location, country, timezone, and active status.
- **Airline:** carrier identifiers and display metadata.
- **SearchRequest:** normalized search criteria and search context.
- **FlightOffer:** provider-returned offer/itinerary representation.
- **Itinerary:** normalized flight segments and material itinerary attributes.
- **FareProduct:** cabin, baggage, fare family, and other fare conditions where available.
- **PriceObservation:** immutable amount, currency, timestamp, provider, offer/itinerary reference, and source metadata.
- **TrackingRequest:** owner, tracking mode, criteria, schedule policy, and active status.
- **DealAssessment:** score, rule version, evidence, sample size, and confidence context.
- **NotificationPreference:** channel, threshold, cooldown, and enabled state.
- **NotificationEvent:** trigger evidence, delivery status, and deduplication key.
- **ExchangeRate:** base/quote currency, rate, source, and timestamp.

### 4.1 Core identity distinctions

| Concept | Definition | Important distinction |
|---|---|---|
| Route | Origin-destination market | Not a specific date or flight |
| Itinerary | Date-specific ordered set of flight segments | Identity depends on material segment attributes |
| FareProduct | Cabin, fare family, baggage, and fare conditions | Missing attributes are `unknown`, not assumed |
| PriceObservation | Immutable record of a source-reported price at a specific time | Append-only historical fact |

Do not treat a route as the identity of an itinerary. Do not merge observations for materially different fare products.

### 4.2 PriceObservation minimum fields

- Internal observation ID.
- Source/provider identifier.
- Source offer ID, nullable and retained as source metadata.
- Internal itinerary/fare-product reference or unresolved matching status.
- `observed_at` timestamp in UTC.
- Original amount using decimal-safe representation.
- Original ISO 4217 currency code.
- Source retrieval/search context.
- Sanitized source metadata or payload reference, subject to provider terms.
- Matching-policy version/status where identity resolution is applied.

Distinguish `observed_at` (provider-reported or search time) from `received_at`/`ingested_at` (when the application stored the observation). Corrections, if ever required, must be explicit and auditable rather than silent overwrites.

## 5. Price observation and identity

Do not use a single route key as the identity of a specific flight product. The matching strategy must tolerate provider offer IDs changing while avoiding false matches between materially different itineraries.

Matching may consider:

- Origin/destination airports.
- Local departure date and segment sequence.
- Marketing/operating carrier and flight numbers where available.
- Stops and connection airports.
- Departure/arrival times within a documented tolerance.
- Cabin and fare attributes.

Define a versioned matching policy and retain provider identifiers as source metadata so historical analytics can explain which observations were considered comparable.

## 6. Collection strategy

Use Celery workers with scheduled jobs and Redis as broker/result backend.

Proposed adaptive policy:
- Baseline frequency for active tracking requests.
- Higher frequency for near-term departures or high-interest tracked items.
- Search-triggered refresh where permitted.
- Per-provider quota budgets, rate limits, retries, and backoff.
- Pause or degrade collection when quotas are exhausted.

Quota, throughput, and caching behavior of the MVP source are recorded in D-001 ([`DECISIONS.md`](DECISIONS.md)); collection intervals and per-request budget accounting are D-004. The scheduler reads these values from configuration for the active plan tier and must not hardcode them.

## 7. Analytics

Initial calculations:
- Minimum, maximum, mean, median.
- Percentile/rank when sample size is sufficient.
- Percentage difference from historical median or another explicit baseline.
- Rule-based deal score with a versioned formula.
- Confidence/data coverage metadata.

Do not compare unlike fare products. Keep analytics service deterministic and independently testable.

## 8. Currency

Store source amount and source currency unchanged. For display conversion, store or reference the applied exchange rate, rate source, and conversion timestamp. Avoid mixing converted values from inconsistent rate snapshots in historical trend calculations without clearly defining the comparison method.

## 9. API design approach

Use versioned REST endpoints under `/api/v1` initially. FastAPI-generated OpenAPI is the machine-readable contract once endpoints exist; candidate resource groups:
- `/searches`
- `/discoveries`
- `/airports`
- `/tracking-requests`
- `/observations`
- `/analytics`
- `/deals`
- `/notifications`
- `/assistant`

Exact paths, request/response schemas, pagination, error envelopes, authentication, and versioning/deprecation rules are recorded in [`DECISIONS.md`](DECISIONS.md) before endpoint implementation. Do not let assistant tool schemas drift from the API contracts they call.

## 10. Observability and reliability

- Structured logs with correlation IDs.
- Metrics for provider latency, success/error rate, quota use, collection freshness, worker retries, and notification delivery.
- Idempotency keys for collection and notification jobs.
- Dead-letter/retry strategy for repeated worker failures.
- Health checks for API, database, Redis, and workers.
- No credentials or sensitive user data in logs.

## 11. Security

- Keep API keys and bot tokens in environment-managed secrets.
- Enforce ownership checks on tracking requests and user data.
- Validate and constrain AI tool inputs.
- Require explicit user intent for state-changing actions.
- Apply rate limits to expensive search and assistant operations.
- Treat provider data, external web content, and model outputs as untrusted input.
- Do not put secrets, credentials, or sensitive user data in prompts or logs.

## 12. Initial deployment topology

Start with a Docker Compose development environment:

- `web` — Next.js.
- `api` — FastAPI.
- `worker` — Celery worker.
- `scheduler` — Celery Beat or equivalent scheduler.
- `db` — PostgreSQL.
- `redis` — broker/cache.

A reverse proxy and production hosting choice remain open. Keep local setup reproducible and document environment variables in `.env.example` without real credentials.

## 13. Open technical decisions

Open technical decisions are tracked centrally in [`DECISIONS.md`](DECISIONS.md). Resolve them before implementing dependent work and record the outcome with rationale and consequences.
