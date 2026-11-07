# Repository-wide Agent Instructions

## Project context

This repository implements fair2fly, a flight price intelligence platform. Its differentiator is persistent, structured flight-price history and evidence-based analysis.

## Source of truth

- Product scope and requirements: `docs/PRD.md`
- Testable requirements and invariants: `docs/SRS.md`
- Architecture and technical decisions: `docs/TECHNICAL_DESIGN.md`
- Milestones: `docs/ROADMAP.md`
- Implementation backlog: GitHub Issues (D-026)
- Open and resolved decisions: `docs/DECISIONS.md`
- Development workflow: `docs/WORKFLOW.md`
- API contracts: generated OpenAPI and `docs/API.md` once implemented; until then, `docs/TECHNICAL_DESIGN.md` §9

If sources conflict, stop and report the conflict. Do not silently choose one. The product owner approves scope changes and unresolved product decisions. Do not reopen an accepted decision in code or in an issue; change it in `docs/DECISIONS.md` first, with the product owner's approval.

## Required context

1. Always read this file.
2. Read the approved task packet and the spec or requirement sections it references.
3. Open only the referenced sections of other documents. Do not load every document by default.
4. For non-trivial work, read `docs/WORKFLOW.md` for handoffs, loop limits, and routing.

## Commands

Run all commands from the repository root. Prerequisites and pinned versions are documented in `README.md`.

- Install: `make install`
- Development: `make dev`
- Test: `make test`
- Lint and format check: `make lint`
- Type-check: `make typecheck`

`make dev` reads `API_PORT` and `WEB_PORT` from `.env`; copy `.env.example` to `.env` to change the defaults (8000 and 3000). Each git worktree needs its own `.env` with free ports.

The migration command is added by T-004 (issue #4) and the end-to-end test command by T-025 (issue #25). Do not guess either command until then.

## Core rules

1. Treat the specifications as the source of truth. Do not silently invent product requirements.
2. If a requirement is ambiguous or conflicts with the specs, identify the conflict and ask or document an explicit proposal.
3. Keep provider-specific code behind an adapter. Do not leak provider response shapes into domain services.
4. Price observations are immutable. Never overwrite historical observations with the latest price.
5. Preserve original fare amount and currency. Display conversion must retain its exchange-rate source and timestamp.
6. Do not compare materially different itineraries or fare products as if they were identical.
7. Missing baggage, fare-family, or other provider attributes mean `unknown`, not false or free.
8. Analytics, deal scores, and booking guidance must be deterministic, testable, explainable, and versioned.
9. Expose sample size, observation window, freshness, and coverage. Suppress or qualify statistics when data is insufficient.
10. LLM output must be grounded in backend tool results. Never fabricate fares, availability, historical observations, or forecasts.
11. Enforce user ownership and authorization for private tracking data and state-changing operations.
12. Respect provider terms, quotas, rate limits, caching, and data-retention rules.
13. Do not claim a price is guaranteed bookable. Users must confirm it with the booking provider.
14. Keep the product's MVP AI assistant single-agent. Development-time agent roles do not change product scope.
15. Add tests for business logic, edge cases, and failure modes. Do not mark a task complete without running relevant checks and reporting results. Name tests after the acceptance criteria and requirement IDs they cover (for example `AC-2`, `FR-014`) so QA can trace evidence.
16. Keep secrets out of source control, prompts, and logs.

## Engineering preferences

- Prefer a modular monolith over premature microservices.
- Use explicit types and validation at boundaries.
- Make background jobs idempotent, retry-safe, and observable.
- Use UTC for persisted timestamps; localize only for presentation.
- Keep migrations versioned and reviewable.
- Use structured logs with correlation/request IDs. Never log secrets or sensitive user data.
- Avoid unnecessary dependencies and abstractions.
- Do not introduce ML forecasting into the MVP unless the product owner explicitly changes scope.

## Running commands

- Wait for slow commands (test suites, builds, a container coming back) inside the command: run it in the foreground, or poll in a loop that ends. Nothing wakes an agent that has stopped, so "I will report when it finishes" is where the work ends. If it does not finish within a ceiling you state, report that as a finding.
- Stop only processes you started, by the job id your tool gave you. Never use broad patterns such as `pkill -f pytest`; they kill other agents' runs and leave an aborted suite that looks like a broken branch.
- After restoring a file you changed on purpose, `git status` and `git diff HEAD` must both be empty. `git checkout <commit> -- <path>` stages what it writes, so a later `git checkout -- <path>` can silently leave the old file in place.
- A run that fails in a strange, scattered way is repeated once, alone and clean, before it is believed.
- Work only inside the worktree path you were given. Reading `main` is fine; writing to it or to another worktree is not.
- Before starting a test run, confirm no run is already alive in your worktree (`pgrep -af pytest`). Two suites in one worktree share one test database and drop it under each other.
- A shell variable such as `DATABASE_URL` overrides the worktree's `.env`. Run commands with the worktree's own database named explicitly, and never assume the shell's value is yours. Isolation details are in `docs/WORKFLOW.md` section 10.
- Never delete anything: not files, worktrees, branches, or databases. A command that destroys something stops the run until a human approves it. Restore with `git checkout -- <path>`, and put scratch files outside the repository.

## Implementation workflow

1. Read the task packet, spec, acceptance criteria, and relevant decisions.
2. Confirm scope, non-goals, dependencies, and required checks. Flag ambiguity before coding.
3. State the intended files/components and implementation approach.
4. Implement the smallest coherent change.
5. Add or update tests and run relevant lint, type, test, and migration checks.
6. Update affected docs, contracts, and decisions.
7. Report changed files, commands/results, acceptance-criteria evidence, limitations, and follow-ups.

## Boundaries

Always:

- Follow the specs and protect the domain invariants above.
- Run relevant checks and report exact results.
- Update docs and contracts when behavior changes.
- Keep changes small and reviewable.

Ask first:

- Product scope or acceptance-criteria changes.
- Data-model, retention, or historical-comparability changes.
- New external costs, providers, or dependencies.
- Authentication, authorization, privacy, or security-sensitive changes.
- Architecture changes with broad impact.
- Destructive or irreversible actions.

Never:

- Overwrite price observations or silently change historical data.
- Fabricate provider data, fares, availability, analytics, or forecasts.
- Bypass authorization or weaken tests merely to obtain a passing result.
- Commit secrets or credentials.
- Add multi-agent orchestration to the product MVP.
- Claim a fare is guaranteed bookable.

## Definition of Done

A task is complete only when:

- Acceptance criteria are met and mapped to evidence.
- Relevant tests/checks pass, or failures are explicitly documented.
- Edge cases, security, authorization, provider constraints, and data integrity are considered.
- API/domain/design/decision docs and tracker (issue) status are updated.
- QA has independently reviewed non-trivial work.
- The implementation report (an issue comment) includes changed files, commands/results, AC evidence, known limitations, and follow-up issues.

See `docs/WORKFLOW.md` for the task lifecycle, loop limits, and handoff formats.
