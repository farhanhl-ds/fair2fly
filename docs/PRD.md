# Product Requirements Document (PRD)

**Status:** Initial baseline. Decision state: [`DECISIONS.md`](DECISIONS.md).  
**Last updated:** 2026-11-05  
**Open decisions:** [`DECISIONS.md`](DECISIONS.md)  
**Related:** [`SRS.md`](SRS.md), [`TECHNICAL_DESIGN.md`](TECHNICAL_DESIGN.md), [`ROADMAP.md`](ROADMAP.md)

## 1. Product summary

**Product name:** Fair2fly

A public flight-deal discovery and price-intelligence platform focused initially on flights departing from Indonesia. It continuously collects flight-price observations, builds historical context, identifies attractive opportunities, and helps travelers decide whether to book, wait, or keep monitoring.

The product combines:
- Public flight discovery and market insights.
- Personalized tracking for registered users.
- Historical price analytics and deal scoring.
- An AI assistant that explains evidence and operates application tools.

## 2. Problem statement

Most flight-search experiences emphasize prices available at the moment of search. A traveler often cannot tell whether a displayed fare is unusually attractive, how it compares with previous observations, or whether waiting is reasonable.

This product aims to close that gap by maintaining a longitudinal dataset of flight prices and turning it into useful, explainable intelligence.

## 3. Product differentiation

The core asset is a persistent, structured dataset of flight-price observations. A generic LLM may help search or explain information, but this application can analyze its own accumulated observations over time.

The AI assistant is an interface to deterministic search and analytics services. It must not invent fares, historical observations, or unsupported predictions.

## 4. Target users

- Travelers who are flexible about destination or travel dates and want to find good-value trips.
- Travelers who know a route or itinerary and want to monitor its price.
- Returning users who want evidence-based booking guidance.

## 5. Geographic and market scope

### MVP
- Flights departing from Indonesian airports.
- Begin with a curated set of major Indonesian airport hubs: CGK, DPS, SUB, KNO, JOG, UPG, BDO.
- Airport coverage must be configurable and expandable.
- Support domestic and international destinations.
- Economy cabin only.
- One-way and round-trip journeys.

### Future
- User-defined origin airports beyond the initial curated set.
- Additional cabin classes.
- Multi-city journeys.
- Global origins and destinations.

**Decision:** see D-002 in [`DECISIONS.md`](DECISIONS.md). The list is seed-configurable, so expansion does not require a PRD change.

## 6. Core user experiences

### 6.1 Public visitor
1. Arrives at an Explore-first homepage.
2. Sees trending deals, notable price drops, and market insights.
3. Searches by route or explores destinations using budget and flexible dates.
4. Reviews flight results and available historical context.
5. Opens an itinerary to inspect price history and fare attributes.
6. Registers to save searches, create tracking requests, and receive alerts.

### 6.2 Registered user
1. Configures preferred origins, destinations, budget, currency, and travel preferences.
2. Creates route, specific-itinerary, or flexible-destination tracking requests.
3. Receives scheduled price monitoring.
4. Reviews price history and deal scores.
5. Receives threshold-based or intelligence-based notifications.
6. Consults the AI assistant for evidence-based analysis and recommendations.

### 6.3 AI assistant
Users can express travel needs conversationally. The assistant translates requests into structured application operations, invokes search and analytics tools, and explains results with their supporting evidence.

## 7. Discovery and search

The product supports:
- **Route-level discovery:** Explore fares and market movements for an origin-destination pair.
- **Flexible destination discovery:** Search from an origin using budget, date window, trip duration, and destination preferences.
- **Specific itinerary search:** Inspect a particular flight combination.
- **Fixed dates and flexible dates.**
- **One-way and round-trip journeys.**

The homepage combines search with public deal and market-insight content. Public visitors should be able to understand the product's value without registering.

## 8. Tracking modes

All three modes are in scope, implemented progressively:

1. **Route tracking:** Monitor opportunities across available itineraries on an origin-destination route.
2. **Specific itinerary tracking:** Monitor a particular flight combination and departure date.
3. **Flexible destination tracking:** Monitor a set of destinations matching a user's search criteria.

Flexible destination monitoring may consume significantly more provider requests; it must be quota-aware and subject to scheduling limits.

## 9. Price intelligence

### MVP: statistical intelligence
- Historical minimum, maximum, mean, and median where sample size permits.
- Current price compared with historical statistics.
- Historical percentile where sufficient observations exist.
- Percentage deviation from a selected baseline.
- Transparent, rule-based deal score.
- Data coverage and confidence indicators.

### Later phases
- Booking-window analysis.
- Seasonal analysis.
- Price anomaly detection enhancements.
- Forecasting and predictive recommendations.
- Broader route and market intelligence.

Do not present forecasts as reliable until data volume, coverage, and evaluation demonstrate that they are useful.

## 10. Deal scoring and booking recommendations

The deal score combines signals such as:
- User budget or price ceiling.
- Current fare relative to historical observations.
- Price movement.
- Data coverage and reliability.

