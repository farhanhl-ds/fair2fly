# Software Requirements Specification (SRS)

**Status:** Provider-neutral requirements; the MVP source is selected in D-001 (Google Flights data via SerpApi) and stays behind the adapter boundary (NFR-001).  
**Last updated:** 2026-11-05  
**Related:** [`PRD.md`](PRD.md), [`TECHNICAL_DESIGN.md`](TECHNICAL_DESIGN.md), [`DECISIONS.md`](DECISIONS.md)

## 1. Purpose

Define testable MVP system requirements for the Flight Price Intelligence Platform. Requirements are intentionally provider-neutral until a flight-data API is selected.

## 2. Actors

- **Visitor:** Unauthenticated user exploring public deals and insights.
- **Registered user:** User with saved preferences and tracking requests.
- **Background worker:** Executes scheduled collection, analytics, and notification jobs.
- **AI assistant:** Calls approved backend tools on behalf of the user.
- **External provider:** Supplies flight offers and related data.
- **Administrator/operator:** Maintains provider configuration and monitors system health.

## 3. Functional requirements

### Discovery
- FR-001: The system shall present public flight deals and market insights.
- FR-002: The system shall accept route searches with origin, destination, dates, and passenger details supported by the provider.
- FR-003: The system shall support one-way and round-trip economy searches.
- FR-004: The system shall support fixed-date and flexible-date search inputs.
- FR-005: The system shall support flexible destination discovery using an origin, budget, date window, and trip duration.
- FR-006: The system shall display provider-sourced offers with their observation/retrieval context and available fare attributes.
- FR-007: The system shall provide outbound booking links when supplied and valid.

### Accounts and preferences
- FR-008: Registered users shall be able to save preferences and searches.
- FR-009: Users shall be able to configure preferred origin airports, budget, and display currency.
- FR-010: Users shall be able to create, view, update, pause, and delete tracking requests.

### Tracking and collection
- FR-011: The system shall support route-level, specific-itinerary, and flexible-destination tracking.
- FR-012: The system shall collect prices on a scheduled basis subject to provider limits.
- FR-013: The system may collect fresh observations in response to user searches, subject to provider terms and quota policy.
- FR-014: The system shall retain historical price observations rather than overwrite prior observations.
- FR-015: Each observation shall retain a timestamp, provider/source identifier, original amount, and original currency.
- FR-016: The system shall record sufficient itinerary and fare attributes to support meaningful comparisons.
- FR-017: The system shall normalize provider responses into a provider-independent internal representation.

### Analytics and recommendations
- FR-018: The system shall calculate historical statistics when sufficient observations exist.
- FR-019: The system shall display historical price movement for supported route or itinerary contexts.
- FR-020: The system shall calculate a transparent, rule-based deal score.
- FR-021: The system shall expose data coverage and confidence context alongside analytical conclusions.
- FR-022: The system shall provide evidence-backed booking guidance: consider booking, wait, or keep monitoring.
- FR-023: The system shall avoid presenting unsupported statistics when sample size or coverage is insufficient.

### Notifications
- FR-024: Users shall be able to configure price thresholds.
- FR-025: The system shall support intelligence-based alerts where sufficient data exists.
- FR-026: The system shall apply cooldown/deduplication rules to reduce repeated alerts.
- FR-027: Notifications shall explain the condition that triggered the alert.
- FR-028: Telegram shall be implemented before email, with both channels included in MVP scope.

### AI assistant
- FR-029: The assistant shall translate natural-language requests into structured search criteria.
- FR-030: The assistant shall retrieve current offers and historical analytics through approved backend tools.
- FR-031: The assistant shall explain recommendations using returned evidence.
- FR-032: The assistant shall not invent prices, availability, historical observations, or forecasts.
- FR-033: State-changing actions such as creating or modifying tracking requests shall require clear user intent and appropriate authorization.

### Currency
- FR-034: The system shall preserve original fare amount and currency.
- FR-035: The system shall support IDR as the default display currency and user-selectable display currency.
- FR-036: Converted values shall retain the exchange rate and conversion timestamp used.

