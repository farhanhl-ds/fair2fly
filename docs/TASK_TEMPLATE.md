# [TASK-ID] — [Short, action-oriented title]

**Spec:** [link to feature spec, PRD section, or SRS requirement]  
**Requirement references:** FR-xxx / NFR-xxx / BR-xxx  
**Dependencies:**  
**Risk:** Low / Medium / High

## Goal

What outcome should this task produce, and why does it matter?

## Context

Relevant product/technical context. Link to specific sections and files; do not paste the entire specification.

## Definition of Ready

- [ ] Scope and non-goals are explicit.
- [ ] Acceptance criteria are observable and testable.
- [ ] Dependencies and related decisions are resolved.
- [ ] Test plan maps each acceptance criterion to a check.
- [ ] Relevant specs, docs, and contracts are linked.
- [ ] Security, authorization, and data-integrity impact are identified.

## Scope

### In scope

-

### Out of scope

-

## Acceptance criteria

Use stable IDs so QA and tests can reference them.

- **AC-1:** Given [context], when [action], then [observable result].
- **AC-2:**
- **AC-3:**

## Must not change

List existing behavior, contracts, data, or invariants that this task must preserve.

-

## Test plan

Name each test after the AC it covers (for example include `AC-1` in the test name).

| AC | Test type | Command/check |
|---|---|---|
| AC-1 | Unit / integration / API / UI / E2E |  |
| AC-2 |  |  |

Failure and edge cases:

-

## Implementation notes

Constraints, expected modules/interfaces, migration considerations, or known alternatives. Avoid prescribing implementation details unless required.

## Security and data impact

- Authorization/ownership:
- Secrets or sensitive data:
- Data retention or historical comparability:
- Provider terms/quotas:

## Risks and assumptions

-

---

This body is the spec written by the PM. Engineer and QA do not edit it; they post their evidence as issue comments (formats in `team/engineer.md` and `team/qa.md`). Status lives in labels, not here.
