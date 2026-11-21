# Tasks — 19 Non-functional & Analytics

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-19-01 | Performance budgets in CI (Lighthouse CI, bundle-size check) | T-20-02 | S | Todo |
| T-19-02 | OpenTelemetry instrumentation + dashboards + alerts | T-20-03 | M | Todo |
| T-19-03 | i18n framework + string extraction | T-16-02 | S | Todo |
| T-19-04 | Analytics pipeline: SDK, consent, event schema, funnels, KPI views | T-16-03 | M | Todo |
| T-19-05 | Accessibility automated checks in CI + manual audit | T-01-08 | M | Todo |
| T-19-06 | Load test plan & execution at 2× peak | T-21-05 | M | Todo |
| T-19-07 | Cross-browser/device test matrix run | M5 | S | Todo |

---

### T-19-01 — Perf budgets
- **Done when:** PRs fail if LCP budget or bundle limits exceeded on key routes.

### T-19-02 — Observability
- **Done when:** Trace for a checkout spans web → API → DB → queue → notification worker; alerts in §6 configured and test-fired.

### T-19-03 — i18n
- **Done when:** No hard-coded UI strings (lint rule); pseudo-locale renders correctly.

### T-19-04 — Analytics
- **Done when:** All §7 events fire with schema validation; funnels and KPI dashboard built.

### T-19-05 — Accessibility
- **Done when:** axe in Playwright on key pages; manual screen-reader test (TalkBack, VoiceOver) of checkout.

### T-19-06 — Load test
- **Done when:** k6 scenario (browse 70%, search 20%, checkout 10%) passes at 600 RPS peak with targets met.

### T-19-07 — Device matrix
- **Done when:** Smoke suite passes on all §5 browsers.