MVP recommendations use three actions:
- **Consider booking**
- **Wait**
- **Keep monitoring**

Every recommendation must show supporting evidence, such as current fare versus historical median, percentile, observation coverage, and confidence. It must communicate uncertainty and must not imply guaranteed future price movement.

Initial scoring should be deterministic and explainable, not an opaque ML model.

## 11. Flight comparison

Comparisons must account for meaningful itinerary and fare attributes, including:
- Airline and flight segments.
- Direct or connecting itinerary and number of stops.
- Departure and arrival times.
- Total duration.
- Cabin class.
- Baggage and fare conditions when supplied by the provider.

Users should be able to understand trade-offs. Historical comparisons must avoid treating materially different itineraries or fare products as identical.

## 12. Notifications

MVP supports:
- User-defined price threshold alerts.
- Intelligence-based alerts, such as an attractive historical percentile.
- Significant price-drop alerts where supported by reliable observations.
- Cooldown periods to prevent repeated notifications.
- A short explanation of why each alert triggered.

Channels:
- Telegram first.
- Email also in MVP, implemented after the initial Telegram workflow.

## 13. AI assistant

MVP capabilities:
- Natural-language flight discovery.
- Convert conversational requests into structured search criteria.
- Retrieve historical price analytics.
- Explain deal scores and booking recommendations.
- Create or manage monitoring requests through explicit user intent and authorization.

Architecture principle:
- Deterministic backend services own data retrieval, calculations, scheduling, and state changes.
- The LLM interprets requests, selects approved tools, and explains grounded results.
- AI must not fabricate prices, routes, availability, or historical statistics.

A single tool-calling agent is sufficient initially. Multi-agent orchestration is out of scope for MVP.

## 14. Data acquisition and currency

- Use a flight-search API as the initial primary source.
- Supplement only with additional sources whose access and use are permitted.
- Begin with one provider integration; keep the provider adapter replaceable.
- Store every valid price observation rather than overwriting the previous price.
- Use scheduled adaptive monitoring plus search-triggered collection where provider terms and quotas allow.
- Preserve provider identity, observation timestamp, original amount, and original currency.
- Display IDR by default and allow a user-selected display currency.
- Store the exchange rate and conversion timestamp used for converted display values.

**Decision:** the MVP fare source is recorded in D-001 ([`DECISIONS.md`](DECISIONS.md)) and sits behind a replaceable adapter (NFR-001). Constraints that hold regardless of provider: collection is budgeted per plan tier (D-004), provider attribution is preserved, original amount and currency are preserved, and missing fare attributes stay `unknown` (BR-004).

## 15. Booking boundary

The product provides outbound links to airlines or online travel agencies where available. Booking, payment, ticket issuance, and booking management are out of scope.

## 16. MVP scope

Included:
- Public Explore-first homepage with search.
- Public deals and basic market insights.
- User accounts and personalized preferences.
- One-way and round-trip economy search.
- Fixed and flexible date search.
- Route, itinerary, and flexible-destination tracking (progressive rollout).
- One flight-data API integration.
- Price normalization and persistent observations.
- Scheduled monitoring.
- Historical charts and statistical analytics.
- Explainable rule-based deal scoring.
- Evidence-based booking recommendations.
- Telegram and email notifications.
- AI assistant with backend tool calling.
- Booking redirection.
- Multi-currency display with original fare preservation.
- Docker-based deployment, tests, and documentation.

Excluded from MVP:
- In-app booking or payment.
- Multi-city journeys.
- Non-economy cabin classes.
- ML-based price forecasting.
- Autonomous multi-agent system.
- Guaranteed predictions or claims of guaranteed savings.

## 17. Success measures

Engineering and product measures:
- Valid price observations collected and retained.
- Coverage and freshness of tracked routes/itineraries.
- Search success and provider error rates.
- Percentage of recommendations with sufficient supporting data.
- Deal-score usefulness, evaluated against historical outcomes and user feedback.
- Notification delivery success and duplicate-alert rate.
- User ability to discover, save, and track a relevant opportunity.

Targets should be set after provider selection and baseline measurement rather than invented now.

## 18. Timeline and budget

Target delivery: 4–6 weeks.

Budget approach: prioritize free tiers and open-source infrastructure, with a modest budget where necessary for reliable flight-data access or deployment.

## 19. Risks and assumptions

- Provider coverage for Indonesian airports may vary.
- API terms may constrain polling, caching, redistribution, and historical storage.
- Sparse observations can make historical statistics misleading.
- Prices may differ due to baggage, fare family, taxes, availability, and point of sale.
- Flexible destination monitoring can consume substantial API quota.
- Exchange-rate movements can distort comparisons if original currency is not preserved.
- Flight prices can change between observation and booking.

## 20. Open decisions before implementation

Open product, provider, and platform decisions are tracked centrally in [`DECISIONS.md`](DECISIONS.md). A decision blocks only the tasks in its *Affects* column: resolve it before the first of those tasks starts, and record the outcome there with rationale and consequences.
