# 21 — Testing Strategy

**Phase:** P0–P1 · **Depends on:** 16, 20 · **Status:** Draft

## 1. Purpose
Define how we test so every `validate.md` can be executed consistently and most of it automatically.

## 2. Test pyramid
| Layer | Tooling | Scope | Gate |
|---|---|---|---|
| Unit | Vitest/Jest | Pure logic: amount calculator, state machine, ranking, validators | PR |
| Integration | Testcontainers (Postgres, Redis) | Repositories, RLS, outbox, webhooks | PR |
| Contract | OpenAPI schema tests; provider contract tests (payment fake vs sandbox) | API & gateway | PR / nightly |
| E2E | Playwright | Critical journeys (§3) on preview/staging | PR smoke, staging full |
| Visual regression | Playwright screenshots / Chromatic | Components & key pages | PR |
| Accessibility | axe-core in Playwright | Key pages | PR |
| Performance | Lighthouse CI, k6 | Budgets, load | PR (LH), pre-release (k6) |
| Security | ZAP baseline, SAST, deps | API & web | Nightly / PR |
| Property-based | fast-check | Ledger invariants, state machine | PR |
| UAT | Pilot vendors & customers | Real usage | Pre-launch |

## 3. Critical journeys (must always pass before any prod deploy)
1. Guest → search "jhumka" → PDP → add → login OTP → checkout with items from 2 vendors → pay (sandbox) → confirmation.
2. Vendor receives alert → accepts → dispatches with tracking → customer sees tracking.
3. Delivery confirmed → return window ends → T2 released; ledger balanced.
4. Customer claims damage → vendor accepts → refund → ledger balanced.
5. New vendor onboarding → admin approval → store live → product searchable.
6. Admin suspends vendor → products disappear from search.

## 4. Test data
Deterministic seed (T-17-05); gateway sandbox; test phone numbers for OTP; fake tracking webhooks; time-travel helper (`/test/clock` endpoint, staging only) for timer validations.

## 5. Defect severity
| Sev | Definition | Release rule |
|---|---|---|
| 1 | Money wrong, data leak, checkout down | Blocks release; hotfix |
| 2 | Core journey broken for some users | Blocks release |
| 3 | Non-core bug with workaround | Fix within sprint |
| 4 | Cosmetic | Backlog |

## 6. Validation workflow
Developer finishes task → runs automated parts → QA executes `validate.md` in staging → records result in module table + `TRACKER.md` → Product owner signs module.