## 4. Non-functional requirements

- NFR-001: Provider integrations shall be isolated behind adapters so providers can be replaced or supplemented.
- NFR-002: Provider integration and collection jobs shall respect provider quotas, terms, rate limits, caching rules, and data-retention rules.
- NFR-003: Background jobs shall be retryable and designed to avoid duplicate observations or duplicate notifications.
- NFR-004: All persisted timestamps shall use UTC; localization is presentation-only.
- NFR-005: Secrets and API credentials shall be stored outside source control.
- NFR-006: User-specific tracking data shall be access-controlled.
- NFR-007: The application shall provide structured logs with correlation/request IDs for API calls, collection jobs, and notification outcomes, without logging secrets or sensitive user data.
- NFR-008: Critical backend logic shall have automated tests.
- NFR-009: User-facing analytics shall identify insufficient or stale data.
- NFR-010: The application shall be deployable using Docker.
- NFR-011: Core search, analytics, assistant, and worker operations shall meet documented performance budgets (D-019).
- NFR-012: Core user-facing flows shall meet the agreed accessibility target (D-018).
- NFR-013: Personal data shall be minimized, access-controlled, and retained/deleted according to a documented policy (D-012).

## 5. Business rules and data interpretation

- BR-001: A price observation is an immutable record of a fare returned by a source at a particular time.
- BR-002: An itinerary identity must account for material attributes such as segments, dates, carrier, stops, and fare conditions where available.
- BR-003: A price change is comparable only when the compared observations meet the application's itinerary/fare comparability rules.
- BR-004: A missing baggage or fare attribute must be represented as unknown, not assumed.
- BR-005: Historical metrics must show their observation window and sample size.
- BR-006: Recommendations must be qualified when data is sparse, stale, or inconsistent.
- BR-007: Converted display currency must not replace the original fare amount/currency.
- BR-008: A price observed by the application is not a guaranteed bookable price; the user must confirm on the provider/booking site.

## 6. Acceptance criteria examples

- A visitor can search a supported route and see provider-returned offers.
- A registered user can create a route tracking request and later see stored observations.
- Repeated collection creates timestamped observations without overwriting prior records.
- A historical chart can distinguish observations from different providers and currencies or normalize them transparently.
- A deal recommendation includes the current observed price, comparison baseline, sample size/coverage, and confidence context.
- A threshold alert fires once per qualifying event within its cooldown window.
- An AI answer about historical prices is traceable to backend analytics results.
- A provider outage or quota error is visible in logs and does not corrupt historical observations.

## 7. Testing invariants

Tests must protect these invariants:

- Price observations are never silently overwritten.
- Original amount and currency remain unchanged after display conversion.
- A missing fare attribute remains unknown.
- Materially different itineraries are not merged into one historical series.
- Analytics expose observation window and sample size.
- Insufficient or stale data does not produce confident recommendations.
- Provider errors or quota exhaustion do not corrupt stored history.
- User A cannot read or modify User B's private tracking requests.
- AI tool calls cannot bypass service-layer authorization.
- Notification retries do not create duplicate user-visible alerts.

## 8. Verification layers

- **Unit:** fare normalization, currency preservation, itinerary identity, comparability, statistics, deal-score rules, recommendation evidence, alert cooldown/deduplication, authorization, input validation.
- **Integration:** database persistence, append-only observations, migrations, provider-adapter fixtures, worker idempotency/retries/quota handling, notification adapters, API authentication/ownership/error contracts.
- **End-to-end:** discovery → account → tracking → observations → analytics → notification → grounded assistant response.
- **External services:** mock paid providers and notification gateways in normal CI; use synthetic fixtures; keep separately triggered sandbox/contract tests only where provider terms permit.
- **Failure cases:** timeout, malformed response, authentication failure, quota exhaustion, transient provider error, duplicate delivery, stale data.

Never call a paid flight provider in ordinary unit-test runs. Report skipped tests and failures honestly.
