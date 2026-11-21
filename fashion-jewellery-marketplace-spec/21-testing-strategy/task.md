# Tasks — 21 Testing Strategy

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-21-01 | Test frameworks set up in monorepo (unit, integration with Testcontainers) | T-16-02 | S | Todo |
| T-21-02 | Playwright project + page objects + CI integration (preview & staging) | T-20-05 | M | Todo |
| T-21-03 | Critical journeys 1–6 automated | T-21-02, M4 | L | Todo |
| T-21-04 | Time-travel clock + test hooks (staging only, disabled in prod) | T-12-03 | S | Todo |
| T-21-05 | k6 load scripts | T-04-04, T-06-05 | M | Todo |
| T-21-06 | Visual regression + accessibility checks in CI | T-21-02 | S | Todo |
| T-21-07 | UAT plan with pilot vendors/customers + feedback form | M5 | S | Todo |
| T-21-08 | Defect workflow + severity labels in issue tracker | — | S | Todo |

---

### T-21-01 — Frameworks
- **Done when:** `pnpm test` runs unit + integration; coverage reported.

### T-21-02 — Playwright
- **Done when:** Runs against any env via `BASE_URL`; traces/videos on failure.

### T-21-03 — Critical journeys
- **Done when:** All 6 automated, green in staging, < 15 min total.

### T-21-04 — Test clock
- **Done when:** Only enabled when `ENV=staging|dev`; startup fails if enabled in prod.

### T-21-05 — Load scripts
- **Done when:** Scenario mix per 19; parameterised RPS.

### T-21-06 — Visual & a11y
- **Done when:** Baselines stored; diffs require approval.

### T-21-07 — UAT
- **Done when:** UAT scripts for vendors and customers; feedback form; schedule agreed.

### T-21-08 — Defects
- **Done when:** Labels Sev1–4; Sev1 auto-pages on-call.
